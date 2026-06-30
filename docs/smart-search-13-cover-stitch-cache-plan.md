# smart-search-13-cover-stitch-cache plan

Prepared: 2026-06-30

This is the planned next GitHub Actions run after `smart-search-12-skeleton-diversity` / run `28404861374`.

## Why this run exists

The latest completed full run did not improve the numeric frontier: it again reached only `59/64` with `22` links. More importantly, it collapsed structurally: all 20 shard-best candidates were `59/64`, but there were only 3 exact `vertices2` representatives, and one exact curve appeared in 18 of 20 shard-best artifacts.

So the next run should not be another broad skeleton-diversity rerun. The working hypothesis is:

```text
The current 59/64 wall is partly a repeat-state problem. The search keeps rediscovering the same strong families. We should add cache pressure and anti-wall pressure so CPU time is spent on new states, new missing-set geometry, and cover/stitch/compress attempts rather than repeated copies of the same 59/64 curve.
```

## What changed

New workflow:

```text
.github/workflows/smart-search-13-cover-stitch-cache.yml
```

New engine generator:

```text
scripts/prepare_cover_stitch_cache_engine.py
```

The workflow is manual-only (`workflow_dispatch`) and keeps the usual known 23-link control check before running the search.

The generated C++ engine is still based on `cpp/repair56_search.cpp`, but the prepare script adds:

1. A bounded worker-local transposition cache for repeated end states.
2. An anti-wall archive for repeated bad 59/64 missing-set families.
3. Diversity-aware seed retention instead of letting the latest high-coverage family dominate all seeds.
4. Different shard roles for cover material, stitching, cached repair, anti-wall search, novelty from 56-58 material, and controls.
5. Extra worker summary fields: `cache_rejects` and `wall_rejects`.

## Shard plan

```text
0-4   cover_set_beam_cache
      Search for rich covering material while caching repeated coverage states.

5-8   stitch_with_transposition
      Try to stitch good material as a connected trail while avoiding repeated states.

9-12  repair_window_cache
      Long-window repair of prior candidates, but with repeated-state rejection.

13-15 anti_wall_archive
      Strong pressure away from archived 59/64 walls.

16-17 novelty_56_58
      Deliberately sample weaker-but-different 56-58 material.

18    old_59_control
      Control shard for the known 59-family behavior.

19    integer_control22
      Conservative integer-coordinate control.
```

## Archived bad walls

The prepare script stores and penalizes repeated walls including:

```text
(1,2,2), (1,3,1), (1,3,2), (2,0,2), (2,0,3)
(1,0,1), (1,2,2), (1,3,2), (2,0,3), (2,2,2)
(2,1,2), (2,2,3), (3,1,0), (3,1,2), (3,1,3)
(0,2,2), (2,1,2), (2,2,3), (3,1,0), (3,1,2)
```

They are not absolutely forbidden. They are probabilistically rejected in novelty/anti-wall modes when they reappear at `59/64` or worse. This keeps the old families available as controls and possible bridges, but stops them from consuming most of the run.

## Smoke-test inputs

Use these first:

```text
workflow: smart-search-13-cover-stitch-cache
seconds: 180
threads: 4
seed: 20260704
latest_run_id: 28404861374
d2_bridge_run_id: 28378489636
d_family_run_id: 28338041580
prior_d_run_id: 28327372242
orbit_bridge_run_id: 28304497479
previous_core5_run_id: 28292425390
old_59_run_id: 28275850889
secondary_run_id: 28275666411
base_repair_run_id: 28200925016
min_covered_to_save: 56
jobs/shards: 20
max-parallel: 20
```

The smoke-test is successful if:

- the workflow dispatch starts manually and does not run on push;
- the 23-link control passes;
- the prepare script writes the generated C++ file;
- the C++ engine compiles;
- all or almost all shards upload JSON artifacts;
- `check_scaled_trail.py` accepts generated shard JSONs;
- worker summaries include `cache_rejects` and `wall_rejects`.

## Full-run inputs after green smoke-test

Use these for the full run:

```text
workflow: smart-search-13-cover-stitch-cache
seconds: 21000
threads: 4
seed: 20260704
latest_run_id: 28404861374
d2_bridge_run_id: 28378489636
d_family_run_id: 28338041580
prior_d_run_id: 28327372242
orbit_bridge_run_id: 28304497479
previous_core5_run_id: 28292425390
old_59_run_id: 28275850889
secondary_run_id: 28275666411
base_repair_run_id: 28200925016
min_covered_to_save: 56
jobs/shards: 20
max-parallel: 20
```

## How to judge the run

Do not judge it only by whether it immediately finds `60/64`.

Useful signs:

- fewer repeats of the run-12 dominant exact candidate;
- more unique exact `vertices2` representatives than run 12's `3`;
- more unique missing-set families;
- nonzero `cache_rejects` and `wall_rejects` showing that the new rejection mechanisms are active;
- new `56/64`-`58/64` representatives with genuinely different missing-set geometry;
- any `60/64+` candidate, of course, is a major frontier change.

Bad sign:

```text
20 shard-best candidates at 59/64, but again only a few representatives and the same dominant missing wall.
```

If that happens, the next step should be a stronger unordered cover-set / stitch-compress engine rather than more inherited repair-search tuning.
