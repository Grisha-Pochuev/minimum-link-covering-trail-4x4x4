# START HERE — compact agent memory

Last updated: 2026-07-09

This file is the first thing to read in a new ChatGPT web chat. It is the boot memory, not the full diary. Read it once at the beginning of the working chat, normally in prompt 1. Do not reopen it in prompts 2-4 unless the user says this is a new chat, memory was lost, or critical context is missing. Detailed history belongs in `frontier/latest.*`, `runs/*/summary.md`, plans, runbooks, and candidate banks.

## 1. Project

Repository: `Grisha-Pochuev/minimum-link-covering-trail-4x4x4`

Problem: find a shortest connected polygonal trail covering all 64 points of the `4×4×4` grid `{0,1,2,3}^3`.

Current target: a `22`-link trail covering `64/64`, or enough obstruction evidence to guide a proof/search.

Known practical status:

- `23` links: known construction; used as control.
- `22` links: open target.
- `21` links: too hard for serious search now; use only as diagnostic pressure.

Important: heuristic search results are evidence, not proof.

## 2. First reading order

At the beginning of a new working chat, start from:

1. `START_HERE.md`
2. `frontier/latest.md`
3. `frontier/latest.json`
4. `docs/web-chat-runbook-prompts.md`
5. exact workflow or prepared workflow
6. matching plan doc
7. candidate bank/additions/originals
8. latest relevant `runs/` folder
9. GitHub Actions artifacts when analyzing a completed run

After this boot read, avoid reopening `START_HERE.md` during prompts 2-4 in the same chat. Use `frontier/latest.*` and run summaries as the index instead of blindly scanning every old run.

## 3. Current recorded frontier

Latest recorded completed full run is now search-20:

- run id: `28973760924`
- run URL: https://github.com/Grisha-Pochuev/minimum-link-covering-trail-4x4x4/actions/runs/28973760924
- workflow: `smart-search-20-line-bridge`
- status: `success`
- head commit: `772596df3d9fd796d2a5bf5ee0ea48697ca17031`
- profile: `full`
- actual parameters: `seconds=21000`, `workers=4`, `seed=20260720`, `beam_width=12000`, `state_cap=2000000`, `candidate_scaffolds=6`, `max_mutations=1`, `candidate_lines=6000`, `start_limit=44`, `line_branch_limit=24`, `bridge_branch_limit=16`, `min_full_lines=14`, `max_full_lines=18`, `max_bridge_links=8`, `save_min_covered=54`
- result type: full-line-preserving bridge ordered-chain diagnostic from search-17 cover64 scaffolds; below the ordered-trail frontier, not a proof and not an ordered-trail improvement

Best recorded GitHub ordered-trail candidate remains:

- candidate id: `mlct22-3cf45a2e21fe611c`
- source: run `28674416173`, same geometry as run `28618565146`
- file: `runs/2026-07-03-smart-search-16-defect-relay-60-full/best_candidate.json`
- covered_count: `60/64`
- links: `22`
- missing: `(0,0,1)`, `(0,2,3)`, `(0,3,1)`, `(2,1,1)`

Best recorded cover64 stitch scaffold from run `28825060197` remains:

- candidate id: `mlct22-lineset-9772981a21b2a88a`
- file: `runs/2026-07-07-smart-search-17-cover64-stitch-graph-full/best_line_set.json`
- unordered line coverage: `64/64`
- line count: `22`
- stitch graph: components=`1`, max component=`22/22`, path lower bound=`22/22`, edges=`23`
- mode: `old_wall_line_injection`
- source artifact: `cover64-stitch-22-shard-12`
- status: `line_set_seed_not_a_trail`

Key lesson from run `28825060197`:

- ordered-trail numeric frontier stayed `60/64`;
- no checked `61/64+` ordered-trail candidate was produced;
- scaffold frontier improved: many unordered 22-line sets cover all `64/64`;
- saved compact line-set scaffold representatives: `20`;
- compact scaffold representatives with stitch path `22/22`: `4`;
- ordinary ordered-trail additions saved: `0`;
- there is no missing-point defect family at scaffold level; all saved line-set representatives cover `64/64`.

Key lesson from run `28875314204`:

- search-18 tried to convert search-17 `64/64` scaffolds into real ordered 22-link chains;
- best ordered-chain reconstruction was only `44/64`, candidate `mlct22-order-5c31614d2aeaa2aa`;
- ordinary ordered-trail additions saved: `0`;
- line-set scaffold additions saved: `0`;
- diagnostic bank saved: `candidates/diagnostic-order-from-cover64-run28875314204.jsonl`.

Key lesson from run `28903545221`:

- search-19 fixed the red technical launch and completed successfully;
- best diagnostic ordered-chain reconstruction improved search-18 only slightly, `44/64 -> 46/64`;
- best candidate: `mlct22-contactdp-2714c28ba62b5c26`, mode `official60_aware`, shard `14`;
- ordinary ordered-trail additions saved: `0`;
- diagnostic rows saved: `3`;
- dominant failure was rich-line clipping: best candidate preserved only `8` rich lines and clipped `12`, losing `17` grid points over pieces.

Key lesson from run `28973760924`:

- search-20 completed the `smart-search-20-line-bridge` full run successfully;
- all prechecks, 20 line-bridge shard jobs, and aggregate job succeeded;
- aggregate rows: `40`;
- shard-best outputs: `20`;
- unique compact ordered candidates in summary: `6`;
- best line-bridge ordered-chain diagnostic improved search-19 strongly, `46/64 -> 58/64`;
- best candidate: `mlct22-flbridge-8da0e01c34bb9c88`, mode `one_line_replacement`, shard `16`, artifact `smart-search-20-line-bridge-22-shard-16`;
- best links: `22`, covered_count: `58/64`, missing_count: `6`;
- best missing: `(0,2,0)`, `(0,2,2)`, `(2,1,0)`, `(2,1,2)`, `(2,3,0)`, `(3,2,0)`;
- best preserved rich lines: `14`, full-line links: `14`, bridge links: `8`;
- official60 old-missing hits: `4`, meaning the four holes of the standing `60/64` candidate were all hit;
- ordinary ordered-trail additions saved: `0`;
- line-set scaffold additions saved: `0`;
- diagnostic line-bridge rows saved: `6`;
- originals index rows saved: `6`.

Search-20 interpretation: full-line preservation is much better than search-19 contact-state clipping, but spending 8 explicit bridge links is still too expensive. The run repaired the old four-hole wall but created a new six-hole bridge-defect family. It is diagnostic progress, not an ordered-frontier improvement.

Counting caution: search-17 artifacts are `cover64-stitch-line-set-v1` scaffolds. They must not be merged into the normal ordered-trail candidate bank until a separate reconstruction/checker turns them into actual consecutive 22-link polygonal trails. Search-18, search-19, and search-20 outputs are checked ordered-chain diagnostics, but search-20 best is still below the `60/64` ordered-trail frontier and must stay in diagnostic banks, not ordinary candidate additions.

Do not rerun `smart-search-17-cover64-stitch-graph`, `smart-search-18-order-from-cover64-stitch`, `smart-search-19-contact-state-dp`, or `smart-search-20-line-bridge` unchanged as the next serious step.

## 4. Standard four-prompt workflow

Use the user's four-step rhythm:

1. result-taking prompt: read `START_HERE.md` once at the start of a new chat, record completed main/full GitHub run results, artifacts, candidates, frontier, and memory;
2. hypothesis prompt: think creatively, choose the next non-repeating hypothesis, and do any small local checks needed to make the idea launchable;
3. launch-preparation prompt: **technical implementation only**. Take the already chosen hypothesis from prompt 2 and prepare runnable GitHub launch files so the user can press Run. This may include writing a new engine/generator/checker/summary builder if the chosen hypothesis requires it. Do not invent a new hypothesis, do not re-test the idea, and do not open a different research branch unless the requested launch is technically impossible;
4. wrap-up prompt: review the whole chat, identify confusion/time loss, and update memory files if needed.

Naming rule for serious numbered searches: keep the workflow/run family as `smart-search-N-short-description`, for example `smart-search-11-d2-bridge-repair` or `smart-search-20-line-bridge`. The suffix should be short, ideally one or two descriptive words, but do not drop the `smart-search-N` prefix.

Prompt 3 caution from 2026-07-08: do not spend time repeatedly trying to open a PR before there are commits. First write the launch files, then open/merge the PR if needed. If the user asks to run automatically but the connector has no workflow_dispatch action, say so honestly and give exact manual Run inputs.

Workflow rename/delete safety rule: before deleting, renaming, or replacing any `.github/workflows/*.yml`, first check whether a long manual GitHub Actions run is queued or running under that workflow. Do not remove the old workflow file while a 5h+ run may be active.

Manual-run profile safety rule: for any serious GitHub Actions search that has smoke/full parameter sets, prefer a single `profile` input with choices `smoke`, `full`, and optionally `custom`. If `profile=full` is selected, GitHub's form may still show all custom numeric boxes as blank; that is expected. The workflow must resolve the full numeric set internally and write an `effective_profile*.json` artifact if possible.

Smoke-test is only a technical green-light before the long run. If the user sees a green check and launches the 5h+ full run, the next result-taking chat records the full run, not the smoke-test. Inspect smoke separately only if it failed, looked suspicious, or the user explicitly asks.

## 5. Latest saved run archive

Search-20 result archive:

```text
runs/2026-07-09-smart-search-20-line-bridge-full/summary.md
runs/2026-07-09-smart-search-20-line-bridge-full/best_line_bridge_candidate.json
runs/2026-07-09-smart-search-20-line-bridge-full/line_bridge_run_summary_compact.json
runs/2026-07-09-smart-search-20-line-bridge-full/mode_breakdown.json
candidates/diagnostic-line-bridge-run28973760924.jsonl
candidates/originals/run28973760924-line-bridge-index.jsonl
```

## 6. Current next step

The `smart-search-20-line-bridge` hypothesis has been tried and recorded. The next chat should use Prompt 2, not Prompt 1 or Prompt 3.

Next non-repeating research direction should use the search-20 lesson:

- preserving rich full lines helped a lot compared with contact-state clipping;
- hitting all four old `60/64` missing points is possible;
- but 8 explicit bridge links still leave a new six-hole bridge-defect family;
- next hypothesis should reduce bridge cost, change the scaffold ordering principle, or construct endpoint-compatible rich scaffolds instead of repeating the same line-bridge workflow.
