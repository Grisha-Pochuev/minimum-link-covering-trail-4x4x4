# fl-bridge-20 launch package

Short workflow name: `fl-bridge-20`.

Hypothesis: preserve rich full scaffold lines and spend explicit bridge links between endpoint components instead of clipping rich lines at interior contacts.

## Files

- Workflow: `.github/workflows/fl-bridge-20.yml`
- Engine: `scripts/full_line_bridge_search.py`
- Summary builder: `scripts/build_full_line_bridge_summary.py`
- Existing checker: `scripts/check_ordered_trail_scaled.py`
- Existing scaffold checker: `scripts/check_cover64_line_set.py`

## Inputs

The workflow reads:

- `runs/2026-07-07-smart-search-17-cover64-stitch-graph-full/best_line_set.json`
- `candidates/line-set-additions-run28825060197-cover64-stitch.jsonl`
- `candidates/diagnostic-contact-state-dp-run28903545221.jsonl`

## Shard modes

- `0..3`: `integer_full_bridge`
- `4..7`: `outside_bridge_expansion`
- `8..11`: `official60_bridge`
- `12..15`: `diverse_endpoint_components`
- `16..18`: `one_line_replacement`
- `19`: `conservative_control`

## Smoke-test inputs

Use these only as a green-lamp technical check:

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

## Full-run inputs

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

## Artifacts

Per shard:

- `fl-bridge-22-shard-<shard>`
  - `fl_bridge_best_shard_<shard>.json`
  - `preferred_fl_bridge_shard_<shard>.jsonl`
  - `fl_bridge_report_shard_<shard>.json`

Aggregate:

- `fl-bridge-run-summary`
  - `fl_bridge_run_summary.json`
  - `fl_bridge_run_summary.md`
  - `fl-bridge-candidates.jsonl`

## Success criteria

- Strong: checked ordered `22`-link candidate above `60/64`, especially `61/64+`.
- Medium: checked ordered `22`-link candidate `56/64+` with many preserved rich full lines.
- Diagnostic: clear evidence which endpoint components and bridge segments are responsible for the remaining losses.
