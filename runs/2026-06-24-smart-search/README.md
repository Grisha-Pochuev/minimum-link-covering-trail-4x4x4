# 2026-06-24 smart search

This folder records the completed `overnight-smart-search` run from 2026-06-24.

This was a heuristic search, not a proof. It did not find a full 64/64 covering trail. It did improve the best known working candidate and it produced better artifacts for the next run.

## Baseline before this run

- Run id: `28029809039`
- Workflow: `overnight-22-parallel-search`
- Best result before this run: `54 / 64`
- Links target: `22`
- Meaning: useful heuristic baseline, not a proof.

## Final run metadata

- Final run id: `28059258009`
- Run URL: https://github.com/Grisha-Pochuev/minimum-link-covering-trail-4x4x4/actions/runs/28059258009
- Workflow name: `overnight-smart-search`
- Commit SHA: `17c2660025d72e08d219a6e60bb9f1f08b7d20a4`
- Status: `success`
- Duration: about 5h 40m 37s
- Core search time per shard: `20400` seconds
- Summary artifact: `smart-run-summary`
- Shard artifacts: `smart-22-shard-0` ... `smart-22-shard-15`

## Parameters

- seconds: `20400`
- workers: `4`
- top_k: `48`
- shards: `16`
- seed: `20260624`
- coordinate_scale: `2`
- prior run id: `28029809039`
- prior seed count: `48`

## Best result

- covered_count: `56 / 64`
- coverage: `87.5%`
- links: `22`
- mode: `warm22`
- status: `partial_candidate`
- missing count: `8`
- missing:
  - `(1, 0, 0)`
  - `(1, 2, 1)`
  - `(1, 2, 2)`
  - `(1, 2, 3)`
  - `(2, 0, 1)`
  - `(2, 1, 0)`
  - `(3, 0, 2)`
  - `(3, 0, 3)`

The best candidate was rechecked from the saved `vertices2` path. It has 22 links and covers exactly 56 grid points. It is still only a partial candidate because 8 points remain uncovered.

## Top recurring missing points

Counts are over 80 JSON result files: 16 shard-best files and 64 worker files.

- `(2, 1, 0)`: 41 / 80
- `(1, 2, 1)`: 39 / 80
- `(1, 2, 3)`: 39 / 80
- `(1, 2, 2)`: 36 / 80
- `(3, 0, 2)`: 36 / 80
- `(3, 0, 3)`: 36 / 80
- `(2, 0, 1)`: 33 / 80
- `(1, 0, 0)`: 32 / 80
- `(0, 0, 1)`: 25 / 80
- `(2, 0, 3)`: 25 / 80

## Mode performance

- `warm22`: best 56/64, average 56.0/64 over 16 worker results.
- `integer22_control`: best 49/64, average 48.75/64 over 4 worker results.
- `catalog22`: best 49/64, average 47.83/64 over 12 worker results.
- `layer_cube22`: best 49/64, average 47.62/64 over 8 worker results.
- `fractional22`: best 49/64, average 46.81/64 over 16 worker results.
- `strict21`: best 44/64, average 41.25/64 over 8 worker results.

The clear winner was `warm22`. It reached 56/64 in all warm-start workers. Other modes stayed at 49/64 or lower in this run.

## What became clear for the next run

- The search should not restart from the old run `28029809039` anymore.
- The next run should start from run `28059258009`.
- The most important artifacts are `smart-22-shard-0`, `smart-22-shard-1`, `smart-22-shard-2`, and `smart-22-shard-3`.
- The loader must understand the new `vertices2` format, not only the old `vertices` format.
- The next search should explicitly target the 8-point missing pattern from the 56/64 candidate.
- The fractional, catalog, and layer modes need retuning before they get a large resource share.

## Starting point for the next run

The next run should use:

- `PRIOR_RUN_ID = "28059258009"`;
- `smart-run-summary` for compact run memory;
- all `smart-22-shard-*` artifacts for seed material;
- priority warm-start seed material from shards `0`, `1`, `2`, `3`.
