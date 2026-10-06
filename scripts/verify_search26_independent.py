#!/usr/bin/env python3
"""Independent exact verifier for search-26 trail banks (integer arithmetic only).

Shares no code with the engine, with search26_common.py or with the repository's
bridge_compress_common.py.  Every vertex is parsed as an exact rational, the whole
trail is scaled by the LCM of all denominators, and incidence is decided with
integer cross and dot products.

Usage: verify_search26_independent.py BANK.jsonl [BANK2.jsonl ...] --report OUT.json
Each row must contain "vertices" (list of 3 strings/ints) and "claimed_covered".
Fails (exit 1) on: wrong link count, zero-length link, covered count lower than
claimed, missing list mismatch, or malformed rows.
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from fractions import Fraction


def parse(v) -> Fraction:
    if isinstance(v, int):
        return Fraction(v)
    if isinstance(v, str):
        return Fraction(v)
    raise ValueError(f"non-exact coordinate {v!r}")


def check_row(row: dict, expected_links: int) -> dict:
    verts = [[parse(c) for c in v] for v in row["vertices"]]
    if any(len(v) != 3 for v in verts):
        raise ValueError("vertex without 3 coordinates")
    den = 1
    for v in verts:
        for c in v:
            den = den * c.denominator // math.gcd(den, c.denominator)
    iv = [[int(c * den) for c in v] for v in verts]
    links = len(iv) - 1
    problems = []
    if links != expected_links:
        problems.append(f"links={links} expected {expected_links}")
    for a, b in zip(iv, iv[1:]):
        if a == b:
            problems.append("zero-length link")
            break
    covered = set()
    for a, b in zip(iv, iv[1:]):
        d = [b[i] - a[i] for i in range(3)]
        dd = d[0] * d[0] + d[1] * d[1] + d[2] * d[2]
        if dd == 0:
            continue
        for x in range(4):
            for y in range(4):
                for z in range(4):
                    g = (x * den, y * den, z * den)
                    w = [g[i] - a[i] for i in range(3)]
                    cr = (d[1] * w[2] - d[2] * w[1], d[2] * w[0] - d[0] * w[2], d[0] * w[1] - d[1] * w[0])
                    if cr != (0, 0, 0):
                        continue
                    t = d[0] * w[0] + d[1] * w[1] + d[2] * w[2]
                    if 0 <= t <= dd:
                        covered.add((x, y, z))
    count = len(covered)
    claimed = int(row["claimed_covered"])
    if count < claimed:
        problems.append(f"covered {count} < claimed {claimed}")
    missing = sorted([x, y, z] for x in range(4) for y in range(4) for z in range(4) if (x, y, z) not in covered)
    if "missing" in row and row["missing"] != missing:
        problems.append("missing list mismatch")
    return {"links": links, "covered": count, "claimed": claimed, "problems": problems}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("banks", nargs="+")
    ap.add_argument("--report", required=True)
    ap.add_argument("--expected-links", type=int, default=22)
    args = ap.parse_args()
    report = {"schema": "search26-verifier-report-v1", "verifier": "independent-integer", "files": [], "status": "pass"}
    for path in args.banks:
        rows = 0
        bad = []
        best = 0
        with open(path, encoding="utf-8") as fh:
            for n, line in enumerate(fh):
                line = line.strip()
                if not line:
                    continue
                rows += 1
                try:
                    r = check_row(json.loads(line), args.expected_links)
                    best = max(best, r["covered"])
                    if r["problems"]:
                        bad.append({"row": n, "problems": r["problems"]})
                except Exception as exc:  # malformed row is a failure
                    bad.append({"row": n, "problems": [f"exception: {exc}"]})
        report["files"].append({"path": path, "rows": rows, "failures": len(bad), "best_covered": best, "examples": bad[:5]})
        if bad:
            report["status"] = "fail"
    with open(args.report, "w", encoding="utf-8") as fh:
        json.dump(report, fh, indent=2, sort_keys=True)
        fh.write("\n")
    print(json.dumps({"verifier": "independent-integer", "status": report["status"], "files": [(f["path"], f["rows"], f["failures"]) for f in report["files"]]}))
    return 0 if report["status"] == "pass" else 1


if __name__ == "__main__":
    sys.exit(main())
