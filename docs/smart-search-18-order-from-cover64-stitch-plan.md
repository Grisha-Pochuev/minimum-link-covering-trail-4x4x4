# smart-search-18-order-from-cover64-stitch plan

## Purpose

This launch package implements the chosen step-2 hypothesis: contact-aware ordered reconstruction from the `smart-search-17-cover64-stitch-graph` scaffolds.

Search-17 found unordered 22-line scaffolds that cover `64/64` grid points and have stitch graph path lower bound `22/22`. That graph condition is weaker than a real polygonal trail. Search-18 tries to convert those scaffolds into actual ordered chains by choosing:

1. a line order;
2. concrete contact vertices between consecutive lines;
3. actual segment endpoints in `vertices2` form;
4. optional small line replacements in mutation modes.

The score is actual ordered-chain coverage, not unordered line-set coverage.

## Inputs

Primary inputs:

```text
runs/2026-07-07-smart-search-17-cover64-stitch-graph-full/best_line_set.json
candidates/line-set-additions-run28825060197-cover64-stitch.jsonl
```

Control checks:

```text
python scripts/check_trail.py data/ripa_23_trail.json --expected-links 23 --require-full
python scripts/check_cover64_line_set.py runs/2026-07-07-smart-search-17-cover64-stitch-graph-full/best_line_set.json --expect-covered 64 --max-lines 22 --min-stitch-path 22
```

## Files in this package

```text
.github/workflows/smart-search-18-order-from-cover64-stitch.yml
docs/proposed-smart-search-18-order-from-cover64-stitch.yml
scripts/order_from_cover64_stitch.py
scripts/check_ordered_trail_scaled.py
scripts/build_order_from_cover64_stitch_summary.py
```

## Shard modes

```text
0-3    strict_reconstruct_top4
       Fixed search-17 stitch-22 scaffolds. This is a diagnostic control.

4-7    one_two_line_mutation
       Replace one or two scaffold lines and re-run contact-aware ordering.

8-11   contact_extreme_search
       Bias toward lines/contact choices that preserve useful endpoints.

12-15  bridge_contact_repair
       Use replacement lines as contact bridges between rich scaffold parts.

16-18  large_neighborhood_ordering
       Larger local neighborhood: replace several lines around bad contact loss.

19     control_fixed_best
       Control mode on the best recorded search-17 scaffold.
```

## Artifact names

Shard artifacts:

```text
order-cover64-stitch-22-shard-*
```

Summary artifact:

```text
order-cover64-stitch-run-summary
```

Summary files:

```text
collected/order_from_cover64_stitch_run_summary.json
collected/order_from_cover64_stitch_run_summary.md
collected/order-from-cover64-candidates.jsonl
```

## Smoke-test inputs

```text
workflow: smart-search-18-order-from-cover64-stitch
seconds: 180
workers: 4
seed: 20260718
min_actual_covered_to_save: 38
beam_width: 512
branch_limit: 5
start_limit: 22
max_mutations: 2
box_min: -1
box_max: 4
candidate_lines: 3000
min_line_cover: 2
```

Smoke-test meaning: technical green light only. It verifies that scripts, input paths, shard artifacts, checker, and aggregation work. If the smoke gets a green check and the user launches the full run, the next ordinary result-taking step should record the full run, not separately analyze the smoke unless it failed or looked suspicious.

## Full-run inputs

```text
workflow: smart-search-18-order-from-cover64-stitch
seconds: 21000
workers: 4
seed: 20260718
min_actual_covered_to_save: 38
beam_width: 512
branch_limit: 5
start_limit: 22
max_mutations: 2
box_min: -1
box_max: 4
candidate_lines: 3000
min_line_cover: 2
```

## Success criteria

Strong success:

```text
checked ordered 22-link trail with covered_count >= 61, especially 64/64
```

Medium success:

```text
actual ordered-chain coverage improves over the local strict baseline from step 2
```

Weak but useful success:

```text
all fixed stitch-22 scaffolds fail in the same contact-loss way, with concrete missing points and weak links recorded
```

Failure:

```text
workflow only reproduces scaffold graph scores and does not measure actual ordered-chain coverage
```

## Important caveat

Search-18 outputs are ordered-chain candidates and diagnostics. A `64/64` result must still be checked by `scripts/check_ordered_trail_scaled.py` and, if converted to unscaled ordinary vertices when possible, by the standard `check_trail.py`-style logic.
