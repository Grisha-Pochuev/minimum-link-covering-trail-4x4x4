from __future__ import annotations

import argparse
import json
from pathlib import Path

GRID = [(2*x, 2*y, 2*z) for x in range(4) for y in range(4) for z in range(4)]
GRID_INDEX = {p: i for i, p in enumerate(GRID)}


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


def load_lines(data):
    if data.get('line_set2'):
        return [(tuple(map(int, a)), tuple(map(int, b))) for a, b in data['line_set2']]
    if data.get('line_set'):
        return [
            ((2*int(a[0]), 2*int(a[1]), 2*int(a[2])), (2*int(b[0]), 2*int(b[1]), 2*int(b[2])))
            for a, b in data['line_set']
        ]
    raise ValueError('No line_set2 or line_set found')


def stitch_stats(masks, node_limit=300000):
    n = len(masks)
    adj = [set() for _ in range(n)]
    for i in range(n):
        for j in range(i+1, n):
            if masks[i] & masks[j]:
                adj[i].add(j)
                adj[j].add(i)

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

    best = []
    nodes = 0

    def dfs(u, path, used):
        nonlocal best, nodes
        nodes += 1
        if len(path) > len(best):
            best = path[:]
        if nodes >= node_limit:
            return
        if len(path) + (n - len(used)) <= len(best):
            return
        ns = sorted((v for v in adj[u] if v not in used), key=lambda x: len(adj[x]), reverse=True)
        for v in ns:
            used.add(v)
            path.append(v)
            dfs(v, path, used)
            path.pop()
            used.remove(v)
            if nodes >= node_limit:
                return

    for s in sorted(range(n), key=lambda x: len(adj[x]), reverse=True):
        dfs(s, [s], {s})
        if len(best) == n or nodes >= node_limit:
            break

    return {
        'components': len(comps),
        'max_component_size': max((len(c) for c in comps), default=0),
        'stitch_path_lower_bound': len(best),
        'stitch_path_nodes': best,
        'stitch_graph_edges': sum(len(a) for a in adj) // 2,
        'search_nodes_used': nodes,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('json_file', type=Path)
    ap.add_argument('--expect-covered', type=int)
    ap.add_argument('--max-lines', type=int, default=22)
    ap.add_argument('--min-stitch-path', type=int)
    args = ap.parse_args()

    data = json.loads(args.json_file.read_text())
    lines = load_lines(data)
    if len(lines) > args.max_lines:
        raise SystemExit(f'line count {len(lines)} exceeds max {args.max_lines}')
    masks = []
    covered = 0
    bad = []
    for i, (a, b) in enumerate(lines):
        if a == b:
            bad.append({'index': i, 'reason': 'zero_length', 'line': [a, b]})
            masks.append(0)
            continue
        m = mask_for_line(a, b)
        if m == 0:
            bad.append({'index': i, 'reason': 'covers_no_grid_points', 'line': [a, b]})
        masks.append(m)
        covered |= m
    missing = [(x//2, y//2, z//2) for x, y, z in GRID if not (covered >> GRID_INDEX[(x, y, z)]) & 1]
    st = stitch_stats(masks)
    report = {
        'file': str(args.json_file),
        'line_count': len(lines),
        'covered_count': covered.bit_count(),
        'missing_count': len(missing),
        'missing': missing,
        'bad_lines': bad,
        **st,
    }
    print(json.dumps(report, indent=2, sort_keys=True))
    if bad:
        raise SystemExit('bad line-set entries found')
    if args.expect_covered is not None and covered.bit_count() != args.expect_covered:
        raise SystemExit(f"covered_count {covered.bit_count()} != expected {args.expect_covered}")
    if args.min_stitch_path is not None and st['stitch_path_lower_bound'] < args.min_stitch_path:
        raise SystemExit(f"stitch_path_lower_bound {st['stitch_path_lower_bound']} < expected {args.min_stitch_path}")


if __name__ == '__main__':
    main()
