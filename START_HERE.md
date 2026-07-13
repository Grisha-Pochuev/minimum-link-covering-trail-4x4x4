# START HERE — compact agent memory

Last updated: 2026-07-13

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

- `frontier/latest.*`: best checked mathematical frontier.
- `frontier/active_run.json`: active run or selected next search.
- `docs/smart-search-N-*.md`: binding Step-2 to Step-3 handoff.
- `docs/retrospectives/*`: process lessons; not mathematical frontier.
- `runs/*`: completed-run evidence.

## Current frontier

Best recorded candidate:

- id: `mlct22-er-7671ee46bd711a25`
- file: `runs/2026-07-12-smart-search-22-endpoint-repair-full/best_candidate.json`
- coverage: `62/64`
- links: `22`
- missing: `(0,2,1)`, `(3,3,1)`
- source run: `29181546758`
- status: `verified_partial_candidate`

It passed both exact rational verifiers.

## Search-22 structural result

Full run `29181546758` produced `1053` checked `62/64` classes, but they share one frozen 18-line core:

- the core covers `58/64`;
- only four links vary;
- there are exactly seven two-hole families, all in plane `z=1`;
- shallow repair, crossover, 2-opt, 3-opt and simple defect-line insertion did not reach `63/64`;
- one `61/64` donor has core overlap `16`;
- four `60/64` donors have overlap only `2`.

Full evidence:

`docs/experiments/2026-07-12-search22-frozen-core-analysis.md`

## Search history

- search-17: unordered 22-line `64/64` scaffolds, not trails.
- search-18: ordered reconstruction `44/64`.
- search-19: contact-state reconstruction `46/64`.
- search-20: rich-line preservation `58/64`, but eight explicit bridges.
- search-21: direct compression `61/64`, zero pure bridges.
- search-22: endpoint repair `62/64`, saturated in one frozen 18-line family.
- search-23: core transplant; implementation and smoke complete, full launched.

The unordered `64/64` scaffold from run `28825060197` is not an ordered trail and must remain in its separate bank.

## Active search-23

Workflow:

`smart-search-23-core-transplant`

Binding specification:

`docs/smart-search-23-core-transplant-launch.md`

Primary hypothesis: break at least one, preferably two, frozen-core lines and rebuild connected or paired `4–8`-link neighborhoods using structurally different `60/64–61/64` donor blocks.

Operational state:

- first smoke `29247958417`: stopped in precheck because the new checker required a redundant `links` field absent from compact seed rows;
- checker compatibility fixed;
- successful smoke `29248411212`: precheck, 20/20 shards, dual exact checks and aggregate artifact succeeded;
- full profile triggered from commit `ac18bf46b23146f4f4a581cbf5af641c746d3171`;
- full parameters: `21000` seconds, 20 shards, max-parallel 20, four workers per shard;
- `frontier/active_run.json` is authoritative and forbids duplicate launch.

Do not edit or replace the historical launch commit of the active run.

## Four-step cycle

1. Record a completed run.
2. Select and test one non-repeating hypothesis; save a precise launch document.
3. Implement and automatically execute one complete chain: local preflight → smoke aggregate → full launch.
4. Review process and memory.

The four user-facing steps remain fixed.

## Mandatory single-prompt Step-3 rule

A Step-3 request authorizes the complete chain. The assistant must not require a second user prompt merely to start full after smoke.

For future numbered searches, prefer one `auto` workflow profile:

```text
precheck
  -> smoke[20]
  -> smoke-aggregate
  -> full[20] only after smoke success
  -> full-aggregate
```

Manual smoke/full profiles may remain for debugging, but normal Step 3 uses `auto` or one narrow `auto.trigger`.

Additional rules learned from search-23:

- local validation and GitHub precheck must call the same versioned preflight script with the same seed files;
- normalize the seed schema before exact checkers; do not assume redundant fields are present;
- commit all permanent seeds before smoke; a scientific workflow must not commit source or seeds back to `main` during precheck;
- scientific aggregate runs only after required shards succeed;
- publish a coherent implementation in one atomic Git tree commit, or the smallest practical number of commits, rather than many one-file commits;
- a ChatGPT connector safety block is not evidence that GitHub Actions launch is forbidden: verify repository state, retry a smaller explicit non-trigger write, and never repeat a trigger without proving no run was created;
- Step 3 ends only after the full run is visible with the intended profile, green precheck and all expected shard jobs.

Detailed retrospective:

`docs/retrospectives/2026-07-13-search23-step3.md`

## Current next action

Read `frontier/active_run.json`.

- Do not launch another search-23 copy.
- When the active full run completes, perform Step 1: inspect jobs/logs/artifacts, record the run under one date/workflow folder, update frontier and all three banks, then commit.
- Do not choose search-24 before search-23 is fully recorded.

Do not treat heuristic failure as proof that 22 links are impossible.
