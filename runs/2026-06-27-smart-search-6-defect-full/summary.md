# smart-search-6-defect full run analysis

Run id: `28275850889`

Head commit SHA: `1c1ba2f574bc075d29b65c6b2f5a571ac6069634`

Result type: heuristic GitHub Actions search, not a proof.

## Jobs and artifacts checked

The run completed successfully. The job list contained:

- `check-known-23`: success; the known 23-link trail verification job passed.
- `defect-repair-search (0..19)`: 20 shard jobs; each reached `Run defect repair shard`, then `Check shard result`, then uploaded shard artifacts.
- `aggregate-defect-results`: success; downloaded shard artifacts and built `defect-run-summary`.

Artifacts checked:

- `defect-run-summary`
- `defect-22-shard-6`
- summary references to all 20 `defect-22-shard-*` shard-best results

## Parameters observed in shard logs

- seconds: `21000`
- threads: `4` per shard
- shards: `20`
- seed: `20260627`
- prior run id: `28275666411`
- base repair run id: `28200925016`
- min covered to save: `56`
- coordinate scale: `2`

## Best result

Best candidate selected by the aggregate summary:

- covered_count: `59 / 64`
- coverage percent: `92.1875%`
- links: `22`
- mode: `fractional_bridge22`
- status: `partial_candidate`
- source artifact: `defect-22-shard-6`
- candidate id: `mlct22-278a7d8dc1d65f25`
- missing count: `5`
- missing:
  - `(1, 2, 2)`
  - `(2, 0, 2)`
  - `(2, 0, 3)`
  - `(3, 1, 2)`
  - `(3, 1, 3)`

The candidate was rechecked after artifact download with exact integer arithmetic on the scaled coordinates. The check confirmed exactly `22` links, `59` covered grid points, and the same 5 missing points.

## Saved files

The full candidate is saved in:

```text
runs/2026-06-27-smart-search-6-defect-full/best_candidate.json
```

A reusable copy is saved in:

```text
candidates/mlct22-278a7d8dc1d65f25-run28275850889.json
```

## Top recurring missing points

Counted across the 20 shard-best results:

- `(1, 2, 2)`: 20 / 20
- `(3, 1, 0)`: 19 / 20
- `(2, 0, 2)`: 18 / 20
- `(2, 0, 3)`: 18 / 20
- `(3, 1, 2)`: 18 / 20
- `(3, 1, 3)`: 3 / 20
- `(2, 1, 2)`: 2 / 20
- `(2, 2, 3)`: 2 / 20

## Missing-pattern structure

- 17 / 20: `(1,2,2), (2,0,2), (2,0,3), (3,1,0), (3,1,2)`
- 2 / 20: `(1,2,2), (2,1,2), (2,2,3), (3,1,0), (3,1,3)`
- 1 / 20: `(1,2,2), (2,0,2), (2,0,3), (3,1,2), (3,1,3)`

This full run did not improve beyond the smoke-run value `59/64`, but it made the obstruction much sharper. The dominant defect pattern appeared in 17 of 20 shard-best candidates. The point `(1,2,2)` was missed in all 20 shard-best candidates.

## Mode comparison

All modes represented in the shard-best set reached `59/64` at least once in this full run:

- `fractional_bridge22`: 5 result(s), best `59/64`, average `59.00/64`
- `integer_control22`: 1 result(s), best `59/64`, average `59.00/64`
- `repair56_target8`: 5 result(s), best `59/64`, average `59.00/64`
- `rich_segment_catalog`: 1 result(s), best `59/64`, average `59.00/64`
- `subcube_stitch22`: 5 result(s), best `59/64`, average `59.00/64`
- `transition_penalty22`: 3 result(s), best `59/64`, average `59.00/64`

Many different modes can reproduce `59/64`, but none escaped to `60/64` or full `64/64` in this run.

## Comparison with previous frontier

- repair-search-5: `58/64` on run `28200925016`.
- smart-search-6-defect smoke: `59/64` on run `28275666411`, but only 90 seconds per shard.
- this full run: `59/64` under the full 21000-second, 20-shard budget.

This run confirms `59/64` as a stable frontier and gives 20 shard-best candidates all at `59/64`.

## Conclusion for next run

The next run should not simply repeat the same defect-repair distribution. It should become a focused `smart-search-7-core5` run that attacks the recurring 5-point defect core directly. We are no longer trying to find any `59/64`; we have many of them. Now the goal is to force at least one stable missing point into the trail without losing two points elsewhere.
