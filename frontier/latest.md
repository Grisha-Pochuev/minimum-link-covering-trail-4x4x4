# Current search frontier

Status: full `smart-search-22-endpoint-repair` run `29181546758` is recorded. The exact checked ordered-trail frontier remains `62/64`; no `63/64` or `64/64` trail was found.

## Best checked ordered trail

- candidate id: `mlct22-er-7671ee46bd711a25`
- covered count: `62 / 64`
- coverage percent: `96.875%`
- links: `22`
- vertices: `23`
- missing: `(0,2,1)`, `(3,3,1)`
- mode: `endpoint_all_61_family_A`
- operation: `seed_crossover`
- source shard: `4`
- source worker: `0`
- effective seed: `24260734`
- rich4 links: `15`
- rich3 links: `3`
- productive connectors: `4`
- pure bridges: `0`
- source run: `29181546758`
- source file: `runs/2026-07-12-smart-search-22-endpoint-repair-full/best_candidate.json`
- status: `verified_partial_candidate`

The candidate and all other saved `62/64+` candidates passed both independent exact rational verifiers.

## Full search-22 result

- run: https://github.com/Grisha-Pochuev/minimum-link-covering-trail-4x4x4/actions/runs/29181546758
- precheck: success
- shards received: `20/20`
- aggregate: success
- compact candidates: `2385`
- compact `62/64`: `1053`
- compact `61/64`: `777`
- compact `60/64`: `555`
- compact `63/64`: `0`
- compact `64/64`: `0`
- verified `62+`: `1053`
- raw originals: `80`
- ordinary bank additions: `2385`
- diagnostic bank additions: `0`

The run did not raise the numeric frontier, but it made `62/64` highly reproducible. The remaining holes stay concentrated in the old `z=1` boundary-line defect neighborhood.

## Mode result

The strongest producers of `62/64` classes were:

- `endpoint_all_61_family_A`: `325`
- `search21_control`: `255`
- `defect_line_forcing`: `198`
- `two_free_ends`: `136`
- `endpoint_window_2to3`: `67`
- `paired_budget_transfer`: `64`
- `free_start_62`: `8`

Family B, windows 4–5 and free-end-only did not reach `62/64`.

## Unordered scaffold frontier

The best unordered line-set scaffold remains `mlct22-lineset-9772981a21b2a88a`, run `28825060197`, with `64/64` coverage and 22 lines. It is not an ordered trail and remains outside the ordinary trail bank.

## Next step

Refactor the fragment-based search-22 engine into normal Python modules, then choose a genuinely non-repeating search-23 hypothesis. Do not rerun search-22 unchanged and do not treat saturation as a proof.
