#!/usr/bin/env python3
"""Search-19 contact-state DP/beam engine.

Takes search-17 64/64 line-set scaffolds and search-18 diagnostic failures,
then builds a real ordered 22-link chain while explicitly scoring contact loss:
full scaffold line mask -> chosen ordered piece mask -> lost grid points.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import multiprocessing as mp
import random
import time
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Sequence, Tuple

import order_from_cover64_stitch as base

Point = Tuple[int, int, int]
Line = Tuple[Point, Point]
SCALE = base.SCALE
GRID = base.GRID
GRID_INDEX = base.GRID_INDEX
OFFICIAL60_MISSING: List[Point] = [
    (0, 0, SCALE),
    (0, 2 * SCALE, 3 * SCALE),
    (0, 3 * SCALE, SCALE),
    (2 * SCALE, SCALE, SCALE),
]
OFFICIAL60_MASK = sum(1 << GRID_INDEX[p] for p in OFFICIAL60_MISSING)


@dataclass(frozen=True)
class Piece:
    line_index: int
    entry: Point
    exit: Point
    piece_mask: int
    full_mask: int
    lost_mask: int
    gain: int
    lost: int
    full: int
    weak: int
    preserves_rich: int
    old_hits: int


@dataclass
class State:
    score: int
    used_mask: int
    current: Point
    vertices: Tuple[Point, ...]
    order: Tuple[int, ...]
    covered_mask: int
    weak_links: int
    total_lost: int
    clipped_rich: int
    preserved_rich: int


def vertices_key(vertices: Sequence[Point]) -> str:
    payload = json.dumps([list(v) for v in vertices], separators=(",", ":"))
    return hashlib.sha256(payload.encode()).hexdigest()


def mask_points(mask: int) -> list:
    return [base.unscale_point(p) for p in GRID if (mask >> GRID_INDEX[p]) & 1]


def load_all_scaffolds(args: argparse.Namespace) -> list[dict]:
    rows: list[dict] = []
    seen: set[str] = set()

    def add(row: dict, source_file: str, source_kind: str) -> None:
        if not isinstance(row, dict) or not (row.get("line_set2") or row.get("line_set")):
            return
        try:
            lines = base.load_lines(row)
        except Exception:
            return
        if len(lines) != 22:
            return
        key = base.line_key(lines)
        if key in seen:
            return
        seen.add(key)
        d = dict(row)
        d.setdefault("candidate_id", Path(source_file).stem)
        d["_source_file"] = source_file
        d["_source_kind"] = source_kind
        d["_line_key"] = key
        rows.append(d)

    for p in args.input_json + args.diagnostic_json:
        if not p.exists():
            continue
        d = json.loads(p.read_text(encoding="utf-8"))
        add(d, str(p), "diagnostic_json" if p in args.diagnostic_json else "search17_json")
    for p in args.input_jsonl + args.diagnostic_jsonl:
        if not p.exists():
            continue
        kind = "diagnostic_jsonl" if p in args.diagnostic_jsonl else "search17_jsonl"
        for raw in p.read_text(encoding="utf-8").splitlines():
            if raw.strip():
                add(json.loads(raw), str(p), kind)
    rows.sort(key=scaffold_sort_key, reverse=True)
    return rows[: max(1, args.candidate_scaffolds)]


def scaffold_sort_key(sc: dict) -> tuple:
    lines = base.load_lines(sc)
    union = 0
    rich4 = 0
    rich3 = 0
    for line in lines:
        m = base.mask_for_segment(*line)
        union |= m
        rich4 += int(m.bit_count() >= 4)
        rich3 += int(m.bit_count() >= 3)
    return (
        int(sc.get("stitch_path_lower_bound", 0) or 0),
        int(sc.get("covered_count", 0) or 0),
        union.bit_count(),
        rich4,
        rich3,
    )


def mode_for_shard(shard: int) -> str:
    if 0 <= shard <= 3:
        return "exact_top4_dp"
    if 4 <= shard <= 7:
        return "wide_beam_contact_state"
    if 8 <= shard <= 11:
        return "loss_minimizing"
    if 12 <= shard <= 15:
        return "official60_aware"
    if 16 <= shard <= 17:
        return "controlled_bridge_replacement"
    if shard == 18:
        return "diagnostic_replay"
    return "conservative_control"


def weights(mode: str) -> dict[str, int]:
    w = {"cov": 1_000_000, "used": 8_000, "gain": 2_000, "lost": 25_000,
         "weak": 90_000, "rich_keep": 35_000, "rich_clip": 45_000, "old": 60_000, "future": 37}
    if mode == "loss_minimizing":
        w.update({"lost": 65_000, "rich_keep": 75_000, "rich_clip": 90_000})
    elif mode == "official60_aware":
        w.update({"old": 180_000})
    elif mode == "wide_beam_contact_state":
        w.update({"lost": 18_000, "gain": 4_000})
    elif mode == "exact_top4_dp":
        w.update({"lost": 40_000, "rich_keep": 60_000})
    elif mode == "diagnostic_replay":
        w.update({"lost": 80_000, "rich_clip": 95_000})
    return w


def score_state(mask: int, used: int, piece: Piece, weak: int, lost: int, clipped: int, kept: int, future: int, mode: str) -> int:
    w = weights(mode)
    old_hits = (mask & OFFICIAL60_MASK).bit_count()
    return (
        mask.bit_count() * w["cov"]
        + used * w["used"]
        + piece.gain * w["gain"]
        + future * w["future"]
        + kept * w["rich_keep"]
        + old_hits * w["old"]
        - lost * w["lost"]
        - weak * w["weak"]
        - clipped * w["rich_clip"]
    )


def prepare_contact_data(lines: Sequence[Line], min_piece_cover: int) -> dict:
    n = len(lines)
    full_masks = [base.mask_for_segment(*line) for line in lines]
    candidates: list[set[Point]] = [set() for _ in lines]
    # Contact candidates are exact integer-scaled points only: endpoints and grid/intersection points.
    # This avoids float geometry and matches check_ordered_trail_scaled.py output format.
    all_probe_points = set(GRID)
    for a, b in lines:
        all_probe_points.add(a)
        all_probe_points.add(b)
    for i, (a, b) in enumerate(lines):
        candidates[i].add(a)
        candidates[i].add(b)
        for p in all_probe_points:
            if base.on_segment(a, b, p):
                candidates[i].add(p)
    integer_contacts = 0
    for i in range(n):
        for j in range(i + 1, n):
            shared = candidates[i].intersection(candidates[j])
            integer_contacts += len(shared)
    cand_lists = [sorted(c) for c in candidates]

    future_degree: list[dict[Point, int]] = []
    for i in range(n):
        d: dict[Point, int] = {}
        for p in cand_lists[i]:
            d[p] = sum(1 for j in range(n) if j != i and base.on_segment(lines[j][0], lines[j][1], p))
        future_degree.append(d)

    pieces: list[dict[tuple[Point, Point], Piece]] = []
    for i, pts in enumerate(cand_lists):
        dct: dict[tuple[Point, Point], Piece] = {}
        full = full_masks[i]
        full_count = full.bit_count()
        for a in pts:
            for b in pts:
                if a == b:
                    continue
                pm = base.mask_for_segment(a, b)
                gain = pm.bit_count()
                if gain < min_piece_cover:
                    continue
                lost = full & ~pm
                lost_count = lost.bit_count()
                dct[(a, b)] = Piece(
                    i, a, b, pm, full, lost, gain, lost_count, full_count,
                    1 if gain <= 1 else 0,
                    1 if full_count >= 4 and lost_count == 0 else 0,
                    (pm & OFFICIAL60_MASK).bit_count(),
                )
        pieces.append(dct)
    return {"candidates": cand_lists, "future_degree": future_degree, "pieces": pieces, "integer_contacts": integer_contacts}


def choose(states: list[State], limit: int) -> list[State]:
    states.sort(key=lambda s: (len(s.order), s.covered_mask.bit_count(), -s.total_lost, -s.weak_links, s.score), reverse=True)
    return states[:limit]


def best_chain_for_lines(lines: Sequence[Line], rng: random.Random, mode: str, args: argparse.Namespace, deadline: float) -> dict:
    n = len(lines)
    data = prepare_contact_data(lines, args.min_piece_cover)
    pieces: list[dict[tuple[Point, Point], Piece]] = data["pieces"]
    candidates: list[list[Point]] = data["candidates"]
    future_degree: list[dict[Point, int]] = data["future_degree"]

    start_lines = list(range(n))
    rng.shuffle(start_lines)
    start_lines = start_lines[: max(1, min(n, args.start_limit))]
    beam: list[State] = []
    best: State | None = None

    for i in start_lines:
        starts = list(pieces[i].values())
        starts.sort(key=lambda p: (p.gain, -p.lost, p.preserves_rich, future_degree[i].get(p.exit, 0)), reverse=True)
        for piece in starts[: max(8, args.branch_limit * 3)]:
            clipped = 1 if piece.full >= 4 and piece.lost > 0 else 0
            st = State(
                score_state(piece.piece_mask, 1, piece, piece.weak, piece.lost, clipped, piece.preserves_rich, future_degree[i].get(piece.exit, 0), mode),
                1 << i,
                piece.exit,
                (piece.entry, piece.exit),
                (i,),
                piece.piece_mask,
                piece.weak,
                piece.lost,
                clipped,
                piece.preserves_rich,
            )
            beam.append(st)
            if best is None or result_key_state(st) > result_key_state(best):
                best = st
    beam = choose(beam, args.beam_width)

    while beam and time.time() < deadline:
        if max(len(s.order) for s in beam) >= n:
            break
        nxt: list[State] = []
        for st in beam:
            if len(st.order) >= n:
                nxt.append(st)
                continue
            current = st.current
            next_lines = [j for j in range(n) if not (st.used_mask >> j) & 1 and base.on_segment(lines[j][0], lines[j][1], current)]
            next_lines.sort(key=lambda j: future_degree[j].get(current, 0), reverse=True)
            for j in next_lines[: max(2, args.branch_limit)]:
                outgoing = [p for (entry, _), p in pieces[j].items() if entry == current]
                outgoing.sort(key=lambda p: ((st.covered_mask | p.piece_mask).bit_count(), -p.lost, p.preserves_rich, p.old_hits, p.gain), reverse=True)
                for piece in outgoing[: max(2, args.branch_limit)]:
                    new_mask = st.covered_mask | piece.piece_mask
                    weak = st.weak_links + piece.weak
                    total_lost = st.total_lost + piece.lost
                    clipped = st.clipped_rich + (1 if piece.full >= 4 and piece.lost > 0 else 0)
                    kept = st.preserved_rich + piece.preserves_rich
                    order = st.order + (j,)
                    ns = State(
                        score_state(new_mask, len(order), piece, weak, total_lost, clipped, kept, future_degree[j].get(piece.exit, 0), mode),
                        st.used_mask | (1 << j),
                        piece.exit,
                        st.vertices + (piece.exit,),
                        order,
                        new_mask,
                        weak,
                        total_lost,
                        clipped,
                        kept,
                    )
                    nxt.append(ns)
                    if best is None or result_key_state(ns) > result_key_state(best):
                        best = ns
                    if len(nxt) >= args.state_cap:
                        break
                if len(nxt) >= args.state_cap or time.time() >= deadline:
                    break
            if len(nxt) >= args.state_cap or time.time() >= deadline:
                break
        beam = choose(nxt, min(args.beam_width, args.state_cap))

    if best is None:
        return {"status": "no_chain", "covered_count": 0, "links": 0, "vertices2": [], "line_order": []}
    missing = [base.unscale_point(p) for p in GRID if not (best.covered_mask >> GRID_INDEX[p]) & 1]
    result = {
        "status": "full_length_ordered_chain" if len(best.vertices) == n + 1 else "partial_ordered_chain",
        "coordinate_scale": SCALE,
        "vertices2": [list(v) for v in best.vertices],
        "vertices": [base.unscale_point(v) for v in best.vertices],
        "links": max(0, len(best.vertices) - 1),
        "line_order": list(best.order),
        "covered_count": best.covered_mask.bit_count(),
        "missing_count": len(missing),
        "missing": missing,
        "weak_links": best.weak_links,
        "score": best.score,
        "contact_state_metrics": {
            "total_lost_points_over_pieces": best.total_lost,
            "clipped_rich_lines": best.clipped_rich,
            "preserved_rich_lines": best.preserved_rich,
            "official60_missing_hits": (best.covered_mask & OFFICIAL60_MASK).bit_count(),
            "integer_contact_points_seen": data["integer_contacts"],
        },
    }
    result["line_loss_table"] = build_line_loss_table(lines, best.order, best.vertices)
    result["contact_loss_report"] = build_contact_loss_report(result["line_loss_table"])
    return result


def result_key_state(s: State) -> tuple:
    return (len(s.order), s.covered_mask.bit_count(), -s.total_lost, -s.weak_links, s.score)


def result_key(row: dict) -> tuple:
    m = row.get("contact_state_metrics") or {}
    return (int(row.get("links", 0) or 0), int(row.get("covered_count", 0) or 0), -int(m.get("total_lost_points_over_pieces", 999999) or 0), -int(row.get("weak_links", 999) or 999), int(row.get("score", 0) or 0))


def build_line_loss_table(lines: Sequence[Line], order: Sequence[int], vertices: Sequence[Point]) -> list[dict]:
    table = []
    for k, line_idx in enumerate(order):
        if k + 1 >= len(vertices) or line_idx >= len(lines):
            continue
        full = base.mask_for_segment(*lines[line_idx])
        piece = base.mask_for_segment(vertices[k], vertices[k + 1])
        lost = full & ~piece
        table.append({
            "link_index": k,
            "line_index": int(line_idx),
            "line2": [list(lines[line_idx][0]), list(lines[line_idx][1])],
            "entry2": list(vertices[k]),
            "exit2": list(vertices[k + 1]),
            "full_line_covered": full.bit_count(),
            "chosen_piece_covered": piece.bit_count(),
            "lost_count": lost.bit_count(),
            "lost_points": mask_points(lost),
            "preserved_full_line": bool(full and lost == 0),
            "rich_line_clipped": bool(full.bit_count() >= 4 and lost.bit_count() > 0),
        })
    return table


def build_contact_loss_report(table: Sequence[dict]) -> dict:
    lost_counter: Counter[tuple] = Counter()
    clipped = []
    for row in table:
        for p in row.get("lost_points", []) or []:
            lost_counter[tuple(p)] += 1
        if row.get("rich_line_clipped"):
            clipped.append(row)
    return {
        "total_lost_points_over_pieces": sum(int(x.get("lost_count", 0) or 0) for x in table),
        "clipped_rich_lines": len(clipped),
        "preserved_full_lines": sum(1 for x in table if x.get("preserved_full_line")),
        "top_lost_points": [{"point": list(p), "count": c} for p, c in lost_counter.most_common(20)],
        "top_clipped_rich_lines": sorted(clipped, key=lambda x: int(x.get("lost_count", 0) or 0), reverse=True)[:20],
    }


def mutate_lines(base_lines: Sequence[Line], universe: Sequence[Line], rng: random.Random, mode: str, max_mutations: int) -> list[Line]:
    lines = list(base_lines)
    if mode in {"exact_top4_dp", "conservative_control", "diagnostic_replay"} or max_mutations <= 0:
        return lines
    count = rng.randint(0, max_mutations)
    if mode == "controlled_bridge_replacement":
        count = rng.randint(1, max(1, max_mutations))
    used = {base.canonical_line(x) for x in lines}
    for _ in range(count):
        pos = rng.randrange(len(lines))
        old_cover = base.mask_for_segment(*lines[pos]).bit_count()
        for _try in range(80):
            cand = universe[rng.randrange(len(universe))]
            cc = base.canonical_line(cand)
            if cc in used:
                continue
            if mode == "controlled_bridge_replacement" and base.mask_for_segment(*cand).bit_count() < old_cover:
                continue
            used.discard(base.canonical_line(lines[pos]))
            lines[pos] = cand
            used.add(cc)
            break
    return lines


def worker_main(payload: tuple) -> dict:
    wid, seed, shard, mode, scaffolds, universe, args_dict = payload
    args = argparse.Namespace(**args_dict)
    rng = random.Random(seed + 1000003 * shard + 10007 * wid)
    deadline = time.time() + max(1, args.seconds)
    attempts = 0
    best: dict | None = None
    if mode == "conservative_control":
        pool = scaffolds[:1]
    elif mode == "diagnostic_replay":
        diag = [s for s in scaffolds if "diagnostic" in str(s.get("_source_kind", ""))]
        pool = diag[:4] if diag else scaffolds[:4]
    else:
        pool = scaffolds[:]
    while time.time() < deadline and pool:
        sc = pool[(attempts + shard + wid) % len(pool)]
        lines = mutate_lines(base.load_lines(sc), universe, rng, mode, args.max_mutations)
        local_deadline = min(deadline, time.time() + max(2.0, args.seconds / 12.0))
        res = best_chain_for_lines(lines, rng, mode, args, local_deadline)
        attempts += 1
        res.update({
            "worker_id": wid,
            "worker_attempts": attempts,
            "mode": mode,
            "source_scaffold_id": sc.get("candidate_id"),
            "source_scaffold_file": sc.get("_source_file"),
            "source_scaffold_kind": sc.get("_source_kind"),
            "line_set2": [[list(a), list(b)] for a, b in lines],
            "line_set_compact_key_sha256": base.line_key(lines),
        })
        if best is None or result_key(res) > result_key(best):
            best = res
        if best.get("links") == 22 and best.get("covered_count") == 64:
            break
    return best or {"status": "no_result", "covered_count": 0, "links": 0, "vertices2": [], "line_order": []}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input-json", action="append", default=[], type=Path)
    ap.add_argument("--input-jsonl", action="append", default=[], type=Path)
    ap.add_argument("--diagnostic-json", action="append", default=[], type=Path)
    ap.add_argument("--diagnostic-jsonl", action="append", default=[], type=Path)
    ap.add_argument("--seconds", type=int, default=180)
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--seed", type=int, default=20260719)
    ap.add_argument("--shard", type=int, default=0)
    ap.add_argument("--shards", type=int, default=20)
    ap.add_argument("--beam-width", type=int, default=2048)
    ap.add_argument("--branch-limit", type=int, default=6)
    ap.add_argument("--start-limit", type=int, default=22)
    ap.add_argument("--state-cap", type=int, default=200000)
    ap.add_argument("--candidate-scaffolds", type=int, default=4)
    ap.add_argument("--max-mutations", type=int, default=1)
    ap.add_argument("--box-min", type=int, default=-1)
    ap.add_argument("--box-max", type=int, default=4)
    ap.add_argument("--candidate-lines", type=int, default=3000)
    ap.add_argument("--min-piece-cover", type=int, default=1)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--preferred-out", type=Path, default=None)
    ap.add_argument("--loss-report-out", type=Path, default=None)
    args = ap.parse_args()

    scaffolds = load_all_scaffolds(args)
    if not scaffolds:
        raise SystemExit("no input scaffolds found")
    mode = mode_for_shard(args.shard)
    universe = base.generate_line_universe(scaffolds, args.box_min, args.box_max, max(1, args.min_piece_cover), args.candidate_lines, args.seed + args.shard)
    args_dict = vars(args).copy()
    for k in ["input_json", "input_jsonl", "diagnostic_json", "diagnostic_jsonl", "out", "preferred_out", "loss_report_out"]:
        args_dict.pop(k, None)
    payloads = [(wid, args.seed, args.shard, mode, scaffolds, universe, args_dict) for wid in range(max(1, args.workers))]
    if args.workers <= 1:
        worker_results = [worker_main(payloads[0])]
    else:
        with mp.Pool(processes=args.workers) as pool:
            worker_results = pool.map(worker_main, payloads)
    result = dict(max(worker_results, key=result_key))
    result.update({
        "schema": "contact-state-dp-result-v1",
        "source_workflow": "smart-search-19-contact-state-dp",
        "source_shard": args.shard,
        "source_artifact": f"contact-state-dp-22-shard-{args.shard}",
        "parameters": {
            "seconds": args.seconds,
            "workers": args.workers,
            "seed": args.seed,
            "shard": args.shard,
            "shards": args.shards,
            "beam_width": args.beam_width,
            "branch_limit": args.branch_limit,
            "start_limit": args.start_limit,
            "state_cap": args.state_cap,
            "candidate_scaffolds": args.candidate_scaffolds,
            "max_mutations": args.max_mutations,
            "box_min": args.box_min,
            "box_max": args.box_max,
            "candidate_lines": args.candidate_lines,
            "min_piece_cover": args.min_piece_cover,
        },
        "worker_results": [
            {"worker_id": r.get("worker_id"), "links": r.get("links"), "covered_count": r.get("covered_count"), "mode": r.get("mode"), "worker_attempts": r.get("worker_attempts"), "contact_state_metrics": r.get("contact_state_metrics")}
            for r in worker_results
        ],
    })
    if result.get("vertices2"):
        result["candidate_id"] = "mlct22-contactdp-" + vertices_key([tuple(v) for v in result["vertices2"]])[:16]
    else:
        result["candidate_id"] = f"mlct22-contactdp-no-result-shard-{args.shard}"
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2, sort_keys=True), encoding="utf-8")
    if args.preferred_out:
        args.preferred_out.parent.mkdir(parents=True, exist_ok=True)
        args.preferred_out.write_text(json.dumps(result, sort_keys=True) + "\n", encoding="utf-8")
    if args.loss_report_out:
        args.loss_report_out.parent.mkdir(parents=True, exist_ok=True)
        args.loss_report_out.write_text(json.dumps({
            "candidate_id": result.get("candidate_id"),
            "source_shard": args.shard,
            "mode": mode,
            "covered_count": result.get("covered_count"),
            "links": result.get("links"),
            "contact_state_metrics": result.get("contact_state_metrics"),
            "contact_loss_report": result.get("contact_loss_report"),
            "line_loss_table": result.get("line_loss_table"),
        }, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps({"candidate_id": result["candidate_id"], "mode": mode, "links": result.get("links"), "covered_count": result.get("covered_count"), "out": str(args.out)}, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
