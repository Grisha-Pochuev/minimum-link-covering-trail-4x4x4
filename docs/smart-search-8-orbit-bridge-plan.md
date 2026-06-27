# smart-search-8-orbit-bridge plan

Prepared after analyzing full run `28292425390`.

The run is manual-only. It does not trigger on `push`. The default input is a safe smoke-test (`seconds=180`). For a full run, manually set `seconds=21000`, `threads=4`, and use the 20-shard matrix.

## Why this run exists

The current numeric frontier is still `59/64` with `22` links, but the evidence improved: we now have distinct `59/64` defect orbits rather than a single repeated obstruction.

Old selected `59/64` best from run `28275850889` missed:

```text
(1,2,2), (2,0,2), (2,0,3), (3,1,2), (3,1,3)
```

New selected `59/64` best from run `28292425390` missed:

```text
(0,1,0), (1,2,3), (2,1,0), (3,1,1), (3,1,3)
```

The only shared point between those two selected bests is `(3,1,3)`. In the latest full run, `(3,1,3)` was also the most frequent missing point, appearing in `17/20` shard-best results. Therefore the next run should not repeat `core5` unchanged. It should compare and bridge the distinct `59/64` orbits, trying to keep what each orbit covers well while repairing the transition around `(3,1,3)` and the `x=3,y=1` region.

## Seed sources

Use all of the following:

- latest full core5 run artifacts: `28292425390`
- previous full 59/64 run artifacts: `28275850889`
- previous 59/64 smoke artifacts: `28275666411`
- earlier 58/64 repair run artifacts: `28200925016`
- saved run folder: `runs/2026-06-27-smart-search-7-core5-full/`
- saved run folder: `runs/2026-06-27-smart-search-6-defect-full/`
- older repair folder: `runs/2026-06-26-repair-search-5/`
- local repair smoke folder: `experiments/2026-06-25-repair57-local-smoke/`
- main candidate bank: `candidates/bank.jsonl`
- unmerged unique additions: `candidates/bank-additions-run28292425390.jsonl`

The 20 original shard-best candidates from run `28292425390` are used through the downloaded `core5-22-shard-*` artifacts. The persistent repo bank keeps symmetry-unique candidates, while artifacts preserve the original concrete shard results.

## Code changes for the run

The workflow uses `scripts/prepare_orbit_bridge_engine.py` to generate `build/orbit_bridge_search.cpp` from `cpp/repair56_search.cpp`.

The generated engine changes the previous repair search in five ways:

1. It targets the union of old-selected, new-selected, and latest-dominant `59/64` defect sets, with the strongest weight on `(3,1,3)`.
2. It boosts the `x=3,y=1` transition column: `(3,1,0)`, `(3,1,1)`, `(3,1,2)`, `(3,1,3)`.
3. It uses a wider seed memory: saved run folders, downloaded artifacts, `candidates/bank.jsonl`, and `bank-additions-run28292425390`.
4. It prefers `59/64` seeds more aggressively while keeping 56/57/58 candidates as fallback structure.
5. It increases local repair window size and repair probability, because the current obstruction looks like a local transition problem rather than a cold-start problem.

## 20-job strategy split

The generated engine allocates shard modes as:

- shards `0..4`: `transition_penalty22`
- shards `5..9`: `fractional_bridge22`
- shards `10..14`: `subcube_stitch22`
- shards `15..17`: `repair56_target8`
- shard `18`: `rich_segment_catalog`
- shard `19`: `integer_control22`

This keeps most budget on transition/fractional/subcube repair, while preserving two small control probes.

## Smoke-test parameters

Use these first:

```text
workflow: smart-search-8-orbit-bridge
seconds: 180
threads: 4
seed: 20260629
prior_run_id: 28292425390
old_59_run_id: 28275850889
secondary_run_id: 28275666411
base_repair_run_id: 28200925016
min_covered_to_save: 56
jobs/shards: 20
max-parallel: 20
```

The smoke-test should confirm artifact downloads, multi-file candidate export, C++ generation, compilation, checker, shard artifact upload, and summary aggregation.

## Full launch parameters

Use these after the smoke-test succeeds:

```text
workflow: smart-search-8-orbit-bridge
seconds: 21000
threads: 4
seed: 20260629
prior_run_id: 28292425390
old_59_run_id: 28275850889
secondary_run_id: 28275666411
base_repair_run_id: 28200925016
min_covered_to_save: 56
jobs/shards: 20
max-parallel: 20
expected wall time: about 5h50m per shard
```

## Post-run rule

After the run finishes, inspect `START_HERE.md`, then this workflow, then jobs/logs/artifacts, then `orbit-bridge-run-summary`. Save champion candidates, save per-run original/top candidates under `runs/`, and merge all new unique candidates with `covered_count >= 56` and `links <= 22` into reusable candidate memory. Do not only save the single best candidate.
