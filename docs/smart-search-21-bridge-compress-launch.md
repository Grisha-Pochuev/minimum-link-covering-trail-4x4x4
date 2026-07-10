# smart-search-21-bridge-compress launch

This package implements the already chosen bridge-compression hypothesis from the project specification.

## Mathematical target

Do not repeat search-20's fixed pattern of 14 full rich lines plus 8 explicit bridges. Search for exact 22-link ordered trails with:

- 16–18 rich or productive links;
- at most 6 pure bridges in full mode;
- local `4→3`, `5→4`, and `6→5` compression of the known 23-link full trail;
- one- and two-window repair of the official `60/64` trail;
- endpoint-aware simultaneous scaffold selection and ordering.

All coverage and collinearity checks use exact `fractions.Fraction` arithmetic. Candidates may contain integer, half-integer, or other rational vertices. A `64/64` candidate is checked by a second independently implemented verifier.

## Files

```text
.github/workflows/smart-search-21-bridge-compress.yml
.github/workflows/smart-search-21-bootstrap.yml
scripts/bridge_compress_common.py
scripts/bridge_compress_search.py
scripts/check_rational_trail.py
scripts/verify_rational_trail_independent.py
scripts/build_bridge_compress_summary.py
launch/smart-search-21-smoke.trigger
```

The main workflow supports `workflow_dispatch` with one normal input: `profile=smoke|full|custom`. The extra custom fields may remain blank for smoke/full.

Because the current connector does not expose GitHub's workflow-dispatch endpoint, the narrow bootstrap workflow exists only to launch the requested smoke/full runs from controlled trigger-file commits. It calls the same reusable main workflow; the serious workflow itself has no push trigger.

## Shard modes

| shards | mode |
|---:|---|
| 0–1 | `ripa_5to4_fixed` |
| 2–3 | `ripa_6to5_slide` |
| 4–5 | `ripa_outside_hub` |
| 6–7 | `official60_single_window` |
| 8–9 | `official60_double_window` |
| 10–11 | `official60_productive_bridge` |
| 12–13 | `scaffold_endpoint_zero_mutation` |
| 14–15 | `scaffold_endpoint_one_mutation` |
| 16–17 | `scaffold_endpoint_two_mutations` |
| 18 | `search20_control` |
| 19 | `mixed_compression` |

Seed rule:

```text
base seed = 20260721
effective shard seed = 20260721 + shard * 1000003
worker seed adds worker * 10007
```

## Effective smoke profile

```text
seconds=180
workers=4
beam_width=2048
state_cap=200000
candidate_lines=3000
start_limit=24
window_min=3
window_max=5
max_mutations=1
max_pure_bridges=7
target_min_rich_or_productive=14
save_min_covered=48
```

## Effective full profile

```text
seconds=21000
workers=4
beam_width=16000
state_cap=3000000
candidate_lines=8000
start_limit=64
window_min=3
window_max=6
max_mutations=2
max_pure_bridges=6
target_min_rich_or_productive=16
save_min_covered=56
```

Full mode uses 20 shards, four worker processes per shard, `max-parallel: 20`, and `timeout-minutes: 359`.

## Per-shard artifacts

```text
effective_profile_<shard>.json
best_candidate_<shard>.json
preferred_candidates_<shard>.jsonl
compression_report_<shard>.json
search_stats_<shard>.json
checkpoint_<shard>.json
```

The engine writes an atomic checkpoint after each computation block of at most five minutes.

## Aggregate artifact

```text
run_summary.json
summary.md
mode_breakdown.json
coverage_histogram.json
missing_point_frequency.json
bridge_count_histogram.json
compact_candidates.jsonl
ordinary_candidate_additions.jsonl
diagnostic_bridge_compress.jsonl
originals_index.jsonl
```

All 20 shard-best rows are preserved in the originals index. Compact candidates are deduplicated under all 48 cube symmetries and reversal of path order.

## Automatic launch sequence

1. Commit `launch/smart-search-21-smoke.trigger` containing `smoke` to start the smoke run.
2. Inspect all prechecks, shard jobs, exact checkers, aggregate job, and summary artifact.
3. Only after a green smoke run, commit `launch/smart-search-21-full.trigger` containing `full` to start the 5h50m run.
4. Do not delete the bootstrap or main workflow while either run is active.
