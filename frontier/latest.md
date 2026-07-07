# Current search frontier

Status: completed `smart-search-17-cover64-stitch-graph` full run recorded. The normal ordered-trail frontier remains `60/64`, because search-17 outputs are unordered line-set scaffolds, not certified polygonal trails. The scaffold frontier improved sharply: 22 unordered lines covering `64/64`, with stitch graph components=`1` and path lower bound=`22/22`.

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

## Current next step

Prepare a new non-repeating reconstruction workflow, tentatively:

```text
smart-search-18-order-from-cover64-stitch
```

Goal: take the best search-17 `64/64`, `22/22` stitch scaffolds and try to reconstruct a real ordered 22-link polygonal trail.

The next checker/engine must separate:

1. graph adjacency by shared covered grid point;
2. actual consecutive trail vertex feasibility;
3. preserving coverage when a line is shortened to use an intersection/contact point;
4. final exact ordered-trail validation by a `check_trail`-style checker.

Do not rerun `smart-search-17-cover64-stitch-graph` with the same seed as the next serious step. It already found the intended scaffold breakthrough; the bottleneck moved to ordered reconstruction.
