#!/usr/bin/env python3
"""Aggregate smart-search-18 order-from-cover64-stitch shard outputs."""
from __future__ import annotations

import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Dict, List


def load_json(path: Path) -> dict | None:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None
    return data if isinstance(data, dict) else None


def candidate_key(row: dict) -> str:
    if row.get("vertices2"):
        payload = json.dumps(row["vertices2"], separators=(",", ":"))
        return hashlib.sha256(payload.encode()).hexdigest()
    payload = json.dumps(row.get("line_order", []), separators=(",", ":")) + str(row.get("source_shard"))
    return hashlib.sha256(payload.encode()).hexdigest()


def score_tuple(row: dict) -> tuple:
    return (
        int(row.get("links", 0) or 0),
        int(row.get("covered_count", 0) or 0),
        -int(row.get("weak_links", 999) or 999),
        int(row.get("score", 0) or 0),
    )


def main() -> int:
    root = Path("collected")
    rows: List[dict] = []
    for p in sorted(root.rglob("order_from_cover64_best_shard_*.json")):
        d = load_json(p)
        if d:
            d.setdefault("_file", str(p))
            rows.append(d)
    for p in sorted(root.rglob("preferred_order_from_cover64_shard_*.jsonl")):
        for line in p.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            try:
                d = json.loads(line)
            except Exception:
                continue
            if isinstance(d, dict):
                d.setdefault("_file", str(p))
                rows.append(d)

    unique: Dict[str, dict] = {}
    for row in rows:
        key = candidate_key(row)
        row.setdefault("ordered_candidate_key_sha256", key)
        if key not in unique or score_tuple(row) > score_tuple(unique[key]):
            unique[key] = row

    compact = sorted(unique.values(), key=score_tuple, reverse=True)
    best = compact[0] if compact else None

    mode_breakdown: dict[str, dict[str, Any]] = {}
    by_mode: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        by_mode[str(row.get("mode", "unknown"))].append(row)
    for mode, items in sorted(by_mode.items()):
        best_mode = max(items, key=score_tuple)
        mode_breakdown[mode] = {
            "count": len(items),
            "best_links": int(best_mode.get("links", 0) or 0),
            "best_covered": int(best_mode.get("covered_count", 0) or 0),
            "best_weak_links": int(best_mode.get("weak_links", 0) or 0),
            "unique_compact": len({candidate_key(x) for x in items}),
        }

    link_hist = Counter(int(x.get("links", 0) or 0) for x in rows)
    coverage_hist = Counter(int(x.get("covered_count", 0) or 0) for x in rows)
    missing_counter = Counter()
    for row in rows:
        for p in row.get("missing", []) or []:
            missing_counter[tuple(p)] += 1

    summary = {
        "schema": "contact-aware-ordering-summary-v1",
        "interpretation": "ordered reconstruction attempts from search-17 cover64 line-set scaffolds",
        "result_count": len(rows),
        "unique_ordered_candidates": len(compact),
        "best_links": int(best.get("links", 0) or 0) if best else 0,
        "best_covered_count": int(best.get("covered_count", 0) or 0) if best else 0,
        "best_missing_count": int(best.get("missing_count", 64) or 64) if best else 64,
        "best": best,
        "mode_breakdown": mode_breakdown,
        "link_histogram": [{"links": k, "count": v} for k, v in sorted(link_hist.items(), reverse=True)],
        "coverage_histogram": [{"covered_count": k, "count": v} for k, v in sorted(coverage_hist.items(), reverse=True)],
        "top_missing_points": [
            {"point": list(p), "count": c}
            for p, c in missing_counter.most_common(20)
        ],
    }

    out_json = root / "order_from_cover64_stitch_run_summary.json"
    out_md = root / "order_from_cover64_stitch_run_summary.md"
    out_jsonl = root / "order-from-cover64-candidates.jsonl"

    out_json.write_text(json.dumps(summary, indent=2, sort_keys=True), encoding="utf-8")
    with out_jsonl.open("w", encoding="utf-8") as f:
        for row in compact[:200]:
            f.write(json.dumps(row, sort_keys=True) + "\n")

    lines = []
    lines.append("# order-from-cover64-stitch run summary")
    lines.append("")
    lines.append("These are contact-aware ordered reconstruction attempts from search-17 line-set scaffolds.")
    lines.append("")
    lines.append(f"- result rows: `{len(rows)}`")
    lines.append(f"- unique ordered candidates: `{len(compact)}`")
    if best:
        lines.append(f"- best candidate: `{best.get('candidate_id')}`")
        lines.append(f"- best links: `{best.get('links')}`")
        lines.append(f"- best covered_count: `{best.get('covered_count')} / 64`")
        lines.append(f"- best missing_count: `{best.get('missing_count')}`")
        lines.append(f"- best mode: `{best.get('mode')}`")
        lines.append(f"- best source shard: `{best.get('source_shard')}`")
    lines.append("")
    lines.append("## Mode breakdown")
    lines.append("")
    lines.append("| mode | rows | unique | best links | best covered |")
    lines.append("|---|---:|---:|---:|---:|")
    for mode, info in mode_breakdown.items():
        lines.append(f"| `{mode}` | {info['count']} | {info['unique_compact']} | {info['best_links']} | {info['best_covered']} |")
    lines.append("")
    lines.append("## Top candidates")
    lines.append("")
    lines.append("| rank | candidate_id | mode | links | covered | missing | shard |")
    lines.append("|---:|---|---|---:|---:|---:|---:|")
    for idx, row in enumerate(compact[:20], 1):
        lines.append(
            f"| {idx} | `{row.get('candidate_id')}` | `{row.get('mode')}` | "
            f"{row.get('links')} | {row.get('covered_count')} | {row.get('missing_count')} | {row.get('source_shard')} |"
        )
    out_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps({"summary": str(out_json), "rows": len(rows), "unique": len(compact)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
