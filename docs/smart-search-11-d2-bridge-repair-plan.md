# smart-search-11-d2-bridge-repair plan

Prepared after local web-chat preflight following run `28338041580`.

The numeric frontier is still `59/64` with 22 links. The goal is not to repeat `smart-search-10-d-family-repair`; that workflow saturated at `59/64` and moved the obstruction into a new D2-style wall.

## Main target

New D2 wall from run `28338041580`:

```text
dominant 9/20: (1,0,1), (1,2,2), (1,3,2), (2,0,3), (2,2,2)
secondary 7/20: (1,0,1), (1,2,1), (1,3,2), (2,0,3), (2,2,2)
```

Core target:

```text
(1,0,1), (1,3,2), (2,0,3), (2,2,2)
```

Variable fifth point:

```text
(1,2,2) or (1,2,1)
```

Guardrails:

```text
old D-family from 28327372242:
(1,2,2), (1,3,1), (1,3,2), (2,0,2), (2,0,3)

old A-family from 28304497479:
(0,2,2), (2,1,3), (2,2,3), (3,1,0), (3,1,2)
```

## Local preflight conclusion

The web-chat local check tried simple recombination of already found shard-best material after run `28338041580`. It did not find `60/64` or `64/64`; it stayed at `59/64`.

Interpretation: the next workflow must create new local bridge material around the D2 wall. It should not merely rerun the same D-family repair with another seed.

## Seed sources

The workflow starts from saved memory rather than zero:

- artifacts from latest D2 run `28338041580`;
- artifacts from previous D-family run `28327372242`;
- artifacts from A/orbit guardrail run `28304497479`;
- artifacts from `28292425390`, `28275850889`, `28275666411`, and `28200925016`;
- `runs/2026-06-29-smart-search-10-d-family-repair-full/`;
- `runs/2026-06-28-smart-search-9-new-defect-repair-full/`;
- `runs/2026-06-28-smart-search-8-orbit-bridge-full/`;
- `runs/2026-06-27-smart-search-7-core5-full/`;
- `runs/2026-06-27-smart-search-6-defect-full/`;
- `runs/2026-06-27-smart-search-6-defect-smoke/`;
- `runs/2026-06-26-repair-search-5/`;
- `experiments/2026-06-25-repair57-local-smoke/`;
- `candidates/bank.jsonl`;
- `candidates/bank-additions-run28338041580.jsonl`;
- `candidates/bank-additions-run28327372242.jsonl`;
- `candidates/bank-additions-run28304497479.jsonl`;
- `candidates/bank-additions-run28292425390.jsonl`.

## Prepared files

Workflow:

```text
.github/workflows/smart-search-11-d2-bridge-repair.yml
```

Engine generator:

```text
scripts/prepare_d2_bridge_repair_engine.py
```

The workflow is manual-only with `workflow_dispatch`. There is no `push` trigger.

## What changed from smart-search-10

`smart-search-11` targets the new D2 wall, not the old D-family wall.

Changes include:

- latest run `28338041580` is now the main artifact seed;
- point weights are centered on `(1,0,1)`, `(1,3,2)`, `(2,0,3)`, and `(2,2,2)`;
- old D/A families are guardrails rather than the main objective;
- bridge windows are widened because the local check showed short swaps did not beat `59/64`;
- more outgoing bridge candidates are kept per step;
- subcube stitching is allowed to use fractional bridge vertices;
- shard budget is shifted toward D2 repair and bridge creation.

## Smoke-test

Use this first:

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

The smoke-test is mainly for safety: artifact download, candidate-bank export, C++ generation, compilation, checker, artifact upload, and aggregation should all pass.

## Full run after smoke passes

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

## What would count as progress

A breakthrough is `60/64` or `64/64`.

A still-useful non-breakthrough is another `59/64` that covers at least one of `(1,0,1)` and `(2,2,2)` without reopening `(2,0,2)` or falling back into the old A-family holes.
