# Web-chat Memento prompts

This project is usually operated from ChatGPT web chat. A new chat may not remember the full previous conversation. Treat the repository as durable memory.

Before analyzing a completed run, saving results, preparing a smoke-test, or preparing a full run, read `START_HERE.md` first. It is the top-level project memory. Then read the relevant workflow: for a completed run, the workflow that launched that run; for a new run, the current or prepared workflow. The workflow is both executable GitHub Actions configuration and a memory note explaining what that run was supposed to do: inputs, seed sources, artifact names, save rules, candidate-bank rules, and post-run expectations.

## Why the loop is now three prompts

The old two-prompt loop was too compressed:

```text
1. Analyze completed run and save everything.
2. Prepare the next smart run.
```

At the current `59/64` plateau this can be too much for one web-chat turn. It is safer to split the loop into three prompts:

```text
1. Diagnose the completed run only. No mandatory repository writes.
2. Save the useful results and prepare a smoke-test/laboratory step.
3. After smoke-test evidence, prepare the full 20 jobs x 4 threads run for about 5h50m.
```

The first prompt is deliberately diagnostic. It should collect facts, compare them, and produce a save/prep plan. It should not be forced to also update many repository files in the same turn. This avoids half-finished memory updates and makes the next step clearer.

## Candidate terminology

There are three different candidate-saving layers. Do not mix them up.

1. Per-run champion candidate: the single strongest candidate from one run. Save it only as a quick reference for `frontier/latest.*` and human reading.

2. Per-run top candidates: the best useful candidates from this particular run, usually all shard-best candidates and/or all distinct high-quality candidates above the run threshold. Save these under that run's folder, for example as `top_candidates.json`, `unique_candidates.jsonl`, or similar. This is not the global bank.

3. Global candidate bank/additions: `candidates/bank.jsonl` and `candidates/bank-additions-*.jsonl`. This is reusable seed memory for future runs. Current normal threshold: `covered_count >= 56` and `links <= 22`, unless the workflow says otherwise. Merge or add by the canonical bank rule, not by hand-picked favorites.

In plain language: save one champion for easy reporting, save the run's full useful top set for analysis, and preserve every eligible useful candidate in compact bank/additions and original archive.

## Prompt 1: diagnose a completed run only

```text
Прогон завершился: вставь ссылку на GitHub Actions run.

Сначала открой START_HERE.md, чтобы понять текущее состояние проекта. Затем открой workflow, которым был запущен именно этот run, и следуй правилам из него. Не подменяй workflow завершённого run самым новым workflow.

Сними результаты, но пока не обязан ничего записывать в репозиторий. Проверь jobs, logs и artifacts; найди лучший covered_count из 64, links, mode, candidate_id, source artifact и пропущенные точки. Сравни с frontier/latest.md, frontier/latest.json, последними runs/, candidates/bank.jsonl, bank-additions и candidates/originals/.

Главная цель этого шага — понять, что произошло: улучшился ли frontier, сколько было shard-best кандидатов, какие defect patterns повторяются, какие точки стали чаще всего пропущенными, какие режимы дали пользу, были ли ошибки workflow/artifacts/aggregation, и отличается ли новый результат от старых семейств.

Не трать время на большой коммит, если диагностика уже длинная. В конце дай короткий отчёт и отдельный план сохранения: какие файлы надо создать или обновить на следующем шаге, какие кандидаты надо сохранить, надо ли менять START_HERE.md, и какая гипотеза выглядит лучшей для smoke-test.
```

## Prompt 2: save results and prepare smoke-test/laboratory step

```text
Теперь сохрани результаты последнего проанализированного run и подготовь лабораторный шаг/smoke-test.

Сначала снова открой START_HERE.md, затем используй диагностический отчёт из прошлого шага, frontier/latest.*, workflow завершённого run, runs/, candidates/bank.jsonl, bank-additions, candidates/originals/ и artifacts.

Сохрани результаты по слоям: 1) champion candidate для frontier/latest.*; 2) per-run top/unique candidates в папку runs/ этого запуска; 3) compact bank/additions для новых уникальных кандидатов выше порога; 4) candidates/originals/ для оригинальных shard-best кандидатов без symmetry deduplication. Обнови START_HERE.md, если изменился frontier, подготовленный workflow или главный следующий шаг.

После сохранения сделай лабораторную часть: сравни defect patterns, mode behavior, missing points, seed families и candidate banks. Не повторяй прошлый workflow автоматически. Подумай, какие гипотезы стоит проверить коротким smoke-test, а какие уже выглядят бесполезными.

Если полезно, подготовь или поправь workflow, C++/Python-генератор и docs-план. Новый workflow должен быть ручным workflow_dispatch без push-trigger. Готовь только безопасный smoke-test: короткое время на shard, 20 jobs x 4 threads, те же seed sources, проверка компиляции, checker, artifact upload и aggregation.

Проверь всё, что можно проверить без дорогого GitHub run: согласованность run_id, artifact names, input names, seed sources, min_covered_to_save, compile/check steps, имена upload artifacts и aggregation. Если локально что-то проверить нельзя, честно скажи что именно не проверено.

В конце дай: что записано в репозиторий, почему smoke-test умнее предыдущего запуска, точные параметры smoke-test, что считать зелёным smoke-test, и что делать, если smoke-test упадёт.
```

## Prompt 3: after smoke-test, prepare the full run

```text
Smoke-test завершился: вставь ссылку на GitHub Actions run.

Сначала открой START_HERE.md. Затем открой workflow smoke-test, jobs/logs/artifacts/summary, frontier/latest.*, docs-план и последние runs/.

Проверь smoke-test как инженерную проверку: прошёл ли known 23-link check, скачались ли seed artifacts, экспортировался ли candidate bank, сгенерировался и скомпилировался ли C++ engine, прошёл ли checker, загрузились ли shard artifacts, сработала ли aggregation. Если smoke-test упал, не готовь полный запуск; объясни причину и подготовь маленький fix/smoke retry.

Если smoke-test зелёный, сравни его результаты с последним frontier. Даже если он короткий, проверь, не показал ли он явную ошибку в идее: все ли shard-best слишком слабые, потерялись ли seed candidates, не повторяется ли старый defect pattern без новой информации.

Если smoke-test нормальный, подготовь параметры полного запуска на 20 jobs x 4 threads примерно на 5ч50м. Обычно это seconds=21000, threads=4, max-parallel=20, правильные run_id для seed artifacts, seed, min_covered_to_save и тот же workflow_dispatch.

Обнови START_HERE.md и docs-план, если smoke-test изменил понимание следующего шага. В конце дай точные inputs для полного запуска и коротко скажи, почему теперь можно жечь большой GitHub run.
```

## Minimal invariant

For every web-chat cycle:

```text
START_HERE first, then frontier, then relevant workflow, then plans, then bank/additions/originals, then runs/artifacts, then action.
```

## Anti-waste rule

Never silently start or recommend a full expensive run immediately after a completed run analysis. First diagnose, then save and smoke-test, then decide whether the full run is justified.
