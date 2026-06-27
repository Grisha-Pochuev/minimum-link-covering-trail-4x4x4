# Web-chat Memento prompts

This project is usually operated from ChatGPT web chat. A new chat may not remember the full previous conversation. Treat the repository as durable memory.

Before analyzing a completed run or preparing a new run, read the relevant workflow first. The workflow is both executable GitHub Actions configuration and a memory note explaining what the run was supposed to do: inputs, seed sources, artifact names, save rules, candidate-bank rules, and post-run expectations.

## Prompt 1: analyze a completed run

```text
Прогон завершился: <ссылка на GitHub Actions run>.

Сначала открой и прочитай workflow, которым был запущен этот run. Не начинай с jobs/logs/artifacts: workflow — это главная “память” запуска, там записано, какие inputs, seed sources, artifacts, thresholds и правила сохранения должны были использоваться.

После этого сними результаты: проверь jobs, logs и artifacts; найди лучший covered_count, число links, mode, candidate_id, source artifact и пропущенные точки; сравни с frontier/latest.md, frontier/latest.json, предыдущими runs/ и candidates/bank.jsonl.

Сохрани лучший кандидат, top candidates, smart_run_summary и выводы в runs/. Обнови frontier/latest.md и frontier/latest.json, если прогон полезный. Обязательно проверь правило candidate bank из workflow и добавь в candidates/bank.jsonl все новые оригинальные кандидаты, которые проходят порог сохранения, а не только один лучший кандидат. Для банка используй scripts/merge_candidate_bank.py или тот же канонический принцип: coordinate permutations, cube reflections и trail reversal.

В конце коротко скажи: что этот прогон дал, улучшился ли frontier, какие точки/паттерны остались проблемными, что записано в репозиторий, и какой следующий шаг лучше.
```

## Prompt 2: prepare the next smart run

```text
Подготовь следующий умный прогон smart-search-<следующий номер>-<1-2 слова>, например smart-search-7-repair или smart-search-7-core5.

Сначала открой и прочитай последний релевантный workflow. Это не просто технический YAML, а “память” проекта: там записано, как устроен прошлый запуск, какие artifacts он создаёт, что считается seed material, какой порог сохранения кандидатов, и что нужно делать после завершения.

Затем изучи frontier/latest.md, frontier/latest.json, последние runs/, candidates/bank.jsonl, docs/*-plan.md и artifacts последнего полезного run. Новый прогон не должен стартовать с нуля: используй лучшие кандидаты, банк кривых, top candidates, defect patterns и выводы прошлых прогонов.

Если нужно, обнови workflow/C++/Python-код, но не делай workflow с trigger on push. Новый workflow должен быть ручным workflow_dispatch, чтобы подготовительные коммиты не запускали дорогой GitHub Actions run автоматически.

Сначала подготовь безопасный smoke-test: короткое время на shard, 20 jobs × 4 threads, те же seed sources, проверка компиляции, checker и artifacts. Затем дай точные параметры для полного запуска: 20 jobs × 4 threads примерно на 5ч50м, обычно seconds=21000, threads=4, max-parallel=20, правильные run_id для seed artifacts и min_covered_to_save.

В конце коротко объясни, почему новый прогон умнее предыдущего, какие старые результаты он использует, что именно изменено в репозитории, и какие параметры нажимать в GitHub Actions.
```

## Minimal invariant

For every new web-chat cycle:

```text
workflow first, then frontier, then bank, then artifacts, then action.
```
