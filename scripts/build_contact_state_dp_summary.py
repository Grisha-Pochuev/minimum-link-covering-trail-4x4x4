#!/usr/bin/env python3
"""Aggregate smart-search-19 contact-state DP shard outputs."""
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
    metrics = row.get("contact_state_metrics") or {}
    return (
        int(row.get("links", 0) or 0),
        int(row.get("covered_count", 0) or 0),
        -int(metrics.get("total_lost_points_over_pieces", 999999) or 0),
        -int(row.get("weak_links", 999) or 999),
        int(metrics.get("official60_missing_hits", 0) or 0),
        int(row.get("score", 0) or 0),
    )


def add_loss_counters(row: dict, lost_counter: Counter, clipped_counter: Counter) -> None:
    report = row.get("contact_loss_report") or {}
    for item in report.get("top_lost_points", []) or []:
        p = tuple(item.get("point", []))
        if p:
            lost_counter[p] += int(item.get("count", 0) or 0)
    for item in report.get("top_clipped_rich_lines", []) or []:
        key = str(item.get("line_index"))
        clipped_counter[key] += int(item.get("lost_count", 0) or 0)


def main() -> int:
    root = Path("collected")
    rows: List[dict] = []
    for p in sorted(root.rglob("contact_state_dp_best_shard_*.json")):
        d = load_json(p)
        if d:
            d.setdefault("_file", str(p))
            rows.append(d)
    for p in sorted(root.rglob("preferred_contact_state_dp_shard_*.jsonl")):
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
            "best_total_lost_points": int((best_mode.get("contact_state_metrics") or {}).get("total_lost_points_over_pieces", 0) or 0),
            "unique_compact": len({candidate_key(x) for x in items}),
        }

    link_hist = Counter(int(x.get("links", 0) or 0) for x in rows)
    coverage_hist = Counter(int(x.get("covered_count", 0) or 0) for x in rows)
    missing_counter = Counter()
    lost_counter = Counter()
    clipped_counter = Counter()
    for row in rows:
        for p in row.get("missing", []) or []:
            missing_counter[tuple(p)] += 1
        add_loss_counters(row, lost_counter, clipped_counter)

    threshold_counts = {
        "above_44": sum(1 for x in compact if int(x.get("covered_count", 0) or 0) > 44),
        "above_50": sum(1 for x in compact if int(x.get("covered_count", 0) or 0) > 50),
        "above_56": sum(1 for x in compact if int(x.get("covered_count", 0) or 0) > 56),
        "above_60": sum(1 for x in compact if int(x.get("covered_count", 0) or 0) > 60),
        "at_least_61": sum(1 for x in compact if int(x.get("covered_count", 0) or 0) >= 61),
        "full_64": sum(1 for x in compact if int(x.get("covered_count", 0) or 0) >= 64),
    }

    summary = {
        "schema": "contact-state-dp-summary-v1",
        "interpretation": "contact-state DP/beam ordered reconstruction from search-17 cover64 line-set scaffolds",
        "result_count": len(rows),
        "unique_ordered_candidates": len(compact),
        "best_links": int(best.get("links", 0) or 0) if best else 0,
        "best_covered_count": int(best.get("covered_count", 0) or 0) if best else 0,
        "best_missing_count": int(best.get("missing_count", 64) or 64) if best else 64,
        "best": best,
        "threshold_counts": threshold_counts,
        "mode_breakdown": mode_breakdown,
        "link_histogram": [{"links": k, "count": v} for k, v in sorted(link_hist.items(), reverse=True)],
        "coverage_histogram": [{"covered_count": k, "count": v} for k, v in sorted(coverage_hist.items(), reverse=True)],
        "top_missing_points": [{"point": list(p), "count": c} for p, c in missing_counter.most_common(20)],
        "top_lost_points": [{"point": list(p), "count": c} for p, c in lost_counter.most_common(20)],
        "top_clipped_line_indices": [{"line_index": k, "loss_score": c} for k, c in clipped_counter.most_common(20)],
    }

    out_json = root / "contact_state_dp_run_summary.json"
    out_md = root / "contact_state_dp_run_summary.md"
    out_jsonl = root / "contact-state-dp-candidates.jsonl"

    out_json.write_text(json.dumps(summary, indent=2, sort_keys=True), encoding="utf-8")
    with out_jsonl.open("w", encoding="utf-8") as f:
        for row in compact[:300]:
            f.write(json.dumps(row, sort_keys=True) + "\n")

    lines = [
        "# contact-state-dp run summary",
        "",
        "These are contact-state DP/beam ordered reconstruction attempts from search-17 cover64 line-set scaffolds.",
        "",
        f"- result rows: `{len(rows)}`",
        f"- unique ordered candidates: `{len(compact)}`",
    ]
    if best:
        metrics = best.get("contact_state_metrics") or {}
        lines.extend([
            f"- best candidate: `{best.get('candidate_id')}`",
            f"- best links: `{best.get('links')}`",
            f"- best covered_count: `{best.get('covered_count')} / 64`",
            f"- best missing_count: `{best.get('missing_count')}`",
            f"- best mode: `{best.get('mode')}`",
            f"- best source shard: `{best.get('source_shard')}`",
            f"- best total lost points over pieces: `{metrics.get('total_lost_points_over_pieces')}`",
            f"- best clipped rich lines: `{metrics.get('clipped_rich_lines')}`",
            f"- best official60 old-missing hits: `{metrics.get('official60_missing_hits')}`",
        ])
    lines.extend(["", "## Threshold counts", ""])
    for name, count in threshold_counts.items():
        lines.append(f"- `{name}`: `{count}`")
    lines.extend(["", "## Mode breakdown", "", "| mode | rows | unique | best links | best covered | best lost |", "|---|---:|---:|---:|---:|---:|"])
    for mode, info in mode_breakdown.items():
        lines.append(f"| `{mode}` | {info['count']} | {info['unique_compact']} | {info['best_links']} | {info['best_covered']} | {info['best_total_lost_points']} |")
    lines.extend(["", "## Top candidates", "", "| rank | candidate_id | mode | links | covered | missing | shard | lost |", "|---:|---|---|---:|---:|---:|---:|---:|"])
    for idx, row in enumerate(compact[:25], 1):
        metrics = row.get("contact_state_metrics") or {}
        lines.append(
            f"| {idx} | `{row.get('candidate_id')}` | `{row.get('mode')}` | "
            f"{row.get('links')} | {row.get('covered_count')} | {row.get('missing_count')} | {row.get('source_shard')} | {metrics.get('total_lost_points_over_pieces')} |"
        )
    lines.extend(["", "## Top lost points", ""])
    for item in summary["top_lost_points"][:15]:
        lines.append(f"- `{item['point']}`: `{item['count']}`")
    out_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps({"summary": str(out_json), "rows": len(rows), "unique": len(compact)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
