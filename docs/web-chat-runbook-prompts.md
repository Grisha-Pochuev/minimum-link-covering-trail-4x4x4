# Web-chat runbook prompts

This file is the operating memory for ChatGPT web-chat work on this repository. It is not a mathematical proof and should not duplicate full run archives.

## File roles

- `START_HERE.md`: stable boot memory and reading order.
- `frontier/latest.md` and `frontier/latest.json`: best checked mathematical frontier.
- `frontier/active_run.json`: current operational run or completed run awaiting recording.
- `docs/web-chat-runbook-prompts.md`: reusable process rules and prompts.
- `docs/smart-search-N-*.md`: exact Step-2 to Step-3 handoff for one numbered search.
- `runs/*`: completed-run evidence.
- candidate banks/originals: reusable checked and diagnostic curves.

## Main process rule

The project uses four web-chat steps:

```text
1. Record a completed run.
2. Think creatively, test locally and choose one next hypothesis.
3. Implement that chosen hypothesis, run smoke, then launch full.
4. Review the chat and improve project memory/process.
```

Important distinction:

- Step 2 is research and selection.
- Step 3 is implementation, verification and launch. It must not replace the chosen primary hypothesis.
- Step 3 ends only after smoke passes and the intended full run is visible with green precheck and all expected shard jobs.
- Step 4 records process lessons without changing the historical run commit or launching another run.

## Naming and one-workflow rule

Every serious numbered search uses:

```text
smart-search-N-short-description
```

The suffix should be short, normally one or two descriptive words. Keep exactly one visible GitHub Actions workflow for each `N`. Never create a second bootstrap, launcher, smoke-only workflow or duplicate workflow carrying the same number.

One workflow should contain precheck, smoke/full profiles, search shards, exact checking, aggregation and artifacts.

## Step-2 handoff contract

Before Step 3 starts, persist the selected hypothesis in a launch/plan document. The document must contain:

```text
1. next unused search number and final workflow name;
2. one primary hypothesis;
3. optional modes clearly marked as optional;
4. exact input seeds and source runs;
5. local test commands and observed results;
6. invariants, especially link count and exact-arithmetic requirements;
7. smoke acceptance gate;
8. fixed full resource profile;
9. expected per-shard and aggregate artifacts;
10. implementation-language choice and reason.
```

Step 3 should implement this contract. It may fix technical mistakes, but it should not broaden the search without a concrete reason.

## Scope-control rule

A serious run should have one primary mechanism. Supporting modes are allowed, but they should not turn the run into several unrelated searches.

Prefer:

```text
one main hypothesis
+ a few ablations or controls
+ one small control shard for the previous method
```

Avoid putting every interesting idea from Step 2 into the same workflow.

## Local dry-run gate before GitHub smoke

Before committing the first smoke trigger:

```text
1. compile every source file;
2. verify the known 23-link full control;
3. verify every new frontier seed with both exact checkers;
4. run every shard mode briefly in a local sequential test;
5. run the aggregate/summary builder on miniature outputs;
6. verify artifact paths and all three bank outputs;
7. confirm all states keep the required number of nonzero links.
```

Do not spend 20 GitHub jobs merely to discover a syntax error, missing seed, wrong path or broken aggregator.

## Readable-source rule

New engines should be ordinary readable source files.

If a connector rejects one large file, split the engine into normal importable modules such as:

```text
geometry.py
state.py
modes.py
search.py
output.py
```

Do not prefer compressed payloads, encoded source or runtime concatenation of arbitrary fragments.

Search-22 used `scripts/endpoint_repair_parts/part-*.pyfrag` because the connector blocked a large single upload. Its full run has completed from an immutable historical commit. After Prompt 1 records the run, refactor this layout into normal Python modules before extending it for search-23.

## Mandatory Step-3 automatic launch rule

When Step 3 is requested after a hypothesis has been selected:

```text
1. Implement the handoff contract in one complete workflow.
2. Run the local dry-run gate.
3. Commit implementation first.
4. Launch smoke through the same workflow.
5. Wait for smoke aggregate, not just green precheck.
6. Require all intended smoke shard artifacts and exact checks.
7. Only then launch full through the same workflow.
8. Verify full profile, green precheck and creation of all shard jobs.
9. Record the run in frontier/active_run.json.
10. Do not launch a duplicate.
```

Normal serious full profile:

```text
seconds=21000
shards=20
max-parallel=20
workers=4 per shard
```

A different worker count requires a documented technical reason. All full parameters must resolve inside YAML.

If the connector exposes true `workflow_dispatch`, use it. Otherwise the same workflow may watch narrow trigger files:

```text
launch/smart-search-N-smoke.trigger
launch/smart-search-N-full.trigger
```

Do not create a separate launcher workflow.

## Trigger-isolation rule

Generic or legacy workflows must use narrow `paths:` filters. Commits changing only launch triggers, docs, memory, run archives, candidate banks or unrelated numbered-search files must not start old short searches.

## Fast technical checklist

```text
1. Use already-opened START_HERE/frontier context.
2. Read frontier/active_run.json and do not duplicate an active or completed-unrecorded run.
3. Confirm selected hypothesis, next unused number and final visible name.
4. Confirm no second workflow already uses that number.
5. Confirm the Step-2 launch/plan document exists.
6. Implement normal readable modules, seeds, workflow, checker and summary builder.
7. Run the local dry-run gate.
8. Confirm smoke and full values inside YAML.
9. Commit implementation.
10. Trigger smoke in the same workflow.
11. Check smoke aggregate, all shard artifacts and exact verification.
12. Trigger full only after smoke passes.
13. Check full profile, green precheck and all shard jobs.
14. Update frontier/active_run.json and stop.
```

## Failure handling

Distinguish:

```text
- engine/search step failed: inspect logs and fix code or inputs;
- checker failed: candidate may be invalid or serialization may be wrong;
- aggregation failed: search results may still be useful, inspect shard artifacts;
- artifact missing: record exactly which shard is absent;
- failed run predates a fix commit: launch a fresh run from main rather than rerunning stale code.
```

Never describe a failed checker as a mathematical negative result.

## Prompt 1 — record completed run

```text
Сними результаты завершённого GitHub run: <RUN_URL>.

Это начало нового рабочего чата, поэтому сначала один раз открой START_HERE.md как долговременную память проекта. Затем открой frontier/latest.*, frontier/active_run.json, docs/web-chat-runbook-prompts.md, workflow этого run, artifacts, jobs/logs и нужные runs/candidates.

Запиши результат в репозиторий и сделай коммит:
- runs/<date>-<workflow>/summary.md и нужные json/jsonl;
- frontier/latest.md и frontier/latest.json;
- frontier/active_run.json: пометь результат как записанный и убери состояние pending;
- START_HERE.md, если изменилась долговременная память;
- candidate additions/originals, если появились новые кривые или важные shard-best записи.

В конце коротко скажи:
1. лучший результат было/стало;
2. сколько shard-best кривых получили;
3. сколько compact/original кандидатов записали;
4. какие дырки или defect-family повторялись;
5. какой следующий неповторяющийся шаг.
```

## Prompt 2 — choose next hypothesis

```text
Теперь сделай следующий исследовательский шаг: подумай, куда нам идти дальше.

START_HERE.md уже был открыт в этом чате, не открывай его заново. Опирайся на последний полностью записанный run, frontier, candidate banks, originals и artifacts.

Не начинай Step 2, если frontier/active_run.json говорит completed_success_pending_recording. Сначала выполни Prompt 1.

Не повторяй прошлый workflow. Выбери одну главную гипотезу и проверь её маленькими локальными тестами. Не складывай все интересные идеи в один будущий прогон.

До конца шага создай или обнови docs/smart-search-N-<name>-launch.md: точная гипотеза, seeds, локальные результаты, инварианты, выбранные режимы, smoke gate, full profile и artifacts.

В конце коротко скажи: какая гипотеза выбрана, почему она не повтор прошлого, что показали проверки и стоит ли запускать большой прогон.
```

## Prompt 3 — implement and launch

```text
Подготовь и автоматически запусти GitHub-прогон по уже сохранённому Step-2 handoff.

START_HERE.md уже был открыт. Не придумывай новую основную гипотезу. Реализуй один workflow smart-search-N-короткая-характеристика.

Сначала выполни локальный dry-run всех режимов и агрегации. Затем запусти smoke. Полный прогон запускай только после успешного smoke aggregate, всех ожидаемых shard artifacts и точных проверок.

Основной full: 21000 секунд, 20 shards/jobs, max-parallel=20, обычно 4 workers/job. Все параметры находятся внутри YAML.

После запуска full проверь правильное имя/profile, precheck success и все 20 shard jobs. Запиши run в frontier/active_run.json. Не запускай копию.
```

## Prompt 4 — whole-chat wrap-up

```text
Посмотри на всю работу в этом чате целиком.

START_HERE.md уже был открыт. Проверь потери времени, путаницу ролей файлов, лишние workflow-запуски, слишком широкий scope, непрозрачную упаковку исходников и незаписанные результаты.

При необходимости измени START_HERE.md, frontier/active_run.json, docs/web-chat-runbook-prompts.md, launch/plan docs или другие файлы. Не меняй исторический commit уже запущенного или завершённого run.

Если run завершился во время Step 4, пометь его completed_success_pending_recording и сделай Prompt 1 следующим обязательным шагом, но не подменяй полноценный анализ результатов поверхностной записью.

В конце коротко скажи: что изменил, зачем изменил и какой следующий шаг записан.
```

## Current project state

```text
best recorded checked ordered trail: 62/64
candidate: mlct22-er-943c78ae82c82664
missing: (2,3,1), (3,3,1)
source smoke run: 29181400035
full run: 29181546758
full run status: completed success, pending Prompt-1 recording
workflow: .github/workflows/smart-search-22-endpoint-repair.yml
full profile: 21000 seconds, 20 shards, max-parallel=20, workers=4
```

Run Prompt 1 for `29181546758` now. Do not launch another search and do not choose search-23 until the full artifacts are recorded.
