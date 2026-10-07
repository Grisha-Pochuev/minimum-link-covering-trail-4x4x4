# smart-search-27-close-B — handoff

Goal: finish the exact closure of search-26 stage B
(anchor = Ripà corner zigzag 333→000→300→033→003→330, 22 links,
every other link on a lattice line with ≥3 grid points, plus at most one free
connector link that covers no grid point).

Starting point: search-26 run 37539721922 (release b56d4ca, trigger 7ed7911):
stage A closed (45 030/45 030 units, no 64/64); stage B 25 008/39 930 depth-2
parents complete, 52 open, 14 870 not started; no 64/64 and no near trail.
The remaining B work is recorded in `docs/search27/B-ledger-from-search26.json`
(with sha256 of every search-26 B `units.jsonl`).

Engine: `src/search27/anchored_exact_plan.cpp` = frozen search-26 engine plus a
`plan=` work-item mode (`PARENT SUBPATH EXTRA`). Without `plan=` it is
byte-for-byte the search-26 behaviour (checked in preflight).
Plan `launch/search27-B.plan`: 52 open parents split one level (15 667 units)
first, then 14 870 whole parents; 30 537 units round-robin over 20 shards.

Preflight `scripts/preflight_search27.py` (local and CI, same command):
classic equivalence with the search-26 engine; split +1 of all parents equals
the depth-3 frontier (2 267 394); subpath descent consistency; split
invariance on an exhaustive links=8 model (max 25 = brute force); ledger and
plan regeneration; budget; 2-shard miniature with a target-48 control whose
trails pass both exact verifiers.

Output: `smart-search-27-close-B-run-summary` with `run_summary.json`,
`summary.md` and `next-ledger.json`. If B is not closed, the next run uses
`make_search27_plan.py --ledger next-ledger.json` and resumes exactly where
this one stopped. Unfinished units are never a negative mathematical result.
