# smart-search-8-orbit-bridge full run analysis

Run: `28304497479`  
Workflow: `smart-search-8-orbit-bridge`  
Run URL: https://github.com/Grisha-Pochuev/minimum-link-covering-trail-4x4x4/actions/runs/28304497479  
Head SHA: `bd5630200cec8e3338435a18ac1d9974e864d63e`  
Status: `success`  
Result type: heuristic search, not a proof.

## Parameters

- seconds per shard: `21000`
- threads per shard: `4`
- shards/jobs: `20`
- max parallel jobs: `20`
- seed: `20260629`
- prior run id: `28292425390`
- old 59 run id: `28275850889`
- secondary run id: `28275666411`
- base repair run id: `28200925016`
- min covered to save: `56`

The workflow ran the full 20-job orbit-bridge search, not only a 180-second smoke-test. The old artifact download step, C++ generation, compilation, shard execution, checker, artifact upload, and aggregation all completed successfully.

## Best result

Best selected candidate from this run:

- candidate id: `mlct22-9c80a2741db704ad`
- covered_count: `59 / 64`
- links: `22`
- mode: `subcube_stitch22`
- source artifact: `orbit-bridge-22-shard-10`
- source shard: `10`
- status: `partial_candidate`
- missing count: `5`

Missing points:

```text
(0, 2, 2)
(2, 1, 3)
(2, 2, 3)
(3, 1, 0)
(3, 1, 2)
```

This does not improve the numeric frontier beyond `59/64`, but it gives a different useful 59/64 defect orbit.

## Result counts

- 20 shard-best candidates were collected.
- All 20 reached `59/64` with 22 links.
- There were 3 canonical unique candidate families in this run.
- Total attempts reported by shard JSON files: `10,304,271,511`.
- Approximate total attempt rate over the 20 jobs: `24534` attempts/second.

## Dominant missing patterns

- 11 / 20: (0,2,2), (2,1,3), (2,2,3), (3,1,0), (3,1,2)
- 7 / 20: (1,0,1), (1,2,2), (1,3,2), (2,0,3), (2,2,2)
- 2 / 20: (1,2,1), (2,1,2), (2,2,3), (3,1,0), (3,1,3)

## Top recurring missing points

- (2, 2, 3): 13 / 20
- (3, 1, 0): 13 / 20
- (0, 2, 2): 11 / 20
- (2, 1, 3): 11 / 20
- (3, 1, 2): 11 / 20
- (1, 0, 1): 7 / 20
- (1, 2, 2): 7 / 20
- (1, 3, 2): 7 / 20
- (2, 0, 3): 7 / 20
- (2, 2, 2): 7 / 20
- (1, 2, 1): 2 / 20
- (2, 1, 2): 2 / 20
- (3, 1, 3): 2 / 20

## Mode behavior

- `fractional_bridge22`: 5 result(s), best `59/64`, shards `[5, 6, 7, 8, 9]`.
- `integer_control22`: 1 result(s), best `59/64`, shards `[19]`.
- `repair56_target8`: 3 result(s), best `59/64`, shards `[15, 16, 17]`.
- `rich_segment_catalog`: 1 result(s), best `59/64`, shards `[18]`.
- `subcube_stitch22`: 5 result(s), best `59/64`, shards `[10, 11, 12, 13, 14]`.
- `transition_penalty22`: 5 result(s), best `59/64`, shards `[0, 1, 2, 3, 4]`.


All modes that ran reached `59/64`; no mode produced `60/64` or `64/64`.

## Comparison with previous frontier

Previous selected frontier from run `28292425390` missed:

```text
(0,1,0), (1,2,3), (2,1,0), (3,1,1), (3,1,3)
```

This run's selected best misses:

```text
(0,2,2), (2,1,3), (2,2,3), (3,1,0), (3,1,2)
```

The most important mathematical signal is that the old shared hard point `(3,1,3)` was no longer dominant: it appears only in 2/20 shard-best results here. The orbit-bridge idea did what it was supposed to do locally, but the obstruction moved to new 5-point patterns, especially the pattern appearing 11/20.

## Files saved

- `runs/2026-06-28-smart-search-8-orbit-bridge-full/summary.md`
- `runs/2026-06-28-smart-search-8-orbit-bridge-full/summary.json`
- `runs/2026-06-28-smart-search-8-orbit-bridge-full/best_candidate.json`
- `runs/2026-06-28-smart-search-8-orbit-bridge-full/unique_candidates.jsonl`
- `candidates/mlct22-9c80a2741db704ad-run28304497479.json`
- `candidates/bank-additions-run28304497479.jsonl`
- `candidates/bank-additions-run28304497479.summary.json`
- `candidates/originals/run-28304497479-smart-search-8-orbit-bridge.jsonl`

## Recommendation

Do not repeat `smart-search-8-orbit-bridge` unchanged. The next useful step is a new targeted repair run, tentatively `smart-search-9-new-defect-repair`, using this run's A/B defect patterns as the main target while keeping `(3,1,3)` only as a control pressure point.
