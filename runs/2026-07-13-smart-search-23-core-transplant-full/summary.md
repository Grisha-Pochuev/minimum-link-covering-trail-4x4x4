# smart-search-23-core-transplant — first full attempt and recovery state

- Run: `29249275103`
- URL: https://github.com/Grisha-Pochuev/minimum-link-covering-trail-4x4x4/actions/runs/29249275103
- Launch commit: `ac18bf46b23146f4f4a581cbf5af641c746d3171`
- Intended profile: `21000` seconds, `20` shards, `4` workers per shard, `timeout-minutes=359`.
- First attempt: precheck succeeded; `19/20` shard artifacts were produced; `core-transplant (11)` produced no artifact; the normal aggregate could not be formed.
- Recovery: GitHub is rerunning the failed shard under the same run id. This archive is a checked partial record and must be finalized after the rerun finishes.

## Checked mathematical result from 19 shards

- Numeric frontier: remains `62/64`; no `63/64` or `64/64` candidate in the 19 available shards.
- Strongest structural candidate: `mlct22-ct-c64aebf0ed34cdf4`.
- Missing points: `(1,0,2)` and `(3,3,1)`.
- Frozen-core overlap: `16/18`, so two frozen-core lines were broken while retaining `62/64`.
- This is a new two-hole orbit relative to the seven search-22 families.
- Exact checks: the shard's two CI verifiers succeeded; the archived best was additionally checked locally by two independent exact rational/incidence implementations.

Partial aggregate over the 19 available shards:

- `1115` compact exact `62/64` classes;
- `40` exact `62/64` classes with frozen-core overlap `<=16`;
- `1600` compact diagnostic core-escape states;
- `74` raw worker-best originals;
- `82,917,351,393` attempts;
- minimum observed frozen-core overlap: `0`;
- one new two-hole orbit;
- maximum measured RAM among available shards: `0.3404 GiB`;
- mean measured RAM: `0.2235 GiB`;
- mean speed: about `207,813 attempts/s` per shard.

## Dominant defect families

The seven old `z=1` pairs still dominate. Counts among compact `62/64` classes from 19 shards:

- `[(2,3,1),(3,3,1)]`: `220`;
- `[(1,3,1),(2,3,1)]`: `217`;
- `[(1,3,1),(3,3,1)]`: `198`;
- `[(0,2,1),(3,3,1)]`: `174`;
- `[(1,2,1),(2,3,1)]`: `111`;
- `[(1,2,1),(3,3,1)]`: `106`;
- `[(0,2,1),(2,3,1)]`: `66`.

The new orbit `[(1,0,2),(3,3,1)]` appeared `23` times.

## Why shard 11 failed

The original failed job log was no longer downloadable after the rerun began, so the exact final platform message is not preserved here. The evidence rules out memory exhaustion:

- neighboring shards 8, 9 and 10 used only about `0.19–0.30 GiB` RAM;
- all successful shards used nearly `400%` CPU and the search executable itself ran for almost exactly `21000` seconds;
- the workflow allowed only `359*60 - 21000 = 540` seconds for checkout, Python setup, seed download/preparation, C++ compilation, final beam trimming, two exact verifiers, resource summary and artifact upload;
- shard 11 left no artifact, which is consistent with the job being stopped at the job/runner boundary before the `if: always()` upload could execute.

Most likely cause: the full profile left only nine minutes of total job headroom, and one slower runner or slower finalization crossed that boundary. This is a technical failure, not a mathematical result.

## Prevention rule

For future serious full runs:

1. Default search time is `20400` seconds, not `21000`, when `timeout-minutes=359`.
2. Require at least `900` seconds of job headroom in preflight; `scripts/check_long_run_budget.py` enforces this.
3. Keep `if: always()` artifact upload, but also produce a lightweight failure report when a shard artifact is missing.
4. The scientific aggregate stays strict: it is final only after all required shards succeed. A partial record may be archived, but must be labelled incomplete.
5. Do not treat a stale rerun as using later workflow fixes; GitHub reruns execute the historical commit.

## Recording status

This run is not yet marked fully recorded because the rerun of shard 11 is still active. The checked structural frontier has nevertheless advanced from a frozen-core `62/64` candidate with overlap `18` to an exact `62/64` candidate with overlap `16` and a new defect orbit.
