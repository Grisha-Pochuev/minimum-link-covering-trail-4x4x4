# START HERE — project memory

Last updated: 2026-06-29

This is the first file to read when starting work in a new ChatGPT web chat.

The assistant may not remember enough from previous project chats. Treat this repository as durable memory. Start here, then read the files listed below before analyzing a run or preparing a new one.

## What this project is

Repository: `Grisha-Pochuev/minimum-link-covering-trail-4x4x4`

Problem: find a shortest connected polygonal trail that covers all 64 points of the `4×4×4` grid `{0,1,2,3}^3`.

Working target: find a `22`-link trail covering `64/64` grid points, or understand the obstruction well enough to guide a proof or a sharper search.

Known practical status:

- `23` links: known construction exists and is used as a control check.
- `22` links: open search target.
- `21` links: currently too hard for serious search; use only as diagnostic pressure unless the frontier changes.

Important caution: a search result is not a proof. A partial candidate is evidence, not a theorem.

## First reading order for a new chat

Read these in this order:

1. `START_HERE.md` — this file.
2. `frontier/latest.md` and `frontier/latest.json` — current best frontier and latest useful run.
3. The relevant workflow in `.github/workflows/` — for a completed run, read the workflow that launched that run. Do not assume the newest workflow is automatically the right one for an old run.
4. `docs/*-plan.md` and `docs/web-chat-memento-prompts.md` — planning notes and web-chat operating prompts.
5. `candidates/bank.jsonl`, `candidates/bank-additions-*.jsonl`, and `candidates/originals/` — reusable seed memory and original candidate archive.
6. The latest relevant folder in `runs/`.
7. GitHub Actions artifacts of the latest useful runs.

Short invariant:

```text
START_HERE -> frontier -> relevant workflow -> plans -> bank/additions/originals -> runs/artifacts -> action
```

## Current frontier to remember

Latest useful completed full run recorded in `frontier/latest.md`:

```text
run id: 28327372242
workflow: smart-search-9-new-defect-repair
status: success
seconds per shard: 21000
threads per shard: 4
shards/jobs: 20
best result: 59/64
links: 22
missing count: 5
```

Best recorded candidate from this run:

```text
candidate id: mlct22-a495eb7a0c4f489d
source artifact: new-defect-22-shard-0
mode: transition_penalty22
saved at: runs/2026-06-28-smart-search-9-new-defect-repair-full/best_candidate.json
```

Missing points for the selected best candidate:

```text
(1, 2, 2)
(1, 3, 1)
(1, 3, 2)
(2, 0, 2)
(2, 0, 3)
```

Dominant recurring defect patterns from run `28327372242`:

```text
12/20: (1,2,2), (1,3,1), (1,3,2), (2,0,2), (2,0,3)
4/20:  (0,2,2), (2,1,3), (2,2,3), (3,1,0), (3,1,2)
3/20:  (0,0,2), (1,2,3), (2,0,1), (2,1,0), (3,1,1)
1/20:  (1,3,1), (2,1,2), (2,2,3), (3,1,0), (3,1,3)
```

Important observation: all 20 shard-best artifacts reached `59/64`, but none reached `60/64` or `64/64`. `smart-search-9-new-defect-repair` did not break the numeric frontier; it moved the obstruction into a new D-family centered on `(1,3,1)`, `(1,3,2)`, `(2,0,2)`, and `(2,0,3)`.

Saved run memory:

```text
frontier/latest.md
frontier/latest.json
runs/2026-06-28-smart-search-9-new-defect-repair-full/summary.md
runs/2026-06-28-smart-search-9-new-defect-repair-full/best_candidate.json
runs/2026-06-28-smart-search-9-new-defect-repair-full/local_preflight.md
candidates/bank-additions-run28327372242.jsonl
```

## Current prepared next workflow

Prepared workflow:

```text
smart-search-10-d-family-repair
.github/workflows/smart-search-10-d-family-repair.yml
```

Prepared support files:

```text
scripts/prepare_d_family_repair_engine.py
docs/smart-search-10-d-family-repair-plan.md
```

The workflow is manual-only with `workflow_dispatch`. It has no push trigger. A preparation commit should not silently burn GitHub Actions time.

Purpose:

```text
Repair the D-family wall exposed by run 28327372242, especially (1,3,1), (1,3,2), (2,0,2), and (2,0,3), while keeping the old A-family from run 28304497479 as a guardrail so the search does not merely rotate back to the previous obstruction.
```

Safe smoke-test parameters:

```text
workflow: smart-search-10-d-family-repair
seconds: 180
threads: 4
seed: 20260701
prior_run_id: 28327372242
orbit_bridge_run_id: 28304497479
previous_core5_run_id: 28292425390
old_59_run_id: 28275850889
secondary_run_id: 28275666411
base_repair_run_id: 28200925016
min_covered_to_save: 56
jobs/shards: 20
max-parallel: 20
```

Full serious-run parameters after the smoke-test succeeds:

```text
workflow: smart-search-10-d-family-repair
seconds: 21000
threads: 4
seed: 20260701
prior_run_id: 28327372242
orbit_bridge_run_id: 28304497479
previous_core5_run_id: 28292425390
old_59_run_id: 28275850889
secondary_run_id: 28275666411
base_repair_run_id: 28200925016
min_covered_to_save: 56
jobs/shards: 20
max-parallel: 20
expected wall time: about 5h50m per shard
```

## Candidate-saving rules

There are three concrete candidate-memory locations. They have two roles: compact search fuel and scientific original archive. Do not mix them up.

### 1. Main compact working bank

```text
candidates/bank.jsonl
```

This is the main small reusable search memory. It stores the best known eligible trail candidates from previous runs as symmetry-deduplicated representatives. Cube symmetries, coordinate permutations/reflections, trail reversal, and exact duplicates should be collapsed here.

Use it as seed fuel for future workflows. Do not treat it as a complete historical archive.

### 2. Run-level compact additions

```text
candidates/bank-additions-*.jsonl
```

These files are append records from specific completed runs. They store compact eligible candidates from that run, also symmetry-deduplicated, before or alongside merging into `candidates/bank.jsonl`.

For run `28327372242`, the dominant compact addition is saved in:

```text
candidates/bank-additions-run28327372242.jsonl
```

### 3. Original trail archive

```text
candidates/originals/
candidates/originals/README.md
candidates/originals/index.jsonl
```

This is the permanent scientific archive of original, non-deduplicated lomanaya/trail candidates from completed runs. It is for analysis of real diversity, repeated patterns, mode behavior, and possible structural obstructions.

Normal eligibility threshold for both compact memory and original archive unless the workflow says otherwise:

```text
covered_count >= 56
links <= 22
```

Post-run saving rule:

```text
1. Save champion candidate(s) and update frontier/latest.* if needed.
2. Save new compact unique eligible candidates into bank/additions.
3. Save all original eligible shard-best candidates into candidates/originals/ when the full shard JSONs are available.
4. Update candidates/originals/index.jsonl with a summary line for the run when originals are archived.
5. Update START_HERE.md if the frontier, prepared workflow, or next step changed.
```

## Flexible post-run reasoning loop

After a completed run, do not merely fill a template. Use `START_HERE.md` as memory, then think from the evidence of this particular run.

A good post-run analysis should ask:

- Did the numeric frontier improve: `56 -> 57 -> 58 -> 59 -> 60 -> 64`, or did it stay the same?
- If the best coverage stayed the same, did the run still discover new defect sets, new modes, or new geometric families?
- Are the new missing points the same as before, a symmetry of old ones, or genuinely different?
- Did many shards converge to one pattern, or did they spread across several patterns?
- Did the compact bank gain genuinely useful new representatives, or only near-duplicates?
- Did any mode underperform so badly that it should be reduced or removed next time?
- Did any mode produce a new kind of near-miss that deserves a specialized repair workflow?
- Are we learning a possible obstruction/lemma, not just collecting candidates?
- Was the workflow itself trustworthy: no artifact failures, no skipped aggregation, no accidental old commit, no missing seed layer?
