from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any, Iterable

from candidate_symmetry import canonical_path_key, has_usable_vertices, inferred_links


def load_json_records(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []

    if path.suffix == ".jsonl":
        records: list[dict[str, Any]] = []
        for line in path.read_text().splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                value = json.loads(line)
            except json.JSONDecodeError:
                continue
            if isinstance(value, dict):
                records.extend(collect_candidate_records(value))
        return records

    try:
        value = json.loads(path.read_text())
    except json.JSONDecodeError:
        return []
    return collect_candidate_records(value)


def collect_candidate_records(value: Any) -> list[dict[str, Any]]:
    """Recursively collect candidate-like dicts from JSON artifacts."""
    out: list[dict[str, Any]] = []
    if isinstance(value, dict):
        if has_usable_vertices(value):
            out.append(value)
        for child in value.values():
            out.extend(collect_candidate_records(child))
    elif isinstance(value, list):
        for item in value:
            out.extend(collect_candidate_records(item))
    return out


def source_runs(record: dict[str, Any]) -> set[str]:
    runs: set[str] = set()
    value = record.get("source_runs")
    if isinstance(value, list):
        runs.update(str(v) for v in value if v is not None)
    elif value is not None:
        runs.add(str(value))
    for key in ("source_run", "run_id", "workflow_run_id", "source_workflow_run_id"):
        if record.get(key) is not None:
            runs.add(str(record[key]))
    return runs


def merge_metadata(existing: dict[str, Any], incoming: dict[str, Any]) -> None:
    existing["source_occurrence_count"] = int(existing.get("source_occurrence_count", 1)) + 1
    runs = set(str(v) for v in existing.get("source_runs", []) if v is not None)
    runs.update(source_runs(incoming))
    if runs:
        existing["source_runs"] = sorted(runs)

    sources = list(existing.get("source_files", []))
    incoming_file = incoming.get("seed_source_file") or incoming.get("source_file")
    if incoming_file is not None and str(incoming_file) not in sources:
        sources.append(str(incoming_file))
    if sources:
        existing["source_files"] = sources


def candidate_is_eligible(record: dict[str, Any], min_covered: int, max_links: int) -> bool:
    try:
        if int(record.get("covered_count", 0)) < min_covered:
            return False
    except (TypeError, ValueError):
        return False
    links = inferred_links(record)
    if links is None or links > max_links:
        return False
    return has_usable_vertices(record)


def candidate_id_from_key(key: str) -> str:
    return "mlct22-" + hashlib.sha256(key.encode("utf-8")).hexdigest()[:16]


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Merge new candidates into candidates/bank.jsonl using symmetry-aware deduplication."
    )
    ap.add_argument("--bank", default="candidates/bank.jsonl")
    ap.add_argument("--out", default=None, help="Output JSONL path. Defaults to overwriting --bank.")
    ap.add_argument("--min-covered", type=int, default=56)
    ap.add_argument("--max-links", type=int, default=22)
    ap.add_argument("inputs", nargs="+", help="JSON or JSONL candidate/artifact files to merge into the bank.")
    args = ap.parse_args()

    bank_path = Path(args.bank)
    out_path = Path(args.out) if args.out else bank_path

    bank_records = load_json_records(bank_path)
    merged: list[dict[str, Any]] = []
    by_key: dict[str, dict[str, Any]] = {}

    for record in bank_records:
        if not candidate_is_eligible(record, args.min_covered, args.max_links):
            continue
        key = canonical_path_key(record)
        if not key:
            continue
        record.setdefault("candidate_id", candidate_id_from_key(key))
        record.setdefault("canonical_key_sha256", hashlib.sha256(key.encode("utf-8")).hexdigest())
        if key in by_key:
            merge_metadata(by_key[key], record)
            continue
        by_key[key] = record
        merged.append(record)

    scanned_new = 0
    added_new = 0
    merged_duplicates = 0
    rejected = 0

    for input_name in args.inputs:
        input_path = Path(input_name)
        for record in load_json_records(input_path):
            scanned_new += 1
            if not candidate_is_eligible(record, args.min_covered, args.max_links):
                rejected += 1
                continue
            key = canonical_path_key(record)
            if not key:
                rejected += 1
                continue
            record.setdefault("candidate_id", candidate_id_from_key(key))
            record.setdefault("canonical_key_sha256", hashlib.sha256(key.encode("utf-8")).hexdigest())
            record.setdefault("source_file", str(input_path))
            if key in by_key:
                merge_metadata(by_key[key], record)
                merged_duplicates += 1
                continue
            by_key[key] = record
            merged.append(record)
            added_new += 1

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("".join(json.dumps(record, sort_keys=True) + "\n" for record in merged))

    summary = {
        "schema": "mlct-candidate-bank-merge-v1",
        "dedupe_rule": "canonical modulo coordinate permutations, cube reflections, and trail reversal",
        "bank_in": str(bank_path),
        "bank_out": str(out_path),
        "min_covered": args.min_covered,
        "max_links": args.max_links,
        "existing_unique_after_canonicalization": len(bank_records),
        "final_unique": len(merged),
        "scanned_new_records": scanned_new,
        "added_new_unique": added_new,
        "merged_symmetric_or_exact_duplicates": merged_duplicates,
        "rejected_records": rejected,
    }
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
