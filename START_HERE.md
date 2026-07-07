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

## 5. Current prepared launch

A launch package now exists for the chosen post-search-18 hypothesis:

```text
smart-search-19-contact-state-dp
```

Files:

- workflow: `.github/workflows/smart-search-19-contact-state-dp.yml`
- engine: `scripts/contact_state_dp_from_scaffolds.py`
- summary builder: `scripts/build_contact_state_dp_summary.py`
- checker: `scripts/check_ordered_trail_scaled.py`
- plan: `docs/smart-search-19-contact-state-dp-plan.md`

Hypothesis implemented: stronger contact-state reconstruction from search-17 scaffolds. It tracks concrete contact points, actual covered grid masks, and per-line contact loss (`full scaffold line mask -> chosen ordered piece mask -> lost grid points`) instead of relying only on the abstract stitch graph.

The engine is currently Python. That is acceptable for this launch as a hypothesis/prototype run. If search-19 shows a real signal, the heavy contact-state DP/beam loop should be ported to C++ while Python remains the workflow/JSON/summary wrapper.

## 6. Current next step

There was an initial red run:

- run id: `28902841543`
- workflow: `smart-search-19-contact-state-dp`
- status: red because the checker step had a technical heredoc/shell bug, not because the engine failed
- observation: shard engine steps ran, but `Check ordered-chain JSON geometry` failed
- fix commit: `ed5c56c90bca2044d55cbab6f48c0fb8c3b4071f` (`Fix contact-state checker heredoc`)

Do **not** use `Re-run failed jobs` on run `28902841543`, because that run used the older broken commit. The next action is a fresh manual `Run workflow` on branch `main` for `smart-search-19-contact-state-dp`.

Smoke-test inputs:

```text
seconds: 180
workers: 4
seed: 20260719
beam_width: 2048
state_cap: 200000
candidate_scaffolds: 4
max_mutations: 1
box_min: -1
box_max: 4
min_piece_cover: 1
save_min_covered: 38
branch_limit: 6
start_limit: 22
candidate_lines: 3000
```

Full-run inputs:

```text
seconds: 21000
workers: 4
seed: 20260719
beam_width: 8192
state_cap: 2000000
candidate_scaffolds: 4
max_mutations: 2
box_min: -1
box_max: 4
min_piece_cover: 1
save_min_covered: 44
branch_limit: 6
start_limit: 22
candidate_lines: 3000
```

Expected useful result means either a checked ordered 22-link trail candidate improving the `60/64` frontier, or a precise obstruction explaining why the search-17 `22/22` line-set stitch graph does not translate into a high-coverage polygonal chain.

## 7. Wrap-up caution from latest chat

What worked well:

- The chat followed the four-step rhythm: record run, choose hypothesis, prepare launch, then clean up memory.
- The search-19 launch package was created with real workflow, engine, checker, summary builder, plan doc, and exact inputs.
- The red run was diagnosed correctly as a technical workflow/checker failure, not as a mathematical failure.

Potential confusion for the next chat:

- `64/64` in search-17 still means unordered scaffold coverage, not solved 22-link trail.
- `44/64` in search-18 is a real ordered-chain reconstruction diagnostic, but it is not useful as a frontier candidate.
- Run `28902841543` should not be recorded as a completed full result unless the user explicitly asks to inspect its artifacts; it was a failed technical launch attempt.
- The next step is not “run search-18 longer” and not “rerun failed jobs”; it is a fresh `smart-search-19-contact-state-dp` run from fixed `main`.
