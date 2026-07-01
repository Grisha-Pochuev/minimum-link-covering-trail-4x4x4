# Web-chat runbook prompts

This file is for ChatGPT web-chat work on this repository. It is not a mathematical proof. It is a compact operating memory so the next chat spends fewer steps rediscovering the same workflow.

## What the recent web-chat process showed

The slow part was not only the math search itself. The slow part was repeatedly reconstructing project state from scattered files and occasionally confusing a planned workflow with a workflow that actually exists in GitHub.

Best optimization: every new chat should read `START_HERE.md`, then `frontier/latest.md`, `frontier/latest.json`, and this runbook before asking what to do next.

Do not treat "all runs" as a request to blindly scan everything. First use the saved frontier and run summaries as the index. Then inspect only the exact run folders, workflow, bank additions, originals, and artifacts that are relevant to the current frontier.

Important correction from 2026-06-30: do not say a workflow has been created merely because a launch plan exists in chat. After creating or editing a workflow, fetch the workflow file back from GitHub and verify its path, name, inputs, artifact names, and generator path.

## Fast checklist before preparing a launch

Use this checklist before giving GitHub inputs:

```text
1. Read START_HERE.md.
2. Read frontier/latest.md and frontier/latest.json.
3. Read this runbook.
4. Read the prepared workflow file from .github/workflows/.
5. Read the docs plan for that workflow.
6. Check that the workflow is workflow_dispatch-only and has no push trigger.
7. Check seed run ids and candidate-bank additions.
8. Check artifact names: shard artifact pattern and summary artifact name.
9. Check C++ generation path, compile command, checker command, and aggregator command.
10. Check that the new hypothesis is not just a same-seed rerun of a saturated workflow.
11. After creating/updating files, fetch them back from GitHub before reporting success.
12. Only then give smoke-test inputs and full-run inputs.
```

## Optimized prompt: after a run finishes

Use this when a GitHub run has completed and needs to be recorded.

```text
Сними результаты завершённого GitHub run: <RUN_URL>.

Сначала открой START_HERE.md, затем frontier/latest.*, затем exact workflow file that launched this run, then latest relevant runs/, candidate bank/additions/originals.

Проверь jobs, logs, artifacts, aggregation, best covered_count, links, mode, candidate_id, source artifact, missing points, repeated missing patterns, and mode breakdown.

Сравни с previous frontier. Если есть новый useful result, обнови runs/<date>-<workflow>/, frontier/latest.*, START_HERE.md, candidate bank additions, and originals index. Если нет численного улучшения, всё равно запиши структурный вывод: что именно изменилось в defect family.

В ответе коротко объясни: было/стало, что дали режимы, сколько shard-best curves, сколько compact representatives, и какой следующий не-повторяющийся шаг.
```

## Optimized prompt: prepare the next GitHub launch

Use this after local analysis or after a completed run has been recorded.

```text
Подготовь пакет запуска на GitHub.

Сначала открой START_HERE.md, frontier/latest.*, prepared workflow, docs plan, latest relevant runs/, candidate bank/additions/originals, and the local preflight conclusion.

Проверь, что smoke-test оправдан:
- workflow_dispatch-only, no push trigger;
- seed run ids and seed sources are aligned;
- artifact names and aggregation match;
- C++/Python generation, compile, checker, and summary builder paths match;
- new hypothesis is not a simple repeat of the previous saturated workflow.

Если всё clean, дай exact GitHub inputs for smoke-test and full run. Do not launch anything automatically unless I explicitly ask.
```

## Current prepared launch package

As of 2026-07-01, the prepared next workflow is:

```text
workflow: smart-search-14-rich-cover-stitch
workflow file: .github/workflows/smart-search-14-rich-cover-stitch.yml
plan file: docs/smart-search-14-rich-cover-stitch-plan.md
engine generator: scripts/prepare_rich_cover_stitch_engine.py
generated C++: build/rich_cover_stitch_search.cpp
```

This package intentionally replaces the older prepared workflow notes. The next search should not repeat `smart-search-13-cover-stitch-cache`; it should smoke-test the rich-cover / endpoint-feasible stitch-compress hypothesis.

Smoke-test inputs:

```text
seconds: 180
threads: 4
seed: 20260705
latest_run_id: 28460740781
previous_diversity_run_id: 28404861374
d2_bridge_run_id: 28378489636
d_family_run_id: 28338041580
new_defect_run_id: 28327372242
min_covered_to_save: 56
jobs/shards: 20
max-parallel: 20
```

Full-run inputs after green smoke-test:

```text
seconds: 21000
threads: 4
seed: 20260705
latest_run_id: 28460740781
previous_diversity_run_id: 28404861374
d2_bridge_run_id: 28378489636
d_family_run_id: 28338041580
new_defect_run_id: 28327372242
min_covered_to_save: 56
jobs/shards: 20
max-parallel: 20
expected wall time: about 5h50m per shard
```
