# Local preflight after smart-search-9

Run checked: `28327372242` / `smart-search-9-new-defect-repair`.

This file records the chat-side local preflight before any new expensive GitHub run. No GitHub Actions workflow was launched during this step.

## Artifact and candidate reconstruction

All 20 shard artifacts were downloaded and unpacked locally:

```text
new-defect-22-shard-0 ... new-defect-22-shard-19
```

Local exact coverage recomputation confirmed every shard-best JSON has:

```text
covered_count = 59 / 64
links = 22
```

Canonical deduplication over the 20 shard-best candidates produced `4` unique 59/64 families:

```text
12/20: mlct22-a495eb7a0c4f489d
       missing (1,2,2), (1,3,1), (1,3,2), (2,0,2), (2,0,3)

4/20:  mlct22-9c80a2741db704ad
       missing (0,2,2), (2,1,3), (2,2,3), (3,1,0), (3,1,2)

3/20:  mlct22-43721805eb17bb12
       missing (0,0,2), (1,2,3), (2,0,1), (2,1,0), (3,1,1)

1/20:  mlct22-04acd0b3f09fcfed
       missing (1,3,1), (2,1,2), (2,2,3), (3,1,0), (3,1,3)
```

Top recurring missing points:

```text
(1,3,1): 13/20
(1,2,2): 12/20
(1,3,2): 12/20
(2,0,2): 12/20
(2,0,3): 12/20
(2,2,3): 5/20
(3,1,0): 5/20
```

The previous result-saving commit had saved the dominant champion and frontier memory, but this local reconstruction shows the full compact layer should preserve all 4 unique families and the original archive should preserve all 20 shard-best rows.

## Mode behavior

```text
transition_penalty22: 4 shards, all 59/64, dominant D-family
fractional_bridge22: 4 shards, all 59/64, dominant D-family
subcube_stitch22: 4 shards, all 59/64, produced one C/control and one E-family
repair56_target8: 4 shards, all 59/64, dominant D-family
rich_segment_catalog: 2 shards, all 59/64, old A-family
integer_control22: 2 shards, all 59/64, old A-family
```

The useful signal is that smart-search-9 moved the obstruction again. It did not break `59/64`, but it exposed a new D-family. Repeating smart-search-9 unchanged is not justified.

## Local checks performed

Passed locally in the chat/container:

```text
python -m py_compile scripts/prepare_d_family_repair_engine.py
YAML parse for .github/workflows/smart-search-10-d-family-repair.yml
workflow static consistency: workflow_dispatch only, 20 shards, max-parallel 20
run_id consistency: prior_run_id=28327372242, orbit_bridge_run_id=28304497479
artifact-name consistency: d-family-22-shard-* and d-family-run-summary
JSON/JSONL parse for generated run, bank-additions, and originals files
coverage recomputation for all 20 original shard-best candidates
replacement-test for scripts/prepare_d_family_repair_engine.py on a small fake template
```

Not fully checked locally:

```text
Actual C++ generation from the real cpp/repair56_search.cpp and actual g++ compilation were not checked in the container because the repo could not be cloned from GitHub in this chat environment. The fake-template replacement test passed, but the real C++ compile must be checked by GitHub smoke-test.
```

## Chosen next hypothesis

Prepare `smart-search-10-d-family-repair`, but do not launch the full run directly.

Hypothesis:

```text
The next useful search should target the D-family wall exposed by run 28327372242, especially (1,3,1), (1,3,2), (2,0,2), and (2,0,3), while using the old A-family as a guardrail so the search does not merely rotate back to the previous obstruction.
```

## Preliminary GitHub smoke-test inputs

```text
workflow: smart-search-10-d-family-repair
seconds: 180
threads: 4
seed: 20260701
prior_run_id: 28327372242
orbit_bridge_run_id: 28304497479
previous_core5_run_id: 28292425390
old_59_run_id: 28275850889
secondary_run_id: 28275666411
base_repair_run_id: 28200925016
min_covered_to_save: 56
jobs/shards: 20
max-parallel: 20
```

## Preliminary full-run inputs after green smoke-test

```text
workflow: smart-search-10-d-family-repair
seconds: 21000
threads: 4
seed: 20260701
prior_run_id: 28327372242
orbit_bridge_run_id: 28304497479
previous_core5_run_id: 28292425390
old_59_run_id: 28275850889
secondary_run_id: 28275666411
base_repair_run_id: 28200925016
min_covered_to_save: 56
jobs/shards: 20
max-parallel: 20
expected wall time: about 5h50m per shard
```
