# Web-chat runbook prompts

This file is for ChatGPT web-chat work on this repository. It is not a mathematical proof. It is a compact operating memory so the next chat spends fewer steps rediscovering the same workflow.

## What the recent web-chat process showed

The slow part was not only the math search itself. The slow part was repeatedly reconstructing project state from scattered files and occasionally confusing a planned workflow with a workflow that actually exists in GitHub.

Best optimization: every new chat should read `START_HERE.md`, then `frontier/latest.md`, `frontier/latest.json`, and this runbook before asking what to do next.

Do not treat "all runs" as a request to blindly scan everything. First use the saved frontier and run summaries as the index. Then inspect only the exact run folders, workflow, bank additions, originals, and artifacts that are relevant to the current frontier.

Important correction from 2026-06-30: do not say a workflow has been created merely because a launch plan exists in chat. After creating or editing a workflow, fetch the workflow file back from GitHub and verify its path, name, inputs, artifact names, and generator path.

Important correction from 2026-07-01: after a hypothesis/preflight chat prepares a new workflow, keep `START_HERE.md`, `frontier/latest.md`, and `frontier/latest.json` synchronized. If `START_HERE.md` says a prepared workflow exists but `frontier/latest.*` still says "hypothesis step", update the frontier before giving launch instructions.

Important correction after user clarification on 2026-07-01: do not add a fifth mandatory smoke-test result-taking step. The user's workflow has four prompts. Smoke-test is only a technical launch gate inside the launch-preparation step. If the user sees a green check and then launches the long run, the next result-taking prompt should normally record the long/full run, not the smoke-test.

Important correction from 2026-07-02: the ChatGPT GitHub connector may be blocked from writing executable workflow files under `.github/workflows/`. In that case, prepare `docs/proposed-<workflow>.yml`, tell the user to copy its raw YAML into `.github/workflows/<workflow>.yml`, then fetch the real workflow file back and verify that the first line is `name: ...`. Do not confuse a plan markdown file with a workflow YAML file.

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
4. Read the prepared workflow file from .github/workflows/ if it exists.
5. Read the docs plan or docs/proposed workflow for that workflow.
6. Check that the workflow is workflow_dispatch-only and has no push trigger.
7. Check that the real workflow is YAML, not a copied plan document. Its first line should usually be `name: <workflow>`.
8. Check seed run ids and candidate-bank additions.
9. Check artifact names: shard artifact pattern and summary artifact name.
10. Check C++ generation path, compile command, checker command, and aggregator command.
11. Check that the new hypothesis is not just a same-seed rerun of a saturated workflow.
12. Check that local/preflight notes are not being misread as proof or as evidence of a solution.
13. Remember: green smoke-test normally means proceed to full run; do not make a separate smoke-result chat unless smoke failed, looked suspicious, or the user asks.
14. After creating/updating files, fetch them back from GitHub before reporting success.
```

## Optimized prompt 1: after a full run finishes

Use this when a main/full GitHub run has completed and needs to be recorded.

```text
Сними результаты завершённого GitHub run: <RUN_URL>.

Сначала открой START_HERE.md как долговременную память проекта. Затем открой frontier/latest.md, frontier/latest.json, этот runbook, workflow-файл, который запустил run, relevant runs/, candidate bank/additions/originals, jobs, logs and artifacts.

Проверь jobs, logs, artifacts, aggregation, best covered_count, links, mode, candidate_id, source artifact, missing points, repeated missing patterns, and mode breakdown.

Сравни с previous frontier. Если есть новый useful result, обнови runs/<date>-<workflow>/, frontier/latest.*, START_HERE.md, candidate bank additions, and originals index. Если нет численного улучшения, всё равно запиши структурный вывод: что именно изменилось в defect family.

Сделай коммит. В ответе коротко объясни: было/стало, что дали режимы, сколько shard-best curves, сколько compact representatives, и какой следующий не-повторяющийся шаг.
```

## Optimized prompt 2: make the next hypothesis

Use this after a completed full run has been recorded.

```text
Теперь посмотри на всю историю прогонов, которую мы уже открыли и записали в памяти проекта.

Открой START_HERE.md, frontier/latest.*, этот runbook, последние run summaries, candidate bank/additions/originals, and any extra file I attached or added for this step.

Сделай новую гипотезу для следующего поиска. Главное — не повторять слепо прошлый насыщенный прогон.

Проверь гипотезу прямо здесь в чате: запусти небольшие локальные проверки на своих серверах OpenAI, сравни несколько вариантов, посмотри, есть ли смысл в идее. Доработай гипотезу до состояния, где её можно превратить в GitHub launch package.

В конце коротко скажи: какая гипотеза; почему она не повтор прошлого; что локальная проверка показала; стоит ли готовить под неё большой GitHub-прогон.
```

## Optimized prompt 3: prepare the next GitHub launch

Use this after local analysis or after a completed run has been recorded.

```text
Подготовь пакет запуска на GitHub.

Сначала открой START_HERE.md, frontier/latest.*, этот runbook, prepared workflow or proposed workflow, docs plan, latest relevant runs/, candidate bank/additions/originals, and the local preflight conclusion.

Создай или измени нужные обычные файлы: generator/engine, plan doc, candidate seed files, candidate bank additions, START_HERE.md or runbook. Если текущий чатовый GitHub-коннектор блокирует запись в `.github/workflows/`, не притворяйся, что workflow создан: положи точный YAML в `docs/proposed-<workflow>.yml` и дай пошаговую инструкцию, как вручную скопировать его в `.github/workflows/<workflow>.yml`.

Проверь, что smoke-test оправдан:
- workflow_dispatch-only, no push trigger;
- real workflow file exists in `.github/workflows/` or there is a clear manual-copy fallback;
- real workflow YAML starts with `name:`, not with a markdown plan heading;
- seed run ids and seed sources are aligned;
- artifact names and aggregation match;
- C++/Python generation, compile, checker, and summary builder paths match;
- new hypothesis is not a simple repeat of the previous saturated workflow;
- local/preflight checks are technical only and not being treated as proof.

Если всё clean, дай exact GitHub inputs for smoke-test and full run. Do not launch anything automatically unless I explicitly ask and the available tool actually supports workflow_dispatch.

Важно: smoke-test — это только техническая зелёная лампочка. Если пользователь уже увидел green check и запустил основной 5h+ прогон, не надо отдельно снимать smoke-test; следующий обычный prompt 1 снимает результаты основного прогона.
```

## Optimized prompt 4: whole-chat wrap-up

Use this at the end of a long web-chat working session.

```text
Посмотри на всю работу в этом чате целиком.

Оцени, что получилось хорошо, где мы потеряли время, где была путаница, и какие файлы памяти могут сбить следующий чат.

Если нужно — измени START_HERE.md, frontier/latest.*, runbook, plan docs или другие файлы, чтобы в следующем чате работать быстрее и точнее.

Особенно проверь третий шаг: мог ли чат сам создать workflow, был ли manual fallback, не был ли случайно скопирован markdown plan вместо YAML, какие inputs реально нужны для smoke и full.

В конце коротко скажи: что изменил, зачем изменил, и какой следующий шаг теперь записан в памяти проекта.
```

## Current prepared launch package

As of 2026-07-02, the prepared launch package is:

```text
workflow: smart-search-15-rich-line-transition-60
workflow file: .github/workflows/smart-search-15-rich-line-transition-60.yml
proposed workflow backup: docs/proposed-smart-search-15-rich-line-transition-60.yml
plan file: docs/smart-search-15-rich-line-transition-60-plan.md
engine generator: scripts/prepare_rich_line_transition_engine.py
generated C++: build/rich_line_transition_search.cpp
local seed: data/search15/local_60_candidate_cover_first_stitch_cost.json
local bank addition: candidates/bank-additions-local-60-chat-20260702.jsonl
```

This package intentionally replaces the older prepared `smart-search-14-rich-cover-stitch` launch notes. The next serious search should use the rich-line transition / stitch-cost hypothesis around the local `60/64` seed.

The expected workflow details are:

```text
workflow_dispatch-only: yes
push trigger: no
control check 1: python scripts/check_trail.py data/ripa_23_trail.json --expected-links 23 --require-full
control check 2: python scripts/check_scaled_trail.py data/search15/local_60_candidate_cover_first_stitch_cost.json --expect-covered 60 --max-links 22
generator: python scripts/prepare_rich_line_transition_engine.py --out build/rich_line_transition_search.cpp
compile: g++ -O3 -std=c++17 -pthread -DNDEBUG build/rich_line_transition_search.cpp -o rich_line_transition_search
checker: python scripts/check_scaled_trail.py results/rich_line_transition/rich_line_transition_best_shard_<shard>.json --max-links 22
shard artifacts: rich-line-transition-22-shard-*
summary artifact: rich-line-transition-run-summary
shards/jobs: 20
max-parallel: 20
```

Smoke-test inputs:

```text
seconds: 180
threads: 4
seed: 20260706
min_covered_to_save: 56
latest_run_id: 28522369532
previous_cover_stitch_run_id: 28460740781
previous_diversity_run_id: 28404861374
```

Full-run inputs after green smoke-test:

```text
seconds: 21000
threads: 4
seed: 20260706
min_covered_to_save: 56
latest_run_id: 28522369532
previous_cover_stitch_run_id: 28460740781
previous_diversity_run_id: 28404861374
expected wall time: about 5h50m per shard
```

Known 2026-07-02 launch pitfall: the first manual copy accidentally put the markdown plan into `.github/workflows/smart-search-15-rich-line-transition-60.yml`. The broken run had no jobs. The fix is to copy raw YAML from `docs/proposed-smart-search-15-rich-line-transition-60.yml`; the workflow file must begin with `name: smart-search-15-rich-line-transition-60`.
