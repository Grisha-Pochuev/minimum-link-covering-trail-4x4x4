# START HERE — compact agent memory

Last updated: 2026-07-02

This file is the first thing to read in a new ChatGPT web chat. It is the boot memory, not the full diary. Keep it short. Detailed history belongs in `frontier/latest.*`, `runs/*/summary.md`, plans, runbooks, and candidate banks.

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

Start from:

1. `START_HERE.md`
2. `frontier/latest.md`
3. `frontier/latest.json`
4. `docs/web-chat-runbook-prompts.md`
5. exact workflow or prepared workflow
6. matching plan doc
7. candidate bank/additions/originals
8. latest relevant `runs/` folder
9. GitHub Actions artifacts when analyzing a completed run

Use `frontier/latest.*` and run summaries as the index instead of blindly scanning every old run.

## 3. Current recorded frontier

Latest recorded completed full run:

- run id: `28522369532`
- workflow: `smart-search-14-rich-cover-stitch`
- status: `success`
- seconds: `21000` per shard
- threads: `4`
- shards/jobs: `20`
- best: `59/64` with `22` links

Best recorded GitHub candidate:

- candidate id: `mlct22-278a7d8dc1d65f25`
- source: `rich-cover-stitch-22-shard-0`
- mode: `new_skeleton_rich4`
- file: `runs/2026-07-01-smart-search-14-rich-cover-stitch-full/best_candidate.json`
- missing: `(1,2,2)`, `(2,0,2)`, `(2,0,3)`, `(3,1,2)`, `(3,1,3)`

Key lesson from run `28522369532`:

- numeric frontier stayed at `59/64`;
- no `60/64` or `64/64` candidate;
- raw shard-best curves: `20`, all `59/64`;
- exact representatives: `7`;
- new exact IDs vs recent recorded additions: `3`;
- rich-cover / stitch idea was active but still insufficient.

Do not rerun `smart-search-14-rich-cover-stitch` with the same seed and modes as the next serious step.

## 4. Standard four-prompt workflow

Use the user's four-step rhythm:

1. result-taking prompt: read `START_HERE.md`, record completed main/full GitHub run results, artifacts, candidates, frontier, and memory;
2. hypothesis prompt: compare recorded history, add any new outside/source file the user provides, make a non-repeating hypothesis, and run small local checks until the idea is launchable or rejected;
3. launch-preparation prompt: prepare files and exact GitHub inputs; smoke-test is a quick technical gate, not a separate scientific stage;
4. wrap-up prompt: review the whole chat, identify confusion/time loss, and update memory files.

Smoke-test is only a technical green-light before the long run. If the user sees a green check and launches the 5h+ full run, the next result-taking chat records the full run, not the smoke-test. Inspect smoke separately only if it failed, looked suspicious, or the user explicitly asks.

## 5. Current next direction

Recorded full run `28522369532` finished `smart-search-14-rich-cover-stitch`. It reduced collapse but still stayed at `59/64`. The next serious hypothesis should not be another same-seed smart-search-14 rerun.

Prepared next idea:

`rich-line transition / stitch-cost search around a local 60/64 skeleton`

Simple meaning: start from the local 22-link candidate that covers `60/64`, then search around its rich-line transition skeleton and pressure the four remaining holes.

Useful next full-run result means either `60/64+` with `links <= 22`, or clear data showing whether the blocker is rich-line ordering, weak bridge stitching, or the four-hole pressure around the local 60.

## 6. Prepared smart-search-15 launch

Prepared files:

- workflow: `.github/workflows/smart-search-15-rich-line-transition-60.yml`
- proposed workflow backup: `docs/proposed-smart-search-15-rich-line-transition-60.yml`
- plan: `docs/smart-search-15-rich-line-transition-60-plan.md`
- generator: `scripts/prepare_rich_line_transition_engine.py`
- local seed: `data/search15/local_60_candidate_cover_first_stitch_cost.json`
- local addition: `candidates/bank-additions-local-60-chat-20260702.jsonl`

2026-07-02 launch note: the ChatGPT GitHub connector blocked writing executable workflow files under `.github/workflows/`, so the user manually copied the prepared YAML. The first manual copy accidentally copied the markdown plan instead of YAML, causing run `28617578178` with no jobs. The corrected workflow must start with `name: smart-search-15-rich-line-transition-60`.

Current smoke-test:

- run id: `28618332477`
- run URL: https://github.com/Grisha-Pochuev/minimum-link-covering-trail-4x4x4/actions/runs/28618332477
- expected jobs: `check-known-23`, `check-local-60-seed`, `rich-line-transition-search (0..19)`, and aggregation
- observed early status: both controls passed, engine generation and compile started correctly in shard jobs

Important: the local `60/64` seed is not a recorded GitHub full-run result and not a proof. The recorded GitHub frontier stays `59/64` until a full GitHub run finishes and is recorded.

Local seed:

- candidate id: `mlct22-3cf45a2e21fe611c`
- links: `22`
- covered: `60/64`
- missing: `(0,0,1)`, `(0,2,3)`, `(0,3,1)`, `(2,1,1)`
- hypothesis: rich-line transition / stitch-cost search around a `60/64` skeleton.

Workflow rules:

- manual only: `workflow_dispatch`;
- no `push` trigger;
- smoke is a technical gate, not a new frontier;
- full run should use the same seed after green smoke;
- for full run after green smoke, change only `seconds` from `180` to `21000` unless the smoke reveals a problem.

Smoke-test inputs:

- workflow: `smart-search-15-rich-line-transition-60`
- seconds: `180`
- threads: `4`
- seed: `20260706`
- min_covered_to_save: `56`
- latest_run_id: `28522369532`
- previous_cover_stitch_run_id: `28460740781`
- previous_diversity_run_id: `28404861374`

Full-run inputs after green smoke:

- workflow: `smart-search-15-rich-line-transition-60`
- seconds: `21000`
- threads: `4`
- seed: `20260706`
- min_covered_to_save: `56`
- latest_run_id: `28522369532`
- previous_cover_stitch_run_id: `28460740781`
- previous_diversity_run_id: `28404861374`

## 7. Candidate memory rules

- `candidates/bank.jsonl`: compact reusable search memory; symmetry-deduplicated fuel.
- `candidates/bank-additions-*.jsonl`: run-level additions before/alongside merging.
- `candidates/originals/`: non-deduplicated scientific archive of real shard-best diversity.
- Normal save threshold: `covered_count >= 56 and links <= 22`.

After every completed full run: save champion, compact additions, original shard-best index if available, update `frontier/latest.*`, and update this file if the frontier or next step changed.

Latest saved additions:

- `candidates/bank-additions-run28522369532.jsonl`
- `candidates/originals/run28522369532-shard-bests-index.jsonl`
- `candidates/bank-additions-local-60-chat-20260702.jsonl`

## 8. Common traps

- Do not call partial candidates proofs.
- Do not confuse local preflight with evidence of a solution.
- Do not confuse a chat hypothesis or plan markdown file with an actual GitHub workflow YAML file.
- Do not treat old smart-search-14 as automatically worth rerunning.
- Do not read `candidates/bank.jsonl` alone; include recent bank-additions files.
- Do not spend a new chat analyzing green smoke unless asked.
- Do not record `check-and-short-search` push runs as full scientific runs.
- Do not record the local `60/64` seed as a GitHub frontier until a full GitHub run is completed and saved.
- If a workflow in `.github/workflows/` begins with `# ... plan`, it is wrong: copy raw YAML from `docs/proposed-*.yml`.

When unsure, prefer a small local check or a short documented smoke gate before a 20-job full run.
