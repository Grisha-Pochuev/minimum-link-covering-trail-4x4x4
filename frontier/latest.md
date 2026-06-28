# Current search frontier

This file is the human-readable working memory of the project.

Status: `smart-search-9-new-defect-repair` completed successfully. Numeric frontier remains `59/64`, but the run exposed a new dominant D-family defect pattern. Do not repeat this workflow unchanged before a local repair preflight.

Latest useful completed run:

- Repository: `Grisha-Pochuev/minimum-link-covering-trail-4x4x4`
- Final run id: `28327372242`
- Run URL: https://github.com/Grisha-Pochuev/minimum-link-covering-trail-4x4x4/actions/runs/28327372242
- Workflow: `smart-search-9-new-defect-repair`
- Commit SHA of the run: `23ed729adbed07ca1dd4983f2de20276383bc633`
- Status: `success`
- Duration: full run, `21000` seconds per shard
- Result type: heuristic search, not a proof
- Artifacts: `new-defect-run-summary`, `new-defect-22-shard-*`

## Best GitHub Actions result

- candidate id: `mlct22-a495eb7a0c4f489d`
- covered_count: `59 / 64`
- coverage percent: `92.1875%`
- links: `22`
- selected mode: `transition_penalty22`
- source artifact: `new-defect-22-shard-0`
- source shard: `0`
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
runs/2026-06-28-smart-search-9-new-defect-repair-full/summary.md
runs/2026-06-28-smart-search-9-new-defect-repair-full/best_candidate.json
candidates/bank-additions-run28327372242.jsonl
```

## Dominant missing patterns from run 28327372242

- 12 / 20: `(1,2,2)`, `(1,3,1)`, `(1,3,2)`, `(2,0,2)`, `(2,0,3)`
- 4 / 20: `(0,2,2)`, `(2,1,3)`, `(2,2,3)`, `(3,1,0)`, `(3,1,2)`
- 3 / 20: `(0,0,2)`, `(1,2,3)`, `(2,0,1)`, `(2,1,0)`, `(3,1,1)`
- 1 / 20: `(1,3,1)`, `(2,1,2)`, `(2,2,3)`, `(3,1,0)`, `(3,1,3)`

## Top recurring missing points

- `(1, 3, 1)`: 13 / 20
- `(1, 2, 2)`: 12 / 20
- `(1, 3, 2)`: 12 / 20
- `(2, 0, 2)`: 12 / 20
- `(2, 0, 3)`: 12 / 20
- `(2, 2, 3)`: 5 / 20
- `(3, 1, 0)`: 5 / 20
- `(0, 2, 2)`: 4 / 20
- `(2, 1, 3)`: 4 / 20
- `(3, 1, 2)`: 4 / 20

## Next local preflight

Before another expensive GitHub run, compare the new D-family champion against the previous A-family champion. Locally test whether a 4-12 link window replacement can close `(1,3,1)`, `(1,3,2)`, `(2,0,2)`, and `(2,0,3)` without recreating `(0,2,2)`, `(2,1,3)`, `(2,2,3)`, `(3,1,0)`, `(3,1,2)`.
