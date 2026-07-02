# START HERE — compact agent memory

Last updated: 2026-07-02

This file is the first thing to read in a new ChatGPT web chat. It is the boot memory, not the full diary. Keep it short. Detailed history belongs in `frontier/latest.*`, `runs/*/summary.md`, plans, and candidate banks.

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

Best recorded candidate:

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
- dominant missing family: `12/20`;
- second missing family: `7/20`;
- rich-cover / stitch idea was active but still insufficient.

Do not rerun `smart-search-14-rich-cover-stitch` with the same seed and modes as the next serious step.

## 4. Standard four-prompt workflow

Use the user's four-step rhythm:

1. result-taking prompt: record completed main/full GitHub run results, artifacts, candidates, frontier, and memory;
2. hypothesis prompt: compare recorded history, make a non-repeating hypothesis, and run small local checks if useful;
3. launch-preparation prompt: prepare files and exact GitHub inputs; smoke-test may be used as a quick technical gate;
4. wrap-up prompt: review confusion/time loss and update memory files.

Smoke-test is only a technical green-light before the long run. If the user sees a green check and launches the 5h+ full run, the next result-taking chat records the full run, not the smoke-test. Inspect smoke separately only if it failed, looked suspicious, or the user explicitly asks.

## 5. Current next direction

Recorded full run `28522369532` finished `smart-search-14-rich-cover-stitch`. It reduced collapse but still stayed at `59/64`. The next serious hypothesis should not be another same-seed smart-search-14 rerun.

Prepared next idea to investigate in the hypothesis prompt:

`cover-first diagnostics -> stitch-cost / transition graph diagnostics`

Meaning in simple words: first save and analyze rich cover skeletons before they are forced into one trail, then measure how expensive it is to stitch them into a connected 22-link trail.

What the next workflow should preserve, if prepared:

- best unordered cover-sets;
- `60+` pre-stitch skeletons if they appear;
- transition-cost tables between rich segments;
- failed-but-promising cover sets;
- final stitched candidates;
- skeleton-level novelty, not only missing-set novelty.

Useful next full-run result means either `60/64+` with `links <= 22`, or clear data showing whether the blocker is poor rich-cover material or the cost of stitching good material into one trail.

## 6. Candidate memory rules

- `candidates/bank.jsonl`: compact reusable search memory; symmetry-deduplicated fuel.
- `candidates/bank-additions-*.jsonl`: run-level additions before/alongside merging.
- `candidates/originals/`: non-deduplicated scientific archive of real shard-best diversity.
- Normal save threshold: `covered_count >= 56 and links <= 22`.

After every completed full run: save champion, compact additions, original shard-best index if available, update `frontier/latest.*`, and update this file if the frontier or next step changed.

Latest saved additions:

- `candidates/bank-additions-run28522369532.jsonl`
- `candidates/originals/run28522369532-shard-bests-index.jsonl`

## 7. Common traps

- Do not call partial candidates proofs.
- Do not confuse local preflight with evidence of a solution.
- Do not confuse a chat hypothesis with an actual GitHub workflow file.
- Do not treat old smart-search-14 as automatically worth rerunning.
- Do not read `candidates/bank.jsonl` alone; include recent bank-additions files.
- Do not spend a new chat analyzing green smoke unless asked.

When unsure, prefer a small local check or a short documented smoke gate before a 20-job full run.
