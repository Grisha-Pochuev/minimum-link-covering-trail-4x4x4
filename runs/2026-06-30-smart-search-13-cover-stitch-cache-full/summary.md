# smart-search-13-cover-stitch-cache — run 28460740781

Recorded: 2026-07-01

Run URL: https://github.com/Grisha-Pochuev/minimum-link-covering-trail-4x4x4/actions/runs/28460740781

Workflow: `smart-search-13-cover-stitch-cache`
Workflow file: `.github/workflows/smart-search-13-cover-stitch-cache.yml`
Head SHA: `2912b39896255e069bce0a544cf5d32ff4fbb71f`
Status: `success`
Result type: heuristic search, not a proof.

## Parameters

```text
seconds per shard: 21000
threads per shard: 4
seed: 20260704
min_covered_to_save: 56
shards/jobs: 20
max-parallel: 20
```

The run passed the known 23-link control and produced 20 shard-best artifacts plus `cover-stitch-cache-run-summary`.

## Best result

- candidate id: `mlct22-1c8736b46b59a730`
- covered_count: `59 / 64`
- links: `22`
- mode: `stitch_with_transposition`
- source artifact: `cover-stitch-cache-22-shard-6`
- status: `partial_candidate`
- missing count: `5`
- missing:
  - `(0, 1, 2)`
  - `(1, 2, 1)`
  - `(1, 3, 2)`
  - `(2, 1, 3)`
  - `(2, 2, 2)`

The best candidate was checked locally with the same exact scaled checker logic as `scripts/check_scaled_trail.py`: `59/64`, `22` links.

## Candidate memory

- raw shard-best curves: `20`
- all raw shard-best curves were: `59/64`
- exact unique `vertices2` representatives inside this run: `5`
- compact run-level bank additions saved: `5`
- exact IDs new relative to the already recorded run `28404861374` additions: `4`
- original shard-best index records saved: `20`

The duplicate exact ID from the previous recorded additions is `mlct22-1c8736b46b59a730`. It reappeared strongly here, but the run also produced four exact 59/64 IDs not recorded in `candidates/bank-additions-run28404861374.jsonl`.

## Missing-set patterns

- `14 / 20`: `(0,1,2)`, `(1,2,1)`, `(1,3,2)`, `(2,1,3)`, `(2,2,2)`
- `6 / 20`: `(1,2,2)`, `(2,0,2)`, `(2,0,3)`, `(3,1,0)`, `(3,1,2)`

Top recurring missing points:

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

## Cache/anti-wall mechanisms

The new fields were active:

- total attempts: `17496566206`
- total `cache_rejects`: `6322767189`
- total `wall_rejects`: `5541198435`

This confirms that the cache and anti-wall machinery was running, not just compiled.

## Comparison with previous frontier

Previous recorded full run `28404861374` also had best `59/64`. It had only `3` exact `vertices2` representatives and one dominant exact curve in `18 / 20` shard-best artifacts.

This run did not improve the numeric frontier, but it improved exact run-level diversity from `3` to `5` representatives and weakened the single-wall collapse from `18 / 20` to `14 / 20`. That is useful, but still not a breakthrough: no `60/64` candidate appeared.

## Conclusion for the next step

The cache/anti-wall idea is validated technically and gives some extra diversity, but it still remains trapped at the 59/64 frontier. The next step should not be a same-seed rerun. A stronger unordered cover-set / stitch-compress engine, or a generator that searches new skeletons before inheriting old 59-families, is now more justified than more tuning of the same repair loop.
