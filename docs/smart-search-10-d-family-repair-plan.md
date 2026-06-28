# smart-search-10-d-family-repair plan

This is the next prepared smart search after the completed `smart-search-9-new-defect-repair` run `28327372242`.

The numeric frontier is still `59/64` with 22 links. The point is not to repeat smart-search-9 unchanged. That run mostly moved the obstruction into a new D-family.

## Main target

Repair the dominant D-family defects from run `28327372242`:

```text
D-family, 12/20: (1,2,2), (1,3,1), (1,3,2), (2,0,2), (2,0,3)
A-family guard, 4/20: (0,2,2), (2,1,3), (2,2,3), (3,1,0), (3,1,2)
E-family, 3/20: (0,0,2), (1,2,3), (2,0,1), (2,1,0), (3,1,1)
Control, 1/20: (1,3,1), (2,1,2), (2,2,3), (3,1,0), (3,1,3)
```

The highest-pressure points are `(1,3,1)`, `(1,2,2)`, `(1,3,2)`, `(2,0,2)`, and `(2,0,3)`. The old A-family is kept as a guardrail so the search does not merely rotate back to the previous obstruction.

## Seed sources

The workflow starts from saved memory rather than zero:

- GitHub Actions artifacts from run `28327372242`, especially `new-defect-22-shard-*`;
- artifacts from `28304497479`, `28292425390`, `28275850889`, `28275666411`, and `28200925016`;
- `runs/2026-06-28-smart-search-9-new-defect-repair-full/`;
- `runs/2026-06-28-smart-search-8-orbit-bridge-full/`;
- `runs/2026-06-27-smart-search-7-core5-full/`;
- `runs/2026-06-27-smart-search-6-defect-full/`;
- `runs/2026-06-27-smart-search-6-defect-smoke/`;
- `runs/2026-06-26-repair-search-5/`;
- `candidates/bank.jsonl`;
- `candidates/bank-additions-run28327372242.jsonl`;
- `candidates/bank-additions-run28304497479.jsonl`;
- `candidates/bank-additions-run28292425390.jsonl`.

## Workflow

Prepared workflow:

```text
.github/workflows/smart-search-10-d-family-repair.yml
```

It is manual-only with `workflow_dispatch`. There is no `push` trigger.

Prepared generator:

```text
scripts/prepare_d_family_repair_engine.py
```

## Smoke-test

Use this first:

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

The smoke-test is mainly for safety: artifact download, candidate-bank export, C++ generation, compilation, checker, artifact upload, and aggregation should all pass.

## Full run after smoke passes

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

## What would count as progress

A clear breakthrough is `60/64` or `64/64`. But even another `59/64` can be useful if it produces a new defect family that closes at least one D-family point without simply recreating the A-family missing set.
