# Search-22 frozen-core analysis

Date: 2026-07-12

Source run: `29181546758`, `smart-search-22-endpoint-repair`, full profile.

This document records the Step-2 analysis performed after the full search-22 run. It is computational evidence and design guidance, not a proof that a 22-link full trail does not exist.

## 1. Input population

The full aggregate contains:

- `2385` compact exact candidates at `60/64+`;
- `1053` exact candidates at `62/64`;
- `777` at `61/64`;
- `555` at `60/64`;
- no `63/64` or `64/64` candidate.

Every `62/64+` candidate was already checked by both exact rational verifiers in the workflow.

## 2. Seven exact two-hole families

The `1053` candidates at `62/64` reduce to exactly seven raw missing-point pairs:

| Count | Missing points | Representative candidate |
|---:|---|---|
| 253 | `(2,3,1)`, `(3,3,1)` | `mlct22-er-1b9d545440a3ee2b` |
| 213 | `(1,3,1)`, `(2,3,1)` | `mlct22-er-44b7464ef2bba268` |
| 194 | `(1,3,1)`, `(3,3,1)` | `mlct22-er-763db4ef21aeba80` |
| 151 | `(0,2,1)`, `(3,3,1)` | `mlct22-er-7671ee46bd711a25` |
| 93 | `(1,2,1)`, `(2,3,1)` | `mlct22-er-592cdba87b09cf5e` |
| 86 | `(1,2,1)`, `(3,3,1)` | `mlct22-er-84b471c2367a34e7` |
| 63 | `(0,2,1)`, `(2,3,1)` | `mlct22-er-579fc6ba3b315bf0` |

All holes lie in the plane `z=1`. The most frequent missing points are:

- `(3,3,1)`: `684` occurrences;
- `(2,3,1)`: `622`;
- `(1,3,1)`: `407`;
- `(0,2,1)`: `214`;
- `(1,2,1)`: `179`.

## 3. Frozen 18-line core

The main structural result is stronger than the raw count of `1053` suggests.

After normalizing supporting lines geometrically, every one of the `1053` exact `62/64` trails contains the same `18` supporting lines out of its `22` links.

For a representative ordering, the common link positions are:

`1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 19, 21`.

Only positions `0, 2, 18, 20` vary across the full `62/64` population.

The union of the common 18-line core covers exactly `58/64` grid points. Its six uncovered points are:

```text
(0,2,1)
(1,2,1)
(1,3,1)
(2,1,2)
(2,3,1)
(3,3,1)
```

Each `62/64` member uses its four variable lines to cover exactly four of those six points and leaves two. Therefore search-22 produced many exact curves, but almost all of the apparent diversity is confined to four links around one inherited Ripa/search-21 skeleton.

This explains why simply spending more time on endpoint sweeps is unlikely to be the best next use of the GitHub budget.

## 4. Structurally different donors in the 60/61 bank

The frozen-core overlap histogram over all `2385` compact candidates is:

| Coverage | Core overlap histogram |
|---:|---|
| 62 | `18: 1053` |
| 61 | `16: 1`, `17: 172`, `18: 604` |
| 60 | `2: 4`, `16: 1`, `17: 269`, `18: 281` |

The most useful structurally different donor candidates are:

- `mlct22-er-7617f3333d5bd4a7`: `61/64`, core overlap `16`, missing `(1,3,1)`, `(2,3,1)`, `(3,3,1)`;
- `mlct22-er-222e6539aa735a14`: `60/64`, core overlap `2`;
- `mlct22-er-8636131b79055dbe`: `60/64`, core overlap `2`;
- `mlct22-er-6ea2d43af05081b7`: `60/64`, core overlap `2`;
- `mlct22-er-cf89ed8c63871970`: `60/64`, core overlap `2`.

All four low-overlap `60/64` donors leave the same four holes:

`(0,0,1)`, `(0,2,3)`, `(0,3,1)`, `(2,1,1)`.

They are worse numerically than the `62/64` parents, but far more valuable as sources of alternative multi-link blocks.

## 5. Exact shallow-neighborhood tests

The following tests were performed with exact integer/rational grid-incidence calculations. None produced `63/64` or `64/64`.

### Single-vertex replacement

- all `1053` exact `62/64` parents;
- all `23` vertex positions;
- a controlled pool of `621` integer/half-coordinate vertices;
- `14,969,448` candidate trails checked.

Result: no improvement above `62/64`.

### Exact two-link window repair

For `295` high-potential two-link windows, replacement vertices were generated from exact intersections of rays through grid points from the two fixed anchors.

- `36,911` exact repairs checked.

Result: no improvement above `62/64`.

### Three-link replacement from the observed vertex bank

- `451` distinct local problems;
- `153,058` exact replacements.

Result: no improvement.

### Prefix/suffix and block crossover

- same-index crossover among `62/64` parents: `150,808` candidates;
- full symmetry/reversal expansion: `101,088` transformed parents and `666,720` same-cut crossovers;
- block substitutions of lengths `2` through `12` using all compact `60/61/62` donors: `176,881` candidates;
- symmetry-expanded block substitutions through length `11`: more than `1.1 million` exact candidates.

Result: no improvement.

### Reordering tests

- 2-opt: `243,243` exact moves;
- 3-opt: `9,624,420` exact variants.

Result: no improvement.

### Insert-a-defect-line and reorder

For every collinear-hole `62/64` candidate, a zero-exclusive supporting line was replaced by the full line through the two defects, after which the supporting-line intersection graph was tested for a Hamiltonian ordering.

- `648` cases had more than two degree-one lines;
- `16` cases were disconnected;
- zero cases admitted a Hamiltonian ordering.

A smaller two-line transplant experiment using a `367`-line bank catalog produced `18` intersection-graph candidates and zero Hamiltonian trails.

## 6. Comparison with other cubes

The 80 collected optimal `3x3x3` 13-link curves are structurally much more varied:

- `80` symmetry/reversal classes remain distinct;
- `65` different per-link grid-point-count sequences;
- every link has at least one uniquely contributed grid point;
- exterior vertices and self-intersections are common, so merely allowing them is not the missing ingredient.

The known `5x5x5` upper construction has `36` links, but only a published figure was available in the project data, not exact ordered coordinates. It supports the broad rich-line/outside-junction principle but is not a direct machine-readable donor for `4x4x4`.

The exact known 23-link `4x4x4` trail remains the strongest geometric control. Its link profile is dense, but it also contains a zero-exclusive link, so the presence of one redundant-looking link alone is not sufficient to explain failure at 22 links.

## 7. Decision

Do not rerun endpoint repair unchanged.

The next primary hypothesis should be:

> A `63/64` or `64/64` 22-link trail requires breaking at least one, and probably two, lines of the frozen 18-line core and replacing a larger connected or paired block with geometry imported from structurally different `60/64–61/64` donors.

The selected next search is `smart-search-23-core-transplant`. Its exact Step-2 handoff is in `docs/smart-search-23-core-transplant-launch.md`.
