# smart-search-12-skeleton-diversity full run

Run URL: https://github.com/Grisha-Pochuev/minimum-link-covering-trail-4x4x4/actions/runs/28404861374

Workflow: `smart-search-12-skeleton-diversity`

Run commit: `7d7960619fbbb5389cb873715e1b698e2576972f`

Status: `success`

Result type: heuristic search, not a proof.

## Inputs

- seconds per shard: `21000`
- threads per shard: `4`
- shards/jobs: `20`
- total worker processes: `80`
- seed: `20260703`
- min_covered_to_save: `56`
- latest_run_id: `28378489636`
- latest_d2_run_id: `28338041580`
- prior_d_run_id: `28327372242`
- orbit_bridge_run_id: `28304497479`
- previous_core5_run_id: `28292425390`
- old_59_run_id: `28275850889`
- secondary_run_id: `28275666411`
- base_repair_run_id: `28200925016`

## Artifacts inspected

- `skeleton-diversity-run-summary`
- `skeleton-diversity-22-shard-0` ... `skeleton-diversity-22-shard-19`

The `check-known-23` control passed. The shard jobs downloaded prior artifacts, exported the candidate bank, generated and compiled the C++ engine, ran the shard, checked the shard result, and uploaded artifacts.

## Best result

- candidate id: `mlct22-dddd317f06883acd`
- covered_count: `59 / 64`
- links: `22`
- mode selected by summary: `anti_wall22`
- source artifact: `skeleton-diversity-22-shard-15`
- source shard: `15`
- missing points:
  - `(1, 2, 2)`
  - `(1, 3, 1)`
  - `(1, 3, 2)`
  - `(2, 0, 2)`
  - `(2, 0, 3)`

No `60/64` or `64/64` candidate was found.

## Candidate counts

- shard-best candidates at `covered_count >= 56`: `20`
- shard-best candidates at `59/64`: `20`
- exact unique `vertices2` representatives among shard-best candidates: `3`
- compact bank additions saved: `3`

## Dominant missing-set patterns

- `18 / 20`: `(1,2,2)`, `(1,3,1)`, `(1,3,2)`, `(2,0,2)`, `(2,0,3)`
- `1 / 20`: `(0,2,0)`, `(2,1,2)`, `(2,2,3)`, `(3,1,0)`, `(3,1,2)`
- `1 / 20`: `(0,1,2)`, `(1,2,1)`, `(1,3,2)`, `(2,1,3)`, `(2,2,2)`

## Mode breakdown

| mode | shards | worker processes | approx CPU-hours | attempts | best | unique exact candidates | useful note |
|---|---:|---:|---:|---:|---:|---:|---|
| `fresh_rich_skeleton` | 6 | 24 | 140.0 | 19146471884 | 59 | 1 | very fast, but fully collapsed to the dominant family |
| `transition_graph22` | 4 | 16 | 93.3 | 809989648 | 59 | 2 | found the only D2-like alternative from shard 7 |
| `diversity_repair22` | 4 | 16 | 93.3 | 746907432 | 59 | 2 | found the only alternate missing-set family from shard 13 |
| `anti_wall22` | 3 | 12 | 70.0 | 551754716 | 59 | 1 | did not avoid the dominant wall |
| `cross_family22` | 1 | 4 | 23.3 | 192430995 | 59 | 1 | reproduced dominant family |
| `integer_control22` | 1 | 4 | 23.3 | 292599102 | 59 | 1 | reproduced dominant family |
| `d2_control22` | 1 | 4 | 23.3 | 184643578 | 59 | 1 | reproduced dominant family |

Total attempts: `21924797355`.

## Interpretation

This run was useful mostly as negative evidence. It was intended to search for new skeletons, but the generator still collapsed back to a strong known `59/64` family. The numeric frontier did not improve, and structural diversity was lower than in run `28378489636`.

Next step: do not launch the same workflow again with the same seed. Revise the generator so novelty is enforced more strongly, or run a smaller diagnostic that rewards new defect geometry even when coverage is only `56/64`-`58/64`.
