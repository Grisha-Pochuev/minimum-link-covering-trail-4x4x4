# Current search frontier

This file is the human-readable working memory of the project.

It records the latest useful GitHub Actions run whose artifacts should be used as input for the next search. The goal is to make each new run continue from the previous computational evidence instead of starting from zero.

## Current status

Status: latest completed smart search analyzed and recorded.

Latest useful completed run:

- Repository: `Grisha-Pochuev/minimum-link-covering-trail-4x4x4`
- Final run id: `28103660449`
- Run URL: https://github.com/Grisha-Pochuev/minimum-link-covering-trail-4x4x4/actions/runs/28103660449
- Workflow: `smart-search-4`
- Commit SHA: `585556feb5c6bcc9dadc74b4ce875caad66ae481`
- Status: `success`
- Duration: core search `20400` seconds per shard, about 5h 40m
- Result type: heuristic search, not a proof
- Artifact set: `smart-run-summary`, `smart-22-shard-*`

## Parameters

- seconds: `20400`
- workers: `4` per shard
- top_k: `64`
- shards: `16`
- seed: `28103660449`
- prior run id used by this run: `28059258009`
- prior seed count: `9`
- coordinate scale: `2`
- prior best values loaded by shards: `[56, 56, 56, 56, 56, 56, 56, 56]`

## Best result

Best known result after this run:

- covered_count: `56 / 64`
- coverage percent: `87.5%`
- links: `22`
- links target: `22`
- mode selected by summary: `targeted_warm22`
- tied strong modes: `warm22`, `targeted_warm22`
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

The best candidate is still partial. It has exactly 22 links and covers 56 of the 64 grid points. This is not a complete covering trail and not a proof.

## Top recurring missing points

Counted over the 80 JSON result files from this run: 16 shard best files plus 64 worker files.

- `(1, 2, 3)`: 57 / 80
- `(3, 0, 2)`: 53 / 80
- `(2, 0, 1)`: 52 / 80
- `(1, 2, 1)`: 51 / 80
- `(1, 0, 0)`: 50 / 80
- `(1, 2, 2)`: 50 / 80
- `(3, 0, 3)`: 50 / 80
- `(2, 1, 0)`: 48 / 80
- `(1, 0, 1)`: 22 / 80
- `(3, 2, 3)`: 19 / 80
- `(3, 0, 1)`: 18 / 80
- `(0, 2, 2)`: 18 / 80
- `(0, 2, 0)`: 18 / 80
- `(1, 0, 3)`: 17 / 80
- `(1, 0, 2)`: 14 / 80
- `(0, 2, 3)`: 14 / 80
- `(1, 1, 2)`: 14 / 80
- `(2, 2, 1)`: 14 / 80
- `(3, 2, 0)`: 14 / 80
- `(3, 2, 2)`: 14 / 80

## Which modes worked best

- `targeted_warm22`: best 56/64, average 56.0/64 over 8 worker results; distribution {56: 8}
- `warm22`: best 56/64, average 56.0/64 over 24 worker results; distribution {56: 24}
- `layer_cube22`: best 48/64, average 46.38/64 over 8 worker results; distribution {45: 2, 46: 2, 47: 3, 48: 1}
- `integer22_control`: best 47/64, average 47.0/64 over 4 worker results; distribution {47: 4}
- `catalog22`: best 47/64, average 46.25/64 over 8 worker results; distribution {45: 2, 46: 2, 47: 4}
- `fractional22`: best 46/64, average 45.5/64 over 8 worker results; distribution {45: 4, 46: 4}
- `strict21`: best 41/64, average 40.75/64 over 4 worker results; distribution {40: 1, 41: 3}

The clear winners remain `warm22` and `targeted_warm22`. They reached `56/64` across all their worker results. The new targeted mode did not break the 56 barrier, but it made the 8-point defect set more stable and more convincing as a real obstruction pattern.

## What became clear for the next run

- The numerical best result did not improve: it stayed `56 / 64`.
- The defect evidence improved: the same 8 missing points were reproduced very strongly.
- The new run should not just repeat warm search. It should focus on local repair of the 8-point defect set.
- The next workflow should use artifacts from run `28103660449` as its warm-start source.
- `warm22` and `targeted_warm22` should get most of the budget.
- `fractional22`, `catalog22`, `layer_cube22`, and `integer22_control` need retuning before they are useful competitors.
- `strict21` is still only reconnaissance.

## Next run seed source

The next serious run should start from GitHub Actions artifacts of run `28103660449`:

- first source to inspect: `smart-run-summary`;
- main warm-start source: all `smart-22-shard-*` artifacts from this run;
- most important seed artifacts: `smart-22-shard-0` through `smart-22-shard-7`, because these are the `warm22` and `targeted_warm22` shards that reached `56/64`.

The workflow file `.github/workflows/smart-search-4.yml` should use `PRIOR_RUN_ID = "28103660449"` for the next run.
