# Current search frontier

This file is the human-readable working memory of the project.

It records the latest useful GitHub Actions run whose artifacts should be used as input for the next search. The goal is to make each new run continue from the previous computational evidence instead of starting from zero.

## Current status

Status: bootstrap scaffold created before the current `overnight-smart-search` run has been analyzed.

Latest confirmed completed baseline run:

- Repository: `Grisha-Pochuev/minimum-link-covering-trail-4x4x4`
- Run id: `28029809039`
- Workflow: `overnight-22-parallel-search`
- Result type: heuristic search, not a proof
- Best known coverage from that run: `54 / 64`
- Links target: `22`

The currently running or most recent `overnight-smart-search` run should replace this baseline after it finishes and its artifacts are analyzed.

## What must be updated after each serious run

After a completed GitHub Actions run, update this file with:

- run id;
- run URL;
- workflow name;
- commit SHA;
- date;
- important parameters: shards, workers, seconds, top_k, seed if available;
- best result: covered_count, links, mode, status;
- most frequent missing grid points;
- best modes or strategies;
- what the next run should use as seed material;
- what should be changed in the next workflow or search script.

## Next update plan

When the current `overnight-smart-search` run finishes:

1. Download or inspect artifacts `smart-run-summary` and `smart-22-shard-*`.
2. Copy the important summary into `runs/2026-06-24-smart-search/`.
3. Update `frontier/latest.json` with the new run id and machine-readable fields.
4. Update this file with a short human explanation.
5. Update `.github/workflows/overnight-smart-search.yml` so the next run uses the newest useful run id instead of the old baseline.
