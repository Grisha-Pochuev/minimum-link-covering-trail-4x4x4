# START HERE — compact agent memory

Last updated: 2026-07-14

Read this file first in a new web chat. It is boot memory, not the full diary.

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
6. current numbered-search launch document and workflow
7. latest relevant `runs/` archive
8. candidate banks/originals
9. Actions jobs, logs and artifacts

File roles:

- `START_HERE.md`: stable compact boot memory and reading order. It must not be the authoritative live-stage tracker.
- `frontier/latest.*`: best checked mathematical frontier.
- `frontier/active_run.json`: the only authoritative live run/stage record.
- `docs/smart-search-N-*.md`: binding Step-2 to Step-3 handoff.
- `docs/retrospectives/*`: process lessons and explicit execution exceptions; not mathematical frontier.
- `runs/*`: completed or explicitly labelled partial-run evidence.
- candidate banks/originals: reusable checked and diagnostic candidates.

If this file and `frontier/active_run.json` disagree about the current stage, trust `active_run.json` and repair this file during Step 4.

## Current checked frontier

Best checked ordered trail:

- id: `mlct22-ct-c64aebf0ed34cdf4`
- file: `runs/2026-07-13-smart-search-23-core-transplant-full/best_candidate.json`
- coverage: `62/64`
- links: `22`
- missing: `(1,0,2)`, `(3,3,1)`
- source run: `29249275103`, first attempt, shard `14`
- frozen-core overlap: `16/18`
- status: `verified_partial_candidate_from_incomplete_run`

It passed both CI exact verifiers and two additional local exact checks.

The numeric frontier did not increase, but the structural frontier did: search-22's best 62-curves retained all 18 frozen-core lines, while this candidate breaks two and belongs to a new two-hole orbit.

## Historical search-23 source state

Run `29249275103`, workflow `smart-search-23-core-transplant`:

- first attempt produced `19/20` shard artifacts;
- shard 11 produced no artifact and was retried under the historical commit;
- checked partial archive: `runs/2026-07-13-smart-search-23-core-transplant-full/`;
- checked partial statistics: `1115` compact exact `62/64`, `40` with frozen-core overlap `<=16`, `1600` compact core-escape diagnostics, `74` raw originals, no `63/64` or `64/64` ordered trail.

Search-24 was later launched under an explicit 19-shard source exception because all 40 known primary core-escape seeds came from available shard 14. The exact exception and cleanup obligation are recorded in `frontier/active_run.json` and `docs/retrospectives/2026-07-14-search-24-step3.md`.

## Current active search identity

Active workflow: `smart-search-24-defect-graft`

Run: `29357369876`

URL: `https://github.com/Grisha-Pochuev/minimum-link-covering-trail-4x4x4/actions/runs/29357369876`

Launch commit: `7ece93a06ea910371ea6a987e43d5b6cdd3e21b5`

Always read `frontier/active_run.json` for the current stage. Do not duplicate this run.

Dated smoke snapshot:

- strict `20/20` smoke aggregate succeeded;
- best ordered trail remained `62/64`;
- `1901` compact exact `64/64` supporting-line sets;
- `93` connected exact `64/64` line sets;
- `0` Hamiltonian supporting-line orders;
- `0` ordered `63/64` or `64/64` trails.

These are smoke diagnostics, not the final search-24 result.

## Search-24 hypothesis

The line through the two missing points is the exact missing coverage object for many search-23 `62/64` seeds. The current search replaces a zero-contribution or zero-exclusive link by that defect line, replaces additional weak links by exact connector lines, then solves the exact supporting-line intersection ordering and finite-segment realization problem.

An unordered `64/64` line set is not a trail. A Hamiltonian order of infinite supporting lines is not success until finite segments are exactly realized and checked.

## Search history

- search-17: unordered 22-line `64/64` scaffolds, not trails.
- search-18: ordered reconstruction `44/64`.
- search-19: contact-state reconstruction `46/64`.
- search-20: rich-line preservation `58/64`, but eight explicit bridges.
- search-21: direct compression `61/64`, zero pure bridges.
- search-22: endpoint repair `62/64`, saturated in one frozen 18-line family.
- search-23: core transplant; exact `62/64` with frozen-core overlap `16/18` and a new defect orbit.
- search-24: defect-line graft plus exact connector topology and Hamiltonian support ordering; active run `29357369876`.

The unordered `64/64` scaffold from run `28825060197` remains in its separate diagnostic bank.

## Permanent long-run safety

The search-23 shard-11 failure was most likely a job-time/runner interruption, not OOM:

- measured sibling RAM was at most `0.3404 GiB`;
- search seconds were `21000`;
- timeout was `359` minutes;
- only `540` seconds remained for setup, compilation, finalization, two verifiers and upload.

Permanent rule:

- normal full search time is `20400` seconds when job timeout is `359` minutes;
- every serious workflow runs `scripts/check_long_run_budget.py` in preflight;
- require at least `900` seconds headroom;
- current search-24 headroom is `1140` seconds;
- scientific aggregate is final only with all required shards and exact verifiers;
- an incomplete failure report must never be called a completed mathematical result;
- rerunning an old run uses its historical commit and does not receive later fixes.

## Four-step cycle

1. Record a completed run, or explicitly archive an incomplete attempt without pretending it is complete.
2. Select and test one non-repeating hypothesis; save a precise launch document.
3. Implement and automatically execute one complete chain: shared preflight -> smoke aggregate -> full launch.
4. Review process and memory without changing the historical commit of an active run.

## Step-3 permanent rules

A Step-3 request authorizes the complete automatic chain:

```text
precheck
  -> smoke[20]
  -> smoke-aggregate
  -> full[20] only after smoke success
  -> full-aggregate
```

Additional rules:

- local validation and GitHub precheck call the same versioned preflight;
- normalize seed schemas before exact checking;
- permanent seeds should be committed before smoke;
- if runtime artifact materialization is unavoidable, record exact artifact ids, source shard count, hashes and a final persistence obligation;
- the Step-2 implementation language is binding unless a benchmarked written exception is recorded before launch;
- prepare a file manifest before publishing;
- publish one atomic tree commit when possible, otherwise implementation bundle -> workflow -> active-run record -> trigger last;
- never repeat a trigger without proving no equivalent run exists;
- Step 3 ends only after intended full jobs are visible;
- long-run preflight validates total job headroom, not only search seconds.

## Step-4 consistency sweep

At every retrospective:

1. inspect the actual Actions stage and artifacts;
2. update `frontier/active_run.json` first;
3. remove contradictory live instructions from `START_HERE.md`;
4. keep smoke or partial diagnostics out of the mathematical frontier;
5. record any handoff, language, input or resource exception;
6. do not modify the historical commit used by an active run;
7. do not launch, rerun or cancel during Step 4 unless explicitly requested.

## Current next action

Read `frontier/active_run.json`.

Do not start another search-24 copy. Let the active full matrix and strict aggregate finish. The next Step 1 must inspect all full jobs, logs and artifacts, require exact `20/20`, persist the prepared seed material and provenance, archive the run, merge ordinary/diagnostic/originals banks only after exact final verification, and then update the mathematical frontier.

Do not treat heuristic failure, a checker failure, a technical missing shard, a connected line set without Hamiltonian order, or an unordered `64/64` cover as proof that 22 links are impossible.
