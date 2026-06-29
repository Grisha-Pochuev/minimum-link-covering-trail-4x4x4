# Current search frontier

This file is the human-readable working memory of the project.

Status: `smart-search-10-d-family-repair` full run completed successfully. Numeric frontier remains `59/64`; the latest useful completed run is run `28338041580`.

Latest useful completed run:

- Repository: `Grisha-Pochuev/minimum-link-covering-trail-4x4x4`
- Final run id: `28338041580`
- Run URL: https://github.com/Grisha-Pochuev/minimum-link-covering-trail-4x4x4/actions/runs/28338041580
- Workflow: `smart-search-10-d-family-repair`
- Commit SHA of the run: `226397ba84fbd8e5415c9be188f651f4af909588`
- Status: `success`
- Duration: full run, `21000` seconds per shard
- Result type: heuristic search, not a proof
- Artifacts: `d-family-run-summary`, `d-family-22-shard-*`

## Best GitHub Actions result

- candidate id: `mlct22-252fb1171852b9db`
- covered_count: `59 / 64`
- coverage percent: `92.1875%`
- links: `22`
- selected mode: `repair56_target8`
- source artifact: `d-family-22-shard-16`
- source shard: `16`
- status: `partial_candidate`
- missing count: `5`
- missing:
  - `(1, 0, 1)`
  - `(1, 2, 2)`
  - `(1, 3, 2)`
  - `(2, 0, 3)`
  - `(2, 2, 2)`

The best candidate is still partial. It has exactly 22 links and covers 59 of the 64 grid points. This is not a complete covering trail and not a proof.

Saved run memory:

```text
runs/2026-06-29-smart-search-10-d-family-repair-full/summary.md
runs/2026-06-29-smart-search-10-d-family-repair-full/best_candidate.json
runs/2026-06-29-smart-search-10-d-family-repair-full/smart_run_summary.json
runs/2026-06-29-smart-search-10-d-family-repair-full/mode_breakdown.json
candidates/bank-additions-run28338041580.jsonl
candidates/originals/run-28338041580-smart-search-10-d-family-repair.jsonl
```

## Dominant missing patterns from run 28338041580

- 9 / 20: `(1,0,1), (1,2,2), (1,3,2), (2,0,3), (2,2,2)`
- 7 / 20: `(1,0,1), (1,2,1), (1,3,2), (2,0,3), (2,2,2)`
- 2 / 20: `(0,2,2), (2,1,3), (2,2,3), (3,1,0), (3,1,2)`
- 1 / 20: `(0,2,2), (1,0,1), (1,3,2), (2,0,3), (2,2,2)`
- 1 / 20: `(1,2,2), (2,0,2), (2,0,3), (3,1,0), (3,1,2)`

## Top recurring missing points

- `(2, 0, 3)`: 18 / 20
- `(1, 0, 1)`: 17 / 20
- `(1, 3, 2)`: 17 / 20
- `(2, 2, 2)`: 17 / 20
- `(1, 2, 2)`: 10 / 20
- `(1, 2, 1)`: 7 / 20
- `(0, 2, 2)`: 3 / 20
- `(3, 1, 0)`: 3 / 20
- `(3, 1, 2)`: 3 / 20
- `(2, 1, 3)`: 2 / 20
- `(2, 2, 3)`: 2 / 20
- `(2, 0, 2)`: 1 / 20

## Comparison with previous frontier

Previous latest useful run was `28327372242`, also `59/64`, with dominant D-family missing set `(1,2,2)`, `(1,3,1)`, `(1,3,2)`, `(2,0,2)`, `(2,0,3)`.

This run did not improve the number. It did improve the map of the obstruction: `(2,0,2)` is no longer common, but `(1,0,1)` and `(2,2,2)` became very common. So the next useful target is the new D2-family wall, not a blind repeat of the same workflow.

## Current prepared next workflow

Prepared workflow:

```text
smart-search-11-d2-bridge-repair
.github/workflows/smart-search-11-d2-bridge-repair.yml
```

Prepared support files:

```text
scripts/prepare_d2_bridge_repair_engine.py
docs/smart-search-11-d2-bridge-repair-plan.md
```

The workflow is manual-only with `workflow_dispatch`. It has no push trigger.

Purpose:

```text
Attack the new D2 wall around (1,0,1), (1,3,2), (2,0,3), and (2,2,2), with (1,2,2)/(1,2,1) as variable fifth points, while keeping old A/D families as guardrails.
```

Safe smoke-test parameters:

```text
workflow: smart-search-11-d2-bridge-repair
seconds: 180
threads: 4
seed: 20260702
latest_d2_run_id: 28338041580
prior_d_run_id: 28327372242
orbit_bridge_run_id: 28304497479
previous_core5_run_id: 28292425390
old_59_run_id: 28275850889
secondary_run_id: 28275666411
base_repair_run_id: 28200925016
min_covered_to_save: 56
jobs/shards: 20
max-parallel: 20
```

Full serious-run parameters after the smoke-test succeeds:

```text
workflow: smart-search-11-d2-bridge-repair
seconds: 21000
threads: 4
seed: 20260702
latest_d2_run_id: 28338041580
prior_d_run_id: 28327372242
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
