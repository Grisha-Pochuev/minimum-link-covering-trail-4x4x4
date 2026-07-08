# Current search frontier

Status: completed `smart-search-19-contact-state-dp` run recorded. The normal ordered-trail frontier remains `60/64`; the scaffold frontier from search-17 remains unordered `64/64` with stitch path lower bound `22/22`. Search-19 improved the ordered-reconstruction diagnostic ceiling from `44/64` to `46/64`, but did not improve the actual ordered-trail frontier.

Latest recorded completed run:

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

Search-19 mode breakdown:

| mode | rows | unique | best links | best covered | best lost |
|---|---:|---:|---:|---:|---:|
| `conservative_control` | 2 | 1 | 22 | 42 | 23 |
| `controlled_bridge_replacement` | 4 | 1 | 22 | 46 | 18 |
| `diagnostic_replay` | 2 | 1 | 22 | 42 | 23 |
| `exact_top4_dp` | 8 | 1 | 22 | 42 | 23 |
| `loss_minimizing` | 8 | 2 | 22 | 46 | 17 |
| `official60_aware` | 8 | 2 | 22 | 46 | 17 |
| `wide_beam_contact_state` | 8 | 1 | 22 | 46 | 17 |

Saved run-19 memory:

```text
runs/2026-07-08-smart-search-19-contact-state-dp-full/summary.md
runs/2026-07-08-smart-search-19-contact-state-dp-full/best_contact_state_candidate.json
runs/2026-07-08-smart-search-19-contact-state-dp-full/mode_breakdown.json
runs/2026-07-08-smart-search-19-contact-state-dp-full/contact_state_dp_run_summary_compact.json
candidates/diagnostic-contact-state-dp-run28903545221.jsonl
candidates/originals/run28903545221-contact-state-dp-index.jsonl
```

## Prepared / suggested next launch

No new workflow is prepared yet after search-19. The next normal web-chat step is prompt 2: choose a non-repeating hypothesis.

Suggested next direction from the recorded evidence:

```text
smart-search-20-full-line-preserving-contact-bridge
```

Reason: search-19 exposes that contact-state ordering destroys coverage by clipping rich 3/4-point lines. The next attempt should preserve full rich pieces first and pay explicit bridge/contact costs between whole pieces, rather than choosing short contact pieces that turn a `64/64` scaffold into a `46/64` chain.

One caveat: run `28903545221` used full seconds but default/smoke DP width. If needed, one controlled follow-up can run the intended true full-width search-19 profile (`beam_width=8192`, `state_cap=2000000`, `max_mutations=2`) before fully abandoning this workflow. But do not rerun search-19 unchanged.

## Candidate preservation rule

Keep three banks separate:

1. ordinary ordered-trail candidates: only checked polygonal trails that are near or above the current ordered frontier;
2. line-set scaffolds: unordered cover64 line sets from search-17 and related runs;
3. ordered-chain diagnostics: search-18/search-19 reconstruction attempts far below the frontier.

Search-17 artifacts are `cover64-stitch-line-set-v1` scaffolds, not solved trails. Search-18 and search-19 outputs are checked ordered-chain diagnostics, but they are below the `60/64` ordered-trail frontier and should not be treated as ordinary candidate-bank improvements.
