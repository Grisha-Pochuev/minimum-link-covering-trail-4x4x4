# smart-search-22-endpoint-repair full run

- Run: `29181546758`
- URL: https://github.com/Grisha-Pochuev/minimum-link-covering-trail-4x4x4/actions/runs/29181546758
- Workflow: `smart-search-22-endpoint-repair`
- Profile: `full`
- Launch commit: `7925fd4e6b42ce8591b0958bce106901c4c305ec`
- Result: success; precheck, 20/20 shards, exact checks and aggregate all succeeded.

## Mathematical result

- Best ordered trail: `62/64` with exactly `22` nonzero links.
- Best candidate: `mlct22-er-7671ee46bd711a25`.
- Missing points: `[[0, 2, 1], [3, 3, 1]]`.
- No `63/64` or `64/64` candidate.
- Compact candidates: `2385`: `1053` at 62, `777` at 61, `555` at 60.
- Every shard best and all `1053` saved 62+ candidates passed both exact rational verifiers.

## Three candidate banks

- Ordinary additions: `2385` compact symmetry classes.
- Diagnostic endpoint-repair bank: `0` entries (no separate diagnostic-only class survived the bank policy).
- Raw originals: `80` worker/shard-best ordered trails, with a separate 80-row originals index in the aggregate artifact.

## Modes

The strongest producers of 62/64 classes were `endpoint_all_61_family_A` (325), `search21_control` (255), `defect_line_forcing` (198), `two_free_ends` (136), `endpoint_window_2to3` (67), `paired_budget_transfer` (64), and `free_start_62` (8). Family B, windows 4-5 and free-end-only did not reach 62.

## Structural conclusion

The full budget greatly expanded the 62/64 population but did not improve the numeric frontier. The remaining defects are concentrated in the same z=1 boundary-line neighborhood. Endpoint freedom is a reliable way to turn three-hole search-21 curves into two-hole curves, but this version saturates at 62/64.
