# START HERE — compact agent memory

Last updated: 2026-07-15

Read this file first in a new web chat. It is boot memory, not the full diary.

## Project

Repository: `Grisha-Pochuev/minimum-link-covering-trail-4x4x4`

Goal: find an exact 22-link polygonal trail covering all 64 points of `{0,1,2,3}^3`, or obtain
strong structural evidence toward impossibility.

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
6. current numbered-search handoff and workflow
7. latest relevant `runs/` archive
8. candidate banks/originals
9. Actions jobs, logs and artifacts

File roles:

- `START_HERE.md`: stable compact boot memory and reading order.
- `frontier/latest.*`: best checked mathematical frontier.
- `frontier/active_run.json`: the only authoritative live stage record.
- `docs/smart-search-N-*.md`: binding Step-2 to Step-3 handoff.
- `docs/retrospectives/*`: process lessons and explicit execution exceptions.
- `runs/*`: completed or explicitly labelled partial-run evidence.
- candidate banks/originals: reusable checked and diagnostic candidates.

If this file and `frontier/active_run.json` disagree about the current stage, trust
`frontier/active_run.json` and repair this file during Step 4.

## Current checked frontier

Best checked ordered trail:

- id: `mlct22-ct-c64aebf0ed34cdf4`
- file: `runs/2026-07-13-smart-search-23-core-transplant-full/best_candidate.json`
- coverage: `62/64`
- links: `22`
- missing: `(1,0,2)`, `(3,3,1)`
- source run: `29249275103`, shard `14`
- frozen-core overlap: `16/18`
- status: exactly verified partial trail from a now-completed run

It passed both CI exact verifiers and two additional local exact checks. Search-24 did not produce a
better ordered trail.

## Latest completed run

Workflow: `smart-search-24-defect-graft`  
Run: `29357369876`  
Archive: `runs/2026-07-14-smart-search-24-defect-graft-full/`

Strict completion:

- precheck: success;
- smoke: `20/20`;
- full: `20/20`;
- strict aggregate: success;
- missing shards: none;
- exact ordered `63/64`: `0`;
- exact ordered `64/64`: `0`.

Main diagnostics:

- `5,782,422` raw exact `64/64` supporting-line-set attempts;
- `3,165` compact exact `64/64` line sets;
- `2,349` connected compact exact `64/64` line sets;
- `2,268` saved near-Hamiltonian graph rows;
- `0` Hamiltonian supporting-line orders;
- `0` finite `63/64` or `64/64` realizations;
- ordinary bank: `21` exact `62/64` rows;
- diagnostic bank: `5,821` exact rows;
- originals: `20` raw shard bests, `2` compact classes.

Interpretation: the defect line repairs coverage at the unordered-line level, but the explored
connector topologies do not stitch into a Hamiltonian support order. This is a bounded negative
result for search-24, not a proof that 22 links are impossible.

## Search-23 source completion

Run `29249275103` later completed its strict `20/20` recovery aggregate:

- exact `62/64` with frozen-core overlap `<=16`: still `40`;
- compact `63/64`: `0`;
- compact `64/64`: `0`.

Therefore search-24's 19-shard launch exception did not omit any intended primary core-escape seed.
The exact prepared bundle is now permanent:

- `data/search24_prepared_inputs.zip`
- `data/search24_defect_graft_manifest.json`
- `data/search24_prepared_inputs.README.md`

Hashes and artifact provenance are in the search-24 archive.

## Search history

- search-17: unordered 22-line `64/64` scaffolds, not trails.
- search-18: ordered reconstruction `44/64`.
- search-19: contact-state reconstruction `46/64`.
- search-20: rich-line preservation `58/64`, but eight explicit bridges.
- search-21: direct compression `61/64`, zero pure bridges.
- search-22: endpoint repair `62/64`, saturated in one frozen 18-line family.
- search-23: core transplant; exact `62/64` with frozen-core overlap `16/18` and a new defect orbit.
- search-24: defect-line graft; many exact connected `64/64` line sets, but zero Hamiltonian orders.

The unordered `64/64` scaffold from run `28825060197` remains in its separate diagnostic bank.

## Current stage

There is no active run. `frontier/active_run.json` is
`completed_recorded_awaiting_step2`.

The next action is Step 2: choose one non-repeating `smart-search-25-*` hypothesis and save a precise
handoff. Do not rerun search-24 unchanged.

## Performance lesson

Search-24 used at most `0.0739 GiB` measured RAM and no shard hit the state cap, but Python throughput
was only `14.17` attempts/s/shard. Before increasing the same graft depth, benchmark the binding
C++20 architecture or write a new explicit implementation-language exception.

## Permanent long-run safety

- normal full search time is `20400` seconds when timeout is `359` minutes;
- every serious workflow runs `scripts/check_long_run_budget.py`;
- require at least `900` seconds headroom;
- scientific aggregate is final only with all required shards and exact verifiers;
- an incomplete failure report must never be called a completed mathematical result;
- rerunning an old run uses its historical commit and does not receive later fixes.

## Four-step cycle

1. Record a completed run, or explicitly archive an incomplete attempt.
2. Select and test one non-repeating hypothesis; save a precise launch document.
3. Implement and execute one chain: shared preflight -> smoke aggregate -> full launch.
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
- runtime materialization requires artifact ids, hashes and final persistence;
- the Step-2 implementation language is binding unless a benchmarked exception is recorded;
- prepare a file manifest before publishing;
- publish one atomic tree commit when possible;
- trigger last and never duplicate without proving no equivalent run exists;
- Step 3 ends only after intended full jobs are visible;
- long-run preflight validates total job headroom.

## Current next action

Read `frontier/active_run.json`, then perform Step 2. Use the completed search-24 topology data to
choose search-25. Do not launch, rerun or treat the absence of a Hamiltonian order in this bounded
neighborhood as a global impossibility result.
