from __future__ import annotations

import argparse
import json
from pathlib import Path

GRID = [(2*x, 2*y, 2*z) for x in range(4) for y in range(4) for z in range(4)]

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
        return p == a
    ap = sub(p, a)
    return cross(d, ap) == (0, 0, 0) and 0 <= dot(ap, d) <= dot(d, d)

def load_vertices(data):
    if data.get('vertices2'):
        scale = int(data.get('coordinate_scale', 2) or 2)
        if scale == 2:
            return [tuple(map(int, p)) for p in data['vertices2']]
        return [tuple(round(2*int(x)/scale) for x in p) for p in data['vertices2']]
    if data.get('vertices'):
        return [(2*int(x), 2*int(y), 2*int(z)) for x, y, z in data['vertices']]
    raise ValueError('No vertices2 or vertices found')

def coverage(vertices):
    covered = set()
    for a, b in zip(vertices, vertices[1:]):
        for p in GRID:
            if on_segment(a, b, p):
                covered.add(p)
    missing = [(x//2, y//2, z//2) for x, y, z in GRID if (x, y, z) not in covered]
    return covered, missing

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('json_file', type=Path)
    ap.add_argument('--expect-covered', type=int)
    ap.add_argument('--max-links', type=int, default=22)
    args = ap.parse_args()

    data = json.loads(args.json_file.read_text())
    vertices = load_vertices(data)
    covered, missing = coverage(vertices)
    links = len(vertices) - 1
    print(json.dumps({
        'file': str(args.json_file),
        'links': links,
        'covered_count': len(covered),
        'missing_count': len(missing),
        'missing': missing,
    }, indent=2, sort_keys=True))
    if links > args.max_links:
        raise SystemExit(f'links {links} exceeds max {args.max_links}')
    if args.expect_covered is not None and len(covered) != args.expect_covered:
        raise SystemExit(f'covered_count {len(covered)} != expected {args.expect_covered}')

if __name__ == '__main__':
    main()
