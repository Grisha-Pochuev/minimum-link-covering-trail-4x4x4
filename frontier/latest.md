# Current search frontier

Status: completed full run `smart-search-20-line-bridge` on 2026-07-09. The normal ordered-trail frontier remains `60/64`; the scaffold frontier from search-17 remains unordered `64/64` with stitch path lower bound `22/22`. Search-20 improved the ordered reconstruction / bridge diagnostic ceiling from `46/64` to `58/64`, but did not improve the actual ordered-trail frontier.

Latest recorded completed full run:

- Repository: `Grisha-Pochuev/minimum-link-covering-trail-4x4x4`
- Final run id: `28973760924`
- Run URL: https://github.com/Grisha-Pochuev/minimum-link-covering-trail-4x4x4/actions/runs/28973760924
- Workflow: `smart-search-20-line-bridge`
- Commit SHA of the run: `772596df3d9fd796d2a5bf5ee0ea48697ca17031`
- Status: `success`
- Profile: `full`
- Duration: long run, `21000` seconds per shard
- Workers per shard: `4`
- Shards/jobs: `20`
- Seed: `20260720`
- Result type: full-line-preserving bridge ordered-chain diagnostic from search-17 cover64 scaffolds; below the ordered-trail frontier, not a proof and not an ordered-trail improvement
- Artifacts: `smart-search-20-line-bridge-run-summary`, `smart-search-20-line-bridge-22-shard-*`

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

## Latest recorded run lesson

Run `28973760924` completed `smart-search-20-line-bridge` successfully. All prechecks, 20 line-bridge shard jobs, and the aggregate job succeeded.

Best line-bridge ordered-chain diagnostic:

- candidate id: `mlct22-flbridge-8da0e01c34bb9c88`
- best covered_count: `58/64`
- links: `22`
- missing_count: `6`
- missing: `(0,2,0)`, `(0,2,2)`, `(2,1,0)`, `(2,1,2)`, `(2,3,0)`, `(3,2,0)`
- best mode: `one_line_replacement`
- best source shard/artifact: shard `16`, `smart-search-20-line-bridge-22-shard-16`
- full-line links: `14`
- bridge links: `8`
- preserved rich lines: `14`
- official60 old-missing hits: `4`
- result rows in summary: `40`
- shard-best outputs: `20`
- unique compact ordered candidates in summary: `6`
- compact diagnostic candidates saved: `6`
- ordinary ordered-trail additions saved: `0`
- line-set scaffold additions saved: `0`

Interpretation: search-20 is a major diagnostic improvement over search-19 (`46/64 -> 58/64`), but still below the standing ordered-trail frontier `60/64`. It confirms that preserving rich scaffold lines is much better than contact-state clipping, but eight explicit bridge links are still too expensive.

The important new failure mode is not the old official four-hole wall. The best search-20 candidate hits all four old missing points from the `60/64` candidate, then opens a new six-hole bridge-defect family:

```text
(0,2,0), (0,2,2), (2,1,0), (2,1,2), (2,3,0), (3,2,0)
```

Most repeated aggregate missing points:

```text
(3,2,2), (2,3,2), (0,0,3), (2,0,1), (2,3,1), (2,3,3), (3,0,1), (0,0,1)
```

Saved run-20 memory:

```text
runs/2026-07-09-smart-search-20-line-bridge-full/summary.md
runs/2026-07-09-smart-search-20-line-bridge-full/best_line_bridge_candidate.json
runs/2026-07-09-smart-search-20-line-bridge-full/line_bridge_run_summary_compact.json
runs/2026-07-09-smart-search-20-line-bridge-full/mode_breakdown.json
candidates/diagnostic-line-bridge-run28973760924.jsonl
candidates/originals/run28973760924-line-bridge-index.jsonl
```

## Candidate preservation rule

Keep three banks separate:

1. ordinary ordered-trail candidates: only checked polygonal trails that are near or above the current ordered frontier;
2. line-set scaffolds: unordered cover64 line sets from search-17 and related runs;
3. ordered-chain diagnostics: search-18/search-19/search-20 reconstruction attempts below the frontier.

Search-20 outputs are checked full-length ordered-chain diagnostics, but their best is `58/64`, below the current `60/64` ordered-trail frontier. They should not be treated as ordinary candidate-bank improvements.

## Current next step

The prepared `smart-search-20-line-bridge` hypothesis has now been tried. Do not rerun search-17, search-18, search-19, or search-20 unchanged as the next serious step.

Next prompt should be Prompt 2: choose a new non-repeating hypothesis using the search-20 lesson. The useful lesson is: full-line preservation helped a lot, but spending 8 bridge links still leaves a new six-hole bridge-defect family. The next idea should reduce bridge cost, change the scaffold ordering principle, or construct richer endpoint-compatible scaffolds rather than repeating the same line-bridge workflow.
