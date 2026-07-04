# Run 28674416173 — smart-search-16-defect-relay-60 full result

Run URL: https://github.com/Grisha-Pochuev/minimum-link-covering-trail-4x4x4/actions/runs/28674416173

Workflow: `smart-search-16-defect-relay-60`

Head commit: `dd8414cdfe2d8c2a97e02a8223d87d69ead9a3c7`

Status: completed successfully.

## Inputs and setup

- seconds per shard: `21000`
- threads per shard: `4`
- shards/jobs: `20`
- seed: `20260716`
- latest_run_id input: `28618565146`
- previous_frontier_run_id: `28522369532`
- previous_cover_stitch_run_id: `28460740781`
- previous_diversity_run_id: `28404861374`

Controls passed:

- known 23-link trail check;
- official 60/64 seed check;
- local relay60 seed check.

Artifacts:

- `defect-relay-run-summary`;
- `defect-relay-22-shard-0` through `defect-relay-22-shard-19`.

## Main result

Best result: `60/64`, `22` links.

No `61/64+` candidate and no complete `64/64` candidate were found.

Best candidate:

- candidate id: `mlct22-3cf45a2e21fe611c`
- source artifact: `defect-relay-22-shard-7`
- source shard: `7`
- mode: `window3_relay_from_official60`
- status: `partial_candidate`
- missing: `(0,0,1)`, `(0,2,3)`, `(0,3,1)`, `(2,1,1)`

The best full geometry has the same `vertices2` as the previous official 60/64 candidate from run `28618565146`. So this run did not add a new reusable compact curve.

## Aggregation counts

The artifact summary says:

- result rows with `covered_count`: `60`
- relay `60+` rows: `60`
- reported unique compact `60+`: `2`
- unique missing families: `1`
- old four-hole wall repeats: `60`

Important counting note: the summary builder counted three record types per shard: best candidate JSON, relay60 JSONL, and missing-pattern JSON. Therefore the practical shard-best count is `20`, not `60`. The reported `unique compact = 2` is also not two reusable curves: one line in `relay60-diversity.jsonl` is a missing-pattern metadata row without `vertices2`.

## Corrected shard-best interpretation

- shard-best curves: `20`
- best coverage among shard-bests: `60/64`
- inferred shard-bests at `60/64`: `20 / 20`
- new compact reusable candidates: `0`
- new missing families: `0`
- dominant missing family: `(0,0,1)`, `(0,2,3)`, `(0,3,1)`, `(2,1,1)` in all shard-best results, inferred `20/20` and counted as `60/60` rows by the current aggregator.

## Mode breakdown

Corrected by dividing summary rows by three:

- `window2_relay_from_official60`: `7` shard-bests, best `60/64`;
- `window3_relay_from_official60`: `4` shard-bests, best `60/64`;
- `old59_to_relay60`: `3` shard-bests, best `60/64`;
- `relay_then_push61`: `4` shard-bests, best `60/64`;
- `integer_control`: `1` shard-best, best `60/64`;
- `old60_and_local_relay_control`: `1` shard-best, best `60/64`.

All modes collapsed to the same old four-hole wall.

## Comparison with previous frontier

Previous latest full run `28618565146` improved the numeric frontier from `59/64` to `60/64` but collapsed to one four-hole wall. This run tried to create relay diversity from that 60-skeleton. It did not do so: it rediscovered the same `60/64` geometry and the same missing family.

Numeric frontier:

- before: `60/64`;
- after: `60/64`;
- change: no numeric improvement.

Structural frontier:

- before: one official 60-family, one dominant four-hole wall;
- after: defect-relay attempt also collapsed to the same wall.

## What this means

The defect-relay / multi-60-skeleton hypothesis did not produce the desired diversity. The old four-hole wall appears stronger than expected. The next step should not be another same-seed `smart-search-16` relay run.

Recommended next non-repeating step:

1. fix or narrow `build_defect_relay_summary.py` so it separates shard-best candidates from metadata rows;
2. move away from small relays around the same official 60 geometry;
3. prepare a new hypothesis that creates genuinely different 58-60 skeletons before four-hole pressure, or uses exact/local enumeration around the four-hole wall to prove why this relay family cannot escape.

## Saved files

```text
runs/2026-07-03-smart-search-16-defect-relay-60-full/summary.md
runs/2026-07-03-smart-search-16-defect-relay-60-full/best_candidate.json
runs/2026-07-03-smart-search-16-defect-relay-60-full/mode_breakdown.json
runs/2026-07-03-smart-search-16-defect-relay-60-full/raw_defect_relay_run_summary.json
runs/2026-07-03-smart-search-16-defect-relay-60-full/relay60-diversity.jsonl
runs/2026-07-03-smart-search-16-defect-relay-60-full/compact_representatives.md
runs/2026-07-03-smart-search-16-defect-relay-60-full/shard-best-summary.jsonl
candidates/originals/run28674416173-shard-bests-index.jsonl
```
