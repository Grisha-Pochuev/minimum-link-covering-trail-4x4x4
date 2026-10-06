#!/usr/bin/env python3
"""Primary exact verifier for search-26 trail banks.

Uses the repository's established exact rational geometry
(scripts/bridge_compress_common.py, the same code path as
scripts/check_rational_trail.py) in batch form.

Usage: verify_search26_primary.py BANK.jsonl [...] --report OUT.json
Fails (exit 1) on wrong link count, zero-length link, covered count below the
claimed count, missing-list mismatch, or malformed rows.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import bridge_compress_common as bc  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("banks", nargs="+")
    ap.add_argument("--report", required=True)
    ap.add_argument("--expected-links", type=int, default=22)
    args = ap.parse_args()
    report = {"schema": "search26-verifier-report-v1", "verifier": "primary-bridge-compress-common", "files": [], "status": "pass"}
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
                    row = json.loads(line)
                    verts = bc.load_vertices({"vertices": row["vertices"]})
                    problems = []
                    if any(a == b for a, b in zip(verts, verts[1:])):
                        problems.append("zero-length link")
                    rep = bc.analyze(verts)
                    if rep["links"] != args.expected_links:
                        problems.append(f"links={rep['links']}")
                    if rep["covered_count"] < int(row["claimed_covered"]):
                        problems.append(f"covered {rep['covered_count']} < claimed {row['claimed_covered']}")
                    if "missing" in row and row["missing"] != rep["missing"]:
                        problems.append("missing list mismatch")
                    best = max(best, rep["covered_count"])
                    if problems:
                        bad.append({"row": n, "problems": problems})
                except Exception as exc:
                    bad.append({"row": n, "problems": [f"exception: {exc}"]})
        report["files"].append({"path": path, "rows": rows, "failures": len(bad), "best_covered": best, "examples": bad[:5]})
        if bad:
            report["status"] = "fail"
    with open(args.report, "w", encoding="utf-8") as fh:
        json.dump(report, fh, indent=2, sort_keys=True)
        fh.write("\n")
    print(json.dumps({"verifier": "primary", "status": report["status"], "files": [(f["path"], f["rows"], f["failures"]) for f in report["files"]]}))
    return 0 if report["status"] == "pass" else 1


if __name__ == "__main__":
    sys.exit(main())
