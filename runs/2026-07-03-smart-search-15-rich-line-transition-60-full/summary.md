# smart-search-15-rich-line-transition-60 full run summary

Recorded: 2026-07-03  
Run id: `28618565146`  
Run URL: https://github.com/Grisha-Pochuev/minimum-link-covering-trail-4x4x4/actions/runs/28618565146  
Workflow: `smart-search-15-rich-line-transition-60`  
Head SHA: `e82bff68d5fde1ae86a19176c3310e81f4c9b8b3`  
Status: `success`  
Result type: heuristic search, not a proof.

## Inputs and scale

- seconds per shard: `21000`
- threads per shard: `4`
- seed: `20260706`
- shards/jobs: `20`
- max parallel: `20`
- total worker streams: `80`
- latest_run_id: `28522369532`
- previous_cover_stitch_run_id: `28460740781`
- previous_diversity_run_id: `28404861374`
- candidate-bank export threshold: `56`

The workflow was manual-only through `workflow_dispatch`, with no `push` trigger. It used the local `60/64` seed and previous run material from smart-search 14, 13, and 12.

## Jobs, checks, artifacts

Both controls passed:

- `check-known-23`: verified the known 23-link construction.
- `check-local-60-seed`: verified `data/search15/local_60_candidate_cover_first_stitch_cost.json` as `60/64` with at most 22 links.

All 20 `rich-line-transition-search` shard jobs completed successfully. Aggregation also completed successfully and produced:

- `rich-line-transition-run-summary`
- `rich-line-transition-22-shard-0` through `rich-line-transition-22-shard-19`

## Best result

- candidate id: `mlct22-3cf45a2e21fe611c`
- covered_count: `60 / 64`
- coverage percent: `93.75%`
- links: `22`
- mode selected by aggregator: `integer_line_control`
- source artifact: `rich-line-transition-22-shard-18`
- source file in artifact: `rich_line_transition_best_shard_18.json`
- status: `partial_candidate`
- target_defect_hits: `11`

Missing points:

- `(0,0,1)`
- `(0,2,3)`
- `(0,3,1)`
- `(2,1,1)`

This candidate has the same `vertices2` as the local pre-run seed `mlct22-3cf45a2e21fe611c`; the run confirms it as a full GitHub Actions result, but it does not improve beyond the local seed.

## Shard-best and compact representatives

- raw shard-best curves at the preservation threshold: `20`
- all raw shard-best curves: `60/64`
- exact/canonical compact representatives: `1`
- original shard-best records archived: `20`
- compact reusable bank additions saved: `1`

All 20 shard-best artifacts canonicalize to the same representative. This means the run improved the recorded GitHub frontier numerically, but did not produce real 60-family diversity.

## Missing patterns

Repeated missing set:

- `20 / 20`: `(0,0,1)`, `(0,2,3)`, `(0,3,1)`, `(2,1,1)`

Top recurring missing points:

- `(0,0,1)`: `20 / 20`
- `(0,2,3)`: `20 / 20`
- `(0,3,1)`: `20 / 20`
- `(2,1,1)`: `20 / 20`

## Mode breakdown

| mode | shards | shard-best count | best |
|---|---:|---:|---:|
| `local60_lns` | `0-4` | 5 | `60/64` |
| `rich_line_transition` | `5-8` | 4 | `60/64` |
| `missing4_pressure` | `9-12,16-17` | 6 | `60/64` |
| `weak_bridge_surgery` | `13-15` | 3 | `60/64` |
| `integer_line_control` | `18` | 1 | `60/64` |
| `old59_vs_60_control` | `19` | 1 | `60/64` |

All modes preserved or returned to the same 60-skeleton. No mode found `61/64+`.

## Comparison with previous recorded frontier

Previous recorded full run `28522369532`:

- best: `59/64`
- missing count: `5`
- raw shard-best curves: `20`
- compact representatives: `7`
- dominant missing family: `12 / 20`

New full run `28618565146`:

- best: `60/64`
- missing count: `4`
- raw shard-best curves: `20`
- compact representatives: `1`
- dominant missing family: `20 / 20`

So the numeric frontier improved by one covered point. But structurally, the search collapsed more strongly: all modes and all shard-bests repeated the same four-hole defect family.

## Structural conclusion

The rich-line transition / stitch-cost run successfully converted the local chat seed into an official GitHub Actions frontier result. The useful lesson is not “we are almost done by repeating this exact run”. The useful lesson is that the current local 60 skeleton is a real strong object, but the four remaining holes are extremely stable under all six tested modes.

The next non-repeating step should not be another same-seed `smart-search-15` rerun. It should attack the four-hole wall directly with a different representation: either exact local window surgery around the four holes, or a multi-60-skeleton search designed to create independent `60/64` families before trying to reach `61/64+`.

## Repository checkpoint

This run-result recording step is committed on `main`. The frontier files, START_HERE memory, run folder, compact bank addition, and originals index are saved for future chats.
