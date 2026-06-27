# Candidate bank

This directory is the unified candidate bank for the 4x4x4 minimum-link covering trail search.

It is different from `runs/`. The `runs/` directory keeps the historical memory of individual GitHub Actions runs. This directory keeps reusable candidate material for later searches.

## Saving rule

Use a threshold rule:

```text
min_covered_to_save = 56
save every unique candidate with covered_count >= min_covered_to_save
```

In plain words: save all `56/64` candidates and everyone above that level: `57/64`, `58/64`, `59/64`, ..., up to a possible full `64/64`.

Do not save only the single best candidate per shard. Strong-but-not-best candidates may contain geometry that can be repaired later.

## Files

- `index.json` — machine-readable bank manifest and counts.
- `bank.jsonl` — one full unique candidate per line, including `vertices2`.
- `by_run/<run_id>.jsonl` — original source records from a run. This may contain duplicate geometries if different shards or modes found the same shape.
- `by_coverage/<covered_count>.jsonl` — unique candidates grouped by coverage level.

## Initial contents

The first version is seeded from GitHub Actions run `28200925016` (`repair-search-5`).

That completed run preserved one best JSON per shard. Therefore the initial source layer has 20 source records: 13 at `58/64` and 7 at `57/64`. After deduplication these become 5 unique candidate geometries.

Future runs should write a broader candidate bank directly, not only shard-best JSON.
