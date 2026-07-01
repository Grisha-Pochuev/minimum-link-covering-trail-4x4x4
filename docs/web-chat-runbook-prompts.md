# Web-chat runbook prompts

This file is for ChatGPT web-chat work on this repository. It is not a mathematical proof. It is a compact operating memory so the next chat spends fewer steps rediscovering the same workflow.

## What the recent web-chat process showed

The slow part was not only the math search itself. The slow part was repeatedly reconstructing project state from scattered files and occasionally confusing a planned workflow with a workflow that actually exists in GitHub.

Best optimization: every new chat should read `START_HERE.md`, then `frontier/latest.md`, `frontier/latest.json`, and this runbook before asking what to do next.

Do not treat "all runs" as a request to blindly scan everything. First use the saved frontier and run summaries as the index. Then inspect only the exact run folders, workflow, bank additions, originals, and artifacts that are relevant to the current frontier.

Important correction from 2026-06-30: do not say a workflow has been created merely because a launch plan exists in chat. After creating or editing a workflow, fetch the workflow file back from GitHub and verify its path, name, inputs, artifact names, and generator path.

Important correction from 2026-07-01: after a hypothesis/preflight chat prepares a new workflow, keep `START_HERE.md`, `frontier/latest.md`, and `frontier/latest.json` synchronized. If `START_HERE.md` says a prepared workflow exists but `frontier/latest.*` still says "hypothesis step", update the frontier before giving launch instructions.

Important correction after user clarification on 2026-07-01: do not add a fifth mandatory smoke-test result-taking step. The user's workflow has four prompts. Smoke-test is only a technical launch gate inside the launch-preparation step. If the user sees a green check and then launches the long run, the next result-taking prompt should normally record the long/full run, not the smoke-test.

## Standard four-prompt cycle

```text
1. Result-taking prompt:
   Record completed main/full GitHub run results.

2. Hypothesis prompt:
   Compare history, form a new non-repeating hypothesis, and run small local checks if useful.

3. Launch-preparation prompt:
   Prepare files and exact GitHub inputs. Smoke-test can be used as a quick green-light, but it is not a separate scientific stage.

4. Wrap-up prompt:
   Review confusion/time loss and update memory files.
```

## Fast checklist before preparing or analyzing a launch

Use this checklist before giving GitHub inputs or deciding on a full run:

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
11. Check that local/preflight notes are not being misread as proof or as evidence of a solution.
12. Remember: green smoke-test normally means proceed to full run; do not make a separate smoke-result chat unless smoke failed, looked suspicious, or the user asks.
13. After creating/updating files, fetch them back from GitHub before reporting success.
```

## Optimized prompt 1: after a full run finishes

Use this when a main/full GitHub run has completed and needs to be recorded.

```text
Сними результаты завершённого GitHub run: <RUN_URL>.

Сначала открой START_HERE.md, затем frontier/latest.*, затем exact workflow file that launched this run, then latest relevant runs/, candidate bank/additions/originals.

Проверь jobs, logs, artifacts, aggregation, best covered_count, links, mode, candidate_id, source artifact, missing points, repeated missing patterns, and mode breakdown.

Сравни с previous frontier. Если есть новый useful result, обнови runs/<date>-<workflow>/, frontier/latest.*, START_HERE.md, candidate bank additions, and originals index. Если нет численного улучшения, всё равно запиши структурный вывод: что именно изменилось в defect family.

В ответе коротко объясни: было/стало, что дали режимы, сколько shard-best curves, сколько compact representatives, и какой следующий не-повторяющийся шаг.
```

## Optimized prompt 2: make the next hypothesis

Use this after a completed full run has been recorded.

```text
Теперь посмотри на всю историю прогонов, которую мы уже открыли и записали в памяти проекта.

Сделай новую гипотезу для следующего поиска. Главное — не повторять слепо прошлый насыщенный прогон.

Проверь гипотезу прямо здесь в чате: запусти небольшие локальные проверки на своих серверах OpenAI, сравни несколько вариантов, посмотри, есть ли смысл в идее.

В конце коротко скажи: какая гипотеза; почему она не повтор прошлого; что локальная проверка показала; стоит ли готовить под неё большой GitHub-прогон.
```

## Optimized prompt 3: prepare the next GitHub launch

Use this after local analysis or after a completed run has been recorded.

```text
Подготовь пакет запуска на GitHub.

Сначала открой START_HERE.md, frontier/latest.*, prepared workflow, docs plan, latest relevant runs/, candidate bank/additions/originals, and the local preflight conclusion.

Проверь, что smoke-test оправдан:
- workflow_dispatch-only, no push trigger;
- seed run ids and seed sources are aligned;
- artifact names and aggregation match;
- C++/Python generation, compile, checker, and summary builder paths match;
- new hypothesis is not a simple repeat of the previous saturated workflow;
- local/preflight checks are technical only and not being treated as proof.

Если всё clean, дай exact GitHub inputs for smoke-test and full run. Do not launch anything automatically unless I explicitly ask.

Важно: smoke-test — это только техническая зелёная лампочка. Если пользователь уже увидел green check и запустил основной 5h+ прогон, не надо отдельно снимать smoke-test; следующий обычный prompt 1 снимает результаты основного прогона.
```

## Optimized prompt 4: whole-chat wrap-up

Use this at the end of a long web-chat working session.

```text
Посмотри на всю работу в этом чате целиком.

Оцени, что получилось хорошо, где мы потеряли время, где была путаница, и какие файлы памяти могут сбить следующий чат.

Если нужно — измени START_HERE.md, frontier/latest.*, runbook, plan docs или другие файлы, чтобы в следующем чате работать быстрее и точнее.

В конце коротко скажи: что изменил, зачем изменил, и какой следующий шаг теперь записан в памяти проекта.
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

This package intentionally replaces the older prepared workflow notes. The next search should not repeat `smart-search-13-cover-stitch-cache`; it should use the rich-cover / endpoint-feasible stitch-compress hypothesis.

The expected workflow details are:

```text
workflow_dispatch-only: yes
push trigger: no
control check: python scripts/check_trail.py data/ripa_23_trail.json --expected-links 23 --require-full
generator: python scripts/prepare_rich_cover_stitch_engine.py --out build/rich_cover_stitch_search.cpp
compile: g++ -O3 -std=c++17 -pthread -DNDEBUG build/rich_cover_stitch_search.cpp -o rich_cover_stitch_search
checker: python scripts/check_scaled_trail.py results/rich_cover_stitch/rich_cover_stitch_best_shard_<shard>.json --max-links 22
shard artifacts: rich-cover-stitch-22-shard-*
summary artifact: rich-cover-stitch-run-summary
```

Prepared smoke-test inputs:

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
