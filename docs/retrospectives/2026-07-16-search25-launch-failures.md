# Retrospective — smart-search-25 launch failures

Date: 2026-07-16  
Working run: `29457051261`  
Scope: technical launch process only; no mathematical conclusion is drawn from failed attempts.

## What happened

Search-25 reached the intended full `20`-shard run only on attempt 9. Attempts 1–8 failed before the
expensive full search:

| Attempt | Run | Failure | Full search |
|---:|---:|---|---|
| 1 | `29452854208` | shared preflight failure | not started |
| 2 | `29453335991` | outer input-bundle hash gate | not started |
| 3 | `29453747947` | shared 20-mode preflight | not started |
| 4 | `29454149578` | corrupted replacement runtime archive | not started |
| 5 | `29454334615` | CRC-corrupted core-break member in the Step-2 ZIP | not started |
| 6 | `29456161606` | one large base64 payload changed during publication | not started |
| 7 | `29456531140` | runner lacked `boost/rational.hpp` | not started |
| 8 | `29456610021` | zero-length finite segments entered a diagnostic valley bank | not started |
| 9 | `29457051261` | precheck and strict smoke `20/20` succeeded; full launched | running |

The smoke architecture prevented all eight technical failures from consuming a five-hour full matrix.
That protection worked. The process before the trigger did not.

## Root causes

### 1. Boot memory was not loaded automatically

The chat did not begin by reading `START_HERE.md`. The user also forgot to remind the agent, but this
must not be a user responsibility. As a result, repository roles, input provenance and launch discipline
had to be reconstructed during the launch itself.

Permanent correction: every repository task auto-opens `START_HERE.md` once, even when the user does not
mention it.

### 2. The trigger was used as a release test

The implementation was repeatedly published and triggered before one frozen release commit had passed
all packaging, dependency, compilation and output-contract checks. GitHub Actions therefore became the
place where the release package was debugged.

Permanent correction: Step 3 now has two distinct phases:

1. freeze and validate a release candidate;
2. make a separate trigger commit only after a passing release report.

### 3. Binary/input transport was not round-trip verified

The original Step-2 ZIP contained a CRC-corrupted member. A later replacement used one large base64 text
file, which changed during publication. Local hashes did not prove that the bytes stored on GitHub were
the same bytes.

Permanent correction:

- the corrupt `data/search25_local_inputs.zip` is retired and removed from the current branch;
- the canonical input is eight small deterministic base64 parts;
- both concatenated-text and decoded-ZIP SHA-256 values are recorded;
- every ZIP member is tested after reconstruction;
- future binary transport must be validated from the committed payload, not only before upload.

### 4. The environment dependency was implicit

Local compilation succeeded because Boost was available locally. `ubuntu-latest` did not provide the
required header. The dependency was not part of the original launch contract.

Permanent correction: every external header/package must appear in the Step-2 handoff, release manifest
and workflow. A clean runner-equivalent compile is required before trigger.

### 5. The output contract covered the best trail but not every bank

The engine could save a diagnostic valley row containing adjacent duplicate vertices. That represents a
zero-length link and is not a valid 22-link trail. The initial preflight did not independently sweep every
saved diagnostic file.

Permanent correction:

- reject zero-length segments inside the engine before saving;
- re-read every best/ordinary/original/checkpoint/diagnostic output;
- run both exact verifiers over all finite trails;
- require exactly 22 nonzero links everywhere, including diagnostic banks.

### 6. Opaque runtime packaging increased fragility

Search-25 was distributed as `data/search25_runtime.tar.gz` and patched at runtime. This made source
inspection, dependency discovery and byte-level publication harder than ordinary committed source files.

Permanent correction: new numbered searches use readable committed source modules. The search-25 runtime
archive is a frozen historical exception because run `29457051261` is active. After completion, its
unpacked source and hashes must be persisted in the final run archive.

## What worked well

- No failed attempt reached the expensive full matrix.
- Hash and CRC gates prevented corrupted scientific inputs from being accepted.
- Strict smoke required all `20/20` artifacts and blocked the bad diagnostic rows.
- Two independent verifiers remained mandatory.
- `frontier/active_run.json` eventually recorded every attempt and the one run that must not be duplicated.
- The final release passed precheck, strict smoke and automatic smoke-to-full gating.

## New release gate

Before any future numbered-search trigger:

1. auto-read `START_HERE.md` and `frontier/active_run.json`;
2. commit ordinary source, exact inputs, workflow and `step3-release-v1` manifest;
3. inspect/re-fetch the committed payload;
4. run `scripts/check_step3_release.py`;
5. test hashes, archive integrity, split concatenation and required workflow literals;
6. clean-compile with declared dependencies;
7. briefly execute every mode;
8. verify every emitted output with both exact verifiers and the nonzero-link invariant;
9. record the passing report and release commit in `frontier/active_run.json`;
10. trigger in a separate final commit exactly once.

Any change after the passing report invalidates the report. A retry requires a new release candidate and a
new complete gate, not a small unverified patch followed immediately by another trigger.

## Current cleanup

- `START_HERE.md` now reflects active run `29457051261` and makes boot automatic.
- `docs/web-chat-runbook-prompts.md` now contains the release-candidate gate, dependency contract,
  transport rules and full output sweep.
- `data/search25_local_inputs.README.md` identifies the canonical eight-part reconstruction.
- stale live-stage instructions are removed from `frontier/latest.*`.
- the corrupted legacy ZIP is removed from the current branch.
- the active workflow and its historical trigger commit are not changed during this retrospective.

## Next action

Monitor only run `29457051261`. After it finishes, perform strict Step 1 recording and persist the
unpacked readable search-25 runtime in the completed run archive. Do not launch another search-25 run.
