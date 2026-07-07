#!/usr/bin/env python3
"""Contact-aware ordering from cover64 stitch scaffolds.

This is the search-18 engine.  It takes unordered 22-line scaffolds from
search-17 and tries to turn them into an actual ordered polygonal chain.

The key difference from the search-17 stitch graph is that every transition
now has a concrete contact point.  If a line is entered and exited through
badly placed contacts, the usable segment can lose many grid points.  The
engine therefore scores the actual covered grid points of the produced
vertices2 chain, not only unordered line-set coverage.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import multiprocessing as mp
import random
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Sequence, Tuple

Point = Tuple[int, int, int]
Line = Tuple[Point, Point]

SCALE = 2
GRID: List[Point] = [(SCALE*x, SCALE*y, SCALE*z) for x in range(4) for y in range(4) for z in range(4)]
GRID_INDEX = {p: i for i, p in enumerate(GRID)}


def sub(a: Point, b: Point) -> Point:
    return (a[0]-b[0], a[1]-b[1], a[2]-b[2])


def dot(a: Point, b: Point) -> int:
    return a[0]*b[0] + a[1]*b[1] + a[2]*b[2]


def cross(a: Point, b: Point) -> Point:
    return (
        a[1]*b[2] - a[2]*b[1],
        a[2]*b[0] - a[0]*b[2],
        a[0]*b[1] - a[1]*b[0],
    )


def on_segment(a: Point, b: Point, p: Point) -> bool:
    d = sub(b, a)
    if d == (0, 0, 0):
        return p == a
    ap = sub(p, a)
    return cross(d, ap) == (0, 0, 0) and 0 <= dot(ap, d) <= dot(d, d)


def mask_for_segment(a: Point, b: Point) -> int:
    if a == b:
        return 0
    m = 0
    for p in GRID:
        if on_segment(a, b, p):
            m |= 1 << GRID_INDEX[p]
    return m


def unscale_point(p: Point) -> list[int] | list[float]:
    if all(v % SCALE == 0 for v in p):
        return [v // SCALE for v in p]
    return [v / SCALE for v in p]


def line_from_raw(raw: object) -> Line:
    a, b = raw  # type: ignore[misc]
    return (tuple(map(int, a)), tuple(map(int, b)))  # type: ignore[return-value]


def load_lines(data: dict) -> List[Line]:
    if data.get("line_set2"):
        return [line_from_raw(x) for x in data["line_set2"]]
    if data.get("line_set"):
        out = []
        for a, b in data["line_set"]:
            out.append(((SCALE*int(a[0]), SCALE*int(a[1]), SCALE*int(a[2])),
                        (SCALE*int(b[0]), SCALE*int(b[1]), SCALE*int(b[2]))))
        return out
    raise ValueError("input scaffold has no line_set2 or line_set")


def canonical_line(line: Line) -> Line:
    a, b = line
    return (a, b) if a <= b else (b, a)


def line_key(lines: Sequence[Line]) -> str:
    payload = json.dumps([[list(a), list(b)] for a, b in sorted(canonical_line(x) for x in lines)], separators=(",", ":"))
    return hashlib.sha256(payload.encode()).hexdigest()


def vertices_key(vertices: Sequence[Point]) -> str:
    payload = json.dumps([list(v) for v in vertices], separators=(",", ":"))
    return hashlib.sha256(payload.encode()).hexdigest()


def load_scaffolds(json_files: Sequence[Path], jsonl_files: Sequence[Path]) -> List[dict]:
    out: List[dict] = []
    seen = set()
    for p in json_files:
        if not p.exists():
            continue
        d = json.loads(p.read_text(encoding="utf-8"))
        if isinstance(d, dict) and (d.get("line_set2") or d.get("line_set")):
            lines = load_lines(d)
            key = line_key(lines)
            if key not in seen:
                seen.add(key)
                d = dict(d)
                d.setdefault("candidate_id", p.stem)
                d["_source_file"] = str(p)
                out.append(d)
    for p in jsonl_files:
        if not p.exists():
            continue
        for raw in p.read_text(encoding="utf-8").splitlines():
            if not raw.strip():
                continue
            d = json.loads(raw)
            if not isinstance(d, dict) or not (d.get("line_set2") or d.get("line_set")):
                continue
            lines = load_lines(d)
            key = line_key(lines)
            if key not in seen:
                seen.add(key)
                d = dict(d)
                d["_source_file"] = str(p)
                out.append(d)
    return out


def generate_line_universe(scaffolds: Sequence[dict], box_min: int, box_max: int, min_cover: int, limit: int, seed: int) -> List[Line]:
    seen = set()
    lines: List[Line] = []
    for sc in scaffolds:
        for line in load_lines(sc):
            c = canonical_line(line)
            if c not in seen and mask_for_segment(*c).bit_count() >= min_cover:
                seen.add(c)
                lines.append(c)

    pts = [(SCALE*x, SCALE*y, SCALE*z)
           for x in range(box_min, box_max + 1)
           for y in range(box_min, box_max + 1)
           for z in range(box_min, box_max + 1)]
    rng = random.Random(seed)
    pairs = []
    for i, a in enumerate(pts):
        for b in pts[i+1:]:
            m = mask_for_segment(a, b)
            c = m.bit_count()
            if c >= min_cover:
                pairs.append((-c, rng.random(), canonical_line((a, b))))
    pairs.sort()
    for _, _, line in pairs:
        if line not in seen:
            seen.add(line)
            lines.append(line)
            if len(lines) >= limit:
                break
    return lines[:limit]


@dataclass
class State:
    score: int
    used_mask: int
    last_line: int
    current: Point
    vertices: Tuple[Point, ...]
    order: Tuple[int, ...]
    covered_mask: int
    weak_links: int


def prepare_line_data(lines: Sequence[Line]) -> dict:
    n = len(lines)
    candidates: List[List[Point]] = []
    for a, b in lines:
        gp = [p for p in GRID if on_segment(a, b, p)]
        cand = set(gp)
        cand.add(a)
        cand.add(b)
        candidates.append(sorted(cand))

    future_degree: List[Dict[Point, int]] = []
    for i in range(n):
        d: Dict[Point, int] = {}
        for p in candidates[i]:
            d[p] = sum(1 for j in range(n) if j != i and on_segment(lines[j][0], lines[j][1], p))
        future_degree.append(d)

    return {
        "candidates": candidates,
        "future_degree": future_degree,
    }


def state_score(covered_mask: int, used_count: int, seg_gain: int, weak_links: int, future_deg: int) -> int:
    return (
        covered_mask.bit_count() * 100000
        + used_count * 1000
        + seg_gain * 100
        + future_deg * 7
        - weak_links * 250
    )


def best_chain_for_lines(
    lines: Sequence[Line],
    rng: random.Random,
    beam_width: int,
    branch_limit: int,
    start_limit: int,
    deadline: float,
) -> dict:
    n = len(lines)
    data = prepare_line_data(lines)
    candidates: List[List[Point]] = data["candidates"]
    future_degree: List[Dict[Point, int]] = data["future_degree"]

    start_lines = list(range(n))
    rng.shuffle(start_lines)
    start_lines = start_lines[:max(1, min(n, start_limit))]

    beam: List[State] = []
    best: State | None = None

    for i in start_lines:
        pts = candidates[i]
        end_pts = sorted(pts, key=lambda p: (future_degree[i].get(p, 0), p), reverse=True)[:max(4, branch_limit)]
        start_pts = pts[:]
        rng.shuffle(start_pts)
        start_pts = start_pts[:max(4, branch_limit)]
        for a in start_pts:
            for b in end_pts:
                if a == b:
                    continue
                seg = mask_for_segment(a, b)
                if not seg:
                    continue
                weak = 1 if seg.bit_count() <= 1 else 0
                st = State(
                    score=state_score(seg, 1, seg.bit_count(), weak, future_degree[i].get(b, 0)),
                    used_mask=1 << i,
                    last_line=i,
                    current=b,
                    vertices=(a, b),
                    order=(i,),
                    covered_mask=seg,
                    weak_links=weak,
                )
                beam.append(st)
                if best is None or st.score > best.score:
                    best = st
    beam.sort(key=lambda s: s.score, reverse=True)
    beam = beam[:beam_width]

    while beam and time.time() < deadline:
        depth = max(len(s.order) for s in beam)
        if depth >= n:
            break
        nxt: List[State] = []
        for st in beam:
            if len(st.order) >= n:
                nxt.append(st)
                continue
            current = st.current
            possible_lines = [
                j for j in range(n)
                if not (st.used_mask >> j) & 1 and on_segment(lines[j][0], lines[j][1], current)
            ]
            if not possible_lines:
                nxt.append(st)
                continue
            possible_lines.sort(key=lambda j: future_degree[j].get(current, 0), reverse=True)
            possible_lines = possible_lines[:max(2, branch_limit)]
            for j in possible_lines:
                pts = [p for p in candidates[j] if p != current]
                pts.sort(
                    key=lambda p: (
                        (mask_for_segment(current, p) | st.covered_mask).bit_count(),
                        mask_for_segment(current, p).bit_count(),
                        future_degree[j].get(p, 0),
                    ),
                    reverse=True,
                )
                pts = pts[:max(2, branch_limit)]
                for p in pts:
                    seg = mask_for_segment(current, p)
                    if not seg:
                        continue
                    new_mask = st.covered_mask | seg
                    weak = st.weak_links + (1 if seg.bit_count() <= 1 else 0)
                    new_order = st.order + (j,)
                    ns = State(
                        score=state_score(new_mask, len(new_order), seg.bit_count(), weak, future_degree[j].get(p, 0)),
                        used_mask=st.used_mask | (1 << j),
                        last_line=j,
                        current=p,
                        vertices=st.vertices + (p,),
                        order=new_order,
                        covered_mask=new_mask,
                        weak_links=weak,
                    )
                    nxt.append(ns)
                    if best is None or (len(ns.order), ns.covered_mask.bit_count(), ns.score) > (len(best.order), best.covered_mask.bit_count(), best.score):
                        best = ns
            if time.time() >= deadline:
                break
        nxt.sort(key=lambda s: (len(s.order), s.covered_mask.bit_count(), s.score), reverse=True)
        beam = nxt[:beam_width]

    if best is None:
        return {"status": "no_chain", "covered_count": 0, "vertices2": [], "links": 0, "line_order": []}

    missing = [unscale_point(p) for p in GRID if not (best.covered_mask >> GRID_INDEX[p]) & 1]
    return {
        "status": "full_length_ordered_chain" if len(best.vertices) == n + 1 else "partial_ordered_chain",
        "coordinate_scale": SCALE,
        "vertices2": [list(v) for v in best.vertices],
        "vertices": [unscale_point(v) for v in best.vertices],
        "links": max(0, len(best.vertices) - 1),
        "line_order": list(best.order),
        "covered_count": best.covered_mask.bit_count(),
        "missing_count": len(missing),
        "missing": missing,
        "weak_links": best.weak_links,
        "score": best.score,
    }


def mutate_lines(base: Sequence[Line], universe: Sequence[Line], rng: random.Random, mode: str, max_mutations: int) -> List[Line]:
    lines = list(base)
    if mode == "strict_reconstruct_top4" or max_mutations <= 0:
        return lines
    mutation_count = 1
    if mode in {"one_two_line_mutation", "large_neighborhood_ordering"}:
        mutation_count = rng.randint(1, max(1, min(max_mutations, 2 if mode == "one_two_line_mutation" else 6)))
    elif mode in {"contact_extreme_search", "bridge_contact_repair"}:
        mutation_count = rng.randint(1, max(1, min(max_mutations, 3)))
    used = {canonical_line(x) for x in lines}
    for _ in range(mutation_count):
        if not universe:
            break
        pos = rng.randrange(len(lines))
        for _tries in range(50):
            cand = universe[rng.randrange(len(universe))]
            c = canonical_line(cand)
            if c not in used:
                used.discard(canonical_line(lines[pos]))
                lines[pos] = cand
                used.add(c)
                break
    return lines


def mode_for_shard(shard: int) -> str:
    if 0 <= shard <= 3:
        return "strict_reconstruct_top4"
    if 4 <= shard <= 7:
        return "one_two_line_mutation"
    if 8 <= shard <= 11:
        return "contact_extreme_search"
    if 12 <= shard <= 15:
        return "bridge_contact_repair"
    if 16 <= shard <= 18:
        return "large_neighborhood_ordering"
    return "control_fixed_best"


def worker_main(payload: tuple) -> dict:
    (
        worker_id, seed, shard, mode, scaffolds, universe, seconds, beam_width,
        branch_limit, start_limit, max_mutations
    ) = payload
    rng = random.Random(seed + 1000003 * shard + 10007 * worker_id)
    deadline = time.time() + max(1, seconds)
    attempts = 0
    best: dict | None = None

    base_scaffolds = scaffolds[:]
    if mode == "control_fixed_best":
        base_scaffolds = scaffolds[:1] if scaffolds else []

    while time.time() < deadline and base_scaffolds:
        sc = base_scaffolds[(attempts + shard + worker_id) % len(base_scaffolds)]
        base_lines = load_lines(sc)
        lines = mutate_lines(base_lines, universe, rng, mode, max_mutations)
        local_deadline = min(deadline, time.time() + max(2.0, seconds / 20.0))
        res = best_chain_for_lines(
            lines,
            rng=rng,
            beam_width=beam_width,
            branch_limit=branch_limit,
            start_limit=start_limit,
            deadline=local_deadline,
        )
        attempts += 1
        res.update({
            "worker_id": worker_id,
            "attempts": attempts,
            "mode": mode,
            "source_scaffold_id": sc.get("candidate_id"),
            "source_scaffold_file": sc.get("_source_file"),
            "source_scaffold_compact_key_sha256": sc.get("compact_key_sha256"),
            "line_set2": [[list(a), list(b)] for a, b in lines],
            "line_set_compact_key_sha256": line_key(lines),
        })
        key = (res.get("links", 0), res.get("covered_count", 0), -res.get("weak_links", 999), res.get("score", 0))
        if best is None:
            best = res
        else:
            best_key = (best.get("links", 0), best.get("covered_count", 0), -best.get("weak_links", 999), best.get("score", 0))
            if key > best_key:
                best = res
        if best and best.get("links") == 22 and best.get("covered_count") == 64:
            break

    if best is None:
        best = {"status": "no_result", "covered_count": 0, "links": 0, "vertices2": [], "line_order": []}
    best["worker_attempts"] = attempts
    return best


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input-json", action="append", default=[], type=Path)
    ap.add_argument("--input-jsonl", action="append", default=[], type=Path)
    ap.add_argument("--seconds", type=int, default=180)
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--seed", type=int, default=20260718)
    ap.add_argument("--shard", type=int, default=0)
    ap.add_argument("--shards", type=int, default=20)
    ap.add_argument("--beam-width", type=int, default=512)
    ap.add_argument("--branch-limit", type=int, default=5)
    ap.add_argument("--start-limit", type=int, default=22)
    ap.add_argument("--max-mutations", type=int, default=2)
    ap.add_argument("--box-min", type=int, default=-1)
    ap.add_argument("--box-max", type=int, default=4)
    ap.add_argument("--candidate-lines", type=int, default=3000)
    ap.add_argument("--min-line-cover", type=int, default=2)
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()

    scaffolds = load_scaffolds(args.input_json, args.input_jsonl)
    if not scaffolds:
        raise SystemExit("no input scaffolds found")
    scaffolds.sort(key=lambda d: (int(d.get("stitch_path_lower_bound", 0)), int(d.get("covered_count", 0))), reverse=True)
    mode = mode_for_shard(args.shard)
    universe = generate_line_universe(
        scaffolds,
        box_min=args.box_min,
        box_max=args.box_max,
        min_cover=args.min_line_cover,
        limit=args.candidate_lines,
        seed=args.seed + args.shard,
    )

    worker_seconds = max(1, int(args.seconds))
    payloads = [
        (
            wid, args.seed, args.shard, mode, scaffolds, universe, worker_seconds,
            args.beam_width, args.branch_limit, args.start_limit, args.max_mutations
        )
        for wid in range(max(1, args.workers))
    ]
    if args.workers <= 1:
        worker_results = [worker_main(payloads[0])]
    else:
        with mp.Pool(processes=args.workers) as pool:
            worker_results = pool.map(worker_main, payloads)

    best = max(
        worker_results,
        key=lambda r: (r.get("links", 0), r.get("covered_count", 0), -r.get("weak_links", 999), r.get("score", 0)),
    )
    result = dict(best)
    result.update({
        "schema": "contact-aware-ordering-result-v1",
        "source_workflow": "smart-search-18-order-from-cover64-stitch",
        "source_shard": args.shard,
        "source_artifact": f"order-cover64-stitch-22-shard-{args.shard}",
        "parameters": {
            "seconds": args.seconds,
            "workers": args.workers,
            "seed": args.seed,
            "shard": args.shard,
            "shards": args.shards,
            "beam_width": args.beam_width,
            "branch_limit": args.branch_limit,
            "start_limit": args.start_limit,
            "max_mutations": args.max_mutations,
            "box_min": args.box_min,
            "box_max": args.box_max,
            "candidate_lines": args.candidate_lines,
            "min_line_cover": args.min_line_cover,
        },
        "worker_results": [
            {
                "worker_id": r.get("worker_id"),
                "status": r.get("status"),
                "links": r.get("links"),
                "covered_count": r.get("covered_count"),
                "weak_links": r.get("weak_links"),
                "score": r.get("score"),
                "attempts": r.get("worker_attempts"),
                "mode": r.get("mode"),
                "source_scaffold_id": r.get("source_scaffold_id"),
            }
            for r in worker_results
        ],
    })
    if result.get("vertices2"):
        result["candidate_id"] = "mlct22-order-" + vertices_key([tuple(v) for v in result["vertices2"]])[:16]
    else:
        result["candidate_id"] = f"mlct22-order-no-result-shard-{args.shard}"

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps({
        "candidate_id": result["candidate_id"],
        "mode": mode,
        "links": result.get("links"),
        "covered_count": result.get("covered_count"),
        "missing_count": result.get("missing_count"),
        "status": result.get("status"),
        "out": str(args.out),
    }, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
