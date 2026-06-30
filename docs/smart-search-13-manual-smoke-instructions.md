# Manual smoke/full instructions — smart-search-13-cover-stitch-cache

Prepared: 2026-06-30

This file is for the web-chat workflow where the human launches GitHub Actions manually.

## What is ready

Prepared workflow:

```text
.github/workflows/smart-search-13-cover-stitch-cache.yml
```

Prepared engine generator:

```text
scripts/prepare_cover_stitch_cache_engine.py
```

Prepared plan:

```text
docs/smart-search-13-cover-stitch-cache-plan.md
```

The workflow now uses the full GitHub parallelism pattern for this project: `20` matrix jobs with `max-parallel: 20`. With `threads=4`, this means up to `80` worker threads across GitHub runners.

## How to launch the 20-job smoke-test

Open GitHub:

```text
Actions -> smart-search-13-cover-stitch-cache -> Run workflow
```

Use these inputs for the short smoke-test:

```text
seconds: 180
threads: 4
seed: 20260704
min_covered_to_save: 56
```

Then press `Run workflow`.

This will run all 20 shards, but only for 180 seconds each. It is still a smoke-test: its main job is to prove that the new engine compiles and all 20 shard roles can produce valid JSON artifacts.

## What the smoke-test does

It does these steps:

1. checks the known 23-link Ripa construction;
2. exports candidate-bank JSONL files into JSON seed files;
3. generates `build/cover_stitch_cache_search.cpp` from `cpp/repair56_search.cpp`;
4. compiles the generated C++ engine;
5. runs 20 shard jobs with `max-parallel: 20`;
6. validates produced trails with `scripts/check_scaled_trail.py`;
7. uploads `cover-stitch-cache-22-shard-*` artifacts;
8. aggregates them into `cover-stitch-cache-run-summary`.

## What counts as green

The smoke-test is good enough if:

```text
check-known-23: success
cover-stitch-cache-search: 20/20 success
aggregate-cover-stitch-cache-results: success
```

And inside shard jobs these steps pass:

```text
Export candidate bank
Prepare C++ engine
Compile C++ engine
Run shard
Check shard result
Upload artifact
```

## What to send back into ChatGPT after the smoke-test

After it finishes, send the run link and ask:

```text
Сними smoke-test smart-search-13-cover-stitch-cache. Проверь, что 20/20 shard jobs прошли, aggregate прошёл, открой artifact cover-stitch-cache-run-summary и shard artifacts, посмотри covered_count, modes, missing, worker_summaries, cache_rejects и wall_rejects. Если smoke зелёный, скажи, запускать ли полный 20-job прогон.
```

## Full run after green smoke

If the 20-job smoke-test is green, launch the same workflow again with:

```text
seconds: 21000
threads: 4
seed: 20260704
min_covered_to_save: 56
```

The full run uses the same 20 shard roles:

```text
0-4   cover_set_beam_cache
5-8   stitch_with_transposition
9-12  repair_window_cache
13-15 anti_wall_archive
16-17 novelty_56_58
18    old_59_control
19    integer_control22
```

## Important interpretation rule

Do not judge the smoke-test by coverage alone. Its first job is to prove that the new engine compiles, all 20 jobs run, artifacts aggregate, and the cache/anti-wall fields appear in worker summaries. The real coverage test comes only after the full 20-shard run.
