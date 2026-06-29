# smart-search-10-d-family-repair full run — results

Run URL: https://github.com/Grisha-Pochuev/minimum-link-covering-trail-4x4x4/actions/runs/28338041580

Workflow: `smart-search-10-d-family-repair`

Run id: `28338041580`

Head commit SHA: `226397ba84fbd8e5415c9be188f651f4af909588`

Status: `success`

Result type: heuristic search, not a proof.

## What was checked

The completed run used the workflow file as it existed at commit `226397ba84fbd8e5415c9be188f651f4af909588`, not the newest workflow by assumption. The workflow is manual-only `workflow_dispatch`, starts with the known 23-link control check, then runs 20 D-family repair shards and an aggregate job.

Observed jobs:

- `check-known-23`: success.
- `d-family-repair-search`: 20 / 20 shard jobs succeeded.
- `aggregate-d-family-results`: success.

Each shard passed these important steps: download previous artifacts, export candidate bank, prepare C++ engine, compile C++ engine, run shard, check shard result, upload artifact. The aggregate job downloaded all shard artifacts and uploaded `d-family-run-summary`.

Inputs used by the run:

```text
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
shards/jobs: 20
max-parallel: 20
```

## Best candidate

- candidate id: `mlct22-252fb1171852b9db`
- covered_count: `59 / 64`
- coverage percent: `92.1875%`
- links: `22`
- mode: `repair56_target8`
- source artifact: `d-family-22-shard-16`
- source shard: `16`
- source file: `collected/d_family_best_shard_16.json`
- status: `partial_candidate`
- missing count: `5`

Missing points:

- `(1, 0, 1)`
- `(1, 2, 2)`
- `(1, 3, 2)`
- `(2, 0, 3)`
- `(2, 2, 2)`

Local exact scaled check of the selected best candidate reproduced `22` links, `59` covered points, and exactly the same 5 missing points.

## Comparison with the previous frontier

Previous recorded frontier before this run was run `28327372242`, also `59/64`, with missing points:

```text
(1,2,2), (1,3,1), (1,3,2), (2,0,2), (2,0,3)
```

This run did not break the numeric frontier: `59/64 -> 59/64`. But it changed the dominant obstruction. The new dominant core is centered on:

```text
(1,0,1), (1,3,2), (2,0,3), (2,2,2)
```

The old D-family point `(2,0,2)` almost disappeared: it occurs in only 1 of 20 shard-best candidates. The run usually replaced it by `(1,0,1)` and `(2,2,2)`. So the search did learn something: closing the old D-wall tends to rotate into a new D2-style wall rather than rising to `60/64`.

## Saved curves by search mode

| mode | saved curves | GitHub jobs | worker processes | best covered | total attempts |
|---|---:|---:|---:|---:|---:|
| `transition_penalty22` | 6 | 6 | 24 | 59 | 2054058073 |
| `fractional_bridge22` | 5 | 5 | 20 | 59 | 1767617770 |
| `subcube_stitch22` | 3 | 3 | 12 | 59 | 969131096 |
| `repair56_target8` | 3 | 3 | 12 | 59 | 994043668 |
| `rich_segment_catalog` | 2 | 2 | 8 | 59 | 3307812707 |
| `integer_control22` | 1 | 1 | 4 | 59 | 375196832 |

Total saved shard-best curves: `20`.

Compact symmetry representatives from this run: `7`.

Total raw attempts reported by shard artifacts: `9467860146`.

## Missing-set patterns

| count | missing set |
|---:|---|
| 9 | `(1,0,1), (1,2,2), (1,3,2), (2,0,3), (2,2,2)` |
| 7 | `(1,0,1), (1,2,1), (1,3,2), (2,0,3), (2,2,2)` |
| 2 | `(0,2,2), (2,1,3), (2,2,3), (3,1,0), (3,1,2)` |
| 1 | `(0,2,2), (1,0,1), (1,3,2), (2,0,3), (2,2,2)` |
| 1 | `(1,2,2), (2,0,2), (2,0,3), (3,1,0), (3,1,2)` |

## What each search did, in simple words

`transition_penalty22` tried to stitch good dense pieces while charging a penalty for bad transitions. It produced 6 saved shard-best curves, all `59/64`, and mostly fell into the new core pattern with `(1,0,1)`, `(1,3,2)`, `(2,0,3)`, `(2,2,2)`.

`fractional_bridge22` allowed half-integer and bridge-like vertices as a local tool. It produced 5 saved shard-best curves, all `59/64`; it found one nearby alternative missing-set pattern but did not push to `60/64`.

`subcube_stitch22` tried to connect dense pieces through subcube/layer structure. It produced 3 saved shard-best curves, all `59/64`, again mostly returning to the new D2-style obstruction.

`repair56_target8` was a direct repair pressure mode aimed at older defect points. It produced 3 saved shard-best curves, all `59/64`; the selected champion came from this mode.

`rich_segment_catalog` emphasized rich 3-point and 4-point segment structure. It produced 2 saved shard-best curves, both `59/64`; these are useful because they recovered old A/D-family guardrail patterns rather than the dominant new core.

`integer_control22` was the conservative integer control. It produced 1 saved shard-best curve at `59/64`, matching the old guardrail family rather than beating the frontier.

## Conclusion

This was a trustworthy full run: the workflow was manual-only, used the intended seed sources, all 20 shards completed, artifacts were uploaded, and aggregation succeeded.

The result is not a proof and not a solution. No `60/64` or `64/64` candidate was found. The numeric frontier remains `59/64`.

The useful new information is structural: smart-search-10 strongly shows a new saturation pattern. It successfully moved pressure away from `(2,0,2)`, but the search then stabilized around `(1,0,1)` and `(2,2,2)`. The next useful step should not be another identical full run with the same seed and modes. It should be local analysis or a new workflow specifically aimed at this new D2-family wall.
