# smart-search-29-close-D — stage-D campaign handoff

Goal: exact closure of stage D
(anchor = Ripà corner zigzag 333→000→300→033→003→330, 22 links, every other
link on a lattice line with ≥3 grid points, plus at most THREE free connector
links that cover no grid point). Stages A, B and C are closed with no 64/64
trail (search-26 run 37539721922, search-27 run 37657538469, search-28 round 4
run 37966358105).

Engine keys: `anchor=5 links=22 w2=0 k=3 allow_t=0 target=64 unit_depth=2`,
save_min=56. Engine: `src/search28/anchored_exact_plan.cpp`, unchanged (stage D
only changes k). Stage D has 126 366 depth-2 parents (engine `units` mode; the
frozen search-26 engine reports the same number at k=3). Knuth estimate
(20 000 probes): D ≈ 2.54e11 nodes vs C ≈ 1.46e11 (C took ~3.3 six-hour rounds
of 20 jobs × 4 threads), so expect ~5–6 rounds. This workflow runs ONE round per
launch.

Campaign state: `docs/search29/D-ledger.json` (schema `search29-D-ledger-v1`,
field `round`). Round 1 = all 126 366 parents not started, plan
`launch/search29-D.plan` (126 366 whole items).

Files (copies of the search-28 ones, parametrized for k=3; search-28 files untouched):
- `scripts/make_search29_plan.py`, `scripts/run_search29_ci.py`,
  `scripts/build_search29_summary.py`, `scripts/preflight_search29.py`
- `.github/workflows/smart-search-29-close-D.yml`, trigger `launch/smart-search-29-close-D.trigger`
- `docs/search29/preflight-mini-ledger.json` (same 8 cheap parents as search-28; at k=3 all 734 units close in ~11 s on 2 threads)

Workflow: precheck (search-26 preflight + search-29 preflight) → smoke[20]
(120 s) → smoke-aggregate (strict) → full[20] (20 400 s search, job timeout
359 min) → full-aggregate (strict; artifact `smart-search-29-close-D-run-summary`
with `run_summary.json`, `summary.md`, `next-ledger.json`, merged banks; both
exact verifiers re-run on merged banks) → failure-report
(`smart-search-29-incomplete-report`, non-strict, never a result).

Memory: TT_CAP_MIB = 2048 per thread (~8.1 GiB per job). 3 GiB per thread cost
a lost runner in search-28 round 3; do not raise.

Fix vs search-28 aggregate: a parent counts complete only if every unit of every
plan item of that parent is verifiably reported complete. Units are numbered
consecutively item by item, so each item's possible unit range is bounded by
its neighbours' received units; an item whose range may contain a unit of a
missing shard stays remaining (whole, in `not_started_items`). Preflight step 8b
checks this by dropping shard 1 of the miniature. (In search-28 the incomplete
report of round 3 over-counted parents of the lost shard.)

Round procedure (always the same):
1. download artifact `smart-search-29-close-D-run-summary` of the finished run;
   require `status == pass`;
2. copy its `next-ledger.json` to `docs/search29/D-ledger.json`;
3. `python scripts/make_search29_plan.py --ledger docs/search29/D-ledger.json --out launch/search29-D.plan`;
4. local gate: `python scripts/preflight_search29.py --repo . --workdir /tmp/pf29 --prebuilt-old build/anchored_exact --prebuilt-new build/plan28`
   (sandbox: compile with `python3 -m ziglang c++ -O2 -std=c++20 -pthread`);
5. commit, append a line to `launch/smart-search-29-close-D.trigger`, push.
If a run fails before the full aggregate, the ledger is NOT advanced: relaunch
the same round (touch the trigger only). If precheck fails on the miniature
control "reconstructed trail has a zero-length link" (seen once in search-28,
flaky), retrigger once; if it repeats, debug.

Unfinished units are never a negative mathematical result. Stage D is closed
only when a round's aggregate reports `closure: closed`.

## Rounds
- Round 1: ledger round 1 (126 366 not started), local preflight pass 2026-10-23 20:34 MSK (classic equivalence at k=3 vs frozen search-26 engine: 32 units identical; split +2 descent 114 304 = 114 304; miniature 734/734 closed, 80 control trails verified; missing-shard accounting check pass).
