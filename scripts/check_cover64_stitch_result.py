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

def load_lines(data):
    raw = data.get("lines2") or data.get("unordered_lines2")
    if not raw:
        raise ValueError("No lines2/unordered_lines2 found")
    lines = []
    for item in raw:
        if len(item) != 2:
            raise ValueError(f"bad line item: {item!r}")
        a = tuple(map(int, item[0]))
        b = tuple(map(int, item[1]))
        if a == b:
            raise ValueError(f"zero-length line is not allowed: {item!r}")
        lines.append((a, b))
    return lines

def coverage(lines):
    covered = set()
    for a, b in lines:
        for p in GRID:
            if on_segment(a, b, p):
                covered.add(p)
    missing = [(x//2, y//2, z//2) for x, y, z in GRID if (x, y, z) not in covered]
    return covered, missing

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("json_file", type=Path)
    ap.add_argument("--expect-cover64", action="store_true")
    ap.add_argument("--min-covered", type=int, default=None)
    ap.add_argument("--max-lines", type=int, default=22)
    args = ap.parse_args()

    data = json.loads(args.json_file.read_text())
    lines = load_lines(data)
    covered, missing = coverage(lines)
    out = {
        "file": str(args.json_file),
        "line_count": len(lines),
        "covered_count": len(covered),
        "missing_count": len(missing),
        "missing": missing,
        "declared_covered_count": data.get("covered_count"),
        "declared_line_count": data.get("line_count"),
        "overlap_greedy_path": data.get("overlap_greedy_path"),
        "endpoint_greedy_path": data.get("endpoint_greedy_path"),
    }
    print(json.dumps(out, indent=2, sort_keys=True))
    if len(lines) > args.max_lines:
        raise SystemExit(f"line_count {len(lines)} exceeds max {args.max_lines}")
    if args.expect_cover64 and len(covered) != 64:
        raise SystemExit(f"covered_count {len(covered)} != 64")
    if args.min_covered is not None and len(covered) < args.min_covered:
        raise SystemExit(f"covered_count {len(covered)} < min {args.min_covered}")
    if data.get("covered_count") is not None and int(data["covered_count"]) != len(covered):
        raise SystemExit(f"declared covered_count {data['covered_count']} != recomputed {len(covered)}")
    if data.get("line_count") is not None and int(data["line_count"]) != len(lines):
        raise SystemExit(f"declared line_count {data['line_count']} != recomputed {len(lines)}")

if __name__ == "__main__":
    main()
