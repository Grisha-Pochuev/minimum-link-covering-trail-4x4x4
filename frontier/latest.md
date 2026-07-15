# Current search frontier

Status: `smart-search-24-defect-graft` run `29357369876` completed successfully with strict
`20/20` full-shard aggregation and two exact verifiers. The checked ordered-trail frontier remains
`62/64`; the run produced a strong connector-topology diagnosis but no `63/64` or `64/64` trail.

## Best checked ordered trail

- candidate id: `mlct22-ct-c64aebf0ed34cdf4`
- covered count: `62 / 64`
- coverage percent: `96.875%`
- links: `22`
- vertices: `23`
- missing: `(1,0,2)`, `(3,3,1)`
- mode: `paired_core_transplant`
- operation: `paired_core_transplant`
- source shard: `14`
- source worker: `1`
- effective seed: `34270772`
- frozen-core overlap: `16 / 18`
- frozen-core lines changed: `2`
- source run: `29249275103`
- source file: `runs/2026-07-13-smart-search-23-core-transplant-full/best_candidate.json`
- status: `verified_partial_trail_from_now_completed_search23`

This candidate passed both CI exact verifiers and two additional independent exact incidence checks.
Search-24 did not produce a numerically or structurally better ordered trail.

## Completed search-24 result

Run `29357369876`, workflow `smart-search-24-defect-graft`:

- precheck: success;
- smoke: strict `20/20`;
- full: strict `20/20`;
- missing shards: none;
- best ordered trail in the run: `62/64`, baseline seed;
- exact ordered `63/64`: `0`;
- exact ordered `64/64`: `0`;
- raw exact `64/64` supporting-line-set attempts: `5,782,422`;
- compact exact `64/64` line sets: `3,165`;
- connected compact exact `64/64` line sets: `2,349`;
- Hamiltonian supporting-line orders: `0`;
- saved near-Hamiltonian graph rows: `2,268`;
- finite `63/64` or `64/64` realizations: `0`;
- ordinary bank: `21` exact `62/64` rows;
- diagnostic bank: `5,821` exact line-set/graph rows;
- originals bank: `20` raw shard bests, `2` compact classes;
- maximum measured RAM: `0.0739 GiB`;
- mean attempts per second per shard: `14.17`.

Archive:
`runs/2026-07-14-smart-search-24-defect-graft-full/`.

## Mathematical interpretation

The defect line is repeatedly sufficient to restore exact `64/64` coverage as an unordered set of
22 supporting lines. The tested connector replacements often make that line set connected, but no
tested exact intersection graph had a Hamiltonian path, so no finite ordered trail at `63/64+` was
realized.

This is strong evidence that the present obstruction is ordering and connector topology rather than
the absence of a 22-line cover. It is a bounded computational negative result for this search
neighborhood, not a proof that a 22-link covering trail is impossible.

## Source and input completion

Search-24 launched from a prepared bundle materialized from `19/20` available search-23 shard
artifacts under a recorded exception. The later strict search-23 aggregate completed `20/20` and
still contained exactly the same `40` core-escape primary seeds. The exact search-24 prepared bundle
is now permanent as `data/search24_prepared_inputs.zip`, with hashes recorded in the run archive.

## Technical lesson

The run was not memory-bound and no shard hit the state cap. The Python search engine averaged only
`14.17` attempts/s/shard. Before repeating the same graft neighborhood at greater depth, benchmark
the binding Step-2 C++20 architecture or justify another explicit implementation-language exception.

## Unordered scaffold frontier

The best general unordered line-set scaffold remains
`mlct22-lineset-9772981a21b2a88a`, run `28825060197`, with `64/64` coverage and 22 lines.
It is not an ordered trail.

## Next action

There is no active run. Step 2 should choose one non-repeating `smart-search-25-*` hypothesis using
the completed search-24 archive. Do not rerun search-24 unchanged and do not interpret its bounded
failure as impossibility.
