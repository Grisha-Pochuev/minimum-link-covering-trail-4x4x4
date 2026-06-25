# Local repair smoke result — 2026-06-25

This folder records a short local pre-launch smoke test of the new C++ repair engine.

This is not yet a full GitHub Actions run result. It is a seed and a sanity check for the next workflow.

## Result

- Source run used as prior material: `28103660449`
- Engine: `cpp/repair56_search.cpp`
- Mode: `repair56_target8`
- Links: `22`
- Covered grid points: `57 / 64`
- Missing count: `7`
- Status: `partial_candidate`

Missing points:

- `(1,2,1)`
- `(1,2,2)`
- `(1,2,3)`
- `(2,1,0)`
- `(3,1,1)`
- `(3,1,2)`
- `(3,1,3)`

## Why it matters

The previous GitHub frontier was `56/64` with 8 stable missing points. The local repair engine immediately found a `57/64` candidate by replacing a small part of the known trail. This supports the strategic shift from broad random search to local surgery around the defect set.

The next full run should use this candidate as a seed, but it should still be treated carefully until reproduced by GitHub Actions artifacts.

## Candidate file

- `repair57_candidate.json`

It uses `vertices2` and `coordinate_scale = 2`.
