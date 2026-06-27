# Current search frontier

This file is the human-readable working memory of the project.

Status: `smart-search-8-orbit-bridge` prepared after `smart-search-7-core5` full run analysis.

Latest useful completed run:

- Repository: `Grisha-Pochuev/minimum-link-covering-trail-4x4x4`
- Final run id: `28292425390`
- Run URL: https://github.com/Grisha-Pochuev/minimum-link-covering-trail-4x4x4/actions/runs/28292425390
- Workflow: `smart-search-7-core5`
- Commit SHA of the run: `b29af6a4af45fa62c531384587377b36c650c832`
- Status: `success`
- Duration: full run, `21000` seconds per shard
- Result type: heuristic search, not a proof
- Artifacts: `core5-run-summary`, `core5-22-shard-*`, `core5-seed-manifest-*`

## Parameters of latest completed run

- seconds: `21000`
- threads: `4` per shard
- shards/jobs: `20`
- max parallel jobs: `20`
- seed: `20260628`
- prior run id: `28275850889`
- secondary run id: `28275666411`
- base repair run id: `28200925016`
- coordinate scale: `2`
- min covered to save: `56`
- checker: `scripts/check_scaled_trail.py`

## Best GitHub Actions result

Best known result after run `28292425390`:

- covered_count: `59 / 64`
- coverage percent: `92.1875%`
- links: `22`
- links target: `22`
- selected mode: `subcube_stitch22`
- source artifact: `core5-22-shard-15`
- source shard: `15`
- candidate id: `mlct22-a584fa7e488e0279`
- status: `partial_candidate`
- missing count: `5`
- missing:
  - `(0, 1, 0)`
  - `(1, 2, 3)`
  - `(2, 1, 0)`
  - `(3, 1, 1)`
  - `(3, 1, 3)`

The best candidate is still partial. It has exactly 22 links and covers 59 of the 64 grid points. This is not a complete covering trail and not a proof.

The exact selected best candidate is saved in:

```text
runs/2026-06-27-smart-search-7-core5-full/best_candidate.json
```

A reusable copy is saved in:

```text
candidates/mlct22-a584fa7e488e0279-run28292425390.json
```

A run summary is saved in:

```text
runs/2026-06-27-smart-search-7-core5-full/summary.md
```

The 6 unique eligible additions from this run are saved safely in:

```text
candidates/bank-additions-run28292425390.jsonl
candidates/bank-additions-run28292425390.summary.json
```

## Candidate preservation rule

The workflow threshold was:

```text
covered_count >= 56
links <= 22
```

All 20 shard-best candidates met this threshold. They all had `59/64` coverage and 22 links. Symmetry-aware deduplication reduced them to 6 unique candidates. The 20 original concrete shard results remain available as `core5-22-shard-*` artifacts from run `28292425390` and are used by the next workflow through downloaded artifact folders.

## Top recurring missing points from run 28292425390

Counted over the 20 shard-best JSON result files:

- `(3, 1, 3)`: 17 / 20
- `(3, 1, 0)`: 16 / 20
- `(2, 1, 2)`: 14 / 20
- `(2, 2, 3)`: 14 / 20
- `(1, 2, 1)`: 13 / 20
- `(0, 1, 0)`: 4 / 20
- `(1, 2, 3)`: 4 / 20
- `(2, 1, 0)`: 4 / 20
- `(3, 1, 1)`: 4 / 20
- `(3, 1, 2)`: 3 / 20
- `(1, 2, 2)`: 2 / 20
- `(2, 0, 2)`: 2 / 20
- `(2, 0, 3)`: 2 / 20
- `(0, 2, 2)`: 1 / 20

## Dominant missing patterns

Across the 20 shard-best results:

- 13 / 20: `(1,2,1), (2,1,2), (2,2,3), (3,1,0), (3,1,3)`
- 4 / 20: `(0,1,0), (1,2,3), (2,1,0), (3,1,1), (3,1,3)`
- 2 / 20: `(1,2,2), (2,0,2), (2,0,3), (3,1,0), (3,1,2)`
- 1 / 20: `(0,2,2), (2,1,2), (2,2,3), (3,1,0), (3,1,2)`

The selected best candidate is the second dominant pattern. It covers the old selected-best hard points `(1,2,2)`, `(2,0,2)`, `(2,0,3)`, and `(3,1,2)`, but it creates a different 5-point defect set around `(0,1,0)`, `(1,2,3)`, `(2,1,0)`, `(3,1,1)`, `(3,1,3)`.

## Which modes worked best in run 28292425390

All modes represented in shard-best results reached `59/64`:

- `fractional_bridge22`: 6 result(s), best `59/64`, average `59.00/64`, shards `[6, 7, 8, 9, 10, 11]`
- `integer_control22`: 1 result(s), best `59/64`, average `59.00/64`, shard `[19]`
- `repair56_target8`: 2 result(s), best `59/64`, average `59.00/64`, shards `[16, 17]`
- `rich_segment_catalog`: 1 result(s), best `59/64`, average `59.00/64`, shard `[18]`
- `subcube_stitch22`: 4 result(s), best `59/64`, average `59.00/64`, shards `[12, 13, 14, 15]`
- `transition_penalty22`: 6 result(s), best `59/64`, average `59.00/64`, shards `[0, 1, 2, 3, 4, 5]`

The conclusion is similar to the previous full run: the C++ repair direction reliably reaches `59/64`, but the current search shape still saturates there.

## Comparison with previous runs

- Run `28103660449` / smart-search-4: best `56/64`, 8 missing points.
- Local prelaunch repair smoke: best `57/64`, 7 missing points.
- Run `28200925016` / repair-search-5: best `58/64`, 6 missing points.
- Run `28275666411` / smart-search-6-defect smoke-test: best `59/64`, 5 missing points.
- Run `28275850889` / smart-search-6-defect full run: best `59/64`, old 5-point defect core.
- Run `28292425390` / smart-search-7-core5 full run: best `59/64`, new 5-point defect orbit.

So run `28292425390` did not raise the numeric frontier, but it expanded the `59/64` evidence from one main defect core to several useful defect orbits.

## Prepared next run

Prepared workflow:

```text
smart-search-8-orbit-bridge
.github/workflows/smart-search-8-orbit-bridge.yml
```

Supporting files:

```text
scripts/prepare_orbit_bridge_engine.py
docs/smart-search-8-orbit-bridge-plan.md
```

Prepared next focus:

```text
smart-search-8-orbit-bridge: compare and bridge distinct 59/64 defect orbits, then use targeted local surgery around the shared hard region near (3,1,3) and the x=3,y=1 transition zone.
```

## What became clear for the next run

- No complete `64/64` candidate was found.
- No `60/64` candidate was found.
- The current `core5` recipe should not simply be repeated unchanged.
- The next useful target is the relationship between distinct `59/64` defect orbits.
- The only point shared by the old selected best and the new selected best is `(3,1,3)`, so it deserves special attention.
- The next search should try to bridge the old and new 59/64 candidates: keep the points each orbit covers well and repair the transition around the `x=3,y=1` region.

## Next run seed source

The next serious run should start from:

- GitHub Actions artifacts of run `28292425390`;
- `core5-run-summary` from this run;
- all `core5-22-shard-*` artifacts from this run;
- GitHub Actions artifacts of runs `28275850889`, `28275666411`, and `28200925016`;
- `runs/2026-06-27-smart-search-7-core5-full/best_candidate.json`;
- `candidates/mlct22-a584fa7e488e0279-run28292425390.json`;
- `candidates/bank-additions-run28292425390.jsonl`;
- older `59/64` bank candidates from run `28275850889`;
- `candidates/bank.jsonl` as broad seed memory.

## Smoke-test launch parameters

```text
workflow: smart-search-8-orbit-bridge
seconds: 180
threads: 4
seed: 20260629
prior_run_id: 28292425390
old_59_run_id: 28275850889
secondary_run_id: 28275666411
base_repair_run_id: 28200925016
min_covered_to_save: 56
jobs/shards: 20
max-parallel: 20
```

## Full serious-run launch parameters

```text
workflow: smart-search-8-orbit-bridge
seconds: 21000
threads: 4
seed: 20260629
prior_run_id: 28292425390
old_59_run_id: 28275850889
secondary_run_id: 28275666411
base_repair_run_id: 28200925016
min_covered_to_save: 56
jobs/shards: 20
max-parallel: 20
expected wall time: about 5h50m per shard
```
