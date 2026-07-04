# START HERE — compact agent memory

Last updated: 2026-07-04

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

After this boot read, avoid reopening `START_HERE.md` during prompts 2-4 in the same chat. Use `frontier/latest.*` and run summaries as the index instead of blindly scanning every old run.

## 3. Current recorded frontier

Latest recorded completed full run:

- run id: `28674416173`
- run URL: https://github.com/Grisha-Pochuev/minimum-link-covering-trail-4x4x4/actions/runs/28674416173
- workflow: `smart-search-16-defect-relay-60`
- status: `success`
- seconds: `21000` per shard
- threads: `4`
- shards/jobs: `20`
- best: `60/64` with `22` links

Best recorded GitHub candidate remains:

- candidate id: `mlct22-3cf45a2e21fe611c`
- source: `defect-relay-22-shard-7` in latest run, but same geometry as run `28618565146`
- mode in latest run: `window3_relay_from_official60`
- file: `runs/2026-07-03-smart-search-16-defect-relay-60-full/best_candidate.json`
- missing: `(0,0,1)`, `(0,2,3)`, `(0,3,1)`, `(2,1,1)`

Key lesson from run `28674416173`:

- numeric frontier stayed `60/64`;
- no `61/64` or `64/64` candidate;
- practical shard-best curves: `20`, all inferred `60/64`;
- reusable compact additions: `0`;
- all six defect-relay mode groups collapsed to the same four-hole wall;
- the run tested the `defect relay / multi-60-skeleton` hypothesis and showed that this exact setup does not create independent 60-family diversity.

Counting caution: `defect_relay_run_summary` reports `60` relay rows and `unique compact = 2`, but the summary builder scanned candidate JSON, relay JSONL, and missing-pattern metadata. This is not 60 independent curves and not two reusable compact curves.

Do not rerun `smart-search-16-defect-relay-60` with the same seed and modes as the next serious step.

## 4. Standard four-prompt workflow

Use the user's four-step rhythm:

1. result-taking prompt: read `START_HERE.md` once at the start of a new chat, record completed main/full GitHub run results, artifacts, candidates, frontier, and memory;
2. hypothesis prompt: use the already-loaded context, add any new outside/source file the user provides, think broadly, make a non-repeating hypothesis, and run small local checks until the idea is launchable or rejected;
3. launch-preparation prompt: use the already-loaded context to prepare files and exact GitHub inputs; smoke-test is a quick technical gate, not a separate scientific stage;
4. wrap-up prompt: review the whole chat, identify confusion/time loss, and update memory files if needed.

Smoke-test is only a technical green-light before the long run. If the user sees a green check and launches the 5h+ full run, the next result-taking chat records the full run, not the smoke-test. Inspect smoke separately only if it failed, looked suspicious, or the user explicitly asks.

## 5. Latest smart-search-16 result

Completed run:

- run id: `28674416173`
- workflow: `smart-search-16-defect-relay-60`
- head SHA: `dd8414cdfe2d8c2a97e02a8223d87d69ead9a3c7`
- controls: known 23-link trail, official 60 seed, and local relay60 seed passed
- aggregation: `defect-relay-run-summary` produced successfully

Run artifacts:

- `defect-relay-run-summary`
- `defect-relay-22-shard-0` through `defect-relay-22-shard-19`

Mode layout, corrected to actual shards:

- `window2_relay_from_official60`: 7 shard-bests, all `60/64`
- `window3_relay_from_official60`: 4 shard-bests, all `60/64`
- `old59_to_relay60`: 3 shard-bests, all `60/64`
- `relay_then_push61`: 4 shard-bests, all `60/64`
- `integer_control`: 1 shard-best, `60/64`
- `old60_and_local_relay_control`: 1 shard-best, `60/64`

## 6. Current next step

Do not launch another identical relay run. Next useful work should be one of:

1. fix/narrow `scripts/build_defect_relay_summary.py` so it counts only real shard-best candidates and not metadata rows;
2. exact/local analysis around the old four-hole wall to learn why relay windows cannot escape;
3. a new skeleton-generation hypothesis that deliberately creates different 58-60 families before applying pressure to the four old holes.
