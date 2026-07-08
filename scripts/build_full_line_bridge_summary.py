#!/usr/bin/env python3
"""Aggregate fl-bridge-20 shard outputs."""
from __future__ import annotations
import hashlib, json
from collections import Counter, defaultdict
from pathlib import Path


def load_json(p: Path):
    try:
        d = json.loads(p.read_text(encoding="utf-8"))
        return d if isinstance(d, dict) else None
    except Exception:
        return None


def ckey(row: dict) -> str:
    payload = json.dumps(row.get("vertices2") or [row.get("source_shard"), row.get("line_order", [])], separators=(",", ":"))
    return hashlib.sha256(payload.encode()).hexdigest()


def skey(row: dict) -> tuple:
    m = row.get("full_line_bridge_metrics") or {}
    return (int(row.get("links", 0) == 22), int(row.get("covered_count", 0) or 0), int(m.get("preserved_rich_lines", 0) or 0), int(m.get("full_line_links", 0) or 0), int(m.get("official60_missing_hits", 0) or 0), -int(m.get("bridge_links", 999) or 999), int(row.get("score", 0) or 0))


def main() -> int:
    root = Path("collected")
    rows = []
    for p in sorted(root.rglob("fl_bridge_best_shard_*.json")):
        d = load_json(p)
        if d:
            d.setdefault("_file", str(p)); rows.append(d)
    for p in sorted(root.rglob("preferred_fl_bridge_shard_*.jsonl")):
        try:
            lines = p.read_text(encoding="utf-8").splitlines()
        except Exception:
            continue
        for line in lines:
            if not line.strip():
                continue
            try:
                d = json.loads(line)
            except Exception:
                continue
            if isinstance(d, dict):
                d.setdefault("_file", str(p)); rows.append(d)

    unique = {}
    for row in rows:
        key = ckey(row); row.setdefault("ordered_candidate_key_sha256", key)
        if key not in unique or skey(row) > skey(unique[key]):
            unique[key] = row
    compact = sorted(unique.values(), key=skey, reverse=True)
    best = compact[0] if compact else None

    by_mode = defaultdict(list)
    for row in rows:
        by_mode[str(row.get("mode", "unknown"))].append(row)
    mode_breakdown = {}
    for mode, items in sorted(by_mode.items()):
        bm = max(items, key=skey); m = bm.get("full_line_bridge_metrics") or {}
        mode_breakdown[mode] = {"count": len(items), "unique_compact": len({ckey(x) for x in items}), "best_links": int(bm.get("links", 0) or 0), "best_covered": int(bm.get("covered_count", 0) or 0), "best_full_line_links": int(m.get("full_line_links", 0) or 0), "best_bridge_links": int(m.get("bridge_links", 0) or 0), "best_preserved_rich_lines": int(m.get("preserved_rich_lines", 0) or 0), "best_official60_hits": int(m.get("official60_missing_hits", 0) or 0)}

    missing_counter = Counter(); bridge_counter = Counter()
    for row in rows:
        for p in row.get("missing", []) or []:
            missing_counter[tuple(p)] += 1
        for seg in row.get("bridge_segments2", []) or []:
            bridge_counter[json.dumps(seg, separators=(",", ":"))] += 1
    thresholds = {"above_46": sum(1 for x in compact if int(x.get("covered_count", 0) or 0) > 46), "above_50": sum(1 for x in compact if int(x.get("covered_count", 0) or 0) > 50), "above_56": sum(1 for x in compact if int(x.get("covered_count", 0) or 0) > 56), "above_60": sum(1 for x in compact if int(x.get("covered_count", 0) or 0) > 60), "at_least_61": sum(1 for x in compact if int(x.get("covered_count", 0) or 0) >= 61), "full_64": sum(1 for x in compact if int(x.get("covered_count", 0) or 0) >= 64)}
    summary = {"schema":"full-line-bridge-summary-v1", "interpretation":"ordered 22-link attempts that preserve rich full scaffold lines and spend explicit bridge links", "result_count":len(rows), "unique_ordered_candidates":len(compact), "best_links":int(best.get("links",0) or 0) if best else 0, "best_covered_count":int(best.get("covered_count",0) or 0) if best else 0, "best_missing_count":int(best.get("missing_count",64) or 64) if best else 64, "best":best, "threshold_counts":thresholds, "mode_breakdown":mode_breakdown, "coverage_histogram":[{"covered_count":k,"count":v} for k,v in sorted(Counter(int(x.get("covered_count",0) or 0) for x in rows).items(), reverse=True)], "link_histogram":[{"links":k,"count":v} for k,v in sorted(Counter(int(x.get("links",0) or 0) for x in rows).items(), reverse=True)], "top_missing_points":[{"point":list(p),"count":c} for p,c in missing_counter.most_common(20)], "top_bridge_segments2":[{"segment2":json.loads(s),"count":c} for s,c in bridge_counter.most_common(20)]}
    (root/"fl_bridge_run_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True), encoding="utf-8")
    with (root/"fl-bridge-candidates.jsonl").open("w", encoding="utf-8") as f:
        for row in compact[:300]:
            f.write(json.dumps(row, sort_keys=True)+"\n")
    md = ["# fl-bridge run summary", "", "Full-line-preserving bridge search.", "", f"- result rows: `{len(rows)}`", f"- unique ordered candidates: `{len(compact)}`"]
    if best:
        m = best.get("full_line_bridge_metrics") or {}
        md += [f"- best candidate: `{best.get('candidate_id')}`", f"- best links: `{best.get('links')}`", f"- best covered_count: `{best.get('covered_count')} / 64`", f"- best missing_count: `{best.get('missing_count')}`", f"- best mode: `{best.get('mode')}`", f"- best source shard: `{best.get('source_shard')}`", f"- best full-line links: `{m.get('full_line_links')}`", f"- best bridge links: `{m.get('bridge_links')}`", f"- best preserved rich lines: `{m.get('preserved_rich_lines')}`", f"- best official60 old-missing hits: `{m.get('official60_missing_hits')}`"]
    md += ["", "## Threshold counts", ""] + [f"- `{k}`: `{v}`" for k,v in thresholds.items()]
    md += ["", "## Mode breakdown", "", "| mode | rows | unique | best links | best covered | full lines | bridges | rich kept | old hits |", "|---|---:|---:|---:|---:|---:|---:|---:|---:|"]
    for mode, info in mode_breakdown.items():
        md.append(f"| `{mode}` | {info['count']} | {info['unique_compact']} | {info['best_links']} | {info['best_covered']} | {info['best_full_line_links']} | {info['best_bridge_links']} | {info['best_preserved_rich_lines']} | {info['best_official60_hits']} |")
    md += ["", "## Top candidates", "", "| rank | candidate_id | mode | links | covered | full lines | bridges | rich kept | shard |", "|---:|---|---|---:|---:|---:|---:|---:|---:|"]
    for i, row in enumerate(compact[:25], 1):
        m = row.get("full_line_bridge_metrics") or {}
        md.append(f"| {i} | `{row.get('candidate_id')}` | `{row.get('mode')}` | {row.get('links')} | {row.get('covered_count')} | {m.get('full_line_links')} | {m.get('bridge_links')} | {m.get('preserved_rich_lines')} | {row.get('source_shard')} |")
    (root/"fl_bridge_run_summary.md").write_text("\n".join(md)+"\n", encoding="utf-8")
    print(json.dumps({"summary":"collected/fl_bridge_run_summary.json", "rows":len(rows), "unique":len(compact)}, indent=2))
    return 0
if __name__ == "__main__": raise SystemExit(main())
