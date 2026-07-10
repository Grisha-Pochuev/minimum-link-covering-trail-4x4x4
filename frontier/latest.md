# Current search frontier

Status: `smart-search-21-bridge-compress` smoke run `29123090565` completed successfully and advanced the checked ordered-trail frontier from `60/64` to `61/64`. The corresponding full 5h50m run `29123493808` is now running.

## Best recorded checked ordered-trail result

- candidate id: `mlct22-bc-889d7f8c45252068`
- covered_count: `61 / 64`
- coverage percent: `95.3125%`
- links: `22`
- missing count: `3`
- missing: `(0,2,1)`, `(1,3,1)`, `(2,3,1)`
- mode: `ripa_6to5_slide`
- construction: exact local `6→5` compression of the known full 23-link Ripa trail
- pure bridges: `0`
- rich4 links: `14`
- rich3 links: `1`
- productive connectors: `7`
- source run: `29123090565`
- source file: `runs/2026-07-10-smart-search-21-bridge-compress-smoke/best_candidate.json`
- status: `verified_partial_candidate`

The candidate has exactly 23 vertices and 22 nonzero links. GitHub Actions checked it with exact rational arithmetic, and the downloaded artifact was independently recomputed again outside the workflow. It is a genuine numerical frontier improvement, but it is not a complete covering trail and not a proof.

A second symmetry-inequivalent checked `61/64` candidate was also saved:

- candidate id: `mlct22-bc-81b7ac625af94cf7`
- missing: `(3,0,3)`, `(3,1,3)`, `(3,2,3)`
- mode: `ripa_6to5_slide`

Both are stored in:

```text
candidates/ordered-trail-additions-run29123090565-bridge-compress-smoke.jsonl
```

## Smoke run

- run id: `29123090565`
- run URL: https://github.com/Grisha-Pochuev/minimum-link-covering-trail-4x4x4/actions/runs/29123090565
- workflow: `smart-search-21-bridge-compress`, launched through the narrow bootstrap workflow
- profile: `smoke`
- status: `success`
- precheck: success
- shards: `20/20` succeeded
- exact checker: succeeded for every shard-best
- aggregate: success
- shard-best rows: `20`
- compact classes: `598`
- total attempts: `60554`
- compact `61/64`: `2`
- compact `60/64`: `9`
- full `64/64`: `0`

Saved smoke archive:

```text
runs/2026-07-10-smart-search-21-bridge-compress-smoke/summary.md
runs/2026-07-10-smart-search-21-bridge-compress-smoke/best_candidate.json
candidates/ordered-trail-additions-run29123090565-bridge-compress-smoke.jsonl
```

## Active full run

- run id: `29123493808`
- run URL: https://github.com/Grisha-Pochuev/minimum-link-covering-trail-4x4x4/actions/runs/29123493808
- workflow: `smart-search-21-bridge-compress`
- profile: `full`
- status when recorded: precheck succeeded; 20 full shards created and computation started
- head commit: `48a5c5a4a6afbbc81cba3fcb0ae5ebe3178261bd`

Effective full profile:

```text
seconds=21000
workers=4
shards=20
beam_width=16000
state_cap=3000000
candidate_lines=8000
start_limit=64
window_min=3
window_max=6
max_mutations=2
max_pure_bridges=6
target_min_rich_or_productive=16
save_min_covered=56
```

## Best cover64 line-set scaffold

The unordered scaffold frontier remains `64/64` with 22 lines from search-17. It is not itself an ordered polygonal trail and must remain in the line-set scaffold bank.

- candidate id: `mlct22-lineset-9772981a21b2a88a`
- source run: `28825060197`
- file: `runs/2026-07-07-smart-search-17-cover64-stitch-graph-full/best_line_set.json`

## Main structural lesson

Search-20 showed that preserving rich lines was better than clipping them but paid for eight explicit bridges and stopped at `58/64`. Search-21 changed the approach: it compressed the already complete 23-link construction directly. Even the three-minute smoke run found two exact `61/64` ordered trails with zero pure bridges.

This is the first numerical improvement beyond the old `60/64` wall. The most promising current family is therefore local `5→4` and `6→5` compression of the full 23-link trail, especially around the first several links.

## Current next step

Do not launch another run while `29123493808` is active. When it completes, use Prompt 1 to record its artifacts, all 20 shard-best originals, compact classes, candidate additions, missing-point frequencies, and the final checked frontier.
