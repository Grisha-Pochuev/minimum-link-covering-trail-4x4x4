# Current search frontier

Status: `smart-search-18-order-from-cover64-stitch` launch package prepared after completed `smart-search-17-cover64-stitch-graph` full run. The normal ordered-trail frontier remains `60/64`; the scaffold frontier from search-17 remains `64/64` with stitch path lower bound `22/22`. Search-18 is the next technical package to convert search-17 scaffolds into actual ordered polygonal chains.

Latest recorded full run:

- Repository: `Grisha-Pochuev/minimum-link-covering-trail-4x4x4`
- Final run id: `28825060197`
- Run URL: https://github.com/Grisha-Pochuev/minimum-link-covering-trail-4x4x4/actions/runs/28825060197
- Workflow: `smart-search-17-cover64-stitch-graph`
- Commit SHA of the run: `5adc2b0d1efe0d89f324c758e44bd23e24d18d28`
- Status: `success`
- Duration: full run, `21000` seconds per shard
- Threads per shard: `4`
- Shards/jobs: `20`
- Seed: `20260717`
- Result type: heuristic line-set scaffold search, not a proof and not an ordered-trail certificate
- Artifacts: `cover64-stitch-run-summary`, `cover64-stitch-22-shard-*`

## Best recorded GitHub Actions ordered-trail result

The best checked ordered-trail candidate remains unchanged from run `28674416173`:

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

The ordered-trail candidate is still partial. It has exactly 22 links and covers 60 of the 64 grid points. This is not a complete covering trail and not a proof.

## Best recorded cover64 stitch scaffold

Best search-17 scaffold:

- candidate id: `mlct22-lineset-9772981a21b2a88a`
- covered_count: `64 / 64`
- line_count: `22`
- stitch graph: components=`1`, max_component=`22/22`, path_lower_bound=`22/22`, edges=`23`
- mode: `old_wall_line_injection`
- source artifact: `cover64-stitch-22-shard-12`
- source shard: `12`
- source file: `runs/2026-07-07-smart-search-17-cover64-stitch-graph-full/best_line_set.json`
- status: `line_set_seed_not_a_trail`

Important caveat: this is an unordered 22-line scaffold. A line-set graph path is not yet the same as a valid ordered polygonal trail. Do not merge this into the ordinary ordered-trail candidate bank until a reconstruction/checker produces actual consecutive trail vertices.

## Last run lesson

Run `28825060197` answered a key structural question. The `60/64` ordered-trail wall is not caused by a shortage of rich 22-line coverage scaffolds: the run found many 22-line unordered scaffolds covering all 64 grid points.

Corrected search-17 counts:

- raw aggregator result rows: `40`
- raw aggregator cover64 rows: `40`
- compact line-set rows saved in `cover64-stitch-candidates.jsonl`: `20`
- unique compact line-sets: `20`
- compact representatives with `stitch_path_lower_bound = 22`: `4`
- compact representatives with `stitch_path_lower_bound = 21`: `13`
- compact representatives with `stitch_path_lower_bound = 20`: `3`
- ordinary ordered-trail compact candidates added: `0`
- strongest full line-set additions saved: `4`; compact line-set representatives indexed: `20`

There is no missing-point defect family at the scaffold level: all saved compact line-set representatives cover `64/64`. The remaining problem is stricter trail reconstruction from these scaffolds.

Saved run-17 memory:

```text
runs/2026-07-07-smart-search-17-cover64-stitch-graph-full/summary.md
runs/2026-07-07-smart-search-17-cover64-stitch-graph-full/best_line_set.json
runs/2026-07-07-smart-search-17-cover64-stitch-graph-full/raw_cover64_stitch_run_summary.json
runs/2026-07-07-smart-search-17-cover64-stitch-graph-full/mode_breakdown.json
runs/2026-07-07-smart-search-17-cover64-stitch-graph-full/stitch_path_histogram.json
runs/2026-07-07-smart-search-17-cover64-stitch-graph-full/compact_representatives.md
candidates/line-set-additions-run28825060197-cover64-stitch.jsonl  # 4 strongest stitch-22 full scaffolds
candidates/originals/run28825060197-cover64-stitch-line-set-index.jsonl
```

## Current prepared launch package

Prepared next workflow:

```text
workflow: smart-search-18-order-from-cover64-stitch
workflow file: .github/workflows/smart-search-18-order-from-cover64-stitch.yml
proposed workflow backup: docs/proposed-smart-search-18-order-from-cover64-stitch.yml
plan file: docs/smart-search-18-order-from-cover64-stitch-plan.md
engine: scripts/order_from_cover64_stitch.py
checker: scripts/check_ordered_trail_scaled.py
summary builder: scripts/build_order_from_cover64_stitch_summary.py
input scaffold: runs/2026-07-07-smart-search-17-cover64-stitch-graph-full/best_line_set.json
input bank: candidates/line-set-additions-run28825060197-cover64-stitch.jsonl
```

Hypothesis: `contact-aware ordered reconstruction from cover64 scaffolds`.

Simple meaning: search-17 found `64/64` unordered 22-line scaffolds with stitch path `22/22`; search-18 now chooses concrete contact vertices and actual segment endpoints, scoring real ordered-chain coverage rather than graph stitchability.

Workflow checks:

- `workflow_dispatch` only;
- no `push` trigger;
- 20 shards/jobs with `max-parallel: 20`;
- shard artifacts: `order-cover64-stitch-22-shard-*`;
- summary artifact: `order-cover64-stitch-run-summary`.

## Launch inputs for smart-search-18

Smoke-test inputs:

```text
workflow: smart-search-18-order-from-cover64-stitch
seconds: 180
workers: 4
seed: 20260718
min_actual_covered_to_save: 38
beam_width: 512
branch_limit: 5
start_limit: 22
max_mutations: 2
box_min: -1
box_max: 4
candidate_lines: 3000
min_line_cover: 2
```

Full-run inputs after green smoke:

```text
workflow: smart-search-18-order-from-cover64-stitch
seconds: 21000
workers: 4
seed: 20260718
min_actual_covered_to_save: 38
beam_width: 512
branch_limit: 5
start_limit: 22
max_mutations: 2
box_min: -1
box_max: 4
candidate_lines: 3000
min_line_cover: 2
```

Expected useful result means either a checked ordered 22-link candidate improving the `60/64` frontier, or a clear contact-loss diagnostic explaining why the search-17 `22/22` scaffold graph does not convert into a high-coverage polygonal chain. If the smoke-test gets a green check and the user launches the full run, the next result-taking prompt should record the full run, not separately analyze the smoke unless it failed or looked suspicious.
