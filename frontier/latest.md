# Current search frontier

This file is the human-readable working memory of the project.

Status: `smart-search-10-d-family-repair` has been prepared as the next manual GitHub smoke-test workflow. Numeric frontier remains `59/64`; the latest completed useful run is still `smart-search-9-new-defect-repair` run `28327372242`.

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
runs/2026-06-28-smart-search-9-new-defect-repair-full/local_preflight.md
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

## Prepared next workflow

Prepared workflow:

```text
smart-search-10-d-family-repair
.github/workflows/smart-search-10-d-family-repair.yml
```

Prepared support files:

```text
scripts/prepare_d_family_repair_engine.py
docs/smart-search-10-d-family-repair-plan.md
```

The workflow is manual-only with `workflow_dispatch`. It has no push trigger.

Purpose:

```text
Repair the D-family wall exposed by run 28327372242, especially (1,3,1), (1,3,2), (2,0,2), and (2,0,3), while keeping the old A-family from run 28304497479 as a guardrail so the search does not merely rotate back to the previous obstruction.
```

## Smoke-test launch inputs

```text
workflow: smart-search-10-d-family-repair
seconds: 180
threads: 4
seed: 20260701
prior_run_id: 28327372242
orbit_bridge_run_id: 28304497479
previous_core5_run_id: 28292425390
old_59_run_id: 28275850889
secondary_run_id: 28275666411
base_repair_run_id: 28200925016
min_covered_to_save: 56
jobs/shards: 20
max-parallel: 20
```

## Full serious-run inputs after smoke-test succeeds

```text
workflow: smart-search-10-d-family-repair
seconds: 21000
threads: 4
seed: 20260701
prior_run_id: 28327372242
orbit_bridge_run_id: 28304497479
previous_core5_run_id: 28292425390
old_59_run_id: 28275850889
secondary_run_id: 28275666411
base_repair_run_id: 28200925016
min_covered_to_save: 56
jobs/shards: 20
max-parallel: 20
expected wall time: about 5h50m per shard
```
