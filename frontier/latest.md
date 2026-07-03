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

## Current prepared launch package

Prepared next workflow:

```text
workflow: smart-search-16-defect-relay-60
workflow file: .github/workflows/smart-search-16-defect-relay-60.yml
proposed workflow backup: docs/proposed-smart-search-16-defect-relay-60.yml
plan file: docs/smart-search-16-defect-relay-60-plan.md
generator: scripts/prepare_defect_relay_engine.py
summary builder: scripts/build_defect_relay_summary.py
seed files:
  data/search16/official_60_seed_run28618565146.json
  data/search16/local_relay60_window2_seed.json
  data/search16/old59_seed_bank_run28522369532.jsonl
candidate addition: candidates/bank-additions-local-relay60-chat-20260703.jsonl
```

Hypothesis: defect relay / multi-60-skeleton. The next run should first create several independent `60/64` skeletons with different missing sets, then try to push them to `61/64+`. This is not a same-seed rerun of `smart-search-15`.

Local preflight idea already found one relay-style `60/64` variant: replacing the window `[2,6,6] -> [6,2,6] -> [6,2,2] -> [6,8,2]` by `[2,6,6] -> [0,6,2] -> [6,0,2] -> [6,8,2]` preserved `60/64` but changed the missing set to `(0,0,1)`, `(0,2,3)`, `(2,2,3)`, `(3,1,2)`.

## Current next step

Run a short smoke-test of `smart-search-16-defect-relay-60`. If the three controls pass, the generator compiles, shard artifacts are created, and aggregation produces `defect-relay-run-summary`, then run the full 20-shard search.

Do not immediately launch another identical `smart-search-15-rich-line-transition-60` full run with the same seed and modes.
