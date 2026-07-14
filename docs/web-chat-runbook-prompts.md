# Web-chat runbook prompts

This file defines reusable process, not mathematical truth. Current mathematical state belongs in `frontier/latest.*`; current execution stage belongs only in `frontier/active_run.json`.

## File roles

- `START_HERE.md`: compact stable boot memory and reading order. It may contain a dated snapshot, but it is not the live-stage authority.
- `frontier/latest.*`: best checked mathematical frontier.
- `frontier/active_run.json`: the only authoritative active run, retry, pending recording or selected-next-search stage.
- `docs/smart-search-N-*.md`: exact Step-2 to Step-3 handoff.
- `docs/retrospectives/*`: process lessons and explicit execution exceptions.
- `runs/*`: completed evidence or explicitly labelled incomplete-attempt evidence.
- candidate banks/originals: reusable checked and diagnostic curves.

If `START_HERE.md` and `frontier/active_run.json` disagree about a live stage, trust `active_run.json` and repair the contradiction in Step 4.

## Fixed four-step process

```text
1. Record a completed run, or explicitly archive an incomplete attempt.
2. Think creatively, test locally and choose one next hypothesis.
3. Implement the saved hypothesis and automatically execute preflight -> smoke -> full.
4. Review the chat and improve project memory/process.
```

Step 2 is research and selection. Step 3 implements the saved handoff and must not broaden it silently. Step 4 records process lessons without rewriting the historical commit of an active run.

## Naming and one-workflow rule

Every serious numbered search is `smart-search-N-short-description`. Keep exactly one visible workflow for each `N`; it owns precheck, smoke, smoke aggregate, full, exact checks, full aggregate and artifacts.

## Step-2 handoff contract

Persist before Step 3:

1. unused number and workflow name;
2. one primary hypothesis;
3. controls/ablations;
4. exact seeds and source runs;
5. local tests and negative neighborhoods;
6. invariants and exact success criteria;
7. one shared preflight;
8. smoke gate;
9. automatic smoke-to-full shape;
10. full resource profile;
11. shard and aggregate artifacts;
12. implementation language and reason;
13. launch dependencies and what evidence would permit an override.

The implementation language and launch dependencies are binding parts of the handoff.

## Handoff override rule

Step 3 must not silently override a Step-2 block, dependency, seed requirement or implementation-language decision.

An override is allowed only when all of the following are written before the trigger:

- exact reason and evidence;
- what source coverage or performance may be lost;
- a preflight guard that makes the exception explicit;
- the cleanup obligation after the run;
- a pointer from `frontier/active_run.json` to the amendment or retrospective.

## Shared preflight rule

Local and CI precheck use the same versioned command. It must compile sources, verify the known 23-link control, normalize and verify seeds twice, reconstruct structural invariants, exercise every mode, run the real miniature aggregate, verify all bank outputs, and assert 22 nonzero links.

For every serious full workflow it must also run:

```text
python scripts/check_long_run_budget.py \
  --search-seconds <seconds> \
  --timeout-minutes <timeout> \
  --minimum-headroom-seconds 900
```

Do not maintain separate local and CI test logic.

## Long-run budget rule

A job timeout covers checkout, setup, downloads, compilation, search, final trimming, exact verification, reports and artifact upload—not only the search executable.

Default serious full profile:

```text
seconds=20400
shards=20
max-parallel=20
workers=4 per shard
timeout-minutes=359
minimum headroom=900 seconds
```

`21000` seconds under a 359-minute job is unsafe: it leaves only `540` seconds. Use a longer search only after measured setup/finalization data proves the required headroom remains.

## Preferred automatic architecture

```text
precheck
  -> smoke matrix [20]
  -> smoke-aggregate
  -> full matrix [20]      needs smoke-aggregate success
  -> full-aggregate
  -> failure-report        if: always()
```

The scientific aggregate is strict and final only after all required shard artifacts exist. A lightweight failure report may run with `if: always()` and archive missing shard ids, checkpoints and available results, but it must clearly say `incomplete` and must not merge final banks.

## Permanent-input and provenance rules

Preferred rule: permanent seeds, manifests and sources are committed before smoke. Scientific workflows are read-only with respect to repository source and seeds.

If a workflow must materialize inputs from retained Actions artifacts:

- require an explicit minimum source-shard count;
- record source run id and artifact ids;
- produce a deterministic manifest and content hashes;
- upload the prepared input bundle once and reuse exactly that bundle in smoke and full;
- after the run, persist the bundle or a lossless reconstruction path in the final run archive;
- never leave the recorded scientific result dependent only on expiring Actions storage.

Use ordinary readable modules, not encoded payloads or runtime concatenation of arbitrary fragments.

## Implementation-language contract

The language selected in Step 2 is binding. A different language requires before launch:

- a representative benchmark;
- an explanation of why the deviation is acceptable;
- expected impact on explored states;
- a written amendment.

Do not silently replace a requested C++ search core with Python. Python is appropriate for materialization, aggregation and independent verification unless Step 2 explicitly chooses it for the search engine.

## Publication order and commit hygiene

Before writing repository files, prepare a file manifest grouped as:

1. permanent inputs and source modules;
2. verifiers, aggregate and preflight;
3. workflow;
4. active-run record;
5. trigger.

Publish one atomic Git tree commit when possible. If the tool cannot do that, use the smallest practical sequence:

```text
implementation bundle -> workflow -> active-run record -> trigger last
```

The trigger is always the last source-changing action. Do not edit the active workflow or its historical launch commit during Step 4.

## Mandatory single-prompt Step 3

A Step-3 request authorizes the whole chain: read the handoff and active run, implement, run shared local preflight, publish coherently, trigger once, require complete smoke aggregate and artifacts, automatically start full, verify the intended profile and jobs, record active-run identity, then stop without asking for another launch prompt.

If smoke fails and permissions allow a fix, diagnose and restart the chain in the same Step-3 work. Never repeat a trigger merely because a run id is not yet visible.

Step 3 is complete only when the intended full jobs are visible, not merely when the workflow is queued.

## Trigger safety

Before writing a trigger:

1. read `frontier/active_run.json`;
2. inspect trigger path and latest commit;
3. confirm no active or unrecorded equivalent run;
4. write once;
5. record launch commit immediately;
6. confirm the actual workflow run and intended full-job creation;
7. never duplicate without proof the first launch did not exist.

Generic and legacy workflows use narrow `paths:` filters so docs, memory and run archives do not start old searches.

## Failure handling

Distinguish:

- preflight/checker failure: code/schema/serialization problem;
- engine failure: inspect shard logs and inputs;
- job-time or runner interruption: inspect duration, headroom and absence of artifact;
- memory failure: require measured peak process-tree RAM, not guesswork;
- aggregation failure after successful shards: shard data may still be useful;
- missing artifact: record exact missing shard and create an incomplete archive;
- stale rerun: GitHub reruns use the historical commit, so later fixes do not affect it;
- connector safety block: tool-layer event, not CI or mathematical evidence.

Never describe a failed checker, missing shard or runner interruption as a mathematical negative result.

## Step-4 consistency sweep

Step 4 must inspect actual Actions state and then:

1. update `frontier/active_run.json` first;
2. remove contradictory live-stage text from `START_HERE.md`;
3. keep smoke and incomplete diagnostics out of `frontier/latest.*`;
4. record handoff, language, input, resource and publication deviations;
5. add a dated file under `docs/retrospectives/` when lessons are specific to one run;
6. verify that the next action is singular and non-duplicating;
7. do not launch, rerun, cancel or modify the historical active workflow unless explicitly requested.

## Prompt 1 — record run

```text
Сними результаты GitHub run: <RUN_URL>.

В начале нового чата один раз открой START_HERE.md, затем frontier/latest.*, frontier/active_run.json, runbook, workflow, artifacts, jobs/logs и нужные runs/candidates.

Если все обязательные shards и aggregate успешны, запиши completed run, обнови frontier, active_run, START_HERE и все три банка. Также сохрани точный prepared-seed bundle или его hashes/reconstruction manifest, если workflow материализовал seeds из Actions artifacts.

Если run неполный, не притворяйся, что он завершён: создай runs/<date>-<workflow>/ с partial summary, best checked candidates, missing-shard/failure analysis; обнови active_run как recovery pending; не сливай окончательные банки до строгого полного aggregate.

В конце скажи: было/стало, shard count, compact/original count, defect families, technical failure if any, and next non-duplicating action.
```

## Prompt 2 — choose next hypothesis

Do not begin while `frontier/active_run.json` contains an active retry, full run or pending recording. Use the last fully recorded run plus any clearly verified structural candidate. Choose one non-repeating hypothesis and save `docs/smart-search-N-<name>-launch.md`.

## Prompt 3 — implement and launch

Use the saved handoff. Treat its language, dependencies and inputs as binding unless a written amendment is created first. Run the shared preflight, including long-run budget validation. Normal full is `20400` seconds, 20 jobs, max-parallel 20, usually 4 workers/job and timeout 359 minutes. Execute the complete automatic smoke-to-full chain once and record the active run.

## Prompt 4 — whole-chat wrap-up

Review lost time, file-role confusion, stale live status, unrecorded overrides, local/CI drift, implementation-language drift, runtime-only inputs, duplicate runs, self-modifying workflows, fragmented commits, opaque sources, unsafe time headroom and unrecorded results. Update memory/process files without changing the historical commit of an active run.
