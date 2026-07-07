# START HERE — compact agent memory

Last updated: 2026-07-07

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

Latest recorded completed full run:

- run id: `28875314204`
- run URL: https://github.com/Grisha-Pochuev/minimum-link-covering-trail-4x4x4/actions/runs/28875314204
- workflow: `smart-search-18-order-from-cover64-stitch`
- status: `success`
- seconds: `21000` per shard
- threads/workers: `4`
- shards/jobs: `20`
- result type: checked ordered-chain reconstruction diagnostics from search-17 cover64 scaffolds; not an ordered-trail improvement

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

Counting caution: search-17 artifacts are `cover64-stitch-line-set-v1` scaffolds. They must not be merged into the normal ordered-trail candidate bank until a separate reconstruction/checker turns them into actual consecutive 22-link polygonal trails. Search-18 outputs are checked ordered-chain diagnostics, but they are far below the `60/64` ordered-trail frontier and also must not be treated as candidate-bank improvements.

Do not rerun `smart-search-17-cover64-stitch-graph` with the same seed or `smart-search-18-order-from-cover64-stitch` unchanged as the next serious step. Search-17 found the scaffold breakthrough; search-18 showed the current reconstruction model is too weak. The bottleneck moved to stronger contact-state reconstruction.

## 4. Standard four-prompt workflow

Use the user's four-step rhythm:

1. result-taking prompt: read `START_HERE.md` once at the start of a new chat, record completed main/full GitHub run results, artifacts, candidates, frontier, and memory;
2. hypothesis prompt: think creatively, choose the next non-repeating hypothesis, and do any small local checks needed to make the idea launchable;
3. launch-preparation prompt: **technical implementation only**. Take the already chosen hypothesis from prompt 2 and prepare runnable GitHub launch files so the user can press Run. This may include writing a new engine/generator/checker/summary builder if the chosen hypothesis requires it. Do not invent a new hypothesis, do not re-test the idea, and do not open a different research branch unless the requested launch is technically impossible;
4. wrap-up prompt: review the whole chat, identify confusion/time loss, and update memory files if needed.

Smoke-test is only a technical green-light before the long run. If the user sees a green check and launches the 5h+ full run, the next result-taking chat records the full run, not the smoke-test. Inspect smoke separately only if it failed, looked suspicious, or the user explicitly asks.

## 5. Current next step

There is no prepared next launch package yet after recording search-18.

Next step should be prompt 2: choose a new hypothesis based on the search-18 failure. The main diagnostic question is why unordered `64/64` line-set coverage collapsed to only `44/64` actual ordered-chain coverage.

Likely direction for the next non-repeating launch package:

```text
stronger contact-state reconstruction from search-17 scaffolds
```

Meaning:

- do not only find a path in the line-set graph;
- track concrete contact vertices/intersections;
- track actual covered grid-point mask while ordering;
- use dynamic programming or beam search over `(line, contact point, covered mask)` states;
- compare the ordered chain against the source scaffold to identify exactly which scaffold lines lose their covered points during ordering;
- save failed-but-informative reconstructions separately from ordinary ordered-trail candidates.

Expected useful result means either a checked ordered 22-link trail candidate improving the `60/64` frontier, or a precise obstruction explaining why the search-17 `22/22` line-set stitch graph does not translate into a high-coverage polygonal chain.

## 6. Wrap-up caution from latest result-taking

What worked well:

- The run was recorded index-first: START_HERE, frontier, runbook, exact workflow, then summary artifact.
- Old runs/logs/candidate banks were not blindly opened because the summary artifact was complete and all jobs succeeded.
- Candidate banks were kept separate: no weak ordered reconstruction was merged into the ordinary ordered-trail bank.

Potential confusion for the next chat:

- `64/64` in search-17 still means unordered scaffold coverage, not solved 22-link trail.
- `44/64` in search-18 is a real ordered-chain reconstruction diagnostic, but it is not useful as a frontier candidate.
- The next step is not “run search-18 longer”; it is to design a stronger reconstruction model.
