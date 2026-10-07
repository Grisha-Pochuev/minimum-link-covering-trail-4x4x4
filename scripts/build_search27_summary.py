#!/usr/bin/env python3
"""Strict aggregate for smart-search-27-close-B (Python stdlib only).

Reads shard-XX/ directories from run_search27_ci.py, checks that every
expected shard is present, verified and ran the committed plan, unions the
reported work units, merges banks and re-runs both exact verifiers.

Closure accounting: the plan covers exactly the stage-B work that the input
ledger lists as unfinished.  Stage B is CLOSED only when every unit of the
plan is reported complete by the shard that owns it.  Otherwise a next ledger
(schema search27-B-ledger-v2) lists every open / not-started unit as an item
"(parent, subpath)", so the next run starts exactly where this one stopped.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PARENTS_TOTAL = 39930


def sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--expected-shards", type=int, required=True)
    ap.add_argument("--ledger", type=Path, required=True)
    ap.add_argument("--plan", type=Path, required=True)
    ap.add_argument("--strict", action="store_true")
    ap.add_argument("--max-rss-gib", type=float, default=13.0)
    args = ap.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    errors: list[str] = []
    ledger = json.loads(args.ledger.read_text())
    plan_sha = sha256(args.plan)
    prev_remaining_parents = (set(ledger["open_parents"]) | set(ledger["not_started_parents"])) if ledger["schema"] == "search27-B-ledger-v1" \
        else {p for p, _ in ledger["open_items"]} | {p for p, _ in ledger["not_started_items"]}
    prev_complete = PARENTS_TOTAL - len(prev_remaining_parents)

    shards = {}
    for d in sorted(args.input.rglob("shard_summary.json")):
        s = json.loads(d.read_text())
        if s["shard"] in shards:
            errors.append(f"duplicate shard {s['shard']}")
        shards[s["shard"]] = (s, d.parent)
    missing = [i for i in range(args.expected_shards) if i not in shards]
    if missing:
        errors.append(f"missing shards {missing}")
    profiles = {s["profile"] for s, _ in shards.values()}
    if len(profiles) > 1:
        errors.append(f"mixed profiles {profiles}")

    units: dict[int, dict] = {}
    units_total = None
    nodes = 0
    max_elapsed = 0.0
    peak = 0.0
    full_rows: list[str] = []
    near_rows: list[str] = []
    for sid, (s, d) in sorted(shards.items()):
        if s.get("status") != "ok":
            errors.append(f"shard {sid} status {s.get('status')}")
        if s.get("shards") != args.expected_shards:
            errors.append(f"shard {sid} ran with shards={s.get('shards')}")
        if s.get("plan_sha256") != plan_sha:
            errors.append(f"shard {sid} ran a different plan")
        for name in ("primary", "independent"):
            if s.get("verification", {}).get(name, {}).get("status") != "pass":
                errors.append(f"shard {sid} {name} verifier not pass")
        peak = max(peak, float(s.get("peak_child_rss_gib", 0)))
        for st in s["stages"]:
            if st["stage"] != "B":
                continue
            e = st["engine"]
            if units_total is None:
                units_total = e["units_total"]
            elif units_total != e["units_total"]:
                errors.append("inconsistent units_total")
            nodes += e["nodes"]
            max_elapsed = max(max_elapsed, e["elapsed"])
            for line in (d / "stage-B" / "units.jsonl").read_text().splitlines():
                if not line.strip():
                    continue
                u = json.loads(line)
                if u["unit"] % args.expected_shards != sid:
                    errors.append(f"shard {sid} reported foreign unit {u['unit']}")
                if u["unit"] in units:
                    errors.append(f"unit {u['unit']} reported twice")
                units[u["unit"]] = u
        for fname, sink in (("bank_full64.jsonl", full_rows), ("bank_near.jsonl", near_rows)):
            p = d / fname
            if not p.exists():
                errors.append(f"shard {sid} missing {fname}")
                continue
            sink.extend(line for line in p.read_text().splitlines() if line.strip())
    if units_total is not None and set(units) != set(range(units_total)):
        errors.append(f"units reported {len(units)} != units_total {units_total}")
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

    st_count = {"complete": 0, "open": 0, "not_started": 0}
    open_items, ns_items = [], []
    for uid in sorted(units):
        u = units[uid]
        st_count[u["status"]] = st_count.get(u["status"], 0) + 1
        if u["status"] == "open":
            open_items.append([u["parent"], u["sub"]])
        elif u["status"] == "not_started":
            ns_items.append([u["parent"], u["sub"]])
    remaining_parents = {p for p, _ in open_items} | {p for p, _ in ns_items}
    if not remaining_parents <= prev_remaining_parents:
        errors.append("remaining work outside the input ledger")
    complete_parents = PARENTS_TOTAL - len(remaining_parents)
    closed = not errors and not missing and units_total is not None and st_count["complete"] == units_total
    best = max([json.loads(r)["claimed_covered"] for r in full_rows + near_rows] or [0])
    next_ledger = {
        "schema": "search27-B-ledger-v2", "stage": "B",
        "engine_keys": "anchor=5 links=22 w2=0 k=1 allow_t=0 target=64 unit_depth=2",
        "previous_ledger": args.ledger.name, "previous_ledger_sha256": sha256(args.ledger), "plan_sha256": plan_sha,
        "parents_total": PARENTS_TOTAL, "parents_complete": complete_parents,
        "open_items": open_items, "not_started_items": ns_items,
    }
    (args.out / "next-ledger.json").write_text(json.dumps(next_ledger) + "\n")
    summary = {
        "schema": "search27-run-summary-v1", "workflow": "smart-search-27-close-B",
        "profile": sorted(profiles)[0] if profiles else None,
        "expected_shards": args.expected_shards, "received_shards": sorted(shards), "complete": not missing,
        "plan_sha256": plan_sha, "plan_units_total": units_total, "units": st_count,
        "stage_B": {
            "class": "anchor5; rich lines plus at most one free connector link covering no grid point",
            "parents_total": PARENTS_TOTAL, "parents_complete_before": prev_complete, "parents_complete_after": complete_parents,
            "complete_fraction": round(complete_parents / PARENTS_TOTAL, 6), "closure": "closed" if closed else "partial",
            "nodes": nodes, "max_engine_elapsed_seconds": round(max_elapsed, 1),
        },
        "verified_full64_trails": len(full_rows), "verified_near_trails": len(near_rows), "best_claimed_covered": best,
        "max_peak_child_rss_gib": peak, "verification": verification, "errors": errors,
        "status": "pass" if not errors else "fail",
    }
    (args.out / "run_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    b = summary["stage_B"]
    md = ["# smart-search-27-close-B aggregate", "",
          f"Profile `{summary['profile']}`; shards `{len(shards)}/{args.expected_shards}`; status `{summary['status']}`.", "",
          f"Stage B parents complete: `{b['parents_complete_before']}` -> `{b['parents_complete_after']}` of `{PARENTS_TOTAL}` "
          f"({b['complete_fraction']:.2%}); closure `{b['closure']}`.",
          f"Plan units: `{units_total}` (complete `{st_count['complete']}`, open `{st_count['open']}`, not started `{st_count['not_started']}`).",
          f"Verified 64/64 trails: `{len(full_rows)}`; verified near trails: `{len(near_rows)}` (best claimed `{best}`).",
          f"Max peak child RSS `{peak}` GiB.", ""]
    if errors:
        md += ["Errors:", ""] + [f"- {e}" for e in errors[:50]]
    (args.out / "summary.md").write_text("\n".join(md) + "\n")
    print(json.dumps({"status": summary["status"], "closure": b["closure"], "parents_complete": complete_parents, "units": st_count, "errors": errors[:10]}))
    if args.strict and errors:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
