# Search runs

This directory stores compact summaries of important GitHub Actions search runs.

Do not use this directory as a dump for every raw log file. Raw logs and large JSON collections can stay in GitHub Actions artifacts. This directory should contain the distilled research memory that is useful for the next run and for human review.

Each serious run should get its own folder, for example:

```text
runs/2026-06-24-smart-search/
```

A run folder should usually contain:

- `README.md` — human-readable summary of what was run and what was learned;
- `smart_run_summary.json` or a reduced copy of the important artifact summary;
- optional small JSON files with best candidates, recurring missing points, or parameters;
- notes about what the next run should use as seed material.

The current frontier is always summarized in:

```text
frontier/latest.md
frontier/latest.json
```

The rule is simple:

- `runs/<date>-<name>/` preserves the memory of one run;
- `frontier/latest.*` tells the next run and the next assistant where to continue.
