# Current search frontier

Status: `smart-search-23-core-transplant` run `29249275103` is in recovery. Its first full attempt produced `19/20` shard artifacts; shard `11` failed before artifact upload and is being rerun. The numeric frontier remains `62/64`, but the checked structural frontier improved.

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
- status: `verified_partial_candidate_from_incomplete_run`

This candidate passed the two CI exact verifiers and two additional local exact incidence checks. It does not improve the number `62/64`, but it breaks two lines of the search-22 frozen core and belongs to a new two-hole orbit.

## Search-23 first-attempt result, 19 available shards

- precheck: success;
- shard artifacts received: `19/20`;
- missing first-attempt shard: `11`;
- compact exact `62/64`: `1115`;
- exact `62/64` with frozen-core overlap `<=16`: `40`;
- compact diagnostic core-escape states: `1600`;
- raw worker-best originals: `74`;
- compact `63/64`: `0`;
- compact `64/64`: `0`;
- new two-hole orbits: `1`;
- attempts: `82,917,351,393`.

The ordinary seven `z=1` defect pairs remain dominant, but the pair `(1,0,2)`, `(3,3,1)` appeared 23 times and is structurally new.

## Completion status

The previous fully completed and fully recorded run remains search-22, run `29181546758`. Search-23 is archived as a checked partial result until the retry of shard 11 and the strict 20/20 aggregate finish. Do not start search-24 yet.

## Technical lesson

The failed shard was not memory-bound: available shards used at most `0.3404 GiB`. The unsafe part was time headroom: `21000` search seconds under `timeout-minutes=359` leaves only `540` seconds for setup, compilation, exact verification and artifact upload. Future full runs default to `20400` seconds and must pass the long-run budget preflight with at least `900` seconds headroom.

## Unordered scaffold frontier

The best unordered line-set scaffold remains `mlct22-lineset-9772981a21b2a88a`, run `28825060197`, with `64/64` coverage and 22 lines. It is not an ordered trail.
