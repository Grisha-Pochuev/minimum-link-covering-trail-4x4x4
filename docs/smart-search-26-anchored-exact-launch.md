# smart-search-26-anchored-exact

## Binding Step-2 handoff

Date: 2026-10-07. This document is the exact Step-2 → Step-3 handoff. It was written after reading
`START_HERE.md`, `frontier/latest.*`, `frontier/active_run.json`, the runbook, every search-17…25 launch
document, the search-22/25 experiment reports, all retrospectives (especially
`docs/retrospectives/2026-07-16-search25-launch-failures.md`) and the search-23/24/25 run archives.

## Why a new kind of search

Searches 1–25 were stochastic or local (mutation, repair, transplant, graft, paired core-valley moves).
Search-25 performed 6.15 billion atomic paired mutations and found no `63/64`; the local families look
saturated. None of these searches can ever produce a *negative* statement, because they sample.

The two reference constructions — the 23-link Ripa trail and the search-23 best `62/64`
(`runs/2026-07-13-smart-search-23-core-transplant-full/best_candidate.json`) — both contain the
**Ripa corner zigzag** `333 → 000 → 300 → 033 → 003 → 330` (space diagonal, edge, face-crossing diagonal,
edge, space diagonal). In the 684 search-25 plateau/valley states, the first four zigzag lines occur in
`580–652` states and the fifth (diagonal `003–330`) in `198`.
Search-26 therefore stops sampling and asks an exact question about that structure:

> **H26.** Does any 22-link covering trail contain the Ripa corner zigzag, within an explicitly defined
> line class? Answer it by *complete* exact enumeration, so that a negative answer closes the class and a
> positive answer is an exactly verified trail.

A note on the counting slack: the bound `4 + 3·21 = 67` holds only when every vertex is a grid point.
Links may start and end off-grid (most links of the best `62/64` trail gain 4 new points), so the true
counting slack is `22·4 − 64 = 24`. Search-26 uses this exact deficit budget together with a stronger
LP-dual bound (below), not the 67-vs-64 heuristic.

## Exact contact model

Lattice lines: the `1492` lines through at least two grid points (`76` with 4 points, `72` with 3,
`1344` with 2). "Rich" lines are the `148` lines with at least 3 grid points.

A trail is a sequence of links. A link on a lattice line `L` covers exactly the grid points of `L` between
its entry and exit parameters. Consecutive links on two lattice lines meet at their exact rational
intersection point. The first and last links of the trail have free outer ends (dominated by full
extension). A **free link** (supporting line without grid points) is represented by its dominating form:
the previous link extends fully, the next link starts before all of its grid points. Consecutive links are
never collinear, except that a reversal pair counts as one free link (dominated by the free-link form).
The engine also contains an exact one-point transversal generator (non-coplanar unique transversal and
exact coplanar breakpoint cells); it is self-tested but **not used** by the search-26 stages.

## Anchor (anchor 5)

Three fixed links `000 → 300 → 033 → 003`; the link arriving at `000` lies on the space diagonal through
`000` and `333` (outer end free), and the link leaving `003` lies on the space diagonal through `003` and
`330` (outer end free). By the 48 cube symmetries and trail reversal this covers every trail containing any
image of the zigzag core. The suffix is enumerated outward from `003`, then the prefix outward from `000`;
the split between the two sides is free. Fewer than 22 links are allowed (padding preserves coverage).

## Closure ladder (the hypothesis classes)

All stages: anchor 5, at most 22 links, target `64/64`, no 2-point lattice links (`w2=0`).

| stage | connectors | class | Knuth estimate (nodes) | units |
|---|---|---|---:|---:|
| A | 0 | every non-anchor link on a rich line | ~4.3e10 | 45,030 (depth 3) |
| B | ≤1 free link | A plus one zero-point connector | ~0.7–1.4e11 | 39,930 (depth 2) |
| C | ≤2 free links | A plus two zero-point connectors | ~1.4–1.9e11 | 39,930 (depth 2) |

Classes are nested `A ⊂ B ⊂ C`. A runs first so that at least one class closes even if throughput on the
runners is far below the local measurement; B and C use the remaining time. Work units are the search-tree
nodes at the stated depth, enumerated deterministically and assigned round-robin (`unit % 20 == shard`).
A stage is **closed** only if every one of its units is reported `complete`.

Known controls: the best `62/64` trail lies in the larger class `w2=3, k=3` (3 two-point links, one free
link, two one-point transversals) and is reproduced exactly by the engine (`data/search26/controls/`).
Larger classes (two-point links, transversals) are 10–100× bigger and are explicitly **not** claimed.

## Search and pruning

Exhaustive depth-first branch and bound, C++20, standard library only, 4 threads per shard.

Admissible feasibility bound at every child (any failure prunes):

1. counting: uncovered points ≤ current-link points ahead + top-`a` rich-line uncovered counts
   + 2·(two-point links) + 1·(transversals) for some allocation of the remaining links;
2. LP-dual fractional cover: with `y_p = 1/m(p)`, `m(p)` the largest number of uncovered points on a rich
   line through `p`, each rich link contributes at most 1 to `Σ y_p`; weak links contribute their top
   values; the current link at most 1.

Exact transposition table per thread (full-key comparison, no hash-only pruning; failure states only),
`2048` MB per thread (`8` GiB per shard). Memoised bound evaluations per node.

Local measurements (2-core ARM sandbox, g++ 14 / g++ 13 / clang 19 identical results): `~2.4–3.2e5`
nodes per thread-second, `~0.15` GiB RSS without the large table.

## Correctness controls (all in the shared preflight)

- line census (`1492 / 1344 / 72 / 76`);
- transversal generator dominance check against dense exact sampling (`>5000` samples, zero misses);
- replay of the best `62/64` trail for anchors 4 and 5: model coverage `62`, 22 links, reconstruction
  verified by both exact verifiers and by `scripts/check_rational_trail.py`;
- admissibility: an independent unpruned Python enumeration (`scripts/search26_bruteforce.py`) and the
  bounded engine agree exactly on the maximum coverage for small link budgets (`links=8`, `k=0,1`);
- verifier negative tests: zero-length link, 21 links, over-claimed coverage are all rejected;
- miniature 2-shard run of every stage plus a control stage (target 48) that produces leaves with free
  connectors, strict aggregate, both verifiers over every bank.

## Inputs, dependencies and transport

- inputs: none besides committed readable source and two small text replay controls;
- no ZIP, tarball, base64 part or binary is committed or downloaded;
- runner image `ubuntu-24.04`; `g++` from the image (asserted `>= 11`); Python `3.12` via
  `actions/setup-python@v5`; Python standard library only; no apt, pip or Boost dependency;
- the engine is compiled inside every job from `src/search26/anchored_exact.cpp`; each job records the
  source and binary SHA-256 and reruns the self-test.

## Outputs and verifier contract

Per shard (`results/search26/shard-XX/`): per-stage `units.jsonl` (status per unit), `leaves.jsonl`
(engine move paths), `engine_summary.json`, `engine.log`; `bank_full64.jsonl` (any `64/64`),
`bank_near.jsonl` (leaves with model coverage `>= 56`, and control leaves), both verifier reports and
`shard_summary.json` (nodes, throughput inputs, peak child RSS, engine SHA-256).

Every saved leaf is reconstructed to exact rational vertices (`scripts/search26_common.py`), padded to
exactly 22 nonzero links if fewer were used, and passed through **both** exact verifiers
(`verify_search26_primary.py` using the repository's rational geometry, and
`verify_search26_independent.py`, integer-only, no shared code). A shard fails on any zero-length link,
wrong link count, or verified coverage below the claimed model coverage. The aggregates re-run both
verifiers over the merged banks.

## Workflow shape and profiles

`precheck (shared preflight) → smoke [20] → strict smoke-aggregate → full [20] → strict full-aggregate`,
plus `failure-report` (`if: always()`, non-strict, labelled incomplete).

- smoke: 150 search seconds per shard (A 45, B 45, C 30) plus a 20 s control stage, 4 threads, 2048 MB TT
  per thread; strict 20/20, every stage did work, control produced verified trails, peak RSS `<= 13` GiB;
- full: `20400` search seconds per shard, ladder A → B → C each taking the remaining time, 4 threads,
  2048 MB TT per thread, job timeout `359` minutes (`1140` s headroom, checked by
  `scripts/check_long_run_budget.py`).

## Success and interpretation

- any `64/64`: exact constructive 22-link solution, archived immediately after both verifiers;
- stage closed with no `64/64`: **no 22-link covering trail contains the Ripa corner zigzag (any symmetric
  image) when all other links lie on rich lines (plus at most k zero-point connectors, consecutive links
  non-collinear)** — an exact computational theorem for that class;
- stage partial: only the completed units are closed; this is not evidence for the open units;
- an infrastructure failure is technical evidence only, never a mathematical result.

## Release gate

Before the trigger: freeze one release commit, run
`python scripts/check_step3_release.py --manifest docs/search26-step3-release-manifest.json --allow-missing-trigger --report <report>`
on a fresh clone of that exact commit (this runs the full shared preflight), record the passing report and
release commit in `frontier/active_run.json`, then create `launch/smart-search-26-anchored-exact.trigger`
in a separate final commit exactly once. The `--allow-missing-trigger` flag (added 2026-10-07) exists
because the trigger file must not exist before the trigger commit; CI precheck runs the gate without it.
