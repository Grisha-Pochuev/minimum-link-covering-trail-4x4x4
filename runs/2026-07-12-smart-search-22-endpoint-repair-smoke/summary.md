# smart-search-22-endpoint-repair smoke

- Run: `29181400035`
- URL: https://github.com/Grisha-Pochuev/minimum-link-covering-trail-4x4x4/actions/runs/29181400035
- Profile: `smoke`
- Status: `success`
- Precheck: success
- Shards received: `20/20`
- Exact checking: every shard best and every saved `62/64+` candidate passed both independent repository verifiers
- Aggregate: success

## Numeric result

- Ordered-trail frontier: `61/64 -> 62/64`
- Links: `22`
- Best candidate: `mlct22-er-943c78ae82c82664`
- Missing: `(2,3,1)`, `(3,3,1)`
- Mode: `free_start_62`
- Operation: `endpoint_sweep`
- Source shard: `0`
- Source worker: `0`
- rich4: `14`
- rich3: `2`
- productive connectors: `6`
- pure bridges: `0`

## Aggregate counts

- Shard bests: `20`
- Raw shard-best originals: `80`
- Compact candidates: `38`
- Compact `62/64`: `38`
- Compact `63/64`: `0`
- Compact `64/64`: `0`

The smoke run reconstructed the 62/64 endpoint repair through its deterministic endpoint sweep. It did not merely trust or copy the stored seed metadata.

## Follow-up

The full run was launched only after this smoke run completed successfully.

- Full run id: `29181546758`
- Full run URL: https://github.com/Grisha-Pochuev/minimum-link-covering-trail-4x4x4/actions/runs/29181546758
- Full profile: 20 shards, 4 workers per shard, 21000 seconds, beam width 12000 per worker, state cap 750000 per worker, 600-second checkpoints.
