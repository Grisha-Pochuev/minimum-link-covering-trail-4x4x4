# Current search frontier

This file is the human-readable working memory of the project.

It records the latest useful GitHub Actions run whose artifacts should be used as input for the next search. The goal is to make each new run continue from the previous computational evidence instead of starting from zero.

## Current status

Status: smart-search-6-defect full run analyzed and recorded.

Latest useful completed run:

- Repository: `Grisha-Pochuev/minimum-link-covering-trail-4x4x4`
- Final run id: `28275850889`
- Run URL: https://github.com/Grisha-Pochuev/minimum-link-covering-trail-4x4x4/actions/runs/28275850889
- Workflow: `smart-search-6-defect`
- Commit SHA: `1c1ba2f574bc075d29b65c6b2f5a571ac6069634`
- Status: `success`
- Duration: full run, `21000` seconds per shard
- Result type: heuristic search, not a proof
- Artifact set: `defect-run-summary`, `defect-22-shard-*`, `defect-seed-manifest-*`

## Parameters

- seconds: `21000`
- threads: `4` per shard
- shards: `20`
- max parallel jobs: `20`
- seed: `20260627`
- prior run id used by this run: `28275666411`
- base repair run id also used: `28200925016`
- coordinate scale: `2`
- min covered to save: `56`
- engine: generated defect repair C++ engine based on `cpp/repair56_search.cpp` and the current defect target
- checker: `scripts/check_scaled_trail.py` plus post-run exact integer scaled-geometry verification

## Best GitHub Actions run result

Best known result after GitHub Actions run `28275850889`:

- covered_count: `59 / 64`
- coverage percent: `92.1875%`
- links: `22`
- links target: `22`
- mode selected by summary: `fractional_bridge22`
- source artifact: `defect-22-shard-6`
- candidate id: `mlct22-278a7d8dc1d65f25`
- status: `partial_candidate`
- missing count: `5`
- missing:
  - `(1, 2, 2)`
  - `(2, 0, 2)`
  - `(2, 0, 3)`
  - `(3, 1, 2)`
  - `(3, 1, 3)`

The best GitHub Actions candidate is still partial. It has exactly 22 links and covers 59 of the 64 grid points. This is not a complete covering trail and not a proof.

The exact full JSON for the best candidate is saved in:

```text
runs/2026-06-27-smart-search-6-defect-full/best_candidate.json
```

A reusable copy is also saved in:

```text
candidates/mlct22-278a7d8dc1d65f25-run28275850889.json
```

## Candidate preservation rule for future runs

Future workflows must use a threshold rule, not a fixed list of levels.

For the next run, keep at least:

```text
min_covered_to_save = 56
```

But for practical analysis after this run, prioritize all unique candidates with:

```text
covered_count >= 59
```

In plain words: do not lose the older `56/64`, `57/64`, and `58/64` evidence, but the next search should treat the many `59/64` candidates as the main seed bank.

## Top recurring missing points from run 28275850889

Counted over the 20 shard-best JSON result files:

- `(1, 2, 2)`: 20 / 20
- `(3, 1, 0)`: 19 / 20
- `(2, 0, 2)`: 18 / 20
- `(2, 0, 3)`: 18 / 20
- `(3, 1, 2)`: 18 / 20
- `(3, 1, 3)`: 3 / 20
- `(2, 1, 2)`: 2 / 20
- `(2, 2, 3)`: 2 / 20

The defect core is now much sharper than after the smoke run. `(1,2,2)` was missed in all 20 shard-best results. The points `(2,0,2)`, `(2,0,3)`, `(3,1,0)`, and `(3,1,2)` were also missed in almost every shard-best result.

## Dominant missing patterns

Across the 20 shard-best results:

- 17 / 20: `(1,2,2), (2,0,2), (2,0,3), (3,1,0), (3,1,2)`
- 2 / 20: `(1,2,2), (2,1,2), (2,2,3), (3,1,0), (3,1,3)`
- 1 / 20: `(1,2,2), (2,0,2), (2,0,3), (3,1,2), (3,1,3)`

The selected best candidate is the rare variant that covers `(3,1,0)` but misses `(3,1,3)` instead. That is useful because it shows the obstruction can move inside the same local region, but it did not disappear.

## Which modes worked best in run 28275850889

All modes represented in the top shard results reached `59/64`:

- `fractional_bridge22`: 5 result(s), best `59/64`, average `59.00/64`
- `integer_control22`: 1 result(s), best `59/64`, average `59.00/64`
- `repair56_target8`: 5 result(s), best `59/64`, average `59.00/64`
- `rich_segment_catalog`: 1 result(s), best `59/64`, average `59.00/64`
- `subcube_stitch22`: 5 result(s), best `59/64`, average `59.00/64`
- `transition_penalty22`: 3 result(s), best `59/64`, average `59.00/64`

The conclusion is different from the earlier smoke-test conclusion. The C++ defect-repair direction is clearly strong enough to reproduce `59/64` across the whole 20-shard run, but the current search shape appears to saturate at `59/64`.

## Comparison with previous runs

- Run `28103660449` / smart-search-4: best `56/64`, 8 missing points.
- Local prelaunch repair smoke: best `57/64`, 7 missing points.
- Run `28200925016` / repair-search-5: best `58/64`, 6 missing points.
- Run `28275666411` / smart-search-6-defect smoke-test: best `59/64`, 5 missing points, but only 90 seconds per shard.
- Run `28275850889` / smart-search-6-defect full run: best `59/64`, 5 missing points, confirmed across 20 full shards with `21000` seconds each.

So this run did not raise the numeric frontier beyond the smoke result, but it turned `59/64` from a short-test surprise into a stable, reproducible frontier.

## What became clear for the next run

- No complete `64/64` candidate was found.
- The next run should not simply repeat the same broad defect-repair distribution.
- The main target should be the dominant 5-point defect core: `(1,2,2)`, `(2,0,2)`, `(2,0,3)`, `(3,1,0)`, `(3,1,2)`, plus the close variant with `(3,1,3)`.
- The best next mathematical move is local repair around the final defect transitions and around the region connecting the `x=2,y=0` and `x=3,y=1` defect clusters.
- `fractional_bridge22` deserves budget because the selected best came from it, but the fact that every mode reached `59/64` means the next improvement probably needs a new repair idea, not just more of the same.

## Next run seed source

The next serious run should start from:

- GitHub Actions artifacts of run `28275850889`;
- GitHub Actions artifacts of run `28275666411`;
- GitHub Actions artifacts of run `28200925016`;
- `defect-run-summary` from this run;
- all `defect-22-shard-*` artifacts from this run;
- `runs/2026-06-27-smart-search-6-defect-full/best_candidate.json`;
- `runs/2026-06-27-smart-search-6-defect-full/top_candidates.json`;
- `candidates/mlct22-278a7d8dc1d65f25-run28275850889.json`;
- `candidates/bank.jsonl` as older broad seed memory.

Prepared next focus:

```text
smart-search-7-core5: repair the stable 5-point defect core of the 59/64 frontier, using exact local repair and transition-aware replacement windows rather than repeating the same broad repair distribution.
```
