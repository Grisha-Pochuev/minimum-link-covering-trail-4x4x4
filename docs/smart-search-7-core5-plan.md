# smart-search-7-core5 plan

This is the prepared next smart run after the full `smart-search-6-defect` run `28275850889`.

The run is intentionally manual-only. It does not trigger on `push`. The default input is a safe smoke-test (`seconds=180`). For the full run, manually set `seconds=21000`, `threads=4`, and keep the 20-shard matrix.

## Why this run exists

The previous full run confirmed a stable frontier of `59/64` with `22` links. All 20 shard-best results reached `59/64`, but none reached `60/64` or full coverage.

The dominant missing pattern appeared in 17 of 20 shard-best candidates:

```text
(1,2,2), (2,0,2), (2,0,3), (3,1,0), (3,1,2)
```

The point `(1,2,2)` was missed in 20 of 20 shard-best candidates. This run therefore does not repeat the broad defect repair distribution. It focuses on the stable 5-point defect core and the close variant involving `(3,1,3)`.

## Seed sources

Use all of the following:

- latest full 59/64 run artifacts: `28275850889`
- previous 59/64 smoke artifacts: `28275666411`
- earlier 58/64 repair run artifacts: `28200925016`
- saved run folder: `runs/2026-06-27-smart-search-6-defect-full/`
- older repair folder: `runs/2026-06-26-repair-search-5/`
- local repair smoke folder: `experiments/2026-06-25-repair57-local-smoke/`
- main candidate bank: `candidates/bank.jsonl`

The main bank now includes the seven unique `59/64` candidates from run `28275850889`, plus older `56/64`, `57/64`, and `58/64` candidates.

## Code changes for the run

The workflow uses `scripts/prepare_core5_engine.py` to generate `build/core5_search.cpp` from `cpp/repair56_search.cpp`.

The generated engine changes the previous repair search in four ways:

1. It targets the dominant core points:

```text
(1,2,2), (2,0,2), (2,0,3), (3,1,0), (3,1,2)
```

and keeps `(3,1,3)` as a lower-weight nearby variant.

2. It boosts point weights, especially `(1,2,2)`, because that point was missed in all 20 shard-best results.

3. It strongly prefers high-frontier seeds by changing seed weighting toward the `59/64` candidates while preserving lower candidates as fallback memory.

4. It widens local repair windows from up to 6 links to up to 8 links and increases repair probability, so the run spends more time replacing local transitions instead of starting from scratch.

## Full launch parameters

Use these for the serious run:

```text
workflow: smart-search-7-core5
seconds: 21000
threads: 4
seed: 20260628
prior_run_id: 28275850889
secondary_run_id: 28275666411
base_repair_run_id: 28200925016
min_covered_to_save: 56
jobs/shards: 20
max-parallel: 20
expected wall time: about 5h50m per shard
```

## Smoke-test parameters

Use these first:

```text
workflow: smart-search-7-core5
seconds: 180
threads: 4
seed: 20260628
prior_run_id: 28275850889
secondary_run_id: 28275666411
base_repair_run_id: 28200925016
min_covered_to_save: 56
jobs/shards: 20
max-parallel: 20
```

The smoke-test should confirm that artifact downloads, candidate-bank export, C++ generation, compilation, checker, and summary aggregation all work before spending a full 20-job run.

## Post-run rule

After the run finishes, inspect the workflow file first, then jobs/logs/artifacts, then `core5-run-summary`, then merge all unique candidates with `covered_count >= 56` and `links <= 22` into `candidates/bank.jsonl` using the canonical bank logic. Do not only save the single best candidate.
