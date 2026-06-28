# Current search frontier

This file is the human-readable working memory of the project.

Status: `smart-search-9-new-defect-repair` has been prepared as the next manual workflow. Numeric frontier remains `59/64`, but the next workflow now targets the new A/B defect families exposed by `smart-search-8-orbit-bridge` instead of repeating smart-search-8 unchanged.

Latest useful completed run:

- Repository: `Grisha-Pochuev/minimum-link-covering-trail-4x4x4`
- Final run id: `28304497479`
- Run URL: https://github.com/Grisha-Pochuev/minimum-link-covering-trail-4x4x4/actions/runs/28304497479
- Workflow: `smart-search-8-orbit-bridge`
- Commit SHA of the run: `bd5630200cec8e3338435a18ac1d9974e864d63e`
- Status: `success`
- Duration: full run, `21000` seconds per shard
- Result type: heuristic search, not a proof
- Artifacts: `orbit-bridge-run-summary`, `orbit-bridge-22-shard-*`, `orbit-bridge-seed-manifest-*`

## Parameters of latest completed run

- seconds: `21000`
- threads: `4` per shard
- shards/jobs: `20`
- max parallel jobs: `20`
- seed: `20260629`
- prior run id: `28292425390`
- old 59 run id: `28275850889`
- secondary run id: `28275666411`
- base repair run id: `28200925016`
- coordinate scale: `2`
- min covered to save: `56`
- checker: `scripts/check_scaled_trail.py`

## Best GitHub Actions result

Best known result after run `28304497479`:

- covered_count: `59 / 64`
- coverage percent: `92.1875%`
- links: `22`
- links target: `22`
- selected mode: `subcube_stitch22`
- source artifact: `orbit-bridge-22-shard-10`
- source shard: `10`
- candidate id: `mlct22-9c80a2741db704ad`
- status: `partial_candidate`
- missing count: `5`
- missing:
  - `(0, 2, 2)`
  - `(2, 1, 3)`
  - `(2, 2, 3)`
  - `(3, 1, 0)`
  - `(3, 1, 2)`

The best candidate is still partial. It has exactly 22 links and covers 59 of the 64 grid points. This is not a complete covering trail and not a proof.

The exact selected best candidate is saved in:

```text
runs/2026-06-28-smart-search-8-orbit-bridge-full/best_candidate.json
```

A run summary is saved in:

```text
runs/2026-06-28-smart-search-8-orbit-bridge-full/summary.md
```

The 3 unique eligible additions from this run are saved safely in:

```text
candidates/bank-additions-run28304497479.jsonl
candidates/bank-additions-run28304497479.summary.json
```

## Candidate preservation rule

The workflow threshold was:

```text
covered_count >= 56
links <= 22
```

All 20 shard-best candidates met this threshold. They all had `59/64` coverage and 22 links. Canonical deduplication reduced them to 3 unique candidate families.

## Top recurring missing points from run 28304497479

Counted over the 20 shard-best JSON result files:

- `(2, 2, 3)`: 13 / 20
- `(3, 1, 0)`: 13 / 20
- `(0, 2, 2)`: 11 / 20
- `(2, 1, 3)`: 11 / 20
- `(3, 1, 2)`: 11 / 20
- `(1, 0, 1)`: 7 / 20
- `(1, 2, 2)`: 7 / 20
- `(1, 3, 2)`: 7 / 20
- `(2, 0, 3)`: 7 / 20
- `(2, 2, 2)`: 7 / 20
- `(1, 2, 1)`: 2 / 20
- `(2, 1, 2)`: 2 / 20
- `(3, 1, 3)`: 2 / 20

## Dominant missing patterns

Across the 20 shard-best results:

- 11 / 20: `(0,2,2)`, `(2,1,3)`, `(2,2,3)`, `(3,1,0)`, `(3,1,2)`
- 7 / 20: `(1,0,1)`, `(1,2,2)`, `(1,3,2)`, `(2,0,3)`, `(2,2,2)`
- 2 / 20: `(1,2,1)`, `(2,1,2)`, `(2,2,3)`, `(3,1,0)`, `(3,1,3)`

## Which modes worked best in run 28304497479

All modes represented in shard-best results reached `59/64`:

- `fractional_bridge22`: 5 result(s), best `59/64`, average `59.00/64`, shards `[5, 6, 7, 8, 9]`
- `integer_control22`: 1 result(s), best `59/64`, average `59.00/64`, shards `[19]`
- `repair56_target8`: 3 result(s), best `59/64`, average `59.00/64`, shards `[15, 16, 17]`
- `rich_segment_catalog`: 1 result(s), best `59/64`, average `59.00/64`, shards `[18]`
- `subcube_stitch22`: 5 result(s), best `59/64`, average `59.00/64`, shards `[10, 11, 12, 13, 14]`
- `transition_penalty22`: 5 result(s), best `59/64`, average `59.00/64`, shards `[0, 1, 2, 3, 4]`

The conclusion changed in an important way: the old shared hard point `(3,1,3)` was successfully suppressed in most shards, but the search still saturated at `59/64`. The obstruction moved into two new dominant 5-point patterns.

## Comparison with previous runs

- Run `28103660449` / smart-search-4: best `56/64`, 8 missing points.
- Local prelaunch repair smoke: best `57/64`, 7 missing points.
- Run `28200925016` / repair-search-5: best `58/64`, 6 missing points.
- Run `28275666411` / smart-search-6-defect smoke-test: best `59/64`, 5 missing points.
- Run `28275850889` / smart-search-6-defect full run: best `59/64`, old 5-point defect core.
- Run `28292425390` / smart-search-7-core5 full run: best `59/64`, different 5-point defect orbit with `(3,1,3)` still frequent.
- Run `28304497479` / smart-search-8-orbit-bridge full run: best `59/64`, new A/B defect families; `(3,1,3)` appears only `2/20` shard-best results.

So run `28304497479` did not raise the numeric frontier, but it is useful: it shows that targeting `(3,1,3)` can move the obstruction elsewhere instead of breaking through to `60/64`.

## Prepared next run

Prepared workflow:

```text
smart-search-9-new-defect-repair
.github/workflows/smart-search-9-new-defect-repair.yml
```

Prepared support files:

```text
scripts/prepare_new_defect_repair_engine.py
docs/smart-search-9-new-defect-repair-plan.md
```

The new workflow is manual-only with `workflow_dispatch`. It has no push trigger.

Prepared next focus:

```text
Repair the new A/B defect patterns from run 28304497479. Pattern A appeared 11/20; pattern B appeared 7/20. Keep `(3,1,3)` as a control, but stop treating it as the only center: smart-search-8 mostly closed it and exposed a different obstruction.
```

## Next run seed source

The next serious run should start from:

- GitHub Actions artifacts of run `28304497479`;
- `orbit-bridge-run-summary` from this run;
- all `orbit-bridge-22-shard-*` artifacts from this run;
- `runs/2026-06-28-smart-search-8-orbit-bridge-full/best_candidate.json`;
- `candidates/bank-additions-run28304497479.jsonl`;
- `candidates/bank-additions-run28292425390.jsonl`;
- older runs `28292425390`, `28275850889`, `28275666411`, and `28200925016`;
- `candidates/bank.jsonl` as broad seed memory.

## Smoke-test launch idea

Use the default manual workflow inputs first:

```text
workflow: smart-search-9-new-defect-repair
seconds: 180
threads: 4
seed: 20260630
prior_run_id: 28304497479
previous_core5_run_id: 28292425390
old_59_run_id: 28275850889
secondary_run_id: 28275666411
base_repair_run_id: 28200925016
min_covered_to_save: 56
jobs/shards: 20
max-parallel: 20
```

## Full serious-run launch idea after smoke-test succeeds

```text
workflow: smart-search-9-new-defect-repair
seconds: 21000
threads: 4
seed: 20260630
prior_run_id: 28304497479
previous_core5_run_id: 28292425390
old_59_run_id: 28275850889
secondary_run_id: 28275666411
base_repair_run_id: 28200925016
min_covered_to_save: 56
jobs/shards: 20
max-parallel: 20
expected wall time: about 5h50m per shard
```
