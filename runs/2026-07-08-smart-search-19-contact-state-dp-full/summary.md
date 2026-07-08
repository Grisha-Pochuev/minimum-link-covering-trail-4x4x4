# smart-search-19-contact-state-dp — run 28903545221

Run URL: https://github.com/Grisha-Pochuev/minimum-link-covering-trail-4x4x4/actions/runs/28903545221

Workflow: `smart-search-19-contact-state-dp`  
Head commit: `ed5c56c90bca2044d55cbab6f48c0fb8c3b4071f`  
Status: `success`

## What this run tested

This was the fresh search-19 run after the earlier red technical launch was fixed. It tested contact-state DP / beam reconstruction from the search-17 unordered `64/64` cover scaffolds. The checker step succeeded on the shard outputs, so this run is a real diagnostic result, not the old shell/heredoc failure.

Important parameter caution: the run used long `seconds = 21000`, but the saved best row shows smoke/default DP-width parameters: `beam_width = 2048`, `state_cap = 200000`, `max_mutations = 1`. So it was a long-duration contact-state run, but not the intended full-width profile `8192 / 2000000 / 2` recorded in the launch notes.

## Result summary

- result rows in aggregate summary: `40`
- shard artifacts: `20` (`contact-state-dp-22-shard-0..19`)
- aggregate artifact: `contact-state-dp-run-summary`
- unique ordered candidates in summary: `3`
- compact diagnostic candidates saved to bank: `3`
- ordinary ordered-trail candidate additions: `0`
- line-set scaffold additions: `0`

Best diagnostic ordered-chain candidate:

- candidate id: `mlct22-contactdp-2714c28ba62b5c26`
- mode: `official60_aware`
- source shard/artifact: shard `14`, `contact-state-dp-22-shard-14`
- source scaffold: `mlct22-lineset-03bc99e72246b78c`
- links: `22`
- covered_count: `46/64`
- missing_count: `18`
- weak_links: `0`
- total lost points over pieces: `17`
- clipped rich lines: `12`
- preserved rich lines: `8`
- official60 old-missing hits: `3`

Best missing points:

```text
(0,0,3), (0,3,0), (0,3,1), (1,0,0), (1,0,1), (1,3,3), (2,0,0), (2,0,1), (2,0,2), (2,3,1), (2,3,2), (2,3,3), (3,0,1), (3,0,2), (3,2,3), (3,3,0), (3,3,1), (3,3,2)
```

## Threshold counts

```json
{
  "above_44": 2,
  "above_50": 0,
  "above_56": 0,
  "above_60": 0,
  "at_least_61": 0,
  "full_64": 0
}
```

## Mode breakdown

| mode | rows | unique | best links | best covered | best lost |
|---|---:|---:|---:|---:|---:|
| `conservative_control` | 2 | 1 | 22 | 42 | 23 |
| `controlled_bridge_replacement` | 4 | 1 | 22 | 46 | 18 |
| `diagnostic_replay` | 2 | 1 | 22 | 42 | 23 |
| `exact_top4_dp` | 8 | 1 | 22 | 42 | 23 |
| `loss_minimizing` | 8 | 2 | 22 | 46 | 17 |
| `official60_aware` | 8 | 2 | 22 | 46 | 17 |
| `wide_beam_contact_state` | 8 | 1 | 22 | 46 | 17 |

## Saved diagnostic candidates

| rank | candidate_id | mode | links | covered | missing | shard | lost |
|---:|---|---|---:|---:|---:|---:|---:|
| 1 | `mlct22-contactdp-f3b2c041be7b6413` | `official60_aware` | 22 | 46 | 18 | 12 | 17 |
| 2 | `mlct22-contactdp-2714c28ba62b5c26` | `official60_aware` | 22 | 46 | 18 | 14 | 17 |
| 3 | `mlct22-contactdp-2ea2c5d692c5afbb` | `conservative_control` | 22 | 42 | 22 | 19 | 23 |

## Repeated defect / loss family

The dominant repeated defect family is not the old `60/64` four-hole wall. It is a reconstruction-loss family caused by clipping rich scaffold lines into shorter contact pieces.

Most frequent missing points across the 40 result rows:

```text
(0, 0, 3): 40
(0, 3, 0): 40
(0, 3, 1): 40
(1, 3, 3): 40
(2, 0, 0): 40
(2, 3, 1): 40
(2, 3, 2): 40
(2, 3, 3): 40
(3, 0, 1): 40
(3, 2, 3): 40
(3, 3, 0): 40
(3, 3, 2): 40
```

Most frequent lost points over rich-line pieces:

```text
(3, 0, 1): 40
(0, 0, 3): 40
(1, 3, 3): 40
(2, 3, 2): 40
(3, 3, 2): 40
(0, 3, 0): 40
(0, 3, 1): 40
(2, 3, 3): 40
(3, 2, 3): 40
(3, 3, 0): 38
(2, 3, 0): 36
(3, 3, 1): 34
```

Most damaging clipped line indices:

```json
[
  {"line_index": "10", "loss_score": 80},
  {"line_index": "9", "loss_score": 80},
  {"line_index": "19", "loss_score": 74},
  {"line_index": "2", "loss_score": 68},
  {"line_index": "12", "loss_score": 68},
  {"line_index": "15", "loss_score": 58},
  {"line_index": "16", "loss_score": 40},
  {"line_index": "0", "loss_score": 40},
  {"line_index": "14", "loss_score": 40},
  {"line_index": "18", "loss_score": 40},
  {"line_index": "8", "loss_score": 40},
  {"line_index": "4", "loss_score": 40}
]
```

Interpretation in plain language: the unordered search-17 scaffold still knows how to cover all 64 points, but when search-19 forces it into one concrete ordered 22-link chain, many rich 3/4-point lines get clipped. The best run preserves only `8` rich lines and clips `12`, so coverage collapses to `46/64`.

## Comparison with previous frontier

Before this run:

- best ordinary checked ordered trail: `60/64`, from run `28674416173`;
- best unordered scaffold: `64/64`, from run `28825060197`;
- best search-18 ordered reconstruction diagnostic: `44/64`.

After this run:

- best ordinary checked ordered trail: still `60/64`;
- best unordered scaffold: still `64/64`;
- best contact-state reconstruction diagnostic: `46/64`.

So search-19 gives a small diagnostic improvement over search-18 (`44/64 -> 46/64`), but no frontier improvement and no `61/64+` ordered candidate.

## Files saved from this result

```text
runs/2026-07-08-smart-search-19-contact-state-dp-full/summary.md
runs/2026-07-08-smart-search-19-contact-state-dp-full/best_contact_state_candidate.json
runs/2026-07-08-smart-search-19-contact-state-dp-full/mode_breakdown.json
runs/2026-07-08-smart-search-19-contact-state-dp-full/contact_state_dp_run_summary_compact.json
candidates/diagnostic-contact-state-dp-run28903545221.jsonl
candidates/originals/run28903545221-contact-state-dp-index.jsonl
```

## Next non-repeating step

Do not rerun `smart-search-19-contact-state-dp` unchanged.

A useful next hypothesis should attack the exact loss mechanism exposed here: full rich lines are being clipped during contact-state ordering. The next launch should either:

1. run the intended true full-width search-19 profile once, because this run used full seconds but smoke/default DP width; or
2. preferably move to `smart-search-20-full-line-preserving-contact-bridge`: preserve complete 3/4-point rich pieces as much as possible and pay explicit bridge/contact costs between whole pieces, instead of choosing short contact pieces that destroy coverage.

The scientific lesson is now sharper: the bottleneck is not finding `64/64` line sets; it is preserving rich-line coverage while turning a scaffold into one continuous ordered trail.
