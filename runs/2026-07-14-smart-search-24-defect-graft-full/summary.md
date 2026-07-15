# smart-search-24-defect-graft — final recorded result

Run: `29357369876`  
Workflow: `smart-search-24-defect-graft`  
Launch commit: `7ece93a06ea910371ea6a987e43d5b6cdd3e21b5`  
Profile: automatic precheck -> strict smoke `20/20` -> full `20/20` -> strict aggregate  
Search time: `20400` seconds per shard, `20` shards, `4` workers per shard  
Status: **complete and exactly verified**

## Ordered-trail result

- Best ordered trail in this run: `62/64`, 22 links.
- Candidate: `mlct22-ct-044ee473dca9d853-baseline`.
- Missing points: `(0,2,1)` and `(3,3,1)`.
- Operation: `baseline_seed`; no defect line was inserted.
- Independent local exact recheck: 22 nonzero links, exactly 62 grid points covered, the same two points missing.
- Exact ordered `63/64`: `0`.
- Exact ordered `64/64`: `0`.

The global checked frontier therefore remains the structurally stronger search-23 candidate
`mlct22-ct-c64aebf0ed34cdf4` at `62/64`, missing `(1,0,2)` and `(3,3,1)`.

## Defect-graft diagnostics

- Raw exact `64/64` supporting-line-set attempts: `5,782,422`.
- Compact exact `64/64` supporting-line sets: `3,165`.
- Connected compact exact `64/64` line sets: `2,349`.
- Compact line sets with `0`, `1`, or `2` degree-one vertices: `4`, `109`, and `663`.
- Saved near-Hamiltonian graph rows: `2,268`.
- Hamiltonian supporting-line orders: `0`.
- Finite realizations at `63/64` or `64/64`: `0`.

This strongly reinforces the current diagnosis: the exact defect line repairs coverage at the
unordered supporting-line level, but connector topology and ordering prevent realization as one
22-link trail in the explored neighborhood.

This is a bounded computational negative result for the tested defect-graft search, **not** a proof
that no 22-link covering trail exists.

## Three banks

- Ordinary: `21` independently checked ordered `62/64` rows.
- Diagnostic: `5,821` exact line-set and graph rows, including `3,165` compact full-cover line sets and `2,268` near-Hamiltonian graphs.
- Originals: `20` raw shard bests; exact compaction leaves `2` classes.

`banks.json` records exact counts and SHA-256 digests. `compact_aggregate_bundle.zip` permanently
contains all small reports plus the exact ordinary and originals JSONL files. The 16.3 MB diagnostic
JSONL remains identified by exact digest and Actions artifact id; it is never counted as an ordered
trail bank.

## Prepared-input provenance

The workflow materialized its seed bundle from search-23 Actions artifacts. The exact bundle is now
persisted as `data/search24_prepared_inputs.zip`, with hashes in `artifact_provenance.json`.

At launch, search-23 supplied `19/20` shard artifacts under an explicit exception. The later strict
search-23 recovery aggregate completed `20/20` and still contained exactly `40` core-escape primary
seeds. Therefore the prepared search-24 primary seed set was complete for its stated policy.

## Performance

- Attempts: `5,782,422`.
- Mean attempts per second per shard: `14.17`.
- Maximum measured process-tree RAM: `0.0739 GiB`.
- No shard hit the configured state cap.

The search was not memory-bound. The Python implementation-language exception materially limited
throughput and should be benchmarked against a C++20 implementation before repeating the same
neighborhood at larger depth.
