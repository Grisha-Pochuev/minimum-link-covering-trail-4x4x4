# Run 28200925016 — repair-search-5

This folder records the distilled memory from GitHub Actions run `28200925016`.

Run URL: https://github.com/Grisha-Pochuev/minimum-link-covering-trail-4x4x4/actions/runs/28200925016

## Basic metadata

- Repository: `Grisha-Pochuev/minimum-link-covering-trail-4x4x4`
- Workflow: `repair-search-5`
- Run id: `28200925016`
- Head commit SHA: `960b3c357689eecd1378b2c0affe59bd6bd73573`
- Status: `success`
- Result type: heuristic search, not a proof
- Artifacts: `repair-run-summary`, `repair-22-shard-*`
- Shard result JSON files analyzed: `20`

## Parameters

- seconds: `21000` per shard, about 5h 50m
- threads: `4` C++ threads per shard
- shards: `20`
- max parallel jobs: `20`
- seed: `28200925016` because workflow input seed was left empty
- prior run id: `28103660449`
- engine: `cpp/repair56_search.cpp`
- checker: `scripts/check_scaled_trail.py`
- coordinate scale: `2`

## Best result

Best coverage improved to:

```text
58 / 64 = 90.625%
```

The run did **not** find a full `64/64` covering trail.

Best selected candidate:

- covered_count: `58 / 64`
- links: `22`
- links target: `22`
- mode: `repair56_target8`
- source file in artifact: `collected/repair_best_shard_4.json`
- saved candidate: `best_candidate.json`
- status: `partial_candidate`
- missing count: `6`
- missing: `(1,1,0)`, `(1,2,1)`, `(2,1,0)`, `(3,1,1)`, `(3,1,2)`, `(3,1,3)`

## Top candidates saved

The file `top_candidates.json` saves more than one champion. It contains all 20 shard-best summaries plus representative candidates from the best and most diverse shards.

Representative candidates with vertices are intended to be saved for shards `4`, `17`, `12`, `13`, `18`, `16`, `2`, and `9`.

This is intentional: the next run should use a seed bank, not only the single best candidate.

## Top recurring missing points

Counted over 20 shard-best result JSON files:

- `(3, 1, 1)`: 20 / 20
- `(3, 1, 2)`: 20 / 20
- `(3, 1, 3)`: 20 / 20
- `(2, 1, 0)`: 18 / 20
- `(1, 1, 0)`: 15 / 20
- `(1, 2, 1)`: 12 / 20
- `(1, 2, 3)`: 12 / 20
- `(1, 2, 2)`: 5 / 20

The new hard core is very clear: every shard-best candidate missed `(3,1,1)`, `(3,1,2)`, and `(3,1,3)`.

## Mode performance

- `transition_penalty22`: 3 results, best `58/64`, average `58.0/64`.
- `repair56_target8`: 8 results, best `58/64`, average `57.875/64`.
- `subcube_stitch22`: 1 result, best `58/64`, average `58.0/64`.
- `fractional_bridge22`: 3 results, best `58/64`, average `57.667/64`.
- `rich_segment_catalog`: 4 results, best `57/64`, average `57.0/64`.
- `integer_control22`: 1 result, best `57/64`, average `57.0/64`.

## What changed compared with the previous frontier

Previous official GitHub best after run `28103660449`: `56/64`.

Local pre-launch seed before this run: `57/64`.

This run `28200925016`: `58/64`.

So this run improved the actual GitHub Actions frontier by `+2` points over the last official run and by `+1` point over the local seed.

## Conclusions for the next run

1. Use `top_candidates.json` as the next seed bank.
2. Focus on local repair of the new 6-point defect patterns.
3. Pay special attention to the always-missing vertical triple `(3,1,1)`, `(3,1,2)`, `(3,1,3)`.
4. Keep `repair56_target8`, `transition_penalty22`, `fractional_bridge22`, and `subcube_stitch22`.
5. Do not treat failure to find `64/64` as a proof. This is still heuristic computational evidence.
