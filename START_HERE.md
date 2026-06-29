# START HERE — project memory

Last updated: 2026-06-29

This is the first file to read when starting work in a new ChatGPT web chat.

The assistant may not remember enough from previous chats. Treat this repository as durable memory. Start here, then read the files listed below before analyzing a run or preparing a new one.

## What this project is

Repository: `Grisha-Pochuev/minimum-link-covering-trail-4x4x4`

Problem: find a shortest connected polygonal trail that covers all 64 points of the `4×4×4` grid `{0,1,2,3}^3`.

Working target: find a `22`-link trail covering `64/64` grid points, or understand the obstruction well enough to guide a proof or sharper search.

Known practical status:

- `23` links: known construction exists and is used as a control check.
- `22` links: open search target.
- `21` links: currently too hard for serious search; use only as diagnostic pressure unless the frontier changes.

Important caution: a search result is not a proof. A partial candidate is evidence, not a theorem.

## First reading order for a new chat

1. `START_HERE.md` — this file.
2. `frontier/latest.md` and `frontier/latest.json` — current frontier and latest useful run.
3. The exact workflow in `.github/workflows/` that launched the completed run. Do not substitute the newest workflow for an old run.
4. Planning docs and web-chat operating prompts.
5. `candidates/bank.jsonl`, `candidates/bank-additions-*.jsonl`, and `candidates/originals/`.
6. The latest relevant folder in `runs/`.
7. GitHub Actions artifacts of the latest useful runs.

Short invariant:

```text
START_HERE -> frontier -> relevant workflow -> plans -> bank/additions/originals -> runs/artifacts -> action
```

## Current frontier to remember

Latest useful completed full run:

```text
run id: 28338041580
workflow: smart-search-10-d-family-repair
status: success
seconds per shard: 21000
threads per shard: 4
shards/jobs: 20
best result: 59/64
links: 22
missing count: 5
```

Best recorded candidate:

```text
candidate id: mlct22-252fb1171852b9db
source artifact: d-family-22-shard-16
mode: repair56_target8
saved at: runs/2026-06-29-smart-search-10-d-family-repair-full/best_candidate.json
```

Missing points:

```text
(1, 0, 1)
(1, 2, 2)
(1, 3, 2)
(2, 0, 3)
(2, 2, 2)
```

Dominant recurring defect patterns from run `28338041580`:

```text
9/20: (1,0,1), (1,2,2), (1,3,2), (2,0,3), (2,2,2)
7/20: (1,0,1), (1,2,1), (1,3,2), (2,0,3), (2,2,2)
2/20: (0,2,2), (2,1,3), (2,2,3), (3,1,0), (3,1,2)
1/20: (0,2,2), (1,0,1), (1,3,2), (2,0,3), (2,2,2)
1/20: (1,2,2), (2,0,2), (2,0,3), (3,1,0), (3,1,2)
```

Observation: all 20 shard-best artifacts reached `59/64`, but none reached `60/64` or `64/64`. The numeric frontier did not improve. The obstruction moved away from old point `(2,0,2)` and into a new D2-style wall centered on `(1,0,1)`, `(1,3,2)`, `(2,0,3)`, and `(2,2,2)`.

Saved run memory:

```text
frontier/latest.md
frontier/latest.json
runs/2026-06-29-smart-search-10-d-family-repair-full/summary.md
runs/2026-06-29-smart-search-10-d-family-repair-full/best_candidate.json
runs/2026-06-29-smart-search-10-d-family-repair-full/mode_breakdown.json
candidates/bank-additions-run28338041580.jsonl
```

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

There is no automatic launch. The workflow is manual-only with `workflow_dispatch`; it has no push trigger.

Purpose:

```text
Attack the new D2 wall: (1,0,1), (1,3,2), (2,0,3), (2,2,2).
Variable fifth point: usually (1,2,2) or (1,2,1).
Guardrails: old A-family from run 28304497479 and old D-family from run 28327372242.
```

The local web-chat preflight after run `28338041580` tried simple recombination of existing shard-best material and did not beat `59/64`. Therefore the next workflow widens bridge windows and keeps more bridge candidates; it is not just a repeated `smart-search-10` seed rerun.

Smoke-test:

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

Full run after green smoke-test:

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

## Candidate-saving rules

`candidates/bank.jsonl` is the compact reusable search memory. It should be symmetry-deduplicated and used as fuel for future workflows.

`candidates/bank-additions-*.jsonl` stores compact run-level additions before or alongside merging into the bank.

`candidates/originals/` is the scientific archive of original, non-deduplicated trail candidates from completed runs. It is for analysis of real diversity, repeated patterns, mode behavior, and possible structural obstructions.

Normal eligibility threshold unless the workflow says otherwise:

```text
covered_count >= 56
links <= 22
```

Post-run rule: save champion, save compact additions, save original shard-best candidates when available, update `frontier/latest.*`, and update `START_HERE.md` if the frontier or next step changed.

## Flexible post-run reasoning loop

After a completed run, do not merely fill a template. Ask whether the numeric frontier improved, whether the defect family changed, whether many shards converged, whether compact memory gained useful representatives, whether any mode should be reduced, and whether the run suggests a possible obstruction rather than just more candidates.
