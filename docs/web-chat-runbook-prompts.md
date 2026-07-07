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

Important correction from 2026-07-07: `smart-search-17-cover64-stitch-graph` outputs are line-set scaffolds, not trail proofs. Do not merge them into the normal ordered-trail bank until they are converted into checked polygonal-trail candidates.

Result from 2026-07-07 run `28825060197`: full search-17 found `64/64` unordered 22-line scaffolds and 4 compact representatives with stitch path lower bound `22/22`. This changed the bottleneck from finding rich scaffolds to ordered reconstruction.

Result from 2026-07-07 run `28875314204`: full search-18 tried contact-aware ordered reconstruction from search-17 scaffolds. It completed successfully, but the best checked ordered-chain reconstruction was only `44/64`, far below the standing ordered-trail frontier `60/64`. This means the current reconstruction engine is too weak; the next step should diagnose contact/coverage loss and design a stronger contact-state reconstruction model, not rerun search-18 unchanged.

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

## Current state after search-18

As of the completed result-taking step for run `28875314204`, there is no prepared next launch package yet.

Current frontier:

```text
best ordered-trail candidate: 60/64, run 28674416173
best unordered cover64 scaffold: 64/64 line-set, run 28825060197
latest full run: 28875314204, smart-search-18-order-from-cover64-stitch
latest full run best ordered reconstruction: 44/64
ordinary candidate-bank additions from search-18: 0
diagnostic ordered-chain rows from search-18: 17
```

Saved files:

```text
runs/2026-07-07-smart-search-18-order-from-cover64-stitch-full/summary.md
runs/2026-07-07-smart-search-18-order-from-cover64-stitch-full/best_ordered_candidate.json
runs/2026-07-07-smart-search-18-order-from-cover64-stitch-full/mode_breakdown.json
runs/2026-07-07-smart-search-18-order-from-cover64-stitch-full/order-cover64-stitch-run-summary.zip
candidates/diagnostic-order-from-cover64-run28875314204.jsonl
candidates/originals/run28875314204-order-from-cover64-index.jsonl
```

Next prompt should be Prompt 2: choose a new hypothesis. A likely direction is stronger contact-state reconstruction from search-17 scaffolds, using actual covered-mask preservation during ordering, not only abstract line-set graph pathability.
