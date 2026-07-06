# Web-chat runbook prompts

This file is for ChatGPT web-chat work on this repository. It is not a mathematical proof. It is a compact operating memory so the next chat spends fewer steps rediscovering the same workflow.

## Main process rule

The project uses four web-chat steps:

```text
1. Record a completed run.
2. Think creatively and choose the next hypothesis.
3. Prepare the GitHub launch package for that already chosen hypothesis.
4. Review the chat and update memory.
```

Important distinction:

- Step 2 is the research/fantasy/checking step.
- Step 3 is not a new research step. Step 3 must not re-test, re-argue, or replace the chosen hypothesis unless the requested launch is technically impossible. Step 3 is where the assistant implements the chosen hypothesis as runnable launch files. That may include writing a new engine/generator/checker/summary builder if the chosen hypothesis requires it.
- Step 4 is where retrospective memory cleanup belongs.

## What the recent web-chat process showed

The slow part was not only the math search itself. The slow part was repeatedly reconstructing project state from scattered files and occasionally confusing a planned workflow with a workflow that actually exists in GitHub.

Best optimization: in a new chat, read `START_HERE.md` once at the very beginning, during prompt 1. After that, do not reopen it in prompts 2, 3, and 4 unless the user explicitly says this is a new chat, memory was lost, or the earlier context is clearly missing.

Do not treat "all runs" as a request to blindly scan everything. First use the saved frontier and run summaries as the index. Then inspect only the exact run folders, workflow, bank additions, originals, and artifacts that are relevant to the current frontier.

Important correction from 2026-07-07: the launch-preparation prompt was too long and pulled the assistant back into hypothesis testing. It has been simplified. In prompt 3, do not do new local experiments or creative exploration. Only prepare the launch package for the hypothesis already chosen in prompt 2. Creating a new engine is allowed when it is the technical implementation of that chosen hypothesis.

Important correction from 2026-07-07: `smart-search-17-cover64-stitch-graph` is a line-set scaffold search, not a trail proof. Do not merge its outputs into the normal ordered-trail bank until they are converted into checked polygonal-trail candidates.

## Fast checklist before preparing or analyzing a launch

Use this checklist only as a technical guardrail. Do not turn it into a new research phase.

```text
1. Use the already-opened context from prompt 1 and prompt 2.
2. Confirm the chosen hypothesis and workflow name from prompt 2 or frontier/latest.*.
3. Create/update the launch implementation: workflow, proposed backup if needed, new or existing engine/generator, checker, summary builder, seed/input files, plan doc.
4. Writing a new engine/script is allowed if it directly implements the already chosen hypothesis. Do not use that as permission to choose a different hypothesis.
5. Update frontier/latest.* only if it is needed to store the exact prepared launch inputs/current workflow pointer.
6. Do not update START_HERE.md during prompt 3 unless the user explicitly asks or the next chat would otherwise lose the launch package. Normal memory cleanup belongs in prompt 4.
7. Verify real workflow YAML begins with name: and is workflow_dispatch-only.
8. Verify no push trigger.
9. Verify artifact names, seed paths, engine/checker/summary paths, shard count, and exact inputs.
10. Stop. Give smoke-test and full-run inputs. Do not run extra hypothesis checks unless the workflow cannot be made technically runnable.
```

## Prompt 1 — record completed run

Use when a main/full GitHub run has completed and needs to be recorded. This is normally the boot prompt for a fresh web chat.

```text
Сними результаты завершённого GitHub run: <RUN_URL>.

Это начало нового рабочего чата, поэтому сначала открой START_HERE.md как долговременную память проекта. Затем открой frontier/latest.md, frontier/latest.json, docs/web-chat-runbook-prompts.md, workflow этого run, artifacts, jobs/logs и нужные runs/candidates.

Запиши результат в репозиторий и сделай коммит:
- runs/<date>-<workflow>/summary.md и нужные json/jsonl;
- frontier/latest.md и frontier/latest.json;
- START_HERE.md, если изменилась долговременная память;
- candidate additions/originals, если появились новые кривые или важные shard-best записи.

В конце коротко скажи:
1. лучший результат было/стало;
2. сколько shard-best кривых получили;
3. сколько новых compact/original кандидатов записали;
4. какие дырки или defect-family повторялись;
5. какой следующий не-повторяющийся шаг.
```

## Prompt 2 — choose next hypothesis

This is the only step where broad thinking, fantasy, and local exploratory checks are expected.

```text
Теперь сделай следующий исследовательский шаг: подумай, куда нам идти дальше.

START_HERE.md уже был открыт в этом чате, не открывай его заново. Опирайся на уже открытый контекст: последний записанный run, frontier, run summaries, candidate banks, originals, artifacts и новые источники, которые я добавил.

Не своди задачу к повтору прошлого workflow. Посмотри шире: какие структуры мы могли не заметить, где может быть новый источник кривых, какие старые стены повторяются.

Выбери одну гипотезу и, если это полезно, проверь её маленькими локальными проверками прямо в чате. Доведи идею до состояния, где её можно превратить в GitHub launch package.

В конце коротко скажи: какая гипотеза выбрана, почему она не повтор прошлого, что показали проверки, и стоит ли готовить под неё большой GitHub-прогон.
```

## Prompt 3 — prepare launch package only

Use after prompt 2, when the hypothesis is already chosen. This prompt is intentionally short and technical.

```text
Подготовь GitHub launch package под уже выбранную гипотезу из предыдущего шага.

START_HERE.md уже был открыт в этом чате, не открывай его заново. Не придумывай новую гипотезу и не запускай дополнительные исследовательские проверки. Сейчас задача техническая: реализовать выбранную гипотезу в файлах запуска, чтобы я мог нажать Run.

Создай или обнови технические файлы запуска. Если для выбранной гипотезы нужен новый движок/скрипт, напиши новый движок/скрипт — это нормально. Но не меняй саму исследовательскую идею.

Обычно нужны:
- workflow в .github/workflows/ или точный proposed YAML в docs/;
- engine/generator;
- checker;
- summary builder;
- seed/input files;
- plan doc, если нужен для запуска.

Не делай ретроспективный анализ и обычно не трогай START_HERE.md. Если нужно записать exact launch inputs/current workflow pointer, обнови frontier/latest.* или runbook; долговременную чистку памяти оставь для prompt 4.

Проверь только техническую готовность:
- workflow начинается с name:;
- workflow_dispatch-only, без push;
- 20 jobs/shards и правильный max-parallel, если это full search;
- seed paths, engine/checker/summary paths совпадают;
- artifact names совпадают;
- smoke и full inputs записаны.

В конце дай только:
1. что создано/обновлено;
2. готов ли workflow к ручному запуску;
3. exact inputs для smoke-test;
4. exact inputs для full run.

Ничего не запускай автоматически, если я явно не попросил.
```

## Prompt 4 — whole-chat wrap-up

Use at the end of a long web-chat working session.

```text
Посмотри на всю работу в этом чате целиком.

START_HERE.md уже был открыт в начале чата, не открывай его заново только ради чтения. Но если выводы сегодняшнего чата нужно сохранить в долговременную память, измени START_HERE.md, frontier/latest.*, docs/web-chat-runbook-prompts.md, plan docs или другие файлы.

Оцени:
- что получилось хорошо;
- где мы потеряли время;
- где была путаница;
- какие правила или файлы памяти могут сбить следующий чат.

Особенно проверь prompt 3: он должен готовить запуск, а не заново исследовать гипотезу.

В конце коротко скажи:
1. что изменил;
2. зачем изменил;
3. какой следующий шаг теперь записан в памяти проекта;
4. какие промпты лучше использовать дальше.
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
