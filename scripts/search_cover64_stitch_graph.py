from __future__ import annotations

import argparse
import hashlib
import json
import math
import multiprocessing as mp
import random
import time
from dataclasses import dataclass
from pathlib import Path

GRID = [(2*x, 2*y, 2*z) for x in range(4) for y in range(4) for z in range(4)]
GRID_INDEX = {p: i for i, p in enumerate(GRID)}
FULL_MASK = (1 << 64) - 1
OLD_WALL = [(0, 0, 1), (0, 2, 3), (0, 3, 1), (2, 1, 1)]
OLD_WALL2 = [(2*x, 2*y, 2*z) for x, y, z in OLD_WALL]


def sub(a, b):
    return (a[0]-b[0], a[1]-b[1], a[2]-b[2])


def dot(a, b):
    return a[0]*b[0] + a[1]*b[1] + a[2]*b[2]


def cross(a, b):
    return (
        a[1]*b[2] - a[2]*b[1],
        a[2]*b[0] - a[0]*b[2],
        a[0]*b[1] - a[1]*b[0],
    )


def on_segment(a, b, p):
    d = sub(b, a)
    if d == (0, 0, 0):
        return False
    ap = sub(p, a)
    return cross(d, ap) == (0, 0, 0) and 0 <= dot(ap, d) <= dot(d, d)


def mask_for_line(a, b):
    m = 0
    for p in GRID:
        if on_segment(a, b, p):
            m |= 1 << GRID_INDEX[p]
    return m


def point_mask(p):
    return 1 << GRID_INDEX[p]


OLD_WALL_MASK = 0
for p in OLD_WALL2:
    OLD_WALL_MASK |= point_mask(p)


@dataclass(frozen=True)
class Line:
    a: tuple[int, int, int]
    b: tuple[int, int, int]
    mask: int
    wall_hits: int
    cover_count: int

    def as_json(self):
        return [list(self.a), list(self.b)]


def canonical_pair(a, b):
    return (a, b) if a <= b else (b, a)


def build_universe(box_min: int, box_max: int, min_line_cover: int, max_universe: int):
    pts = [(2*x, 2*y, 2*z) for x in range(box_min, box_max + 1) for y in range(box_min, box_max + 1) for z in range(box_min, box_max + 1)]
    by_mask: dict[int, Line] = {}
    for i, a in enumerate(pts):
        for b in pts[i+1:]:
            m = mask_for_line(a, b)
            c = m.bit_count()
            if c < min_line_cover:
                continue
            wh = (m & OLD_WALL_MASK).bit_count()
            aa, bb = canonical_pair(a, b)
            old = by_mask.get(m)
            cand = Line(aa, bb, m, wh, c)
            # Prefer shorter endpoints near the 4x4x4 box when several segments cover the same grid subset.
            span = sum(abs(aa[k]-bb[k]) for k in range(3))
            old_span = 10**9 if old is None else sum(abs(old.a[k]-old.b[k]) for k in range(3))
            if old is None or (wh, c, -span) > (old.wall_hits, old.cover_count, -old_span):
                by_mask[m] = cand
    lines = list(by_mask.values())
    lines.sort(key=lambda x: (x.wall_hits, x.cover_count, -sum(abs(x.a[k]-x.b[k]) for k in range(3))), reverse=True)
    if max_universe and len(lines) > max_universe:
        # Keep all strong old-wall and 4-point lines, then a deterministic prefix.
        keep = [x for x in lines if x.wall_hits or x.cover_count >= 4]
        seen = {x.mask for x in keep}
        for x in lines:
            if len(keep) >= max_universe:
                break
            if x.mask not in seen:
                keep.append(x)
                seen.add(x.mask)
        lines = keep
    return lines


def load_line_set(path: Path):
    d = json.loads(path.read_text())
    rows = d.get('line_set2') or []
    out = []
    for a, b in rows:
        aa, bb = canonical_pair(tuple(map(int, a)), tuple(map(int, b)))
        out.append((aa, bb))
    return out


def state_key(state):
    return tuple(sorted(state))


def coverage_mask(state, lines):
    m = 0
    for i in state:
        m |= lines[i].mask
    return m


def stitch_graph(state, lines):
    n = len(state)
    adj = [set() for _ in range(n)]
    for i in range(n):
        mi = lines[state[i]].mask
        for j in range(i+1, n):
            if mi & lines[state[j]].mask:
                adj[i].add(j)
                adj[j].add(i)
    return adj


def components(adj):
    n = len(adj)
    seen = set()
    comps = []
    for i in range(n):
        if i in seen:
            continue
        stack = [i]
        seen.add(i)
        comp = []
        while stack:
            u = stack.pop()
            comp.append(u)
            for v in adj[u]:
                if v not in seen:
                    seen.add(v)
                    stack.append(v)
        comps.append(comp)
    return comps


def greedy_path_lower_bound(adj, repeats=6, rng=None):
    rng = rng or random
    n = len(adj)
    best = []
    starts = sorted(range(n), key=lambda x: len(adj[x]), reverse=True)[:max(1, min(n, repeats))]
    starts += [rng.randrange(n)] if n else []
    for s in starts:
        path = [s]
        used = {s}
        while True:
            opts = [v for v in adj[path[-1]] if v not in used]
            if not opts:
                break
            opts.sort(key=lambda v: (len([w for w in adj[v] if w not in used]), len(adj[v])), reverse=True)
            v = opts[0]
            path.append(v)
            used.add(v)
        if len(path) > len(best):
            best = path
    return best


def eval_state(state, lines, rng=None):
    cov = coverage_mask(state, lines)
    covered = cov.bit_count()
    missing_mask = FULL_MASK ^ cov
    old_missing = (missing_mask & OLD_WALL_MASK).bit_count()
    adj = stitch_graph(state, lines)
    comps = components(adj)
    max_comp = max((len(c) for c in comps), default=0)
    path = greedy_path_lower_bound(adj, rng=rng)
    edges = sum(len(a) for a in adj) // 2
    score = (
        covered * 100000
        + len(path) * 3500
        + max_comp * 1000
        + edges * 50
        - len(comps) * 2500
        - old_missing * 20000
        - abs(22 - len(state)) * 5000
    )
    return {
        'score': score,
        'covered_count': covered,
        'missing_mask': missing_mask,
        'old_missing': old_missing,
        'components': len(comps),
        'max_component_size': max_comp,
        'stitch_path_lower_bound': len(path),
        'stitch_path_nodes': path,
        'stitch_graph_edges': edges,
    }


def missing_points(mask):
    return [(x//2, y//2, z//2) for x, y, z in GRID if (mask >> GRID_INDEX[(x, y, z)]) & 1]


def make_output(state, lines, ev, args, shard, worker_id, attempts, mode):
    ordered = sorted(state, key=lambda i: (lines[i].a, lines[i].b))
    line_set = [lines[i].as_json() for i in ordered]
    raw = json.dumps(line_set, sort_keys=True, separators=(',', ':'))
    cid = 'mlct22-lineset-' + hashlib.sha256(raw.encode()).hexdigest()[:16]
    return {
        'schema': 'cover64-stitch-line-set-v1',
        'candidate_id': cid,
        'source_workflow': 'smart-search-17-cover64-stitch-graph',
        'source_shard': shard,
        'source_artifact': f'cover64-stitch-22-shard-{shard}',
        'mode': mode,
        'coordinate_scale': 2,
        'line_count': len(state),
        'links_target': 22,
        'covered_count': ev['covered_count'],
        'missing': missing_points(ev['missing_mask']),
        'missing_count': len(missing_points(ev['missing_mask'])),
        'stitch_components': ev['components'],
        'max_component_size': ev['max_component_size'],
        'stitch_path_lower_bound': ev['stitch_path_lower_bound'],
        'stitch_graph_edges': ev['stitch_graph_edges'],
        'score': ev['score'],
        'status': 'line_set_seed_not_a_trail',
        'interpretation': 'Unordered 22-line cover/stitch scaffold. This is not yet a certified polygonal trail.',
        'parameters': {
            'seconds': args.seconds,
            'seed': args.seed,
            'shard': shard,
            'shards': args.shards,
            'worker_id': worker_id,
            'box_min': args.box_min,
            'box_max': args.box_max,
            'max_lines': args.max_lines,
            'min_line_cover': args.min_line_cover,
            'max_universe': args.max_universe,
        },
        'attempts': attempts,
        'line_set2': line_set,
    }


def greedy_cover(rng, lines, max_lines, bias_wall=True):
    state = []
    covered = 0
    while len(state) < max_lines and covered != FULL_MASK:
        miss = FULL_MASK ^ covered
        scored = []
        sample_n = min(len(lines), 700)
        sample = rng.sample(range(len(lines)), sample_n) if len(lines) > sample_n else range(len(lines))
        for i in sample:
            if i in state:
                continue
            gain = (lines[i].mask & miss).bit_count()
            if gain == 0:
                continue
            wall_gain = (lines[i].mask & OLD_WALL_MASK & miss).bit_count()
            scored.append((gain * 100 + wall_gain * (80 if bias_wall else 20) + rng.random(), i))
        if not scored:
            break
        scored.sort(reverse=True)
        pick_pool = scored[:min(12, len(scored))]
        _, i = rng.choice(pick_pool)
        state.append(i)
        covered |= lines[i].mask
    while len(state) < max_lines:
        i = rng.randrange(len(lines))
        if i not in state:
            state.append(i)
    return state


def mutate(state, lines, rng, max_lines):
    state = list(state)
    cov = coverage_mask(state, lines)
    miss = FULL_MASK ^ cov
    # Remove weak lines.
    remove_n = rng.choice([1, 1, 2, 2, 3])
    utilities = []
    for i in state:
        others = cov & ~lines[i].mask
        unique = (lines[i].mask & ~others).bit_count()
        utilities.append((unique + rng.random(), i))
    utilities.sort()
    for _, i in utilities[:remove_n]:
        if i in state:
            state.remove(i)
    cov = coverage_mask(state, lines)
    miss = FULL_MASK ^ cov
    while len(state) < max_lines:
        pool = []
        sample_n = min(len(lines), 900)
        sample = rng.sample(range(len(lines)), sample_n) if len(lines) > sample_n else range(len(lines))
        for i in sample:
            if i in state:
                continue
            gain = (lines[i].mask & miss).bit_count()
            wall_gain = (lines[i].mask & OLD_WALL_MASK & miss).bit_count()
            touch = 0
            for j in state:
                if lines[i].mask & lines[j].mask:
                    touch += 1
            if gain or touch:
                pool.append((gain * 200 + wall_gain * 500 + min(touch, 5) * 35 + lines[i].cover_count * 5 + rng.random(), i))
        if not pool:
            break
        pool.sort(reverse=True)
        _, i = rng.choice(pool[:min(20, len(pool))])
        state.append(i)
        cov |= lines[i].mask
        miss = FULL_MASK ^ cov
    return state[:max_lines]


def worker(payload):
    args, shard, worker_id, seed_pairs = payload
    rng = random.Random(args.seed + 1000003 * shard + 9176 * worker_id)
    lines = build_universe(args.box_min, args.box_max, args.min_line_cover, args.max_universe)
    by_pair = {canonical_pair(x.a, x.b): i for i, x in enumerate(lines)}
    seed_state = []
    for a, b in seed_pairs:
        idx = by_pair.get(canonical_pair(a, b))
        if idx is not None and idx not in seed_state:
            seed_state.append(idx)
    while len(seed_state) < args.max_lines:
        i = rng.randrange(len(lines))
        if i not in seed_state:
            seed_state.append(i)

    if shard % 5 == 0:
        mode = 'cover64_from_seed_rewire'
    elif shard % 5 == 1:
        mode = 'cover64_stitch_connectivity_pressure'
    elif shard % 5 == 2:
        mode = 'old_wall_line_injection'
    elif shard % 5 == 3:
        mode = 'random_greedy_cover64_scaffold'
    else:
        mode = 'component_bridge_pressure'

    best_state = seed_state[:args.max_lines]
    best_ev = eval_state(best_state, lines, rng)
    cur_state = list(best_state)
    cur_ev = dict(best_ev)
    attempts = 0
    deadline = time.time() + args.seconds
    temp0 = 3500.0
    while time.time() < deadline:
        attempts += 1
        if attempts % 251 == 0 or (mode == 'random_greedy_cover64_scaffold' and attempts % 17 == 0):
            cand = greedy_cover(rng, lines, args.max_lines, bias_wall=(mode != 'random_greedy_cover64_scaffold'))
        else:
            cand = mutate(cur_state, lines, rng, args.max_lines)
        ev = eval_state(cand, lines, rng)
        temp = max(50.0, temp0 * (1.0 - min(0.95, attempts / 250000.0)))
        if ev['score'] >= cur_ev['score'] or rng.random() < math.exp((ev['score'] - cur_ev['score']) / temp):
            cur_state, cur_ev = cand, ev
        if (
            ev['covered_count'], ev['stitch_path_lower_bound'], ev['max_component_size'], -ev['components'], ev['score']
        ) > (
            best_ev['covered_count'], best_ev['stitch_path_lower_bound'], best_ev['max_component_size'], -best_ev['components'], best_ev['score']
        ):
            best_state, best_ev = cand, ev
    return make_output(best_state, lines, best_ev, args, shard, worker_id, attempts, mode)


def main():
    ap = argparse.ArgumentParser(description='Search 22-line 64-cover scaffolds with strong stitch graphs.')
    ap.add_argument('--seed-line-set', type=Path, default=Path('data/search17/local_cover64_stitch_graph_seed.json'))
    ap.add_argument('--out', type=Path, required=True)
    ap.add_argument('--seconds', type=int, default=180)
    ap.add_argument('--workers', type=int, default=4)
    ap.add_argument('--seed', type=int, default=20260717)
    ap.add_argument('--shard', type=int, default=0)
    ap.add_argument('--shards', type=int, default=20)
    ap.add_argument('--box-min', type=int, default=-1)
    ap.add_argument('--box-max', type=int, default=4)
    ap.add_argument('--max-lines', type=int, default=22)
    ap.add_argument('--min-line-cover', type=int, default=2)
    ap.add_argument('--max-universe', type=int, default=9000)
    args = ap.parse_args()

    seed_pairs = load_line_set(args.seed_line_set)
    payloads = [(args, args.shard, w, seed_pairs) for w in range(max(1, args.workers))]
    if args.workers <= 1:
        results = [worker(payloads[0])]
    else:
        with mp.Pool(processes=args.workers) as pool:
            results = pool.map(worker, payloads)
    results.sort(key=lambda r: (r['covered_count'], r['stitch_path_lower_bound'], r['max_component_size'], -r['stitch_components'], r['score']), reverse=True)
    best = results[0]
    best['worker_results'] = [
        {
            'worker_id': r['parameters']['worker_id'],
            'covered_count': r['covered_count'],
            'stitch_path_lower_bound': r['stitch_path_lower_bound'],
            'stitch_components': r['stitch_components'],
            'max_component_size': r['max_component_size'],
            'score': r['score'],
            'attempts': r['attempts'],
            'mode': r['mode'],
        }
        for r in results
    ]
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(best, indent=2, sort_keys=True))
    print(json.dumps({
        'out': str(args.out),
        'covered_count': best['covered_count'],
        'line_count': best['line_count'],
        'stitch_path_lower_bound': best['stitch_path_lower_bound'],
        'stitch_components': best['stitch_components'],
        'max_component_size': best['max_component_size'],
        'candidate_id': best['candidate_id'],
    }, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
