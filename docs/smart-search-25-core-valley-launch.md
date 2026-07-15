# smart-search-25-core-valley

## Binding Step-2 handoff

This document is the exact handoff for Step 3. Step 2 does not launch GitHub Actions.

## Scientific objective

Search for an exactly verified ordered `22`-link trail covering at least `63/64`, with immediate stop
and certificate output at `64/64`.

The search must work on **finite contact spans**, not merely unordered coverage or a Hamiltonian graph
of infinite supporting lines.

## Hypothesis

The `62/64` wall is a closed one-line-replacement component with a common `17`-line core. Any single
change to this core falls to `61/64` or lower. Progress therefore requires an atomic paired mutation:
remove at least one common-core line and a second line, add two new lines jointly, and evaluate the
final ordered finite trail without pruning the intermediate half-move.

## Required implementation

- language: `C++20`;
- exact geometry: normalized integer line keys plus exact rational contact parameters;
- no Python search loop in the full matrix;
- state contains:
  - ordered sequence of `22` supporting lines;
  - exact entry and exit contact on each line;
  - exact finite coverage mask;
  - common-17 overlap;
  - missing-point mask;
  - parent and paired-operation metadata;
- all saved candidates pass two independent exact verifiers.

## Permanent inputs

- `data/search25_local_inputs.zip` — bundle containing the `43` plateau states, common `17` lines, `641` exact `61/64` core-break states, and inner manifest;
- `data/search25_local_inputs.README.md` — bundle SHA-256 and materialization rules;
- `data/search25_local_experiment_manifest.json` — plain quick-read copy of hashes and counts;
- the current ordered frontier candidate from search-23;
- the known full `23`-link Ripa trail only as a control.

Preflight must independently recheck row counts, file hashes, line counts, and exact coverage.

## Atomic mutation families

Every primary mutation changes two supporting lines in one transaction. It is forbidden to reject the
mutation because its first half is only `59/64`, `60/64`, or `61/64`.

1. **core-rich-pair**
   - remove one common-17 line and one variable/weak line;
   - add two rich lines jointly;
   - rank by exact final finite coverage and contact-span compatibility.

2. **core-rich-contact**
   - remove one common-17 line and one weak line;
   - add one productive rich line and one contact/transversal line;
   - generate the contact line from the final pair of new lines and neighboring retained lines, not as
     an isolated one-line repair.

3. **core-contact-pair**
   - add two mutually cooperating connector/transversal lines;
   - allow either new line to cover zero or one grid point when their combined final trail improves
     coverage.

4. **valley-beam**
   - start from the `641` exact core-break `61/64` seeds;
   - retain diverse `59/64`–`61/64` states with common-17 overlap at most `16`;
   - expand only with exact finite-span scoring;
   - deduplicate by ordered line keys, contact signature, coverage mask, and symmetry class.

## Shard allocation

- shards `0–5`: `core-rich-pair`, partitioned by common-core line index;
- shards `6–10`: `core-rich-contact`, partitioned by missing-triple orbit;
- shards `11–14`: `core-contact-pair`, partitioned by contact/separator type;
- shards `15–17`: `valley-beam`, different diversity and temporary-loss budgets;
- shard `18`: exact bounded closure/control around the `43` plateau states;
- shard `19`: old best `62/64` control and throughput benchmark.

No shard may merely repeat search-24 defect grafting or generic single-vertex repair.

## Scoring order

1. exact finite covered count;
2. exact `63/64` or `64/64` success;
3. lower common-17 overlap, provided coverage is at least `59/64`;
4. fewer forced articulation separators in the ordered contact state;
5. missing-orbit novelty;
6. contact-span slack around currently uncovered points;
7. symmetry and raw-path novelty.

An unordered `64/64` line set, a connected graph, or a Hamiltonian support order is diagnostic only.

## Save policy

Always save and exactly verify:

- every ordered `63/64` or `64/64` trail;
- every ordered `62/64` trail outside the closed `43`-state component;
- diverse ordered `60/64` and `61/64` states with common-17 overlap `<=15`;
- paired-operation diagnostics showing which two removed and two added lines were used;
- per-shard throughput, peak RAM, state counts, pruning counts, and missing-orbit histograms.

Do not flood the ordinary bank with old plateau states; keep them in the dedicated search-25 input
bank.

## Profiles

Smoke:

- `20` shards;
- `4` workers per shard;
- `180` search seconds;
- small but nonzero valley beam;
- strict aggregate must receive `20/20` artifacts and run both exact verifiers.

Full:

- `20` shards;
- `4` workers per shard;
- `20400` search seconds;
- job timeout `359` minutes;
- at least `900` seconds total headroom;
- checkpoint interval `600` seconds;
- full starts automatically only after strict smoke success.

## Smoke acceptance

Smoke is accepted only if:

- all `20` shards finish and upload artifacts;
- all permanent input hashes and counts match;
- at least one primary shard performs real atomic paired mutations;
- at least one primary shard reaches a state with common-17 overlap `<=15`;
- exact finite-span verifier agrees with the independent verifier;
- no state-cap or serialization bug silently disables a mutation family;
- measured C++ throughput is recorded.

## Explicitly exhausted or forbidden repeats

Do not spend a full run on:

- crawling the closed `43`-state `62/64` component by one rich-line replacement;
- one defect line through two holes as a standalone repair;
- one separator transversal as a standalone repair;
- support-graph Hamiltonicity without finite contact spans;
- generic single-vertex plateau search;
- a Python implementation of the full search.

## Success and interpretation

- `63/64`: real numeric breakthrough; archive and promote the candidate after both exact verifiers.
- `64/64`: solve the constructive `22`-link target, archive a full certificate immediately.
- no improvement: archive as a bounded negative result for atomic two-line core-valley mutations; it
  is not a global proof that `22` links are impossible.
