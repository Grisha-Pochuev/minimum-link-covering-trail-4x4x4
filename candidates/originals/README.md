# Original trail archive

This directory is the permanent archive for original, non-deduplicated trail candidates found in GitHub Actions runs.

It is intentionally separate from `candidates/bank.jsonl`.

## Two candidate layers

### 1. Compact working bank

`candidates/bank.jsonl` and `candidates/bank-additions-*.jsonl` are the compact search memory. They should be symmetry-deduplicated and convenient for future workflows.

Use this layer as fuel for new searches.

### 2. Original trail archive

`candidates/originals/` is the scientific archive. It should preserve original run outputs before symmetry deduplication.

Use this layer for analysis: repeated shapes, real diversity, symmetry collapses, hard defect patterns, and comparison of runs.

## File naming convention

For each completed useful run, create a file like:

```text
candidates/originals/run-<run_id>-<workflow_short_name>.jsonl
```

Example:

```text
candidates/originals/run-28292425390-smart-search-7-core5.jsonl
```

Also update:

```text
candidates/originals/index.jsonl
```

with one summary line for that archived run.

## What to store

Store every original shard-best candidate that satisfies the run threshold, normally:

```text
covered_count >= 56
links <= 22
```

Do not collapse cube symmetries, coordinate reflections, coordinate permutations, trail reversal, or repeated missing-set patterns in this archive.

Each JSONL row should contain at least:

```json
{
  "schema": "mlct-original-trail-v1",
  "run_id": 0,
  "workflow": "workflow-name",
  "source_artifact": "artifact-name",
  "source_shard": 0,
  "candidate_id": "...",
  "covered_count": 0,
  "links": 22,
  "missing": [],
  "coordinate_scale": 2,
  "vertices2": []
}
```

Optional but useful fields:

```text
mode, source_file, source_job, source_occurrence_count, target_defect_hits,
parameters, created_utc, notes
```

## What not to store here

Do not store only canonical representatives here. That belongs in `candidates/bank.jsonl` or `candidates/bank-additions-*.jsonl`.

Do not rely only on GitHub Actions artifacts for original trails. Artifacts are useful but fragile: they can expire, be inaccessible, or be hard to rediscover in a new chat.

## Post-run rule

After each completed useful run:

1. Save/update the compact bank with symmetry-deduplicated eligible candidates.
2. Save/update this original archive with all original eligible shard-best candidates.
3. Update `frontier/latest.*` and `START_HERE.md` if the frontier or next step changed.

The archive is not meant to be small. It is meant to be honest.
