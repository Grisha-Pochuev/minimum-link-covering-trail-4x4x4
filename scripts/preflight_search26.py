#!/usr/bin/env python3
"""Shared preflight for smart-search-26-anchored-exact.

The SAME command is used locally, by the Step-3 release gate and by the CI
precheck job:

    python scripts/preflight_search26.py --repo . --workdir preflight-search26

Steps (any failure exits non-zero):
  1. compile the engine with the declared toolchain (g++, -std=c++20, -pthread);
  2. engine self-test (line census, exhaustive T-generator dominance sampling);
  3. replay controls: the best known 62/64 trail is a member of the model for
     anchors 4 and 5, reconstructs to an exact 22-link trail and passes both
     verifiers and scripts/check_rational_trail.py;
  4. admissibility cross-check: unpruned independent Python enumeration vs the
     bounded C++ engine on small link budgets (exact maxima must agree);
  5. long-run budget check (20400 s, 359 min, >= 900 s headroom);
  6. verifier negative tests (zero-length link, wrong link count, overclaim);
  7. miniature execution of every stage + control on 2 shards, strict
     aggregate, both verifiers over every emitted bank;
  8. preflight_report.json with throughput and peak RSS.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import platform
import resource
import shutil
import subprocess
import sys
import time
from pathlib import Path

SEARCH_SECONDS = 20400
TIMEOUT_MINUTES = 359
MIN_HEADROOM = 900


def sh(cmd: list[str], cwd: Path, log: list, timeout: int = 900, capture: bool = True) -> str:
    t0 = time.time()
    p = subprocess.run(cmd, cwd=cwd, stdout=subprocess.PIPE if capture else None, stderr=subprocess.STDOUT if capture else None,
                       text=True, timeout=timeout, check=False)
    out = p.stdout or ""
    log.append({"cmd": cmd, "rc": p.returncode, "seconds": round(time.time() - t0, 2), "tail": out[-2000:]})
    if p.returncode != 0:
        print(out)
        raise SystemExit(f"preflight step failed ({p.returncode}): {' '.join(cmd)}")
    return out


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", type=Path, default=Path("."))
    ap.add_argument("--workdir", type=Path, default=Path("preflight-search26"))
    ap.add_argument("--cxx", default="g++")
    args = ap.parse_args()
    repo = args.repo.resolve()
    work = args.workdir.resolve()
    if work.exists():
        shutil.rmtree(work)
    work.mkdir(parents=True)
    log: list = []
    report: dict = {"schema": "search26-preflight-report-v1", "python": sys.version.split()[0], "platform": platform.platform()}
    scripts = repo / "scripts"
    py = sys.executable

    # 1. compile
    engine = work / "anchored_exact"
    report["compiler"] = sh([args.cxx, "--version"], repo, log).splitlines()[0]
    sh([args.cxx, "-O2", "-std=c++20", "-pthread", "-Wall", "-Wextra", "-o", str(engine), str(repo / "src/search26/anchored_exact.cpp")], repo, log)
    report["engine_sha256"] = sha256(engine)
    report["source_sha256"] = sha256(repo / "src/search26/anchored_exact.cpp")

    # 2. self-test
    out = sh([str(engine), "selftest"], repo, log)
    if "selftest PASS" not in out:
        raise SystemExit("engine selftest did not pass")
    report["selftest"] = out.strip().splitlines()

    # 3. replay controls
    ctrl_dir = repo / "data/search26/controls"
    replays = []
    for anchor, fname in ((4, "best62_anchor4.replay"), (5, "best62_anchor5.replay")):
        out = sh([str(engine), "replay", f"anchor={anchor}", f"file={ctrl_dir / fname}", "w2=3", "k=3", "links=22", "target=62"], repo, log)
        if "final model coverage 62 links 22" not in out:
            raise SystemExit(f"replay control {fname} did not reproduce 62/64 with 22 links")
        leaf = json.loads([l for l in out.splitlines() if l.startswith("LEAF ")][0][5:])
        sys.path.insert(0, str(scripts))
        import search26_common as sc  # noqa: E402
        verts = sc.reconstruct(leaf["path"], 22, leaf["anchor"])
        row = {"claimed_covered": 62, "vertices": sc.vertices_json(verts)}
        bank = work / f"replay_anchor{anchor}.jsonl"
        bank.write_text(json.dumps(row) + "\n")
        (work / f"replay_anchor{anchor}.json").write_text(json.dumps({"vertices": row["vertices"], "links": 22}) + "\n")
        sh([py, str(scripts / "verify_search26_primary.py"), str(bank), "--report", str(work / f"replay{anchor}_primary.json")], repo, log)
        sh([py, str(scripts / "verify_search26_independent.py"), str(bank), "--report", str(work / f"replay{anchor}_independent.json")], repo, log)
        out2 = sh([py, str(scripts / "check_rational_trail.py"), str(work / f"replay_anchor{anchor}.json"), "--expected-links", "22", "--min-covered", "62"], repo, log)
        if '"covered_count": 62' not in out2:
            raise SystemExit("check_rational_trail.py disagrees on replay control")
        replays.append({"anchor": anchor, "model_covered": 62, "verified_covered": 62, "links": 22, "uses_F": any(m["kind"] == 2 for m in leaf["path"]),
                        "uses_T": any(m["kind"] in (3, 4) for m in leaf["path"])})
    report["replay_controls"] = replays

    # 4. admissibility cross-check on small budgets
    adm = []
    for k in (0, 1):
        out = sh([py, str(scripts / "search26_bruteforce.py"), "--links", "8", "--k", str(k)], repo, log, timeout=1200)
        bmax = json.loads(out.strip().splitlines()[-1])["max_model_covered"]
        res = {}
        for t in (bmax, bmax + 1):
            od = work / f"adm_k{k}_t{t}"
            od.mkdir()
            sh([str(engine), "search", "anchor=5", "links=8", "w2=0", f"k={k}", "allow_t=0", f"target={t}", f"save_min={t}", "unit_depth=0",
                "shards=1", "shard=0", "threads=1", "seconds=300", "tt_mb=16", f"out={od}"], repo, log)
            s = json.loads((od / "engine_summary.json").read_text())
            if s["units_complete"] != 1:
                raise SystemExit("admissibility run did not complete")
            res[t] = s["best_model_covered"]
        if res[bmax] != bmax or res[bmax + 1] >= bmax + 1:
            raise SystemExit(f"admissibility mismatch k={k}: brute max {bmax}, engine {res}")
        adm.append({"links": 8, "k": k, "bruteforce_max": bmax, "engine_at_max": res[bmax], "engine_at_max_plus_1": res[bmax + 1]})
    report["admissibility"] = adm

    # 5. long-run budget
    out = sh([py, str(scripts / "check_long_run_budget.py"), "--search-seconds", str(SEARCH_SECONDS), "--timeout-minutes", str(TIMEOUT_MINUTES),
              "--minimum-headroom-seconds", str(MIN_HEADROOM)], repo, log)
    report["budget"] = out.strip()

    # 6. verifier negative tests
    bad = work / "negative.jsonl"
    good_v = json.loads((work / "replay_anchor5.jsonl").read_text())["vertices"]
    rows = [
        {"claimed_covered": 62, "vertices": good_v[:5] + [good_v[4]] + good_v[5:-1]},  # zero-length link, 22 links
        {"claimed_covered": 62, "vertices": good_v[:-1]},                               # 21 links
        {"claimed_covered": 63, "vertices": good_v},                                    # overclaim
    ]
    neg = []
    for i, r in enumerate(rows):
        bad.write_text(json.dumps(r) + "\n")
        for script in ("verify_search26_primary.py", "verify_search26_independent.py"):
            p = subprocess.run([py, str(scripts / script), str(bad), "--report", str(work / f"neg_{i}_{script}.json")], cwd=repo, check=False,
                               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            if p.returncode == 0:
                raise SystemExit(f"{script} accepted invalid row {i}")
            neg.append({"row": i, "script": script, "rejected": True})
    report["negative_tests"] = neg

    # 7. miniature execution of every stage + control on 2 shards, strict aggregate
    mini = work / "mini"
    t0 = time.time()
    for shard in (0, 1):
        sh([py, str(scripts / "run_search26_ci.py"), "--profile", "preflight", "--shard", str(shard), "--shards", "2", "--threads", "2",
            "--engine", str(engine), "--out", str(mini)], repo, log, timeout=600)
    sh([py, str(scripts / "build_search26_summary.py"), "--input", str(mini), "--out", str(work / "mini-aggregate"), "--expected-shards", "2",
        "--strict", "--require-control-leaves"], repo, log)
    agg = json.loads((work / "mini-aggregate/run_summary.json").read_text())
    if agg["status"] != "pass" or agg["verified_near_trails"] <= 0:
        raise SystemExit("miniature aggregate failed or produced no verified control trails")
    nodes = 0
    secs = 0.0
    for shard in (0, 1):
        s = json.loads((mini / f"shard-{shard:02d}/shard_summary.json").read_text())
        for st in s["stages"]:
            if not st.get("skipped"):
                nodes += st["engine"]["nodes"]
                secs += st["engine"]["elapsed"] * st["engine"]["threads"]
    report["miniature"] = {"seconds": round(time.time() - t0, 1), "aggregate_status": agg["status"], "stages": agg["stages"],
                           "verified_control_trails": agg["verified_near_trails"], "nodes": nodes,
                           "nodes_per_thread_second": round(nodes / secs) if secs else 0}
    report["peak_child_rss_gib"] = round(resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss / (1024 * 1024), 4)
    report["steps"] = log
    report["status"] = "pass"
    (work / "preflight_report.json").write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps({k: report[k] for k in ("status", "compiler", "engine_sha256", "replay_controls", "admissibility", "miniature", "peak_child_rss_gib")}, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
