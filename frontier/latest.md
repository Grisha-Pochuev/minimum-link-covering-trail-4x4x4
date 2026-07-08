# Current search frontier

Status: launch package `smart-search-20-line-bridge` is prepared on `main`. The normal ordered-trail frontier remains `60/64`; the scaffold frontier from search-17 remains unordered `64/64` with stitch path lower bound `22/22`. Search-19 improved the ordered-reconstruction diagnostic ceiling from `44/64` to `46/64`, but did not improve the actual ordered-trail frontier.

Latest recorded completed full run:

- Repository: `Grisha-Pochuev/minimum-link-covering-trail-4x4x4`
- Final run id: `28903545221`
- Run URL: https://github.com/Grisha-Pochuev/minimum-link-covering-trail-4x4x4/actions/runs/28903545221
- Workflow: `smart-search-19-contact-state-dp`
- Commit SHA of the run: `ed5c56c90bca2044d55cbab6f48c0fb8c3b4071f`
- Status: `success`
- Duration: long run, `21000` seconds per shard
- Workers per shard: `4`
- Shards/jobs: `20`
- Seed: `20260719`
- Result type: contact-state DP ordered-chain reconstruction diagnostics from search-17 cover64 scaffolds; not a proof and not an ordered-trail improvement
- Important parameter caution: actual saved best row has `beam_width=2048`, `state_cap=200000`, `max_mutations=1`; this is full-duration but smoke/default DP width, not the intended full-width profile `8192/2000000/2`.
- Artifacts: `contact-state-dp-run-summary`, `contact-state-dp-22-shard-*`

## Best recorded GitHub Actions ordered-trail result

The best checked ordered-trail candidate remains unchanged from run `28674416173`:

- candidate id: `mlct22-3cf45a2e21fe611c`
- covered_count: `60 / 64`
- coverage percent: `93.75%`
- links: `22`
- latest source mode: `window3_relay_from_official60`
- latest source artifact: `defect-relay-22-shard-7`
- source shard: `7`
- status: `partial_candidate`
- missing count: `4`
- missing: `(0,0,1)`, `(0,2,3)`, `(0,3,1)`, `(2,1,1)`

The ordered-trail candidate is still partial. It has exactly 22 links and covers 60 of the 64 grid points. This is not a complete covering trail and not a proof.

## Best recorded cover64 stitch scaffold

Best search-17 scaffold remains:

- candidate id: `mlct22-lineset-9772981a21b2a88a`
- covered_count: `64 / 64`
- line_count: `22`
- stitch graph: components=`1`, max_component=`22/22`, path_lower_bound=`22/22`, edges=`23`
- mode: `old_wall_line_injection`
- source artifact: `cover64-stitch-22-shard-12`
- source shard: `12`
- source file: `runs/2026-07-07-smart-search-17-cover64-stitch-graph-full/best_line_set.json`
- status: `line_set_seed_not_a_trail`

Important caveat: this is an unordered 22-line scaffold. A line-set graph path is not yet the same as a valid ordered polygonal trail. Do not merge this into the ordinary ordered-trail candidate bank until a reconstruction/checker produces actual consecutive trail vertices.

## Latest recorded run lesson

Run `28903545221` completed the fresh search-19 contact-state DP reconstruction after the previous red checker bug was fixed. All precheck, shard, and aggregate jobs succeeded.

Best diagnostic ordered-chain candidate:

- candidate id: `mlct22-contactdp-2714c28ba62b5c26`
- best covered_count: `46/64`
- links: `22`
- missing_count: `18`
- best mode: `official60_aware`
- best source shard/artifact: shard `14`, `contact-state-dp-22-shard-14`
- source scaffold: `mlct22-lineset-03bc99e72246b78c`
- result rows in summary: `40`
- unique ordered candidates in summary: `3`
- compact diagnostic candidates saved: `3`
- ordinary ordered-trail additions saved: `0`
- line-set scaffold additions saved: `0`
- diagnostic ordered-chain rows saved: `3`

Interpretation: search-19 is a real diagnostic improvement over search-18 (`44/64 -> 46/64`), but still far below the standing ordered-trail frontier `60/64`. It confirms that the hard part is preserving rich scaffold lines while forcing one continuous ordered 22-link chain.

The dominant failure is rich-line clipping:

- best total lost points over pieces: `17`
- clipped rich lines in best candidate: `12`
- preserved rich lines in best candidate: `8`
- official60 old-missing hits: `3`

Most repeated missing/lost points are concentrated in the reconstruction-loss family, not in the old four-hole `60/64` wall:

```text
(0,0,3), (0,3,0), (0,3,1), (1,3,3), (2,0,0), (2,3,1),
(2,3,2), (2,3,3), (3,0,1), (3,2,3), (3,3,0), (3,3,2)
```

Saved run-19 memory:

```text
runs/2026-07-08-smart-search-19-contact-state-dp-full/summary.md
runs/2026-07-08-smart-search-19-contact-state-dp-full/best_contact_state_candidate.json
runs/2026-07-08-smart-search-19-contact-state-dp-full/mode_breakdown.json
runs/2026-07-08-smart-search-19-contact-state-dp-full/contact_state_dp_run_summary_compact.json
candidates/diagnostic-contact-state-dp-run28903545221.jsonl
candidates/originals/run28903545221-contact-state-dp-index.jsonl
```

## Prepared launch package

A new launch package is now prepared and merged on `main`:

```text
smart-search-20-line-bridge
```

This corrects the temporary bad name `fl-bridge-20`. Serious numbered searches should keep the `smart-search-N-short-description` pattern.

Prepared files:

```text
.github/workflows/smart-search-20-line-bridge.yml
scripts/full_line_bridge_search.py
scripts/build_full_line_bridge_summary.py
docs/smart-search-20-line-bridge-launch.md
```

Hypothesis: preserve rich full scaffold lines and spend explicit bridge links between endpoint components instead of clipping rich lines at interior contacts.

Workflow facts:

- starts with `name: smart-search-20-line-bridge`;
- `workflow_dispatch` only;
- 20 shard matrix, `max-parallel: 20`;
- per-shard artifact: `smart-search-20-line-bridge-22-shard-<shard>`;
- aggregate artifact: `smart-search-20-line-bridge-run-summary`.

Smoke-test inputs:

```text
seconds=180
workers=4
seed=20260720
beam_width=2048
state_cap=200000
candidate_scaffolds=4
max_mutations=0
box_min=-1
box_max=4
candidate_lines=3000
start_limit=22
line_branch_limit=12
bridge_branch_limit=8
min_full_lines=10
max_full_lines=18
max_bridge_links=8
save_min_covered=38
```

Full-run inputs:

```text
seconds=21000
workers=4
seed=20260720
beam_width=12000
state_cap=2000000
candidate_scaffolds=6
max_mutations=1
box_min=-1
box_max=4
candidate_lines=6000
start_limit=44
line_branch_limit=24
bridge_branch_limit=16
min_full_lines=14
max_full_lines=18
max_bridge_links=8
save_min_covered=54
```

## Candidate preservation rule

Keep three banks separate:

1. ordinary ordered-trail candidates: only checked polygonal trails that are near or above the current ordered frontier;
2. line-set scaffolds: unordered cover64 line sets from search-17 and related runs;
3. ordered-chain diagnostics: search-18/search-19 reconstruction attempts far below the frontier.

Search-17 artifacts are `cover64-stitch-line-set-v1` scaffolds, not solved trails. Search-18 and search-19 outputs are checked ordered-chain diagnostics, but they are below the `60/64` ordered-trail frontier and should not be treated as ordinary candidate-bank improvements.

## Current next step

Do not choose another new hypothesis yet. The chosen hypothesis has already been implemented as `smart-search-20-line-bridge`.

Next action:

1. If `smart-search-20-line-bridge` has not been run yet, launch the smoke-test manually from GitHub Actions with the smoke inputs above.
2. If smoke-test is green, launch the full run with the full inputs above.
3. If the full run is complete, use prompt 1 to record the completed full run.
4. If smoke-test is red, inspect it as a technical failure first.
