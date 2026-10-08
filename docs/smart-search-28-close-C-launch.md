# smart-search-28-close-C — stage-C campaign handoff

Goal: exact closure of stage C
(anchor = Ripà corner zigzag 333→000→300→033→003→330, 22 links, every other
link on a lattice line with ≥3 grid points, plus at most two free connector
links that cover no grid point). Stages A and B are already closed with no
64/64 trail (search-26 run 37539721922, search-27 run 37657538469).

Stage C has 126 366 depth-2 parents (engine keys
`anchor=5 links=22 w2=0 k=2 allow_t=0 target=64 unit_depth=2`).
Search-26 completed 1 202 of them (only 7 of 20 shards reached stage C),
28 were open, 125 136 not started. Measured cost of completed C parents:
median 16 s, mean ~69 s per thread, heavy tail to >3 300 s; so stage C needs
several 6-hour rounds. This workflow runs ONE round per launch.

Campaign state: `docs/search28/C-ledger.json` (schema `search28-C-ledger-v2`,
field `round`). Round 1 was built from the search-26 stage-C `units.jsonl`
files (their sha256 are recorded in the ledger).

Round procedure (always the same):
1. download artifact `smart-search-28-close-C-run-summary` of the finished run;
   require `status == pass`;
2. copy its `next-ledger.json` to `docs/search28/C-ledger.json`;
3. `python scripts/make_search28_plan.py --ledger docs/search28/C-ledger.json --out launch/search28-C.plan`
   (open units split one level deeper and placed first, not-started units whole);
4. commit both, append a line to `launch/smart-search-28-close-C.trigger`, push.
If a run fails before the aggregate, the ledger is NOT advanced: relaunch the
same round (touch the trigger only).

Preflight `scripts/preflight_search28.py`: classic equivalence with the frozen
search-26 engine (k=2), split +1 of all 126 366 parents equals the depth-3
frontier, subpath descent consistency, split invariance on an exhaustive
links=8 model, ledger integrity and byte-exact plan regeneration, budget,
2-shard miniature on cheap stage-C parents that must close, plus a target-48
control whose trails pass both exact verifiers.

Unfinished units are never a negative mathematical result. Stage C is closed
only when a round's aggregate reports `closure: closed`.

## Memory policy (from round 2)
Round 1 ran the search-27 plan engine with 2 GiB tables per thread (~8 GiB per job).
From round 2 the workflow builds `src/search28/anchored_exact_plan.cpp`: identical to
the search-27 engine except that the transposition table now uses the full `tt_mb`
budget (the old sizing rounded down to a power of two, so 3 GiB gave 2 GiB).
Power-of-two sizes keep the old indexing bit-for-bit (checked: identical units at
tt_mb=64 and 2048); other sizes use multiply-shift indexing; entries store the full
key, so soundness does not depend on the index map (preflight 5b: tt_mb 64/48/40 give
the same exact maximum). `run_search28_ci.py` picks `tt_mb=auto`:
min(3072, (MemTotal − 3584 MiB)/threads), i.e. 4 × 3 GiB ≈ 12.2 GiB on the 16 GB runner.
Tables are zero-filled at start, so smoke (same tt) proves every runner can hold them
before the 6-hour jobs start.
