# smart-search-7-core5 full run — results

Run analyzed: `28292425390`  
Run URL: https://github.com/Grisha-Pochuev/minimum-link-covering-trail-4x4x4/actions/runs/28292425390  
Workflow: `smart-search-7-core5`  
Head SHA: `b29af6a4af45fa62c531384587377b36c650c832`  
Result type: heuristic search, not a proof.

## Parameters actually used

- seconds per shard: `21000`
- threads per shard: `4`
- shards/jobs: `20`
- max parallel jobs: `20`
- seed: `20260628`
- prior run id: `28275850889`
- secondary run id: `28275666411`
- base repair run id: `28200925016`
- min covered to save: `56`
- coordinate scale: `2`

## Best result

- covered_count: `59 / 64`
- coverage percent: `92.1875%`
- links: `22`
- mode: `subcube_stitch22`
- source artifact: `core5-22-shard-15`
- source shard: `15`
- candidate id: `mlct22-a584fa7e488e0279`
- status: `partial_candidate`
- missing count: `5`
- missing:
  - `(0, 1, 0)`
  - `(1, 2, 3)`
  - `(2, 1, 0)`
  - `(3, 1, 1)`
  - `(3, 1, 3)`

The run did not improve the numeric frontier beyond `59/64`, but it found a different 59-point defect orbit. This is useful because the old hard points `(1,2,2)`, `(2,0,2)`, `(2,0,3)`, and `(3,1,2)` can be covered by this candidate; the obstruction moves to another local region instead of disappearing.

## Result counts

All 20 shard-best artifacts were exactly checked as 22-link candidates covering `59/64`.

- `fractional_bridge22`: 6 result(s), best `59/64`, average `59.00/64`, shards [6, 7, 8, 9, 10, 11]
- `integer_control22`: 1 result(s), best `59/64`, average `59.00/64`, shards [19]
- `repair56_target8`: 2 result(s), best `59/64`, average `59.00/64`, shards [16, 17]
- `rich_segment_catalog`: 1 result(s), best `59/64`, average `59.00/64`, shards [18]
- `subcube_stitch22`: 4 result(s), best `59/64`, average `59.00/64`, shards [12, 13, 14, 15]
- `transition_penalty22`: 6 result(s), best `59/64`, average `59.00/64`, shards [0, 1, 2, 3, 4, 5]

## Unique candidates from this run

The 20 shard-best candidates reduce to `6` unique candidates modulo coordinate permutations, cube reflections, and trail reversal. All `6` unique candidates are `59/64` and eligible under the workflow threshold `covered_count >= 56`, `links <= 22`.

- `mlct22-30c323971c1e79c5`: count 9, modes ['fractional_bridge22', 'repair56_target8', 'transition_penalty22'], shards [0, 1, 2, 3, 4, 5, 6, 11, 17], missing [[1, 2, 1], [2, 1, 2], [2, 2, 3], [3, 1, 0], [3, 1, 3]]
- `mlct22-fb6f35639e636e82`: count 2, modes ['fractional_bridge22', 'repair56_target8'], shards [7, 16], missing [[1, 2, 1], [2, 1, 2], [2, 2, 3], [3, 1, 0], [3, 1, 3]]
- `mlct22-a77764189bd3e13a`: count 1, modes ['fractional_bridge22'], shards [8], missing [[0, 2, 2], [2, 1, 2], [2, 2, 3], [3, 1, 0], [3, 1, 2]]
- `mlct22-a7b17a52b1969f31`: count 2, modes ['fractional_bridge22'], shards [9, 10], missing [[1, 2, 1], [2, 1, 2], [2, 2, 3], [3, 1, 0], [3, 1, 3]]
- `mlct22-a584fa7e488e0279`: count 4, modes ['subcube_stitch22'], shards [12, 13, 14, 15], missing [[0, 1, 0], [1, 2, 3], [2, 1, 0], [3, 1, 1], [3, 1, 3]]
- `mlct22-750c1a2a8cc45c12`: count 2, modes ['integer_control22', 'rich_segment_catalog'], shards [18, 19], missing [[1, 2, 2], [2, 0, 2], [2, 0, 3], [3, 1, 0], [3, 1, 2]]

## Recurring missing points

- `(3, 1, 3)`: 17 / 20
- `(3, 1, 0)`: 16 / 20
- `(2, 1, 2)`: 14 / 20
- `(2, 2, 3)`: 14 / 20
- `(1, 2, 1)`: 13 / 20
- `(0, 1, 0)`: 4 / 20
- `(1, 2, 3)`: 4 / 20
- `(2, 1, 0)`: 4 / 20
- `(3, 1, 1)`: 4 / 20
- `(3, 1, 2)`: 3 / 20
- `(1, 2, 2)`: 2 / 20
- `(2, 0, 2)`: 2 / 20
- `(2, 0, 3)`: 2 / 20
- `(0, 2, 2)`: 1 / 20

## Dominant missing patterns

- 13 / 20: (1,2,1), (2,1,2), (2,2,3), (3,1,0), (3,1,3)
- 4 / 20: (0,1,0), (1,2,3), (2,1,0), (3,1,1), (3,1,3)
- 2 / 20: (1,2,2), (2,0,2), (2,0,3), (3,1,0), (3,1,2)
- 1 / 20: (0,2,2), (2,1,2), (2,2,3), (3,1,0), (3,1,2)

## Comparison with previous frontier

Previous recorded full frontier run `28275850889` also had best `59/64`, but its selected best missed:

`(1,2,2), (2,0,2), (2,0,3), (3,1,2), (3,1,3)`.

This run's selected best misses:

`(0,1,0), (1,2,3), (2,1,0), (3,1,1), (3,1,3)`.

So the numeric frontier is unchanged, but the evidence changed: there are now several distinct 59/64 orbits, and the only point common to the old selected best and the new selected best is `(3,1,3)`.

## Next recommendation

Do not simply repeat `smart-search-7-core5`. The next useful step is to compare the old 59/64 orbit and the new 59/64 orbit, then prepare a new `smart-search-8-orbit-bridge` style workflow that tries to combine their strengths: keep the old core coverage while repairing the new orbit around `(3,1,3)` and the nearby `(3,1,*)` transition region.
