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
- Step 3 is not a new research step. Step 3 must not re-test, re-argue, or replace the chosen hypothesis unless the requested launch is technically impossible. Step 3 implements the chosen hypothesis as runnable launch files. Writing a new engine/generator/checker/summary builder is allowed if the chosen hypothesis requires it.
- Step 4 is where retrospective memory cleanup belongs.

## Naming rule for serious searches

Serious numbered search workflows and run folders should keep this family format:

```text
smart-search-N-short-description
```

Examples already in the repository:

```text
smart-search-11-d2-bridge-repair
smart-search-12-skeleton-diversity
smart-search-19-contact-state-dp
smart-search-20-line-bridge
```

The suffix should be short, ideally one or two descriptive words, but do **not** drop the `smart-search-N` prefix.

## What the recent web-chat process showed

Do not treat "all runs" as a request to blindly scan everything. First use `START_HERE.md`, `frontier/latest.*`, and run summaries as the index. Then inspect only the exact run folders, workflow, bank additions, originals, and artifacts that are relevant to the current frontier.

Important correction from 2026-07-07: `smart-search-17-cover64-stitch-graph` outputs are line-set scaffolds, not trail proofs. Do not merge them into the normal ordered-trail bank until they are converted into checked polygonal-trail candidates.

Result from run `28825060197`: full search-17 found `64/64` unordered 22-line scaffolds and 4 compact representatives with stitch path lower bound `22/22`. This changed the bottleneck from finding rich scaffolds to ordered reconstruction.

Result from run `28875314204`: search-18 tried ordered reconstruction from search-17 scaffolds. It completed successfully, but the best checked ordered-chain reconstruction was only `44/64`, far below the standing ordered-trail frontier `60/64`.

Result from run `28903545221`: full-duration search-19 completed successfully and improved the diagnostic ordered reconstruction only `44/64 -> 46/64`. Dominant failure: rich-line clipping, not the old four-hole `60/64` wall.

Result from run `28973760924`: full `smart-search-20-line-bridge` completed successfully. It preserved rich full lines much better and improved the diagnostic ceiling `46/64 -> 58/64`, but did not improve the ordered-trail frontier `60/64`. Best candidate `mlct22-flbridge-8da0e01c34bb9c88` has `22` links, covers `58/64`, preserves `14` rich lines, uses `8` bridge links, and hits all 4 old missing points from the official `60/64` candidate. New best missing set: `(0,2,0)`, `(0,2,2)`, `(2,1,0)`, `(2,1,2)`, `(2,3,0)`, `(3,2,0)`.

Search-20 lesson: preserving full rich lines helps, but the explicit bridge budget is still too expensive. Do not rerun search-20 unchanged.

## Fast checklist before preparing or analyzing a launch

Use this checklist only as a technical guardrail. Do not turn it into a new research phase.

```text
1. Use the already-opened context from prompt 1 and prompt 2.
2. Confirm the chosen hypothesis and workflow name from prompt 2 or frontier/latest.*.
3. Confirm the workflow name follows smart-search-N-short-description.
4. Create/update the launch implementation: workflow, proposed backup if needed, new or existing engine/generator, checker, summary builder, seed/input files, plan doc.
5. Writing a new engine/script is allowed if it directly implements the already chosen hypothesis. Do not use that as permission to choose a different hypothesis.
6. Update frontier/latest.* only if it is needed to store the exact prepared launch inputs/current workflow pointer.
7. Do not update START_HERE.md during prompt 3 unless the user explicitly asks or the next chat would otherwise lose the launch package. Normal memory cleanup belongs in prompt 4.
8. Verify real workflow YAML begins with name: and is workflow_dispatch-only.
9. Verify no push trigger.
10. Verify artifact names, seed paths, engine/checker/summary paths, shard count, and exact inputs.
11. If asked to run automatically, use a real workflow_dispatch action only if the connector/tool exposes it. If no such tool exists, say that honestly and give the exact manual Run workflow inputs.
12. Stop. Give smoke-test and full-run inputs. Do not run extra hypothesis checks unless the workflow cannot be made technically runnable.
```

If a smoke-test fails red, first distinguish:

```text
- engine/search step failed: inspect logs and fix the engine or inputs;
- post-search checker/summary step failed: this may be a workflow plumbing bug, not a mathematical failure;
- old failed run was before a fix commit: start a fresh Run workflow from main, not Re-run failed jobs.
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

Use this only when the previous prepared launch has already been tried or intentionally abandoned. This is the only step where broad thinking, fantasy, and local exploratory checks are expected.

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

Создай или обнови технические файлы запуска. Если для выбранной гипотезы нужен новый движок/скрипт, напиши новый движок/скрипт — это нормально. Но не меняй саму исследовательскую идею. Название прогона делай в формате smart-search-N-короткая-характеристика.

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

Если я прошу запустить автоматически, запускай только если доступен настоящий workflow_dispatch-инструмент. Если такого инструмента нет, не притворяйся, что запустил: скажи, что запуск вручную через Actions → workflow → Run workflow, и дай exact inputs.
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

Особенно проверь prompt 3: он должен готовить запуск, а не заново исследовать гипотезу. Если был красный smoke-test, проверь, не является ли он технической ошибкой workflow/checker и не нужно ли зафиксировать "fresh Run workflow from main, not Re-run failed jobs".

В конце коротко скажи:
1. что изменил;
2. зачем изменил;
3. какой следующий шаг теперь записан в памяти проекта;
4. какие промпты лучше использовать дальше.
```

## Current state after `smart-search-20-line-bridge`

Current frontier:

```text
best ordered-trail candidate: 60/64, run 28674416173
best unordered cover64 scaffold: 64/64 line-set, run 28825060197
latest recorded completed full run: 28973760924, smart-search-20-line-bridge
latest recorded full-run best line-bridge diagnostic: 58/64
ordinary candidate-bank additions from search-20: 0
diagnostic line-bridge rows from search-20: 6
originals index rows from search-20: 6
```

Saved search-20 files:

```text
runs/2026-07-09-smart-search-20-line-bridge-full/summary.md
runs/2026-07-09-smart-search-20-line-bridge-full/best_line_bridge_candidate.json
runs/2026-07-09-smart-search-20-line-bridge-full/line_bridge_run_summary_compact.json
runs/2026-07-09-smart-search-20-line-bridge-full/mode_breakdown.json
candidates/diagnostic-line-bridge-run28973760924.jsonl
candidates/originals/run28973760924-line-bridge-index.jsonl
```

Next prompt:

- use Prompt 2;
- choose a new non-repeating hypothesis;
- do not rerun search-20 unchanged;
- key lesson to use: full-line preservation repairs the old four-hole wall, but explicit bridge cost creates a new six-hole bridge-defect family.
