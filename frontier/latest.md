# Current search frontier

Status: `smart-search-16-defect-relay-60` full run completed successfully. Numeric frontier remains `60/64`; run `28674416173` is the latest recorded completed full run. It did not find `61/64+` or a complete `64/64` candidate. It also did not produce the intended multi-60 diversity: all practical shard-best results collapsed back to the same old four-hole wall from run `28618565146`.

Latest recorded full run:

- Repository: `Grisha-Pochuev/minimum-link-covering-trail-4x4x4`
- Final run id: `28674416173`
- Workflow: `smart-search-16-defect-relay-60`
- Commit SHA of the run: `dd8414cdfe2d8c2a97e02a8223d87d69ead9a3c7`
- Status: `success`
- Duration: full run, `21000` seconds per shard
- Threads per shard: `4`
- Shards/jobs: `20`
- Seed: `20260716`
- Result type: heuristic search, not a proof
- Artifacts: `defect-relay-run-summary`, `defect-relay-22-shard-*`

## Best GitHub Actions result

- candidate id: `mlct22-3cf45a2e21fe611c`
- covered_count: `60 / 64`
- coverage percent: `93.75%`
- links: `22`
- selected mode: `window3_relay_from_official60`
- source artifact: `defect-relay-22-shard-7`
- source shard: `7`
- status: `partial_candidate`
- missing count: `4`
- missing: `(0,0,1)`, `(0,2,3)`, `(0,3,1)`, `(2,1,1)`

The best candidate is still partial. It has exactly 22 links and covers 60 of the 64 grid points. This is not a complete covering trail and not a proof.

It has the same `vertices2` as the previous official 60/64 candidate from run `28618565146`. So this run is recorded as a structural negative result, not as a new compact reusable candidate.

Saved run memory:

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

## Candidate memory from run 28674416173

- practical shard-best curves: `20`
- all inferred shard-best curves were `60/64`
- compact reusable bank additions saved: `0`
- new exact full-geometry representatives: `0`
- original shard-best index records saved: `20`
- aggregation rows with `covered_count`: `60`

Counting caution: the current defect-relay aggregator counted best JSON, relay60 JSONL, and missing-pattern JSON. This is why the artifact summary reports `60` relay rows and `unique compact = 2`. The second compact row is metadata without `vertices2`, not a new curve.

## Dominant missing pattern

- practical shard-bests: `20 / 20`: `(0,0,1)`, `(0,2,3)`, `(0,3,1)`, `(2,1,1)`
- raw aggregation rows: `60 / 60`: same missing family

## Mode breakdown

Corrected by actual shard mapping:

- `window2_relay_from_official60`: `7` shard-bests, all `60/64`.
- `window3_relay_from_official60`: `4` shard-bests, all `60/64`.
- `old59_to_relay60`: `3` shard-bests, all `60/64`.
- `relay_then_push61`: `4` shard-bests, all `60/64`.
- `integer_control`: `1` shard-best, `60/64`.
- `old60_and_local_relay_control`: `1` shard-best, `60/64`.

All modes led to the same four-point wall; no mode found `61/64+`.

## Prepared next launch package

Prepared workflow:

```text
workflow: smart-search-17-cover64-stitch-graph
workflow file: .github/workflows/smart-search-17-cover64-stitch-graph.yml
proposed workflow backup: docs/proposed-smart-search-17-cover64-stitch-graph.yml
plan file: docs/smart-search-17-cover64-stitch-graph-plan.md
engine: cpp/cover64_stitch_graph_search.cpp
checker: scripts/check_cover64_stitch_result.py
summary builder: scripts/build_cover64_stitch_summary.py
seed: data/search17/cover64_stitch_seed.json
```

Hypothesis: stop trying to repair the same ordered `60/64` trail. First search for unordered 22-line skeletons covering `64/64`; then optimize the stitch graph between those lines. This is not a proof and not yet a valid polygonal trail.

Local preflight seed: from the official 60/64 candidate, remove old line indices `3`, `12`, and `18`, then add three hole-closing lines. This gives a 22-line unordered skeleton covering all `64/64` grid points.

Artifact names:

```text
shard artifacts: cover64-stitch-22-shard-*
summary artifact: cover64-stitch-run-summary
summary files:
  collected/cover64_stitch_run_summary.json
  collected/cover64_stitch_run_summary.md
  collected/cover64-stitch-candidates.jsonl
```

## Current next step

Run a short smoke-test of `smart-search-17-cover64-stitch-graph`. If seed check, compile, shard artifacts, checker, and aggregation are green, run the full 20-shard search.

Exact smoke-test inputs:

```text
seconds: 180
threads: 4
seed: 20260717
min_covered_to_save: 63
```

Exact full-run inputs after green smoke:

```text
seconds: 21000
threads: 4
seed: 20260717
min_covered_to_save: 63
```

Do not rerun `smart-search-16-defect-relay-60` with the same seed and modes.
