# smart-search-20-line-bridge full run

Run recorded: 2026-07-09.

- Repository: `Grisha-Pochuev/minimum-link-covering-trail-4x4x4`
- Run id: `28973760924`
- Run URL: https://github.com/Grisha-Pochuev/minimum-link-covering-trail-4x4x4/actions/runs/28973760924
- Workflow: `smart-search-20-line-bridge`
- Head commit: `772596df3d9fd796d2a5bf5ee0ea48697ca17031`
- Status: `success`
- Profile: `full`
- Shards/jobs: `20` line-bridge shards + prechecks + aggregate
- Workers per shard: `4`
- Main artifact: `smart-search-20-line-bridge-run-summary`
- Per-shard artifacts: `smart-search-20-line-bridge-22-shard-*`

## Effective full profile

```json
{
  "beam_width": 12000,
  "box_max": 4,
  "box_min": -1,
  "bridge_branch_limit": 16,
  "candidate_lines": 6000,
  "candidate_scaffolds": 6,
  "line_branch_limit": 24,
  "max_bridge_links": 8,
  "max_full_lines": 18,
  "max_mutations": 1,
  "min_full_lines": 14,
  "profile": "full",
  "save_min_covered": 54,
  "seconds": 21000,
  "seed": 20260720,
  "start_limit": 44,
  "state_cap": 2000000,
  "workers": 4
}
```

## Result

This run did **not** improve the standing ordered-trail frontier.

Standing ordered-trail frontier before the run:

- `60/64`, 22 links
- candidate `mlct22-3cf45a2e21fe611c`
- source run `28674416173`
- missing: `(0,0,1)`, `(0,2,3)`, `(0,3,1)`, `(2,1,1)`

Best result from this run:

- candidate id: `mlct22-flbridge-8da0e01c34bb9c88`
- links: `22`
- covered_count: `58/64`
- missing_count: `6`
- missing: `(0,2,0), (0,2,2), (2,1,0), (2,1,2), (2,3,0), (3,2,0)`
- mode: `one_line_replacement`
- source shard: `16`
- source artifact: `smart-search-20-line-bridge-22-shard-16`
- full-line links: `14`
- bridge links: `8`
- preserved rich lines: `14`
- official60 old-missing hits: `4`

Interpretation: the line-bridge hypothesis produced a checked 22-link ordered-chain diagnostic at `58/64`. It is below the known `60/64` ordered-trail frontier, so it is saved in the diagnostic bank, not in the ordinary ordered-trail candidate bank.

## Aggregate counts

- raw result rows in summary: `40`
- shard-best outputs: `20`
- unique compact ordered candidates: `6`
- ordinary ordered-trail additions saved: `0`
- diagnostic compact candidates saved: `6`
- originals index rows saved: `6`
- `above_46`: `6`
- `above_50`: `6`
- `above_56`: `3`
- `above_60`: `0`
- `at_least_61`: `0`
- `full_64`: `0`

Coverage histogram:

```json
[
  {
    "count": 2,
    "covered_count": 58
  },
  {
    "count": 8,
    "covered_count": 57
  },
  {
    "count": 30,
    "covered_count": 56
  }
]
```

## Mode breakdown

| mode | rows | unique | best covered | best links | full lines | bridges | rich kept | old hits |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `conservative_control` | 2 | 1 | 56 | 22 | 14 | 8 | 14 | 3 |
| `diverse_endpoint_components` | 8 | 1 | 56 | 22 | 14 | 8 | 14 | 3 |
| `integer_full_bridge` | 8 | 1 | 56 | 22 | 14 | 8 | 14 | 3 |
| `official60_bridge` | 8 | 1 | 56 | 22 | 14 | 8 | 14 | 3 |
| `one_line_replacement` | 6 | 3 | 58 | 22 | 14 | 8 | 14 | 4 |
| `outside_bridge_expansion` | 8 | 3 | 57 | 22 | 14 | 8 | 14 | 4 |

## Top compact candidates

| rank | candidate_id | mode | covered | links | missing_count | shard |
|---:|---|---|---:|---:|---:|---:|
| 1 | `mlct22-flbridge-8da0e01c34bb9c88` | `one_line_replacement` | 58 | 22 | 6 | 16 |
| 2 | `mlct22-flbridge-5c8e53ea4022f851` | `outside_bridge_expansion` | 57 | 22 | 7 | 5 |
| 3 | `mlct22-flbridge-a29d3218b0b1a04c` | `outside_bridge_expansion` | 57 | 22 | 7 | 4 |
| 4 | `mlct22-flbridge-5c17c9908346d910` | `outside_bridge_expansion` | 56 | 22 | 8 | 7 |
| 5 | `mlct22-flbridge-618022fb78e0abe2` | `one_line_replacement` | 56 | 22 | 8 | 17 |
| 6 | `mlct22-flbridge-1e4d0f13955aa79a` | `conservative_control` | 56 | 22 | 8 | 19 |

## Repeated missing points

Top repeated missing points over the aggregate rows:

```json
[
  {
    "count": 36,
    "point": [3, 2, 2]
  },
  {
    "count": 32,
    "point": [2, 3, 2]
  },
  {
    "count": 30,
    "point": [0, 0, 3]
  },
  {
    "count": 30,
    "point": [2, 0, 1]
  },
  {
    "count": 30,
    "point": [2, 3, 1]
  },
  {
    "count": 30,
    "point": [2, 3, 3]
  },
  {
    "count": 30,
    "point": [3, 0, 1]
  },
  {
    "count": 26,
    "point": [0, 0, 1]
  }
]
```

The strongest new diagnostic candidate hits all four old missing points from the official `60/64` candidate. The new best six-hole family is:

```text
(0,2,0), (0,2,2), (2,1,0), (2,1,2), (2,3,0), (3,2,0)
```

This matters because the run did not merely repeat the old four-hole wall. It shows that preserving rich full lines and paying explicit bridge links can repair the old holes, but the bridge budget then opens a new six-hole defect family.

## Saved files

```text
runs/2026-07-09-smart-search-20-line-bridge-full/summary.md
runs/2026-07-09-smart-search-20-line-bridge-full/best_line_bridge_candidate.json
runs/2026-07-09-smart-search-20-line-bridge-full/line_bridge_run_summary_compact.json
runs/2026-07-09-smart-search-20-line-bridge-full/mode_breakdown.json
candidates/diagnostic-line-bridge-run28973760924.jsonl
candidates/originals/run28973760924-line-bridge-index.jsonl
```

## Conclusion

Search-20 is useful as a diagnostic but not as a frontier improvement.

- ordered-trail numeric frontier: `60/64 -> 60/64`
- ordered-reconstruction / bridge diagnostic: `46/64 -> 58/64`
- ordinary ordered-trail additions: `0`
- compact diagnostic additions: `6`
- originals index rows: `6`

Do not rerun `smart-search-20-line-bridge` unchanged as the next serious step. The next research step should use this result as evidence: full-line preservation helped a lot compared with contact-state clipping, but eight explicit bridges are still too expensive and leave a new six-hole bridge-defect family.
