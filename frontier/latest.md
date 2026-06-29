# Current search frontier

This file is the human-readable working memory of the project.

Status: `smart-search-11-d2-bridge-repair` full run completed successfully. Numeric frontier remains `59/64`; the latest useful completed run is run `28378489636`.

Latest useful completed run:

- Repository: `Grisha-Pochuev/minimum-link-covering-trail-4x4x4`
- Final run id: `28378489636`
- Run URL: https://github.com/Grisha-Pochuev/minimum-link-covering-trail-4x4x4/actions/runs/28378489636
- Workflow: `smart-search-11-d2-bridge-repair`
- Commit SHA of the run: `cb70091df2faa27d14d7921ec8779ab7256b25ff`
- Status: `success`
- Duration: full run, `21000` seconds per shard
- Result type: heuristic search, not a proof
- Artifacts: `d2-bridge-run-summary`, `d2-bridge-22-shard-*`

## Best GitHub Actions result

- candidate id: `mlct22-a77764189bd3e13a`
- covered_count: `59 / 64`
- coverage percent: `92.1875%`
- links: `22`
- selected mode: `repair56_target8`
- source artifact: `d2-bridge-22-shard-0`
- source shard: `0`
- status: `partial_candidate`
- missing count: `5`
- missing:
  - `(0, 2, 2)`
  - `(2, 1, 2)`
  - `(2, 2, 3)`
  - `(3, 1, 0)`
  - `(3, 1, 2)`

The best candidate is still partial. It has exactly 22 links and covers 59 of the 64 grid points. This is not a complete covering trail and not a proof.

Saved run memory:

```text
runs/2026-06-29-smart-search-11-d2-bridge-repair-full/summary.md
runs/2026-06-29-smart-search-11-d2-bridge-repair-full/best_candidate.json
runs/2026-06-29-smart-search-11-d2-bridge-repair-full/mode_breakdown.json
runs/2026-06-29-smart-search-11-d2-bridge-repair-full/compact_representatives.md
```

Note: `candidates/bank.jsonl` was inspected for comparison, but it was not merged in this step. The next hypothesis step should decide whether the 16 compact representatives are useful enough to formalize as `bank-additions` for future search seeding.

## Dominant missing patterns from run 28378489636

- 4 / 20: `(1,2,2)`, `(2,1,2)`, `(2,2,3)`, `(3,1,0)`, `(3,1,2)`
- 4 / 20: `(1,2,1)`, `(2,1,2)`, `(2,2,3)`, `(3,1,0)`, `(3,1,3)`
- 3 / 20: `(1,0,1)`, `(1,2,2)`, `(1,3,2)`, `(2,0,3)`, `(2,2,2)`
- 2 / 20: `(1,2,2)`, `(1,3,1)`, `(1,3,2)`, `(2,1,2)`, `(2,2,3)`
- 2 / 20: `(0,2,2)`, `(2,1,2)`, `(2,2,3)`, `(3,1,2)`, `(3,1,3)`
- 1 / 20: `(0,2,2)`, `(2,1,2)`, `(2,2,3)`, `(3,1,0)`, `(3,1,2)`
- 1 / 20: `(1,2,1)`, `(2,1,2)`, `(2,2,3)`, `(3,1,2)`, `(3,1,3)`
- 1 / 20: `(0,2,2)`, `(2,1,2)`, `(2,2,3)`, `(3,1,0)`, `(3,1,3)`
- 1 / 20: `(0,1,0)`, `(1,2,3)`, `(2,1,0)`, `(3,1,1)`, `(3,1,3)`
- 1 / 20: `(1,2,2)`, `(2,1,2)`, `(2,2,3)`, `(3,1,0)`, `(3,1,3)`

## Top recurring missing points

- `(2, 1, 2)`: 16 / 20
- `(2, 2, 3)`: 16 / 20
- `(3, 1, 0)`: 11 / 20
- `(1, 2, 2)`: 10 / 20
- `(3, 1, 3)`: 10 / 20
- `(3, 1, 2)`: 8 / 20
- `(1, 3, 2)`: 5 / 20
- `(1, 2, 1)`: 5 / 20
- `(0, 2, 2)`: 4 / 20
- `(1, 0, 1)`: 3 / 20
- `(2, 0, 3)`: 3 / 20
- `(2, 2, 2)`: 3 / 20
- `(1, 3, 1)`: 2 / 20
- `(0, 1, 0)`: 1 / 20
- `(1, 2, 3)`: 1 / 20
- `(2, 1, 0)`: 1 / 20
- `(3, 1, 1)`: 1 / 20


## Comparison with previous frontier

Previous latest useful run was `28338041580`, also `59/64`, with dominant D2-family missing set `(1,0,1)`, `(1,2,2)`, `(1,3,2)`, `(2,0,3)`, `(2,2,2)`.

This run did not improve the number. It did improve the diversity of stored curves: previous run had `7` compact representatives from 20 shard-best curves; this run has `16` compact representatives from 20 shard-best curves.

The most important new sign is a shifted defect wall. The points `(2,1,2)` and `(2,2,3)` became extremely common, appearing in `16 / 20` shard-best candidates. So the run seems to have escaped part of the previous D2 wall but saturated against a nearby new wall.

## Current next step

Do not immediately launch another identical D2 bridge full run with the same seed and modes.

The next step should be a hypothesis step: compare the new compact representatives with old A/D/D2 families and decide whether to continue bridge repair, switch to new-skeleton search, or design a smaller diagnostic around the `(2,1,2)/(2,2,3)` wall.
