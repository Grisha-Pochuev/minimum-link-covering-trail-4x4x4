# START HERE — compact agent memory

Last updated: 2026-07-07

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
- threads/workers: `4`
- shards/jobs: `20`
- best ordered-trail candidate: `60/64` with `22` links

Best recorded GitHub ordered-trail candidate remains:

- candidate id: `mlct22-3cf45a2e21fe611c`
- source: `defect-relay-22-shard-7` in latest run, but same geometry as run `28618565146`
- mode in latest run: `window3_relay_from_official60`
- file: `runs/2026-07-03-smart-search-16-defect-relay-60-full/best_candidate.json`
- missing: `(0,0,1)`, `(0,2,3)`, `(0,3,1)`, `(2,1,1)`

Key lesson from run `28674416173`:

- numeric ordered-trail frontier stayed `60/64`;
- no `61/64` or `64/64` ordered-trail candidate;
- practical shard-best curves: `20`, all inferred `60/64`;
- reusable compact additions: `0`;
- all six defect-relay mode groups collapsed to the same four-hole wall;
- the run tested the `defect relay / multi-60-skeleton` hypothesis and showed that this exact setup does not create independent 60-family diversity.

Counting caution: `defect_relay_run_summary` reports `60` relay rows and `unique compact = 2`, but the summary builder scanned candidate JSON, relay JSONL, and missing-pattern metadata. This is not 60 independent curves and not two reusable compact curves.

Do not rerun `smart-search-16-defect-relay-60` with the same seed and modes as the next serious step.

## 4. Standard four-prompt workflow

Use the user's four-step rhythm:

1. result-taking prompt: read `START_HERE.md` once at the start of a new chat, record completed main/full GitHub run results, artifacts, candidates, frontier, and memory;
2. hypothesis prompt: think creatively, choose the next non-repeating hypothesis, and do any small local checks needed to make the idea launchable;
3. launch-preparation prompt: **technical only**. Take the already chosen hypothesis from prompt 2 and prepare the GitHub launch package so the user can press Run. Do not invent a new hypothesis, do not re-test the idea, and do not open a new research branch unless the requested launch is technically impossible;
4. wrap-up prompt: review the whole chat, identify confusion/time loss, and update memory files if needed.

Smoke-test is only a technical green-light before the long run. If the user sees a green check and launches the 5h+ full run, the next result-taking chat records the full run, not the smoke-test. Inspect smoke separately only if it failed, looked suspicious, or the user explicitly asks.

## 5. Prepared next launch package

Prepared workflow:

```text
workflow: smart-search-17-cover64-stitch-graph
workflow file: .github/workflows/smart-search-17-cover64-stitch-graph.yml
proposed workflow backup: docs/proposed-smart-search-17-cover64-stitch-graph.yml
plan file: docs/smart-search-17-cover64-stitch-graph-plan.md
engine: scripts/search_cover64_stitch_graph.py
checker: scripts/check_cover64_line_set.py
summary builder: scripts/build_cover64_stitch_summary.py
seed: data/search17/local_cover64_stitch_graph_seed.json
local line-set addition: candidates/line-set-additions-local-cover64-stitch-chat-20260704.jsonl
```

Hypothesis: `cover64 skeleton -> stitch graph -> ordered trail`.

Simple meaning: the web-chat preflight found that a nearby unordered set of 22 lines can cover all `64/64`; the hard part is stitching those lines into one ordered 22-link polygonal trail. So search-17 should stop repairing the same ordered `60/64` curve and instead optimize `64/64` line skeletons for stitchability.

Local preflight seed:

- `22` unordered lines;
- observed unordered coverage: `64/64`;
- no zero-length lines;
- stitch path lower bound around `18/22`;
- not a verified polygonal trail and not a proof.

Artifact names:

```text
shard artifacts: cover64-stitch-22-shard-*
summary artifact: cover64-stitch-run-summary
summary files:
  collected/cover64_stitch_run_summary.json
  collected/cover64_stitch_run_summary.md
  collected/cover64-stitch-candidates.jsonl
```

## 6. Launch inputs for smart-search-17

Smoke-test inputs:

```text
workflow: smart-search-17-cover64-stitch-graph
seconds: 180
workers: 4
seed: 20260717
min_covered_to_save: 64
min_stitch_path_to_save: 18
box_min: -1
box_max: 4
max_universe: 9000
max_lines: 22
latest_run_id: 28674416173
previous_frontier_run_id: 28618565146
```

Full-run inputs after green smoke:

```text
workflow: smart-search-17-cover64-stitch-graph
seconds: 21000
workers: 4
seed: 20260717
min_covered_to_save: 64
min_stitch_path_to_save: 18
box_min: -1
box_max: 4
max_universe: 9000
max_lines: 22
latest_run_id: 28674416173
previous_frontier_run_id: 28618565146
```

Expected useful result means either a `64/64` line-set scaffold with stitch path near `22/22`, or many different `64/64` scaffolds that show a new stitching landscape. It is still not a proof and not automatically a complete 22-link trail.
