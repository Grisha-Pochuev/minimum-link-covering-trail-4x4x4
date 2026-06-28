# smart-search-9-new-defect-repair full run analysis

Run: `28327372242`  
Workflow: `smart-search-9-new-defect-repair`  
Run URL: https://github.com/Grisha-Pochuev/minimum-link-covering-trail-4x4x4/actions/runs/28327372242  
Head SHA: `23ed729adbed07ca1dd4983f2de20276383bc633`  
Status: `success`  
Result type: heuristic search, not a proof.

## Parameters

- seconds per shard: `21000`
- threads per shard: `4`
- shards/jobs: `20`
- max parallel jobs: `20`
- seed: `20260630`
- prior run id: `28304497479`
- previous core5 run id: `28292425390`
- old 59 run id: `28275850889`
- secondary run id: `28275666411`
- base repair run id: `28200925016`
- min covered to save: `56`

The workflow ran the full 20-job new-defect repair search. The 23-link control, artifact downloads, candidate-bank export, C++ generation, compilation, shard execution, checker, artifact upload, and aggregation completed successfully.

## Best result

- candidate id: `mlct22-a495eb7a0c4f489d`
- covered_count: `59 / 64`
- links: `22`
- mode: `transition_penalty22`
- source artifact: `new-defect-22-shard-0`
- source shard: `0`
- status: `partial_candidate`
- missing count: `5`

Missing points:

```text
(1, 2, 2)
(1, 3, 1)
(1, 3, 2)
(2, 0, 2)
(2, 0, 3)
```

This does not improve the numeric frontier beyond `59/64`, but it gives a new useful 59/64 defect family.

## Result counts

- 20 shard-best candidates were collected in the summary artifact.
- All 20 reached `59/64` with 22 links.
- No shard reached `60/64` or `64/64`.
- The dominant saved compact family appeared in `12 / 20` shard-best results.

## Dominant missing patterns

- 12 / 20: `(1,2,2)`, `(1,3,1)`, `(1,3,2)`, `(2,0,2)`, `(2,0,3)`
- 4 / 20: `(0,2,2)`, `(2,1,3)`, `(2,2,3)`, `(3,1,0)`, `(3,1,2)`
- 3 / 20: `(0,0,2)`, `(1,2,3)`, `(2,0,1)`, `(2,1,0)`, `(3,1,1)`
- 1 / 20: `(1,3,1)`, `(2,1,2)`, `(2,2,3)`, `(3,1,0)`, `(3,1,3)`

## Top recurring missing points

- `(1, 3, 1)`: 13 / 20
- `(1, 2, 2)`: 12 / 20
- `(1, 3, 2)`: 12 / 20
- `(2, 0, 2)`: 12 / 20
- `(2, 0, 3)`: 12 / 20
- `(2, 2, 3)`: 5 / 20
- `(3, 1, 0)`: 5 / 20
- `(0, 2, 2)`: 4 / 20
- `(2, 1, 3)`: 4 / 20
- `(3, 1, 2)`: 4 / 20
- `(0, 0, 2)`: 3 / 20
- `(1, 2, 3)`: 3 / 20
- `(2, 0, 1)`: 3 / 20
- `(2, 1, 0)`: 3 / 20
- `(3, 1, 1)`: 3 / 20
- `(2, 1, 2)`: 1 / 20
- `(3, 1, 3)`: 1 / 20

## Mode behavior

- `transition_penalty22`: 4 result(s), best `59/64`, shards `[0, 1, 2, 3]`.
- `fractional_bridge22`: 4 result(s), best `59/64`, shards `[4, 5, 6, 7]`.
- `subcube_stitch22`: 4 result(s), best `59/64`, shards `[8, 9, 10, 11]`.
- `repair56_target8`: 4 result(s), best `59/64`, shards `[12, 13, 14, 15]`.
- `rich_segment_catalog`: 2 result(s), best `59/64`, shards `[16, 17]`.
- `integer_control22`: 2 result(s), best `59/64`, shards `[18, 19]`.

## Comparison with previous frontier

Previous selected frontier from run `28304497479` missed:

```text
(0,2,2), (2,1,3), (2,2,3), (3,1,0), (3,1,2)
```

This run's selected best misses:

```text
(1,2,2), (1,3,1), (1,3,2), (2,0,2), (2,0,3)
```

The numeric frontier did not move, but the obstruction moved. The search repaired the old A/B target pressure enough to expose a new D-family concentrated around the `y=3` layer and the `(2,0,2)/(2,0,3)` bridge area.

## Recommendation

Do not launch another full GitHub run immediately. First do a local chat preflight: compare this D-family champion with the previous A-family champion and test 4-12 link surgery aimed at closing `(1,3,1)`, `(1,3,2)`, `(2,0,2)`, and `(2,0,3)` without recreating the previous A-family defect set.
