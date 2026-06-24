# 2026-06-24 smart search

This folder is a prepared memory slot for the `overnight-smart-search` run from 2026-06-24.

It was created before the final artifacts were analyzed, so the fields below must be completed after the run finishes.

## Purpose

The purpose of this run is to continue from previous GitHub Actions artifacts instead of starting from zero.

The smart workflow is intended to use the previous baseline run as seed material and split the search into multiple modes:

- warm-start 22-link search;
- fractional-coordinate 22-link search;
- catalog-style 22-link search;
- strict 21-link reconnaissance;
- layer/subcube 22-link search;
- integer 22-link control.

## Baseline before this run

Latest confirmed completed baseline before this smart search:

- Run id: `28029809039`
- Workflow: `overnight-22-parallel-search`
- Best result: `54 / 64`
- Links target: `22`
- Meaning: useful heuristic baseline, not a proof.

## To fill after the run finishes

Fill this section from GitHub Actions artifacts.

- Final run id: `TODO`
- Run URL: `TODO`
- Workflow name: `overnight-smart-search`
- Commit SHA: `TODO`
- Status: `TODO`
- Duration: `TODO`
- Number of artifacts: `TODO`
- Parameters:
  - seconds: `TODO`
  - workers: `TODO`
  - top_k: `TODO`
  - shards: `16`
  - seed: `TODO`
- Best result:
  - covered_count: `TODO`
  - links: `TODO`
  - mode: `TODO`
  - status: `TODO`
  - missing: `TODO`
- Top recurring missing points: `TODO`
- Best modes or strategies: `TODO`
- New conclusions for the next run: `TODO`

## Required follow-up after artifacts are available

1. Copy the important content of `smart-run-summary` here.
2. Update `frontier/latest.md`.
3. Update `frontier/latest.json`.
4. Update `.github/workflows/overnight-smart-search.yml` so the next run uses this run id as the new artifact source.
5. If the smart run finds a significantly better candidate, preserve its vertices in a small JSON file in this folder.

## Notes

This folder is not meant to replace GitHub Actions artifacts. It is the compact research memory that survives as part of the repository.
