# Current search frontier

This file is the human-readable working memory of the project.

It records the latest useful GitHub Actions run whose artifacts should be used as input for the next search. The goal is to make each new run continue from the previous computational evidence instead of starting from zero.

## Current status

Status: latest completed repair search analyzed and recorded.

Latest useful completed run:

- Repository: `Grisha-Pochuev/minimum-link-covering-trail-4x4x4`
- Final run id: `28200925016`
- Run URL: https://github.com/Grisha-Pochuev/minimum-link-covering-trail-4x4x4/actions/runs/28200925016
- Workflow: `repair-search-5`
- Commit SHA: `960b3c357689eecd1378b2c0affe59bd6bd73573`
- Status: `success`
- Duration: core search `21000` seconds per shard, about 5h 50m
- Result type: heuristic search, not a proof
- Artifact set: `repair-run-summary`, `repair-22-shard-*`

## Parameters

- seconds: `21000`
- threads: `4` per shard
- shards: `20`
- max parallel jobs: `20`
- seed: `28200925016`
- prior run id used by this run: `28103660449`
- coordinate scale: `2`
- engine: `cpp/repair56_search.cpp`
- checker: `scripts/check_scaled_trail.py`

## Best GitHub Actions run result

Best known result after GitHub Actions run `28200925016`:

- covered_count: `58 / 64`
- coverage percent: `90.625%`
- links: `22`
- links target: `22`
- mode selected by summary: `repair56_target8`
- status: `partial_candidate`
- missing count: `6`
- missing:
  - `(1, 1, 0)`
  - `(1, 2, 1)`
  - `(2, 1, 0)`
  - `(3, 1, 1)`
  - `(3, 1, 2)`
  - `(3, 1, 3)`

The best GitHub Actions candidate is still partial. It has exactly 22 links and covers 58 of the 64 grid points. This is not a complete covering trail and not a proof.

The exact full JSON for the best candidate remains in the run artifact `repair-22-shard-4`. The compact candidate bank is saved in:

```text
runs/2026-06-26-repair-search-5/top_candidates.json
```

## Top candidate bank

Do not use only the single best candidate for the next run.

The compact top candidate bank saves the upper layer of useful candidates, not just one champion. It contains summaries for representative shards `4`, `17`, `12`, `13`, `18`, `16`, `2`, and `9`. Full candidate JSON files with `vertices2` remain in the original `repair-22-shard-*` GitHub Actions artifacts.

This preserves several useful families:

- `58/64` repair candidates;
- `58/64` transition-penalty candidates;
- `58/64` fractional/subcube candidates;
- diverse `57/64` candidates with different defect geometry.

## Top recurring missing points from run 28200925016

Counted over the 20 shard-best JSON result files:

- `(3, 1, 1)`: 20 / 20
- `(3, 1, 2)`: 20 / 20
- `(3, 1, 3)`: 20 / 20
- `(2, 1, 0)`: 18 / 20
- `(1, 1, 0)`: 15 / 20
- `(1, 2, 1)`: 12 / 20
- `(1, 2, 3)`: 12 / 20
- `(1, 2, 2)`: 5 / 20
- `(2, 0, 0)`: 2 / 20
- `(0, 0, 0)`: 1 / 20
- `(0, 1, 0)`: 1 / 20
- `(2, 3, 0)`: 1 / 20

The new hard core is the vertical triple `(3,1,1)`, `(3,1,2)`, `(3,1,3)`: it appears as missing in every shard-best candidate.

## Which modes worked best in run 28200925016

- `transition_penalty22`: best `58/64`, average `58.0/64` over 3 results.
- `repair56_target8`: best `58/64`, average `57.875/64` over 8 results.
- `subcube_stitch22`: best `58/64`, average `58.0/64` over 1 result.
- `fractional_bridge22`: best `58/64`, average `57.667/64` over 3 results.
- `rich_segment_catalog`: best `57/64`, average `57.0/64` over 4 results.
- `integer_control22`: best `57/64`, average `57.0/64` over 1 result.

The clear conclusion is that the C++ repair direction worked. The next run should repair around the new 6-point defect set, not go back to broad warm search.

## What became clear for the next run

- The official GitHub Actions frontier improved from `56 / 64` to `58 / 64`.
- The local repair seed `57 / 64` was surpassed by the full GitHub repair run.
- No complete `64 / 64` candidate was found.
- The most stable new obstruction is `(3,1,1)`, `(3,1,2)`, `(3,1,3)`.
- The next run should use `top_candidates.json` together with the original `repair-22-shard-*` artifacts as seed material, not only the single best result.
- `repair56_target8`, `transition_penalty22`, `fractional_bridge22`, and `subcube_stitch22` deserve continued budget.
- `rich_segment_catalog` and `integer_control22` are weaker here but useful as controls and for alternative defect shapes.

## Next run seed source

The next serious run should start from:

- GitHub Actions artifacts of run `28200925016`;
- `repair-run-summary`;
- all `repair-22-shard-*` artifacts from that run;
- `runs/2026-06-26-repair-search-5/top_candidates.json`.

Prepared next focus:

```text
repair the new 6-point defect patterns, especially the vertical triple at x=3, y=1.
```
