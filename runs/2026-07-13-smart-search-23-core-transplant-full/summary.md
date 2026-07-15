# smart-search-23-core-transplant — final recovery result

- Run: `29249275103`
- Launch commit: `ac18bf46b23146f4f4a581cbf5af641c746d3171`
- Intended profile: `21000` seconds, `20` shards, `4` workers per shard, `timeout-minutes=359`.
- First attempt: `19/20` shard artifacts; shard `11` missed artifact upload.
- Recovery: shard `11` succeeded under the historical commit and the strict aggregate completed `20/20`.
- Final summary artifact: `8328628940`, digest
  `sha256:fe1c45a8adf084cbb5f3d87d7553d6e536d23b406493570e8ac7435ec060dc9e`.

## Final checked mathematical result

- Best: `62/64`; no exact `63/64` or `64/64`.
- Best candidate: `mlct22-ct-c64aebf0ed34cdf4`.
- Missing: `(1,0,2)` and `(3,3,1)`.
- Frozen-core overlap: `16/18`.
- Compact ordinary `62/64+`: `1115`.
- Exact `62/64` with frozen-core overlap `<=16`: `40`.
- Compact diagnostic core-escape states: `1602`.
- Raw worker-best originals: `79`.
- Search attempts: `87,975,890,177`.
- New two-hole orbits: `1`.
- Every saved shard best, ordinary candidate and diagnostic candidate passed two independent exact
  verifiers.

The recovered shard did not add another intended primary core-escape seed: the final count remained
`40`. This retrospectively confirms the exact primary seed bundle used by search-24.

## Technical lesson

The first-attempt failure was not memory-bound. The `21000`-second search left only `540` seconds
inside a `359`-minute job for setup, compilation, finalization, two exact verifiers and artifact
upload. Future serious runs use `20400` seconds and require at least `900` seconds headroom.

## Recording status

The run is now strictly complete. The earlier `partial_run_summary.json` remains as historical
first-attempt evidence; `final_run_summary.json` is the authoritative final aggregate record.
