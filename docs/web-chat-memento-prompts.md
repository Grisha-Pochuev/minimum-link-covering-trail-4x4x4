# Web-chat Memento prompts

Always read `START_HERE.md` first. Then read `frontier/latest.md`, `frontier/latest.json`, the relevant workflow, docs/plans, candidate banks, runs, originals, and artifacts.

## Three-prompt loop

Use three prompts, not two.

```text
1. Diagnose the completed run. Repository writes are optional.
2. Save results and do a local chat preflight. This uses the chat/container only; it is not a GitHub Actions run.
3. Prepare the GitHub launch package: first a short manual GitHub smoke-test, then the full 20 jobs x 4 threads run for about 5h50m if the smoke-test is green.
```

Prompt 2 is local: static checks, small Python/YAML checks, generator sanity checks, seed-source consistency, artifact-name consistency, and any small test possible inside the chat environment.

Prompt 3 is manual GitHub launch preparation. It should give exact `workflow_dispatch` inputs for a short GitHub smoke-test first, and exact full-run inputs for after the smoke-test succeeds.

## Candidate terminology

1. Champion candidate: the single best candidate from one run, used for `frontier/latest.*` and easy reporting.
2. Per-run top candidates: useful candidates from this run, saved in the run folder.
3. Global compact memory: `candidates/bank.jsonl` and `candidates/bank-additions-*.jsonl`.
4. Original archive: `candidates/originals/`, without symmetry deduplication.

Normal saving threshold unless a workflow says otherwise:

```text
covered_count >= 56
links <= 22
```

## Prompt 1: diagnose a completed run only

```text
Прогон завершился: вставь ссылку на GitHub Actions run.

Сначала открой START_HERE.md. Затем открой workflow, которым был запущен именно этот run. Не подменяй workflow завершённого run самым новым workflow.

Сними результаты, но пока не обязан ничего записывать в репозиторий. Проверь jobs, logs и artifacts. Найди лучший covered_count из 64, links, mode, candidate_id, source artifact и пропущенные точки.

Сравни с frontier/latest.md, frontier/latest.json, последними runs/, candidates/bank.jsonl, bank-additions и candidates/originals/.

Главная цель этого шага — понять, что произошло: улучшился ли frontier, сколько было shard-best кандидатов, какие defect patterns повторяются, какие точки чаще всего пропущены, какие режимы дали пользу, были ли ошибки workflow/artifacts/aggregation, и отличается ли новый результат от старых семейств.

Не делай большой коммит, если диагностика уже длинная. В конце дай короткий отчёт и отдельный план сохранения: какие файлы надо создать или обновить на следующем шаге, какие кандидаты надо сохранить, надо ли менять START_HERE.md, и какую гипотезу стоит проверить локально в чате перед большим GitHub-запуском.
```

## Prompt 2: save results and do local chat preflight

```text
Теперь сохрани результаты последнего проанализированного run и сделай локальную проверку в чате перед большим прогоном.

Сначала снова открой START_HERE.md. Используй диагностический отчёт из прошлого шага, frontier/latest.*, workflow завершённого run, runs/, candidates/bank.jsonl, bank-additions, candidates/originals/ и artifacts.

Сохрани результаты по слоям: champion candidate для frontier/latest.*, per-run top/unique candidates в runs/, compact bank/additions для новых уникальных кандидатов выше порога, candidates/originals/ для оригинальных shard-best кандидатов без symmetry deduplication. Обнови START_HERE.md, если изменился frontier, подготовленный workflow или главный следующий шаг.

После сохранения сделай лабораторную часть без запуска GitHub Actions. Сравни defect patterns, mode behavior, missing points, seed families и candidate banks. Не повторяй прошлый workflow автоматически.

Если полезно, подготовь или поправь workflow, C++/Python-генератор и docs-план. Новый workflow должен быть ручным workflow_dispatch без push-trigger. Не запускай его.

Проверь локально в чате всё, что возможно: YAML, Python py_compile, согласованность run_id, artifact names, input names, seed sources, min_covered_to_save, compile/check commands, upload artifact names и aggregation. Если можно локально сгенерировать C++ из шаблона и проверить компиляцию на маленьком наборе файлов — сделай это. Если нельзя, честно скажи что именно не проверено.

В конце дай: что записано в репозиторий, какая гипотеза выбрана, что проверено локально без GitHub Actions, что осталось непроверенным, и предварительные параметры GitHub smoke-test/full-run для следующего шага.
```

## Prompt 3: prepare GitHub smoke-test and full run

```text
Локальная проверка в чате завершена. Подготовь пакет запуска на GitHub: короткий smoke-test и затем полный прогон.

Сначала открой START_HERE.md. Затем открой подготовленный workflow, docs-план, frontier/latest.*, последние runs/, candidate bank/additions/originals и выводы локальной проверки из прошлого шага.

Проверь, что GitHub smoke-test оправдан: локальные проверки не нашли явных ошибок, workflow ручной workflow_dispatch без push-trigger, seed sources и run_id согласованы, artifact names и aggregation согласованы, C++/Python-генерация выглядит рабочей, а новая гипотеза не является простым повтором прошлого насыщенного workflow.

Если всё чисто, дай точные inputs для короткого GitHub smoke-test: workflow name, seconds примерно 180, threads=4, seed, все нужные run_id для seed artifacts, min_covered_to_save, jobs/shards=20, max-parallel=20.

Затем дай точные inputs для полного GitHub запуска после зелёного smoke-test: seconds=21000, threads=4, тот же workflow_dispatch, seed, run_id, min_covered_to_save, jobs/shards=20, max-parallel=20, ожидаемое время около 5ч50м на shard.

В конце коротко скажи, почему теперь можно запускать GitHub smoke-test и какие inputs использовать.
```

## Anti-waste rule

First diagnose, then save and run local chat preflight, then prepare a short GitHub smoke-test and only after it succeeds use the full run parameters.
