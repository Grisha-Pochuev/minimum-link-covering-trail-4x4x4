# Current search frontier

This file is the human-readable working memory of the project.

It records the latest useful GitHub Actions run whose artifacts should be used as input for the next search. The goal is to make each new run continue from the previous computational evidence instead of starting from zero.

## Current status

Status: smart-search-6-defect smoke-test analyzed and recorded.

Latest useful completed run:

- Repository: `Grisha-Pochuev/minimum-link-covering-trail-4x4x4`
- Final run id: `28275666411`
- Run URL: https://github.com/Grisha-Pochuev/minimum-link-covering-trail-4x4x4/actions/runs/28275666411
- Workflow: `smart-search-6-defect`
- Commit SHA: `a9192d722ecd80e3b29a59bea2b2efffec4f8a13`
- Status: `success`
- Duration: smoke-test, `90` seconds per shard
- Result type: heuristic search, not a proof
- Artifact set: `defect-run-summary`, `defect-22-shard-*`

## Parameters

- seconds: `90`
- threads: `4` per shard
- shards: `20`
- max parallel jobs: `20`
- seed: `20260627`
- prior run id used by this run: `28200925016`
- coordinate scale: `2`
- engine: generated from `cpp/repair56_search.cpp` by `scripts/prepare_repair58_engine.py`
- checker: `scripts/check_scaled_trail.py`

## Best GitHub Actions run result

Best known result after GitHub Actions run `28275666411`:

- covered_count: `59 / 64`
- coverage percent: `92.1875%`
- links: `22`
- links target: `22`
- mode selected by summary: `subcube_stitch22`
- source artifact: `defect-22-shard-15`
- status: `partial_candidate`
- missing count: `5`
- missing:
  - `(1, 2, 1)`
  - `(2, 1, 2)`
  - `(2, 2, 3)`
  - `(3, 1, 0)`
  - `(3, 1, 3)`

The best GitHub Actions candidate is still partial. It has exactly 22 links and covers 59 of the 64 grid points. This is not a complete covering trail and not a proof.

The exact full JSON for the best candidate is saved in:

```text
runs/2026-06-27-smart-search-6-defect-smoke/best_candidate.json
```

## Candidate preservation rule for future runs

Future workflows must use a threshold rule, not a fixed list of levels.

For the next run, set:

```text
min_covered_to_save = 56
```

Then save every unique candidate with:

```text
covered_count >= min_covered_to_save
```

In plain words: save all `56/64` candidates and everyone above that level: `57/64`, `58/64`, `59/64`, ..., up to a possible full `64/64`.

## Top recurring missing points from run 28275666411

Counted over the 20 shard-best JSON result files:

- `(3, 1, 3)`: 13 / 20
- `(1, 2, 3)`: 13 / 20
- `(1, 2, 2)`: 12 / 20
- `(2, 1, 0)`: 9 / 20
- `(1, 2, 1)`: 8 / 20
- `(1, 1, 0)`: 7 / 20
- `(3, 1, 1)`: 7 / 20
- `(3, 1, 2)`: 7 / 20
- `(2, 2, 3)`: 6 / 20
- `(0, 0, 2)`: 6 / 20
- `(1, 1, 3)`: 6 / 20
- `(0, 0, 0)`: 5 / 20

The old 58/64 hard triple `(3,1,1)`, `(3,1,2)`, `(3,1,3)` is no longer missed in every best shard. The smoke run moved the obstruction into a new 5-point defect pattern.

## Which modes worked best in run 28275666411

- `subcube_stitch22`: best `59/64`, average about `58.33/64` over 3 results.
- `fractional_bridge22`: best `59/64`, average `58.25/64` over 4 results.
- `repair56_target8`: best `59/64`, average about `58.17/64` over 6 results.
- `transition_penalty22`: best `58/64` over 5 results.
- `rich_segment_catalog`: best `58/64` over 1 result.
- `integer_control22`: best `58/64` over 1 result.

The clear conclusion is that the C++ defect-repair direction worked again. The next full run should repair around the new 5-point defect set and use the smoke artifacts as seed material.

## What became clear for the next run

- The official GitHub Actions frontier improved from `58 / 64` to `59 / 64` even in a 90-second smoke-test.
- No complete `64 / 64` candidate was found.
- The next run should use both artifact sets: base repair run `28200925016` and smoke run `28275666411`.
- The next run should also use `runs/2026-06-26-repair-search-5/`, `runs/2026-06-27-smart-search-6-defect-smoke/`, and the curve bank `candidates/bank.jsonl`.
- The generated C++ engine should target the current 5 missing points, not the old 6 missing points from the 58/64 frontier.
- `subcube_stitch22`, `fractional_bridge22`, and local repair deserve the largest budget.

## Next run seed source

The next serious run should start from:

- GitHub Actions artifacts of run `28275666411`;
- GitHub Actions artifacts of run `28200925016`;
- `defect-run-summary`;
- all `defect-22-shard-*` artifacts from the smoke run;
- all `repair-22-shard-*` artifacts from the repair-search-5 run;
- `runs/2026-06-26-repair-search-5/top_candidates.json`;
- `runs/2026-06-27-smart-search-6-defect-smoke/best_candidate.json`;
- `candidates/bank.jsonl`.

Prepared next focus:

```text
repair the new 5-point defect pattern from the 59/64 candidate, while preserving every unique candidate with covered_count >= 56.
```
