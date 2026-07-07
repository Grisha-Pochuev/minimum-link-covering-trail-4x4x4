# smart-search-19-contact-state-dp plan

## Purpose

This launch package implements the chosen post-search-18 hypothesis without changing it: search-18 proved that unordered `64/64` line-set scaffolds are not enough. The next run must order those lines while tracking the actual contact point and the actual covered grid mask kept by each chosen line piece.

The new search uses contact-state DP/beam states of the form:

```text
(current line, current contact point, used lines mask, covered 64-grid mask)
```

and records the loss table:

```text
full scaffold line mask -> chosen ordered piece mask -> lost grid points
```

## Workflow

Native workflow file:

```text
.github/workflows/smart-search-19-contact-state-dp.yml
```

Workflow name:

```text
smart-search-19-contact-state-dp
```

The workflow is `workflow_dispatch` only. It has no `push` trigger.

## Main files

- engine: `scripts/contact_state_dp_from_scaffolds.py`
- checker: `scripts/check_ordered_trail_scaled.py`
- summary builder: `scripts/build_contact_state_dp_summary.py`
- plan: `docs/smart-search-19-contact-state-dp-plan.md`
- workflow: `.github/workflows/smart-search-19-contact-state-dp.yml`

## Inputs used by the engine

Search-17 strong `64/64` line-set scaffolds:

- `runs/2026-07-07-smart-search-17-cover64-stitch-graph-full/best_line_set.json`
- `candidates/line-set-additions-run28825060197-cover64-stitch.jsonl`

Search-18 diagnostic ordered failures:

- `runs/2026-07-07-smart-search-18-order-from-cover64-stitch-full/best_ordered_candidate.json`
- `candidates/diagnostic-order-from-cover64-run28875314204.jsonl`

Search-18 diagnostics are not treated as frontier candidates. They are used as examples of contact-loss failure patterns.

## Shard modes

The 20 shards are intentionally not identical:

- `0..3`: `exact_top4_dp`
- `4..7`: `wide_beam_contact_state`
- `8..11`: `loss_minimizing`
- `12..15`: `official60_aware`
- `16..17`: `controlled_bridge_replacement`
- `18`: `diagnostic_replay`
- `19`: `conservative_control`

## Artifact names

Shard artifacts:

```text
contact-state-dp-22-shard-*
```

Summary artifact:

```text
contact-state-dp-run-summary
```

Summary files:

- `collected/contact_state_dp_run_summary.json`
- `collected/contact_state_dp_run_summary.md`
- `collected/contact-state-dp-candidates.jsonl`

Each shard saves:

- `contact_state_dp_best_shard_<shard>.json`
- `preferred_contact_state_dp_shard_<shard>.jsonl`
- `contact_loss_report_shard_<shard>.json`

## Smoke-test inputs

```text
seconds: 180
workers: 4
seed: 20260719
beam_width: 2048
state_cap: 200000
candidate_scaffolds: 4
max_mutations: 1
box_min: -1
box_max: 4
min_piece_cover: 1
save_min_covered: 38
branch_limit: 6
start_limit: 22
candidate_lines: 3000
```

## Full-run inputs

```text
seconds: 21000
workers: 4
seed: 20260719
beam_width: 8192
state_cap: 2000000
candidate_scaffolds: 4
max_mutations: 2
box_min: -1
box_max: 4
min_piece_cover: 1
save_min_covered: 44
branch_limit: 6
start_limit: 22
candidate_lines: 3000
```

## Technical readiness checks

The workflow:

- starts with `name:`;
- is `workflow_dispatch` only;
- has 20 matrix shards;
- uses `max-parallel: 20`;
- checks the known 23-link construction;
- checks search-17 input scaffolds;
- runs `scripts/contact_state_dp_from_scaffolds.py`;
- validates shard best JSON with `scripts/check_ordered_trail_scaled.py` when `vertices2` exists;
- aggregates with `scripts/build_contact_state_dp_summary.py`;
- uploads shard and summary artifacts with the expected names.

## Known technical launch issue and fix

Initial run:

```text
https://github.com/Grisha-Pochuev/minimum-link-covering-trail-4x4x4/actions/runs/28902841543
```

failed red because of a technical checker-step shell/heredoc bug in `Check ordered-chain JSON geometry`. The contact-state engine step itself completed in shard jobs; this was not evidence that the mathematical hypothesis failed.

Fix commit:

```text
ed5c56c90bca2044d55cbab6f48c0fb8c3b4071f
Fix contact-state checker heredoc
```

Do not use `Re-run failed jobs` on run `28902841543`; it used the old broken commit. Start a fresh manual `Run workflow` from branch `main`.

## Implementation-language note

The current engine is Python. That is acceptable for the first hypothesis/prototype launch because it is not meant to be a final high-performance brute-force engine. If search-19 shows a real signal, especially clear movement above the search-18 `44/64` ceiling, port the heavy contact-state DP/beam loop to C++ and keep Python for workflow, JSON, checker, and summary plumbing.

## Success criteria

Strong success:

- a checked ordered 22-link candidate with `covered_count >= 61`.

Medium success:

- any checked ordered candidate clearly above search-18's `44/64` diagnostic ceiling.

Useful negative result:

- no big coverage jump, but the summary explains which rich scaffold lines are being clipped and which grid points are repeatedly lost.
