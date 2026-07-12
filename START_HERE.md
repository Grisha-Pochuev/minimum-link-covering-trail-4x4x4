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

Roles:

- `START_HERE.md`: stable boot memory.
- `frontier/latest.md` and `frontier/latest.json`: best checked mathematical frontier.
- `frontier/active_run.json`: current operational run or completed run awaiting recording.
- `docs/web-chat-runbook-prompts.md`: reusable four-step process.
- `docs/smart-search-N-*.md`: exact handoff from research Step 2 to implementation Step 3.
- `runs/*`: completed-run evidence.
- candidate banks/originals: reusable curves and raw shard outputs.

At the start of a new working chat, read once:

1. `START_HERE.md`
2. `frontier/latest.md`
3. `frontier/latest.json`
4. `frontier/active_run.json`
5. `docs/web-chat-runbook-prompts.md`
6. workflow and launch document for the run being handled
7. latest relevant `runs/` archive
8. candidate banks/originals
9. Actions jobs, logs and artifacts

Do not repeatedly reopen this file during one four-step cycle unless context is genuinely missing.

## 3. Current recorded exact ordered frontier: 62/64

Best candidate:

- candidate id: `mlct22-er-943c78ae82c82664`
- file: `runs/2026-07-12-smart-search-22-endpoint-repair-smoke/best_candidate.json`
- covered count: `62/64`
- links: `22`
- vertices: `23`
- missing: `(2,3,1)`, `(3,3,1)`
- mode: `free_start_62`
- operation: `endpoint_sweep`
- source run: `29181400035`
- status: `verified_partial_candidate`

Verification:

- 22 nonzero links;
- checked by `scripts/check_rational_trail.py`;
- checked independently by `scripts/verify_rational_trail_independent.py`;
- smoke aggregate received `20/20` shards;
- smoke saved `38` compact symmetry classes at `62/64`;
- smoke found no `63/64` or `64/64` class.

Mechanism: moving one free endpoint changes only one link, while moving an internal vertex changes two. This converted a search-21 three-hole family into a two-hole family.

## 4. Search-21 full result

Run `29123493808`:

- workflow: `smart-search-21-bridge-compress`
- profile: full
- intended shards: `20`
- successful shard artifacts: `19`
- one failed shard: `official60_productive_bridge`, shard `10`
- exact failure cause unavailable because the downloadable log blob was missing
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

Lesson: direct compression of the exact 23-link trail is much stronger than rebuilding a trail from an unordered scaffold, but broad compression saturated around these defect lines.

## 5. Search-22 smoke

Run: `29181400035`

URL: https://github.com/Grisha-Pochuev/minimum-link-covering-trail-4x4x4/actions/runs/29181400035

- workflow: `smart-search-22-endpoint-repair`
- status: success
- precheck: success
- shards received: `20/20`
- best: `62/64`
- compact `62/64`: `38`
- compact `63/64`: `0`
- compact `64/64`: `0`
- raw shard-best originals: `80`

The smoke validated every mode, both exact verifiers, aggregation and all three candidate-bank outputs before full launch.

## 6. Full search-22 completed — Prompt 1 required now

Authoritative operational record: `frontier/active_run.json`.

- run id: `29181546758`
- URL: https://github.com/Grisha-Pochuev/minimum-link-covering-trail-4x4x4/actions/runs/29181546758
- workflow: `smart-search-22-endpoint-repair`
- profile: full
- launch commit: `7925fd4e6b42ce8591b0958bce106901c4c305ec`
- status: completed
- conclusion: success
- summary artifact: present

Full profile:

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

The mathematical contents of this full run have not yet been recorded into `runs/`, candidate banks or the frontier. Do not launch another search and do not choose search-23 before Prompt 1 analyzes and records run `29181546758`.

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

Technical debt: the search engine was split into `part-*.pyfrag` because a connector blocked one large source upload. After the full run is recorded, refactor it into normal importable Python modules before reusing or extending the engine for search-23.

Shard modes:

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

All states keep exactly 23 vertices and 22 nonzero links.

## 8. Earlier structural history

- search-17: unordered 22-line `64/64` scaffolds; not trails.
- search-18: ordered reconstruction reached `44/64`.
- search-19: contact-state reconstruction reached `46/64`.
- search-20: preserved rich lines and reached `58/64`, but used eight explicit bridges.
- search-21: direct compression reached exact `61/64` with zero pure bridges.
- search-22 smoke: endpoint repair reached exact `62/64` before the full run.

Best unordered scaffold remains `mlct22-lineset-9772981a21b2a88a`, run `28825060197`, `64/64` as an unordered line set only. Never merge line-set scaffolds into the ordered-trail bank without constructing and exactly checking consecutive trail vertices.

## 9. Four-step cycle

1. Record a completed run.
2. Choose one non-repeating hypothesis, test locally and persist a precise launch/plan document.
3. Implement that handoff in one workflow, run local dry checks, smoke, then full.
4. Review the chat and improve memory/process without changing the historical run commit.

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

Generic workflows must use narrow path filters. Launch, docs and memory commits must not start unrelated legacy searches.

## 10. Current next step

Run Prompt 1 for completed full run `29181546758`:

1. inspect all jobs and failures;
2. download every available shard artifact and aggregate;
3. verify every `62/64+` candidate independently;
4. record any `63/64` or `64/64` improvement immediately;
5. save ordinary additions, diagnostic classes and raw originals;
6. record defect families, RAM and throughput;
7. update `runs/`, `frontier/latest.*`, `frontier/active_run.json` and this memory;
8. refactor the fragment-based search-22 engine into normal modules;
9. only then choose search-23.
