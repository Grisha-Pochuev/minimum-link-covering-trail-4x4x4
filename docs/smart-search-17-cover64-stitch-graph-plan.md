# smart-search-17-cover64-stitch-graph plan

## Why this is not a repeat

The last two useful full runs reached the same wall:

- run `28618565146`: first official GitHub `60/64`, but all shard-bests collapsed to one four-hole wall;
- run `28674416173`: defect-relay attempt, still `60/64`, no new 60-family diversity.

The repeated missing points are:

```text
(0,0,1), (0,2,3), (0,3,1), (2,1,1)
```

The new idea is different: stop asking the search to produce a valid ordered 22-link trail immediately. First search for an unordered 22-line skeleton that covers all 64 grid points, then optimize the graph of possible stitching between those 22 lines.

This is a bridge hypothesis:

```text
cover64 skeleton -> stitch graph -> ordered 22-link trail candidate
```

It is not a proof and not a final candidate format.

## Local preflight behind the package

Starting from the previous `60/64` candidate `mlct22-3cf45a2e21fe611c`, remove old line indices `3`, `12`, and `18`, then add these three hole-closing lines:

```text
(0,3,1) -> (1,2,1) -> (2,1,1) -> (3,0,1)
(0,0,1) -> (1,1,1) -> (2,2,1) -> (3,3,1)
(0,2,3) -> (1,1,2) -> (2,0,1)
```

In scaled `vertices2` coordinates:

```text
[0,6,2] -> [6,0,2]
[0,0,2] -> [6,6,2]
[0,4,6] -> [4,0,2]
```

This gives a 22-line unordered skeleton covering `64/64`. The hard part is still ordering/stitching it into one polygonal trail.

Saved seed:

```text
data/search17/cover64_stitch_seed.json
```

## Search target

Each shard searches 22 unordered line segments and scores:

1. `covered_count`, with strong priority for `64/64`;
2. old four-hole wall covered count;
3. overlap graph component size and greedy path length;
4. endpoint graph component size and greedy path length.

Definitions:

- `overlap graph`: two lines are adjacent if they share at least one covered grid point;
- `endpoint graph`: two lines are adjacent if the chosen finite segments share an endpoint.

This remains only a stitching proxy. A high overlap/endpoint path is not automatically a valid ordered trail, but it is much closer to the real obstruction than another raw `60/64` repair.

## Files

```text
cpp/cover64_stitch_graph_search.cpp
scripts/check_cover64_stitch_result.py
scripts/build_cover64_stitch_summary.py
data/search17/cover64_stitch_seed.json
docs/smart-search-17-cover64-stitch-graph-plan.md
docs/proposed-smart-search-17-cover64-stitch-graph.yml
.github/workflows/smart-search-17-cover64-stitch-graph.yml
```

## Workflow

```text
workflow: smart-search-17-cover64-stitch-graph
workflow_dispatch-only: yes
push trigger: no
seed check: python scripts/check_cover64_stitch_result.py data/search17/cover64_stitch_seed.json --expect-cover64 --max-lines 22
compile: g++ -O3 -std=c++17 -pthread -DNDEBUG cpp/cover64_stitch_graph_search.cpp -o cover64_stitch_graph_search
run: ./cover64_stitch_graph_search --seconds ... --threads ... --seed ... --shard ... --shards 20 --out results/cover64_stitch/cover64_stitch_best_shard_<shard>.json
checker: python scripts/check_cover64_stitch_result.py results/cover64_stitch/cover64_stitch_best_shard_<shard>.json --min-covered <min_covered_to_save> --max-lines 22
summary builder: python scripts/build_cover64_stitch_summary.py
shard artifacts: cover64-stitch-22-shard-*
summary artifact: cover64-stitch-run-summary
```

## Shard mode layout

```text
0-3    seed64_stitch_improve
4-7    overlap_stitch_pressure
8-11   endpoint_stitch_pressure
12-15  cover64_diversity
16-18  old60_escape_mix
19     seed64_control
```

## Success criteria

Strong:

- `covered_count = 64` and endpoint graph has path/component near `22/22`, suggesting a possible ordered trail reconstruction.

Medium:

- `covered_count = 64` and overlap graph path improves beyond the local preflight baseline by a visible margin.

Weak but useful:

- many distinct `64/64` skeletons with different stitch graph structures.

Failure:

- all shards remain at the seed-like `64/64` skeleton with poor endpoint/overlap path metrics.

## Exact inputs

Smoke-test:

```text
seconds: 180
threads: 4
seed: 20260717
min_covered_to_save: 63
```

Full run after green smoke:

```text
seconds: 21000
threads: 4
seed: 20260717
min_covered_to_save: 63
```

Expected wall time: about 5h50m per shard.
