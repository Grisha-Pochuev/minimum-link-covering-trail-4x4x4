# smart-search-9-new-defect-repair plan

This is the next prepared smart search after the completed `smart-search-8-orbit-bridge` run `28304497479`.

The numeric frontier is still `59/64` with 22 links. The point is not to repeat smart-search-8 unchanged. That run mostly closed the old hard point `(3,1,3)` but exposed new A/B defect families.

## Main target

Repair the new dominant defects from run `28304497479`:

```text
Pattern A, 11/20: (0,2,2), (2,1,3), (2,2,3), (3,1,0), (3,1,2)
Pattern B, 7/20:  (1,0,1), (1,2,2), (1,3,2), (2,0,3), (2,2,2)
Pattern C, 2/20:  (1,2,1), (2,1,2), (2,2,3), (3,1,0), (3,1,3)
```

The highest-pressure points are `(2,2,3)` and `(3,1,0)`, each seen in `13/20` shard-best candidates. `(3,1,3)` remains only as a control point because smart-search-8 reduced it to `2/20`.

## Seed sources

The workflow starts from saved memory rather than zero:

- GitHub Actions artifacts from run `28304497479`, especially `orbit-bridge-22-shard-*`;
- artifacts from `28292425390`, `28275850889`, `28275666411`, and `28200925016`;
- `runs/2026-06-28-smart-search-8-orbit-bridge-full/`;
- `runs/2026-06-27-smart-search-7-core5-full/`;
- `runs/2026-06-27-smart-search-6-defect-full/`;
- `runs/2026-06-27-smart-search-6-defect-smoke/`;
- `runs/2026-06-26-repair-search-5/`;
- `candidates/bank.jsonl`;
- `candidates/bank-additions-run28304497479.jsonl`;
- `candidates/bank-additions-run28292425390.jsonl`.

## Workflow

Prepared workflow:

```text
.github/workflows/smart-search-9-new-defect-repair.yml
```

It is manual-only with `workflow_dispatch`. There is no `push` trigger.

## Smoke-test

Use this first:

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

The smoke-test is mainly for safety: artifact download, candidate-bank export, C++ generation, compilation, checker, artifact upload, and aggregation should all pass.

## Full run after smoke passes

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

## What would count as progress

A clear breakthrough is `60/64` or `64/64`. But even another `59/64` can be useful if it produces a new defect family that covers at least one of the current A/B pressure points without simply recreating an old missing set.
