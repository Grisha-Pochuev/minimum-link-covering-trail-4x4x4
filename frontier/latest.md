# Current search frontier

Status: completed `smart-search-18-order-from-cover64-stitch` full run recorded. The normal ordered-trail frontier remains `60/64`; the scaffold frontier from search-17 remains unordered `64/64` with stitch path lower bound `22/22`. Search-18 was a diagnostic ordered-reconstruction attempt and did not improve the ordered-trail frontier.

Latest recorded full run:

- Repository: `Grisha-Pochuev/minimum-link-covering-trail-4x4x4`
- Final run id: `28875314204`
- Run URL: https://github.com/Grisha-Pochuev/minimum-link-covering-trail-4x4x4/actions/runs/28875314204
- Workflow: `smart-search-18-order-from-cover64-stitch`
- Commit SHA of the run: `13699553f63bd8a96c33a5c05752ff44590e8240`
- Status: `success`
- Duration: full run, `21000` seconds per shard
- Threads/workers per shard: `4`
- Shards/jobs: `20`
- Seed: `20260718`
- Result type: checked ordered-chain reconstruction diagnostics from search-17 cover64 scaffolds; not a proof and not an ordered-trail improvement
- Artifacts: `order-cover64-stitch-run-summary`, `order-cover64-stitch-22-shard-*`

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

Best search-17 scaffold remains:

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

## Latest run lesson

Run `28875314204` tested contact-aware ordered reconstruction from the `64/64` line-set scaffolds. The result was much weaker than the existing ordered-trail frontier:

- best ordered reconstruction candidate: `mlct22-order-5c31614d2aeaa2aa`
- best covered_count: `44/64`
- links: `22`
- missing_count: `20`
- best mode: `one_two_line_mutation`
- best source shard/artifact: shard `7`, `order-cover64-stitch-22-shard-7`
- source scaffold: `mlct22-lineset-03bc99e72246b78c`
- result rows in summary: `40`
- compact unique ordered diagnostic candidates saved: `17`
- ordinary ordered-trail additions saved: `0`
- line-set scaffold additions saved: `0`
- diagnostic ordered-chain rows saved: `17`

Interpretation: search-17 showed that rich unordered `64/64` scaffolds exist, but search-18 showed that the current reconstruction model loses a lot of actual grid coverage when it converts those scaffolds into one ordered 22-link chain. Graph stitchability is much weaker than real polygonal-chain reconstruction.

Search-18 mode breakdown:

| mode | rows | unique | best links | best covered |
|---|---:|---:|---:|---:|
| `bridge_contact_repair` | 8 | 4 | 22 | 42 |
| `contact_extreme_search` | 8 | 4 | 22 | 42 |
| `control_fixed_best` | 2 | 1 | 22 | 40 |
| `large_neighborhood_ordering` | 6 | 3 | 22 | 43 |
| `one_two_line_mutation` | 8 | 4 | 22 | 44 |
| `strict_reconstruct_top4` | 8 | 1 | 22 | 42 |

Saved run-18 memory:

```text
runs/2026-07-07-smart-search-18-order-from-cover64-stitch-full/summary.md
runs/2026-07-07-smart-search-18-order-from-cover64-stitch-full/best_ordered_candidate.json
runs/2026-07-07-smart-search-18-order-from-cover64-stitch-full/mode_breakdown.json
runs/2026-07-07-smart-search-18-order-from-cover64-stitch-full/order-cover64-stitch-run-summary.zip
candidates/diagnostic-order-from-cover64-run28875314204.jsonl
candidates/originals/run28875314204-order-from-cover64-index.jsonl
```

## Current next step

Do not rerun `smart-search-18-order-from-cover64-stitch` unchanged. It answered a diagnostic question: the current ordering engine is too weak.

Next useful step should be a research/hypothesis step, not immediate relaunch. Diagnose the collapse from unordered `64/64` line-set coverage to actual ordered-chain `44/64` coverage. The likely next launch package should use a stronger contact-state reconstruction model, for example dynamic programming/beam search over `(line, contact point, covered mask)` states for the strongest search-17 scaffolds, with explicit accounting for which grid points are preserved or lost at each transition.
