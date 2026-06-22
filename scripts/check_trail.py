#!/usr/bin/env python3
"""Check a covering trail for the 4x4x4 cubic grid.

The trail is a list of vertices. Consecutive vertices form straight segments.
A grid point is covered if it lies on at least one segment, including endpoints.

This checker is intentionally small and dependency-free so that other people can
verify results from GitHub Actions or local runs.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Iterable, List, Sequence, Tuple

Point = Tuple[int, int, int]

GRID: List[Point] = [(x, y, z) for x in range(4) for y in range(4) for z in range(4)]


def as_point_list(raw: object) -> List[Point]:
    if not isinstance(raw, list):
        raise ValueError("vertices must be a list")
    out: List[Point] = []
    for item in raw:
        if not (isinstance(item, list) or isinstance(item, tuple)) or len(item) != 3:
            raise ValueError(f"bad vertex: {item!r}")
        out.append((int(item[0]), int(item[1]), int(item[2])))
    return out


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
    """Return True if p lies on the closed segment a--b."""
    d = sub(b, a)
    if d == (0, 0, 0):
        return p == a
    ap = sub(p, a)
    if cross(d, ap) != (0, 0, 0):
        return False
    t = dot(ap, d)
    return 0 <= t <= dot(d, d)


def covered_points(vertices: Sequence[Point]) -> List[Point]:
    covered = set()
    for a, b in zip(vertices, vertices[1:]):
        for p in GRID:
            if on_segment(a, b, p):
                covered.add(p)
    return sorted(covered)


def read_vertices(path: Path) -> List[Point]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(data, list):
        return as_point_list(data)
    if not isinstance(data, dict):
        raise ValueError("JSON must be either a list of vertices or an object with a vertices field")
    return as_point_list(data.get("vertices"))


def main() -> int:
    parser = argparse.ArgumentParser(description="Check a covering trail for {0,1,2,3}^3")
    parser.add_argument("json_file", type=Path)
    parser.add_argument("--expected-links", type=int, default=None)
    parser.add_argument("--require-full", action="store_true")
    args = parser.parse_args()

    vertices = read_vertices(args.json_file)
    links = max(0, len(vertices) - 1)
    covered = covered_points(vertices)
    missing = [p for p in GRID if p not in covered]

    print(f"file: {args.json_file}")
    print(f"vertices: {len(vertices)}")
    print(f"links: {links}")
    print(f"covered_count: {len(covered)} / 64")
    print(f"missing: {missing}")

    ok = True
    if args.expected_links is not None and links != args.expected_links:
        print(f"ERROR: expected {args.expected_links} links, got {links}")
        ok = False
    if args.require_full and missing:
        print("ERROR: trail does not cover all 64 grid points")
        ok = False
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
