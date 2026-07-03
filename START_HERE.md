# START HERE — compact agent memory

Last updated: 2026-07-03

This file is the first thing to read in a new ChatGPT web chat. It is the boot memory, not the full diary. Read it once at the beginning of the working chat, normally in prompt 1. Do not reopen it in prompts 2-4 unless the user says this is a new chat, memory was lost, or critical context is missing. Detailed history belongs in `frontier/latest.*`, `runs/*/summary.md`, plans, runbooks, and candidate banks.

## 1. Project

Repository: `Grisha-Pochuev/minimum-link-covering-trail-4x4x4`

Problem: find a shortest connected polygonal trail covering all 64 points of the `4×4×4` grid `{0,1,2,3}^3`.

Current target: a `22`-link trail covering `64/64`, or enough obstruction evidence to guide a proof/search.

Known practical status:

- `23` links: known construction; used as control.
- `22` links: open target.
- `21` links: too hard for serious search now; use only as diagnostic pressure.

Important: heuristic search results are evidence, not proof.

## 2. First reading order

At the beginning of a new working chat, start from:

1. `START_HERE.md`
2. `frontier/latest.md`
3. `frontier/latest.json`
4. `docs/web-chat-runbook-prompts.md`
5. exact workflow or prepared workflow
6. matching plan doc
7. candidate bank/additions/originals
8. latest relevant `runs/` folder
9. GitHub Actions artifacts when analyzing a completed run

After this boot read, avoid reopening `START_HERE.md` during prompts 2-4 in the same chat. Use the already-loaded context and the smaller targeted files.

Use `frontier/latest.*` and run summaries as the index instead of blindly scanning every old run.

## 3. Current recorded frontier

Latest recorded completed full run:

- run id: `28618565146`
- workflow: `smart-search-15-rich-line-transition-60`
- status: `success`
- seconds: `21000` per shard
- threads: `4`
- shards/jobs: `20`
- best: `60/64` with `22` links

Best recorded GitHub candidate:

- candidate id: `mlct22-3cf45a2e21fe611c`
- source: `rich-line-transition-22-shard-18`
- mode: `integer_line_control`
- file: `runs/2026-07-03-smart-search-15-rich-line-transition-60-full/best_candidate.json`
- missing: `(0,0,1)`, `(0,2,3)`, `(0,3,1)`, `(2,1,1)`

Key lesson from run `28618565146`:

- numeric GitHub frontier improved from `59/64` to `60/64`;
- no `61/64` or `64/64` candidate;
- raw shard-best curves: `20`, all `60/64`;
- compact representatives: `1`;
- all six modes collapsed to the same four-hole wall;
- the run confirms the local `60/64` seed as a full GitHub Actions result but does not create independent 60-family diversity.

Do not rerun `smart-search-15-rich-line-transition-60` with the same seed and modes as the next serious step.

## 4. Standard four-prompt workflow

Use the user's four-step rhythm:

1. result-taking prompt: read `START_HERE.md` once at the start of a new chat, record completed main/full GitHub run results, artifacts, candidates, frontier, and memory;
2. hypothesis prompt: use the already-loaded context, add any new outside/source file the user provides, think broadly, make a non-repeating hypothesis, and run small local checks until the idea is launchable or rejected;
3. launch-preparation prompt: use the already-loaded context to prepare files and exact GitHub inputs; smoke-test is a quick technical gate, not a separate scientific stage;
4. wrap-up prompt: review the whole chat, identify confusion/time loss, and update memory files if needed.

Smoke-test is only a technical green-light before the long run. If the user sees a green check and launches the 5h+ full run, the next result-taking chat records the full run, not the smoke-test. Inspect smoke separately only if it failed, looked suspicious, or the user explicitly asks.

## 5. Current prepared launch package

Prepared next workflow:

```text
workflow: smart-search-16-defect-relay-60
workflow file: .github/workflows/smart-search-16-defect-relay-60.yml
proposed workflow backup: docs/proposed-smart-search-16-defect-relay-60.yml
plan file: docs/smart-search-16-defect-relay-60-plan.md
generator: scripts/prepare_defect_relay_engine.py
summary builder: scripts/build_defect_relay_summary.py
```

Seed and bank files:

```text
data/search16/official_60_seed_run28618565146.json
data/search16/local_relay60_window2_seed.json
data/search16/old59_seed_bank_run28522369532.jsonl
candidates/bank-additions-local-relay60-chat-20260703.jsonl
```

Hypothesis: `defect relay / multi-60-skeleton`.

Simple meaning: the last run gave one official `60/64` object but no diversity. The next run should first create several genuinely different `60/64` skeletons with different missing sets, then try to push them to `61/64+`.

Local check behind the package: a two-vertex window replacement changed the end window from `[2,6,6] -> [6,2,6] -> [6,2,2] -> [6,8,2]` to `[2,6,6] -> [0,6,2] -> [6,0,2] -> [6,8,2]`. This preserved `60/64` but changed the missing set from `(0,0,1), (0,2,3), (0,3,1), (2,1,1)` to `(0,0,1), (0,2,3), (2,2,3), (3,1,2)`. It is search fuel, not proof.

## 6. Launch inputs for smart-search-16

Smoke-test inputs:

```text
workflow: smart-search-16-defect-relay-60
seconds: 180
threads: 4
seed: 20260716
min_covered_to_save: 56
min_relay_covered_to_save: 60
latest_run_id: 28618565146
previous_frontier_run_id: 28522369532
previous_cover_stitch_run_id: 28460740781
previous_diversity_run_id: 28404861374
max_links: 22
```

Full-run inputs after green smoke:

```text
workflow: smart-search-16-defect-relay-60
seconds: 21000
threads: 4
seed: 20260716
min_covered_to_save: 56
min_relay_covered_to_save: 60
latest_run_id: 28618565146
previous_frontier_run_id: 28522369532
previous_cover_stitch_run_id: 28460740781
previous_diversity_run_id: 28404861374
max_links: 22
```

Expected useful result means either `61/64+` with `links <= 22`, or clear structural progress: at least several unique compact `60/64` representatives and several different missing sets.

## 7. Latest smart-search-15 result

Completed run:

- run id: `28618565146`
- run URL: https://github.com/Grisha-Pochuev/minimum-link-covering-trail-4x4x4/actions/runs/28618565146
- workflow: `smart-search-15-rich-line-transition-60`
- head SHA: `e82bff68d5fde1ae86a19176c3310e81f4c9b8b3`
- controls: `check-known-23` passed, `check-local-60-seed` passed
- aggregation: `rich-line-transition-run-summary` produced successfully

Run artifacts:

- `rich-line-transition-run-summary`
- `rich-line-transition-22-shard-0` through `rich-line-transition-22-shard-19`

Mode layout observed:

- `local60_lns`: 5 shard-bests, all `60/64`
- `rich_line_transition`: 4 shard-bests, all `60/64`
- `missing4_pressure`: 6 shard-bests, all `60/64`
- `weak_bridge_surgery`: 3 shard-bests, all `60/64`
- `integer_line_control`: 1 shard-best, `60/64`
- `old59_vs_60_control`: 1 shard-best, `60/64`

All 20 shard-best records have the same missing set: `(0,0,1)`, `(0,2,3)`, `(0,3,1)`, `(2,1,1)`.

## 8. Candidate memory rules

- `candidates/bank.jsonl`: compact reusable search memory; symmetry-deduplicated fuel.
- `candidates/bank-additions-*.jsonl`: compact reusable additions before/alongside merging.
- `runs/<date>-<workflow>/shard_bests.jsonl`: run-level additions and full run context.
- `candidates/originals/`: non-deduplicated scientific archive of real shard-best diversity.
- Normal save threshold: `covered_count >= 56 and links <= 22`.

After every completed full run: save champion, compact additions, original shard-best index/full originals if available, update `frontier/latest.*`, and update this file if the frontier or next step changed.

Latest saved additions:

- `candidates/bank-additions-local-relay60-chat-20260703.jsonl`
- `candidates/bank-additions-run28618565146.jsonl`
- `candidates/originals/run28618565146-shard-bests-index.jsonl`
- `candidates/originals/run28618565146-shard-bests.jsonl`
- `candidates/bank-additions-run28522369532.jsonl`
- `candidates/originals/run28522369532-shard-bests-index.jsonl`
- `candidates/bank-additions-local-60-chat-20260702.jsonl`

## 9. Common traps

- Do not call partial candidates proofs.
- Do not confuse local preflight with evidence of a solution.
- Do not confuse a chat hypothesis or plan markdown file with an actual GitHub workflow YAML file.
- Do not treat old smart-search-14 as automatically worth rerunning.
- Do not rerun smart-search-15 with the same seed/modes just to reconfirm the 60 seed.
- Do not read `candidates/bank.jsonl` alone; include recent bank-additions files.
- Do not spend a new chat analyzing green smoke unless asked.
- Do not record `check-and-short-search` push runs as full scientific runs.
- Do not record a local seed as a GitHub frontier until a full GitHub run is completed and saved.
- If a workflow in `.github/workflows/` begins with `# ... plan`, it is wrong: copy raw YAML from `docs/proposed-*.yml`.
- For the prepared smart-search-16 package, verify that the workflow starts with `name: smart-search-16-defect-relay-60` and uses only `workflow_dispatch`.
- In prompts 2-4 of the same chat, do not reopen `START_HERE.md` just to reread it; update it only if memory needs to change.

When unsure, prefer a small local check or a short documented smoke gate before a 20-job full run.
