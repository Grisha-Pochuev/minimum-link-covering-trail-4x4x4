# START HERE — project memory

Last updated: 2026-06-28

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

1. `START_HERE.md` — this file.
2. `frontier/latest.md` and `frontier/latest.json` — current best frontier and latest useful run.
3. The relevant workflow in `.github/workflows/` — for a completed run, read the workflow that launched that run. Do not assume the newest workflow is automatically the right one for an old run.
4. `docs/*-plan.md` and `docs/web-chat-memento-prompts.md` — planning notes and web-chat operating prompts.
5. `candidates/bank.jsonl`, `candidates/bank-additions-*.jsonl`, and `candidates/originals/` — reusable seed memory and original candidate archive.
6. The latest relevant folder in `runs/`.
7. GitHub Actions artifacts of the latest useful runs.

Short invariant:

```text
START_HERE → frontier → relevant workflow → plans → bank/additions/originals → runs/artifacts → action
```

## What START_HERE is, and what workflow is

`START_HERE.md` is the global project memory. It answers: what is this project, what is the current frontier, where is the candidate bank, which workflow is currently prepared, and what is the next strategic direction.

A workflow file is not the global project memory. A workflow is the executable recipe and local memory for one search line or one completed run.

So the rule is:

```text
START_HERE tells where we are.
The relevant workflow tells how that particular run works.
```

## Current frontier to remember

Latest useful completed full run recorded in `frontier/latest.md`:

```text
run id: 28292425390
workflow: smart-search-7-core5
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
candidate id: mlct22-a584fa7e488e0279
source artifact: core5-22-shard-15
mode: subcube_stitch22
saved at: runs/2026-06-27-smart-search-7-core5-full/best_candidate.json
reusable copy: candidates/mlct22-a584fa7e488e0279-run28292425390.json
```

Missing points for the selected best candidate:

```text
(0, 1, 0)
(1, 2, 3)
(2, 1, 0)
(3, 1, 1)
(3, 1, 3)
```

Important comparison:

The previous selected 59/64 best from run `28275850889` missed:

```text
(1,2,2), (2,0,2), (2,0,3), (3,1,2), (3,1,3)
```

The new selected 59/64 best from run `28292425390` misses a different set. The numeric frontier did not improve beyond `59/64`, but we now have more than one useful 59/64 defect orbit. This is valuable evidence for the next search.

Dominant recurring defect patterns from run `28292425390`:

```text
13/20: (1,2,1), (2,1,2), (2,2,3), (3,1,0), (3,1,3)
4/20:  (0,1,0), (1,2,3), (2,1,0), (3,1,1), (3,1,3)
2/20:  (1,2,2), (2,0,2), (2,0,3), (3,1,0), (3,1,2)
1/20:  (0,2,2), (2,1,2), (2,2,3), (3,1,0), (3,1,2)
```

Important observation: all 20 shard-best artifacts reached `59/64`, and all major modes represented in this run reached `59/64`, but none reached `60/64` or `64/64`. The next improvement probably needs a new repair idea, not simply another identical core5 run.

## Current prepared workflow

The next workflow is now prepared:

```text
.github/workflows/smart-search-8-orbit-bridge.yml
```

Workflow name:

```text
smart-search-8-orbit-bridge
```

Supporting files prepared:

```text
scripts/prepare_orbit_bridge_engine.py
docs/smart-search-8-orbit-bridge-plan.md
```

Purpose:

Compare and bridge the distinct `59/64` defect orbits from runs `28275850889` and `28292425390`. The search should try to combine what each orbit covers well, with targeted local surgery around the shared hard point `(3,1,3)` and the `x=3,y=1` transition zone.

It should not start from zero. It should use:

```text
prior_run_id: 28292425390          # latest full core5 run with new 59/64 orbit
old_59_run_id: 28275850889         # previous full 59/64 run with old defect core
secondary_run_id: 28275666411      # previous 59/64 smoke run
base_repair_run_id: 28200925016    # earlier 58/64 repair run
candidates/bank.jsonl
candidates/bank-additions-run28292425390.jsonl
runs/2026-06-27-smart-search-7-core5-full/
runs/2026-06-27-smart-search-6-defect-full/
runs/2026-06-26-repair-search-5/
experiments/2026-06-25-repair57-local-smoke/
GitHub Actions artifacts from the listed runs, especially core5-22-shard-* from 28292425390
```

The 20 original shard-best candidates from run `28292425390` are preserved as GitHub Actions artifacts and are used through the downloaded `core5-22-shard-*` artifact folders. The persistent repo bank keeps symmetry-unique candidates; do not confuse that with the original per-shard artifact layer.

Suggested smoke-test parameters:

```text
workflow: smart-search-8-orbit-bridge
seconds: 180
threads: 4
seed: 20260629
prior_run_id: 28292425390
old_59_run_id: 28275850889
secondary_run_id: 28275666411
base_repair_run_id: 28200925016
min_covered_to_save: 56
jobs/shards: 20
max-parallel: 20
```

Suggested full serious-run parameters:

```text
workflow: smart-search-8-orbit-bridge
seconds: 21000
threads: 4
seed: 20260629
prior_run_id: 28292425390
old_59_run_id: 28275850889
secondary_run_id: 28275666411
base_repair_run_id: 28200925016
min_covered_to_save: 56
jobs/shards: 20
max-parallel: 20
expected wall time: about 5h50m per shard
```

Important: workflows for expensive searches should be manual `workflow_dispatch`, not automatic `push`, unless there is an explicit reason. Do not silently burn GitHub Actions time from a preparation commit.

## Workflow robustness lesson from smart-search-8

This is a known assistant failure mode, not just a random one-off.

When preparing a new GitHub Actions workflow, the assistant may overfocus on the mathematical search idea and under-check operational fragility. The concrete failure from run `28303978510` was: all shard jobs failed before C++ generation/search because `gh run download` for old artifacts was a hard-failing step. The run died in under a minute; this was not a mathematical result.

Rules for future workflow preparation:

- Add explicit permissions when downloading artifacts:

```yaml
permissions:
  contents: read
  actions: read
```

- Treat old GitHub Actions artifacts as useful but fragile. They can be missing, expired, inaccessible, renamed, or intermittently fail to download.
- Do not make the whole expensive search fail merely because one old artifact download failed, unless that artifact is absolutely required and no repository seed fallback exists.
- Prefer best-effort artifact download wrappers: create the target directories, run `gh run download`, log a warning on failure, and continue with `candidates/bank.jsonl`, `bank-additions`, saved `runs/`, and whatever artifacts did download.
- A smoke-test must verify more than the 23-link checker. It should reach artifact download, seed export, C++ generation, compilation, shard execution, result checking, artifact upload, and summary aggregation.
- If a failed run used an old workflow commit, do not press `Re-run jobs` after fixing the workflow. Start a new manual workflow run from current `main`, otherwise GitHub may rerun the old broken commit.
- In explanations to the user, distinguish clearly between: a workflow infrastructure failure, a smoke-test failure, and a real mathematical search result.

For `smart-search-8-orbit-bridge`, the workflow was fixed after the failed run by adding `actions: read` and making the artifact downloads best-effort. After this fix, run a new smoke-test from the workflow page rather than rerunning failed jobs from the red run.

## Candidate-saving rules

There are now two different candidate-memory layers. Do not mix them up.

### Compact working bank

This is the small reusable search memory:

```text
candidates/bank.jsonl
candidates/bank-additions-*.jsonl
```

This layer should be symmetry-deduplicated and convenient for future workflows. It is fuel for the next search, not a full scientific archive.

Normal compact-bank threshold unless the workflow says otherwise:

```text
covered_count >= 56
links <= 22
```

Merge new unique eligible candidates into this layer using `scripts/merge_candidate_bank.py` or the same canonical idea: coordinate permutations, cube reflections, and trail reversal.

For run `28292425390`, the 6 unique eligible candidates were saved in:

```text
candidates/bank-additions-run28292425390.jsonl
candidates/bank-additions-run28292425390.summary.json
```

These additions must be included as seed material in the next run even if `candidates/bank.jsonl` has not yet been physically merged.

### Original trail archive

This is the permanent archive of original, non-deduplicated lomanaya/trail candidates:

```text
candidates/originals/
candidates/originals/README.md
candidates/originals/index.jsonl
```

This layer is for scientific analysis. It should preserve original shard-best candidates before symmetry deduplication. Do not collapse cube symmetries, reflections, coordinate permutations, trail reversal, or repeated missing-set patterns here.

For each completed useful run, create a file like:

```text
candidates/originals/run-<run_id>-<workflow_short_name>.jsonl
```

Example:

```text
candidates/originals/run-28292425390-smart-search-7-core5.jsonl
```

Also append/update one summary line in:

```text
candidates/originals/index.jsonl
```

Normally archive every original shard-best candidate satisfying:

```text
covered_count >= 56
links <= 22
```

Each JSONL row should contain at least:

```text
schema, run_id, workflow, source_artifact, source_shard, candidate_id,
covered_count, links, missing, coordinate_scale, vertices2
```

Important: the original archive is not a replacement for GitHub Actions artifacts. It is protection against losing them. Artifacts can expire or become hard to rediscover; the original archive should keep the scientific evidence in the repository.

Post-run saving rule:

```text
1. Save champion candidate(s) and update frontier/latest.* if needed.
2. Save compact unique eligible candidates into bank/additions.
3. Save all original eligible shard-best candidates into candidates/originals/.
4. Update START_HERE.md if the frontier, prepared workflow, or next step changed.
```

## Standard command: analyze a completed run

Use this style when the user says a run has finished:

```text
Прогон завершился: <ссылка на GitHub Actions run>.

Сначала открой START_HERE.md, чтобы понять текущее состояние проекта. Затем открой workflow, которым был запущен этот run, и следуй правилам из него. Не подменяй workflow завершенного run самым новым workflow.

Сними результаты: проверь jobs, logs и artifacts; найди лучшее покрытие из 64, links, mode, source artifact и пропущенные точки.

Сравни с frontier/latest.md, frontier/latest.json, последними runs/, candidates/bank.jsonl, bank-additions и candidates/originals/.

Сохрани результаты по правилам workflow: кандидатов-чемпионов для frontier, все новые уникальные кандидаты выше порога — в reusable compact bank/additions, а все оригинальные shard-best кандидаты выше порога — в candidates/originals/ без symmetry deduplication.

Обнови START_HERE.md, если изменился текущий frontier, актуальный следующий workflow или главный следующий шаг.

В конце коротко скажи: что дал прогон, сколько кандидатов какого уровня найдено, сколько оригинальных кривых записано в candidates/originals, какой режим что дал, какие точки остались проблемными, что записано в GitHub и какой следующий шаг лучше для поиска 64/64.
```

## Standard command: prepare a next smart run

Use this style when the user asks to prepare the next run:

```text
Подготовь следующий умный прогон smart-search-<следующий номер>-<1-2 слова>.

Сначала открой START_HERE.md, чтобы понять текущее состояние проекта. Затем открой актуальный workflow, frontier/latest.md, frontier/latest.json, последние runs/, candidates/bank.jsonl, candidates/originals/, планы в docs/ и artifacts последних полезных запусков.

Новый прогон не должен начинаться с нуля. Он должен использовать старые данные: лучшие кандидаты, общий банк кривых, original archive, artifacts, частые пропущенные точки, defect patterns и выводы прошлых прогонов.

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
- how many compact-bank candidates were saved if known;
- how many original shard-best candidates were saved in `candidates/originals/` if known;
- which modes produced what;
- what was committed to GitHub;
- what the next useful action is.

## Current best strategic idea

Do not merely search wider.

The current frontier is still `59/64`, 22 links, but now there are multiple useful `59/64` defect orbits. The next search should not target only one missing set. It should compare or bridge the old and new 59/64 candidates.

Prioritize:

- local repair of good 22-link candidates;
- comparison of distinct 59/64 defect orbits;
- defect-set analysis around `(3,1,3)`;
- transition repair in the `x=3,y=1` region;
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
