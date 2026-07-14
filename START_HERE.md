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

- `frontier/latest.*`: best checked mathematical frontier, including a verified candidate from an incomplete run when clearly labelled.
- `frontier/active_run.json`: active run, retry or selected next search.
- `docs/smart-search-N-*.md`: binding Step-2 to Step-3 handoff.
- `docs/retrospectives/*`: process lessons; not mathematical frontier.
- `runs/*`: completed or explicitly labelled partial-run evidence.

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

## Search-23 first-attempt result

Run `29249275103`, workflow `smart-search-23-core-transplant`:

- precheck succeeded;
- first attempt produced `19/20` shard artifacts;
- `core-transplant (11)` produced no artifact;
- GitHub is rerunning shard 11 under the same run id;
- strict full aggregate is therefore not final yet;
- partial archive: `runs/2026-07-13-smart-search-23-core-transplant-full/`.

Checked partial statistics from 19 shards:

- compact exact `62/64`: `1115`;
- exact `62/64` with frozen-core overlap `<=16`: `40`;
- compact diagnostic core-escape states: `1600`;
- raw worker-best originals: `74`;
- `63/64`: `0`;
- `64/64`: `0`;
- one new two-hole orbit;
- `82,917,351,393` attempts.

Do not start search-24 before the shard-11 retry and strict 20/20 aggregate are recorded.

## Why `core-transplant (11)` failed

The exact old platform log became unavailable after the retry began, so do not claim a fully proven final message. The evidence strongly supports a job-time/runner interruption, not OOM:

- sibling shards used at most `0.3404 GiB` RAM;
- successful search executables ran almost exactly `21000` seconds;
- `timeout-minutes=359` left only `540` seconds for checkout, setup, seed preparation, compilation, final sorting, two verifiers and artifact upload;
- shard 11 left no artifact at all.

Permanent prevention rule:

- normal full search time is now `20400` seconds when job timeout is `359` minutes;
- every new full workflow must run `scripts/check_long_run_budget.py` in preflight;
- require at least `900` seconds of job headroom;
- scientific aggregate is final only with every required shard;
- an `if: always()` failure report may archive missing-shard evidence, but must be labelled incomplete;
- rerunning an old run uses its historical commit and does not receive later fixes.

## Search history

- search-17: unordered 22-line `64/64` scaffolds, not trails.
- search-18: ordered reconstruction `44/64`.
- search-19: contact-state reconstruction `46/64`.
- search-20: rich-line preservation `58/64`, but eight explicit bridges.
- search-21: direct compression `61/64`, zero pure bridges.
- search-22: endpoint repair `62/64`, saturated in one frozen 18-line family.
- search-23: core transplant; first attempt already found exact `62/64` with overlap `16`, but shard 11 is being recovered.

The unordered `64/64` scaffold from run `28825060197` is not an ordered trail and must remain in its separate bank.

## Four-step cycle

1. Record a completed run, or explicitly archive an incomplete attempt without pretending it is complete.
2. Select and test one non-repeating hypothesis; save a precise launch document.
3. Implement and automatically execute one complete chain: local preflight → smoke aggregate → full launch.
4. Review process and memory.

## Mandatory single-prompt Step-3 rule

A Step-3 request authorizes the complete chain. Normal future architecture:

```text
precheck
  -> smoke[20]
  -> smoke-aggregate
  -> full[20] only after smoke success
  -> full-aggregate
```

Manual smoke/full profiles may remain for recovery only.

Additional permanent rules:

- local validation and GitHub precheck call the same versioned preflight with the same seeds;
- normalize seed schemas before exact checkers;
- commit permanent seeds before smoke; scientific workflows do not commit source/seeds during execution;
- publish coherent source in one atomic tree commit or the smallest practical number;
- never repeat a trigger without proving no equivalent run exists;
- Step 3 ends only after the intended full jobs are visible;
- long-run preflight must validate time headroom, not only search seconds.

## Current next action

Read `frontier/active_run.json`.

- Do not launch another search-23 copy.
- Do not start search-24.
- After shard 11 retry completes, inspect its artifact and logs, run the strict 20/20 aggregate, merge ordinary/diagnostic/originals banks, finalize the run archive, and mark search-23 fully recorded.

Do not treat heuristic failure or a technical missing shard as proof that 22 links are impossible.
