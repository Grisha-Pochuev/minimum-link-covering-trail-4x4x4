# smart-search-14-rich-cover-stitch full run summary

Run recorded: `28522369532`

- Run URL: https://github.com/Grisha-Pochuev/minimum-link-covering-trail-4x4x4/actions/runs/28522369532
- Workflow: `smart-search-14-rich-cover-stitch`
- Head SHA: `14318efc17aa14b648f87c5f608d40a3d006d921`
- Status: `success`
- Result type: heuristic search, not a proof
- Seconds per shard: `21000`
- Threads per shard: `4`
- Shards/jobs: `20`
- Seed: `20260705`
- Source artifacts: `rich-cover-stitch-run-summary`, `rich-cover-stitch-22-shard-*`

## Best result

- candidate id: `mlct22-278a7d8dc1d65f25`
- covered_count: `59 / 64`
- coverage percent: `92.1875%`
- links: `22`
- mode: `new_skeleton_rich4`
- source artifact: `rich-cover-stitch-22-shard-0`
- source shard: `0`
- status: `partial_candidate`
- missing:
  - `(1, 2, 2)`
  - `(2, 0, 2)`
  - `(2, 0, 3)`
  - `(3, 1, 2)`
  - `(3, 1, 3)`

The run did not find a `60/64` or `64/64` candidate. The best candidate remains partial: 22 links covering 59 of 64 grid points.

## Candidate memory

- raw shard-best curves saved/analyzed: `20`
- raw shard-best curves at normal preservation threshold `covered_count >= 56`: `20`
- all raw shard-best curves were `59/64`
- exact unique `vertices2` representatives among shard-bests: `7`
- compact run-level additions saved: `7`
- exact IDs not seen in the recent recorded additions from runs 28460740781/28404861374: `3`
- `candidates/bank.jsonl` was not merged in this step; additions are saved separately in `candidates/bank-additions-run28522369532.jsonl`.

## Missing patterns

- 12 / 20: `(0,1,2)`, `(1,2,1)`, `(1,3,2)`, `(2,1,3)`, `(2,2,2)`
- 7 / 20: `(1,2,2)`, `(2,0,2)`, `(2,0,3)`, `(3,1,2)`, `(3,1,3)`
- 1 / 20: `(1,2,1)`, `(2,1,2)`, `(2,2,3)`, `(3,1,2)`, `(3,1,3)`

## Top recurring missing points

- `(1, 2, 1)`: 13 / 20
- `(0, 1, 2)`: 12 / 20
- `(1, 3, 2)`: 12 / 20
- `(2, 1, 3)`: 12 / 20
- `(2, 2, 2)`: 12 / 20
- `(3, 1, 2)`: 8 / 20
- `(3, 1, 3)`: 8 / 20
- `(1, 2, 2)`: 7 / 20
- `(2, 0, 2)`: 7 / 20
- `(2, 0, 3)`: 7 / 20
- `(2, 1, 2)`: 1 / 20
- `(2, 2, 3)`: 1 / 20

## Mode breakdown

- `new_skeleton_rich4`: 6 shard-best curves, best `59/64`
- `endpoint_feasible_stitch`: 5 shard-best curves, best `59/64`
- `bridge_budget_compress`: 4 shard-best curves, best `59/64`
- `defect_spread_novelty`: 3 shard-best curves, best `59/64`
- `seed_window_control`: 1 shard-best curves, best `59/64`
- `integer_rich_control`: 1 shard-best curves, best `59/64`

## Comparison with previous frontier

Previous recorded full run `28460740781` also reached `59/64` only. It had 5 exact representatives and a dominant missing family appearing in 14/20 shard-best artifacts.

This run still did not break the `59/64` wall, but it changed the structure slightly: it produced 7 exact representatives and 3 exact IDs not present in the immediately recorded recent additions. The dominant missing family dropped to 12/20, while a second family appeared in 7/20 and one novelty-family shard produced a third pattern.

## Interpretation

The rich-cover / endpoint-feasible stitch-compress idea was technically valid and produced many strong `59/64` candidates, but it still behaved like a `59/64` wall detector rather than a `60/64` breaker.

The useful next step should not be another identical `smart-search-14` rerun. The next hypothesis should analyze the two-level failure more explicitly: unordered rich cover quality versus stitch/transition cost. Save or compute richer pre-stitch objects, transition-cost tables, and skeleton-level novelty, not only final curves.
