# START HERE — project memory

Last updated: 2026-06-27

This is the first file to read when starting work in a new ChatGPT web chat.

The assistant may not remember enough from previous project chats. Treat this repository as durable memory. Start here, then read the files listed below before analyzing a run or preparing a new one.

## What this project is

Repository: `Grisha-Pochuev/minimum-link-covering-trail-4x4x4`

Problem: find a shortest connected polygonal trail that covers all 64 points of the `4×4×4` grid `{0,1,2,3}^3`.

Working target: find a `22`-link trail covering `64/64` grid points, or understand the obstruction well enough to guide a proof or a sharper search.

Known practical status:

- `23` links: known construction exists and is used as a control check.
- `22` links: open search target.
- `21` links: currently too hard for serious search; use only as diagnostic pressure unless the frontier changes.

Important caution: a search result is not a proof. A partial candidate is evidence, not a theorem.

## First reading order for a new chat

Read these in this order:

1. `START_HERE.md` — this file; top-level memory of the whole project.
2. `frontier/latest.md` and `frontier/latest.json` — current best frontier and latest useful run.
3. The relevant workflow in `.github/workflows/` — for a completed run, read the workflow that launched that run; for a new run, read the current or prepared workflow. Do not assume the newest workflow is automatically the right one for an old run.
4. `docs/*-plan.md` and `docs/web-chat-memento-prompts.md` — current planning notes and web-chat operating prompts.
5. `candidates/bank.jsonl` — global candidate bank / reusable seed memory.
6. The latest relevant folder in `runs/` — saved summaries, best candidates, and top candidates.
7. GitHub Actions artifacts of the latest useful runs, when analyzing or preparing computation.

Short invariant:

```text
START_HERE → frontier → relevant workflow → plans → bank → runs/artifacts → action
```

## What START_HERE is, and what workflow is

`START_HERE.md` is the global project memory. It answers: what is this project, what is the current frontier, where is the candidate bank, which workflow is currently prepared, and what is the next strategic direction.

A workflow file is not the global project memory. A workflow is the executable recipe and local memory for one search line or one completed run. It answers: what inputs were used, which old artifacts were downloaded, how many shards and threads were launched, what artifacts were saved, and what candidate-saving threshold applied.

So the rule is:

```text
START_HERE tells where we are.
The relevant workflow tells how that particular run works.
```

## Maintenance rule for this file

Update `START_HERE.md` after every useful run or important preparation step if any of these changed:

- current best frontier;
- latest useful run id;
- current best candidate or missing points;
- prepared next workflow;
- full-run parameters;
- candidate-saving rule;
- main next mathematical strategy.

If nothing important changed, say that `START_HERE.md` was checked and did not need an update.

## Current frontier to remember

Latest useful completed full run recorded in `frontier/latest.md`:

```text
run id: 28275850889
workflow: smart-search-6-defect
status: success
seconds per shard: 21000
threads per shard: 4
shards/jobs: 20
best result: 59/64
links: 22
missing count: 5
```

Best recorded candidate:

```text
candidate id: mlct22-278a7d8dc1d65f25
source artifact: defect-22-shard-6
mode: fractional_bridge22
saved at: runs/2026-06-27-smart-search-6-defect-full/best_candidate.json
reusable copy: candidates/mlct22-278a7d8dc1d65f25-run28275850889.json
```

Missing points for the selected best candidate:

```text
(1, 2, 2)
(2, 0, 2)
(2, 0, 3)
(3, 1, 2)
(3, 1, 3)
```

Dominant recurring defect core from the full 20-shard run:

```text
(1,2,2), (2,0,2), (2,0,3), (3,1,0), (3,1,2)
```

Important observation: all major modes reached `59/64`, but none reached `60/64` or `64/64`. So the next improvement probably needs a better repair idea, not only more of the same search.

## Current next workflow

Prepared next workflow:

```text
.github/workflows/smart-search-7-core5.yml
```

Workflow name:

```text
smart-search-7-core5
```

Purpose:

Repair the stable 5-point defect core of the `59/64` frontier using old artifacts, the candidate bank, exact checking, and transition-aware local repair windows.

It should not start from zero. It should use:

```text
prior_run_id: 28275850889        # latest full 59/64 run
secondary_run_id: 28275666411    # previous 59/64 smoke run
base_repair_run_id: 28200925016  # earlier 58/64 repair run
candidates/bank.jsonl
runs/2026-06-27-smart-search-6-defect-full/
runs/2026-06-26-repair-search-5/
experiments/2026-06-25-repair57-local-smoke/
```

Default smoke-test parameters:

```text
seconds: 180
threads: 4
seed: 20260628
min_covered_to_save: 56
jobs/shards: 20
max-parallel: 20
```

Full serious-run parameters:

```text
seconds: 21000
threads: 4
seed: 20260628
prior_run_id: 28275850889
secondary_run_id: 28275666411
base_repair_run_id: 28200925016
min_covered_to_save: 56
jobs/shards: 20
max-parallel: 20
expected wall time: about 5h50m per shard
```

Important: workflows for expensive searches should be manual `workflow_dispatch`, not automatic `push`, unless there is an explicit reason. Do not silently burn GitHub Actions time from a preparation commit.

## Candidate-saving rules

There are three different candidate layers:

1. Per-run champion candidate: one or several best candidates from a run, saved for easy reference in `frontier/latest.*`.
2. Per-run top candidates: useful best candidates from that particular run, saved under that run folder, for example `runs/.../top_candidates.json`.
3. Global candidate bank: `candidates/bank.jsonl`, the reusable seed memory across runs.

Normal bank threshold unless the workflow says otherwise:

```text
covered_count >= 56
links <= 22
```

Do not only save the single best candidate. Merge all new unique eligible candidates into `candidates/bank.jsonl` using `scripts/merge_candidate_bank.py` or the same canonical idea: coordinate permutations, cube reflections, and trail reversal.

## Standard command: analyze a completed run

Use this style when the user says a run has finished:

```text
Прогон завершился: <ссылка на GitHub Actions run>.

Сначала открой START_HERE.md, чтобы понять текущее состояние проекта. Затем открой workflow, которым был запущен этот run, и следуй правилам из него. Не подменяй workflow завершенного run самым новым workflow.

Сними результаты: проверь jobs, logs и artifacts; найди лучшее покрытие из 64, links, mode, source artifact и пропущенные точки.

Сравни с frontier/latest.md, frontier/latest.json, последними runs/ и candidates/bank.jsonl.

Сохрани результаты по правилам workflow: кандидатов-чемпионов для frontier, лучших оригинальных кандидатов этого run в runs/, всех новых уникальных кандидатов выше порога — в candidates/bank.jsonl.

Обнови START_HERE.md, если изменился текущий frontier, актуальный следующий workflow или главный следующий шаг.

В конце коротко скажи: что дал прогон, сколько кандидатов какого уровня найдено, какой режим что дал, какие точки остались проблемными, что записано в GitHub и какой следующий шаг лучше для поиска 64/64.
```

## Standard command: prepare a next smart run

Use this style when the user asks to prepare the next run:

```text
Подготовь следующий умный прогон smart-search-<следующий номер>-<1-2 слова>.

Сначала открой START_HERE.md, чтобы понять текущее состояние проекта. Затем открой актуальный workflow, frontier/latest.md, frontier/latest.json, последние runs/, candidates/bank.jsonl, планы в docs/ и artifacts последних полезных запусков.

Новый прогон не должен начинаться с нуля. Он должен использовать старые данные: лучшие кандидаты, общий банк кривых, artifacts, частые пропущенные точки, defect patterns и выводы прошлых прогонов.

Цель нового прогона — умнее приблизиться к 64/64: закрыть оставшиеся дырки, отремонтировать лучшие 22-звенные кандидаты или проверить новую математическую идею на основе прошлых неудач.

Если нужно, обнови START_HERE.md как главную память проекта, а также workflow/C++/Python-код. Новый workflow делай ручным workflow_dispatch, без trigger on push. Сначала подготовь безопасный smoke-test, затем дай точные параметры полного запуска на 20 jobs × 4 threads примерно на 5ч50м.
```

## How to explain progress to the user

Use simple language. The user works from ChatGPT web UI and cannot supervise hidden background work.

Do not promise delayed checks or future background work. If something is launched, it must be clear what was launched and what must be done after it finishes.

When explaining results, say:

- best coverage: `X/64`;
- how many points are still missing;
- which points are missing;
- how many candidates of each level were saved if known;
- which modes produced what;
- what was committed to GitHub;
- what the next useful action is.

## Current best strategic idea

Do not merely search wider.

The current frontier is a stable `59/64`, 22-link partial candidate. The useful direction is to understand and repair the final defect core, especially around:

```text
(1,2,2), (2,0,2), (2,0,3), (3,1,0), (3,1,2), with variant (3,1,3)
```

Prioritize:

- local repair of good 22-link candidates;
- defect-set analysis;
- rich 3-point and 4-point segment skeletons;
- transition penalties between rich segments;
- half-integer or outside vertices only as targeted local tools;
- symmetry-normalized comparison of defect patterns;
- extracting possible structural lemmas from repeated failures.

Low priority for now:

- blind broad random search;
- serious 21-link search;
- broad free fractional search;
- vague layer bonuses;
- exact global proof search before local structure is understood.

## Human reminder

The user wants this project to work like a scientific notebook with memory. A new assistant should not wake up and start from zero. Read this file first, then continue the chain of evidence.
