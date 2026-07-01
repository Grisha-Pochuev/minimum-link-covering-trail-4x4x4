# Current search frontier

This file is the human-readable working memory of the project.

Status: `smart-search-13-cover-stitch-cache` full run completed successfully. Numeric frontier remains `59/64`; run `28460740781` is recorded as the latest completed full run. It did not find `60/64`, but it did improve run-level exact diversity compared with run `28404861374`.

The next prepared package is `smart-search-14-rich-cover-stitch`. Smoke-test is only a technical launch gate before the long run. It is not a separate mandatory result-taking stage in the standard web-chat cycle.

Latest recorded full run:

- Repository: `Grisha-Pochuev/minimum-link-covering-trail-4x4x4`
- Final run id: `28460740781`
- Run URL: https://github.com/Grisha-Pochuev/minimum-link-covering-trail-4x4x4/actions/runs/28460740781
- Workflow: `smart-search-13-cover-stitch-cache`
- Commit SHA of the run: `2912b39896255e069bce0a544cf5d32ff4fbb71f`
- Status: `success`
- Duration: full run, `21000` seconds per shard
- Threads per shard: `4`
- Shards/jobs: `20`
- Seed: `20260704`
- Result type: heuristic search, not a proof
- Artifacts: `cover-stitch-cache-run-summary`, `cover-stitch-cache-22-shard-*`

## Best GitHub Actions result

- candidate id: `mlct22-1c8736b46b59a730`
- covered_count: `59 / 64`
- coverage percent: `92.1875%`
- links: `22`
- selected mode: `stitch_with_transposition`
- source artifact: `cover-stitch-cache-22-shard-6`
- source shard: `6`
- status: `partial_candidate`
- missing count: `5`
- missing:
  - `(0, 1, 2)`
  - `(1, 2, 1)`
  - `(1, 3, 2)`
  - `(2, 1, 3)`
  - `(2, 2, 2)`

The best candidate is still partial. It has exactly 22 links and covers 59 of the 64 grid points. This is not a complete covering trail and not a proof.

Saved run memory:

```text
runs/2026-06-30-smart-search-13-cover-stitch-cache-full/summary.md
runs/2026-06-30-smart-search-13-cover-stitch-cache-full/best_candidate.json
runs/2026-06-30-smart-search-13-cover-stitch-cache-full/mode_breakdown.json
runs/2026-06-30-smart-search-13-cover-stitch-cache-full/compact_representatives.md
candidates/bank-additions-run28460740781.jsonl
candidates/originals/run28460740781-shard-bests-index.jsonl
```

## Candidate memory from run 28460740781

- raw shard-best curves at the normal preservation threshold `covered_count >= 56`: `20`
- all raw shard-best curves were `59/64`
- exact unique `vertices2` curves among the 20: `5`
- compact bank additions saved: `5`
- exact IDs new relative to run `28404861374` additions: `4`
- original shard-best index records saved: `20`

`candidates/bank.jsonl` was not merged in this step. The run-level additions were saved separately in `candidates/bank-additions-run28460740781.jsonl`.

## Dominant missing patterns from run 28460740781

- 14 / 20: `(0,1,2)`, `(1,2,1)`, `(1,3,2)`, `(2,1,3)`, `(2,2,2)`
- 6 / 20: `(1,2,2)`, `(2,0,2)`, `(2,0,3)`, `(3,1,0)`, `(3,1,2)`

## Top recurring missing points

- `(0, 1, 2)`: 14 / 20
- `(1, 2, 1)`: 14 / 20
- `(1, 3, 2)`: 14 / 20
- `(2, 1, 3)`: 14 / 20
- `(2, 2, 2)`: 14 / 20
- `(1, 2, 2)`: 6 / 20
- `(2, 0, 2)`: 6 / 20
- `(2, 0, 3)`: 6 / 20
- `(3, 1, 0)`: 6 / 20
- `(3, 1, 2)`: 6 / 20

## Comparison with previous frontier

Previous latest useful run was `28404861374`, also `59/64`, with `3` exact representatives and one dominant exact candidate appearing in `18 / 20` shard-best artifacts. This run again reached only `59/64`, but had `5` exact representatives and its dominant missing-set family appeared in `14 / 20` shard-best artifacts.

So the cache/anti-wall launch gave a real but modest structural improvement: it reduced collapse and produced four exact 59/64 IDs not already recorded in the previous run additions. But it still did not break the `59/64` wall.

## Current next step

Use the standard four-prompt web-chat cycle:

```text
1. record completed full-run results;
2. make and locally sanity-check a new hypothesis;
3. prepare the next GitHub launch, with smoke-test only as a technical gate;
4. wrap up and update memory.
```

Do not immediately launch another identical `smart-search-13-cover-stitch-cache` full run with the same seed and modes.

Do not create an extra mandatory step to record a green smoke-test. If the user already saw a green smoke-test and launched the 5h+ full run, the next result-taking prompt should record that full run. Smoke-test should be inspected separately only if it failed, looked suspicious, or the user explicitly asks for it.

Prepared workflow details:

```text
workflow: smart-search-14-rich-cover-stitch
workflow file: .github/workflows/smart-search-14-rich-cover-stitch.yml
plan file: docs/smart-search-14-rich-cover-stitch-plan.md
engine generator: scripts/prepare_rich_cover_stitch_engine.py
summary artifact: rich-cover-stitch-run-summary
shard artifacts: rich-cover-stitch-22-shard-*
```

Hypothesis for the prepared workflow:

```text
rich-cover -> endpoint-feasible stitch-compress
```

In simple words: first build richer 3-point and 4-point covering material, then stitch only through intervals whose chosen endpoints actually cover the intended grid points. This is intended to avoid another inherited 59-family repair loop.

Prepared smoke-test inputs were:

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
```

A useful full-run result is either any `60/64+` candidate with `links <= 22`, or a clearly new `59/64` family with weaker convergence than the `14/20` dominant wall from smart-search-13.
