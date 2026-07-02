# Web-chat runbook prompts

This file is for ChatGPT web-chat work on this repository. It is not a mathematical proof. It is a compact operating memory so the next chat spends fewer steps rediscovering the same workflow.

## What the recent web-chat process showed

The slow part was not only the math search itself. The slow part was repeatedly reconstructing project state from scattered files and occasionally confusing a planned workflow with a workflow that actually exists in GitHub.

Best optimization: in a new chat, read `START_HERE.md` once at the very beginning, during prompt 1. After that, do not reopen it in prompts 2, 3, and 4 unless the user explicitly says this is a new chat, memory was lost, or the earlier context is clearly missing.

Do not treat "all runs" as a request to blindly scan everything. First use the saved frontier and run summaries as the index. Then inspect only the exact run folders, workflow, bank additions, originals, and artifacts that are relevant to the current frontier.

Important correction from 2026-06-30: do not say a workflow has been created merely because a launch plan exists in chat. After creating or editing a workflow, fetch the workflow file back from GitHub and verify its path, name, inputs, artifact names, and generator path.

Important correction from 2026-07-01: after a hypothesis/preflight chat prepares a new workflow, keep `START_HERE.md`, `frontier/latest.md`, and `frontier/latest.json` synchronized. If `START_HERE.md` says a prepared workflow exists but `frontier/latest.*` still says "hypothesis step", update the frontier before giving launch instructions.

Important correction after user clarification on 2026-07-01: do not add a fifth mandatory smoke-test result-taking step. The user's workflow has four prompts. Smoke-test is only a technical launch gate inside the launch-preparation step. If the user sees a green check and then launches the long run, the next result-taking prompt should normally record the long/full run, not the smoke-test.

Important correction from 2026-07-02: the ChatGPT GitHub connector may be blocked from writing executable workflow files under `.github/workflows/`. In that case, prepare `docs/proposed-<workflow>.yml`, tell the user to copy its raw YAML into `.github/workflows/<workflow>.yml`, then fetch the real workflow file back and verify that the first line is `name: ...`. Do not confuse a plan markdown file with a workflow YAML file.

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

Use this checklist before giving GitHub inputs or deciding on a full run:

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
10. Check C++ generation path, compile command, checker command, and aggregator command.
11. Check that the new hypothesis is not just a same-seed rerun of a saturated workflow.
12. Check that local/preflight notes are not being misread as proof or as evidence of a solution.
13. Remember: green smoke-test normally means proceed to full run; do not make a separate smoke-result chat unless smoke failed, looked suspicious, or the user asks.
14. After creating/updating files, fetch them back from GitHub before reporting success.
```

## Optimized prompt 1: after a full run finishes

Use this when a main/full GitHub run has completed and needs to be recorded. This is also the boot prompt for a fresh web chat.

```text
Сними результаты завершённого GitHub run: <RUN_URL>.

Это начало нового рабочего чата, поэтому сначала один раз открой START_HERE.md как долговременную память проекта. Потом открой frontier/latest.md, frontier/latest.json, docs/web-chat-runbook-prompts.md, workflow-файл, который запустил run, relevant runs/, candidate bank/additions/originals, jobs, logs and artifacts.

Проверь jobs, logs, artifacts, aggregation, best covered_count, links, mode, candidate_id, source artifact, missing points, repeated missing patterns, and mode breakdown.

Сравни с previous frontier. Если есть новый useful result, обнови runs/<date>-<workflow>/, frontier/latest.*, START_HERE.md, candidate bank additions, and originals index. Если нет численного улучшения, всё равно запиши структурный вывод: что именно изменилось в defect family.

Обязательно запиши кривые в соответствующие три банка кривых: compact reusable bank/additions для дальнейшего поиска, run-level additions для этого прогона, and originals archive/index без потери реального разнообразия shard-best кривых. Не смешивай эти три роли.

Сделай коммит. В ответе коротко объясни: было/стало, что дали режимы, сколько shard-best curves, сколько compact representatives, что записано в каждый из трёх банков кривых, и какой следующий не-повторяющийся шаг.
```

## Optimized prompt 2: make the next hypothesis

Use this after prompt 1 in the same chat. Do not reopen `START_HERE.md`; rely on the context already loaded in prompt 1 unless the user says this is a new chat.

```text
Теперь сделай следующий исследовательский шаг: подумай, куда нам идти дальше.

Опирайся на уже открытый в этом чате контекст: результаты последнего записанного прогона, frontier, runbook, summaries, candidate banks, originals, artifacts и любые новые файлы или источники, которые я добавил для этого шага.

Не своди задачу к простому улучшению прошлого workflow. Посмотри шире: какие структуры мы могли не заметить, где может быть новый источник кривых, какие старые стены повторяются, какие данные из банков или новых источников могут подсказать другой заход.

Сформулируй несколько возможных направлений, выбери самое перспективное и проверь его прямо здесь в чате маленькими локальными проверками. Доработай идею до состояния, где её можно либо отвергнуть, либо превратить в GitHub launch package.

В конце коротко скажи: какая гипотеза выбрана, почему она не повтор прошлого, что показали локальные проверки, и стоит ли готовить под неё большой GitHub-прогон.
```

## Optimized prompt 3: prepare the next GitHub launch

Use this after prompt 2 in the same chat. Do not reopen `START_HERE.md`; rely on the context already loaded earlier unless the user says this is a new chat or the needed context is missing.

```text
Подготовь пакет запуска на GitHub под выбранную гипотезу.

Используй уже открытый в этом чате контекст: frontier, runbook, выбранную гипотезу, вывод локальной проверки, relevant runs, candidate bank/additions/originals, prepared workflow or proposed workflow, and docs plan. Не открывай START_HERE.md заново, если мы уже открывали его в начале этого чата.

Создай или измени нужные обычные файлы: generator/engine, plan doc, seed files, candidate additions, START_HERE.md or runbook if memory must change.

Если текущий чатовый GitHub-коннектор блокирует запись в `.github/workflows/`, не притворяйся, что workflow создан. Положи точный YAML в `docs/proposed-<workflow>.yml` и дай пошаговую инструкцию, как вручную скопировать его в `.github/workflows/<workflow>.yml`.

Проверь запуск:
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

Use this at the end of a long web-chat working session. Do not reopen `START_HERE.md` just to reread it; update it only if memory actually needs to change.

```text
Посмотри на всю работу в этом чате целиком.

Оцени, что получилось хорошо, где мы потеряли время, где была путаница, и какие правила или файлы памяти могут сбить следующий чат.

Не открывай START_HERE.md заново только ради чтения, если он уже был открыт в начале чата. Но если выводы сегодняшнего чата нужно сохранить в долговременную память, измени START_HERE.md, frontier/latest.*, docs/web-chat-runbook-prompts.md, plan docs или другие файлы.

Особенно проверь третий шаг: мог ли чат сам создать workflow, был ли manual fallback, не был ли случайно скопирован markdown plan вместо YAML, какие inputs реально нужны для smoke и full.

В конце коротко скажи: что изменил, зачем изменил, какой следующий шаг теперь записан в памяти проекта, и какие четыре промпта лучше использовать дальше.
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
