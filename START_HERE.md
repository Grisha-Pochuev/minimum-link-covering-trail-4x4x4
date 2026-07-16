# START HERE — compact agent memory

Last updated: 2026-07-16

## Mandatory boot rule

For every new web-chat task that may inspect, change, run, or interpret this repository, open this file
first exactly once. This is automatic agent responsibility; it does not depend on the user remembering
to ask. Then follow the read-first order below.

This file is boot memory, not the full diary. Live execution state belongs only in `frontier/active_run.json`.

## Project

Repository: `Grisha-Pochuev/minimum-link-covering-trail-4x4x4`

Goal: find an exact 22-link polygonal trail covering all 64 points of `{0,1,2,3}^3`, or obtain strong structural evidence toward impossibility.

- 23 links: known exact full construction.
- 22 links: open; best checked ordered trail covers `62/64`.
- 21 links: not a current serious search target.

Heuristic output is evidence only. Every frontier candidate requires exact checking.

## Read-first order

1. `START_HERE.md`
2. `frontier/latest.md`
3. `frontier/latest.json`
4. `frontier/active_run.json`
5. `docs/web-chat-runbook-prompts.md`
6. current numbered-search handoff, release manifest, workflow and trigger
7. latest relevant `runs/` archive
8. candidate banks/originals
9. Actions jobs, logs and artifacts

File roles:

- `START_HERE.md`: stable compact boot memory and reading order.
- `frontier/latest.*`: best checked mathematical and structural frontier; never infer live stage from it.
- `frontier/active_run.json`: the only authoritative live stage record.
- `docs/smart-search-N-*.md`: binding Step-2 to Step-3 handoff.
- `docs/retrospectives/*`: dated process lessons and exceptions.
- `docs/templates/step3-release-manifest.example.json`: machine-readable release-gate template.
- `runs/*`: completed or explicitly labelled partial-run evidence.
- candidate banks/originals: reusable checked and diagnostic candidates.

If this file and `frontier/active_run.json` disagree about the current stage, trust `frontier/active_run.json` and repair this file during Step 4.

## Current checked numeric frontier

Best checked ordered trail:

- id: `mlct22-ct-c64aebf0ed34cdf4`
- file: `runs/2026-07-13-smart-search-23-core-transplant-full/best_candidate.json`
- coverage: `62/64`
- links: `22`
- missing: `(1,0,2)`, `(3,3,1)`
- source run: `29249275103`, shard `14`
- frozen-core overlap: `16/18`
- status: exactly verified partial trail from a completed run

It passed both CI exact verifiers and two additional local exact checks. Searches 24 and 25 did not produce `63/64`.

## Latest completed recorded run

Workflow: `smart-search-25-core-valley`  
Run: `29457051261`  
Archive: `runs/2026-07-16-smart-search-25-core-valley-full/`

Strict result:

- precheck, smoke and full aggregate: success, `20/20` shards;
- exact ordered `63/64+`: `0`;
- exact ordered `64/64`: `0`;
- atomic paired attempts: `6,151,145,399`;
- finite contact-span realizations: `78,081,729`;
- minimum overlap with the formerly common 17-line core: `14/17`;
- new exact ordinary `62/64` rows: `53`;
- exact diagnostic valley rows: `16,052` (`59/64`–`61/64`);
- raw shard bests: `20`, compact symmetry/reversal classes: `5`.

Run-best candidate: `mlct22-cv-40a5999c05294be6`, `62/64`, missing `(0,2,1)` and `(3,3,1)`, common-core overlap `14/17`.

Interpretation: search-25 genuinely escaped the closed one-line plateau and changed three of the common 17 supporting lines, but no tested atomic two-line repair reached `63/64`. This strongly weakens that repair family; it is bounded computational evidence, not an impossibility proof.

## Search-25 structural basis and conclusion

Exact local report: `docs/experiments/2026-07-15-search25-core-valley-analysis.md`.

The natural one-rich-line neighborhood around the wall was closed exactly:

- `43` exact ordered `62/64` states;
- `134` one-line-replacement edges, one component, diameter `8`;
- no outgoing one-rich-line replacement to `63/64`;
- all `43` states share the same `17` supporting lines;
- breaking one common-core line yields `641` exact `61/64` valley states.

Search-25 then tried atomic paired changes from this valley at large scale. It reached `14/17` overlap but still no `63/64`. Do not rerun search-25 unchanged merely with a new seed.

## Canonical search-25 inputs and provenance

The original `data/search25_local_inputs.zip` was CRC-corrupted and is retired. Never use it.

Canonical lossless transport:

- parts: `data/search25_reconstructed_inputs.parts/part00.b64` through `part07.b64`;
- concatenated base64 SHA-256: `18c0a360cad88dafa40cd5ff039fca4b3a94f293010e3f5b2d3600b985236cfd`;
- decoded ZIP SHA-256: `49210583f1bc518b31decaa23b6c07b83ae3104e36e1b048d5ffba4e475ee182`;
- runtime archive: `data/search25_runtime.tar.gz`, SHA-256 `51f642824516333142732818b9eaca75932b7c1aeca4e0788cbad63e2869b493`;
- historical trigger commit: `22becb63bb5dc00fcc547e97a9366f25b35c391b`.

Search-25 is historical evidence. Do not edit or rerun its historical commit to apply later fixes.


## Search-25 launch retrospective

Detailed record: `docs/retrospectives/2026-07-16-search25-launch-failures.md`.

Eight attempts failed before the successful full run because the release was not frozen and verified
before each trigger. Failures included corrupted binary/base64 transport, an undeclared Boost dependency,
and zero-length segments reaching a diagnostic bank. The smoke gate protected the expensive full search,
but GitHub Actions was incorrectly used as a release debugger.

The successful historical run still uses `data/search25_runtime.tar.gz`; do not edit its historical commit.
The exact archive and hashes are durable, but the post-run cleanup item to duplicate its unpacked readable
sources inside the completed run archive remains incomplete. Search-26 and later must use ordinary readable
source files and a passing `step3-release-v1` gate before triggering.

## Mandatory Step-3 release gate

Before any future trigger commit:

1. Read this file and `frontier/active_run.json`; user reminder is not required.
2. Freeze one release-candidate commit containing readable source, inputs, workflow and a `step3-release-v1` manifest.
3. Re-fetch or check the exact committed payload, not only a local working copy.
4. Run `scripts/check_step3_release.py` against the manifest.
5. Verify every archive member and every concatenated part by SHA-256.
6. Compile in a clean environment with every dependency listed in the handoff and workflow.
7. Run a miniature execution of every mode and both exact verifiers over every saved output bank,
   including diagnostic JSONL.
8. Require exactly `22` nonzero links for every finite trail.
9. Record a passing release report and release commit in `frontier/active_run.json`.
10. Trigger in a separate final commit, exactly once.

A trigger is forbidden while any release-gate item is missing. GitHub Actions is not the release debugger.
A failed attempt may be retried only after the whole gate passes again on the new frozen release commit.

## Search history

- search-17: unordered 22-line `64/64` scaffolds, not trails.
- search-18: ordered reconstruction `44/64`.
- search-19: contact-state reconstruction `46/64`.
- search-20: rich-line preservation `58/64`, but eight explicit bridges.
- search-21: direct compression `61/64`, zero pure bridges.
- search-22: endpoint repair `62/64`, saturated in one frozen 18-line family.
- search-23: core transplant; `62/64`, two frozen-core lines changed, new defect orbit.
- search-24: defect-line graft; many unordered/connected `64/64` sets, no trail.
- search-25: atomic paired core-valley search; `6.15` billion attempts, overlap down to `14/17`, no `63/64`.

## Performance and long-run safety

- normal full search time: `20400` seconds with timeout `359` minutes;
- every serious workflow runs `scripts/check_long_run_budget.py`;
- require at least `900` seconds headroom;
- scientific aggregate is final only with all required shards and exact verifiers;
- incomplete failures are technical evidence only, never mathematical negative results;
- rerunning an old run uses its historical commit and does not receive later fixes.

## Four-step cycle

1. Record a completed run, or explicitly archive an incomplete attempt.
2. Select and test one non-repeating hypothesis; save a precise launch document.
3. Freeze and validate one release -> trigger once -> strict smoke -> automatic full.
4. Review process and memory without changing the historical commit of an active run.

## Next action

Step 1 is complete for run `29457051261`. Perform Step 2: analyze search-25 and choose one genuinely broader, non-repeating hypothesis. Do not launch or rerun anything until a new binding handoff exists.
