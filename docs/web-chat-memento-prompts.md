# Web-chat Memento prompts

This project is usually operated from ChatGPT web chat. A new chat may not remember the full previous conversation. Treat the repository as durable memory.

Before analyzing a completed run or preparing a new run, read `START_HERE.md` first. It is the top-level project memory. Then read the relevant workflow: for a completed run, the workflow that launched that run; for a new run, the current or prepared workflow. The workflow is both executable GitHub Actions configuration and a memory note explaining what that run was supposed to do: inputs, seed sources, artifact names, save rules, candidate-bank rules, and post-run expectations.

## Candidate terminology

There are three different candidate-saving layers. Do not mix them up.

1. Per-run champion candidate: the single strongest candidate from one run. Save it only as a quick reference for `frontier/latest.*` and human reading.

2. Per-run top candidates: the best useful candidates from this particular run, usually all shard-best candidates and/or all distinct high-quality candidates above the run threshold. Save these under that run's folder, for example as `top_candidates.json` or similar. This is not the global bank.

3. Global candidate bank: `candidates/bank.jsonl`. This is the reusable seed memory for future runs. It should contain all unique eligible candidates, not only the single best one. Current normal threshold: `covered_count >= 56` and `links <= 22`, unless the workflow says otherwise. Merge by the canonical bank rule, not by hand-picked favorites.

In plain language: save one champion for easy reporting, save the run's full top set for analysis, and merge every eligible unique candidate into the global bank.

## Prompt 1: analyze a completed run

```text
Прогон завершился: <ссылка на GitHub Actions run>.

Сначала открой START_HERE.md, чтобы понять текущее состояние проекта. Затем открой workflow, которым был запущен этот run, и следуй правилам из него.

Сними результаты: проверь jobs, logs и artifacts; найди лучший covered_count, число links, mode, candidate_id, source artifact и пропущенные точки; сравни с frontier/latest.md, frontier/latest.json, предыдущими runs/ и candidates/bank.jsonl.

Сохрани не только одного победителя. Раздели результаты на три уровня: 1) один per-run champion candidate для удобной ссылки во frontier/latest.*; 2) per-run top candidates — все лучшие/полезные кандидаты этого конкретного run, например все shard-best и все отличающиеся кандидаты выше порога; 3) global candidate bank — добавь в candidates/bank.jsonl все новые уникальные кандидаты, которые проходят порог сохранения из workflow, обычно covered_count >= 56 и links <= 22.

Обнови frontier/latest.md и frontier/latest.json, если прогон полезный. Обнови START_HERE.md, если изменился текущий frontier, актуальный следующий workflow или главный следующий шаг. Для обновления candidates/bank.jsonl используй scripts/merge_candidate_bank.py или тот же канонический принцип: coordinate permutations, cube reflections и trail reversal. Не путай per-run top candidates с общим банком: top candidates — отчет по одному run, bank.jsonl — долговременная память всех run.

В конце коротко скажи: что этот прогон дал, улучшился ли frontier, какие точки/паттерны остались проблемными, что записано в репозиторий, и какой следующий шаг лучше.
```

## Prompt 2: prepare the next smart run

```text
Подготовь следующий умный прогон smart-search-<следующий номер>-<1-2 слова>, например smart-search-7-repair или smart-search-7-core5.

Сначала открой START_HERE.md, чтобы понять текущее состояние проекта. Затем открой последний релевантный workflow. Это не просто технический YAML, а “память” конкретного запуска: там записано, как устроен прошлый или следующий запуск, какие artifacts он создаёт, что считается seed material, какой порог сохранения кандидатов, и что нужно делать после завершения.

Затем изучи frontier/latest.md, frontier/latest.json, последние runs/, candidates/bank.jsonl, docs/*-plan.md и artifacts последнего полезного run. Новый прогон не должен стартовать с нуля: используй champion candidates из frontier, per-run top candidates из последних runs, общий банк кривых candidates/bank.jsonl, defect patterns и выводы прошлых прогонов.

Если нужно, обнови START_HERE.md как главную память проекта, а также workflow/C++/Python-код. Новый workflow должен быть ручным workflow_dispatch, без trigger on push, чтобы подготовительные коммиты не запускали дорогой GitHub Actions run автоматически.

Сначала подготовь безопасный smoke-test: короткое время на shard, 20 jobs × 4 threads, те же seed sources, проверка компиляции, checker и artifacts. Затем дай точные параметры для полного запуска: 20 jobs × 4 threads примерно на 5ч50м, обычно seconds=21000, threads=4, max-parallel=20, правильные run_id для seed artifacts и min_covered_to_save.

В конце коротко объясни, почему новый прогон умнее предыдущего, какие старые результаты он использует, что именно изменено в репозитории, и какие параметры нажимать в GitHub Actions.
```

## Minimal invariant

For every new web-chat cycle:

```text
START_HERE first, then frontier, then the relevant workflow, then plans, then bank, then runs/artifacts, then action.
```
