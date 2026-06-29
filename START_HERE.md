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
candidates/bank-additions-run28378489636.jsonl
candidates/originals/run-28378489636-smart-search-11-d2-bridge-repair.jsonl
```

## Current next step

The next step is not to launch a new run immediately.

First do a hypothesis step: compare the new `16` compact representatives against old A/D/D2 families and decide whether the project should continue D2 bridge repair, design a small diagnostic around `(2,1,2)/(2,2,3)`, or switch to a broader new-skeleton search.

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
