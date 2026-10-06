# Search-26 Step 2/3 notes — 2026-10-07

## Lessons from the search-25 launch failures that the search-26 release guards against

| search-25 failure | search-26 guard |
|---|---|
| corrupted ZIP / changed base64 payload | no archives, no base64, no binaries; only readable source and two small text replay files; every file hashed in the manifest and re-checked statically by CI precheck on the committed payload |
| undeclared Boost header | C++ standard library only; Python standard library only; no apt/pip; toolchain asserted in the workflow; compiled locally with g++ 14, g++ 13 and clang 19 (identical results) |
| zero-length segments in a diagnostic bank | engine junctions are strictly ahead; every saved leaf is reconstructed, padded to exactly 22 links and rejected on any zero-length link by both verifiers; verifier negative tests in preflight |
| opaque runtime tarball patched at runtime | engine compiled from `src/search26/anchored_exact.cpp` inside every job; source and binary SHA-256 recorded per shard |
| Actions used as a release debugger | full shared preflight (same command locally, in the release gate and in CI precheck) passed on a fresh clone of the release commit before the trigger |
| unfrozen release | release commit frozen; report and active-run record in a later commit that changes no manifest file; trigger alone in the final commit |

## Process detail added

`scripts/check_step3_release.py --allow-missing-trigger`: the pre-trigger gate cannot require the trigger
file to exist, because creating it fires the workflow. CI precheck runs the static gate without the flag.

## Mathematical selection

The 4 + 3·21 = 67 slack argument assumes grid-point vertices; with off-grid vertices the exact deficit
budget is 22·4 − 64 = 24. Unanchored exhaustive enumeration was estimated (Knuth) at 1e16–1e22 nodes and
rejected; anchoring on the Ripa corner zigzag with rich lines plus at most two zero-point connectors gives
closable classes (≈4e10–2e11 nodes) within 20 × 4 × 20400 thread-seconds.
