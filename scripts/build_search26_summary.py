#!/usr/bin/env python3
"""Strict aggregate for smart-search-26-anchored-exact (Python stdlib only).

Reads shard-XX/ directories produced by run_search26_ci.py, checks that every
expected shard is present and verified, computes per-stage closure status from
the union of completed work units, merges banks and re-runs both exact
verifiers over the merged banks.

A stage is CLOSED only if every one of its work units is reported complete by
the shard that owns it.  Anything else is reported as partial.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--expected-shards", type=int, required=True)
    ap.add_argument("--strict", action="store_true")
    ap.add_argument("--require-control-leaves", action="store_true")
    ap.add_argument("--max-rss-gib", type=float, default=13.0)
    args = ap.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    errors: list[str] = []
    shards = {}
    for d in sorted(args.input.rglob("shard_summary.json")):
        s = json.loads(d.read_text())
        if s["shard"] in shards:
            errors.append(f"duplicate shard {s['shard']}")
        shards[s["shard"]] = (s, d.parent)
    received = sorted(shards)
    missing = [i for i in range(args.expected_shards) if i not in shards]
    if missing:
        errors.append(f"missing shards {missing}")
    profiles = {s["profile"] for s, _ in shards.values()}
    if len(profiles) > 1:
        errors.append(f"mixed profiles {profiles}")
    stage_stats: dict[str, dict] = {}
    full_rows: list[str] = []
    near_rows: list[str] = []
    peak = 0.0
    for sid, (s, d) in sorted(shards.items()):
        if s.get("status") != "ok":
            errors.append(f"shard {sid} status {s.get('status')}")
        if s.get("shards") != args.expected_shards:
            errors.append(f"shard {sid} ran with shards={s.get('shards')}")
        for name in ("primary", "independent"):
            v = s.get("verification", {}).get(name, {})
            if v.get("status") != "pass":
                errors.append(f"shard {sid} {name} verifier not pass")
        peak = max(peak, float(s.get("peak_child_rss_gib", 0)))
        for st in s["stages"]:
            name = st["stage"]
            agg = stage_stats.setdefault(name, {"class": st.get("class"), "units_total": None, "complete": set(), "assigned": 0,
                                                "complete_count": 0, "open": 0, "not_started": 0, "nodes": 0, "shards_run": 0,
                                                "shards_skipped": 0, "max_elapsed": 0.0, "full_leaves": 0, "near_leaves": 0})
            if st.get("skipped"):
                agg["shards_skipped"] += 1
                continue
            e = st["engine"]
            if agg["units_total"] is None:
                agg["units_total"] = e["units_total"]
            elif agg["units_total"] != e["units_total"]:
                errors.append(f"stage {name}: inconsistent units_total")
            for u in st["complete_units"]:
                if u % args.expected_shards != sid:
                    errors.append(f"stage {name}: shard {sid} reported foreign unit {u}")
                agg["complete"].add(u)
            agg["assigned"] += e["units_assigned"]
            agg["complete_count"] += e["units_complete"]
            agg["open"] += e["units_open"]
            agg["not_started"] += e["units_not_started"]
            agg["nodes"] += e["nodes"]
            agg["shards_run"] += 1
            agg["max_elapsed"] = max(agg["max_elapsed"], e["elapsed"])
            agg["full_leaves"] += st["full_leaves"]
            agg["near_leaves"] += st["near_leaves"]
        for fname, sink in (("bank_full64.jsonl", full_rows), ("bank_near.jsonl", near_rows)):
            p = d / fname
            if not p.exists():
                errors.append(f"shard {sid} missing {fname}")
                continue
            sink.extend(line for line in p.read_text().splitlines() if line.strip())
    if peak > args.max_rss_gib:
        errors.append(f"peak RSS {peak} GiB exceeds {args.max_rss_gib}")
    merged_full = args.out / "merged_full64.jsonl"
    merged_near = args.out / "merged_near.jsonl"
    merged_full.write_text("".join(r + "\n" for r in full_rows))
    merged_near.write_text("".join(r + "\n" for r in near_rows))
    verification = {}
    for name, script in (("primary", "verify_search26_primary.py"), ("independent", "verify_search26_independent.py")):
        rep = args.out / f"aggregate_verify_{name}.json"
        rc = subprocess.run([sys.executable, str(HERE / script), str(merged_full), str(merged_near), "--report", str(rep)], check=False).returncode
        verification[name] = json.loads(rep.read_text())["status"] if rep.exists() else "missing"
        if rc != 0 or verification[name] != "pass":
            errors.append(f"aggregate {name} verifier failed")
    stages_report = {}
    for name, a in stage_stats.items():
        total = a["units_total"]
        closed = (total is not None and len(a["complete"]) == total and a["shards_run"] == args.expected_shards)
        stages_report[name] = {
            "class": a["class"], "units_total": total, "units_complete": len(a["complete"]), "units_open": a["open"],
            "units_not_started": a["not_started"], "nodes": a["nodes"], "shards_run": a["shards_run"], "shards_skipped": a["shards_skipped"],
            "max_engine_elapsed_seconds": round(a["max_elapsed"], 1), "full64_leaves": a["full_leaves"], "near_leaves": a["near_leaves"],
            "closure": "closed" if closed else "partial",
            "complete_fraction": (round(len(a["complete"]) / total, 6) if total else 0.0),
        }
    if args.require_control_leaves:
        if stages_report.get("control", {}).get("near_leaves", 0) + stages_report.get("control", {}).get("full64_leaves", 0) <= 0:
            errors.append("control stage produced no leaves")
        for name in ("A", "B", "C"):
            if stages_report.get(name, {}).get("nodes", 0) <= 0:
                errors.append(f"stage {name} did no work")
    best = 0
    for line in full_rows + near_rows:
        best = max(best, json.loads(line)["claimed_covered"])
    summary = {
        "schema": "search26-run-summary-v1",
        "workflow": "smart-search-26-anchored-exact",
        "profile": sorted(profiles)[0] if profiles else None,
        "expected_shards": args.expected_shards,
        "received_shards": received,
        "complete": not missing,
        "stages": stages_report,
        "verified_full64_trails": len(full_rows),
        "verified_near_trails": len(near_rows),
        "best_claimed_covered": best,
        "max_peak_child_rss_gib": peak,
        "verification": verification,
        "errors": errors,
        "status": "pass" if not errors else "fail",
    }
    (args.out / "run_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    lines = ["# smart-search-26-anchored-exact aggregate", "", f"Profile: `{summary['profile']}`; shards received `{len(received)}/{args.expected_shards}`; status `{summary['status']}`.", ""]
    lines.append("| stage | class | units | complete | closure | nodes |")
    lines.append("|---|---|---:|---:|---|---:|")
    for name in sorted(stages_report):
        r = stages_report[name]
        lines.append(f"| {name} | {r['class']} | {r['units_total']} | {r['units_complete']} | {r['closure']} | {r['nodes']} |")
    lines += ["", f"Verified 64/64 trails: `{len(full_rows)}`. Verified near trails: `{len(near_rows)}` (best claimed `{best}`).",
              f"Max peak child RSS: `{peak}` GiB.", ""]
    if errors:
        lines += ["Errors:", ""] + [f"- {e}" for e in errors]
    (args.out / "summary.md").write_text("\n".join(lines) + "\n")
    print(json.dumps({"status": summary["status"], "errors": errors[:10], "stages": {k: (v["units_complete"], v["units_total"], v["closure"]) for k, v in stages_report.items()}}))
    if args.strict and errors:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
