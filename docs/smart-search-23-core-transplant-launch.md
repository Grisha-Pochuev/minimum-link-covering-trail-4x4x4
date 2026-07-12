# Exact handoff for `smart-search-23-core-transplant`

Status: selected Step-2 hypothesis. This document is the binding handoff to Step 3. Do not broaden it into an unrelated multi-method run.

## 1. Final name and files

Workflow name:

```text
smart-search-23-core-transplant
```

Required workflow path:

```text
.github/workflows/smart-search-23-core-transplant.yml
```

Use exactly one visible workflow for search number 23. The same workflow must contain precheck, smoke/full profiles, search shards, exact verification, aggregation and artifact upload.

Before adapting any search-22 code, refactor the fragment layout `scripts/endpoint_repair_parts/part-*.pyfrag` into normal importable Python modules or write the new search-23 engine as normal source files. Do not introduce a second fragment concatenation system.

## 2. Primary hypothesis

Full search-22 produced `1053` exact `62/64` classes, but all of them contain one identical 18-line supporting core. That core covers `58/64`; only four links vary and choose four of six residual points.

Shallow endpoint movement, one-vertex replacement, 2–3-link repair, bank crossover, symmetry-expanded crossover, 2-opt, 3-opt and simple defect-line insertion all failed to exceed `62/64`.

Primary hypothesis:

> Escaping the `62/64` wall requires replacing a larger block that contains at least one frozen-core line, and the stronger modes should replace at least two frozen-core lines. Structurally different `60/64–61/64` candidates should be used as donor geometry rather than discarded because of their lower coverage.

Search-23 is therefore a core-transplant search, not endpoint repair and not a blind reconstruction from scratch.

## 3. Authoritative inputs

### Search-22 full population

Source run:

```text
29181546758
```

Source artifact:

```text
smart-search-22-endpoint-repair-run-summary
```

Required source records:

```text
verified_62plus.jsonl          # exactly 1053 exact 62/64 candidates
compact_candidates.jsonl       # exactly 2385 compact 60/61/62 candidates
```

Because the Actions artifact expires, Step 3 must persist the necessary seed material in the repository before smoke, split into ordinary text parts if needed:

```text
data/search23_verified62_seed_parts/part-*.jsonlpart
data/search23_core_diverse_donors.jsonl
```

Do not depend on an expiring artifact during a future full run.

### Search-21 and full-control inputs

- run `29123493808`, search-21 compact `60/64–61/64` population;
- `data/ripa_23_trail.json`, exact complete 23-link control;
- the seven defect-pair representatives listed below;
- five core-diverse donors listed below.

### Seven required 62/64 representatives

Use at least one exact representative for every observed two-hole family:

```text
mlct22-er-1b9d545440a3ee2b
mlct22-er-44b7464ef2bba268
mlct22-er-763db4ef21aeba80
mlct22-er-7671ee46bd711a25
mlct22-er-592cdba87b09cf5e
mlct22-er-84b471c2367a34e7
mlct22-er-579fc6ba3b315bf0
```

### Required core-diverse donors

```text
mlct22-er-7617f3333d5bd4a7   # 61/64, frozen-core overlap 16
mlct22-er-222e6539aa735a14   # 60/64, overlap 2
mlct22-er-8636131b79055dbe   # 60/64, overlap 2
mlct22-er-6ea2d43af05081b7   # 60/64, overlap 2
mlct22-er-cf89ed8c63871970   # 60/64, overlap 2
```

The four overlap-2 donors must be expanded by cube symmetries and path reversal when generating transplant blocks.

## 4. Exact geometry representation

Use exact arithmetic for every final incidence and connectivity decision.

Recommended representation:

- grid coverage mask: one `uint64_t`;
- supporting line: normalized rational/integer direction plus exact line invariant;
- endpoint/junction coordinates: reduced rationals;
- line intersection: exact rational computation;
- trail state: exactly 23 ordered vertices and 22 nonzero links.

Precompute:

1. all useful supporting lines that contain at least two grid points;
2. productive one-point connector lines observed in search-21/search-22 seeds;
3. exact line-line intersection table;
4. coverage masks and line richness;
5. cube symmetries and path reversal;
6. the frozen 18-line core and each candidate's core-overlap count;
7. unique-contribution counts for every link.

Integer, half-integer and bounded small-denominator outside vertices are allowed. Broad unbounded fractional wandering is not part of this search.

## 5. Search operations

Every primary operation must alter a block that contains at least one frozen-core line. Strong modes must remove or change at least two frozen-core supporting lines.

### A. Contiguous core-window rebuild

Remove `4`, `5`, `6`, `7` or `8` consecutive links between two fixed anchors. Rebuild the same number of links using exact line junctions.

- length `4–6`: meet-in-the-middle or exact bounded enumeration;
- length `7–8`: beam/A* with exact coverage masks and admissible optimistic coverage bounds.

The replacement may use donor-derived supporting lines, catalog lines and new exact junctions.

### B. Paired disjoint transplant

Choose two disjoint windows whose total replaced length is `4–8` links. One window must touch the defect/variable region and the other must break the frozen core.

Search both repairs jointly so that a point lost in one place can be recovered by the other. This is different from search-22 paired endpoint movement: the units here are multi-link support-line blocks.

### C. Donor-block transplant

Extract contiguous blocks of `2–6` supporting lines from the core-diverse `60/64–61/64` donors, under all cube symmetries and reversal. Attempt to splice them into each of the seven `62/64` parent families, rebuilding boundary junctions exactly.

Do not require donor vertices to match parent vertices literally. Match by support lines, coverage masks, anchor compatibility and exact intersections.

### D. Support-line transplant and reorder

Replace one or two frozen-core lines with defect-hitting or donor lines, then search the induced exact line-intersection graph for a 22-line Hamiltonian ordering with high coverage.

The earlier simple one-line replacement failed. This mode must permit two interacting line replacements and a global or large-neighborhood reorder.

## 6. State, scoring and pruning

A state should contain at least:

```text
links_used
last supporting line / exact last junction
covered_mask
remaining fixed suffix information
frozen_core_overlap
parent id
donor id or donor block id
operation provenance
```

Use lexicographic ranking, not one opaque weighted scalar:

1. higher exact covered count;
2. closing both parent defects;
3. higher optimistic upper bound for final coverage;
4. lower frozen-core overlap, provided coverage is competitive;
5. more links with unique contribution;
6. fewer zero-exclusive links;
7. fewer weak connector-only transitions;
8. structural novelty of the defect orbit and supporting-line sequence.

Safe pruning:

- reject zero-length links;
- reject states that cannot return to exactly 22 links;
- use an optimistic union bound from remaining catalog masks;
- reject duplicate `(covered_mask, last_line, links_used, remaining_anchor_class, core_overlap)` states when one dominates another;
- use exact connectivity feasibility in the remaining line-intersection graph;
- stop all local workers immediately after an exact `64/64` candidate is independently verified.

Heuristic no-good caches are allowed for speed but must never be described as proof-level pruning unless the stored dominance relation is exact.

## 7. Implementation language

Preferred architecture:

- C++20 search core for `uint64_t` masks, exact/bounded line catalogs, meet-in-the-middle, beam search and four shared-memory worker threads;
- Python only for seed preparation, independent exact verification, aggregation and reports.

Reason: search-23 needs millions of multi-link block joins and intersection-graph operations. The heavy inner loop should not remain Python multiprocessing if a readable C++ implementation is practical.

If Step 3 retains Python for the core, it must document a measured reason and still use normal importable modules, not `*.pyfrag` concatenation.

Inside one GitHub job, four threads may share read-only geometry, the current best candidate and a bounded exact dominance cache. Avoid high-frequency locking.

## 8. Fixed 20-shard allocation

Use one primary mechanism with controlled variations:

```text
0–3    contiguous 4-link core rebuild, four spatial/sequence regions
4–7    contiguous 5-link core rebuild, four regions
8–11   contiguous 6-link core rebuild, four regions
12     7-link high-potential core window
13     8-link high-potential core window
14     paired front + middle transplant
15     paired front + tail transplant
16     paired middle + tail transplant
17     62-parent × core-diverse donor-block transplant
18     two-line support transplant + large/global reorder
19     no-core-break ablation/control reproducing the 62 wall
```

Shards `0–18` must not silently collapse into endpoint-only movement. Shard `19` is the only intentional no-core-break control.

Each shard should distribute work over all seven defect-pair parent representatives, not only the current best candidate.

## 9. Profiles

### Local dry run before GitHub

Before the smoke trigger:

1. compile all C++ and Python source;
2. verify the known 23-link full trail;
3. verify all 12 required parent/donor seeds with both exact checkers;
4. reconstruct and assert the frozen-core facts: `18` common lines, core coverage `58/64`, six residual points;
5. run every shard mode sequentially for `3–5` seconds;
6. run the aggregate builder on miniature outputs;
7. confirm all three bank outputs;
8. confirm every emitted candidate has exactly 22 nonzero links.

### Smoke

```text
seconds=180
shards=20
max-parallel=20
workers/threads=4
beam width approximately 2000 per worker
state cap approximately 100000 per worker
checkpoint_seconds=60
```

Smoke acceptance does not require `63/64`. It requires:

- green precheck;
- all `20/20` shard artifacts;
- aggregate success;
- dual exact verification of shard bests and all saved `62/64+` candidates;
- at least one valid candidate from every primary mode;
- proof in the reports that shards `0–18` actually changed the required number of frozen-core lines;
- nonempty diagnostic output for core-diverse `60/64–61/64` states;
- no zero-length link and exactly 22 links everywhere.

Only after the complete smoke aggregate passes may the full profile be launched.

### Full

```text
seconds=21000
shards=20
max-parallel=20
workers/threads=4 per shard
timeout-minutes=359
checkpoint_seconds=600
base_seed=20260723
seed_stride=1000003
```

Mix `github.run_id`, shard and worker into effective random seeds while recording all values. All parameters must resolve inside YAML.

Use a practical per-job memory cap leaving headroom below the runner limit. Record process-tree peak RAM, CPU time, states/tasks processed and states/tasks per second.

## 10. Success criteria

### Numerical success

- any independently exact `63/64` candidate;
- any independently exact `64/64` candidate, which must be saved immediately and checked by both verifiers.

### Structural success if the frontier remains 62

At least one of:

- exact `62/64` with frozen-core overlap `<=16`;
- a new two-hole orbit outside the seven search-22 families;
- an exact `61/64` or `62/64` candidate whose support-line sequence is structurally outside the Ripa/search-21 frozen family;
- a strong negative classification of a precisely defined `4–8`-link core-rebuild neighborhood, with complete task counts and no missing shards.

Another `62/64` candidate with all 18 frozen-core lines and an old defect pair is not a meaningful scientific success.

## 11. Required artifacts

Per shard:

```text
best_candidate_<shard>.json
verified_62plus_<shard>.jsonl
core_escape_diagnostics_<shard>.jsonl
raw_worker_bests_<shard>.jsonl
checkpoint_<shard>.json
search_stats_<shard>.json
resource_usage_<shard>.json
mode_manifest_<shard>.json
```

The mode manifest must record parent ids, donor ids, changed frozen-core lines, window lengths, operations, seeds and effective profile.

Aggregate:

```text
run_summary.json
summary.md
best_candidate.json
coverage_histogram.json
defect_pair_and_orbit_histogram.json
frozen_core_overlap_histogram.json
window_length_breakdown.json
donor_usage_breakdown.json
operation_breakdown.json
exact_verification_report.json
ordinary_candidate_additions.jsonl
diagnostic_core_escape.jsonl
originals_index.jsonl
shard_best_originals.jsonl
```

Three banks:

1. ordinary bank: all compact independently checked `62/64+` additions;
2. diagnostic bank: independently checked `60/64–61/64` states with frozen-core overlap `<=16`, a new defect orbit, or another explicitly recorded structural novelty;
3. originals bank: raw shard/worker best trails before symmetry compaction.

## 12. Stop and reporting rules

- Do not launch a duplicate search-23.
- Do not launch full before the smoke aggregate passes.
- Do not call failure of this bounded neighborhood a proof that 22 links are impossible.
- Record a completed full run through Prompt 1 before selecting search-24.
- Report numerical and structural outcomes separately.
