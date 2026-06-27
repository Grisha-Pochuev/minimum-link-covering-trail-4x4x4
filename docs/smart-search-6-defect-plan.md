# smart-search-6-defect plan

Prepared on 2026-06-27.

## Starting point

This run must not start from zero. It starts from the latest useful completed frontier:

- run id: `28200925016`
- workflow: `repair-search-5`
- best: `58/64`, 22 links
- artifact set: `repair-run-summary`, `repair-22-shard-*`
- saved run memory: `runs/2026-06-26-repair-search-5/top_candidates.json`

The persistent defect after that run is the six-point set:

```text
(1,1,0), (1,2,1), (2,1,0), (3,1,1), (3,1,2), (3,1,3)
```

The hardest visible core is the vertical triple:

```text
(3,1,1), (3,1,2), (3,1,3)
```

## Seed material

The workflow uses three seed sources:

1. downloaded GitHub Actions artifacts from run `28200925016`;
2. saved run memory from `runs/2026-06-26-repair-search-5/`;
3. the unified curve bank `candidates/bank.jsonl`, exported into individual JSON files before the C++ engine starts.

The bank currently includes original strong curves from 56/64 upward, deduplicated so mirrored/reflected/coordinate-permuted/reversed copies are not treated as new candidates.

## Engine

The workflow generates a temporary C++ engine at runtime from `cpp/repair56_search.cpp` using:

```text
scripts/prepare_repair58_engine.py
```

The generated engine changes the weighted target defects from the old 56/64 missing pattern to the new 58/64 six-point defect pattern.

## 20-job strategy split

The 20 jobs are not identical. The generated engine allocates shard modes as:

- shards 0-5: `repair56_target8`
- shards 6-10: `transition_penalty22`
- shards 11-14: `fractional_bridge22`
- shards 15-17: `subcube_stitch22`
- shard 18: `rich_segment_catalog`
- shard 19: `integer_control22`

This follows the previous run: repair, transition penalty, fractional bridge, and subcube stitching were stronger; rich catalog and integer control remain as small alternative/control probes.

## Manual launch parameters

Smoke-test first:

```text
workflow: smart-search-6-defect
seconds: 90
threads: 4
seed: 20260627
prior_run_id: 28200925016
min_covered_to_save: 56
```

Full serious run after smoke-test passes:

```text
workflow: smart-search-6-defect
seconds: 21000
threads: 4
seed: 20260627
prior_run_id: 28200925016
min_covered_to_save: 56
```

`21000` seconds is 5h50m and leaves a small margin inside the GitHub runner limit for checking and artifact upload.
