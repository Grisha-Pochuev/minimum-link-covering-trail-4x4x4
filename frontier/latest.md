# Current search frontier

Status: `smart-search-22-endpoint-repair` smoke run `29181400035` advanced the exact checked ordered-trail frontier from `61/64` to `62/64`. The corresponding full run `29181546758` is active; do not duplicate it.

## Best checked ordered trail

- candidate id: `mlct22-er-943c78ae82c82664`
- covered count: `62 / 64`
- coverage percent: `96.875%`
- links: `22`
- vertices: `23`
- missing: `(2,3,1)`, `(3,3,1)`
- missing count: `2`
- mode: `free_start_62`
- operation: `endpoint_sweep`
- source shard: `0`
- source worker: `0`
- effective seed: `20260722`
- rich4 links: `14`
- rich3 links: `2`
- productive connectors: `6`
- pure bridges: `0`
- canonical key: `ed8bcae4c5a60fe7be9838ae0d8e716ccffaa294c29b14dd7352da67cfd76d72`
- source run: `29181400035`
- source file: `runs/2026-07-12-smart-search-22-endpoint-repair-smoke/best_candidate.json`
- status: `verified_partial_candidate`

The candidate was checked by both independent exact rational verifiers in GitHub Actions. It is a genuine numerical improvement, but not a full cover and not a proof.

## Search-22 smoke

- run: https://github.com/Grisha-Pochuev/minimum-link-covering-trail-4x4x4/actions/runs/29181400035
- status: success
- precheck: success
- shards received: `20/20`
- compact candidates: `38`
- compact `62/64`: `38`
- compact `63/64`: `0`
- compact `64/64`: `0`
- raw shard-best originals: `80`
- all shard bests and saved `62+` classes passed both exact verifiers

The smoke run reconstructed the 62/64 result through an endpoint sweep rather than merely trusting stored metadata.

## Active full run

- run: https://github.com/Grisha-Pochuev/minimum-link-covering-trail-4x4x4/actions/runs/29181546758
- workflow: `smart-search-22-endpoint-repair`
- profile: full
- launch commit: `7925fd4e6b42ce8591b0958bce106901c4c305ec`
- precheck: success
- all `20` shard jobs created and computation started
- `seconds=21000`
- `workers=4`
- `max-parallel=20`
- `beam_width_per_worker=12000`
- `state_cap_per_worker=750000`
- `checkpoint_seconds=600`

## Structural interpretation

Search-21's broad direct compression saturated at two three-hole families after about 6.65 million saved-shard attempts. Search-22 exploits a cheaper degree of freedom: moving a free endpoint changes one link rather than two. That immediately converted the three-hole family `(0,2,1), (1,3,1), (2,3,1)` into a two-hole family `(2,3,1), (3,3,1)`.

The full search now combines endpoint sweeps with local windows, paired distant repair/compression, two-end changes, and forced defect-line links, always retaining exactly 22 links.

## Unordered scaffold frontier

The best unordered line-set scaffold remains `mlct22-lineset-9772981a21b2a88a`, run `28825060197`, with `64/64` coverage and 22 lines. It is not an ordered polygonal trail and remains outside the ordinary trail bank.

## Next step

Do not launch another search-22. When full run `29181546758` finishes, record all jobs, logs, artifacts, exact `62+` checks, three candidate banks, raw originals, defect families, RAM/speed statistics, and the final frontier before selecting search-23.
