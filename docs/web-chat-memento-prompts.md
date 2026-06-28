# Web-chat Memento prompts

This project is operated from ChatGPT web chat. A new chat may not remember the full previous conversation. Treat the repository as durable memory.

Always read `START_HERE.md` first. Then read `frontier/latest.md`, `frontier/latest.json`, the relevant workflow, docs/plans, candidate banks, runs, originals, and artifacts.

## Three-prompt loop

Use three prompts, not two.

```text
1. Diagnose the completed run. Do not require repository writes.
2. Save results and run a local chat preflight. Do not run GitHub Actions.
3. If the local preflight is clean, prepare the full GitHub run.
```

The middle step is local. It means static checks, small Python/YAML checks, generator sanity checks, seed-source consistency, artifact-name consistency, and any small test possible inside the chat environment. It is not a short GitHub Actions run.

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

## Prompt 2: save results and do local preflight

```text
Теперь сохрани результаты последнего проанализированного run и сделай локальную проверку в чате перед большим прогоном.

Сначала снова открой START_HERE.md. Используй диагностический отчёт из прошлого шага, frontier/latest.*, workflow завершённого run, runs/, candidates/bank.jsonl, bank-additions, candidates/originals/ и artifacts.

Сохрани результаты по слоям: champion candidate для frontier/latest.*, per-run top/unique candidates в runs/, compact bank/additions для новых уникальных кандидатов выше порога, candidates/originals/ для оригинальных shard-best кандидатов без symmetry deduplication. Обнови START_HERE.md, если изменился frontier, подготовленный workflow или главный следующий шаг.

После сохранения сделай лабораторную часть без запуска GitHub Actions. Сравни defect patterns, mode behavior, missing points, seed families и candidate banks. Не повторяй прошлый workflow автоматически.

Если полезно, подготовь или поправь workflow, C++/Python-генератор и docs-план. Новый workflow должен быть ручным workflow_dispatch без push-trigger. Не запускай его.

Проверь локально в чате всё, что возможно: YAML, Python py_compile, согласованность run_id, artifact names, input names, seed sources, min_covered_to_save, compile/check commands, upload artifact names и aggregation. Если можно локально сгенерировать C++ из шаблона и проверить компиляцию на маленьком наборе файлов — сделай это. Если нельзя, честно скажи что именно не проверено.

В конце дай: что записано в репозиторий, какая гипотеза выбрана, что проверено локально без GitHub Actions, что осталось непроверенным, и точные параметры будущего полного GitHub-запуска.
```

## Prompt 3: prepare full GitHub run after local preflight

```text
Локальная проверка в чате завершена. Подготовь полный GitHub-запуск.

Сначала открой START_HERE.md. Затем открой подготовленный workflow, docs-план, frontier/latest.*, последние runs/, candidate bank/additions/originals и выводы локальной проверки из прошлого шага.

Проверь, что полный запуск оправдан: локальные проверки не нашли явных ошибок, workflow ручной workflow_dispatch без push-trigger, seed sources и run_id согласованы, artifact names и aggregation согласованы, C++/Python-генерация выглядит рабочей, а новая гипотеза не является простым повтором прошлого насыщенного workflow.

Если есть явная ошибка, не готовь полный запуск. Сначала предложи маленькую правку и повтор локальной проверки в чате без GitHub Actions.

Если всё чисто, дай точные inputs для полного запуска на GitHub: workflow name, seconds=21000, threads=4, seed, все нужные run_id для seed artifacts, min_covered_to_save, jobs/shards=20, max-parallel=20, ожидаемое время около 5ч50м на shard. Обнови START_HERE.md и docs-план, если после локальной проверки изменился главный следующий шаг.

В конце коротко скажи, почему теперь можно запускать большой GitHub run и какие inputs использовать.
```

## Anti-waste rule

Do not recommend a full expensive run immediately after run analysis. First diagnose, then save and run local chat preflight, then decide whether the full run is justified.
