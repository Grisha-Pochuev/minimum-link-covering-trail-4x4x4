# smart-search-17-cover64-stitch-graph full run — results

Run URL: https://github.com/Grisha-Pochuev/minimum-link-covering-trail-4x4x4/actions/runs/28825060197

Recorded: 2026-07-07

## Run metadata

- workflow: `smart-search-17-cover64-stitch-graph`
- run id: `28825060197`
- head commit: `5adc2b0d1efe0d89f324c758e44bd23e24d18d28`
- status: `success`
- run type: full `cover64 stitch graph` scaffold search
- seconds per shard: `21000`
- workers per shard: `4`
- shards/jobs: `20`
- seed: `20260717`
- max lines: `22`
- endpoint box: `[-1, 4]`
- max universe: `9000`
- artifacts: `cover64-stitch-run-summary`, `cover64-stitch-22-shard-*`

This run searches unordered 22-line cover/stitch scaffolds. It does **not** certify a polygonal trail by itself. Outputs must stay in the line-set scaffold bank until a separate ordered-trail reconstruction/check converts them into valid consecutive links.

## Main result

Best scaffold:

- candidate id: `mlct22-lineset-9772981a21b2a88a`
- covered_count: `64 / 64`
- line_count: `22`
- stitch graph: components=`1`, max_component=`22/22`, path_lower_bound=`22/22`, edges=`23`
- mode: `old_wall_line_injection`
- source shard: `12`
- source artifact: `cover64-stitch-22-shard-12`
- compact key: `02e5eb682b758d3ca9d6f1773c3227cf8b1a38671e1ca32bc8106cc1e7299fab`
- status: `line_set_seed_not_a_trail`

Interpretation: this is a major scaffold result. Compared with the local search-17 seed, the scaffold frontier moved from `64/64` coverage with stitch lower bound about `18/22` and `2` components to `64/64` coverage with stitch lower bound `22/22` and `1` component. It is still not a verified ordered 22-link trail.

## Aggregation counts

- aggregator `result_count`: `40`
- aggregator `cover64_count`: `40`
- persisted compact candidate rows in `cover64-stitch-candidates.jsonl`: `20`
- unique compact line-sets: `20`
- shard-best / useful shard rows represented: `20` shards
- missing points among saved rows: none; all persisted rows cover `64/64` as unordered line-sets
- stitch path histogram from aggregator: `22: 8, 21: 26, 20: 6`

The difference between `result_count=40` and the saved JSONL row count `20` is aggregation compaction: the summary counted raw best/preferred inputs, while the saved candidate file preserved one compact representative per shard/compact line-set.

## Mode breakdown

- `component_bridge_pressure`: rows=8, cover64=8, best_stitch=22, compact=4
- `cover64_from_seed_rewire`: rows=8, cover64=8, best_stitch=22, compact=4
- `cover64_stitch_connectivity_pressure`: rows=8, cover64=8, best_stitch=21, compact=4
- `old_wall_line_injection`: rows=8, cover64=8, best_stitch=22, compact=4
- `random_greedy_cover64_scaffold`: rows=8, cover64=8, best_stitch=22, compact=4

## Shard-best / compact representatives

| shard | candidate_id | mode | covered | stitch path | components | edges |
|---:|---|---|---:|---:|---:|---:|
| 0 | `mlct22-lineset-03bc99e72246b78c` | `cover64_from_seed_rewire` | 64/64 | 22/22 | 1 | 23 |
| 1 | `mlct22-lineset-5a64541e316bb358` | `cover64_stitch_connectivity_pressure` | 64/64 | 21/22 | 1 | 24 |
| 2 | `mlct22-lineset-559cbdc2a2a95238` | `old_wall_line_injection` | 64/64 | 20/22 | 1 | 26 |
| 3 | `mlct22-lineset-6cf49a59fb147a1a` | `random_greedy_cover64_scaffold` | 64/64 | 21/22 | 1 | 27 |
| 4 | `mlct22-lineset-15d092d623f52f52` | `component_bridge_pressure` | 64/64 | 21/22 | 1 | 28 |
| 5 | `mlct22-lineset-fe60c01c2882cd50` | `cover64_from_seed_rewire` | 64/64 | 20/22 | 1 | 26 |
| 6 | `mlct22-lineset-4e5f3521482e2c65` | `cover64_stitch_connectivity_pressure` | 64/64 | 21/22 | 1 | 25 |
| 7 | `mlct22-lineset-4d7b06ae4704e1e6` | `old_wall_line_injection` | 64/64 | 21/22 | 1 | 22 |
| 8 | `mlct22-lineset-5f42541323afebb6` | `random_greedy_cover64_scaffold` | 64/64 | 21/22 | 1 | 23 |
| 9 | `mlct22-lineset-a6e6659c4fafa344` | `component_bridge_pressure` | 64/64 | 20/22 | 1 | 30 |
| 10 | `mlct22-lineset-1277ec894815ccd2` | `cover64_from_seed_rewire` | 64/64 | 21/22 | 1 | 25 |
| 11 | `mlct22-lineset-8431ec991235a7d5` | `cover64_stitch_connectivity_pressure` | 64/64 | 21/22 | 1 | 24 |
| 12 | `mlct22-lineset-9772981a21b2a88a` | `old_wall_line_injection` | 64/64 | 22/22 | 1 | 23 |
| 13 | `mlct22-lineset-faadfe124b120444` | `random_greedy_cover64_scaffold` | 64/64 | 22/22 | 1 | 23 |
| 14 | `mlct22-lineset-1be28cb2ecff1025` | `component_bridge_pressure` | 64/64 | 21/22 | 1 | 26 |
| 15 | `mlct22-lineset-bddd1c013511e40a` | `cover64_from_seed_rewire` | 64/64 | 21/22 | 1 | 24 |
| 16 | `mlct22-lineset-4dd134e20958b436` | `cover64_stitch_connectivity_pressure` | 64/64 | 21/22 | 1 | 26 |
| 17 | `mlct22-lineset-d9407f842bc262e5` | `old_wall_line_injection` | 64/64 | 21/22 | 1 | 24 |
| 18 | `mlct22-lineset-daec8ad17149b45a` | `random_greedy_cover64_scaffold` | 64/64 | 21/22 | 1 | 27 |
| 19 | `mlct22-lineset-c52356383c1a0bd6` | `component_bridge_pressure` | 64/64 | 22/22 | 1 | 23 |

## Comparison with previous frontier

Previous recorded ordered-trail frontier:

- run id: `28674416173`
- best ordered-trail candidate: `60/64`, 22 links
- missing: `(0,0,1)`, `(0,2,3)`, `(0,3,1)`, `(2,1,1)`

New run:

- no new checked ordered-trail candidate;
- no change to the normal ordered-trail numeric frontier: still `60/64`;
- line-set scaffold frontier improved sharply: `64/64` unordered coverage and stitch-path lower bound `22/22` appeared in `4` compact representatives;
- all 20 compact representatives cover `64/64`; no defect-family/missing-point pattern remains at the scaffold level.

## What this means

The old ordered-trail wall was not simply “there are no 22 rich lines covering all points”. This run found many unordered 22-line scaffolds that cover all 64 grid points, and several are connected enough that the line-intersection stitch graph has a Hamiltonian-path lower bound of `22/22`.

The remaining hard part is stricter than the graph test: convert such a scaffold into an actual ordered polygonal trail, where consecutive links share the correct trail vertex and each chosen segment still covers the intended grid points.

## Next non-repeating step

Do not repeat search-17 with the same seed as the next serious step. The useful next step is a reconstruction workflow, e.g. `smart-search-18-order-from-cover64-stitch`, that takes the best `22/22` stitch scaffolds and tries to build a real ordered 22-link trail from them.

A useful reconstruction/checker should distinguish:

1. graph adjacency by shared covered grid point;
2. feasible consecutive segment endpoints in an actual polygonal chain;
3. whether shortening/splitting a line to use an intersection still preserves its covered points;
4. final exact `check_trail`-style validation as a 22-link polygonal trail.
