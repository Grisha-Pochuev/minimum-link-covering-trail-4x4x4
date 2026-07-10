# Web-chat runbook prompts

This file is for ChatGPT web-chat work on this repository. It is a compact operating memory, not a mathematical proof.

## Main process rule

The project uses four web-chat steps:

```text
1. Record a completed run.
2. Think creatively and choose the next hypothesis.
3. Implement that chosen hypothesis and automatically launch the full GitHub run.
4. Review the chat and update memory.
```

Important distinction:

- Step 2 is the research/fantasy/checking step.
- Step 3 is technical execution. It must not replace the chosen hypothesis with another one.
- Step 3 ends only after the intended full run is visible in Actions and its precheck/start state has been verified.
- Step 4 is retrospective memory cleanup.

## Naming and one-workflow rule

Every serious numbered search uses:

```text
smart-search-N-short-description
```

The suffix should be short, ideally one or two descriptive words. Keep the `smart-search-N` prefix.

Examples:

```text
smart-search-19-contact-state-dp
smart-search-20-line-bridge
smart-search-21-bridge-compress
```

For each number `N`, keep exactly one visible GitHub Actions workflow. Never create a second `bootstrap`, `launcher`, smoke-only workflow, or another workflow carrying the same number.

A technical filename may differ for historical reasons, but the workflow's visible `name:` must follow the serious-run naming rule. Search-21 currently lives in `.github/workflows/smart-search-21-bootstrap.yml`, but its visible name is `smart-search-21-bridge-compress`, and it contains the complete workflow itself.

## Mandatory Step-3 automatic launch rule

When Step 3 is requested after a hypothesis has been selected:

```text
1. Implement the chosen hypothesis in one complete workflow.
2. Include precheck, engine/generator, exact checker, aggregation and artifacts.
3. Use 20 shards/jobs and max-parallel=20 for a normal full search.
4. Put all full parameters inside YAML.
5. Full duration is seconds=21000, i.e. 5 h 50 min.
6. Normally use 4 workers per shard unless the engine has a documented reason not to.
7. Launch the full run automatically from the web chat when repository write access exists.
8. Verify that the intended full profile started, precheck passed, and all 20 shard jobs were created.
9. Do not launch a duplicate.
```

If the connector exposes a true `workflow_dispatch` action, use it.

If it does not expose `workflow_dispatch`, the same serious workflow must contain a narrow push trigger watching:

```text
launch/smart-search-N-full.trigger
```

Then launch by committing that trigger file after the workflow implementation has been committed. Do not create a separate launcher workflow.

The push-triggered path must resolve automatically to `profile=full`. Manual `Run workflow` should also default to `full`. Custom numeric boxes may remain blank because they are used only by `profile=custom`.

## Fast technical checklist

```text
1. Read the already-opened START_HERE/frontier context.
2. Confirm the selected hypothesis and next unused number N.
3. Confirm the visible name is smart-search-N-short-description.
4. Confirm no second workflow already uses N.
5. Implement workflow, engine, checker, summary builder, seeds and plan as needed.
6. Compile/check scripts before spending GitHub time.
7. Confirm full: seconds=21000, 20 shards, max-parallel=20, normally workers=4.
8. Confirm seed paths, artifact names and checker inputs match.
9. Commit implementation first.
10. Trigger the same workflow automatically.
11. Inspect Actions: correct run name/profile, green precheck, 20 shard jobs.
12. Stop; do not start another copy.
```

If a run fails red, distinguish:

```text
- engine/search step failed: inspect logs and fix engine or inputs;
- checker/summary failed after search: may be workflow plumbing, not mathematical failure;
- failed run predates a fix commit: start a fresh run from main, not Re-run failed jobs.
```

## Prompt 1 — record completed run

```text
Сними результаты завершённого GitHub run: <RUN_URL>.

Это начало нового рабочего чата, поэтому сначала один раз открой START_HERE.md как долговременную память проекта. Затем открой frontier/latest.md, frontier/latest.json, docs/web-chat-runbook-prompts.md, workflow этого run, artifacts, jobs/logs и нужные runs/candidates.

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
5. какой следующий неповторяющийся шаг.
```

## Prompt 2 — choose next hypothesis

```text
Теперь сделай следующий исследовательский шаг: подумай, куда нам идти дальше.

START_HERE.md уже был открыт в этом чате, не открывай его заново. Опирайся на последний записанный run, frontier, run summaries, candidate banks, originals и artifacts.

Не повторяй прошлый workflow. Выбери одну новую гипотезу и при необходимости проверь её маленькими локальными проверками прямо в чате. Доведи идею до точного технического задания для GitHub-прогона.

В конце коротко скажи: какая гипотеза выбрана, почему она не повтор прошлого, что показали проверки и стоит ли запускать большой прогон.
```

## Prompt 3 — implement and launch

```text
Подготовь и автоматически запусти GitHub-прогон под уже выбранную гипотезу.

START_HERE.md уже был открыт в этом чате, не открывай его заново. Не придумывай новую гипотезу. Реализуй выбранную идею в одном полном workflow с названием smart-search-N-короткая-характеристика.

Не создавай отдельный bootstrap/launcher и не создавай второй workflow с тем же номером. Если workflow_dispatch недоступен, добавь узкий push-trigger в этот же workflow и запусти full через launch/smart-search-N-full.trigger.

Основной full: 21000 секунд (5 ч 50 мин), 20 shards/jobs, max-parallel=20, обычно 4 workers/job. Все параметры full должны быть внутри YAML.

После запуска проверь Actions: правильное имя, profile=full, precheck success и 20 созданных shard jobs. В ответе дай ссылку на один главный run и коротко перечисли, что было создано.
```

## Prompt 4 — whole-chat wrap-up

```text
Посмотри на всю работу в этом чате целиком.

START_HERE.md уже был открыт в начале чата, не открывай его заново только ради чтения. Но если выводы нужно сохранить, измени START_HERE.md, frontier/latest.*, docs/web-chat-runbook-prompts.md, plan docs или другие файлы.

Проверь, не появились ли:
- два workflow с одним номером;
- отдельный launcher/bootstrap;
- ручные параметры, которые должны быть внутри full-профиля;
- незаписанные результаты или противоречивые правила.

В конце коротко скажи: что изменил, зачем изменил и какой следующий шаг записан в памяти проекта.
```

## Current project state

```text
best checked ordered-trail candidate: 61/64
candidate: mlct22-bc-889d7f8c45252068
source smoke run: 29123090565
active full run: 29123493808
active hypothesis: direct 23-link to 22-link bridge compression
single search-21 workflow file: .github/workflows/smart-search-21-bootstrap.yml
visible workflow name: smart-search-21-bridge-compress
full profile: 21000 seconds, 20 shards, max-parallel=20, workers=4
```

Do not duplicate active run `29123493808`. When it completes, use Prompt 1 before choosing another hypothesis.
