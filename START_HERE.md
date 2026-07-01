# START HERE — compact agent memory

Last updated: 2026-07-01

This file is the first thing to read in a new ChatGPT web chat. It is the boot memory, not the full diary. Keep it short. Detailed history belongs in `frontier/latest.*`, `runs/*/summary.md`, plans, and candidate banks.

## 1. Project

Repository: `Grisha-Pochuev/minimum-link-covering-trail-4x4x4`

Problem: find a shortest connected polygonal trail covering all 64 points of the `4×4×4` grid `{0,1,2,3}^3`.

Current target: a `22`-link trail covering `64/64`, or enough obstruction evidence to guide a proof/search.

Practical status:

```text
23 links: known construction; used as control
22 links: open target
21 links: too hard for serious search now; use only as diagnostic pressure
```

Important: heuristic search results are evidence, not proof.

## 2. First reading order

Always start here, then read only what the task needs:

```text
START_HERE.md
frontier/latest.md
frontier/latest.json
docs/web-chat-runbook-prompts.md
exact workflow or prepared workflow
matching plan doc
candidate bank/additions/originals
latest relevant runs/ folder
GitHub Actions artifacts if analyzing a completed run
```

Do not blindly scan every old run. Use `frontier/latest.*` and run summaries as the index.

## 3. Current recorded frontier

Latest recorded completed full run:

```text
run id: 28460740781
workflow: smart-search-13-cover-stitch-cache
status: success
seconds: 21000 per shard
threads: 4
shards/jobs: 20
best: 59/64 with 22 links
```

Best recorded candidate:

```text
candidate id: mlct22-1c8736b46b59a730
source: cover-stitch-cache-22-shard-6
mode: stitch_with_transposition
file: runs/2026-06-30-smart-search-13-cover-stitch-cache-full/best_candidate.json
missing: (0,1,2), (1,2,1), (1,3,2), (2,1,3), (2,2,2)
```

Key lesson from run `28460740781`:

```text
numeric frontier: unchanged at 59/64
no 60/64 or 64/64 candidate
raw shard-best curves: 20, all 59/64
exact representatives: 5
new exact IDs vs run 28404861374 additions: 4
dominant missing family: 14/20
cache/anti-wall: active but insufficient
```

Do not rerun `smart-search-13-cover-stitch-cache` with the same seed/modes as the next serious step.

## 4. Standard four-prompt workflow

Use the user's four-step rhythm. Do not add a fifth mandatory smoke-test result step.

```text
1. Result-taking prompt
   Record completed main/full GitHub run results, artifacts, candidates, frontier, and memory.

2. Hypothesis prompt
   Compare recorded history, make a non-repeating hypothesis, and run small local checks if useful.

3. Launch-preparation prompt
   Prepare files and exact GitHub inputs. Smoke-test may be used as a quick technical gate.

4. Wrap-up prompt
   Review confusion/time loss and update memory files.
```

Smoke-test rule:

```text
Smoke-test is only a technical green-light before the long run.
If the user sees a green check and launches the 5h+ full run, the next result-taking chat records the full run, not the smoke-test.
Inspect smoke separately only if it failed, looked suspicious, or the user explicitly asks.
```

## 5. Prepared next direction

Prepared serious direction:

```text
workflow: smart-search-14-rich-cover-stitch
workflow file: .github/workflows/smart-search-14-rich-cover-stitch.yml
plan file: docs/smart-search-14-rich-cover-stitch-plan.md
engine generator: scripts/prepare_rich_cover_stitch_engine.py
generated C++: build/rich_cover_stitch_search.cpp
hypothesis: rich-cover -> endpoint-feasible stitch-compress
```

Meaning in simple words: first build richer 3-point and 4-point covering material, then stitch only through intervals whose endpoints really cover the intended grid points. Goal: avoid another inherited `59/64` repair loop.

Before giving launch/full-run advice, verify the workflow, plan, generator, and `frontier/latest.*` still agree.

Prepared smoke-test inputs:

```text
seconds: 180
threads: 4
seed: 20260705
min_covered_to_save: 56
latest_run_id: 28460740781
previous_diversity_run_id: 28404861374
d2_bridge_run_id: 28378489636
d_family_run_id: 28338041580
new_defect_run_id: 28327372242
jobs/shards: 20
max-parallel: 20
```

Full-run inputs after green smoke-test:

```text
seconds: 21000
threads: 4
seed: 20260705
min_covered_to_save: 56
latest_run_id: 28460740781
previous_diversity_run_id: 28404861374
d2_bridge_run_id: 28378489636
d_family_run_id: 28338041580
new_defect_run_id: 28327372242
jobs/shards: 20
max-parallel: 20
expected wall time: about 5h50m per shard
```

Useful full-run result means either `60/64+` with `links <= 22`, or a clearly new `59/64` family with weaker convergence than the `14/20` dominant wall from smart-search-13.

## 6. Candidate memory rules

```text
candidates/bank.jsonl: compact reusable search memory; symmetry-deduplicated fuel
candidates/bank-additions-*.jsonl: run-level additions before/alongside merging
candidates/originals/: non-deduplicated scientific archive of real shard-best diversity
normal save threshold: covered_count >= 56 and links <= 22
```

After every completed full run: save champion, compact additions, original shard-best index if available, update `frontier/latest.*`, and update this file if the frontier or next step changed.

## 7. Common traps

```text
Do not call partial candidates proofs.
Do not confuse local preflight with evidence of a solution.
Do not confuse a chat hypothesis with an actual GitHub workflow file.
Do not treat old smart-search-13 plan docs as the next launch plan.
Do not read candidates/bank.jsonl alone; include recent bank-additions files.
Do not spend a new chat analyzing green smoke unless asked.
```

When unsure, prefer a small local check or a short documented smoke gate before a 20-job full run.
