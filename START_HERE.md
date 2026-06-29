# START HERE — project memory

Last updated: 2026-06-30

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
3. `docs/web-chat-runbook-prompts.md` — optimized web-chat prompts and launch checklist.
4. The exact workflow in `.github/workflows/` that launched the completed run. Do not substitute the newest workflow for an old run.
5. Planning docs for the prepared or completed workflow.
6. `candidates/bank.jsonl`, `candidates/bank-additions-*.jsonl`, and `candidates/originals/`.
7. The latest relevant folder in `runs/`.
8. GitHub Actions artifacts of the latest useful runs.

Short invariant:

```text
START_HERE -> frontier -> web-chat runbook -> relevant workflow -> plan -> bank/additions/originals -> runs/artifacts -> action
```

Web-chat optimization rule:

```text
Do not rescan everything blindly. Use frontier/latest.* and saved run summaries as the index, then inspect only the relevant exact workflow, run folder, candidate additions, originals, and artifacts. Do not promise to check a run later; either check it now from available GitHub data or say what the user must do manually.
```

## Current frontier to remember

Latest useful completed full run:

```text
run id: 28378489636
workflow: smart-search-11-d2-bridge-repair
status: success
seconds per shard: 21000
threads per shard: 4
shards/jobs: 20
best result: 59/64
links: 22
missing count: 5
```

Best recorded candidate from the latest run:

```text
candidate id: mlct22-a77764189bd3e13a
source artifact: d2-bridge-22-shard-0
mode: repair56_target8
saved at: runs/2026-06-29-smart-search-11-d2-bridge-repair-full/best_candidate.json
```

Missing points:

```text
(0, 2, 2)
(2, 1, 2)
(2, 2, 3)
(3, 1, 0)
(3, 1, 2)
```

Observation: all 20 shard-best artifacts reached `59/64`, but none reached `60/64` or `64/64`. The numeric frontier did not improve over run `28338041580`. The useful change is diversity: run `28338041580` produced `7` compact representatives, while run `28378489636` produced `16` compact representatives. The new common defect wall is centered on `(2,1,2)` and `(2,2,3)`, each appearing in `16 / 20` shard-best candidates.

Saved run memory:

```text
frontier/latest.md
frontier/latest.json
runs/2026-06-29-smart-search-11-d2-bridge-repair-full/summary.md
runs/2026-06-29-smart-search-11-d2-bridge-repair-full/best_candidate.json
runs/2026-06-29-smart-search-11-d2-bridge-repair-full/mode_breakdown.json
runs/2026-06-29-smart-search-11-d2-bridge-repair-full/compact_representatives.md
```

Note: `candidates/bank.jsonl` was inspected for comparison, but it was not merged in this step. The next hypothesis step should decide whether the 16 compact representatives are useful enough to formalize as `bank-additions` for future search seeding.

## Prepared next workflow

A broader follow-up workflow now exists:

```text
.github/workflows/smart-search-12-skeleton-diversity.yml
scripts/prepare_skeleton_diversity_engine.py
docs/smart-search-12-skeleton-diversity-plan.md
```

Purpose: do not simply repeat D2 bridge repair. The working hypothesis is that repeated `59/64` runs are hitting a skeleton-level obstruction: local repair moves the five missing points but does not remove the five-hole wall. The next run should search for different 22-link skeletons and better transitions between rich segments.

Shard split in the prepared workflow:

```text
0-5   fresh_rich_skeleton
6-9   transition_graph22
10-13 diversity_repair22
14-16 anti_wall22
17    cross_family22
18    integer_control22
19    d2_control22
```

Suggested launch order from web chat:

```text
First smoke-test:
seconds=180
threads=4
seed=20260703
latest_run_id=28378489636
latest_d2_run_id=28338041580
prior_d_run_id=28327372242
orbit_bridge_run_id=28304497479
previous_core5_run_id=28292425390
old_59_run_id=28275850889
secondary_run_id=28275666411
base_repair_run_id=28200925016
min_covered_to_save=56

If smoke is green, full run:
seconds=21000
threads=4
same run ids and seed unless there is a reason to change seed
```

Important: the workflow is `workflow_dispatch` only. Do not add a push trigger for these expensive runs.

## Current next step

Run a short smoke-test of `smart-search-12-skeleton-diversity` from the GitHub Actions UI. If it compiles, downloads artifacts, runs shards, and uploads a summary, then launch the full `21000` second run. After completion, analyze both numeric frontier and structural diversity: a new `59/64` family with different missing points can still be useful.

## Lessons from the 2026-06-30 web-chat process

Do not confuse a plan with a repository change. In this chat, the workflow was first described before it actually existed, and the user correctly noticed that it was not visible in GitHub. Future assistants must create the file, fetch it back, and only then say it exists.

When preparing expensive GitHub runs from web chat:

```text
1. Read START_HERE.md first.
2. Read docs/web-chat-runbook-prompts.md.
3. Read the workflow and plan file from GitHub, not from memory.
4. Verify workflow_dispatch-only and no push trigger.
5. Verify generator path, compile command, checker command, artifact names, and aggregation.
6. If the connector lacks workflow_dispatch, do not claim the run was launched; give exact GitHub UI steps.
7. After changing files, fetch them back from GitHub and update START_HERE.md.
```

The current web-chat connector could create and update files but did not expose a workflow-dispatch action. Therefore smoke/full runs may need manual UI launch unless a future tool explicitly provides dispatch.

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
