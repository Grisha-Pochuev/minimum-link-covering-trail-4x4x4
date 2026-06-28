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

`START_HERE.md` is the global project memory. It answers: what is this project, what is the current frontier, where is the candidate bank, which workflow or next direction is current, and what is the next strategic direction.

A workflow file is not the global project memory. A workflow is the executable recipe and local memory for one search line or one completed run.

So the rule is:

```text
START_HERE tells where we are.
The relevant workflow tells how that particular run works.
```

## Current frontier to remember

Latest useful completed full run recorded in `frontier/latest.md`:

```text
run id: 28304497479
workflow: smart-search-8-orbit-bridge
status: success
seconds per shard: 21000
threads per shard: 4
shards/jobs: 20
best result: 59/64
links: 22
missing count: 5
```

Best recorded candidate from this run:

```text
candidate id: mlct22-9c80a2741db704ad
source artifact: orbit-bridge-22-shard-10
mode: subcube_stitch22
saved at: runs/2026-06-28-smart-search-8-orbit-bridge-full/best_candidate.json
```

Missing points for the selected best candidate:

```text
(0, 2, 2)
(2, 1, 3)
(2, 2, 3)
(3, 1, 0)
(3, 1, 2)
```

Important comparison:

The previous selected 59/64 best from run `28292425390` missed:

```text
(0,1,0), (1,2,3), (2,1,0), (3,1,1), (3,1,3)
```

The new selected 59/64 best from run `28304497479` misses a different set. The numeric frontier did not improve beyond `59/64`, but the run changed the defect picture: `(3,1,3)` appears only `2/20` times instead of being the dominant hard point.

Dominant recurring defect patterns from run `28304497479`:

```text
11/20: (0,2,2), (2,1,3), (2,2,3), (3,1,0), (3,1,2)
7/20:  (1,0,1), (1,2,2), (1,3,2), (2,0,3), (2,2,2)
2/20:  (1,2,1), (2,1,2), (2,2,3), (3,1,0), (3,1,3)
```

Important observation: all 20 shard-best artifacts reached `59/64`, but none reached `60/64` or `64/64`. `smart-search-8-orbit-bridge` did not break the frontier; it moved the obstruction. The next improvement probably needs a specialized repair of the new A/B defect families, not simply another identical orbit-bridge run.

## Current next direction

No new workflow has been prepared yet after analyzing run `28304497479`.

Recommended next workflow name:

```text
smart-search-9-new-defect-repair
```

Purpose:

Repair the new A/B defect patterns from run `28304497479`. Pattern A appeared `11/20`; pattern B appeared `7/20`. Keep `(3,1,3)` as a control point, but do not keep treating it as the only center: smart-search-8 mostly closed it and exposed a different obstruction.

The next run should not start from zero. It should use:

```text
prior_run_id: 28304497479           # latest full orbit-bridge run with new A/B defects
previous_core5_run_id: 28292425390  # prior 59/64 run, old selected best had (3,1,3)
old_59_run_id: 28275850889          # previous full 59/64 run with old defect core
secondary_run_id: 28275666411       # previous 59/64 smoke run
base_repair_run_id: 28200925016     # earlier 58/64 repair run
candidates/bank.jsonl
candidates/bank-additions-run28304497479.jsonl
candidates/bank-additions-run28292425390.jsonl
runs/2026-06-28-smart-search-8-orbit-bridge-full/
GitHub Actions artifacts from the listed runs, especially orbit-bridge-22-shard-* from 28304497479
```

Suggested smoke-test parameters for the next prepared workflow:

```text
workflow: smart-search-9-new-defect-repair
seconds: 180
threads: 4
seed: new fixed seed or github.run_id
prior_run_id: 28304497479
min_covered_to_save: 56
jobs/shards: 20
max-parallel: 20
```

Suggested full serious-run parameters after the smoke-test succeeds:

```text
workflow: smart-search-9-new-defect-repair
seconds: 21000
threads: 4
seed: new fixed seed or github.run_id
prior_run_id: 28304497479
min_covered_to_save: 56
jobs/shards: 20
max-parallel: 20
expected wall time: about 5h50m per shard
```

Important: workflows for expensive searches should be manual `workflow_dispatch`, not automatic `push`, unless there is an explicit reason. Do not silently burn GitHub Actions time from a preparation commit.

## Candidate-saving rules

There are three concrete candidate-memory locations. They have two roles: compact search fuel and scientific original archive. Do not mix them up.

### 1. Main compact working bank

```text
candidates/bank.jsonl
```

This is the main small reusable search memory. It stores the best known eligible trail candidates from previous runs as symmetry-deduplicated representatives. Cube symmetries, coordinate permutations/reflections, trail reversal, and exact duplicates should be collapsed here.

Use it as seed fuel for future workflows. Do not treat it as a complete historical archive.

### 2. Run-level compact additions

```text
candidates/bank-additions-*.jsonl
```

These files are append records from specific completed runs. They store compact eligible candidates from that run, also symmetry-deduplicated, before or alongside merging into `candidates/bank.jsonl`.

Use them as seed fuel together with `candidates/bank.jsonl`, especially when the additions have not yet been physically merged into the main bank. Do not ignore them just because they are separate files.

For run `28304497479`, the 3 unique eligible additions are saved in:

```text
candidates/bank-additions-run28304497479.jsonl
candidates/bank-additions-run28304497479.summary.json
```

### 3. Original trail archive

```text
candidates/originals/
candidates/originals/README.md
candidates/originals/index.jsonl
```

This is the permanent scientific archive of original, non-deduplicated lomanaya/trail candidates from completed runs. It is for analysis of real diversity, repeated patterns, mode behavior, and possible structural obstructions.

Do not collapse cube symmetries, reflections, coordinate permutations, or trail reversal here. Exact byte-identical duplicates may be compressed into one row with `source_occurrence_count`, `source_shards`, and `source_artifacts`, but do not lose the fact that several shards/runs found the same trail.

Normal eligibility threshold for both compact memory and original archive unless the workflow says otherwise:

```text
covered_count >= 56
links <= 22
```

Post-run saving rule:

```text
1. Save champion candidate(s) and update frontier/latest.* if needed.
2. Save new compact unique eligible candidates into bank/additions.
3. Save all original eligible shard-best candidates into candidates/originals/.
4. Update candidates/originals/index.jsonl with a summary line for the run.
5. Update START_HERE.md if the frontier, prepared workflow, or next step changed.
```

Important: `candidates/originals/` is protection against losing scientific evidence. GitHub Actions artifacts are useful but fragile: they can expire, be inaccessible, or be hard to rediscover in a new chat.

## Flexible post-run reasoning loop

After a completed run, do not merely fill a template. Use `START_HERE.md` as memory, then think from the evidence of this particular run.

A good post-run analysis should ask, in free form:

- Did the numeric frontier improve: `56→57→58→59→60→64`, or did it stay the same?
- If the best coverage stayed the same, did the run still discover new defect sets, new modes, or new geometric families?
- Are the new missing points the same as before, a symmetry of old ones, or genuinely different?
- Did many shards converge to one pattern, or did they spread across several patterns?
- Did the compact bank gain genuinely useful new representatives, or only near-duplicates?
- Did the original archive show real diversity hidden by symmetry deduplication?
- Did any mode underperform so badly that it should be reduced or removed next time?
- Did any mode produce a new kind of near-miss that deserves a specialized repair workflow?
- Are we learning a possible obstruction/lemma, not just collecting candidates?
- Was the workflow itself trustworthy: no artifact failures, no skipped aggregation, no accidental old commit, no missing seed layer?

Then decide the next action. Do not automatically launch the same style of run again.

Possible next actions include:

- repeat the same workflow only if it clearly produced new useful diversity;
- adjust weights or targets if it found near-misses but missed the intended defect region;
- build a local repair workflow if several candidates differ only in a small window;
- build an orbit/defect comparison workflow if several `59/64` families disagree on the missing set;
- pause search and write a structural note if repeated failures point to a stable obstruction;
- update banks/archives first if the run produced valuable candidates but the memory layer is incomplete.

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

The current frontier is still `59/64`, 22 links, but now there are multiple useful `59/64` defect families. Run `28304497479` showed that targeting the old shared hard point `(3,1,3)` can mostly close it, but the obstruction moves into two new dominant 5-point patterns.

Prioritize:

- local repair of the new A/B 5-point defect patterns;
- comparison of distinct 59/64 defect orbits;
- transition repair around `(3,1,0)`, `(3,1,2)`, `(2,2,3)`, `(2,1,3)`, `(0,2,2)`;
- keeping `(3,1,3)` as a control point, not the only target;
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
- exact global proof search before local structure is understood;
- repeating `smart-search-8-orbit-bridge` unchanged.

## Human reminder

The user wants this project to work like a scientific notebook with memory. A new assistant should not wake up and start from zero. Read this file first, then continue the chain of evidence.
