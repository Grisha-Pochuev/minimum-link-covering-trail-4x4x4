# Run 28103660449 — smart-search-4

This folder records the distilled memory from GitHub Actions run `28103660449`.

Run URL: https://github.com/Grisha-Pochuev/minimum-link-covering-trail-4x4x4/actions/runs/28103660449

## Basic metadata

- Repository: `Grisha-Pochuev/minimum-link-covering-trail-4x4x4`
- Workflow: `smart-search-4`
- Run id: `28103660449`
- Head commit SHA: `585556feb5c6bcc9dadc74b4ce875caad66ae481`
- Status: `success`
- Result type: heuristic search, not a proof
- Artifacts: `smart-run-summary`, `smart-22-shard-*`
- Result JSON files analyzed: `80` = 16 shard best files + 64 worker files

## Parameters

- seconds: `20400` per shard
- workers: `4` per shard
- top_k: `64`
- shards: `16`
- seed: `28103660449`
- prior run id: `28059258009`
- prior seed count: `9`
- coordinate scale: `2`
- prior best values seen by shards: `[56, 56, 56, 56, 56, 56, 56, 56]`
- total recorded shard attempts: `998236512`

## Best result

Best coverage stayed at:

```text
56 / 64 = 87.5%
```

The run did not find a full `64/64` covering trail.

The summary artifact selected:

- covered_count: `56 / 64`
- links: `22`
- mode: `targeted_warm22`
- file: `collected/smart_best_shard_6.json`
- status: `partial_candidate`

Important nuance: this was a tie. The `warm22` shards and the `targeted_warm22` shards repeatedly reached the same `56/64` defect pattern. So this run did not improve the numerical frontier, but it made the obstruction much clearer.

Best missing points:

  - `(1, 0, 0)`
  - `(1, 2, 1)`
  - `(1, 2, 2)`
  - `(1, 2, 3)`
  - `(2, 0, 1)`
  - `(2, 1, 0)`
  - `(3, 0, 2)`
  - `(3, 0, 3)`

## Top recurring missing points

Counted over all 80 result JSON files:

- `(1, 2, 3)`: 57 / 80
- `(3, 0, 2)`: 53 / 80
- `(2, 0, 1)`: 52 / 80
- `(1, 2, 1)`: 51 / 80
- `(1, 0, 0)`: 50 / 80
- `(1, 2, 2)`: 50 / 80
- `(3, 0, 3)`: 50 / 80
- `(2, 1, 0)`: 48 / 80
- `(1, 0, 1)`: 22 / 80
- `(3, 2, 3)`: 19 / 80
- `(3, 0, 1)`: 18 / 80
- `(0, 2, 2)`: 18 / 80
- `(0, 2, 0)`: 18 / 80
- `(1, 0, 3)`: 17 / 80
- `(1, 0, 2)`: 14 / 80
- `(0, 2, 3)`: 14 / 80
- `(1, 1, 2)`: 14 / 80
- `(2, 2, 1)`: 14 / 80
- `(3, 2, 0)`: 14 / 80
- `(3, 2, 2)`: 14 / 80

## Which modes worked best

- `targeted_warm22`: best 56/64, average 56.0/64 over 8 worker results; distribution {56: 8}
- `warm22`: best 56/64, average 56.0/64 over 24 worker results; distribution {56: 24}
- `layer_cube22`: best 48/64, average 46.38/64 over 8 worker results; distribution {45: 2, 46: 2, 47: 3, 48: 1}
- `integer22_control`: best 47/64, average 47.0/64 over 4 worker results; distribution {47: 4}
- `catalog22`: best 47/64, average 46.25/64 over 8 worker results; distribution {45: 2, 46: 2, 47: 4}
- `fractional22`: best 46/64, average 45.5/64 over 8 worker results; distribution {45: 4, 46: 4}
- `strict21`: best 41/64, average 40.75/64 over 4 worker results; distribution {40: 1, 41: 3}

Main reading:

- `warm22` and `targeted_warm22` are the only modes that consistently reach `56/64`.
- `targeted_warm22` did not break the 56 barrier, but it confirmed that the same 8-point defect set is very stable.
- `fractional22`, `catalog22`, `layer_cube22`, and `integer22_control` did not compete with warm-start search in this run.
- `strict21` is still far from the target and should remain reconnaissance only.

## What changed compared with the previous frontier

Previous analyzed smart run `28059258009`:

- best result: `56/64`
- best mode: `warm22`
- recurring defect map was already visible
- prior seed count used by the new run: `9`

This run `28103660449`:

- best result: still `56/64`
- best selected mode: `targeted_warm22`
- same 8 missing points were reproduced many times
- top missing point `(1,2,3)` appeared in `57/80` results
- the best defect set became stronger evidence for a structural obstruction, not just a random miss

So the run improved the research memory, but not the raw best coverage.

## Conclusions for the next run

The next run should not simply repeat the same warm-start search.

Recommended next direction:

1. Use artifacts of run `28103660449` as the seed source.
2. Keep `warm22` and `targeted_warm22` as the main high-value modes.
3. Put direct repair pressure on the stable 8-point defect set.
4. Try local surgery around weak links and around the transition regions that leave these 8 points uncovered.
5. Do not spend much budget on `strict21` yet.
6. Retune non-warm modes before treating them as serious competitors.
7. Preserve `vertices2` and `coordinate_scale = 2` compatibility.

## Next run seed source

The next serious run should start from GitHub Actions artifacts of run `28103660449`:

- first source to inspect: `smart-run-summary`;
- main warm-start source: all `smart-22-shard-*` artifacts;
- priority artifacts: `smart-22-shard-0` through `smart-22-shard-7`, because these are the warm and targeted warm shards that reached `56/64`.
