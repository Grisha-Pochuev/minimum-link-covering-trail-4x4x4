# smart-search-16-defect-relay-60 plan

Recorded: 2026-07-03

## Purpose

The latest recorded full GitHub run, `28618565146`, raised the official frontier from `59/64` to `60/64`, but all 20 shard-best outputs collapsed to the same compact representative and the same four missing points:

```text
(0,0,1), (0,2,3), (0,3,1), (2,1,1)
```

This package is not a same-seed rerun of `smart-search-15-rich-line-transition-60`. It prepares a defect-relay search: first create multiple independent `60/64` skeletons with different missing sets, then try to push those families to `61/64+`.

## Hypothesis

A local two-vertex window replacement around the official `60/64` seed can preserve `60/64` while moving the four-hole defect. That suggests the wall is not completely fixed; it may be possible to walk through a graph of different `60/64` skeletons and find a family that can be pushed to `61/64+`.

## New local relay seed

Official end window:

```text
[2,6,6] -> [6,2,6] -> [6,2,2] -> [6,8,2]
```

Local relay window:

```text
[2,6,6] -> [0,6,2] -> [6,0,2] -> [6,8,2]
```

Observed effect:

```text
old missing: (0,0,1), (0,2,3), (0,3,1), (2,1,1)
new missing: (0,0,1), (0,2,3), (2,2,3), (3,1,2)
```

This does not solve the problem. It is search fuel showing that `60/64` can be preserved while changing the defect family.

## Files in this package

```text
data/search16/official_60_seed_run28618565146.json
data/search16/local_relay60_window2_seed.json
data/search16/old59_seed_bank_run28522369532.jsonl
candidates/bank-additions-local-relay60-chat-20260703.jsonl
scripts/prepare_defect_relay_engine.py
scripts/build_defect_relay_summary.py
docs/proposed-smart-search-16-defect-relay-60.yml
.github/workflows/smart-search-16-defect-relay-60.yml  # if the connector could create it
```

## Shard layout

```text
0-3   window2_relay_from_official60
4-7   window3_relay_from_official60
8-10  old59_to_relay60
11-13 mixed bank relay, implemented through the window2 relay scoring core
14-17 relay_then_push61
18    integer_control
19    old60_and_local_relay_control
```

## Seed sources

```text
latest_run_id: 28618565146
previous_frontier_run_id: 28522369532
previous_cover_stitch_run_id: 28460740781
previous_diversity_run_id: 28404861374
```

Search input directories:

```text
data/search16
seed-material/from-candidate-bank
runs/2026-07-03-smart-search-15-rich-line-transition-60-full
runs/2026-07-01-smart-search-14-rich-cover-stitch-full
runs/2026-06-30-smart-search-13-cover-stitch-cache-full
runs/2026-06-30-smart-search-12-skeleton-diversity-full
```

Candidate-bank export sources:

```text
candidates/bank.jsonl
candidates/bank-additions-local-relay60-chat-20260703.jsonl
candidates/bank-additions-run28618565146.jsonl
candidates/bank-additions-run28522369532.jsonl
candidates/bank-additions-run28460740781.jsonl
candidates/bank-additions-run28404861374.jsonl
```

## Controls

The workflow must pass three controls before search shards run:

```text
python scripts/check_trail.py data/ripa_23_trail.json --expected-links 23 --require-full
python scripts/check_scaled_trail.py data/search16/official_60_seed_run28618565146.json --expect-covered 60 --max-links 22
python scripts/check_scaled_trail.py data/search16/local_relay60_window2_seed.json --expect-covered 60 --max-links 22
```

These are technical checks only. They are not proof of a solution.

## Artifacts

Shard artifact pattern:

```text
defect-relay-22-shard-*
```

Summary artifact:

```text
defect-relay-run-summary
```

Per-shard output paths:

```text
results/defect_relay/defect_relay_best_shard_<shard>.json
results/defect_relay/relay60_candidates_shard_<shard>.jsonl
results/defect_relay/diverse_candidates_shard_<shard>.jsonl
results/defect_relay/missing_patterns_shard_<shard>.json
```

Aggregator outputs:

```text
collected/defect_relay_run_summary.json
collected/defect_relay_run_summary.md
collected/relay60-diversity.jsonl
```

## Success criteria

Strong success:

```text
61/64 or better with links <= 22
```

Medium success:

```text
at least 5 unique compact representatives with covered_count = 60
and at least 3 different missing sets
```

Weak but useful success:

```text
no 61/64, but a visible relay graph of different 60/64 missing families
```

Failure:

```text
all or almost all shard-bests collapse again to mlct22-3cf45a2e21fe611c
with missing set (0,0,1), (0,2,3), (0,3,1), (2,1,1)
```

## Smoke-test inputs

```text
seconds: 180
threads: 4
seed: 20260716
min_covered_to_save: 56
min_relay_covered_to_save: 60
latest_run_id: 28618565146
previous_frontier_run_id: 28522369532
previous_cover_stitch_run_id: 28460740781
previous_diversity_run_id: 28404861374
max_links: 22
```

## Full-run inputs after green smoke

```text
seconds: 21000
threads: 4
seed: 20260716
min_covered_to_save: 56
min_relay_covered_to_save: 60
latest_run_id: 28618565146
previous_frontier_run_id: 28522369532
previous_cover_stitch_run_id: 28460740781
previous_diversity_run_id: 28404861374
max_links: 22
```
