# Current search frontier

Status: `smart-search-17-cover64-stitch-graph` launch package prepared after the completed `smart-search-16-defect-relay-60` run. The latest recorded full run remains `28674416173`; numeric frontier remains `60/64`. The next prepared run is not another 60/64 repair. It searches unordered 22-line `64/64` scaffolds and optimizes their stitch graph.

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

## Best recorded GitHub Actions trail result

- candidate id: `mlct22-3cf45a2e21fe611c`
- covered_count: `60 / 64`
- coverage percent: `93.75%`
- links: `22`
- latest source mode: `window3_relay_from_official60`
- latest source artifact: `defect-relay-22-shard-7`
- source shard: `7`
- status: `partial_candidate`
- missing count: `4`
- missing: `(0,0,1)`, `(0,2,3)`, `(0,3,1)`, `(2,1,1)`

The best ordered-trail candidate is still partial. It has exactly 22 links and covers 60 of the 64 grid points. This is not a complete covering trail and not a proof.

## Last run lesson

Run `28674416173` did not improve the numeric frontier and did not create independent 60-family diversity. It is useful because it tested the defect-relay / multi-60-skeleton hypothesis and showed that this exact setup still collapses to the old wall.

Corrected run-16 counts:

- practical shard-best curves: `20`
- all inferred shard-best curves were `60/64`
- compact reusable bank additions saved: `0`
- new exact full-geometry representatives: `0`
- dominant missing pattern in practical shard-bests: `20 / 20`: `(0,0,1)`, `(0,2,3)`, `(0,3,1)`, `(2,1,1)`

Counting caution: the defect-relay aggregator counted best JSON, relay60 JSONL, and missing-pattern JSON. This is why the artifact summary reports `60` relay rows and `unique compact = 2`. The second compact row is metadata without `vertices2`, not a new curve.

Saved run-16 memory:

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

## Current prepared launch package

Prepared next workflow:

```text
workflow: smart-search-17-cover64-stitch-graph
workflow file: .github/workflows/smart-search-17-cover64-stitch-graph.yml
proposed workflow backup: docs/proposed-smart-search-17-cover64-stitch-graph.yml
plan file: docs/smart-search-17-cover64-stitch-graph-plan.md
seed file: data/search17/local_cover64_stitch_graph_seed.json
local line-set addition: candidates/line-set-additions-local-cover64-stitch-chat-20260704.jsonl
checker: scripts/check_cover64_line_set.py
search engine: scripts/search_cover64_stitch_graph.py
summary builder: scripts/build_cover64_stitch_summary.py
```

Hypothesis: `cover64 stitch graph`. Instead of repairing the same ordered 60/64 trail, search for unordered 22-line scaffolds that cover all 64 points, then optimize stitch graph quality. This is not a proof and not a valid trail by itself.

Local seed behind the package:

- `22` lines;
- `64/64` coverage;
- no zero-length lines;
- stitch path lower bound around `18/22`;
- used only as a technical seed/scaffold, not as a solution.

Workflow checks:

- `workflow_dispatch` only;
- no `push` trigger;
- 20 shards/jobs with max-parallel 20;
- shard artifacts: `cover64-stitch-22-shard-*`;
- summary artifact: `cover64-stitch-run-summary`.

## Current next step

Run a short smoke-test of `smart-search-17-cover64-stitch-graph`. If the seed check, search script, shard artifacts, checker, and aggregation are green, proceed to the full 20-shard run.

Do not launch another identical `smart-search-16-defect-relay-60` run with the same seed and modes.
