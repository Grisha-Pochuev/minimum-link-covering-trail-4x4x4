# START HERE — compact agent memory

Last updated: 2026-07-08

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

Latest recorded completed run:

- run id: `28903545221`
- run URL: https://github.com/Grisha-Pochuev/minimum-link-covering-trail-4x4x4/actions/runs/28903545221
- workflow: `smart-search-19-contact-state-dp`
- status: `success`
- head commit: `ed5c56c90bca2044d55cbab6f48c0fb8c3b4071f`
- result type: contact-state DP ordered-chain reconstruction diagnostic from search-17 cover64 scaffolds; not an ordered-trail frontier improvement
- actual parameters from best row: `seconds=21000`, `workers=4`, `seed=20260719`, `beam_width=2048`, `state_cap=200000`, `candidate_scaffolds=4`, `max_mutations=1`, `branch_limit=6`, `start_limit=22`, `candidate_lines=3000`
- caution: this used full-duration seconds but smoke/default DP width, not the intended full-width profile `beam_width=8192`, `state_cap=2000000`, `max_mutations=2`

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
- best mode: `one_two_line_mutation`, shard `7`;
- unique compact diagnostic ordered candidates saved: `17`;
- ordinary ordered-trail additions saved: `0`;
- line-set scaffold additions saved: `0`;
- diagnostic bank saved: `candidates/diagnostic-order-from-cover64-run28875314204.jsonl`;
- originals index saved: `candidates/originals/run28875314204-order-from-cover64-index.jsonl`.

Key lesson from run `28903545221`:

- search-19 fixed the red technical launch and completed successfully;
- all 20 contact-state shard jobs and the aggregate job succeeded;
- aggregate rows: `40`;
- unique ordered candidates in summary: `3`;
- best diagnostic ordered-chain reconstruction improved search-18 only slightly, `44/64 -> 46/64`;
- best candidate: `mlct22-contactdp-2714c28ba62b5c26`, mode `official60_aware`, shard `14`, artifact `contact-state-dp-22-shard-14`;
- best links: `22`, covered_count: `46/64`, missing_count: `18`;
- ordinary ordered-trail additions saved: `0`;
- line-set scaffold additions saved: `0`;
- diagnostic rows saved: `3`;
- originals index rows saved: `3`;
- dominant failure is not the old four-hole `60/64` defect family. It is rich-line clipping during contact-state reconstruction: the best candidate preserved only `8` rich lines and clipped `12`, losing `17` grid points over pieces.

Counting caution: search-17 artifacts are `cover64-stitch-line-set-v1` scaffolds. They must not be merged into the normal ordered-trail candidate bank until a separate reconstruction/checker turns them into actual consecutive 22-link polygonal trails. Search-18 and search-19 outputs are checked ordered-chain diagnostics, but they are far below the `60/64` ordered-trail frontier and must stay in diagnostic banks, not ordinary candidate additions.

Do not rerun `smart-search-17-cover64-stitch-graph`, `smart-search-18-order-from-cover64-stitch`, or `smart-search-19-contact-state-dp` unchanged as the next serious step. Search-17 found the scaffold breakthrough; search-18 showed abstract stitchability is too weak; search-19 showed contact-state ordering still clips too many rich lines.

## 4. Standard four-prompt workflow

Use the user's four-step rhythm:

1. result-taking prompt: read `START_HERE.md` once at the start of a new chat, record completed main/full GitHub run results, artifacts, candidates, frontier, and memory;
2. hypothesis prompt: think creatively, choose the next non-repeating hypothesis, and do any small local checks needed to make the idea launchable;
3. launch-preparation prompt: **technical implementation only**. Take the already chosen hypothesis from prompt 2 and prepare runnable GitHub launch files so the user can press Run. This may include writing a new engine/generator/checker/summary builder if the chosen hypothesis requires it. Do not invent a new hypothesis, do not re-test the idea, and do not open a different research branch unless the requested launch is technically impossible;
4. wrap-up prompt: review the whole chat, identify confusion/time loss, and update memory files if needed.

Smoke-test is only a technical green-light before the long run. If the user sees a green check and launches the 5h+ full run, the next result-taking chat records the full run, not the smoke-test. Inspect smoke separately only if it failed, looked suspicious, or the user explicitly asks.

## 5. Latest saved run archive

Search-19 result archive:

```text
runs/2026-07-08-smart-search-19-contact-state-dp-full/summary.md
runs/2026-07-08-smart-search-19-contact-state-dp-full/best_contact_state_candidate.json
runs/2026-07-08-smart-search-19-contact-state-dp-full/mode_breakdown.json
runs/2026-07-08-smart-search-19-contact-state-dp-full/contact_state_dp_run_summary_compact.json
candidates/diagnostic-contact-state-dp-run28903545221.jsonl
candidates/originals/run28903545221-contact-state-dp-index.jsonl
```

## 6. Current next step

The next chat should normally be prompt 2: choose a new non-repeating hypothesis.

Best next direction from the saved evidence:

```text
smart-search-20-full-line-preserving-contact-bridge
```

Goal: attack the exact failure exposed by search-19. Preserve complete 3/4-point rich line pieces as much as possible and pay explicit bridge/contact costs between whole pieces, instead of letting contact-state reconstruction choose short contact pieces that destroy coverage.

One technical caveat before abandoning search-19 entirely: run `28903545221` used full seconds but smoke/default DP-width parameters. If the user wants to close that loose end, run the intended true full-width profile once (`beam_width=8192`, `state_cap=2000000`, `max_mutations=2`). But as a research direction, do not rerun search-19 unchanged.

Expected useful next result means either a checked ordered 22-link trail candidate improving the `60/64` frontier, or a sharper obstruction explaining which rich full-line pieces cannot be preserved together in a continuous 22-link trail.
