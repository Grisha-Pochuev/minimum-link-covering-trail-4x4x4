# Web-chat runbook prompts

This file is the operating memory for ChatGPT web-chat work on this repository. It defines process, not mathematical truth. Current state belongs in `START_HERE.md`, `frontier/latest.*` and `frontier/active_run.json`; do not append a stale project-status snapshot here.

## File roles

- `START_HERE.md`: compact boot memory and reading order.
- `frontier/latest.md` and `frontier/latest.json`: best checked mathematical frontier.
- `frontier/active_run.json`: current operational run, pending recording state or selected next search.
- `docs/web-chat-runbook-prompts.md`: reusable four-step process rules.
- `docs/smart-search-N-*.md`: exact Step-2 to Step-3 handoff for one numbered search.
- `docs/retrospectives/*`: process lessons.
- `runs/*`: completed-run evidence.
- candidate banks/originals: reusable checked and diagnostic curves.

## Fixed four-step process

```text
1. Record a completed run.
2. Think creatively, test locally and choose one next hypothesis.
3. Implement the chosen hypothesis and automatically execute preflight -> smoke -> full.
4. Review the chat and improve project memory/process.
```

Important distinctions:

- Step 2 is research and selection.
- Step 3 is implementation, validation and launch. It must not replace the selected primary hypothesis.
- Step 3 is one user-prompt transaction. It ends only after full is launched with the intended profile, green precheck and all expected shard jobs.
- Step 4 records process lessons without changing the historical commit of an active or completed run.

## Naming and one-workflow rule

Every serious numbered search uses:

```text
smart-search-N-short-description
```

Keep exactly one visible GitHub Actions workflow for each `N`. Never create a second bootstrap, launcher or smoke-only workflow with the same number.

One workflow owns precheck, smoke, smoke aggregate, full, exact checks, full aggregate and artifacts.

## Step-2 handoff contract

Before Step 3 starts, persist the selected hypothesis in a launch document containing:

```text
1. next unused search number and final workflow name;
2. one primary hypothesis;
3. optional modes clearly marked as controls or ablations;
4. exact input seeds and source runs;
5. local tests and observed results;
6. invariants, especially link count and exact arithmetic;
7. one shared preflight command;
8. smoke acceptance gate;
9. automatic smoke-to-full workflow shape;
10. fixed full resource profile;
11. expected per-shard and aggregate artifacts;
12. implementation language and reason.
```

Step 3 implements this contract. It may fix technical errors but must not broaden the scientific search without a concrete recorded reason.

## Scope control

Prefer:

```text
one primary mechanism
+ a few controlled variants
+ one small previous-method control
```

Do not put every idea from Step 2 into one expensive run.

## Shared preflight rule

Each numbered search must provide one versioned preflight entry point, for example:

```text
scripts/preflight_searchN.py
```

or an equivalent shell command.

The exact same command and files must be used locally and in GitHub precheck. It must:

```text
1. compile every source file;
2. verify the known 23-link full control;
3. normalize and verify every required seed with both exact checkers;
4. reconstruct any structural invariants required by the launch document;
5. run every shard mode briefly;
6. run the real aggregate builder on miniature outputs;
7. verify artifact paths and all three bank outputs;
8. assert exactly 22 nonzero links for every emitted state.
```

Do not maintain separate local and CI test logic that can drift.

### Seed schema rule

Define one canonical internal seed schema. Normalize compact/historical rows before checkers and search code.

Do not assume redundant fields such as `links` exist when `23` ordered vertices already determine `22` links. Checkers may derive redundant values, but must verify them when explicitly present.

## Readable-source and coherent-commit rule

New engines must use ordinary readable modules.

Do not use encoded payloads or runtime concatenation of arbitrary source fragments.

Prepare the complete coherent implementation locally, then publish it as:

1. one atomic Git tree commit when blob/tree/commit/ref operations are available; or
2. the smallest practical number of coherent commits.

Avoid long chains of one-file commits. They clutter provenance and increase exposure to transient connector or safety-layer failures.

## Permanent-input rule

All permanent seed data, manifests and source files required by the run must be committed before the smoke trigger.

A scientific workflow must be read-only with respect to repository source and seeds. It may upload artifacts, but precheck or shard jobs must not commit generated source or seed material back to `main`.

Reason: self-modifying workflows advance the branch while the active run still executes its original commit, creating provenance and race problems.

## Mandatory single-prompt Step 3

When Step 3 is requested after Step 2 is complete, the request authorizes the whole chain:

```text
1. Read the saved handoff and active-run state.
2. Implement one numbered workflow and normal source modules.
3. Run the shared preflight locally.
4. Publish one coherent implementation commit.
5. Trigger the automatic profile.
6. Run precheck.
7. Run smoke on all intended shards.
8. Require smoke aggregate, exact checks and every expected artifact.
9. Automatically start full after the smoke gate succeeds.
10. Verify full profile, green precheck and creation of all 20 shard jobs.
11. Record launch identity in frontier/active_run.json.
12. Stop without requiring another user prompt or launch click.
```

The assistant must not finish Step 3 merely because smoke was launched.

If smoke fails and repository permissions allow a fix, diagnose, correct and restart the chain during the same Step-3 work. Do not ask the user to supply the smoke URL or send a separate command merely to launch full.

## Preferred automatic workflow architecture

For future numbered searches, normal Step 3 uses one `auto` profile or one narrow `auto.trigger`:

```text
precheck
  -> smoke matrix [20]
  -> smoke-aggregate
  -> full matrix [20]      needs smoke-aggregate; runs only on success
  -> full-aggregate
```

Manual `smoke` and `full` profiles may remain for debugging and recovery, but they are not the normal user-facing Step-3 path.

The full matrix jobs use their own `timeout-minutes=359`; the preceding smoke jobs do not consume that per-job limit.

Normal serious full profile:

```text
seconds=21000
shards=20
max-parallel=20
workers=4 per shard
```

A different worker count requires a documented technical reason. All parameters resolve inside YAML.

If true `workflow_dispatch` is unavailable, use one narrow path such as:

```text
launch/smart-search-N-auto.trigger
```

Do not create a separate launcher workflow.

## Aggregate dependency rule

The scientific aggregate must run only after all required shard jobs succeed and artifacts exist.

A lightweight failure-report job may use `if: always()`, but it must not run the normal aggregator against missing outputs.

## Trigger safety and duplicate prevention

Before any smoke, auto or full trigger:

```text
1. read frontier/active_run.json;
2. inspect the trigger path and latest commit;
3. confirm no active or completed-unrecorded run uses the same search number/profile;
4. write the trigger once;
5. record the launch commit immediately;
6. never repeat the trigger merely because the run ID is not yet visible.
```

A ChatGPT connector safety block is not proof that GitHub Actions rejected or forbids the launch.

When a write is blocked:

- determine whether it was a trigger or a non-trigger write;
- inspect repository and Actions state before retrying;
- reduce or clarify the payload;
- prefer an atomic explicit commit;
- retry only when no equivalent write or run exists.

Never conflate connector safety warnings, GitHub CI failures and mathematical search results.

## Trigger isolation

Generic and legacy workflows must use narrow `paths:` filters. Commits changing docs, memory, run archives, candidate banks or another numbered search must not start old workflows.

## Failure handling

Distinguish:

```text
- preflight/checker failure: code, schema or candidate serialization problem;
- engine/search failure: inspect shard logs and inputs;
- aggregation failure after successful shards: shard results may still be useful;
- missing artifact: record the exact missing shard;
- connector safety block: tool-layer event, not CI evidence;
- failed run predates a fix commit: launch a fresh run from fixed main, not stale rerun.
```

Never describe a failed checker as a mathematical negative result.

## Fast Step-3 checklist

```text
1. Reuse already-opened START_HERE/frontier context.
2. Read frontier/active_run.json; do not duplicate.
3. Confirm selected hypothesis, unused number and final visible name.
4. Confirm exactly one workflow uses that number.
5. Confirm the Step-2 launch document exists.
6. Commit all permanent seeds before launch.
7. Implement readable modules, workflow, checkers and aggregation.
8. Run the same preflight command locally that CI will run.
9. Publish coherently, preferably one atomic tree commit.
10. Trigger auto once.
11. Check complete smoke aggregate and all artifacts.
12. Let full begin automatically.
13. Check intended full profile, green precheck and all 20 jobs.
14. Update frontier/active_run.json and stop.
```

## Prompt 1 — record completed run

```text
Сними результаты завершённого GitHub run: <RUN_URL>.

Это начало нового рабочего чата, поэтому сначала один раз открой START_HERE.md как долговременную память проекта. Затем открой frontier/latest.*, frontier/active_run.json, docs/web-chat-runbook-prompts.md, workflow этого run, artifacts, jobs/logs и нужные runs/candidates.

Запиши результат в репозиторий и сделай коммит:
- runs/<date>-<workflow>/summary.md и нужные json/jsonl;
- frontier/latest.md и frontier/latest.json;
- frontier/active_run.json: пометь результат как записанный и убери pending;
- START_HERE.md, если изменилась долговременная память;
- все три банка: ordinary, diagnostic и originals.

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

Не повторяй прошлый workflow. Выбери одну главную гипотезу и проверь её маленькими локальными тестами. Не складывай все идеи в один будущий прогон.

До конца шага создай или обнови docs/smart-search-N-<name>-launch.md: гипотеза, seeds, локальные результаты, общий preflight, инварианты, режимы, автоматический smoke-to-full gate, full profile и artifacts.

В конце коротко скажи: какая гипотеза выбрана, почему она не повтор прошлого, что показали проверки и стоит ли запускать большой прогон.
```

## Prompt 3 — implement and automatically launch

```text
Подготовь и автоматически выполни весь Step 3 по сохранённому Step-2 handoff одним заходом.

START_HERE.md уже был открыт. Не меняй основную гипотезу. Реализуй один workflow smart-search-N-короткая-характеристика и нормальные читаемые модули.

Сначала запусти общий локальный preflight, совпадающий с GitHub precheck. Затем один раз запусти auto-профиль: smoke, полный smoke aggregate и точные проверки должны автоматически открыть full-матрицу.

Основной full: 21000 секунд, 20 shards/jobs, max-parallel=20, обычно 4 workers/job. Все параметры находятся внутри YAML.

Не заканчивай шаг после запуска smoke и не проси у меня второе сообщение для запуска full. После старта full проверь profile, green precheck и все 20 shard jobs. Запиши active run и не запускай копию.
```

## Prompt 4 — whole-chat wrap-up

```text
Посмотри на всю работу в этом чате целиком.

START_HERE.md уже был открыт. Проверь потери времени, путаницу ролей файлов, лишние workflow-запуски, несовпадение local preflight и CI, self-modifying workflow, слишком много мелких коммитов, непрозрачные исходники и незаписанные результаты.

При необходимости измени START_HERE.md, frontier/active_run.json, docs/web-chat-runbook-prompts.md, launch/plan docs или другие файлы. Не меняй исторический commit уже запущенного или завершённого run.

Если run завершился во время Step 4, пометь его completed_success_pending_recording и сделай Prompt 1 следующим обязательным шагом, но не подменяй полноценный анализ результатов поверхностной записью.

В конце коротко скажи: что изменил, зачем изменил и какой следующий шаг записан.
```
