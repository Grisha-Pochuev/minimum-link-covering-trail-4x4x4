#!/usr/bin/env python3
"""Shard runner for smart-search-26-anchored-exact (Python stdlib only).

Runs the closure ladder of the C++ engine for one shard, reconstructs every
saved leaf into an exact 22-link trail, runs both exact verifiers over every
bank, and writes shard_summary.json.  Exit code is non-zero on any engine
error, verification failure, or invariant violation.

The same command is used by the local/CI preflight (profile=preflight), smoke
and full.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import resource
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import search26_common as sc  # noqa: E402

# Closure ladder.  Every stage is a complete enumeration of one class (anchor 5,
# 22 links, target 64) split into deterministic work units; units are assigned
# round-robin to shards.  Later stages contain earlier ones.
STAGES = [
    {"name": "A", "w2": 0, "k": 0, "allow_t": 0, "unit_depth": 3, "target": 64,
     "class": "anchor5; every other link on a lattice line with >=3 grid points"},
    {"name": "B", "w2": 0, "k": 1, "allow_t": 0, "unit_depth": 2, "target": 64,
     "class": "anchor5; rich lines plus at most one free connector link covering no grid point"},
    {"name": "C", "w2": 0, "k": 2, "allow_t": 0, "unit_depth": 2, "target": 64,
     "class": "anchor5; rich lines plus at most two free connector links covering no grid point"},
]
# Control stage: same model with a low target so leaves exist; exercises the
# leaf -> exact trail -> two verifiers pipeline in preflight and smoke.
CONTROL = {"name": "control", "w2": 0, "k": 1, "allow_t": 0, "unit_depth": 2, "target": 48,
           "class": "pipeline control (target 48, not a scientific claim)"}

PROFILES = {
    # total search seconds, per-stage caps (None = remaining), control seconds, TT MB/thread, save_min
    "preflight": {"total": 40, "caps": {"A": 8, "B": 8, "C": 6}, "control": 10, "tt_mb": 64, "save_min": 56, "max_saved": 40},
    "smoke": {"total": 150, "caps": {"A": 45, "B": 45, "C": 30}, "control": 20, "tt_mb": 2048, "save_min": 56, "max_saved": 200},
    "full": {"total": 20400, "caps": {"A": None, "B": None, "C": None}, "control": 0, "tt_mb": 2048, "save_min": 56, "max_saved": 300},
}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def run_engine(engine: Path, stage: dict, args, seconds: float, outdir: Path, prof: dict) -> dict:
    outdir.mkdir(parents=True, exist_ok=True)
    cmd = [str(engine), "search", "anchor=5", "links=22", f"w2={stage['w2']}", f"k={stage['k']}", f"allow_t={stage['allow_t']}",
           f"target={stage['target']}", f"unit_depth={stage['unit_depth']}", f"shards={args.shards}", f"shard={args.shard}",
           f"threads={args.threads}", f"seconds={max(1.0, seconds):.1f}", f"tt_mb={prof['tt_mb']}",
           f"save_min={stage['target'] if stage['name'] == 'control' else prof['save_min']}", f"max_saved={prof['max_saved']}", f"out={outdir}"]
    t0 = time.time()
    with (outdir / "engine.log").open("w") as log:
        rc = subprocess.run(cmd, stdout=log, stderr=subprocess.STDOUT, check=False).returncode
    if rc != 0:
        raise SystemExit(f"engine failed with exit {rc} in stage {stage['name']}: {' '.join(cmd)}")
    summ = json.loads((outdir / "engine_summary.json").read_text())
    summ["wall_seconds"] = round(time.time() - t0, 3)
    summ["command"] = cmd
    return summ


def reconstruct_bank(outdir: Path, stage: dict, shard: int) -> tuple[list[dict], list[dict]]:
    full, near = [], []
    leaves = outdir / "leaves.jsonl"
    if not leaves.exists():
        return full, near
    for row in sc.load_jsonl(leaves):
        verts = sc.reconstruct(row["path"], 22, row["anchor"])
        if len(verts) != 23:
            raise SystemExit("reconstructed trail does not have 22 links")
        if any(a == b for a, b in zip(verts, verts[1:])):
            raise SystemExit("reconstructed trail has a zero-length link")
        rec = {
            "schema": "search26-trail-v1",
            "stage": stage["name"],
            "class": stage["class"],
            "shard": shard,
            "unit": row["unit"],
            "anchor": row["anchor"],
            "claimed_covered": row["model_covered"],
            "model_mask_hex": row["model_mask_hex"],
            "vertices": sc.vertices_json(verts),
        }
        (full if row["model_covered"] == 64 else near).append(rec)
    return full, near


def write_jsonl(path: Path, rows: list[dict]) -> None:
    with path.open("w", encoding="utf-8") as fh:
        for r in rows:
            fh.write(json.dumps(r, sort_keys=True) + "\n")


def verify(paths: list[Path], outdir: Path) -> dict:
    res = {}
    for name, script in (("primary", "verify_search26_primary.py"), ("independent", "verify_search26_independent.py")):
        rep = outdir / f"verify_{name}.json"
        rc = subprocess.run([sys.executable, str(HERE / script), *map(str, paths), "--report", str(rep)], check=False).returncode
        data = json.loads(rep.read_text())
        res[name] = {"exit": rc, "status": data["status"], "files": data["files"]}
        if rc != 0 or data["status"] != "pass":
            raise SystemExit(f"{name} verifier failed: {rep}")
    return res


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--profile", choices=sorted(PROFILES), required=True)
    ap.add_argument("--shard", type=int, required=True)
    ap.add_argument("--shards", type=int, default=20)
    ap.add_argument("--threads", type=int, default=4)
    ap.add_argument("--engine", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--tt-mb", type=int, default=None)
    args = ap.parse_args()
    prof = dict(PROFILES[args.profile])
    if args.tt_mb is not None:
        prof["tt_mb"] = args.tt_mb
    shard_dir = args.out / f"shard-{args.shard:02d}"
    shard_dir.mkdir(parents=True, exist_ok=True)
    t_start = time.time()
    deadline = t_start + prof["total"]
    stages_out = []
    all_full: list[dict] = []
    all_near: list[dict] = []
    plan = list(STAGES)
    if prof["control"] > 0:
        plan = plan + [CONTROL]
    for st in plan:
        remaining = deadline - time.time()
        if st["name"] == "control":
            secs = prof["control"]
        else:
            cap = prof["caps"].get(st["name"])
            secs = remaining if cap is None else min(cap, remaining)
        if secs < 1:
            stages_out.append({"stage": st["name"], "class": st["class"], "skipped": True, "reason": "no time left"})
            continue
        sdir = shard_dir / f"stage-{st['name']}"
        summ = run_engine(args.engine, st, args, secs, sdir, prof)
        full, near = reconstruct_bank(sdir, st, args.shard)
        all_full += full
        all_near += near
        units = sc.load_jsonl(sdir / "units.jsonl")
        complete = sorted(u["unit"] for u in units if u["status"] == "complete")
        stages_out.append({"stage": st["name"], "class": st["class"], "skipped": False, "engine": summ,
                           "complete_units": complete, "units_reported": len(units),
                           "full_leaves": len(full), "near_leaves": len(near)})
        if summ["units_complete"] + summ["units_open"] + summ["units_not_started"] != summ["units_assigned"]:
            raise SystemExit(f"unit accounting mismatch in stage {st['name']}")
        if len(units) != summ["units_assigned"]:
            raise SystemExit(f"units.jsonl rows {len(units)} != assigned {summ['units_assigned']} in stage {st['name']}")
    full_path = shard_dir / "bank_full64.jsonl"
    near_path = shard_dir / "bank_near.jsonl"
    write_jsonl(full_path, all_full)
    write_jsonl(near_path, all_near)
    ver = verify([full_path, near_path], shard_dir)
    ru = resource.getrusage(resource.RUSAGE_CHILDREN)
    summary = {
        "schema": "search26-shard-summary-v1",
        "workflow": "smart-search-26-anchored-exact",
        "profile": args.profile,
        "shard": args.shard,
        "shards": args.shards,
        "threads": args.threads,
        "tt_mb_per_thread": prof["tt_mb"],
        "search_seconds_budget": prof["total"],
        "elapsed_seconds": round(time.time() - t_start, 3),
        "engine_sha256": sha256(args.engine),
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
        if not s.get("skipped"):
            e = s["engine"]
            print(f"stage {s['stage']}: units {e['units_assigned']} complete {e['units_complete']} open {e['units_open']} "
                  f"not_started {e['units_not_started']} nodes {e['nodes']} elapsed {e['elapsed']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
