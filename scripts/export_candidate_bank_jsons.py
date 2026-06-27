from __future__ import annotations

import argparse
import json
from pathlib import Path

from candidate_symmetry import canonical_path_key, has_usable_vertices


def main() -> int:
    ap = argparse.ArgumentParser(description="Export JSONL candidate bank records into individual JSON seed files.")
    ap.add_argument("--out", default="seed-material/from-candidate-bank")
    ap.add_argument("--min-covered", type=int, default=56)
    ap.add_argument("files", nargs="*", default=["candidates/bank.jsonl"])
    args = ap.parse_args()

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    seen: set[str] = set()
    written = 0
    scanned = 0
    skipped_symmetric_duplicates = 0

    for name in args.files:
        path = Path(name)
        if not path.exists():
            continue
        for line_no, line in enumerate(path.read_text().splitlines(), start=1):
            line = line.strip()
            if not line:
                continue
            scanned += 1
            try:
                rec = json.loads(line)
            except json.JSONDecodeError:
                continue
            if int(rec.get("covered_count", 0)) < args.min_covered:
                continue
            if not has_usable_vertices(rec):
                continue
            key = canonical_path_key(rec)
            if not key:
                continue
            if key in seen:
                skipped_symmetric_duplicates += 1
                continue
            seen.add(key)
            cid = rec.get("candidate_id") or f"candidate_{written:04d}"
            rec.setdefault("seed_source_file", str(path))
            rec.setdefault("seed_source_line", line_no)
            (out / f"{written:04d}_{cid}.json").write_text(json.dumps(rec, sort_keys=True) + "\n")
            written += 1

    manifest = {
        "schema": "mlct-seed-export-v1",
        "dedupe_rule": "canonical modulo coordinate permutations, cube reflections, and trail reversal",
        "scanned_records": scanned,
        "written_seed_files": written,
        "skipped_symmetric_duplicates": skipped_symmetric_duplicates,
        "min_covered": args.min_covered,
    }
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
    print(json.dumps(manifest, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
