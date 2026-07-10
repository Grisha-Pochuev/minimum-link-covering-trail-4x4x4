#!/usr/bin/env python3
"""Primary exact checker for integer, half-integer, and arbitrary rational trails."""
from __future__ import annotations
import argparse, json
from pathlib import Path
import bridge_compress_common as bc


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("json_file", type=Path)
    ap.add_argument("--expected-links", type=int)
    ap.add_argument("--min-covered", type=int)
    ap.add_argument("--require-full", action="store_true")
    args = ap.parse_args()
    data = bc.read_json(args.json_file)
    vertices = bc.load_vertices(data)
    if any(a == b for a, b in zip(vertices, vertices[1:])):
        raise SystemExit("ERROR: zero-length link")
    report = bc.analyze(vertices)
    report.update({"file": str(args.json_file), "vertices": len(vertices), "exact_rational": True})
    print(json.dumps(report, indent=2, sort_keys=True))
    ok = True
    if args.expected_links is not None and report["links"] != args.expected_links:
        print(f"ERROR: expected {args.expected_links} links, got {report['links']}")
        ok = False
    if args.min_covered is not None and report["covered_count"] < args.min_covered:
        print(f"ERROR: covered_count {report['covered_count']} < {args.min_covered}")
        ok = False
    if args.require_full and report["covered_count"] != 64:
        print("ERROR: trail is not 64/64")
        ok = False
    if isinstance(data, dict):
        for key in ("links", "covered_count", "missing_count"):
            if key in data and int(data[key]) != int(report[key]):
                print(f"ERROR: stored {key}={data[key]} but recomputed {report[key]}")
                ok = False
        if "missing" in data and data["missing"] != report["missing"]:
            print("ERROR: stored missing list disagrees with exact recomputation")
            ok = False
    return 0 if ok else 1

if __name__ == "__main__":
    raise SystemExit(main())
