# smart-search-17-cover64-stitch-graph plan

## Hypothesis

The last two serious runs showed that repairing the same 60/64 ordered trail keeps collapsing to the old four-hole wall:

```text
(0,0,1), (0,2,3), (0,3,1), (2,1,1)
```

The new hypothesis is deliberately different:

> Do not search for a complete ordered 22-link trail immediately. First search for unordered 22-line sets that cover all 64 grid points and have a strong stitch/intersection graph. Then use those scaffolds as a bridge toward a real ordered trail.

This separates the problem into two layers:

1. **coverage layer** — can 22 rich lines cover all 64 points?
2. **stitch layer** — can those 22 lines be arranged into one connected polygonal trail?

The local web-chat check found a seed line-set with:

- `22` lines;
- `64/64` coverage;
- no zero-length lines;
- stitch path lower bound around `18/22`;
- stitch graph not yet good enough for a trail.

This seed is not a proof and not a valid solution. It is search fuel.

## Why this is not a repeat of smart-search-16

`smart-search-16-defect-relay-60` tried to repair/relay around the already known ordered 60/64 skeleton. It failed: all shard-best curves returned to the same missing family.

`smart-search-17-cover64-stitch-graph` changes the target object:

- old target: ordered 22-link trail, measured mainly by `covered_count`;
- new target: unordered 22-line scaffold, measured by `covered_count` and stitch-graph quality.

A good result is not only `60/64 -> 61/64`. A useful result can also be:

- many distinct `64/64` line-sets;
- a `64/64` line-set with stitch path `20/22` or `21/22`;
- a connected stitch graph with all 22 lines in one component;
- evidence that certain line-set covers cannot be stitched.

## Files

```text
data/search17/local_cover64_stitch_graph_seed.json
candidates/line-set-additions-local-cover64-stitch-chat-20260704.jsonl
scripts/check_cover64_line_set.py
scripts/search_cover64_stitch_graph.py
scripts/build_cover64_stitch_summary.py
docs/smart-search-17-cover64-stitch-graph-plan.md
docs/proposed-smart-search-17-cover64-stitch-graph.yml
.github/workflows/smart-search-17-cover64-stitch-graph.yml
```

## Workflow contract

```text
workflow: smart-search-17-cover64-stitch-graph
trigger: workflow_dispatch only
push trigger: no
shards/jobs: 20
max-parallel: 20
artifact per shard: cover64-stitch-22-shard-<shard>
summary artifact: cover64-stitch-run-summary
```

## Smoke-test inputs

```text
seconds: 180
workers: 4
seed: 20260717
min_covered_to_save: 64
min_stitch_path_to_save: 18
box_min: -1
box_max: 4
max_universe: 9000
max_lines: 22
latest_run_id: 28674416173
previous_frontier_run_id: 28618565146
```

## Full-run inputs after green smoke-test

```text
seconds: 21000
workers: 4
seed: 20260717
min_covered_to_save: 64
min_stitch_path_to_save: 18
box_min: -1
box_max: 4
max_universe: 9000
max_lines: 22
latest_run_id: 28674416173
previous_frontier_run_id: 28618565146
expected wall time: about 5h50m per shard
```

## Success criteria

Strong:

- a `64/64` line-set with stitch path lower bound `22/22`; or
- a `64/64` line-set with stitch path `21/22` and one clear local gap.

Medium:

- several distinct `64/64` line-sets with stitch path at least `20/22`;
- connected 22-line stitch graph with strong max component and high path lower bound.

Weak but useful:

- many distinct `64/64` line-sets with path `18/22` or `19/22`, giving raw material for a follow-up stitch repair.

Failure:

- no better scaffold than the local seed;
- repeated `64/64` line-sets but stitch graph stuck at disconnected/low-path forms.

## Important caveat

This workflow searches line-set scaffolds, not certified polygonal trails. A `64/64` line-set with a good stitch graph is not automatically a 22-link solution. It only becomes a solution candidate after a separate ordered-trail reconstruction/check.
