# smart-search-14-rich-cover-stitch plan

Date prepared: 2026-07-01

Workflow: `smart-search-14-rich-cover-stitch`

Workflow file: `.github/workflows/smart-search-14-rich-cover-stitch.yml`

Engine generator: `scripts/prepare_rich_cover_stitch_engine.py`

Generated C++: `build/rich_cover_stitch_search.cpp`

## Hypothesis

Use a richer skeleton-first search:

```text
rich-cover -> endpoint-feasible stitch-compress
```

The previous full run, `28460740781`, validated cache and anti-wall pressure but still produced only `59/64` shard-best candidates. The new run is not a same-seed rerun of `smart-search-13-cover-stitch-cache`. It changes the search object: first create richer 3-point and 4-point line material, then stitch through intervals whose chosen endpoints actually cover the intended grid points.

## Local preflight

A small local implementation of this idea was tested before preparing the package.

Observed locally:

```text
standalone rich-cover endpoint-feasible C++ generated
local compile passed with g++ -O2 -std=c++17 -pthread -DNDEBUG
1-second no-bank test produced a valid 56/64, 22-link candidate
1-second seeded representative-mode tests produced valid 59/64, 22-link candidates
local exact checker matched covered_count and links <= 22 for tested JSON outputs
```

This is only a smoke-level technical check, not evidence of a solution.

## Shard plan

```text
0-5    new_skeleton_rich4
6-10   endpoint_feasible_stitch
11-14  bridge_budget_compress
15-17  defect_spread_novelty
18     seed_window_control
19     integer_rich_control
```

## Seed run ids and seed files

Workflow inputs record these seed run ids:

```text
latest_run_id: 28460740781
previous_diversity_run_id: 28404861374
d2_bridge_run_id: 28378489636
d_family_run_id: 28338041580
new_defect_run_id: 28327372242
```

Candidate export uses `candidates/bank.jsonl` plus additions from runs `28460740781`, `28404861374`, `28378489636`, `28338041580`, `28327372242`, `28304497479`, and `28292425390`.

Runtime input directories include saved run folders from smart-search-13 down to older repair smoke folders when present.

## Workflow checks

The workflow is `workflow_dispatch`-only: no `push`, no `pull_request`, no schedule trigger.

Control check:

```text
python scripts/check_trail.py data/ripa_23_trail.json --expected-links 23 --require-full
```

Generator:

```text
python scripts/prepare_rich_cover_stitch_engine.py --out build/rich_cover_stitch_search.cpp
```

Compile:

```text
g++ -O3 -std=c++17 -pthread -DNDEBUG build/rich_cover_stitch_search.cpp -o rich_cover_stitch_search
```

Shard checker:

```text
python scripts/check_scaled_trail.py results/rich_cover_stitch/rich_cover_stitch_best_shard_<shard>.json --max-links 22
```

Shard artifact pattern:

```text
rich-cover-stitch-22-shard-*
```

Aggregation:

```text
python scripts/build_smart_summary.py
summary artifact: rich-cover-stitch-run-summary
```

## Smoke-test inputs

```text
workflow: smart-search-14-rich-cover-stitch
seconds: 180
threads: 4
seed: 20260705
min_covered_to_save: 56
latest_run_id: 28460740781
previous_diversity_run_id: 28404861374
d2_bridge_run_id: 28378489636
d_family_run_id: 28338041580
new_defect_run_id: 28327372242
jobs/shards: 20
max-parallel: 20
```

Smoke is green if all shards compile, all produced shard JSONs pass the scaled checker, and artifact `rich-cover-stitch-run-summary` contains `smart_run_summary.json` and `smart_run_summary.md`.

## Full-run inputs after green smoke-test

```text
workflow: smart-search-14-rich-cover-stitch
seconds: 21000
threads: 4
seed: 20260705
min_covered_to_save: 56
latest_run_id: 28460740781
previous_diversity_run_id: 28404861374
d2_bridge_run_id: 28378489636
d_family_run_id: 28338041580
new_defect_run_id: 28327372242
jobs/shards: 20
max-parallel: 20
expected wall time: about 5h50m per shard
```

A useful result is either any `60/64` or better candidate with `links <= 22`, or a clearly new `59/64` family with weaker convergence than the `14/20` dominant wall from smart-search-13.
