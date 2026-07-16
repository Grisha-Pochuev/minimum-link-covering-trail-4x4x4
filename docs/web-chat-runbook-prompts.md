# Web-chat runbook prompts

This file defines reusable process, not mathematical truth. Current mathematical state belongs in
`frontier/latest.*`; current execution stage belongs only in `frontier/active_run.json`.

## Automatic boot rule

For every new web-chat request that may inspect, change, run, or interpret this repository, the agent
must open `START_HERE.md` first exactly once and then follow its read-first order. This is automatic and
does not depend on the user remembering to mention it.

## File roles

- `START_HERE.md`: compact stable boot memory and reading order.
- `frontier/latest.*`: best checked mathematical frontier; no authoritative live-stage instructions.
- `frontier/active_run.json`: the only authoritative active run, retry, pending recording or selected-next-search stage.
- `docs/smart-search-N-*.md`: exact Step-2 to Step-3 handoff.
- `docs/retrospectives/*`: process lessons and explicit execution exceptions.
- `docs/templates/step3-release-manifest.example.json`: release-gate schema example.
- `runs/*`: completed evidence or explicitly labelled incomplete-attempt evidence.
- candidate banks/originals: reusable checked and diagnostic curves.

If `START_HERE.md` and `frontier/active_run.json` disagree about a live stage, trust `active_run.json`
and repair the contradiction in Step 4.

## Fixed four-step process

```text
1. Record a completed run, or explicitly archive an incomplete attempt.
2. Think creatively, test locally and choose one next hypothesis.
3. Freeze and validate one release, then execute preflight -> smoke -> full once.
4. Review the chat and improve project memory/process.
```

Step 2 is research and selection. Step 3 implements the saved handoff and must not broaden it silently.
Step 4 records process lessons without rewriting the historical commit of an active run.

## Naming and one-workflow rule

Every serious numbered search is `smart-search-N-short-description`. Keep exactly one visible workflow
for each `N`; it owns precheck, smoke, smoke aggregate, full, exact checks, full aggregate and artifacts.

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
13. all system/compiler/Python dependencies;
14. exact input transport format, hashes and member counts;
15. every output bank and its verifier contract;
16. launch dependencies and what evidence would permit an override.

The implementation language, dependencies, input transport and output verifier contract are binding
parts of the handoff.

## Handoff override rule

Step 3 must not silently override a Step-2 block, dependency, seed requirement, transport format,
output contract or implementation-language decision.

An override is allowed only when all of the following are written before the trigger:

- exact reason and evidence;
- what source coverage or performance may be lost;
- a preflight guard that makes the exception explicit;
- the cleanup obligation after the run;
- a pointer from `frontier/active_run.json` to the amendment or retrospective.

## Shared preflight rule

Local and CI precheck use the same versioned command. It must:

- compile sources;
- verify the known 23-link control;
- normalize and verify seeds twice;
- reconstruct structural invariants;
- exercise every mode;
- run the real miniature aggregate;
- verify every saved output bank, including diagnostic JSONL;
- reject every finite trail with a zero-length segment;
- assert exactly 22 nonzero links;
- record throughput and peak process-tree RAM.

For every serious full workflow it must also run:

```text
python scripts/check_long_run_budget.py \
  --search-seconds <seconds> \
  --timeout-minutes <timeout> \
  --minimum-headroom-seconds 900
```

Do not maintain separate local and CI test logic.

## Mandatory release-candidate gate

GitHub Actions is not the release debugger. Before any trigger:

1. Build one release-candidate commit containing all source, inputs, workflow and a
   `step3-release-v1` manifest.
2. Re-fetch or inspect the exact committed payload. Local files alone are not evidence that GitHub
   received the same bytes.
3. Run `python scripts/check_step3_release.py --manifest <manifest> --report <report>`.
4. Validate all hashes, archive CRC/member lists, split-file concatenations and workflow literals.
5. Compile in a clean environment with the exact declared dependencies.
6. Run every mode briefly and pass both exact verifiers over every emitted file.
7. Record the release commit and passing report in `frontier/active_run.json`.
8. Make the trigger a separate final commit and write it once.

If any source or input changes after the report, the report is invalid and the full gate must run again.
A failed run may be retried only from a new frozen release commit with a new passing report.

## Long-run budget rule

A job timeout covers checkout, setup, downloads, compilation, search, final trimming, exact verification,
reports and artifact upload—not only the search executable.

Default serious full profile:

```text
seconds=20400
shards=20
max-parallel=20
workers=4 per shard
timeout-minutes=359
minimum headroom=900 seconds
```

`21000` seconds under a 359-minute job is unsafe: it leaves only `540` seconds. Use a longer search only
after measured setup/finalization data proves the required headroom remains.

## Preferred automatic architecture

```text
release gate (before trigger)
  -> precheck
  -> smoke matrix [20]
  -> smoke-aggregate
  -> full matrix [20]      needs smoke-aggregate success
  -> full-aggregate
  -> failure-report        if: always()
```

The scientific aggregate is strict and final only after all required shard artifacts exist. A lightweight
failure report may run with `if: always()` and archive missing shard ids, checkpoints and available
results, but it must clearly say `incomplete` and must not merge final banks.

## Permanent-input and provenance rules

Preferred rule: permanent seeds, manifests and readable source modules are committed before smoke.
Scientific workflows are read-only with respect to repository source and seeds.

- Prefer ordinary UTF-8/JSONL/TSV files.
- Do not publish a large binary or one giant base64 payload through a connector and trust the local hash.
- If binary transport is unavoidable, split it into small deterministic text parts, record each part,
  concatenated text and decoded archive hashes, then test every archive member after reassembly.
- A corrupt or superseded bundle must be deleted or explicitly marked retired so later chats cannot use it.
- Opaque runtime archives are forbidden for new searches unless a written exception explains why normal
  sources cannot be committed; the final run archive must contain the unpacked readable sources.

If a workflow must materialize inputs from retained Actions artifacts:

- require an explicit minimum source-shard count;
- record source run id and artifact ids;
- produce a deterministic manifest and content hashes;
- upload the prepared input bundle once and reuse exactly that bundle in smoke and full;
- after the run, persist the bundle or a lossless reconstruction path in the final run archive;
- never leave the recorded scientific result dependent only on expiring Actions storage.

## Dependency contract

Every non-standard header, package and runtime module must be listed in the Step-2 handoff and installed
or vendored before the first trigger. Local success is not enough when the local machine may already have
the dependency. Compile once in a clean runner-equivalent environment.

## Output-contract rule

The engine must enforce invariants before writing, and the preflight must independently re-read all
written outputs. The verifier sweep covers best candidates, ordinary banks, originals, checkpoints,
valley/diagnostic banks and aggregate files. Diagnostic data is not exempt from geometry validity.

## Implementation-language contract

The language selected in Step 2 is binding. A different language requires before launch:

- a representative benchmark;
- an explanation of why the deviation is acceptable;
- expected impact on explored states;
- a written amendment.

Do not silently replace a requested C++ search core with Python. Python is appropriate for
materialization, aggregation and independent verification unless Step 2 explicitly chooses it for the
search engine.

## Publication order and commit hygiene

Prepare a file manifest grouped as:

1. permanent inputs and ordinary source modules;
2. verifiers, aggregate and preflight;
3. workflow;
4. release manifest and passing report;
5. active-run record with release commit;
6. trigger.

Publish one atomic Git tree commit when possible. Otherwise use the smallest practical sequence:

```text
implementation bundle -> workflow -> release gate -> active-run record -> trigger last
```

The trigger is always the last source-changing action. Do not edit the active workflow or its historical
launch commit during Step 4.

## Mandatory single-prompt Step 3

A Step-3 request authorizes the whole chain: auto-read `START_HERE.md`, read the handoff and active run,
implement, freeze a release candidate, run the release gate and shared preflight, publish coherently,
trigger once, require complete smoke aggregate and artifacts, automatically start full, verify the
intended profile and jobs, record active-run identity, then stop without asking for another launch prompt.

If smoke fails and permissions allow a fix, diagnose it, create a new release candidate, rerun the full
release gate and only then trigger again. Never use a trigger merely to discover packaging, dependency or
serialization mistakes.

Step 3 is complete only when the intended full jobs are visible, not merely when the workflow is queued.

## Trigger safety

Before writing a trigger:

1. read `frontier/active_run.json`;
2. confirm a passing release report for the exact release commit;
3. inspect trigger path and latest commit;
4. confirm no active or unrecorded equivalent run;
5. write once;
6. record launch commit immediately;
7. confirm the actual workflow run and intended full-job creation;
8. never duplicate without proof the first launch did not exist.

Generic and legacy workflows use narrow `paths:` filters so docs, memory and run archives do not start
old searches.

## Failure handling

Distinguish:

- release-gate failure: do not trigger;
- preflight/checker failure: code/schema/serialization problem, not mathematical evidence;
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
2. remove contradictory live-stage text from `START_HERE.md` and `frontier/latest.*`;
3. keep smoke and incomplete diagnostics out of the mathematical frontier;
4. record language, dependency, input, output, resource and publication deviations;
5. add a dated file under `docs/retrospectives/` for run-specific lessons;
6. retire/delete corrupt payloads while preserving the historical active commit;
7. verify that the next action is singular and non-duplicating;
8. do not launch, rerun, cancel or modify the historical active workflow unless explicitly requested.

## Prompt 1 — record run

```text
Сними результаты GitHub run: <RUN_URL>.

В начале нового чата сам один раз открой START_HERE.md, затем frontier/latest.*,
frontier/active_run.json, runbook, workflow, artifacts, jobs/logs и нужные runs/candidates.

Если все обязательные shards и aggregate успешны, запиши completed run, обнови frontier, active_run,
START_HERE и все три банка. Сохрани точный prepared-seed bundle или его hashes/reconstruction manifest.

Если run неполный, создай runs/<date>-<workflow>/ с partial summary, best checked candidates,
missing-shard/failure analysis; обнови active_run как recovery pending; не сливай окончательные банки.
```

## Prompt 2 — choose next hypothesis

Do not begin while `frontier/active_run.json` contains an active retry, full run or pending recording.
Use the last fully recorded run plus any clearly verified structural candidate. Choose one non-repeating
hypothesis and save `docs/smart-search-N-<name>-launch.md`.

## Prompt 3 — implement and launch

Auto-read `START_HERE.md`. Use the saved handoff. Treat its language, dependencies, inputs and output
contracts as binding. Freeze one release candidate, run `scripts/check_step3_release.py`, clean compile,
all-mode miniature execution and full output verification. Trigger separately and once. Normal full is
`20400` seconds, 20 jobs, max-parallel 20, usually 4 workers/job and timeout 359 minutes. Execute the
complete automatic smoke-to-full chain and record the active run.

## Prompt 4 — whole-chat wrap-up

Review lost time, skipped boot memory, stale live status, unrecorded overrides, local/CI drift,
dependency drift, runtime-only inputs, corrupted transport, incomplete output verification, duplicate
runs, self-modifying workflows, fragmented commits, opaque sources, unsafe time headroom and unrecorded
results. Update memory/process files without changing the historical commit of an active run.
