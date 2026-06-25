# repair-search-5 plan

This is the next prepared search mode after GitHub Actions run `28103660449`.

The old broad warm search repeatedly reached `56/64` but did not break the stable 8-point defect set. The next useful step is not another blind random walk. It is a targeted repair search.

## Main idea

Take known `56/64` candidates, especially the warm and targeted-warm candidates from run `28103660449`, and try local surgery:

- choose a window of 2--6 consecutive links;
- keep the rest of the trail fixed;
- replace the window with another path of the same length;
- score candidates by total coverage and by hits on the stable 8 missing points.

The C++ engine is intentionally separate from the older Python search. It should be faster per attempt and easier to run for 20 shards x 4 threads.

## Why this mode now

The mathematical notes say the current frontier is a `56/64` partial 22-link candidate with 8 stable missing points, and the useful direction is repair of the obstruction rather than restarting blind search.

This mode directly implements that idea.

## Current stable 8-point defect set

- `(1,0,0)`
- `(1,2,1)`
- `(1,2,2)`
- `(1,2,3)`
- `(2,0,1)`
- `(2,1,0)`
- `(3,0,2)`
- `(3,0,3)`

## Shard allocation

The C++ engine chooses mode by shard:

- shards `0..7`: `repair56_target8`
- shards `8..11`: `rich_segment_catalog`
- shards `12..14`: `transition_penalty22`
- shards `15..17`: `fractional_bridge22`
- shard `18`: `subcube_stitch22`
- shard `19`: `integer_control22`

## Local smoke-test result

During preparation, a short local smoke test of the C++ repair engine found a verified `57/64` candidate with 22 links. This is recorded under:

`experiments/2026-06-25-repair57-local-smoke/repair57_candidate.json`

This is not yet a full GitHub Actions run result. Treat it as a promising seed and an early confirmation that the local-repair direction is better than simply repeating warm search.

## How to run

Use workflow:

`.github/workflows/repair-search-5.yml`

For a smoke-test:

```text
seconds = 60
threads = 1 or 2
```

For a serious run:

```text
seconds = 21000
threads = 4
20 shards
max-parallel = 20
```

The workflow downloads artifacts from run `28103660449`, also reads the recorded local `57/64` seed, compiles the C++ engine, runs all shards, checks each result with `scripts/check_scaled_trail.py`, and uploads a `repair-run-summary` artifact.

## What to compare after the run

- Best coverage: old `56/64`, local smoke `57/64`, new Actions result `?/64`.
- Missing count: old `8`, local smoke `7`, new `?`.
- Does any mode reach `58/64` or better?
- Does the old 8-point obstruction change shape?
- Which repair windows produce real gains?
- Are the new defects merely shifted, or is the obstruction genuinely weaker?

Do not call this a proof. It is a sharper search mode and a seed generator for the next mathematical step.
