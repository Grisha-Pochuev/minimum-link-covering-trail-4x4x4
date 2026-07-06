# Web-chat runbook prompts

This file is for ChatGPT web-chat work on this repository. It is not a mathematical proof. It is a compact operating memory so the next chat spends fewer steps rediscovering the same workflow.

## What the recent web-chat process showed

The slow part was not only the math search itself. The slow part was repeatedly reconstructing project state from scattered files and occasionally confusing a planned workflow with a workflow that actually exists in GitHub.

Best optimization: in a new chat, read `START_HERE.md` once at the very beginning, during prompt 1. After that, do not reopen it in prompts 2, 3, and 4 unless the user explicitly says this is a new chat, memory was lost, or the earlier context is clearly missing.

Do not treat "all runs" as a request to blindly scan everything. First use the saved frontier and run summaries as the index. Then inspect only the exact run folders, workflow, bank additions, originals, and artifacts that are relevant to the current frontier.

Important correction from 2026-06-30: do not say a workflow has been created merely because a launch plan exists in chat. After creating or editing a workflow, fetch the workflow file back from GitHub and verify its path, name, inputs, artifact names, and generator path.

Important correction from 2026-07-01: after a hypothesis/preflight chat prepares a new workflow, keep `START_HERE.md`, `frontier/latest.md`, and `frontier/latest.json` synchronized.

Important correction after user clarification on 2026-07-01: do not add a fifth mandatory smoke-test result-taking step. The user's workflow has four prompts. Smoke-test is only a technical launch gate inside the launch-preparation step. If the user sees a green check and then launches the long run, the next result-taking prompt should normally record the long/full run, not the smoke-test.

Important correction from 2026-07-02: if the GitHub connector cannot write executable workflow files under `.github/workflows/`, prepare `docs/proposed-<workflow>.yml`, tell the user to copy its raw YAML into `.github/workflows/<workflow>.yml`, then fetch the real workflow file back and verify that the first line is `name: ...`.

Important correction from 2026-07-07: `smart-search-17-cover64-stitch-graph` is a line-set scaffold search, not a trail proof. Do not merge its outputs into the normal ordered-trail bank until they are converted into checked polygonal-trail candidates.

## Standard four-prompt cycle

```text
1. Result-taking prompt:
   Start the chat by reading START_HERE.md once, then record completed main/full GitHub run results.

2. Hypothesis prompt:
   Use the already-loaded project context, think broadly, form a new non-repeating hypothesis, and run small local checks if useful.

3. Launch-preparation prompt:
   Use the already-loaded context to prepare files and exact GitHub inputs. Smoke-test can be used as a quick green-light, but it is not a separate scientific stage.

4. Wrap-up prompt:
   Review confusion/time loss and update memory files.
```

## Fast checklist before preparing or analyzing a launch

```text
1. In a new chat only: read START_HERE.md once at the beginning.
2. Use the context already opened earlier in the chat; avoid rereading START_HERE.md in prompts 2-4.
3. Use frontier/latest.md, frontier/latest.json, and this runbook as compact indexes when needed.
4. Read the prepared workflow file from .github/workflows/ if it exists.
5. Read the docs plan or docs/proposed workflow for that workflow.
6. Check that the workflow is workflow_dispatch-only and has no push trigger.
7. Check that the real workflow is YAML, not a copied plan document. Its first line should usually be `name: <workflow>`.
8. Check seed run ids and candidate-bank additions.
9. Check artifact names: shard artifact pattern and summary artifact name.
10. Check engine/checker/summary builder paths match.
11. Check that the new hypothesis is not just a same-seed rerun of a saturated workflow.
12. Check that local/preflight notes are not being misread as proof or as evidence of a solution.
13. Remember: green smoke-test normally means proceed to full run; do not make a separate smoke-result chat unless smoke failed, looked suspicious, or the user asks.
14. After creating/updating files, fetch them back from GitHub before reporting success.
```

## Optimized prompt 1: after a full run finishes

```text
Сними результаты завершённого GitHub run: <RUN_URL>.

Это начало нового рабочего чата, поэтому сначала один раз открой START_HERE.md как долговременную память проекта. Потом открой frontier/latest.md, frontier/latest.json, docs/web-chat-runbook-prompts.md, workflow-файл, который запустил run, relevant runs/, candidate bank/additions/originals, jobs, logs and artifacts.

Проверь jobs, logs, artifacts, aggregation, best covered_count, links, mode, candidate_id, source artifact, missing points, repeated missing patterns, and mode breakdown.

Сравни с previous frontier. Если есть новый useful result, обнови runs/<date>-<workflow>/, frontier/latest.*, START_HERE.md, candidate bank additions, and originals index. Если нет численного улучшения, всё равно запиши структурный вывод: что именно изменилось в defect family.

Обязательно запиши кривые в соответствующие три банка кривых: compact reusable bank/additions для дальнейшего поиска, run-level additions для этого прогона, and originals archive/index без потери реального разнообразия shard-best кривых. Не смешивай эти три роли.

Сделай коммит. В ответе коротко объясни: было/стало, что дали режимы, сколько shard-best curves, сколько compact representatives, что записано в каждый из трёх банков кривых, и какой следующий не-повторяющийся шаг.
```

## Optimized prompt 2: make the next hypothesis

```text
Теперь сделай следующий исследовательский шаг: подумай, куда нам идти дальше.

Опирайся на уже открытый в этом чате контекст: результаты последнего записанного прогона, frontier, runbook, summaries, candidate banks, originals, artifacts и любые новые файлы или источники, которые я добавил для этого шага.

Не своди задачу к простому улучшению прошлого workflow. Посмотри шире: какие структуры мы могли не заметить, где может быть новый источник кривых, какие старые стены повторяются, какие данные из банков или новых источников могут подсказать другой заход.

Сформулируй несколько возможных направлений, выбери самое перспективное и проверь его прямо здесь в чате маленькими локальными проверками. Доработай идею до состояния, где её можно либо отвергнуть, либо превратить в GitHub launch package.

В конце коротко скажи: какая гипотеза выбрана, почему она не повтор прошлого, что показали локальные проверки, и стоит ли готовить под неё большой GitHub-прогон.
```

## Optimized prompt 3: prepare the next GitHub launch

```text
Подготовь пакет запуска на GitHub под выбранную гипотезу.

Используй уже открытый в этом чате контекст: frontier, runbook, выбранную гипотезу, вывод локальной проверки, relevant runs, candidate bank/additions/originals, prepared workflow or proposed workflow, and docs plan. Не открывай START_HERE.md заново, если мы уже открывали его в начале этого чата.

Создай или измени нужные обычные файлы: generator/engine, plan doc, seed files, candidate additions, START_HERE.md or runbook if memory must change.

Если текущий чатовый GitHub-коннектор блокирует запись в `.github/workflows/`, не притворяйся, что workflow создан. Положи точный YAML в `docs/proposed-<workflow>.yml` и дай пошаговую инструкцию, как вручную скопировать его в `.github/workflows/<workflow>.yml`.

Проверь запуск: workflow_dispatch-only, no push trigger, real workflow YAML starts with name:, seed run ids and seed sources are aligned, artifact names and aggregation match, engine/checker/summary builder paths match, new hypothesis is not a repeat.

Если всё clean, дай exact GitHub inputs for smoke-test and full run. Do not launch anything automatically unless I explicitly ask and the available tool actually supports workflow_dispatch.
```

## Optimized prompt 4: whole-chat wrap-up

```text
Посмотри на всю работу в этом чате целиком.

Оцени, что получилось хорошо, где мы потеряли время, где была путаница, и какие правила или файлы памяти могут сбить следующий чат.

Не открывай START_HERE.md заново только ради чтения, если он уже был открыт в начале чата. Но если выводы сегодняшнего чата нужно сохранить в долговременную память, измени START_HERE.md, frontier/latest.*, docs/web-chat-runbook-prompts.md, plan docs или другие файлы.

Особенно проверь третий шаг: мог ли чат сам создать workflow, был ли manual fallback, не был ли случайно скопирован markdown plan вместо YAML, какие inputs реально нужны для smoke и full.

В конце коротко скажи: что изменил, зачем изменил, какой следующий шаг теперь записан в памяти проекта, и какие четыре промпта лучше использовать дальше.
```

## Current prepared launch package

As of 2026-07-07, the prepared launch package is:

```text
workflow: smart-search-17-cover64-stitch-graph
workflow file: .github/workflows/smart-search-17-cover64-stitch-graph.yml
proposed workflow backup: docs/proposed-smart-search-17-cover64-stitch-graph.yml
plan file: docs/smart-search-17-cover64-stitch-graph-plan.md
engine: scripts/search_cover64_stitch_graph.py
checker: scripts/check_cover64_line_set.py
summary builder: scripts/build_cover64_stitch_summary.py
seed: data/search17/local_cover64_stitch_graph_seed.json
local line-set addition: candidates/line-set-additions-local-cover64-stitch-chat-20260704.jsonl
```

This package intentionally replaces repeating `smart-search-16-defect-relay-60`. The new serious search should use the cover64 stitch graph hypothesis: first find/optimize unordered 22-line `64/64` scaffolds, then use those as raw material for ordered-trail reconstruction.

Expected workflow details:

```text
workflow_dispatch-only: yes
push trigger: no
control check 1: python scripts/check_trail.py data/ripa_23_trail.json --expected-links 23 --require-full
control check 2: python scripts/check_cover64_line_set.py data/search17/local_cover64_stitch_graph_seed.json --expect-covered 64 --max-lines 22 --min-stitch-path 18
engine: python scripts/search_cover64_stitch_graph.py
checker: python scripts/check_cover64_line_set.py results/cover64_stitch/cover64_stitch_best_shard_<shard>.json --max-lines 22
summary builder: python scripts/build_cover64_stitch_summary.py
shard artifacts: cover64-stitch-22-shard-*
summary artifact: cover64-stitch-run-summary
shards/jobs: 20
max-parallel: 20
```

Smoke-test inputs:

```text
seconds: 180
workers: 4
seed: 20260717
min_covered_to_save: 64
min_stitch_path_to_save: 18
box_min: -1
box_max: 4
max_universe: 9000
max_lines: 22
latest_run_id: 28674416173
previous_frontier_run_id: 28618565146
```

Full-run inputs after green smoke-test:

```text
seconds: 21000
workers: 4
seed: 20260717
min_covered_to_save: 64
min_stitch_path_to_save: 18
box_min: -1
box_max: 4
max_universe: 9000
max_lines: 22
latest_run_id: 28674416173
previous_frontier_run_id: 28618565146
expected wall time: about 5h50m per shard
```

Known caveat: search-17 outputs are unordered line-set scaffolds. They are not final trail candidates and not proofs until a separate ordered-trail reconstruction/check succeeds.
