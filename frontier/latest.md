# Current search frontier

This file is the human-readable working memory of the project.

It records the latest useful GitHub Actions run whose artifacts should be used as input for the next search. The goal is to make each new run continue from the previous computational evidence instead of starting from zero.

## Current status

Status: latest completed smart search analyzed and recorded.

Latest useful completed run:

- Repository: `Grisha-Pochuev/minimum-link-covering-trail-4x4x4`
- Final run id: `28059258009`
- Run URL: https://github.com/Grisha-Pochuev/minimum-link-covering-trail-4x4x4/actions/runs/28059258009
- Workflow: `overnight-smart-search`
- Commit SHA: `17c2660025d72e08d219a6e60bb9f1f08b7d20a4`
- Status: `success`
- Duration: about 5h 40m 37s (core search: 20400 seconds per shard)
- Result type: heuristic search, not a proof
- Artifact set: `smart-run-summary`, `smart-22-shard-*`

## Parameters

- seconds: `20400`
- workers: `4` per shard
- top_k: `48`
- shards: `16`
- seed: `20260624`
- prior run id used by this run: `28029809039`
- prior seed count: `48`
- coordinate scale: `2`

## Best result

Best known result after this run:

- covered_count: `56 / 64`
- links: `22`
- links target: `22`
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

The best candidate was independently rechecked from its `vertices2` path with `coordinate_scale = 2`: it has exactly 22 links and covers 56 of the 64 grid points. This is still a partial candidate, not a complete covering trail and not a proof.

## Top recurring missing points

Counted over the 80 JSON result files from this run: 16 shard best files plus 64 worker files.

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
- `(1, 1, 3)`: 23 / 80
- `(2, 0, 0)`: 23 / 80
- `(0, 1, 2)`: 21 / 80
- `(3, 1, 3)`: 21 / 80
- `(2, 0, 2)`: 21 / 80
- `(3, 1, 0)`: 21 / 80
- `(1, 1, 0)`: 21 / 80
- `(1, 1, 1)`: 20 / 80
- `(2, 2, 2)`: 20 / 80
- `(1, 0, 3)`: 20 / 80

## Which modes worked best

- `catalog22`: best 49/64, average 47.83/64 over 12 worker results; distribution {47: 4, 48: 6, 49: 2}
- `fractional22`: best 49/64, average 46.81/64 over 16 worker results; distribution {46: 5, 47: 10, 49: 1}
- `integer22_control`: best 49/64, average 48.75/64 over 4 worker results; distribution {48: 1, 49: 3}
- `layer_cube22`: best 49/64, average 47.62/64 over 8 worker results; distribution {46: 1, 47: 3, 48: 2, 49: 2}
- `strict21`: best 44/64, average 41.25/64 over 8 worker results; distribution {40: 2, 41: 4, 42: 1, 44: 1}
- `warm22`: best 56/64, average 56.0/64 over 16 worker results; distribution {56: 16}

The clear winner was `warm22`. All 4 warm-start shards and all 16 warm-start workers reached 56/64. The other modes did not beat the old 54/64 baseline during this run; their best result was 49/64 for `fractional22`, `catalog22`, `layer_cube22`, and `integer22_control`, and 44/64 for `strict21`.

## What became clear for the next run

- The run improved the best known heuristic candidate from `54 / 64` to `56 / 64`.
- The improvement came from `warm22`, meaning the previous best trails are useful seed material.
- The current best 56/64 candidate leaves a stable block of 8 missing points. The next search should put extra pressure on these points, especially `(2,1,0)`, `(1,2,1)`, `(1,2,3)`, `(1,2,2)`, `(3,0,2)`, `(3,0,3)`, `(2,0,1)`, `(1,0,0)`.
- The new artifacts use `vertices2` with `coordinate_scale = 2`. The workflow must read both old `vertices` and new `vertices2`; otherwise the next run would download the new artifacts but fail to use them as warm-start seeds.
- `fractional22`, `catalog22`, and `layer_cube22` need retuning before they can compete with warm-start search.
- `strict21` did not approach 64/64 in this run, so it is useful only as reconnaissance, not as the main route yet.

## Next run seed source

The next serious run should start from GitHub Actions artifacts of run `28059258009`:

- first source to inspect: `smart-run-summary`;
- main warm-start source: all `smart-22-shard-*` artifacts from this run;
- most important seed artifacts: `smart-22-shard-0`, `smart-22-shard-1`, `smart-22-shard-2`, `smart-22-shard-3`, because these are the `warm22` shards that reached 56/64.

The workflow file `.github/workflows/overnight-smart-search.yml` should use `PRIOR_RUN_ID = "28059258009"` for the next run.
