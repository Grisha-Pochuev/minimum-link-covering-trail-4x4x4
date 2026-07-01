# START HERE — project memory

Last updated: 2026-07-01 wrap-up

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
2. `frontier/latest.md` and `frontier/latest.json` — current frontier, latest useful run, and prepared next package.
3. `docs/web-chat-runbook-prompts.md` — optimized web-chat prompts and launch checklist.
4. The exact workflow in `.github/workflows/` that launched the completed run or is prepared for the next smoke-test. Do not substitute the newest workflow for an old run.
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

## Whole-chat wrap-up from 2026-07-01

What went well:

```text
- Results from run 28460740781 were recorded, checked, and saved.
- The next idea was not chosen blindly: runs 9-13 were compared as a sequence of changing 59/64 defect walls.
- The selected next hypothesis is different in kind: rich-cover first, then endpoint-feasible stitch-compress.
- A prepared smart-search-14 package now exists in the repository and is documented.
```

Where time was lost:

```text
- Some time was spent re-deriving history that should be read from START_HERE/frontier/run summaries first.
- There was risk of confusing three things: a chat-level hypothesis, a locally checked prototype, and an actual GitHub workflow file.
- frontier/latest.md and frontier/latest.json lagged behind START_HERE after the smart-search-14 package was prepared; this has now been corrected.
```

Files that can mislead the next chat if read carelessly:

```text
- docs/smart-search-13-cover-stitch-cache-plan.md is historical. It is not the next launch plan.
- frontier/latest.* should be treated as the current index only after confirming it mentions smart-search-14.
- candidates/bank.jsonl is not the full recent memory by itself; also read bank-additions-run28460740781 and earlier additions.
- Local/preflight notes are technical smoke evidence, not evidence that a 22-link solution exists.
```

## Current next step

Do not launch another same-seed `smart-search-13-cover-stitch-cache` full run. The run validates the cache/anti-wall machinery technically, but it still stayed at `59/64`.

The next concrete step is to run a short GitHub smoke-test for the prepared workflow `smart-search-14-rich-cover-stitch`. Only after a green smoke-test should a full 20-job run be considered.

The hypothesis behind smart-search-14:

```text
rich-cover -> endpoint-feasible stitch-compress
```

In simple words: first build richer 3-point and 4-point covering material, then stitch only through intervals whose chosen endpoints actually cover the intended grid points. The goal is to avoid another inherited 59-family repair loop.

Useful lesson from the latest full run:

```text
cache/anti-wall pressure: technically active and somewhat useful
numeric frontier: unchanged at 59/64
structural diversity: 3 -> 5 exact representatives, dominant family 18/20 -> 14/20
next search: smart-search-14 rich-cover / endpoint-feasible stitch-compress, not smart-search-13 rerun
```

## Prepared next launch package

Prepared workflow package:

```text
workflow: smart-search-14-rich-cover-stitch
workflow file: .github/workflows/smart-search-14-rich-cover-stitch.yml
plan file: docs/smart-search-14-rich-cover-stitch-plan.md
engine generator: scripts/prepare_rich_cover_stitch_engine.py
generated C++: build/rich_cover_stitch_search.cpp
```

This package is manual-only and should be smoke-tested before any full run. It is not a proof and not a guaranteed improvement; it is the next non-repeating search hypothesis after smart-search-13.

Before giving launch inputs in a new chat, fetch back and verify:

```text
.github/workflows/smart-search-14-rich-cover-stitch.yml
docs/smart-search-14-rich-cover-stitch-plan.md
scripts/prepare_rich_cover_stitch_engine.py
frontier/latest.md
frontier/latest.json
```

Smoke-test inputs:

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
