# Run 28275666411 — smart-search-6-defect smoke

This folder records the useful smoke-test result from GitHub Actions run `28275666411`.

Run URL: https://github.com/Grisha-Pochuev/minimum-link-covering-trail-4x4x4/actions/runs/28275666411

## Basic metadata

- Repository: `Grisha-Pochuev/minimum-link-covering-trail-4x4x4`
- Workflow: `smart-search-6-defect`
- Run id: `28275666411`
- Head commit SHA: `a9192d722ecd80e3b29a59bea2b2efffec4f8a13`
- Status: `success`
- Seconds per shard: `90`
- Threads per shard: `4`
- Prior run id used by smoke: `28200925016`
- Candidate bank export: `23` records scanned, `23` seed JSON files written

## Best result

The smoke-test unexpectedly improved the frontier:

```text
59 / 64 = 92.1875%
```

Best selected candidate:

- covered_count: `59 / 64`
- links: `22`
- mode: `subcube_stitch22`
- source artifact: `defect-22-shard-15`
- status: `partial_candidate`
- missing count: `5`
- missing: `(1,2,1)`, `(2,1,2)`, `(2,2,3)`, `(3,1,0)`, `(3,1,3)`

This is still a partial candidate, not a full `64/64` covering trail and not a proof.

## Mode performance in the smoke summary

- `subcube_stitch22`: best `59/64`, average about `58.33/64` over 3 shard-best results.
- `fractional_bridge22`: best `59/64`, average `58.25/64` over 4 shard-best results.
- `repair56_target8`: best `59/64`, average about `58.17/64` over 6 shard-best results.
- `transition_penalty22`: best `58/64` over 5 shard-best results.
- `rich_segment_catalog`: best `58/64` over 1 result.
- `integer_control22`: best `58/64` over 1 result.

## What this changes for the full run

Do not run the old 58-target full search unchanged. The full run should now use run `28275666411` as latest seed material and should retarget the C++ defect weighting to the new 5-point missing set from the 59/64 candidate.
