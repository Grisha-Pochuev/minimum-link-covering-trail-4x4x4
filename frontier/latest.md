# Current search frontier

This file is the human-readable working memory of the project.

Status: `smart-search-12-skeleton-diversity` full run completed successfully. Numeric frontier remains `59/64`; run `28404861374` is now recorded as the latest completed full run, but it did not improve the best coverage or structural diversity.

Latest recorded full run:

- Repository: `Grisha-Pochuev/minimum-link-covering-trail-4x4x4`
- Final run id: `28404861374`
- Run URL: https://github.com/Grisha-Pochuev/minimum-link-covering-trail-4x4x4/actions/runs/28404861374
- Workflow: `smart-search-12-skeleton-diversity`
- Commit SHA of the run: `7d7960619fbbb5389cb873715e1b698e2576972f`
- Status: `success`
- Duration: full run, `21000` seconds per shard
- Threads per shard: `4`
- Shards/jobs: `20`
- Result type: heuristic search, not a proof
- Artifacts: `skeleton-diversity-run-summary`, `skeleton-diversity-22-shard-*`

## Best GitHub Actions result

- candidate id: `mlct22-dddd317f06883acd`
- covered_count: `59 / 64`
- coverage percent: `92.1875%`
- links: `22`
- selected mode: `anti_wall22` in the run summary; the same exact curve also appeared under several other modes
- source artifact: `skeleton-diversity-22-shard-15`
- source shard: `15`
- status: `partial_candidate`
- missing count: `5`
- missing:
  - `(1, 2, 2)`
  - `(1, 3, 1)`
  - `(1, 3, 2)`
  - `(2, 0, 2)`
  - `(2, 0, 3)`

The best candidate is still partial. It has exactly 22 links and covers 59 of the 64 grid points. This is not a complete covering trail and not a proof.

Saved run memory:

```text
runs/2026-06-30-smart-search-12-skeleton-diversity-full/summary.md
runs/2026-06-30-smart-search-12-skeleton-diversity-full/best_candidate.json
runs/2026-06-30-smart-search-12-skeleton-diversity-full/mode_breakdown.json
runs/2026-06-30-smart-search-12-skeleton-diversity-full/compact_representatives.md
candidates/bank-additions-run28404861374.jsonl
candidates/originals/run28404861374-shard-bests-index.jsonl
```

## Candidate memory from run 28404861374

- raw shard-best curves at the normal preservation threshold `covered_count >= 56`: `20`
- all raw shard-best curves were `59/64`
- exact unique `vertices2` curves among the 20: `3`
- compact bank additions saved: `3`
- original shard-best index records saved: `20`

`candidates/bank.jsonl` was not merged in this step. The run-level additions were saved separately in `candidates/bank-additions-run28404861374.jsonl`.

## Dominant missing patterns from run 28404861374

- 18 / 20: `(1,2,2)`, `(1,3,1)`, `(1,3,2)`, `(2,0,2)`, `(2,0,3)`
- 1 / 20: `(0,2,0)`, `(2,1,2)`, `(2,2,3)`, `(3,1,0)`, `(3,1,2)`
- 1 / 20: `(0,1,2)`, `(1,2,1)`, `(1,3,2)`, `(2,1,3)`, `(2,2,2)`

## Top recurring missing points

- `(1, 3, 2)`: 19 / 20
- `(1, 2, 2)`: 18 / 20
- `(1, 3, 1)`: 18 / 20
- `(2, 0, 2)`: 18 / 20
- `(2, 0, 3)`: 18 / 20

## Comparison with previous frontier

Previous latest useful run was `28378489636`, also `59/64`, with `16` compact representatives. This run again reached only `59/64`, and its diversity was lower: only `3` exact `vertices2` representatives, with one dominant candidate appearing in `18 / 20` shard-best artifacts.

So the intended skeleton-diversity launch did not really escape the old frontier. It mostly collapsed back to a strong `59/64` family. This is useful negative evidence: the next generator should impose stronger novelty pressure rather than trusting broad skeleton-diversity labels alone.

## Current next step

Do not immediately launch another identical `smart-search-12-skeleton-diversity` full run with the same seed and modes.

The next step should be a hypothesis and generator-revision step: either hard-block the dominant 5-hole family, deliberately seed from structurally different `56/64`-`58/64` curves, or run a smaller diagnostic that scores new missing-set geometry more strongly than raw `59/64` reuse.
