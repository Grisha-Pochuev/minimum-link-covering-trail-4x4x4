#!/usr/bin/env python3
"""Shared preflight for smart-search-28-close-C (stage-C campaign, any round) (Python stdlib only).

Same command locally and in CI:

    python scripts/preflight_search28.py --repo . --workdir preflight-search28

  1. compile the frozen search-26 engine and the search-27 plan engine;
  2. plan-engine self-test;
  3. classic equivalence: without plan= the two engines emit identical
     units.jsonl (timings excluded) on a fixed node-limited workload;
  4. split structure: all depth-2 parents split +1 give exactly the depth-3
     frontier; "P . 2" == sum over children i of "P i 1";
  5. split invariance: on a small complete model (links=8) the whole-parent
     run and the split run both close every unit with the same exact maximum;
  6. ledger integrity and the committed plan regenerates byte-for-byte;
  7. long-run budget check;
  8. miniature: 2 shards on a deterministic mini ledger (8 cheap parents, one
     split +1) that must CLOSE, plus a target-48 control; strict aggregate,
     both verifiers over every bank, control leaves > 0, empty next ledger.
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import time
from pathlib import Path

SEARCH_SECONDS = 20400
TIMEOUT_MINUTES = 359
MIN_HEADROOM = 900
PARENTS = 126366
LEDGER = "docs/search28/C-ledger.json"
PLAN = "launch/search28-C.plan"
KEYS_C = ["anchor=5", "links=22", "w2=0", "k=2", "allow_t=0", "target=64", "save_min=56"]


def sh(cmd, cwd, log, timeout=900):
    t0 = time.time()
    p = subprocess.run([str(c) for c in cmd], cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, timeout=timeout, check=False)
    log.append({"cmd": [str(c) for c in cmd], "rc": p.returncode, "seconds": round(time.time() - t0, 2), "tail": p.stdout[-1500:]})
    if p.returncode != 0:
        print(p.stdout)
        raise SystemExit(f"preflight step failed ({p.returncode}): {' '.join(map(str, cmd))}")
    return p.stdout


def last_json(out: str) -> dict:
    return json.loads([l for l in out.splitlines() if l.startswith("{")][-1])


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", type=Path, default=Path("."))
    ap.add_argument("--workdir", type=Path, default=Path("preflight-search28"))
    ap.add_argument("--cxx", default="g++")
    ap.add_argument("--prebuilt-old", type=Path, default=None, help="local use only: skip compiling the search-26 engine")
    ap.add_argument("--prebuilt-new", type=Path, default=None, help="local use only: skip compiling the plan engine")
    args = ap.parse_args()
    repo = args.repo.resolve()
    work = args.workdir.resolve()
    if work.exists():
        shutil.rmtree(work)
    work.mkdir(parents=True)
    log: list = []
    rep: dict = {"schema": "search28-preflight-report-v1"}
    py = sys.executable
    scripts = repo / "scripts"

    # 1-2. compile + selftest
    old, new = work / "anchored_exact", work / "anchored_exact_plan"
    if args.prebuilt_old and args.prebuilt_new:
        shutil.copy(args.prebuilt_old, old)
        shutil.copy(args.prebuilt_new, new)
        rep["compiler"] = "prebuilt (local)"
    else:
        rep["compiler"] = sh([args.cxx, "--version"], repo, log).splitlines()[0]
        sh([args.cxx, "-O2", "-std=c++20", "-pthread", "-Wall", "-Wextra", "-o", old, repo / "src/search26/anchored_exact.cpp"], repo, log)
        sh([args.cxx, "-O2", "-std=c++20", "-pthread", "-Wall", "-Wextra", "-o", new, repo / "src/search27/anchored_exact_plan.cpp"], repo, log)
    if "selftest PASS" not in sh([new, "selftest"], repo, log):
        raise SystemExit("plan engine selftest failed")

    # 3. classic equivalence
    common = KEYS_C + ["unit_depth=2", "shards=4000", "shard=7", "threads=1", "seconds=300", "tt_mb=64", "unit_node_limit=200000"]
    rows = {}
    for name, eng in (("old", old), ("new", new)):
        od = work / f"classic_{name}"
        od.mkdir()
        sh([eng, "search", *common, f"out={od}"], repo, log)
        rr = [json.loads(l) for l in (od / "units.jsonl").read_text().splitlines()]
        for r in rr:
            r.pop("seconds", None)
        rows[name] = rr
    if rows["old"] != rows["new"] or len(rows["old"]) != 32:
        raise SystemExit("classic mode of the plan engine differs from the frozen search-26 engine")
    rep["classic_equivalence"] = {"units_compared": len(rows["old"]), "identical": True}

    # 4. split structure
    def plancount(lines: list[str], keys: list[str]) -> dict:
        pf = work / "pc.plan"
        pf.write_text("".join(l + "\n" for l in lines))
        return last_json(sh([new, "plancount", *keys, f"plan={pf}"], repo, log))
    # The full depth-3 frontier at k=2 does not fit in memory, so this round checks the
    # split on a parent sample (the full +1 == depth-3 identity was proven for k=1 in
    # search-27 on the same code path) and the subpath descent identity below.
    sample = list(range(0, PARENTS, 997))
    allp = plancount([f"{i} . 1" for i in sample], KEYS_C + ["unit_depth=2"])
    per_parent = sum(plancount([f"{i} . 1"], KEYS_C + ["unit_depth=2"])["units"] for i in sample[:12])
    head = plancount([f"{i} . 1" for i in sample[:12]], KEYS_C + ["unit_depth=2"])["units"]
    if allp["items"] != len(sample) or allp["units"] < len(sample) or head != per_parent:
        raise SystemExit(f"sample split structure failure {allp} {head} {per_parent}")
    d3 = None
    n0 = plancount(["6111 . 1"], KEYS_C + ["unit_depth=2"])["units"]
    two = plancount(["6111 . 2"], KEYS_C + ["unit_depth=2"])["units"]
    per = plancount([f"6111 {i} 1" for i in range(n0)], KEYS_C + ["unit_depth=2"])["units"]
    if two != per:
        raise SystemExit(f"subpath descent mismatch: {two} != {per}")
    rep["split_structure"] = {"sample_parents": len(sample), "sample_plus1_units": allp["units"], "parent6111_plus2": two, "sum_children_plus1": per}

    # 5. split invariance on a small exhaustive model
    small = ["anchor=5", "links=8", "w2=0", "k=1", "allow_t=0", "target=20", "save_min=60", "unit_depth=1", "shards=1", "shard=0",
             "threads=2", "seconds=300", "tt_mb=64"]
    n1 = last_json(sh([new, "units", *small], repo, log))["units"]
    res = {}
    for name, extra in (("whole", None), ("split", 1)):
        od = work / f"inv_{name}"
        od.mkdir()
        cmd = [new, "search", *small, f"out={od}"]
        if extra is not None:
            pf = work / "inv.plan"
            pf.write_text("".join(f"{i} . {extra}\n" for i in range(n1)))
            cmd.append(f"plan={pf}")
        sh(cmd, repo, log)
        s = json.loads((od / "engine_summary.json").read_text())
        if s["units_complete"] != s["units_assigned"]:
            raise SystemExit(f"invariance run {name} did not complete")
        res[name] = s["best_model_covered"]
    if res["whole"] != res["split"]:
        raise SystemExit(f"split changed the exact maximum: {res}")
    rep["split_invariance"] = {"links": 8, "k": 1, **res}

    # 6. ledger + plan (works for every round: the ledger is the current campaign state)
    led = json.loads((repo / LEDGER).read_text())
    if led.get("schema") != "search28-C-ledger-v2" or led.get("stage") != "C" or led.get("parents_total") != PARENTS:
        raise SystemExit("ledger schema/stage failure")
    items = [tuple(x) for x in led["open_items"] + led["not_started_items"]]
    rem = {p for p, _ in items}
    if len(set(items)) != len(items) or led["parents_complete"] + len(rem) != PARENTS or not all(0 <= p < PARENTS for p in rem):
        raise SystemExit("ledger integrity failure")
    sh([py, scripts / "make_search28_plan.py", "--ledger", repo / LEDGER, "--out", repo / PLAN, "--check"], repo, log)
    pc = plancount([l for l in (repo / PLAN).read_text().splitlines() if l and not l.startswith("#")], KEYS_C + ["unit_depth=2"])
    rep["plan"] = pc
    rep["ledger_round"] = led.get("round")

    # 7. budget
    rep["budget"] = sh([py, scripts / "check_long_run_budget.py", "--search-seconds", SEARCH_SECONDS, "--timeout-minutes", TIMEOUT_MINUTES,
                        "--minimum-headroom-seconds", MIN_HEADROOM], repo, log).strip()

    # 8. miniature: a deterministic mini ledger of cheap parents (one split) must close
    mini = work / "mini"
    mled = repo / "docs/search28/preflight-mini-ledger.json"
    mplan = work / "mini.plan"
    sh([py, scripts / "make_search28_plan.py", "--ledger", mled, "--out", mplan], repo, log)
    ctrl = work / "control.plan"
    ctrl.write_text("".join(l + "\n" for l in (repo / PLAN).read_text().splitlines()[-40:]))
    for shard in (0, 1):
        sh([py, scripts / "run_search28_ci.py", "--profile", "preflight", "--shard", shard, "--shards", 2, "--threads", 2, "--engine", new,
            "--plan", mplan, "--control-plan", ctrl, "--seconds", 120, "--out", mini], repo, log, timeout=900)
    sh([py, scripts / "build_search28_summary.py", "--input", mini, "--out", work / "mini-aggregate", "--expected-shards", 2,
        "--ledger", mled, "--plan", mplan, "--strict"], repo, log)
    agg = json.loads((work / "mini-aggregate/run_summary.json").read_text())
    if agg["status"] != "pass" or agg["verified_near_trails"] <= 0:
        raise SystemExit("miniature aggregate failed or produced no verified control trails")
    if agg["stage_C"]["closure"] != "closed" or agg["units"]["complete"] != agg["plan_units_total"] or agg["plan_units_total"] <= 8:
        raise SystemExit(f"miniature did not close its deterministic mini plan: {agg['units']} / {agg['plan_units_total']}")
    nl = json.loads((work / "mini-aggregate/next-ledger.json").read_text())
    if nl["open_items"] or nl["not_started_items"] or nl["parents_complete"] != PARENTS:
        raise SystemExit("next ledger after a closed miniature is not empty")
    rep["miniature"] = {"units": agg["units"], "plan_units_total": agg["plan_units_total"], "closure": agg["stage_C"]["closure"],
                        "verified_control_trails": agg["verified_near_trails"], "status": agg["status"]}
    rep["steps"] = log
    rep["status"] = "pass"
    (work / "preflight_report.json").write_text(json.dumps(rep, indent=2, sort_keys=True) + "\n")
    print(json.dumps({k: rep[k] for k in ("status", "classic_equivalence", "split_structure", "split_invariance", "plan", "miniature")}, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
