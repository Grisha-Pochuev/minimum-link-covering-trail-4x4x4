#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

FAMILY_IDS = [
    "mlct22-er-1b9d545440a3ee2b",
    "mlct22-er-44b7464ef2bba268",
    "mlct22-er-763db4ef21aeba80",
    "mlct22-er-7671ee46bd711a25",
    "mlct22-er-592cdba87b09cf5e",
    "mlct22-er-84b471c2367a34e7",
    "mlct22-er-579fc6ba3b315bf0",
]
DONOR_IDS = [
    "mlct22-er-7617f3333d5bd4a7",
    "mlct22-er-222e6539aa735a14",
    "mlct22-er-8636131b79055dbe",
    "mlct22-er-6ea2d43af05081b7",
    "mlct22-er-cf89ed8c63871970",
]
KEEP = ("candidate_id", "covered_count", "missing", "vertices2")


def load(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def compact(row: dict) -> dict:
    return {key: row[key] for key in KEEP}


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(compact(r), separators=(",", ":")) + "\n" for r in rows), encoding="utf-8")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--verified62", type=Path, required=True)
    ap.add_argument("--compact", dest="compact_path", type=Path, required=True)
    ap.add_argument("--repo", type=Path, default=Path("."))
    ap.add_argument("--parts", type=int, default=4)
    args = ap.parse_args()

    parents = load(args.verified62)
    all_rows = load(args.compact_path)
    if len(parents) != 1053:
        raise AssertionError(f"expected 1053 verified 62/64 rows, got {len(parents)}")
    if any(int(r["covered_count"]) != 62 for r in parents):
        raise AssertionError("verified62 input contains a non-62 row")
    by_id = {r["candidate_id"]: r for r in parents + all_rows}
    missing = [x for x in FAMILY_IDS + DONOR_IDS if x not in by_id]
    if missing:
        raise AssertionError(f"missing required ids: {missing}")

    root = args.repo / "data"
    parts_dir = root / "search23_verified62_seed_parts"
    parts_dir.mkdir(parents=True, exist_ok=True)
    for old in parts_dir.glob("part-*.jsonlpart"):
        old.unlink()
    for index in range(args.parts):
        write_jsonl(parts_dir / f"part-{index:02d}.jsonlpart", parents[index::args.parts])

    donors = [by_id[x] for x in DONOR_IDS]
    required = [by_id[x] for x in FAMILY_IDS + DONOR_IDS]
    write_jsonl(root / "search23_core_diverse_donors.jsonl", donors)
    write_jsonl(root / "search23_required_seeds.jsonl", required)

    manifest = {
        "schema": "search23-materialized-seeds-v1",
        "parent_count": len(parents),
        "part_count": args.parts,
        "donor_count": len(donors),
        "required_seed_count": len(required),
        "source_verified62": str(args.verified62),
        "source_compact": str(args.compact_path),
    }
    (root / "search23_seed_materialization.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
