# smart-search-12-skeleton-diversity plan

Date: 2026-06-30

This plan records why `smart-search-12-skeleton-diversity` exists and how to use it from ChatGPT web chat.

## Why this workflow exists

Recent full runs repeatedly reached `59/64` with `22` links but did not reach `60/64`.

The latest useful run is:

```text
run id: 28378489636
workflow: smart-search-11-d2-bridge-repair
best: 59/64, 22 links
all 20 shard-best artifacts: 59/64
no 60/64 and no 64/64
```

The important signal was not numeric improvement. The important signal was structural diversity: the latest run produced more compact representatives but still concentrated around a new repeated wall, especially `(2,1,2)` and `(2,2,3)`.

Working hypothesis:

```text
The 59/64 wall is not only a local repair failure. The old skeleton families may naturally leave five holes. The next useful run should search for different 22-link skeletons and different transitions between rich segments, not only repair the same D2 wall again.
```

## Files

```text
workflow: .github/workflows/smart-search-12-skeleton-diversity.yml
engine generator: scripts/prepare_skeleton_diversity_engine.py
base C++ engine: cpp/repair56_search.cpp
```

The workflow is `workflow_dispatch` only. It intentionally has no `push` trigger.

## Shard strategy

```text
0-5   fresh_rich_skeleton
      Build new chains using rich 3-point and 4-point segments.

6-9   transition_graph22
      Search for better transitions between rich segments; avoid wasting links on 1-new-point transitions.

10-13 diversity_repair22
      Repair diverse known 59/64 representatives with long bridge windows, not just the latest champion.

14-16 anti_wall22
      Push away from repeated D/D2/A defect walls to discover new families.

17    cross_family22
      Try cross-family stitches between old A/D/D2 material and latest representatives.

18    integer_control22
      Conservative integer-coordinate control.

19    d2_control22
      D2-like control for comparison with smart-search-11.
```

## Seed sources

Use the latest full run plus older frontier runs:

```text
latest_run_id=28378489636
latest_d2_run_id=28338041580
prior_d_run_id=28327372242
orbit_bridge_run_id=28304497479
previous_core5_run_id=28292425390
old_59_run_id=28275850889
secondary_run_id=28275666411
base_repair_run_id=28200925016
min_covered_to_save=56
```

The workflow also reads saved run folders and candidate bank files when present.

## Launch order

First run a smoke-test:

```text
seconds=180
threads=4
seed=20260703
```

If the smoke-test is green, launch the full run:

```text
seconds=21000
threads=4
seed=20260703
```

Keep the same run ids unless a newer completed run has already been recorded in `frontier/latest.*` and `START_HERE.md`.

## What counts as success

Primary success:

```text
60/64 or better with <=22 links.
```

Useful success even without numeric improvement:

```text
59/64 with a genuinely new compact family or a defect set not equivalent to the old A/D/D2/D2-bridge walls.
```

Also useful:

```text
57/64 or 58/64 with a strongly different skeleton, because it may give a new repair direction.
```

## What to inspect after the run

Do not only ask whether the best candidate improved. Inspect:

```text
best covered_count
best links
best mode
missing points
defect-set frequencies
mode breakdown
number of compact representatives
whether any shard family is new modulo symmetry
whether one mode dominates or fails
whether d2_control22 merely reproduces the old wall
```

If the run completes, record the result in a new `runs/<date>-smart-search-12-skeleton-diversity-*/` folder, update `frontier/latest.*`, and update `START_HERE.md`.

## Web-chat operational note

In this web-chat environment, creating the workflow file is possible through the GitHub connector, but launching `workflow_dispatch` may not be available unless the tool exposes an explicit dispatch action. If no dispatch action is available, do not claim the run was launched. Tell the user to use GitHub UI: Actions -> `smart-search-12-skeleton-diversity` -> Run workflow.

After creating or editing a workflow, fetch the file back from GitHub before telling the user it exists.
