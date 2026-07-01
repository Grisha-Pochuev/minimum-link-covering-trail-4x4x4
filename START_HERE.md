# START HERE — project memory

Last updated: 2026-07-01

This is the first file to read when starting work in a new ChatGPT web chat. Treat this repository as durable memory: read this file first, then continue from the current frontier and the exact workflow/run being analyzed.

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

## Current frontier to remember

Latest recorded completed full run:

```text
run id: 28460740781
workflow: smart-search-13-cover-stitch-cache
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
candidate id: mlct22-1c8736b46b59a730
source artifact: cover-stitch-cache-22-shard-6
mode: stitch_with_transposition
saved at: runs/2026-06-30-smart-search-13-cover-stitch-cache-full/best_candidate.json
```

Missing points:

```text
(0, 1, 2)
(1, 2, 1)
(1, 3, 2)
(2, 1, 3)
(2, 2, 2)
```

Observation: all 20 shard-best artifacts reached `59/64`, but none reached `60/64` or `64/64`. This run improved structural diversity only modestly: run `28404861374` had 3 exact representatives and a dominant exact curve in `18 / 20` shard-best artifacts; run `28460740781` had 5 exact representatives and the dominant missing-set family in `14 / 20` artifacts. Cache and anti-wall fields were active, with nonzero `cache_rejects` and `wall_rejects`, but they did not break the `59/64` wall.

Saved run memory:

```text
frontier/latest.md
frontier/latest.json
runs/2026-06-30-smart-search-13-cover-stitch-cache-full/summary.md
runs/2026-06-30-smart-search-13-cover-stitch-cache-full/best_candidate.json
runs/2026-06-30-smart-search-13-cover-stitch-cache-full/mode_breakdown.json
runs/2026-06-30-smart-search-13-cover-stitch-cache-full/compact_representatives.md
candidates/bank-additions-run28460740781.jsonl
candidates/originals/run28460740781-shard-bests-index.jsonl
```

Note: `candidates/bank.jsonl` was not merged in this step. The five compact run-level additions are saved in `candidates/bank-additions-run28460740781.jsonl`. Four exact IDs are new relative to the recorded run `28404861374` additions; one exact ID, `mlct22-1c8736b46b59a730`, was already present there and reappeared strongly.

## Current next step

Do not immediately launch another same-seed `smart-search-13-cover-stitch-cache` full run. The run validates the cache/anti-wall machinery technically, but it still stayed at `59/64`.

The next hypothesis step should move beyond inherited repair-search tuning. The most natural direction is a stronger unordered cover-set / stitch-compress engine, or a new-skeleton-first generator that delays or limits domination by old 59-families.

Useful lesson from this run:

```text
cache/anti-wall pressure: technically active and somewhat useful
numeric frontier: unchanged at 59/64
structural diversity: 3 -> 5 exact representatives, dominant family 18/20 -> 14/20
next search: stronger new skeleton / unordered cover-set / stitch-compress, not same rerun
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

Post-run rule: save champion, save compact additions, save original shard-best candidate index when available, update `frontier/latest.*`, and update `START_HERE.md` if the frontier or next step changed.

## Flexible post-run reasoning loop

After a completed run, do not merely fill a template. Ask whether the numeric frontier improved, whether the defect family changed, whether many shards converged, whether compact memory gained useful representatives, whether any mode should be reduced, and whether the run suggests a possible obstruction rather than just more candidates.
