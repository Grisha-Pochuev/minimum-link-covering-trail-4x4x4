# Current search frontier

Status: `smart-search-15-rich-line-transition-60` full run completed successfully. Numeric GitHub frontier improved from `59/64` to `60/64`; run `28618565146` is now the latest recorded completed full run. It did not find `61/64+` or a complete `64/64` candidate. It confirmed the local 60-seed as a real GitHub Actions result, but all 20 shard-best curves collapsed to one compact representative and the same four missing points.

Latest recorded full run:

- Repository: `Grisha-Pochuev/minimum-link-covering-trail-4x4x4`
- Final run id: `28618565146`
- Workflow: `smart-search-15-rich-line-transition-60`
- Commit SHA of the run: `e82bff68d5fde1ae86a19176c3310e81f4c9b8b3`
- Status: `success`
- Duration: full run, `21000` seconds per shard
- Threads per shard: `4`
- Shards/jobs: `20`
- Seed: `20260706`
- Result type: heuristic search, not a proof
- Artifacts: `rich-line-transition-run-summary`, `rich-line-transition-22-shard-*`

## Best GitHub Actions result

- candidate id: `mlct22-3cf45a2e21fe611c`
- covered_count: `60 / 64`
- coverage percent: `93.75%`
- links: `22`
- selected mode: `integer_line_control`
- source artifact: `rich-line-transition-22-shard-18`
- source shard: `18`
- status: `partial_candidate`
- missing count: `4`
- missing: `(0,0,1)`, `(0,2,3)`, `(0,3,1)`, `(2,1,1)`

The best candidate is still partial. It has exactly 22 links and covers 60 of the 64 grid points. This is not a complete covering trail and not a proof.

It has the same `vertices2` as the local seed `data/search15/local_60_candidate_cover_first_stitch_cost.json`, previously recorded as `mlct22-3cf45a2e21fe611c`. The difference is status: it is now confirmed by a completed full GitHub Actions run.

Saved run memory:

```text
runs/2026-07-03-smart-search-15-rich-line-transition-60-full/summary.md
runs/2026-07-03-smart-search-15-rich-line-transition-60-full/best_candidate.json
runs/2026-07-03-smart-search-15-rich-line-transition-60-full/mode_breakdown.json
runs/2026-07-03-smart-search-15-rich-line-transition-60-full/compact_representatives.md
runs/2026-07-03-smart-search-15-rich-line-transition-60-full/shard-best-summary.jsonl
runs/2026-07-03-smart-search-15-rich-line-transition-60-full/shard_bests.jsonl
candidates/bank-additions-run28618565146.jsonl
candidates/originals/run28618565146-shard-bests-index.jsonl
candidates/originals/run28618565146-shard-bests.jsonl
```

## Candidate memory from run 28618565146

- raw shard-best curves at the normal preservation threshold `covered_count >= 56`: `20`
- all raw shard-best curves were `60/64`
- compact representatives among the 20: `1`
- compact bank additions saved: `1`
- original shard-best index records saved: `20`
- full original geometry record saved: `1` representative, with all 20 original shard entries indexed separately

`candidates/bank.jsonl` was not merged in this step. The compact reusable addition was saved separately in `candidates/bank-additions-run28618565146.jsonl`; the run-level summary and originals index preserve all 20 shard-best outputs. Because all 20 have the same `vertices2`, the full geometry is stored once as the representative.

## Dominant missing pattern

- 20 / 20: `(0,0,1)`, `(0,2,3)`, `(0,3,1)`, `(2,1,1)`

## Mode breakdown

- `local60_lns`: 5 shard-best curves, all `60/64`.
- `rich_line_transition`: 4 shard-best curves, all `60/64`.
- `missing4_pressure`: 6 shard-best curves, all `60/64`.
- `weak_bridge_surgery`: 3 shard-best curves, all `60/64`.
- `integer_line_control`: 1 shard-best curve, `60/64`; selected by aggregation as best source.
- `old59_vs_60_control`: 1 shard-best curve, `60/64`.

All modes led to the same four-point wall; no mode found `61/64+`.

## Comparison with previous frontier

Previous latest useful run was `28522369532`, with best `59/64`, `7` exact representatives, and a dominant missing family in `12 / 20` shard-best artifacts.

Run `28618565146` improves the recorded GitHub numeric frontier to `60/64`, but it has only `1` compact representative and one missing family in `20 / 20` shard-best artifacts. So the new run is useful because it confirms the local 60 skeleton on GitHub, but it also shows strong saturation around the same four points.

## Current next step

Do not immediately launch another identical `smart-search-15-rich-line-transition-60` full run with the same seed and modes.

Next useful hypothesis: exact four-point local repair around the 60-skeleton, or multi-60-skeleton generation to create independent 60/64 families before pushing to `61/64+`.
