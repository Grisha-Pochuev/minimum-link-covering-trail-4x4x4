# smart-search-11-d2-bridge-repair full run — results

Run URL: https://github.com/Grisha-Pochuev/minimum-link-covering-trail-4x4x4/actions/runs/28378489636

Workflow: `smart-search-11-d2-bridge-repair`

Run id: `28378489636`

Head commit SHA: `cb70091df2faa27d14d7921ec8779ab7256b25ff`

Status: `success`

Result type: heuristic search, not a proof.

## What was checked

The completed run used the workflow file as it existed at commit `cb70091df2faa27d14d7921ec8779ab7256b25ff`, not a newer workflow by assumption. The workflow is manual-only `workflow_dispatch`, starts with the known 23-link control check, then runs 20 D2 bridge repair shards and an aggregate job.

Observed jobs:

- `check-known-23`: success.
- `d2-bridge-repair-search`: 20 / 20 shard jobs succeeded.
- `aggregate-d2-bridge-results`: success.

Each shard passed the important steps: download previous artifacts, export candidate bank, prepare C++ engine, compile C++ engine, run shard, check shard result, upload artifact. The aggregate job downloaded all shard artifacts and uploaded `d2-bridge-run-summary`.

Inputs used by the run:

```text
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
shards/jobs: 20
max-parallel: 20
```

## Best candidate

- candidate id: `mlct22-a77764189bd3e13a`
- covered_count: `59 / 64`
- coverage percent: `92.1875%`
- links: `22`
- mode: `repair56_target8`
- source artifact: `d2-bridge-22-shard-0`
- source shard: `0`
- source file: `collected/d2_bridge_best_shard_0.json`
- status: `partial_candidate`
- missing count: `5`

Missing points:

- `(0, 2, 2)`
- `(2, 1, 2)`
- `(2, 2, 3)`
- `(3, 1, 0)`
- `(3, 1, 2)`

Local exact scaled check of all 20 shard-best candidates reproduced `22` links and `59` covered points for every saved shard-best candidate. No `60/64` or `64/64` candidate was found.

## Comparison with the previous frontier

Previous recorded frontier before this run was run `28338041580`, also `59/64`, with candidate `mlct22-252fb1171852b9db` and missing points:

```text
(1,0,1), (1,2,2), (1,3,2), (2,0,3), (2,2,2)
```

This run did not break the numeric frontier: `59/64 -> 59/64`.

But it did change the explored family. The new best selected by the aggregator has missing points:

```text
(0,2,2), (2,1,2), (2,2,3), (3,1,0), (3,1,2)
```

The previous run produced `7` compact symmetry representatives from 20 shard-best curves. This run produced `16` compact symmetry representatives from 20 shard-best curves. So the useful result is not a higher number, but more structural diversity and a new defect wall around `(2,1,2)` and `(2,2,3)`.

## Saved curves by search mode

| mode | saved curves | GitHub jobs | worker processes | best covered | total attempts |
|---|---:|---:|---:|---:|---:|
| `repair56_target8` | 6 | 6 | 24 | 59 | 1170085623 |
| `fractional_bridge22` | 4 | 4 | 16 | 59 | 797045841 |
| `transition_penalty22` | 4 | 4 | 16 | 59 | 771362816 |
| `subcube_stitch22` | 3 | 3 | 12 | 59 | 583096906 |
| `rich_segment_catalog` | 2 | 2 | 8 | 59 | 3327804882 |
| `integer_control22` | 1 | 1 | 4 | 59 | 371388118 |


Total saved raw shard-best curves: `20`.

Compact symmetry representatives from this run: `16`.

Total raw attempts reported by shard artifacts: `7020784186`.

## Missing-set patterns

| count | missing set |
|---:|---|
| 4 | `(1,2,2)`, `(2,1,2)`, `(2,2,3)`, `(3,1,0)`, `(3,1,2)` |
| 4 | `(1,2,1)`, `(2,1,2)`, `(2,2,3)`, `(3,1,0)`, `(3,1,3)` |
| 3 | `(1,0,1)`, `(1,2,2)`, `(1,3,2)`, `(2,0,3)`, `(2,2,2)` |
| 2 | `(1,2,2)`, `(1,3,1)`, `(1,3,2)`, `(2,1,2)`, `(2,2,3)` |
| 2 | `(0,2,2)`, `(2,1,2)`, `(2,2,3)`, `(3,1,2)`, `(3,1,3)` |
| 1 | `(0,2,2)`, `(2,1,2)`, `(2,2,3)`, `(3,1,0)`, `(3,1,2)` |
| 1 | `(1,2,1)`, `(2,1,2)`, `(2,2,3)`, `(3,1,2)`, `(3,1,3)` |
| 1 | `(0,2,2)`, `(2,1,2)`, `(2,2,3)`, `(3,1,0)`, `(3,1,3)` |
| 1 | `(0,1,0)`, `(1,2,3)`, `(2,1,0)`, `(3,1,1)`, `(3,1,3)` |
| 1 | `(1,2,2)`, `(2,1,2)`, `(2,2,3)`, `(3,1,0)`, `(3,1,3)` |


## What each search did, in simple words

`repair56_target8` kept direct pressure on older repair-style candidates. It produced 6 shard-best curves, all `59/64`, and contributed several new compact representatives.

`fractional_bridge22` used half-integer bridge-like geometry as a local repair tool. It produced 4 shard-best curves, all `59/64`, and helped confirm the new `(2,1,2)/(2,2,3)` wall.

`transition_penalty22` tried to stitch dense pieces while charging for bad transitions. It produced 4 shard-best curves, all `59/64`, including one unusual compact representative with missing `(0,1,0), (1,2,3), (2,1,0), (3,1,1), (3,1,3)`.

`subcube_stitch22` explored subcube/layer-style stitching. It produced 3 shard-best curves, all `59/64`.

`rich_segment_catalog` emphasized rich 3-point and 4-point segment structure. It produced 2 shard-best curves, both `59/64`, and recovered the old D2 champion family.

`integer_control22` was the conservative integer control. It produced 1 shard-best curve at `59/64`, also in the old D2 champion family.

## Conclusion

This was a trustworthy full run: the exact workflow from the run head commit was inspected, all 20 shard jobs completed, all shard artifacts were uploaded, and the aggregate artifact was created.

The result is not a proof and not a solution. No `60/64` or `64/64` candidate was found. The numeric frontier remains `59/64`.

The useful new information is structural: the run did not just repeat the previous D2 wall. It generated more compact representatives (`16` instead of `7`) and shifted the common missing points toward `(2,1,2)` and `(2,2,3)`. This suggests that the next step should analyze whether this is a genuinely new family or another symmetry-adjacent saturation wall before launching another expensive run.
