# smart-search-15-rich-line-transition-60 plan

Prepared: 2026-07-02

## Why this is not another blind 59/64 rerun

The recorded frontier is still `59/64`: run `28522369532` completed `smart-search-14-rich-cover-stitch`, produced 20 shard-best curves, and all of them were `59/64`. It improved diversity but did not find `60/64`.

The new hypothesis starts from a local chat candidate that reached `60/64` with 22 links. This candidate is not a proof and not a recorded GitHub full-run result. It is seed material for the next controlled search.

Local seed:

- id: `mlct22-3cf45a2e21fe611c`
- links: `22`
- covered: `60/64`
- missing: `(0,0,1)`, `(0,2,3)`, `(0,3,1)`, `(2,1,1)`
- file: `data/search15/local_60_candidate_cover_first_stitch_cost.json`

## Hypothesis

Search around a rich-line transition skeleton instead of repairing old 59/64 curves.

Simple meaning:

1. Treat 3-point and 4-point grid lines as rich material.
2. Keep the real stitched segment between consecutive vertices as the source of truth.
3. Give strong pressure to the four remaining holes of the local `60/64` seed.
4. Preserve mode-separated shard results, missing patterns, and worker summaries so we can see whether rich-line ordering or weak bridges are blocking progress.

The goal is not only “find another final curve”. The run should also tell us whether the new `60/64` skeleton is a real gateway or just another saturated wall.

## Files

- Workflow: `.github/workflows/smart-search-15-rich-line-transition-60.yml`
- Generator: `scripts/prepare_rich_line_transition_engine.py`
- Local 60 seed: `data/search15/local_60_candidate_cover_first_stitch_cost.json`
- Candidate-bank addition: `candidates/bank-additions-local-60-chat-20260702.jsonl`

## Workflow checks

The workflow is manual only:

```yaml
on:
  workflow_dispatch:
```

There is no `push` trigger.

Control checks:

- known 23-link construction: `python scripts/check_trail.py data/ripa_23_trail.json --expected-links 23 --require-full`
- local 60 seed: `python scripts/check_scaled_trail.py data/search15/local_60_candidate_cover_first_stitch_cost.json --expect-covered 60 --max-links 22`

Engine build:

```bash
python scripts/prepare_rich_line_transition_engine.py --out build/rich_line_transition_search.cpp
g++ -O3 -std=c++17 -pthread -DNDEBUG build/rich_line_transition_search.cpp -o rich_line_transition_search
```

Shard checker:

```bash
python scripts/check_scaled_trail.py results/rich_line_transition/rich_line_transition_best_shard_${shard}.json --max-links 22
```

Shard artifacts:

```text
rich-line-transition-22-shard-0
...
rich-line-transition-22-shard-19
```

Aggregation:

```text
download pattern: rich-line-transition-22-shard-*
summary artifact: rich-line-transition-run-summary
script: python scripts/build_smart_summary.py
```

## Mode layout

- `0-4`: `local60_lns` — large-neighborhood pressure around the local `60/64` seed.
- `5-8`: `rich_line_transition` — fresh rich-line transition walks.
- `9-12`: `missing4_pressure` — direct pressure on the four holes of the local 60.
- `13-15`: `weak_bridge_surgery` — allow weak bridges if they connect rich lines.
- `16-17`: `skeleton_novelty` — push away from old 59-wall skeletons.
- `18`: `integer_line_control` — integer-coordinate control.
- `19`: `old59_vs_60_control` — old-family control seeded with the new 60.

## Smoke-test inputs

Use this first:

```text
Workflow: smart-search-15-rich-line-transition-60
seconds: 180
threads: 4
seed: 20260706
min_covered_to_save: 56
latest_run_id: 28522369532
previous_cover_stitch_run_id: 28460740781
previous_diversity_run_id: 28404861374
```

Smoke-test is a technical gate only. It should pass the known 23 check, the local 60 seed check, compile the generated C++ engine, run all 20 shards, upload 20 shard artifacts, and upload `rich-line-transition-run-summary`.

A good smoke result is at least `60/64`, because the local seed is saved in `data/search15`.

## Full-run inputs after green smoke

Use the same workflow and same seed:

```text
Workflow: smart-search-15-rich-line-transition-60
seconds: 21000
threads: 4
seed: 20260706
min_covered_to_save: 56
latest_run_id: 28522369532
previous_cover_stitch_run_id: 28460740781
previous_diversity_run_id: 28404861374
```

Expected scale: `20` shards/jobs, `max-parallel: 20`, `4` threads per shard.

## What counts as success

Strong success:

- any `61/64+` with `links <= 22`;
- especially `64/64`.

Useful result even without improvement:

- many independent `60/64` variants;
- clear missing-pattern data around the four local-60 holes;
- mode-separated evidence showing whether weak bridge search, missing-4 pressure, or rich-line ordering is the blocker.

Do not record the smoke as the new frontier. Record only the full run after it finishes.
