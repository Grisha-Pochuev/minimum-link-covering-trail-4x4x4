#!/usr/bin/env python3
"""Shard runner for smart-search-27-close-B (Python stdlib only).

Runs the search-27 plan engine on stage B (anchor 5, 22 links, k=1, target 64)
for one shard, reconstructs every saved leaf into an exact 22-link trail, runs
both exact verifiers over the banks and writes shard_summary.json.  Non-zero
exit on any engine error, verification failure or accounting mismatch.

The same command is used by preflight (profile=preflight), smoke and full.
"""
from __future__ import annotations

import argparse
import json
import resource
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import search26_common as sc  # noqa: E402
from run_search26_ci import reconstruct_bank, sha256, verify, write_jsonl  # noqa: E402

STAGE_B = {"name": "B", "w2": 0, "k": 1, "allow_t": 0, "unit_depth": 2, "target": 64,
           "class": "anchor5; rich lines plus at most one free connector link covering no grid point"}
CONTROL = dict(STAGE_B, name="control", target=48, class_="pipeline control (target 48, not a scientific claim)")

PROFILES = {
    "preflight": {"total": 30, "tt_mb": 64, "save_min": 56, "max_saved": 40},
    "smoke": {"total": 120, "tt_mb": 2048, "save_min": 56, "max_saved": 200},
    "full": {"total": 20400, "tt_mb": 2048, "save_min": 56, "max_saved": 300},
}


def run(engine: Path, stage: dict, plan: Path, args, seconds: float, outdir: Path, prof: dict, save_min: int) -> dict:
    import subprocess
    outdir.mkdir(parents=True, exist_ok=True)
    cmd = [str(engine), "search", "anchor=5", "links=22", f"w2={stage['w2']}", f"k={stage['k']}", f"allow_t={stage['allow_t']}",
           f"target={stage['target']}", f"unit_depth={stage['unit_depth']}", f"plan={plan}", f"shards={args.shards}", f"shard={args.shard}",
           f"threads={args.threads}", f"seconds={max(1.0, seconds):.1f}", f"tt_mb={prof['tt_mb']}", f"save_min={save_min}",
           f"max_saved={prof['max_saved']}", f"out={outdir}"]
    t0 = time.time()
    with (outdir / "engine.log").open("w") as log:
        rc = subprocess.run(cmd, stdout=log, stderr=subprocess.STDOUT, check=False).returncode
    if rc != 0:
        raise SystemExit(f"engine failed with exit {rc} in stage {stage['name']}: {' '.join(cmd)}")
    summ = json.loads((outdir / "engine_summary.json").read_text())
    summ["wall_seconds"] = round(time.time() - t0, 3)
    summ["command"] = cmd
    return summ


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--profile", choices=sorted(PROFILES), required=True)
    ap.add_argument("--shard", type=int, required=True)
    ap.add_argument("--shards", type=int, default=20)
    ap.add_argument("--threads", type=int, default=4)
    ap.add_argument("--engine", type=Path, required=True)
    ap.add_argument("--plan", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--control-plan", type=Path, default=None, help="preflight only: run a target-48 control on this plan")
    ap.add_argument("--seconds", type=float, default=None, help="override the profile search budget (preflight/tests)")
    args = ap.parse_args()
    prof = dict(PROFILES[args.profile])
    if args.seconds is not None:
        prof["total"] = args.seconds
    shard_dir = args.out / f"shard-{args.shard:02d}"
    shard_dir.mkdir(parents=True, exist_ok=True)
    t_start = time.time()
    stages_out = []
    all_full: list[dict] = []
    all_near: list[dict] = []
    plan_list = [(STAGE_B, args.plan, prof["total"], prof["save_min"])]
    if args.control_plan is not None:
        ctrl = {k: v for k, v in CONTROL.items() if k != "class_"}
        ctrl["class"] = CONTROL["class_"]
        plan_list.append((ctrl, args.control_plan, 10.0, 48))
    for st, plan, secs, save_min in plan_list:
        sdir = shard_dir / f"stage-{st['name']}"
        summ = run(args.engine, st, plan, args, secs, sdir, prof, save_min)
        full, near = reconstruct_bank(sdir, st, args.shard)
        all_full += full
        all_near += near
        units = sc.load_jsonl(sdir / "units.jsonl")
        if summ["units_complete"] + summ["units_open"] + summ["units_not_started"] != summ["units_assigned"]:
            raise SystemExit(f"unit accounting mismatch in stage {st['name']}")
        if len(units) != summ["units_assigned"] or len({u["unit"] for u in units}) != len(units):
            raise SystemExit(f"units.jsonl rows do not match assignment in stage {st['name']}")
        for u in units:
            if u["unit"] % args.shards != args.shard or not {"item", "parent", "sub"} <= set(u):
                raise SystemExit(f"bad unit row {u}")
        stages_out.append({"stage": st["name"], "class": st["class"], "skipped": False, "engine": summ,
                           "plan_sha256": sha256(plan), "units_reported": len(units),
                           "full_leaves": len(full), "near_leaves": len(near)})
    full_path = shard_dir / "bank_full64.jsonl"
    near_path = shard_dir / "bank_near.jsonl"
    write_jsonl(full_path, all_full)
    write_jsonl(near_path, all_near)
    ver = verify([full_path, near_path], shard_dir)
    ru = resource.getrusage(resource.RUSAGE_CHILDREN)
    summary = {
        "schema": "search27-shard-summary-v1",
        "workflow": "smart-search-27-close-B",
        "profile": args.profile,
        "shard": args.shard,
        "shards": args.shards,
        "threads": args.threads,
        "tt_mb_per_thread": prof["tt_mb"],
        "search_seconds_budget": prof["total"],
        "elapsed_seconds": round(time.time() - t_start, 3),
        "engine_sha256": sha256(args.engine),
        "plan_sha256": sha256(args.plan),
        "peak_child_rss_gib": round(ru.ru_maxrss / (1024 * 1024), 4),
        "stages": stages_out,
        "full64_rows": len(all_full),
        "near_rows": len(all_near),
        "verification": ver,
        "status": "ok",
    }
    (shard_dir / "shard_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps({k: summary[k] for k in ("profile", "shard", "elapsed_seconds", "peak_child_rss_gib", "full64_rows", "near_rows", "status")}))
    for s in stages_out:
        e = s["engine"]
        print(f"stage {s['stage']}: units {e['units_assigned']} complete {e['units_complete']} open {e['units_open']} "
              f"not_started {e['units_not_started']} nodes {e['nodes']} elapsed {e['elapsed']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
