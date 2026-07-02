# Current search frontier

This file is the human-readable working memory of the project.

Status: `smart-search-14-rich-cover-stitch` full run completed successfully. Numeric frontier remains `59/64`; run `28522369532` is recorded as the latest completed full run. It did not find `60/64`, but it produced more exact shard-best diversity than run `28460740781` and showed that rich-cover / endpoint-feasible stitching still collapses to a small set of `59/64` walls.

Latest recorded full run:

- Repository: `Grisha-Pochuev/minimum-link-covering-trail-4x4x4`
- Final run id: `28522369532`
- Run URL: https://github.com/Grisha-Pochuev/minimum-link-covering-trail-4x4x4/actions/runs/28522369532
- Workflow: `smart-search-14-rich-cover-stitch`
- Commit SHA of the run: `14318efc17aa14b648f87c5f608d40a3d006d921`
- Status: `success`
- Duration: full run, `21000` seconds per shard
- Threads per shard: `4`
- Shards/jobs: `20`
- Seed: `20260705`
- Result type: heuristic search, not a proof
- Artifacts: `rich-cover-stitch-run-summary`, `rich-cover-stitch-22-shard-*`

## Best GitHub Actions result

- candidate id: `mlct22-278a7d8dc1d65f25`
- covered_count: `59 / 64`
- coverage percent: `92.1875%`
- links: `22`
- selected mode: `new_skeleton_rich4`
- source artifact: `rich-cover-stitch-22-shard-0`
- source shard: `0`
- status: `partial_candidate`
- missing count: `5`
- missing:
  - `(1, 2, 2)`
  - `(2, 0, 2)`
  - `(2, 0, 3)`
  - `(3, 1, 2)`
  - `(3, 1, 3)`

The best candidate is still partial. It has exactly 22 links and covers 59 of the 64 grid points. This is not a complete covering trail and not a proof.

Saved run memory:

```text
runs/2026-07-01-smart-search-14-rich-cover-stitch-full/summary.md
runs/2026-07-01-smart-search-14-rich-cover-stitch-full/best_candidate.json
runs/2026-07-01-smart-search-14-rich-cover-stitch-full/mode_breakdown.json
runs/2026-07-01-smart-search-14-rich-cover-stitch-full/compact_representatives.md
candidates/bank-additions-run28522369532.jsonl
candidates/originals/run28522369532-shard-bests-index.jsonl
```

## Candidate memory from run 28522369532

- raw shard-best curves at the normal preservation threshold `covered_count >= 56`: `20`
- all raw shard-best curves were `59/64`
- exact unique `vertices2` curves among the 20: `7`
- compact bank additions saved: `7`
- exact IDs new relative to the recent recorded additions from runs `28460740781` and `28404861374`: `3`
- original shard-best index records saved: `20`

`candidates/bank.jsonl` was not merged in this step. The run-level additions were saved separately in `candidates/bank-additions-run28522369532.jsonl`.

## Dominant missing patterns from run 28522369532

- 12 / 20: `(0,1,2)`, `(1,2,1)`, `(1,3,2)`, `(2,1,3)`, `(2,2,2)`
- 7 / 20: `(1,2,2)`, `(2,0,2)`, `(2,0,3)`, `(3,1,2)`, `(3,1,3)`
- 1 / 20: `(1,2,1)`, `(2,1,2)`, `(2,2,3)`, `(3,1,2)`, `(3,1,3)`

## Top recurring missing points

- `(1, 2, 1)`: 13 / 20
- `(0, 1, 2)`: 12 / 20
- `(1, 3, 2)`: 12 / 20
- `(2, 1, 3)`: 12 / 20
- `(2, 2, 2)`: 12 / 20
- `(3, 1, 2)`: 8 / 20
- `(3, 1, 3)`: 8 / 20
- `(1, 2, 2)`: 7 / 20
- `(2, 0, 2)`: 7 / 20
- `(2, 0, 3)`: 7 / 20
- `(2, 1, 2)`: 1 / 20
- `(2, 2, 3)`: 1 / 20

## Comparison with previous frontier

Previous latest useful run was `28460740781`, also `59/64`, with `5` exact representatives and a dominant missing family in `14 / 20` shard-best artifacts. This run again reached only `59/64`, but had `7` exact representatives, `3` exact IDs not present in the recent recorded additions from runs `28460740781` and `28404861374`, and its dominant missing-set family appeared in `12 / 20` shard-best artifacts.

So the rich-cover / endpoint-feasible stitch-compress launch gave a real but still modest structural improvement: it reduced collapse, produced a new dominant `new_skeleton_rich4` representative, and exposed two competing `59/64` walls. But it still did not break the `59/64` wall.

## Current next step

Do not immediately launch another identical `smart-search-14-rich-cover-stitch` full run with the same seed and modes.

The useful next hypothesis should separate the two subproblems more sharply:

```text
cover-first diagnostics -> stitch-cost / transition graph diagnostics
```

In simple words: save and analyze the rich covering skeleton before it is forced into one trail, then measure the cost of stitching that skeleton into a continuous 22-link trail. The next search should preserve pre-stitch cover sets, transition-cost tables, and skeleton-level novelty, not only final shard-best curves.

A useful next full-run result is either any `60/64+` candidate with `links <= 22`, or concrete evidence showing whether the current blocker is poor rich-cover material or the price of stitching good material into one trail.
