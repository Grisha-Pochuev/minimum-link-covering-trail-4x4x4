# smart-search-18-order-from-cover64-stitch — completed run 28875314204

Run URL: https://github.com/Grisha-Pochuev/minimum-link-covering-trail-4x4x4/actions/runs/28875314204

Workflow: `smart-search-18-order-from-cover64-stitch`

Head SHA: `13699553f63bd8a96c33a5c05752ff44590e8240`

Status: `success`

Artifact family:

- summary artifact: `order-cover64-stitch-run-summary`
- shard artifacts: `order-cover64-stitch-22-shard-*`
- raw artifact ZIP saved here: `order-cover64-stitch-run-summary.zip`

## What this run tested

This was the first full contact-aware ordered reconstruction attempt after search-17. Search-17 found unordered 22-line scaffolds covering all `64/64` grid points. Search-18 tried to turn those scaffolds into actual ordered 22-link polygonal chains by choosing line order, contact vertices, and concrete `vertices2` chain geometry.

Important distinction: these outputs are checked ordered-chain reconstruction attempts, but they are far below the existing ordered-trail frontier. They are useful mainly as diagnostics of the reconstruction bottleneck.

## Controls and jobs

The workflow checks were successful:

- `check-known-23`: known Ripa 23-link construction passed.
- `check-search17-input-scaffolds`: search-17 best scaffold and strongest scaffold additions passed the cover64 line-set checker.
- `order-from-cover64-stitch`: 20 shard jobs completed successfully.
- `aggregate-order-from-cover64-stitch`: summary artifact was produced.

Because the summary artifact was complete and all jobs were successful, old runs/logs/candidate banks were not scanned deeply.

## Result

Best ordered-chain reconstruction candidate:

- candidate id: `mlct22-order-5c31614d2aeaa2aa`
- source artifact: `order-cover64-stitch-22-shard-7`
- source shard: `7`
- mode: `one_two_line_mutation`
- status: `full_length_ordered_chain`
- links: `22`
- covered_count: `44 / 64`
- missing_count: `20`
- coordinate_scale: `2`
- weak_links: `0`
- source scaffold: `mlct22-lineset-03bc99e72246b78c`

Missing points for the best candidate:

```text
(0,0,3), (0,3,0), (0,3,1), (1,0,0), (1,0,1), (1,3,3), (2,0,0), (2,0,1), (2,0,2), (2,3,1), (2,3,2), (2,3,3), (3,0,1), (3,0,2), (3,0,3), (3,1,3), (3,2,0), (3,3,0), (3,3,1), (3,3,2)
```

This is not an improvement over the existing ordered-trail frontier `60/64`. No `61/64+` ordered-trail candidate was found. The run also did not produce new unordered `64/64` line-set scaffolds; it consumed search-17 scaffolds and produced ordered reconstruction diagnostics.

## Aggregated counts

- result rows: `40`
- unique ordered candidates: `17`
- best covered_count: `44 / 64`
- best missing_count: `20`
- link histogram: all `40` rows had `22` links

Coverage histogram:

| covered_count | rows |
|---:|---:|
| 44 | 2 |
| 43 | 4 |
| 42 | 14 |
| 41 | 8 |
| 40 | 6 |
| 39 | 2 |
| 37 | 4 |

## Mode breakdown

| mode | rows | unique | best links | best covered | best weak links |
|---|---:|---:|---:|---:|---:|
| `bridge_contact_repair` | 8 | 4 | 22 | 42 | 0 |
| `contact_extreme_search` | 8 | 4 | 22 | 42 | 0 |
| `control_fixed_best` | 2 | 1 | 22 | 40 | 0 |
| `large_neighborhood_ordering` | 6 | 3 | 22 | 43 | 0 |
| `one_two_line_mutation` | 8 | 4 | 22 | 44 | 0 |
| `strict_reconstruct_top4` | 8 | 1 | 22 | 42 | 0 |

## Top compact candidates

| rank | candidate_id | mode | links | covered | missing | shard | source scaffold |
|---:|---|---|---:|---:|---:|---:|---|
| 1 | `mlct22-order-5c31614d2aeaa2aa` | `one_two_line_mutation` | 22 | 44 | 20 | 7 | `mlct22-lineset-03bc99e72246b78c` |
| 2 | `mlct22-order-70d5499035197d44` | `one_two_line_mutation` | 22 | 43 | 21 | 5 | `mlct22-lineset-03bc99e72246b78c` |
| 3 | `mlct22-order-fbaa57eaf9670a22` | `large_neighborhood_ordering` | 22 | 43 | 21 | 16 | `mlct22-lineset-03bc99e72246b78c` |
| 4 | `mlct22-order-185886c59a003870` | `one_two_line_mutation` | 22 | 42 | 22 | 6 | `mlct22-lineset-03bc99e72246b78c` |
| 5 | `mlct22-order-2ea2c5d692c5afbb` | `strict_reconstruct_top4` | 22 | 42 | 22 | 0 | `mlct22-lineset-03bc99e72246b78c` |
| 6 | `mlct22-order-3d18258629d916ad` | `contact_extreme_search` | 22 | 42 | 22 | 8 | `mlct22-lineset-03bc99e72246b78c` |
| 7 | `mlct22-order-c99fbb90116ecfe6` | `bridge_contact_repair` | 22 | 42 | 22 | 15 | `mlct22-lineset-03bc99e72246b78c` |
| 8 | `mlct22-order-bd381513264825f3` | `bridge_contact_repair` | 22 | 41 | 23 | 14 | `mlct22-lineset-03bc99e72246b78c` |
| 9 | `mlct22-order-37ab3fee63c5a071` | `contact_extreme_search` | 22 | 41 | 23 | 11 | `mlct22-lineset-03bc99e72246b78c` |
| 10 | `mlct22-order-3b264e448d06f954` | `large_neighborhood_ordering` | 22 | 41 | 23 | 17 | `mlct22-lineset-03bc99e72246b78c` |

## Diagnostic interpretation

The main lesson is negative but useful: graph-stitchability of a cover64 line-set scaffold is much weaker than real polygonal-chain orderability. Search-17 showed that good unordered 22-line scaffolds exist. Search-18 showed that the current contact-aware ordering engine loses a lot of actual grid coverage when it turns those scaffolds into one consecutive 22-link chain.

In plain words: we had the right set of buses, but when we tried to put them into one real route, the route only visited `44/64` grid points. That means the missing ingredient is not just a path in the line-set graph. We need a stronger reconstruction model that treats actual intersection/contact geometry and point preservation much more tightly.

## Candidate-bank decision

- ordinary ordered-trail candidate bank: no additions; best is only `44/64`, below the recorded `60/64` frontier.
- line-set/scaffold additions: no additions; this workflow did not create new cover64 scaffolds.
- diagnostic bank: save compact checked ordered-chain reconstruction attempts as failed-but-informative diagnostics.
- originals/index: save compact index for diagnostic ordered-chain attempts, with source shard/artifact/mode/scaffold.

## Files saved for this run

```text
runs/2026-07-07-smart-search-18-order-from-cover64-stitch-full/summary.md
runs/2026-07-07-smart-search-18-order-from-cover64-stitch-full/best_ordered_candidate.json
runs/2026-07-07-smart-search-18-order-from-cover64-stitch-full/mode_breakdown.json
runs/2026-07-07-smart-search-18-order-from-cover64-stitch-full/order-cover64-stitch-run-summary.zip
candidates/diagnostic-order-from-cover64-run28875314204.jsonl
candidates/originals/run28875314204-order-from-cover64-index.jsonl
```

## Next non-repeating step

Do not rerun `smart-search-18-order-from-cover64-stitch` with the same engine/seed as the next serious step. The useful result is that the current reconstruction model is too weak.

The next research step should diagnose why contact-aware ordering collapses from `64/64` line-set coverage to only `44/64` actual ordered-chain coverage, then design a stronger reconstruction approach. Promising directions:

- build an exact contact-state graph where a transition preserves actual covered grid points, not only abstract line adjacency;
- use dynamic programming/beam search over `(line, contact point, covered mask)` states for the 4 strongest search-17 scaffolds;
- allow controlled bridge replacement only when it preserves or increases actual coverage;
- compare the ordered `44/64` chain against its source scaffold to identify which scaffold lines lose their covered points during ordering.
