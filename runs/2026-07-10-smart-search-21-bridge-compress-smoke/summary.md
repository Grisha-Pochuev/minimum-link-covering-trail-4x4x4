# smart-search-21-bridge-compress smoke

- Run: `29123090565`
- URL: https://github.com/Grisha-Pochuev/minimum-link-covering-trail-4x4x4/actions/runs/29123090565
- Profile: `smoke`
- Status: `success`
- Precheck: success
- Shard jobs: `20/20` succeeded
- Exact checker: succeeded for every shard-best
- Aggregate artifact: success

## Numeric result

- Ordered-trail frontier: `60/64 -> 61/64`
- Links: `22`
- Verified compact `61/64` candidates: `2`
- Full `64/64`: `0`
- Best candidate: `mlct22-bc-889d7f8c45252068`
- Missing: `(0,2,1)`, `(1,3,1)`, `(2,3,1)`
- Mode: `ripa_6to5_slide`
- Pure bridges: `0`
- rich4: `14`
- rich3: `1`
- productive connectors: `7`

The best candidate is an exact `6->5` local compression of the known 23-link full construction. It was checked in GitHub Actions and independently recomputed from the downloaded artifact using exact rational arithmetic.

## Smoke statistics

- Shard-best: `20`
- Compact classes: `598`
- Total attempts: `60554`
- Compact `61/64`: `2`
- Compact `60/64`: `9`
- Candidates with at most six pure bridges: `598`

## Follow-up

The full run was launched only after this smoke run completed successfully.

- Full run id: `29123493808`
- Full run URL: https://github.com/Grisha-Pochuev/minimum-link-covering-trail-4x4x4/actions/runs/29123493808
- Effective full profile: `20` shards, `4` workers per shard, `21000` seconds, `beam_width=16000`, `state_cap=3000000`, `candidate_lines=8000`, `start_limit=64`, `window=3..6`, `max_mutations=2`, `max_pure_bridges=6`, `save_min_covered=56`.
