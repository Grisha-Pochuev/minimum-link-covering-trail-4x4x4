#!/usr/bin/env python3
"""Search-20 engine: preserve full rich scaffold lines, spend explicit bridge links."""
from __future__ import annotations
import argparse, hashlib, json, multiprocessing as mp, random, time
from collections import Counter, defaultdict, deque
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence, Tuple
import order_from_cover64_stitch as base

Point = Tuple[int, int, int]
Line = Tuple[Point, Point]
SCALE = base.SCALE
GRID = base.GRID
GRID_INDEX = base.GRID_INDEX
TARGET_LINKS = 22
OFFICIAL60 = [(0,0,SCALE),(0,2*SCALE,3*SCALE),(0,3*SCALE,SCALE),(2*SCALE,SCALE,SCALE)]
OFFICIAL60_MASK = sum(1 << GRID_INDEX[p] for p in OFFICIAL60)


def vkey(vertices: Sequence[Point]) -> str:
    return hashlib.sha256(json.dumps([list(v) for v in vertices], separators=(",", ":")).encode()).hexdigest()


def dist2(a: Point, b: Point) -> int:
    return sum((a[i] - b[i]) ** 2 for i in range(3))


def line_mask(line: Line) -> int:
    return base.mask_for_segment(*line)


def load_scaffolds(args: argparse.Namespace) -> list[dict]:
    rows, seen = [], set()
    def add(row: dict, src: str, kind: str) -> None:
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
        d.setdefault("candidate_id", Path(src).stem)
        d["_source_file"] = src
        d["_source_kind"] = kind
        rows.append(d)
    for p in args.input_json + args.diagnostic_json:
        if p.exists():
            add(json.loads(p.read_text(encoding="utf-8")), str(p), "json")
    for p in args.input_jsonl + args.diagnostic_jsonl:
        if not p.exists():
            continue
        for raw in p.read_text(encoding="utf-8").splitlines():
            if raw.strip():
                try:
                    add(json.loads(raw), str(p), "jsonl")
                except Exception:
                    pass
    rows.sort(key=lambda r: scaffold_score(base.load_lines(r)), reverse=True)
    return rows[: max(1, args.candidate_scaffolds)]


def scaffold_score(lines: Sequence[Line]) -> tuple:
    union = 0; rich4 = rich3 = 0
    for ln in lines:
        m = line_mask(ln); union |= m
        rich4 += int(m.bit_count() >= 4); rich3 += int(m.bit_count() >= 3)
    return (union.bit_count(), rich4, rich3, -endpoint_components(lines))


def endpoint_components(lines: Sequence[Line]) -> int:
    parent = {}
    def find(x):
        parent.setdefault(x, x)
        while parent[x] != x:
            parent[x] = parent[parent[x]]; x = parent[x]
        return x
    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb: parent[rb] = ra
    for a, b in lines: union(a, b)
    return len({find(x) for x in parent}) if parent else 0


def endpoint_summary(lines: Sequence[Line]) -> dict:
    by_pt = defaultdict(list)
    for i, (a, b) in enumerate(lines):
        by_pt[a].append(i); by_pt[b].append(i)
    adj = {i: set() for i in range(len(lines))}; contacts = 0
    for inc in by_pt.values():
        contacts += max(0, len(inc) - 1)
        for i in inc:
            for j in inc:
                if i != j: adj[i].add(j)
    seen, comps = set(), []
    for i in range(len(lines)):
        if i in seen: continue
        q, comp = deque([i]), []
        seen.add(i)
        while q:
            u = q.popleft(); comp.append(u)
            for v in adj[u]:
                if v not in seen:
                    seen.add(v); q.append(v)
        comps.append(comp)
    return {"endpoint_component_count": len(comps), "endpoint_component_sizes": sorted([len(c) for c in comps], reverse=True), "endpoint_contact_count": contacts}


def mode_for_shard(shard: int) -> str:
    if shard <= 3: return "integer_full_bridge"
    if shard <= 7: return "outside_bridge_expansion"
    if shard <= 11: return "official60_bridge"
    if shard <= 15: return "diverse_endpoint_components"
    if shard <= 18: return "one_line_replacement"
    return "conservative_control"


@dataclass
class State:
    vertices: tuple[Point, ...]
    current: Point
    used_mask: int
    covered_mask: int
    full_lines: int
    bridges: int
    rich_kept: int
    line_order: tuple[int, ...]
    link_types: tuple[str, ...]
    bridge_segments: tuple[tuple[Point, Point], ...]
    score: int = 0
    @property
    def links(self) -> int: return max(0, len(self.vertices) - 1)


def score_state(st: State, mode: str) -> int:
    old = (st.covered_mask & OFFICIAL60_MASK).bit_count()
    cov = st.covered_mask.bit_count()
    bridge_penalty = 12000 if mode == "outside_bridge_expansion" else 24000
    old_bonus = 260000 if mode == "official60_bridge" else 150000
    rich_bonus = 145000 if mode == "conservative_control" else 105000
    return cov*1_000_000 + st.full_lines*65000 + st.rich_kept*rich_bonus + old*old_bonus + (st.links == TARGET_LINKS)*350000 - st.bridges*bridge_penalty


def rkey(st: State) -> tuple:
    old = (st.covered_mask & OFFICIAL60_MASK).bit_count()
    return (int(st.links == TARGET_LINKS), st.covered_mask.bit_count(), st.rich_kept, st.full_lines, old, -st.bridges, st.score)


def keep(states: list[State], limit: int) -> list[State]:
    best = {}
    for st in states:
        k = (st.links, st.current, st.used_mask, st.bridges)
        if k not in best or rkey(st) > rkey(best[k]): best[k] = st
    out = list(best.values()); out.sort(key=rkey, reverse=True)
    return out[:limit]


def options(lines: Sequence[Line]) -> list[tuple[int, Point, Point, int, int]]:
    out = []
    for i, (a, b) in enumerate(lines):
        m = line_mask((a, b)); rich = int(m.bit_count() >= 3)
        out.append((i, a, b, m, rich)); out.append((i, b, a, m, rich))
    return out


def add_full(st: State, opt, mode: str) -> State:
    i, _a, b, m, rich = opt
    ns = State(st.vertices+(b,), b, st.used_mask|(1<<i), st.covered_mask|m, st.full_lines+1, st.bridges, st.rich_kept+rich, st.line_order+(i,), st.link_types+("full_line",), st.bridge_segments)
    ns.score = score_state(ns, mode); return ns


def add_bridge_full(st: State, opt, mode: str) -> State:
    i, a, b, m, rich = opt
    bm = base.mask_for_segment(st.current, a)
    ns = State(st.vertices+(a,b), b, st.used_mask|(1<<i), st.covered_mask|bm|m, st.full_lines+1, st.bridges+1, st.rich_kept+rich, st.line_order+(i,), st.link_types+("bridge","full_line"), st.bridge_segments+((st.current,a),))
    ns.score = score_state(ns, mode); return ns


def add_repair(st: State, target: Point, mode: str) -> State:
    bm = base.mask_for_segment(st.current, target)
    ns = State(st.vertices+(target,), target, st.used_mask, st.covered_mask|bm, st.full_lines, st.bridges+1, st.rich_kept, st.line_order, st.link_types+("repair_bridge",), st.bridge_segments+((st.current,target),))
    ns.score = score_state(ns, mode); return ns


def bridge_targets(st: State, opts, mode: str, limit: int):
    scored = []
    for opt in opts:
        i, a, _b, m, rich = opt
        if (st.used_mask >> i) & 1 or a == st.current: continue
        bm = base.mask_for_segment(st.current, a)
        gain = ((bm | m) & ~st.covered_mask).bit_count()
        old = ((bm | m) & OFFICIAL60_MASK & ~st.covered_mask).bit_count()
        penalty = dist2(st.current, a) * (1 if mode == "outside_bridge_expansion" else 8)
        scored.append((gain*100000 + old*220000 + rich*80000 - penalty, opt))
    scored.sort(key=lambda x: x[0], reverse=True)
    return [x[1] for x in scored[:limit]]


def repair_targets(st: State, lines: Sequence[Line], mode: str, limit: int):
    pts = set(GRID)
    for a, b in lines: pts.add(a); pts.add(b)
    scored = []
    for p in pts:
        if p == st.current: continue
        m = base.mask_for_segment(st.current, p)
        gain = (m & ~st.covered_mask).bit_count(); old = (m & OFFICIAL60_MASK & ~st.covered_mask).bit_count()
        scored.append((gain*100000 + old*220000 - dist2(st.current, p)*3, p))
    scored.sort(key=lambda x: x[0], reverse=True)
    return [p for _, p in scored[:limit]]


def search_chain(lines: Sequence[Line], rng: random.Random, mode: str, args: argparse.Namespace, deadline: float) -> dict:
    opts = options(lines); rng.shuffle(opts)
    opts.sort(key=lambda o: (line_mask((o[1], o[2])).bit_count(), o[4], rng.random()), reverse=True)
    beam = []
    for opt in opts[:max(2, args.start_limit*2)]:
        i, a, b, m, rich = opt
        st = State((a,b), b, 1<<i, m, 1, 0, rich, (i,), ("full_line",), ())
        st.score = score_state(st, mode); beam.append(st)
    beam = keep(beam, args.beam_width); best = beam[0]
    while beam and time.time() < deadline:
        if all(st.links >= TARGET_LINKS for st in beam): break
        nxt = []
        for st in beam:
            if st.links >= TARGET_LINKS:
                nxt.append(st); continue
            rem = TARGET_LINKS - st.links
            if st.full_lines < args.max_full_lines:
                direct = [o for o in opts if o[1] == st.current and not ((st.used_mask >> o[0]) & 1)]
                direct.sort(key=lambda o: ((o[3] & ~st.covered_mask).bit_count(), o[4]), reverse=True)
                for opt in direct[:args.line_branch_limit]: nxt.append(add_full(st, opt, mode))
            if rem >= 2 and st.bridges < args.max_bridge_links and st.full_lines < args.max_full_lines:
                for opt in bridge_targets(st, opts, mode, args.bridge_branch_limit): nxt.append(add_bridge_full(st, opt, mode))
            if st.bridges < args.max_bridge_links and (st.full_lines >= args.min_full_lines or rem <= 2):
                for p in repair_targets(st, lines, mode, min(args.bridge_branch_limit, 12)): nxt.append(add_repair(st, p, mode))
            if len(nxt) >= args.state_cap: break
        if not nxt: break
        for ns in nxt:
            if ns.links <= TARGET_LINKS and rkey(ns) > rkey(best): best = ns
        beam = keep([x for x in nxt if x.links <= TARGET_LINKS], min(args.beam_width, args.state_cap))
    missing = [base.unscale_point(p) for p in GRID if not (best.covered_mask >> GRID_INDEX[p]) & 1]
    bridge_masks = [base.mask_for_segment(a,b) for a,b in best.bridge_segments]
    full_mask = 0
    for i in best.line_order: full_mask |= line_mask(lines[i])
    return {"status":"full_length_ordered_chain" if best.links == TARGET_LINKS else "partial_ordered_chain", "coordinate_scale":SCALE, "vertices2":[list(v) for v in best.vertices], "vertices":[base.unscale_point(v) for v in best.vertices], "links":best.links, "covered_count":best.covered_mask.bit_count(), "grid_points":64, "coverage_percent":100*best.covered_mask.bit_count()/64, "missing_count":len(missing), "missing":missing, "line_order":list(best.line_order), "link_types":list(best.link_types), "bridge_segments2":[[list(a),list(b)] for a,b in best.bridge_segments], "full_line_bridge_metrics":{"full_line_links":best.full_lines, "bridge_links":best.bridges, "preserved_rich_lines":best.rich_kept, "official60_missing_hits":(best.covered_mask&OFFICIAL60_MASK).bit_count(), "bridge_points_total":sum(m.bit_count() for m in bridge_masks), "bridge_only_points":sum((m & ~full_mask).bit_count() for m in bridge_masks), "unused_scaffold_lines":len(lines)-best.full_lines}, "score":best.score}


def mutate(lines: Sequence[Line], universe: Sequence[Line], rng: random.Random, mode: str, max_mutations: int) -> list[Line]:
    lines = list(lines)
    if mode not in {"one_line_replacement", "outside_bridge_expansion"} or max_mutations <= 0: return lines
    used = {base.canonical_line(x) for x in lines}
    for _ in range(rng.randint(0, max_mutations)):
        pos = rng.randrange(len(lines)); old = line_mask(lines[pos]).bit_count()
        for _try in range(120):
            cand = universe[rng.randrange(len(universe))]; cc = base.canonical_line(cand)
            if cc not in used and line_mask(cand).bit_count() >= max(2, old-1):
                used.discard(base.canonical_line(lines[pos])); lines[pos] = cand; used.add(cc); break
    return lines


def res_key(row: dict) -> tuple:
    m = row.get("full_line_bridge_metrics") or {}
    return (int(row.get("links",0)==TARGET_LINKS), int(row.get("covered_count",0) or 0), int(m.get("preserved_rich_lines",0) or 0), int(m.get("full_line_links",0) or 0), int(m.get("official60_missing_hits",0) or 0), -int(m.get("bridge_links",999) or 999), int(row.get("score",0) or 0))


def worker(payload) -> dict:
    wid, seed, shard, mode, scaffolds, universe, args_dict = payload
    args = argparse.Namespace(**args_dict); rng = random.Random(seed + 1000003*shard + 10007*wid)
    deadline = time.time() + max(1, args.seconds); attempts = 0; best = None
    pool = scaffolds[:1] if mode == "conservative_control" else scaffolds[:]
    while time.time() < deadline and pool:
        sc = pool[(attempts + shard + wid) % len(pool)]
        lines = mutate(base.load_lines(sc), universe, rng, mode, args.max_mutations)
        res = search_chain(lines, rng, mode, args, min(deadline, time.time()+max(2.0,args.seconds/10)))
        attempts += 1
        res.update({"worker_id":wid, "worker_attempts":attempts, "mode":mode, "source_scaffold_id":sc.get("candidate_id"), "source_scaffold_file":sc.get("_source_file"), "source_scaffold_kind":sc.get("_source_kind"), "line_set2":[[list(a),list(b)] for a,b in lines], "line_set_compact_key_sha256":base.line_key(lines), "endpoint_component_summary":endpoint_summary(lines)})
        if best is None or res_key(res) > res_key(best): best = res
        if best.get("links") == TARGET_LINKS and best.get("covered_count") == 64: break
    return best or {"status":"no_result", "links":0, "covered_count":0, "vertices2":[]}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input-json", action="append", default=[], type=Path); ap.add_argument("--input-jsonl", action="append", default=[], type=Path)
    ap.add_argument("--diagnostic-json", action="append", default=[], type=Path); ap.add_argument("--diagnostic-jsonl", action="append", default=[], type=Path)
    ap.add_argument("--seconds", type=int, default=180); ap.add_argument("--workers", type=int, default=4); ap.add_argument("--seed", type=int, default=20260720)
    ap.add_argument("--shard", type=int, default=0); ap.add_argument("--shards", type=int, default=20); ap.add_argument("--beam-width", type=int, default=2048); ap.add_argument("--state-cap", type=int, default=200000)
    ap.add_argument("--candidate-scaffolds", type=int, default=4); ap.add_argument("--max-mutations", type=int, default=0); ap.add_argument("--box-min", type=int, default=-1); ap.add_argument("--box-max", type=int, default=4); ap.add_argument("--candidate-lines", type=int, default=3000)
    ap.add_argument("--start-limit", type=int, default=22); ap.add_argument("--line-branch-limit", type=int, default=12); ap.add_argument("--bridge-branch-limit", type=int, default=8)
    ap.add_argument("--min-full-lines", type=int, default=10); ap.add_argument("--max-full-lines", type=int, default=18); ap.add_argument("--max-bridge-links", type=int, default=8)
    ap.add_argument("--out", type=Path, required=True); ap.add_argument("--preferred-out", type=Path); ap.add_argument("--bridge-report-out", type=Path)
    args = ap.parse_args(); scaffolds = load_scaffolds(args)
    if not scaffolds: raise SystemExit("no input scaffolds found")
    mode = mode_for_shard(args.shard)
    universe = base.generate_line_universe(scaffolds, args.box_min, args.box_max, 2 if mode == "outside_bridge_expansion" else 3, args.candidate_lines, args.seed + args.shard)
    args_dict = vars(args).copy()
    for k in ["input_json","input_jsonl","diagnostic_json","diagnostic_jsonl","out","preferred_out","bridge_report_out"]: args_dict.pop(k, None)
    payloads = [(wid,args.seed,args.shard,mode,scaffolds,universe,args_dict) for wid in range(max(1,args.workers))]
    results = [worker(payloads[0])] if args.workers <= 1 else mp.Pool(processes=args.workers).map(worker, payloads)
    result = dict(max(results, key=res_key))
    result.update({"schema":"full-line-bridge-result-v1", "source_workflow":"fl-bridge-20", "source_shard":args.shard, "source_artifact":f"fl-bridge-22-shard-{args.shard}", "parameters":{k:v for k,v in vars(args).items() if k not in {"input_json","input_jsonl","diagnostic_json","diagnostic_jsonl","out","preferred_out","bridge_report_out"}}, "worker_results":[{"worker_id":r.get("worker_id"), "links":r.get("links"), "covered_count":r.get("covered_count"), "mode":r.get("mode"), "worker_attempts":r.get("worker_attempts"), "full_line_bridge_metrics":r.get("full_line_bridge_metrics")} for r in results], "interpretation":"full-line-preserving ordered chain: rich scaffold lines are traversed whole and bridge links are spent explicitly between endpoint components"})
    result["candidate_id"] = "mlct22-flbridge-" + vkey([tuple(v) for v in result.get("vertices2", [])])[:16] if result.get("vertices2") else f"mlct22-flbridge-no-result-shard-{args.shard}"
    args.out.parent.mkdir(parents=True, exist_ok=True); args.out.write_text(json.dumps(result, indent=2, sort_keys=True), encoding="utf-8")
    if args.preferred_out:
        args.preferred_out.parent.mkdir(parents=True, exist_ok=True); args.preferred_out.write_text(json.dumps(result, sort_keys=True)+"\n", encoding="utf-8")
    if args.bridge_report_out:
        report = {"candidate_id":result.get("candidate_id"), "mode":result.get("mode"), "links":result.get("links"), "covered_count":result.get("covered_count"), "missing_count":result.get("missing_count"), "full_line_bridge_metrics":result.get("full_line_bridge_metrics"), "endpoint_component_summary":result.get("endpoint_component_summary"), "bridge_segments2":result.get("bridge_segments2"), "line_order":result.get("line_order"), "link_type_counts":dict(Counter(result.get("link_types", [])))}
        args.bridge_report_out.parent.mkdir(parents=True, exist_ok=True); args.bridge_report_out.write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps({"candidate_id":result["candidate_id"], "mode":mode, "links":result.get("links"), "covered_count":result.get("covered_count"), "out":str(args.out)}, indent=2, sort_keys=True))
    return 0
if __name__ == "__main__": raise SystemExit(main())
