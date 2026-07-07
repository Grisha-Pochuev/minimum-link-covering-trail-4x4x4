#!/usr/bin/env python3
"""Exact scaled-coordinate checker for 4x4x4 polygonal trails.

Accepts JSON objects with either:
  - vertices2: coordinates scaled by coordinate_scale (default 2), or
  - vertices: ordinary unscaled integer coordinates.

The checker is intentionally dependency-free and prints a machine-readable JSON report.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Iterable, List, Sequence, Tuple

Point = Tuple[int, int, int]


def sub(a: Point, b: Point) -> Point:
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def dot(a: Point, b: Point) -> int:
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def cross(a: Point, b: Point) -> Point:
    return (
        a[1] * b[2] - a[2] * b[1],
        a[2] * b[0] - a[0] * b[2],
        a[0] * b[1] - a[1] * b[0],
    )


def on_segment(a: Point, b: Point, p: Point) -> bool:
    d = sub(b, a)
    if d == (0, 0, 0):
        return p == a
    ap = sub(p, a)
    if cross(d, ap) != (0, 0, 0):
        return False
    t = dot(ap, d)
    return 0 <= t <= dot(d, d)


def as_point_list(raw: object, scale: int) -> List[Point]:
    if not isinstance(raw, list):
        raise ValueError("vertices must be a list")
    out: List[Point] = []
    for item in raw:
        if not (isinstance(item, list) or isinstance(item, tuple)) or len(item) != 3:
            raise ValueError(f"bad vertex: {item!r}")
        out.append((int(item[0]), int(item[1]), int(item[2])))
    return out


def read_vertices(path: Path) -> tuple[List[Point], int]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(data, list):
        return as_point_list(data, 1), 1
    if not isinstance(data, dict):
        raise ValueError("JSON must be either a list of vertices or an object")
    scale = int(data.get("coordinate_scale", 2))
    if data.get("vertices2") is not None:
        return as_point_list(data["vertices2"], scale), scale
    if data.get("vertices") is not None:
        verts = as_point_list(data["vertices"], 1)
        return [(scale * x, scale * y, scale * z) for x, y, z in verts], scale
    raise ValueError("JSON object must contain vertices2 or vertices")


def covered_points(vertices: Sequence[Point], scale: int) -> List[Point]:
    grid: List[Point] = [(scale * x, scale * y, scale * z) for x in range(4) for y in range(4) for z in range(4)]
    covered = set()
    for a, b in zip(vertices, vertices[1:]):
        for p in grid:
            if on_segment(a, b, p):
                covered.add(p)
    return sorted(covered)


def unscale_point(p: Point, scale: int) -> list[int]:
    if all(v % scale == 0 for v in p):
        return [v // scale for v in p]
    return list(p)


def main() -> int:
    parser = argparse.ArgumentParser(description="Check a scaled-coordinate trail for {0,1,2,3}^3")
    parser.add_argument("json_file", type=Path)
    parser.add_argument("--expected-links", type=int, default=None)
    parser.add_argument("--min-covered", type=int, default=None)
    parser.add_argument("--require-full", action="store_true")
    args = parser.parse_args()

    vertices, scale = read_vertices(args.json_file)
    links = max(0, len(vertices) - 1)
    covered = covered_points(vertices, scale)
    covered_set = set(covered)
    grid = [(scale * x, scale * y, scale * z) for x in range(4) for y in range(4) for z in range(4)]
    missing = [p for p in grid if p not in covered_set]

    report = {
        "file": str(args.json_file),
        "coordinate_scale": scale,
        "vertices": len(vertices),
        "links": links,
        "covered_count": len(covered),
        "grid_points": 64,
        "missing_count": len(missing),
        "missing": [unscale_point(p, scale) for p in missing],
    }
    print(json.dumps(report, indent=2, sort_keys=True))

    ok = True
    if args.expected_links is not None and links != args.expected_links:
        print(f"ERROR: expected {args.expected_links} links, got {links}")
        ok = False
    if args.min_covered is not None and len(covered) < args.min_covered:
        print(f"ERROR: covered_count {len(covered)} < min_covered {args.min_covered}")
        ok = False
    if args.require_full and missing:
        print("ERROR: trail does not cover all 64 grid points")
        ok = False
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
