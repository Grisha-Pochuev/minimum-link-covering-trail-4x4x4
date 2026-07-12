# START HERE — compact agent memory

Last updated: 2026-07-12

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
- `runs/*`: completed-run evidence.

## Current frontier

Best candidate:

- id: `mlct22-er-7671ee46bd711a25`
- file: `runs/2026-07-12-smart-search-22-endpoint-repair-full/best_candidate.json`
- coverage: `62/64`
- links: `22`
- missing: `(0,2,1)`, `(3,3,1)`
- source run: `29181546758`
- status: `verified_partial_candidate`

It passed both exact rational verifiers.

## Full search-22 result

Run `29181546758`, `smart-search-22-endpoint-repair`, full profile:

- success, precheck success, aggregate success;
- shards: `20/20`;
- compact candidates: `2385`;
- `62/64`: `1053`;
- `61/64`: `777`;
- `60/64`: `555`;
- `63/64`: `0`;
- `64/64`: `0`;
- raw originals: `80`.

Search-22 made 62 reproducible but did not improve beyond the smoke result.

## Step-2 structural result

The `1053` exact `62/64` curves are not independent skeletons.

- every curve contains the same `18` supporting lines out of `22`;
- this frozen core covers `58/64`;
- only four link positions vary in a representative ordering;
- the common core leaves six points;
- every 62-curve covers four of those six and leaves two;
- there are exactly seven two-hole families, all in plane `z=1`.

Large exact shallow-neighborhood tests found no `63/64`: one-vertex replacement, short-window repair, crossover, symmetry/reversal crossover, 2-opt, 3-opt and simple defect-line insertion/reordering.

Structurally different donors exist below the frontier:

- one `61/64` candidate with frozen-core overlap `16`;
- four `60/64` candidates with overlap only `2`.

Full evidence:

`docs/experiments/2026-07-12-search22-frozen-core-analysis.md`

## Search history

- search-17: unordered 22-line `64/64` scaffolds, not trails.
- search-18: ordered reconstruction `44/64`.
- search-19: contact-state reconstruction `46/64`.
- search-20: rich-line preservation `58/64`, but eight explicit bridges.
- search-21: direct compression `61/64`, zero pure bridges.
- search-22: endpoint repair `62/64`, saturated in one frozen 18-line family.

The unordered `64/64` scaffold from run `28825060197` is not an ordered trail and must remain in its separate bank.

## Selected search-23

Step 2 is complete.

Selected workflow:

`smart-search-23-core-transplant`

Binding specification:

`docs/smart-search-23-core-transplant-launch.md`

Primary hypothesis: a `63/64` or `64/64` trail requires breaking at least one, preferably two, frozen-core lines and rebuilding a connected or paired `4–8`-link neighborhood using blocks from structurally different `60/64–61/64` donors.

Another `62/64` curve retaining all 18 frozen lines and an old defect pair is not meaningful progress.

## Four-step cycle

1. Record a completed run.
2. Select and test one non-repeating hypothesis; save a precise launch document.
3. Implement one workflow, pass local checks, smoke aggregate, then full.
4. Review process and memory.

Normal full profile: 20 shards, max-parallel 20, four workers per shard, 21000 seconds. Exactly one workflow per search number. Use normal readable modules. Never launch a duplicate.

## Current next action

Run Step 3 from `docs/smart-search-23-core-transplant-launch.md`:

1. persist the expiring search-22 seed population in repository text parts;
2. refactor the old `*.pyfrag` source or write normal search-23 C++20/Python modules;
3. pass the local dry-run gate;
4. run one smoke and wait for the complete aggregate;
5. only then launch one full search-23 run.

Do not rerun search-22 unchanged. Do not treat heuristic failure as proof.
