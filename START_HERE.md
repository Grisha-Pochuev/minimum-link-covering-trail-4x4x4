# START HERE — compact agent memory

Last updated: 2026-07-12

This file is the first thing to read in a new ChatGPT web chat. It is boot memory, not the full diary. Detailed run evidence belongs in `frontier/latest.*`, `runs/*`, candidate banks, launch docs, and GitHub Actions artifacts.

## 1. Project

Repository: `Grisha-Pochuev/minimum-link-covering-trail-4x4x4`

Problem: find a shortest connected polygonal trail covering all 64 points of the grid `{0,1,2,3}^3`.

Current target: an exact `22`-link trail covering `64/64`, or strong structural evidence toward impossibility.

Practical status:

- `23` links: known exact full construction; control and compression source.
- `22` links: open; best checked partial candidate is now `62/64`.
- `21` links: not a serious current search target.

Heuristic output is evidence only. A candidate enters the frontier only after exact checking.

## 2. First reading order

At the start of a new working chat, read once:

1. `START_HERE.md`
2. `frontier/latest.md`
3. `frontier/latest.json`
4. `docs/web-chat-runbook-prompts.md`
5. the active workflow and its launch document
6. the latest relevant `runs/` folder
7. candidate banks/originals
8. Actions jobs, logs and artifacts for the run being analyzed

Do not repeatedly reopen this file during the same four-step cycle unless context is genuinely missing.

## 3. Current exact ordered frontier: 62/64

Search-22 smoke run found and independently checked the current frontier.

- candidate id: `mlct22-er-943c78ae82c82664`
- file: `runs/2026-07-12-smart-search-22-endpoint-repair-smoke/best_candidate.json`
- covered count: `62/64`
- links: `22`
- missing: `(2,3,1)`, `(3,3,1)`
- mode: `free_start_62`
- operation: `endpoint_sweep`
- source shard: `0`
- source worker: `0`
- pure bridges: `0`
- rich4 links: `14`
- rich3 links: `2`
- productive connectors: `6`
- source run: `29181400035`
- status: `verified_partial_candidate`

Verification:

- 23 vertices and 22 nonzero links;
- checked by `scripts/check_rational_trail.py`;
- checked independently by `scripts/verify_rational_trail_independent.py`;
- the smoke aggregate received all `20/20` shards;
- the smoke run saved `38` compact symmetry classes at `62/64`;
- smoke found no `63/64` or `64/64` class.

The improvement mechanism is cheap endpoint freedom: changing one free endpoint changes only one link, while moving an internal vertex changes two links.

## 4. Search-21 full result

Full run `29123493808` completed before search-22 was designed.

- workflow: `smart-search-21-bridge-compress`
- profile: full
- intended shards: `20`
- saved successful shard artifacts: `19`
- one failed shard: `official60_productive_bridge`, shard `10`; exact root cause was unavailable because its downloadable log blob was missing
- total attempts over saved shards: `6,653,246`
- compact candidates: `965`
- compact `61/64`: `24`
- compact `60/64`: `79`
- `62/64+`: `0`

All 24 compact `61/64` classes reduced to two three-hole families:

```text
(0,2,1), (1,3,1), (2,3,1)
(3,0,3), (3,1,3), (3,2,3)
```

Structural lesson: direct compression of the exact 23-link trail is much stronger than rebuilding an ordered trail from an unordered scaffold, but broad search-21 compression saturated around these two defect lines.

## 5. Search-22 smoke run

- run id: `29181400035`
- URL: https://github.com/Grisha-Pochuev/minimum-link-covering-trail-4x4x4/actions/runs/29181400035
- workflow: `smart-search-22-endpoint-repair`
- profile: smoke
- status: success
- precheck: success
- shards received: `20/20`
- best: `62/64`
- compact `62/64`: `38`
- compact `63/64`: `0`
- compact `64/64`: `0`
- raw shard-best originals: `80`

The smoke run proved that the package, both exact verifiers, all modes, aggregation, and all three candidate-bank outputs work before spending the full budget.

## 6. Active full run — do not duplicate

The serious search-22 run is active.

- run id: `29181546758`
- URL: https://github.com/Grisha-Pochuev/minimum-link-covering-trail-4x4x4/actions/runs/29181546758
- workflow: `smart-search-22-endpoint-repair`
- profile: full
- launch commit: `7925fd4e6b42ce8591b0958bce106901c4c305ec`
- precheck: success
- all `20` shard jobs: created; computation started

Effective full profile:

```text
seconds=21000
workers=4
shards=20
max-parallel=20
seed=20260722 + shard*1000003
beam_width_per_worker=12000
state_cap_per_worker=750000
save_min_covered=60
top_diverse_per_worker=200
checkpoint_seconds=600
timeout-minutes=359
```

Do not launch another search-22 while this run is active.

## 7. Search-22 package

Exactly one visible workflow exists for search number 22:

```text
.github/workflows/smart-search-22-endpoint-repair.yml
scripts/endpoint_repair_search.py
scripts/endpoint_repair_parts/part-*.pyfrag
scripts/verify_endpoint_repair_batch.py
scripts/build_endpoint_repair_summary.py
data/search22_endpoint_62_seed.json
data/search22_run21_60plus_seed_parts/part-*.jsonlpart
docs/smart-search-22-endpoint-repair-launch.md
```

The package includes precheck, 20 modes, two exact verifiers, checkpoints, memory statistics, per-shard artifacts, aggregation, three candidate-bank outputs, manual dispatch, and narrow smoke/full push triggers. Do not create a second launcher/bootstrap workflow for search-22.

## 8. Search-22 shard modes

```text
0–1   free_start_62
2–3   free_end_62
4–5   endpoint_all_61_family_A
6–7   endpoint_all_61_family_B
8–9   endpoint_window_2to3
10–11 endpoint_window_4to5
12–13 endpoint_window_6to8
14–16 paired_budget_transfer
17    two_free_ends
18    defect_line_forcing
19    search21_control
```

The search always keeps exactly 23 vertices and 22 nonzero links.

## 9. Earlier structural history

- search-17: unordered 22-line `64/64` scaffolds; not trails.
- search-18: ordered reconstruction reached `44/64`.
- search-19: contact-state reconstruction reached `46/64`.
- search-20: preserved rich lines and reached `58/64`, but paid eight explicit bridges.
- search-21: direct compression reached exact `61/64` with zero pure bridges.
- search-22: endpoint repair reached exact `62/64` before the serious full run.

Best unordered scaffold remains `mlct22-lineset-9772981a21b2a88a`, run `28825060197`, `64/64` as an unordered line set only. Never merge line-set scaffolds into the ordinary ordered-trail bank without constructing and exactly checking consecutive trail vertices.

## 10. Standard four-prompt cycle

1. Record the completed full run: jobs, logs, artifacts, frontier, banks, originals, memory.
2. Choose one non-repeating hypothesis and run small local tests.
3. Implement that hypothesis in one workflow and automatically launch smoke then full.
4. Review the chat and clean project memory.

Step-3 rules remain mandatory:

- exactly one workflow for a search number;
- serious profile `21000` seconds, 20 shards, normally four workers;
- all parameters resolved inside YAML;
- smoke must pass before full;
- confirm precheck and creation of all 20 full shard jobs;
- never launch a duplicate after success.

## 11. Current next step

Wait for full run `29181546758` to finish. Then use Prompt 1 to:

1. inspect all jobs and any failures;
2. download every available shard artifact and the aggregate;
3. verify every `62/64+` candidate independently;
4. record any `63/64` or `64/64` improvement immediately;
5. save ordinary additions, diagnostic classes, and raw originals in their three banks;
6. update `runs/`, `frontier/latest.*`, and this memory;
7. only then choose search-23.
