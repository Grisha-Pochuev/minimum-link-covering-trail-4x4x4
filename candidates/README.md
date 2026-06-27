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

Important deduplication rule:

```text
mirrored / reflected / coordinate-permuted / reversed-path copies are not new candidates
```

So the bank should keep only genuinely new candidate geometries, not symmetric copies of an already saved line.

## Files

- `index.json` — original machine-readable bank manifest.
- `index_2026_06_27.json` — updated count snapshot after the symmetry-aware import.
- `bank.jsonl` — one full unique candidate per line, including `vertices2`.
- `by_run/<run_id>.jsonl` — source candidates from a run. This may contain candidates already deduplicated into `bank.jsonl`.
- `by_coverage/<covered_count>.jsonl` — unique candidates grouped by coverage level.
- `by_coverage/56_2026_06_27_added.jsonl` — supplement containing the 7 newly added 56/64 candidates from run `28059258009`.

## Current contents

The bank is currently seeded from:

- GitHub Actions run `28103660449` (`smart-search-4`);
- GitHub Actions run `28200925016` (`repair-search-5`);
- GitHub Actions run `28059258009` (`overnight-smart-search`);
- local repo seed `experiments/2026-06-25-repair57-local-smoke/repair57_candidate.json`.

The current unified bank has 23 unique candidate geometries:

- `2` candidates at `58/64`;
- `3` candidates at `57/64`;
- `18` candidates at `56/64`.

Run `28059258009` contributed 7 new `56/64` geometries after deduplication under coordinate permutations, cube reflections, and trail reversal. Its other `56/64` top results were already represented in the bank.

The old baseline run `27988186082` is not included because its recorded best was `53/64`, below the current threshold.

The old baseline run `28029809039` is not included because its recorded best was `54/64`, below the current threshold.

Future runs should write a broader candidate bank directly, not only shard-best JSON.
