# Exact handoff for `smart-search-24-defect-graft`

Status: selected Step-2 hypothesis and binding handoff for Step 3. **Launch is blocked until search-23 shard 11 finishes and the strict 20/20 search-23 aggregate and three banks are recorded.** Step 3 must first merge any additional search-23 core-escape seeds, then implement this handoff without reverting to generic core-transplant mutation.

## 1. Final name and primary question

Workflow name:

```text
smart-search-24-defect-graft
```

Required workflow path:

```text
.github/workflows/smart-search-24-defect-graft.yml
```

Primary question:

> Can an exact line through the two remaining holes be grafted into a search-23 `62/64` core-escape trail by replacing a zero-contribution bridge plus two or three weak supporting lines with exact connector lines, and then solving the resulting line-intersection ordering problem?

This is not another random endpoint repair and not another broad core-transplant run. It starts from the structural result of search-23 and turns the remaining problem into a focused line-graft and ordering problem.

## 2. Evidence from search-23 and local probes

The checked 19-shard portion of run `29249275103` produced:

- `1115` compact exact `62/64` classes;
- `40` exact `62/64` classes with frozen-core overlap `16/18`;
- all `40` came from shard `14`, the paired front-plus-middle transplant mode;
- `23` have the new missing pair `[(1,0,2),(3,3,1)]`;
- `17` have `[(0,2,1),(3,3,1)]`;
- `20` of the `40` contain a link whose finite segment covers zero grid points;
- the other `20` still contain one zero-exclusive link whose covered points are duplicated elsewhere.

Exact local probes performed in the web-chat environment:

1. **Defect-line substitution.** For every one of the `20` zero-point-bridge candidates, remove that bridge and insert the finite segment joining the two missing grid points. The resulting unordered set of exactly `22` finite segments covers `64/64` in all `20/20` cases.

2. **Why direct insertion fails.** After replacing the bridge by the defect line, the supporting-line intersection graph is disconnected in all `20` cases:
   - in `12`, the defect line has degree `0`;
   - in `8`, it has degree `2`, but both intersections lie in the same small left component;
   - therefore the same 22 supporting lines cannot simply be reordered into a trail.

3. **Single-vertex neighborhood is exhausted.** Every internal vertex of all `40` core-escape candidates was replaced exhaustively by every point in the bounded search-23 half-grid pool (`3700` points), for `40 * 21 * 3700 = 3,108,000` exact replacements. None exceeded `62/64`.

4. **Naive local graft is too small.** For all `20` zero-point-bridge candidates, forcing the defect line inside exact 3-link and 4-link rebuilt windows reached at most `57/64` and `59/64`, respectively. Exact 5-link meet-in-the-middle probes on eight strongest representatives also reached at most `59/64`.

5. **Simple link-budget compression fails.** Exhaustive exact `2 links -> 1 link` and `3 links -> 2 links` compressions over all `40` core-escape candidates reached at most `59/64`. There is no free local link budget obtainable by one simple compression.

6. **One extra rich connector is insufficient.** For all `20` zero-point-bridge candidates, weak secondary links with exclusive contribution at most one were replaced by every one of the `1492` supporting lines containing at least two grid points (`107,424` tested substitutions in total), while keeping the defect line. Sixteen line sets became connected, but every one had at least three degree-one vertices, so none could have a Hamiltonian path.

Conclusion from the probes:

```text
The defect line is exactly the missing coverage object.
The remaining obstacle is connector topology and finite-segment realization.
A one-line or one-vertex repair is too small.
The next smallest credible neighborhood is a three-line or four-line graft.
```

## 3. Authoritative inputs

After search-23 is fully recorded, persist before smoke:

```text
data/search24_core_escape62_seeds.jsonl
data/search24_defect_graft_manifest.json
```

The seed set must include:

1. every exact search-23 `62/64` candidate with frozen-core overlap `<=16`;
2. a flag for zero-point bridge and zero-exclusive link positions;
3. the two missing points and the exact defect-line key through them;
4. link masks, exclusive contribution counts, supporting-line keys and original order;
5. parent, donor, shard, worker and canonical class provenance;
6. at least one representative of each of the seven old search-22 defect families as controls.

Primary seeds are the zero-point-bridge candidates. Zero-exclusive nonzero-link candidates are the secondary seed family.

Do not depend on an expiring Actions artifact during full search.

## 4. Exact mathematical representation

Use exact arithmetic throughout:

- grid coverage: `uint64_t` mask;
- coordinates: reduced rationals, with a fast scaled-integer path when denominator divides `4`;
- supporting line: normalized exact direction and line invariant;
- line intersection: exact rational result or exact `parallel/skew/coincident` classification;
- trail: exactly `23` ordered vertices and `22` nonzero finite links;
- graph: one node per selected supporting line, edge only for exact intersection or exact coincident compatibility.

For each seed define the defect line `D` through the two missing grid points. A realized finite segment on `D` must span both missing points, not merely lie on the same infinite line.

## 5. Primary search operation: three-line defect graft

For a primary zero-point-bridge seed:

1. remove the zero-point bridge `P`;
2. choose two weak links `Q1,Q2`, initially with exclusive contribution `<=1`;
3. add the defect line `D`;
4. add two exact connector lines `C1,C2`;
5. retain exactly `22` supporting lines;
6. require exact `64/64` optimistic line/segment coverage before expensive ordering;
7. solve the exact line-intersection Hamiltonian-path problem;
8. realize the order as finite segments and check exact coverage.

The connector lines must be generated from finite exact attachment catalogs, not blind coordinate mutation. Candidate attachment points include:

- existing trail vertices;
- grid points and unique points of the removed weak links;
- exact intersections of retained parent/donor supporting lines;
- bounded rational points on `D` and retained lines with denominator at most `4`;
- productive one-point connector lines observed in search-21, search-22 and search-23 banks;
- connector lines through one exact point on `D` and one exact point on a retained component.

The two connectors should normally attach `D` to different components of the graph left after removing `P,Q1,Q2`.

## 6. Secondary operation: four-line defect graft

If three-line graft topology is exhausted or too restrictive:

- remove `P` plus three weak links;
- add `D` plus three connectors;
- allow exclusive contribution up to `2` only when the added connectors or retained segments recover the lost points exactly;
- use exact component and coverage bounds before ordering.

This is a controlled enlargement of the same hypothesis, not a separate search method.

## 7. Exact graph and ordering layer

For every candidate 64-cover line set:

1. build the exact intersection graph;
2. reject if disconnected;
3. reject if it has more than two degree-one vertices;
4. apply safe Hamiltonian-path necessary conditions, including articulation/component bounds;
5. warm-start from the original trail order with the grafted block inserted;
6. run exact branch-and-bound or subset dynamic programming on the sparse graph;
7. rank next nodes by preservation of original adjacency and finite-segment coverage;
8. store the first exact Hamiltonian support-line order, even if finite realization covers only `62/64` or `63/64`.

For a chosen line order, consecutive line intersections determine internal vertices. Handle coincident lines explicitly and reject zero-length links. Choose first and last endpoints so every intended grid point on the endpoint lines lies inside the finite segment.

If a Hamiltonian line order gives less than full finite-segment coverage, allow one bounded exact `4-8`-link realization repair while keeping `D` fixed and preserving the support order outside the repair window.

## 8. Safe pruning and scoring

Use lexicographic ranking:

1. exact finite-segment covered count;
2. exact `64/64` supporting-line-set coverage;
3. Hamiltonian support-line order found;
4. connected graph with at most two degree-one vertices;
5. fewer connected components before graft completion;
6. fewer removed exclusive points;
7. fewer substitutions;
8. more original adjacencies preserved;
9. lower frozen-core overlap and structural novelty.

Safe pruning:

- exact coverage union upper bound;
- exact component count;
- degree-zero and degree-one constraints;
- articulation/component necessary bounds for a Hamiltonian path;
- reject duplicate `(selected_line_set, endpoint_classes, covered_mask)` states under exact dominance;
- reject a removed-link choice if its exclusive points cannot be covered by `D`, connectors or retained lines;
- stop all workers immediately after a candidate passes both exact `64/64` verifiers.

Heuristic caches may prioritize but must not be described as proof-level exclusions.

## 9. Fixed 20-shard allocation

Use one mechanism with controlled depth variations:

```text
0-3    three-line graft, old-orbit zero-point-bridge seeds, four attachment-region partitions
4-7    three-line graft, new-orbit zero-point-bridge seeds, four attachment-region partitions
8-11   three-line graft, zero-exclusive nonzero-link seeds, four weak-link partitions
12-15  four-line graft, exclusive contribution cap 1/1/2/2
16     donor/productive-connector catalog expansion
17     deep Hamiltonian ordering on best exact 64-cover line sets found by all seed families
18     finite-segment realization and bounded 4-8-link repair after a Hamiltonian line order
19     exact ablation: defect line plus only one additional rich connector, recording the bounded negative classification
```

Every primary shard must process all applicable canonical seed classes, not only one champion.

## 10. Implementation architecture

Preferred:

- C++20 for line-set enumeration, exact graph filters, Hamiltonian ordering, finite-segment masks and four shared-memory workers;
- Python for seed materialization, two independent exact verifiers, aggregation and reports.

The C++ engine must use normal readable modules. Suggested layout:

```text
src/search24/common.hpp
src/search24/geometry.hpp
src/search24/graft_catalog.hpp
src/search24/graph_search.hpp
src/search24/realization.hpp
src/defect_graft_search.cpp
```

Unlike search-23, `state_cap` must be a real enforced bound and must be reported as reached/not reached. Keep bounded caches and periodic atomic checkpoints.

## 11. Shared preflight

Create one versioned entry point used both locally and in GitHub precheck, for example:

```text
scripts/preflight_search24.py
```

It must:

1. compile every C++ and Python source;
2. verify the known 23-link full control;
3. verify all search-24 seeds twice;
4. reproduce the search-23 structural counts after the final 20/20 merge;
5. reproduce the `20/20` zero-point-bridge to unordered `64/64` defect-line substitution result, updated if shard 11 adds seeds;
6. reproduce the disconnected direct-substitution graph diagnosis;
7. reproduce the bounded one-extra-rich-connector negative probe;
8. run every shard mode for `3-5` seconds;
9. run the real aggregate builder on miniature outputs;
10. confirm exactly 22 nonzero links in every emitted trail;
11. run `scripts/check_long_run_budget.py` with the final workflow parameters.

## 12. Profiles and operational safety

Smoke:

```text
seconds=180
shards=20
workers=4
max-parallel=20
checkpoint_seconds=60
```

Full:

```text
seconds=20400
timeout-minutes=359
minimum job headroom=900 seconds
shards=20
workers=4
max-parallel=20
checkpoint_seconds=600
```

The workflow must use the automatic chain:

```text
precheck -> smoke[20] -> smoke aggregate -> full[20] -> full aggregate
```

A failed or interrupted shard must still upload its latest atomic checkpoint and a failure report. The scientific aggregate remains strict and final only with every required shard artifact.

## 13. Required artifacts

Per shard:

```text
best_trail_<shard>.json
verified_62plus_<shard>.jsonl
cover64_line_sets_<shard>.jsonl
hamiltonian_line_orders_<shard>.jsonl
near_hamiltonian_graphs_<shard>.jsonl
graft_diagnostics_<shard>.jsonl
search_stats_<shard>.json
resource_usage_<shard>.json
checkpoint_<shard>.json
mode_manifest_<shard>.json
```

Aggregate:

```text
run_summary.json
summary.md
best_candidate.json
coverage_histogram.json
defect_orbit_breakdown.json
graft_size_breakdown.json
removed_weak_link_breakdown.json
connector_usage_breakdown.json
graph_component_histogram.json
degree_one_histogram.json
hamiltonian_order_report.json
finite_realization_report.json
exact_verification_report.json
ordinary_candidate_additions.jsonl
diagnostic_cover64_and_graph_states.jsonl
originals_index.jsonl
shard_best_originals.jsonl
```

Three banks:

1. ordinary: independently checked ordered trails at `62/64+`;
2. diagnostic: exact `64/64` line sets, Hamiltonian support orders, connected near-Hamiltonian graphs and `60/64-61/64` structurally novel graft states;
3. originals: raw worker/shard best ordered trails before symmetry compaction.

## 14. Success criteria

Numerical success:

- any independently exact `63/64` ordered trail;
- any independently exact `64/64` ordered 22-link trail.

Strong structural success if the numerical frontier remains `62/64`:

- first exact `64/64` selected line set whose intersection graph has a Hamiltonian path;
- first Hamiltonian support-line order realizing `63/64` or `64/64` finite coverage;
- an exact `62/64` trail containing the defect line and no zero-point bridge, with connector topology outside search-23;
- a complete bounded classification of the three-line graft neighborhood, with exact task counts and no missing shards.

## 15. Stop rules

- Do not launch search-24 until search-23 is strictly finalized and all final seeds are persisted.
- Do not rerun generic search-23 core mutation under a new number.
- Do not count an unordered `64/64` line set as an ordered trail.
- Do not count a Hamiltonian infinite-line order as success until finite segments are exactly realized and checked.
- Do not describe bounded graft failure as proof that no 22-link solution exists.
