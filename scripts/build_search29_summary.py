#!/usr/bin/env python3
"""Strict aggregate for smart-search-29-close-D (one round of the stage-D campaign) (Python stdlib only).

Copy of build_search28_summary.py parametrized for stage D (k=3), with one fix:
a parent is counted complete only when every unit of every plan item of that
parent is verifiably reported complete.  search-28 built the remaining set only
from the units it received, so the parents of a missing shard were counted as
complete (search-28 round 3 incomplete-report).  Units are numbered
consecutively item by item in plan order, so the possible unit range of each
item is bounded by the received units of its neighbours; an item whose range
could contain a unit of a missing shard is unverified and stays remaining
(whole, as a not-started item) in the next ledger.

Reads shard-XX/ directories from run_search29_ci.py, checks that every
expected shard is present, verified and ran the committed plan, unions the
reported work units, merges banks and re-runs both exact verifiers.

Closure accounting: the plan covers exactly the stage-D work that the input
ledger lists as unfinished.  Stage D is CLOSED only when every unit of the
plan is reported complete by the shard that owns it.  Otherwise a next ledger
(schema search29-D-ledger-v1) lists every open / not-started unit as an item
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
PARENTS_TOTAL = 126366  # depth-2 frontier, engine units mode, keys below
ENGINE_KEYS = "anchor=5 links=22 w2=0 k=3 allow_t=0 target=64 unit_depth=2"
CLASS_D = "anchor5; rich lines plus at most three free connector links covering no grid point"


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
    if ledger.get("schema") != "search29-D-ledger-v1" or ledger.get("stage") != "D" or ledger.get("parents_total") != PARENTS_TOTAL:
        raise SystemExit("not a search29 stage-D ledger")
    prev_remaining_parents = {p for p, _ in ledger["open_items"]} | {p for p, _ in ledger["not_started_items"]}
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
            if st["stage"] != "D":
                continue
            e = st["engine"]
            if units_total is None:
                units_total = e["units_total"]
            elif units_total != e["units_total"]:
                errors.append("inconsistent units_total")
            nodes += e["nodes"]
            max_elapsed = max(max_elapsed, e["elapsed"])
            for line in (d / "stage-D" / "units.jsonl").read_text().splitlines():
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

    # plan items in plan order (item index = engine "item" field)
    plan_items: list[tuple[int, str]] = []
    for line in args.plan.read_text().splitlines():
        if not line.strip() or line.startswith("#"):
            continue
        p, sub, _extra = line.split()
        plan_items.append((int(p), sub))
    by_item: dict[int, list[dict]] = {}
    for uid, u in units.items():
        it = u.get("item")
        if not isinstance(it, int) or not 0 <= it < len(plan_items) or plan_items[it][0] != u["parent"]:
            errors.append(f"unit {uid} has item {it} inconsistent with the plan")
            continue
        by_item.setdefault(it, []).append(u)
    # Possible unit-id range of item i: (max unit of any earlier item, min unit of any later item).
    n_items = len(plan_items)
    pref_max = [-1] * (n_items + 1)
    for i in range(n_items):
        pref_max[i + 1] = max(pref_max[i], max((u["unit"] for u in by_item.get(i, [])), default=-1))
    upper = units_total if units_total is not None else (max(units, default=-1) + 1)
    suf_min = [upper] * (n_items + 1)
    for i in range(n_items - 1, -1, -1):
        suf_min[i] = min(suf_min[i + 1], min((u["unit"] for u in by_item.get(i, [])), default=upper))
    missing_set = set(missing)

    def item_verified(i: int) -> bool:
        if not missing_set:
            return True
        if units_total is None:
            return False
        lo, hi = pref_max[i] + 1, suf_min[i + 1] - 1
        return not any((x % args.expected_shards) in missing_set for x in range(lo, hi + 1))

    st_count = {"complete": 0, "open": 0, "not_started": 0}
    for u in units.values():
        st_count[u["status"]] = st_count.get(u["status"], 0) + 1
    open_items, ns_items = [], []
    unverified_items = 0
    for i in range(n_items):
        if not item_verified(i):
            unverified_items += 1
            ns_items.append([plan_items[i][0], plan_items[i][1]])
            continue
        for u in sorted(by_item.get(i, []), key=lambda r: r["unit"]):
            if u["status"] == "open":
                open_items.append([u["parent"], u["sub"]])
            elif u["status"] == "not_started":
                ns_items.append([u["parent"], u["sub"]])
    if units_total is None:  # no shard reported anything: nothing is verified
        ns_items = [[p, s] for p, s in plan_items]
    remaining_parents = {p for p, _ in open_items} | {p for p, _ in ns_items}
    if not remaining_parents <= prev_remaining_parents:
        errors.append("remaining work outside the input ledger")
    complete_parents = PARENTS_TOTAL - len(remaining_parents)
    closed = not errors and not missing and units_total is not None and st_count["complete"] == units_total
    best = max([json.loads(r)["claimed_covered"] for r in full_rows + near_rows] or [0])
    next_ledger = {
        "schema": "search29-D-ledger-v1", "stage": "D", "round": int(ledger.get("round") or 0) + 1,
        "engine_keys": ENGINE_KEYS,
        "previous_ledger": args.ledger.name, "previous_ledger_sha256": sha256(args.ledger), "plan_sha256": plan_sha,
        "parents_total": PARENTS_TOTAL, "parents_complete": complete_parents,
        "from_complete_run": not missing, "unverified_plan_items": unverified_items,
        "open_items": open_items, "not_started_items": ns_items,
    }
    (args.out / "next-ledger.json").write_text(json.dumps(next_ledger) + "\n")
    summary = {
        "schema": "search29-run-summary-v1", "workflow": "smart-search-29-close-D", "round": ledger.get("round"),
        "profile": sorted(profiles)[0] if profiles else None,
        "expected_shards": args.expected_shards, "received_shards": sorted(shards), "complete": not missing,
        "plan_sha256": plan_sha, "plan_units_total": units_total, "units": st_count,
        "stage_D": {
            "class": CLASS_D,
            "parents_total": PARENTS_TOTAL, "parents_complete_before": prev_complete, "parents_complete_after": complete_parents,
            "complete_fraction": round(complete_parents / PARENTS_TOTAL, 6), "closure": "closed" if closed else "partial",
            "unverified_plan_items": unverified_items, "nodes": nodes, "max_engine_elapsed_seconds": round(max_elapsed, 1),
        },
        "verified_full64_trails": len(full_rows), "verified_near_trails": len(near_rows), "best_claimed_covered": best,
        "max_peak_child_rss_gib": peak, "verification": verification, "errors": errors,
        "status": "pass" if not errors else "fail",
    }
    (args.out / "run_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    b = summary["stage_D"]
    md = [f"# smart-search-29-close-D aggregate (round {ledger.get('round')})", "",
          f"Profile `{summary['profile']}`; shards `{len(shards)}/{args.expected_shards}`; status `{summary['status']}`.", "",
          f"Stage D parents complete: `{b['parents_complete_before']}` -> `{b['parents_complete_after']}` of `{PARENTS_TOTAL}` "
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
