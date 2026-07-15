# Step 2 experiment: why the 62/64 wall repeats

Date: 2026-07-15

## Result in one sentence

The numeric frontier did **not** move above `62/64`, but the local experiments isolated the actual
mechanism of the wall: all exactly reachable `62/64` supporting-line states in the tested rich-line
neighborhood keep the same `17`-line core, and any single change to that core falls to `61/64` or
lower. A search which refuses this temporary loss is forced back onto the same wall.

This is a bounded exact computational result, not a proof that `63/64` or `64/64` is impossible.

## What search-24 was measuring incorrectly

Search-24 first optimized an unordered set of infinite supporting lines, then its intersection graph,
and only afterwards asked whether the finite segments between consecutive intersections actually
cover the grid points.

Those are three different properties:

1. twenty-two infinite lines can cover all `64` grid points;
2. their intersection graph can be connected or even Hamiltonian;
3. the finite segment between the two chosen contacts on each line must contain its assigned grid
   points.

The third condition is the real obstruction. Two lines may intersect, but the intersection can lie on
the wrong side of the grid points. The correct search state therefore needs the exact entry and exit
contact on every supporting line, not only the line-set graph.

## Local exact experiments

All geometry decisions used exact integer or rational arithmetic.

### Search-24 graph diagnosis

After exact line-key deduplication, the `5,433` line-set diagnostic rows collapsed to only `502`
unique supporting-line sets. `380` were connected. Only `9` connected graphs had at most two leaves.
Small articulation separators explained most failures.

A separator-directed repair generated `164` exact `64/64` line sets and, for the first time in this
local analysis, `53` supporting-line sets with a Hamiltonian path. This broke the *graph* wall, but
not the trail wall: the best finite-segment realization from these orders covered only `52/64`.
Thus Hamiltonicity of the infinite lines is not a sufficient objective.

### Ordered local repairs

- exhaustive one-vertex plateau search from the best trail: `147` distinct `62/64` neighbors, no
  `63/64`;
- the same search from all `47` search-24 prepared seeds: `661` exact `62/64` states, no `63/64`;
- a `61/64` valley search examined more than `63,000` exact states and roughly `400 million` local
  mutation attempts, no `63/64`;
- randomized two- and three-vertex changes performed more than `116 million` exact evaluations, no
  `63/64`;
- exact contact-span replacement of every four-link and five-link window by rich supporting lines
  stayed at `62/64` or below;
- exhaustive local compression and reordering around the known full `23`-link Ripa trail also stayed
  at `62/64` or below.

### Exact supporting-line replacement closure

Starting from the best ordered `62/64` trail, every one-rich-line replacement was checked:

- `32,406` line sets;
- `38,746` Hamiltonian supporting-line orders;
- exactly `9` new finite `62/64` states;
- no `63/64`.

Repeating the same exact one-line replacement from every new `62/64` state produced a finite closed
component:

- `43` exact `62/64` supporting-line states;
- `134` one-replacement edges;
- one connected component;
- graph diameter `8`;
- no outgoing one-rich-line replacement to `63/64`;
- no new state after closure.

The four missing-point pairs in this component are:

- `20` states: `(2,2,1)`, `(3,3,1)`;
- `10` states: `(1,0,2)`, `(3,3,1)`;
- `10` states: `(1,3,1)`, `(2,2,1)`;
- `3` states: `(2,2,1)`, `(3,2,1)`.

All `43` states contain the same `17` supporting lines. Their union contains only `49` distinct
lines, so just `32` lines vary across the entire closed component.

### Tests outside the closed `62/64` component

Targeted one-point connector replacements through the actual holes of all `43` states examined
`780,846` attempts. After exact support and topology filters only `4,840` distinct sets remained; the
best finite trail was `61/64`.

Breaking one of the common `17` lines with one rich-line replacement produced:

- `1,076,763` attempted replacements;
- `1,074,485` distinct line sets;
- `2,656,623` Hamiltonian support orders;
- `641` exact `61/64` core-break states;
- `51` distinct missing triples.

These `641` states are the useful valley bank for search-25.

The simplest second repair was also exhausted:

- add the line through two of the three holes, then remove one old line: no `63/64`;
- add an exact transversal through one hole and two current supporting lines, then remove one old
  line: no `63/64`.

Therefore search-25 must make a genuinely **coordinated two-line change**, scored by finite contact
spans from the beginning. It must not require either half of the change to be a good standalone
state.

## What was being missed

The previous searches were too monotone. They retained `62/64` and discarded most `61/64` states.
But the exact closure shows that the `62/64` plateau cannot change any of its common `17` lines one at
a time. The required move has the form:

```text
62/64 closed plateau
    -> break a common-core line and temporarily fall to 61/64 or lower
    -> change a second line before pruning
    -> evaluate the final two-line replacement by exact contact spans
```

The two changes must be one atomic mutation. Testing a defect line or a transversal as a complete
second step is still too restrictive; both new lines may need to cooperate before either one is
useful.

## Durable data

- `data/search25_local_inputs.zip`: permanent bundle containing all `43` plateau states, the common `17`-line core, all `641` core-break `61/64` seeds, and the inner manifest;
- `data/search25_local_inputs.README.md`: bundle hash, contents and preflight rules;
- `data/search25_local_experiment_manifest.json`: plain quick-read copy of row counts and inner SHA-256 hashes.

## Conclusion

The honest result is not a discovered `63/64` trail. The important advance is that the obvious
neighborhood around `62/64` has been exactly closed and cannot be rescued by a single rich line, a
single hole line, or a single separator transversal. The next credible route is an atomic paired
core-valley search, not another deeper copy of search-24.
