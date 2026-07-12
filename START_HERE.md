# START HERE — compact agent memory

Last updated: 2026-07-12

This is the first file to read in a new ChatGPT web chat. It is boot memory, not the full diary and not the live status database.

## 1. Project

Repository: `Grisha-Pochuev/minimum-link-covering-trail-4x4x4`

Problem: find a shortest connected polygonal trail covering all 64 points of `{0,1,2,3}^3`.

Current target: an exact `22`-link trail covering `64/64`, or strong structural evidence toward impossibility.

Practical status:

- `23` links: known exact full construction; control and compression source.
- `22` links: open; best checked and recorded partial candidate is `62/64`.
- `21` links: not a serious current search target.

Heuristic output is evidence only. A candidate enters the frontier only after exact checking.

## 2. File roles and reading order

- `START_HERE.md`: stable boot memory.
- `frontier/latest.md` and `frontier/latest.json`: best checked mathematical frontier.
- `frontier/active_run.json`: operational run state.
- `docs/web-chat-runbook-prompts.md`: reusable four-step process.
- `docs/smart-search-N-*.md`: exact handoff from Step 2 to Step 3.
- `runs/*`: completed-run evidence.
- candidate banks/originals: reusable curves and raw outputs.

At the start of a working chat, read once:

1. `START_HERE.md`
2. `frontier/latest.md`
3. `frontier/latest.json`
4. `frontier/active_run.json`
5. `docs/web-chat-runbook-prompts.md`
6. workflow and launch document for the run being handled
7. latest relevant `runs/` archive
8. candidate banks/originals
9. Actions jobs, logs and artifacts

## 3. Current exact ordered frontier: 62/64

Best recorded candidate after full search-22:

- candidate id: `mlct22-er-7671ee46bd711a25`
- file: `runs/2026-07-12-smart-search-22-endpoint-repair-full/best_candidate.json`
- covered count: `62/64`
- links: `22`
- vertices: `23`
- missing: `(0,2,1)`, `(3,3,1)`
- mode: `endpoint_all_61_family_A`
- operation: `seed_crossover`
- source run: `29181546758`
- status: `verified_partial_candidate`

It passed both exact rational verifiers and has exactly 22 nonzero links.

## 4. Full search-22 result

Run `29181546758`:

- workflow: `smart-search-22-endpoint-repair`
- profile: full
- status: success
- precheck: success
- shards received: `20/20`
- aggregate: success
- compact candidates: `2385`
- compact `62/64`: `1053`
- compact `61/64`: `777`
- compact `60/64`: `555`
- compact `63/64`: `0`
- compact `64/64`: `0`
- raw originals: `80`
- ordinary bank: `2385`
- diagnostic bank: `0`
- originals bank: `80`

Every shard best and every saved `62/64+` candidate was checked by both exact rational verifiers.

The full run did not improve the numerical frontier beyond the smoke result, but made `62/64` highly reproducible. The remaining defects stay concentrated in the old `z=1` boundary-line neighborhood.

Best 62-producing modes:

- `endpoint_all_61_family_A`: 325 classes
- `search21_control`: 255
- `defect_line_forcing`: 198
- `two_free_ends`: 136
- `endpoint_window_2to3`: 67
- `paired_budget_transfer`: 64
- `free_start_62`: 8

Family B, windows 4–5 and free-end-only did not reach 62.

## 5. Search history

- search-17: unordered 22-line `64/64` scaffolds; not trails.
- search-18: ordered reconstruction reached `44/64`.
- search-19: contact-state reconstruction reached `46/64`.
- search-20: preserved rich lines and reached `58/64`, but used eight explicit bridges.
- search-21: direct compression reached exact `61/64` with zero pure bridges.
- search-22: endpoint repair reached exact `62/64`; full run saturated there.

Best unordered scaffold remains `mlct22-lineset-9772981a21b2a88a`, run `28825060197`, `64/64` as an unordered line set only. Never merge it into the ordered-trail bank without constructing and exactly checking consecutive trail vertices.

## 6. Four-step cycle

1. Record a completed run.
2. Choose one non-repeating hypothesis, test locally and persist a precise plan.
3. Implement it in one workflow, run local dry checks, smoke, then full.
4. Review the chat and improve memory/process.

Mandatory Step-3 rules:

- exactly one workflow per search number;
- one primary hypothesis with limited controls;
- normal readable source modules;
- local compile/control/seed/all-mode/aggregation dry run before GitHub smoke;
- smoke aggregate and all expected artifacts must pass before full;
- full is normally 21000 seconds, 20 shards, max-parallel 20, four workers;
- all parameters resolved inside YAML;
- record run state in `frontier/active_run.json`;
- never launch a duplicate.

Generic workflows must use narrow path filters.

## 7. Current next step

Search-22 is fully recorded. Before adapting the engine for search-23, refactor `scripts/endpoint_repair_parts/part-*.pyfrag` into normal importable Python modules. Then perform Step 2 and choose one genuinely non-repeating search-23 hypothesis.

Do not rerun search-22 unchanged. Do not treat repeated heuristic failure as proof.
