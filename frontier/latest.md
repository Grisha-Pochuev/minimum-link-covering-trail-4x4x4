# Current search frontier

Status: the checked ordered-trail frontier remains `62/64`. Search-24 completed strict `20/20`, and
Step-2 local exact experiments have now closed the natural one-rich-line-replacement neighborhood
around the `62/64` wall. The next binding hypothesis is `smart-search-25-core-valley`.

## Best checked ordered trail

- candidate id: `mlct22-ct-c64aebf0ed34cdf4`
- covered count: `62 / 64`
- coverage percent: `96.875%`
- links: `22`
- vertices: `23`
- missing: `(1,0,2)`, `(3,3,1)`
- mode and operation: `paired_core_transplant`
- source run: `29249275103`, shard `14`, worker `1`
- frozen-core overlap: `16 / 18`
- source file: `runs/2026-07-13-smart-search-23-core-transplant-full/best_candidate.json`
- status: exactly verified partial trail from a completed run

It passed both CI exact verifiers and two additional independent exact incidence checks.

## Latest completed Actions run

Run `29357369876`, workflow `smart-search-24-defect-graft`:

- precheck: success;
- smoke and full: strict `20/20`;
- exact ordered `63/64`: `0`;
- exact ordered `64/64`: `0`;
- compact exact `64/64` supporting-line sets: `3,165`;
- connected compact exact `64/64` line sets: `2,349`;
- Hamiltonian supporting-line orders: `0`;
- saved near-Hamiltonian graph rows: `2,268`;
- finite `63/64` or `64/64` realizations: `0`;
- maximum measured RAM: `0.0739 GiB`;
- mean Python throughput: `14.17` attempts/s/shard.

Archive: `runs/2026-07-14-smart-search-24-defect-graft-full/`.

## Step-2 structural frontier

The complete local report is
`docs/experiments/2026-07-15-search25-core-valley-analysis.md`.

Exact contact-span experiments found:

- search-24 diagnostic rows collapse to only `502` unique supporting-line sets;
- graph-directed repairs can produce Hamiltonian `64/64` supporting-line sets, but their finite
  segment realizations are poor, confirming that graph Hamiltonicity is not the real objective;
- every one-rich-line replacement from the best `62/64` trail gives only `9` new `62/64` states;
- repeated exact replacement closes after exactly `43` `62/64` states and `134` adjacency edges;
- all `43` states retain the same `17` supporting lines;
- the component uses only `49` lines in total and has diameter `8`;
- no one-rich-line replacement exits this component to `63/64`;
- targeted one-point connector replacements through the actual holes also fail;
- breaking one of the common `17` lines yields `641` exact `61/64` valley states with `51` missing
  triples;
- a standalone line through two holes and a standalone separator transversal both fail as the second
  repair.

This is a bounded exact result. It does not prove that `63/64` or `64/64` is impossible.

## Mathematical interpretation

The previous searches were too monotone. They preserved `62/64`, but the closed plateau cannot change
any of its common `17` lines one at a time. The next credible move must change two lines atomically and
score the final finite contact spans directly. The intermediate half-move must be allowed to fall to
`59/64`, `60/64`, or `61/64`.

An unordered `64/64` line set, a connected graph, or a Hamiltonian support order remains diagnostic
only, not a trail.

## Permanent search-25 inputs

- `data/search25_local_inputs.zip` — permanent bundle containing the `43` plateau states, common `17`-line core, `641` core-break valley seeds, and inner manifest;
- `data/search25_local_inputs.README.md` — bundle hash and preflight materialization rules;
- `data/search25_local_experiment_manifest.json` — plain quick-read copy of counts and inner hashes.

## Next action

There is no active run. Step 3 must implement and launch
`docs/smart-search-25-core-valley-launch.md` exactly. Use C++20, atomic paired mutations, and finite
contact-span scoring. Do not rerun search-24, crawl the closed `43`-state plateau, or use a standalone
defect line/transversal as the primary hypothesis.
