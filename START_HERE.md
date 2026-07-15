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
- `frontier/latest.*`: best checked mathematical and structural frontier.
- `frontier/active_run.json`: the only authoritative live stage record.
- `docs/smart-search-N-*.md`: binding Step-2 to Step-3 handoff.
- `docs/experiments/*`: exact local probes and bounded negative results.
- `runs/*`: completed or explicitly labelled partial-run evidence.
- candidate banks/originals: reusable checked and diagnostic candidates.

If this file and `frontier/active_run.json` disagree about the current stage, trust
`frontier/active_run.json` and repair this file during Step 4.

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

It passed both CI exact verifiers and two additional local exact checks. Search-24 and the Step-2
local experiments did not produce `63/64`.

## Latest completed Actions run

Workflow: `smart-search-24-defect-graft`  
Run: `29357369876`  
Archive: `runs/2026-07-14-smart-search-24-defect-graft-full/`

Strict result:

- precheck, smoke and full aggregate: success, `20/20` shards;
- exact ordered `63/64`: `0`;
- exact ordered `64/64`: `0`;
- compact exact unordered `64/64` line sets: `3,165`;
- connected compact exact `64/64` line sets: `2,349`;
- Hamiltonian supporting-line orders: `0`;
- finite `63/64` or `64/64` realizations: `0`.

Interpretation: unordered coverage is plentiful, but a connected or Hamiltonian graph of infinite
lines is not enough. The finite segment between its two chosen contacts must contain the intended
grid points.

## Step-2 structural breakthrough

Exact local report:
`docs/experiments/2026-07-15-search25-core-valley-analysis.md`.

Binding Step-3 handoff:
`docs/smart-search-25-core-valley-launch.md`.

The numeric frontier stayed `62/64`, but the natural one-rich-line neighborhood around the wall was
closed exactly:

- `43` exact ordered `62/64` states;
- `134` one-line-replacement edges, one component, diameter `8`;
- no outgoing one-rich-line replacement to `63/64`;
- all `43` states share the same `17` supporting lines;
- only `49` supporting lines occur in the whole component;
- targeted standalone hole lines and separator transversals also fail;
- breaking one common-core line yields `641` exact `61/64` valley states with `51` missing triples.

This is bounded exact computational evidence, not an impossibility proof.

What previous searches missed: they were too monotone. To change any of the common `17` lines, the
search must temporarily accept `59/64`–`61/64`. The next mutation must replace two lines atomically;
neither half-change may be pruned before the final ordered finite-contact trail is evaluated.

Permanent search-25 inputs:

- `data/search25_local_inputs.zip` — bundle with all `43` plateau states, common `17` lines, all `641` core-break valley states, and inner manifest;
- `data/search25_local_inputs.README.md` — bundle hash and materialization rules;
- `data/search25_local_experiment_manifest.json` — plain quick-read counts and inner hashes.

## Search history

- search-17: unordered 22-line `64/64` scaffolds, not trails.
- search-18: ordered reconstruction `44/64`.
- search-19: contact-state reconstruction `46/64`.
- search-20: rich-line preservation `58/64`, but eight explicit bridges.
- search-21: direct compression `61/64`, zero pure bridges.
- search-22: endpoint repair `62/64`, saturated in one frozen 18-line family.
- search-23: core transplant; `62/64`, two frozen-core lines changed, new defect orbit.
- search-24: defect-line graft; many unordered/connected `64/64` sets, no trail.
- search-25 selected: atomic paired core-valley search with exact finite contact spans.

## Current stage

There is no active run. Step 2 is complete and committed. `frontier/active_run.json` status is
`step2_handoff_ready_for_search25`.

Next action is Step 3: implement the binding C++20 engine, run shared preflight, strict `20`-shard
smoke, and launch full automatically only after smoke succeeds. Do not launch another search-24 copy.

## Binding search-25 rules

- name: `smart-search-25-core-valley`;
- full search loop: C++20, not Python;
- state includes ordered supporting lines, exact entry/exit contacts and finite coverage mask;
- primary operation replaces two lines atomically;
- allow the implicit half-move to fall to `59/64`, `60/64`, or `61/64`;
- do not count unordered `64/64`, connected graphs, or Hamiltonian support orders as trails;
- save every verified `63/64+`, every new `62/64` outside the closed 43-state component, and diverse
  core-broken valley states;
- two independent exact verifiers are mandatory.

## Performance and long-run safety

Search-24 Python averaged only `14.17` attempts/s/shard and was not memory-bound. Search-25 is
therefore binding C++20.

- normal full search time: `20400` seconds with timeout `359` minutes;
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
- permanent seeds must be committed before smoke;
- runtime materialization requires artifact ids, hashes and final persistence;
- the Step-2 implementation language and hypothesis are binding unless a benchmarked exception is
  recorded before launch;
- prepare a file manifest before publishing;
- publish one atomic tree commit when possible;
- trigger last and never duplicate without proving no equivalent run exists;
- Step 3 ends only after intended full jobs are visible;
- long-run preflight validates total job headroom.
