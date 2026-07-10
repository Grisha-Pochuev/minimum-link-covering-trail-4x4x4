# START HERE — compact agent memory

Last updated: 2026-07-11

This file is the first thing to read in a new ChatGPT web chat. It is boot memory, not the full diary. Read it once at the beginning of the working chat. Detailed history belongs in `frontier/latest.*`, `runs/*/summary.md`, plans, runbooks, and candidate banks.

## 1. Project

Repository: `Grisha-Pochuev/minimum-link-covering-trail-4x4x4`

Problem: find a shortest connected polygonal trail covering all 64 points of the `4×4×4` grid `{0,1,2,3}^3`.

Current target: a `22`-link trail covering `64/64`, or enough obstruction evidence to guide a proof/search.

Known practical status:

- `23` links: known full construction; used as control and compression source.
- `22` links: open target; best checked partial candidate is now `61/64`.
- `21` links: too hard for serious search now; use only as diagnostic pressure.

Heuristic search results are evidence, not proof. A candidate becomes frontier evidence only after exact checking.

## 2. First reading order

At the beginning of a new working chat, start from:

1. `START_HERE.md`
2. `frontier/latest.md`
3. `frontier/latest.json`
4. `docs/web-chat-runbook-prompts.md`
5. exact workflow or prepared workflow
6. matching plan/launch doc
7. candidate bank/additions/originals
8. latest relevant `runs/` folder
9. GitHub Actions artifacts when analyzing a completed run

After this boot read, avoid reopening `START_HERE.md` during prompts 2–4 unless critical context is missing.

## 3. Current checked ordered frontier

A three-minute smoke run of search-21 produced the first checked improvement beyond the old `60/64` wall.

Best candidate:

- candidate id: `mlct22-bc-889d7f8c45252068`
- file: `runs/2026-07-10-smart-search-21-bridge-compress-smoke/best_candidate.json`
- covered_count: `61/64`
- links: `22`
- missing: `(0,2,1)`, `(1,3,1)`, `(2,3,1)`
- mode: `ripa_6to5_slide`
- construction: exact local `6→5` compression of the known full 23-link trail
- pure bridges: `0`
- rich4 links: `14`
- rich3 links: `1`
- productive connectors: `7`
- source run: `29123090565`
- status: `verified_partial_candidate`

Verification:

- 23 vertices, 22 nonzero links;
- checked by the exact rational checker in GitHub Actions;
- downloaded artifact independently recomputed again with a separate exact implementation;
- result confirmed as exactly `61/64`.

A second symmetry-inequivalent checked `61/64` candidate was also found:

- candidate id: `mlct22-bc-81b7ac625af94cf7`
- missing: `(3,0,3)`, `(3,1,3)`, `(3,2,3)`
- same `ripa_6to5_slide` family.

Both are saved in:

```text
candidates/ordered-trail-additions-run29123090565-bridge-compress-smoke.jsonl
```

## 4. Search-21 smoke run

- run id: `29123090565`
- run URL: https://github.com/Grisha-Pochuev/minimum-link-covering-trail-4x4x4/actions/runs/29123090565
- workflow display name: `smart-search-21-bridge-compress`
- profile: `smoke`
- status: `success`
- all prechecks succeeded
- all `20/20` shards succeeded
- every shard-best passed the exact checker
- aggregate succeeded
- shard-best rows: `20`
- compact classes: `598`
- total attempts: `60554`
- compact `61/64`: `2`
- compact `60/64`: `9`
- full `64/64`: `0`

Important lesson: direct local compression of the already complete 23-link trail is much more promising than reconstructing a trail from an unordered scaffold. Search-21 found `61/64` during smoke, before the long run.

## 5. Active full run

The full search-21 run is active. Do not launch a duplicate.

- run id: `29123493808`
- run URL: https://github.com/Grisha-Pochuev/minimum-link-covering-trail-4x4x4/actions/runs/29123493808
- workflow display name: `smart-search-21-bridge-compress`
- historical launch note: this run was started before workflow consolidation, through the old wrapper/reusable-workflow pair at head commit `48a5c5a4a6afbbc81cba3fcb0ae5ebe3178261bd`
- profile: `full`
- precheck: success
- 20 full shards: created and computation started

Effective full parameters:

```text
seconds=21000
workers=4
shards=20
seed=20260721 + shard*1000003
beam_width=16000
state_cap=3000000
candidate_lines=8000
start_limit=64
window_min=3
window_max=6
max_mutations=2
max_pure_bridges=6
target_min_rich_or_productive=16
save_min_covered=56
max-parallel=20
timeout-minutes=359
```

When this run completes, the next fresh chat should use Prompt 1 to record it. Do not choose a new hypothesis before its artifacts are analyzed.

## 6. Search-21 package after consolidation

There is now exactly one visible workflow for search number 21:

```text
.github/workflows/smart-search-21-bootstrap.yml
scripts/bridge_compress_common.py
scripts/bridge_compress_search.py
scripts/check_rational_trail.py
scripts/verify_rational_trail_independent.py
scripts/build_bridge_compress_summary.py
docs/smart-search-21-bridge-compress-launch.md
```

The file keeps the historical filename `smart-search-21-bootstrap.yml`, but it is now the complete self-contained workflow. Its visible GitHub Actions name is `smart-search-21-bridge-compress`, which follows the serious-run naming rule. It directly contains precheck, 20 search shards, exact checking, aggregation, artifacts, manual `workflow_dispatch`, and a narrow automatic full-run push trigger. The duplicate `.github/workflows/smart-search-21-bridge-compress.yml` was removed.

Automatic launch behavior for search-21:

- changing `launch/smart-search-21-full.trigger` launches the same single workflow;
- push-triggered launches always resolve to `profile=full`;
- `full` means `21000` seconds = `5 h 50 min`, `20` shards, `max-parallel=20`, `4` workers per shard;
- manual `Run workflow` remains available, with `full` as the default profile;
- no second launcher/bootstrap workflow may be created for the same search number.

## 7. Search-21 shard modes

```text
0–1   ripa_5to4_fixed
2–3   ripa_6to5_slide
4–5   ripa_outside_hub
6–7   official60_single_window
8–9   official60_double_window
10–11 official60_productive_bridge
12–13 scaffold_endpoint_zero_mutation
14–15 scaffold_endpoint_one_mutation
16–17 scaffold_endpoint_two_mutations
18    search20_control
19    mixed_compression
```

The strongest smoke family was `ripa_6to5_slide`.

## 8. Previous structural history

- search-17 found unordered 22-line scaffolds covering `64/64`; these are not trails.
- search-18 ordered reconstruction reached only `44/64`.
- search-19 contact-state reconstruction reached `46/64`; rich-line clipping was the main failure.
- search-20 preserved 14 rich lines and reached `58/64`, but spent 8 explicit bridge links.
- search-21 directly compressed the full 23-link trail and reached checked `61/64` with zero pure bridges.

Best unordered scaffold remains:

- candidate `mlct22-lineset-9772981a21b2a88a`
- run `28825060197`
- unordered coverage `64/64`
- status `line_set_seed_not_a_trail`.

Counting caution: line-set scaffolds must never be merged into the ordinary ordered-trail bank until exact consecutive trail vertices are constructed and checked.

## 9. Standard four-prompt workflow

1. Record a completed full run: artifacts, frontier, banks, originals, memory.
2. Choose one new non-repeating research hypothesis and do small local checks if useful.
3. Implement only that chosen hypothesis and automatically launch the serious full run.
4. Review the chat and clean up project memory.

### Mandatory Step-3 launch rule

When the user asks for Step 3 after a hypothesis has been selected:

1. create one complete workflow for that numbered search;
2. name it `smart-search-N-short-description`, with a short one- or two-word descriptive suffix;
3. keep exactly one visible workflow for that number — never create a second `bootstrap`, `launcher`, or duplicate workflow with the same `N`;
4. include precheck, engine, checker, aggregation and artifacts in that one workflow;
5. automatically launch the full profile from the web chat without asking the user to press buttons when repository write access is available;
6. if the connector has no `workflow_dispatch` action, put a narrow push trigger in that same workflow and launch it by committing `launch/smart-search-N-full.trigger`; do not create another workflow as a launcher;
7. the serious full profile is `seconds=21000` (`5 h 50 min`), `20` shards/jobs, `max-parallel=20`, and normally `4` workers per shard unless the chosen engine has a documented reason to differ;
8. all full numeric parameters must be resolved inside YAML; never rely on the user manually filling many boxes;
9. verify from Actions that the intended full run started, precheck passed, and all 20 shard jobs were created;
10. do not launch a duplicate after success.

Manual-run safety rule: use one `profile` input. `profile=full` must be the default serious option and resolve all numeric parameters inside YAML; blank custom boxes are expected.

Active-run safety rule: edits on `main` do not change the immutable workflow graph already running from its recorded head commit. Do not cancel or duplicate an active long run merely to improve workflow organization.

## 10. Current next step

Do nothing that duplicates the active full run.

When run `29123493808` completes:

1. use Prompt 1;
2. inspect all jobs, logs, artifacts, effective profiles and aggregate;
3. save all 20 shard-best originals;
4. save compact candidate classes and ordinary additions;
5. verify every `61/64+` candidate independently;
6. update `frontier/latest.*`, `START_HERE.md`, run archive and candidate banks;
7. only then choose the next hypothesis.
