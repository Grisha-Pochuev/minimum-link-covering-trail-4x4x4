# Manual smoke-test instructions — smart-search-13-cover-stitch-cache

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

The workflow is intentionally a **smoke-test workflow first**, not the full 20-shard expensive run. It compiles the new engine and runs one small shard so we can confirm that the new cache/anti-wall generator is valid before spending all 20 GitHub runners.

## How to launch the smoke-test

Open GitHub:

```text
Actions -> smart-search-13-cover-stitch-cache -> Run workflow
```

Use these inputs:

```text
seconds: 180
threads: 4
seed: 20260704
min_covered_to_save: 56
```

Then press `Run workflow`.

## What the smoke-test does

It does these steps:

1. checks the known 23-link Ripa construction;
2. exports candidate-bank JSONL files into JSON seed files;
3. generates `build/cover_stitch_cache_search.cpp` from `cpp/repair56_search.cpp`;
4. compiles the generated C++ engine;
5. runs one smoke shard, shard `0`, for the chosen number of seconds;
6. validates the produced trail with `scripts/check_scaled_trail.py`;
7. uploads artifact `cover-stitch-cache-smoke-shard-0`.

## What counts as green

The smoke-test is good enough if:

```text
check-known-23: success
cover-stitch-cache-smoke: success
```

And inside the smoke job these steps pass:

```text
Export candidate bank
Prepare C++ engine
Compile C++ engine
Run tiny local smoke shard
Check smoke result
Upload artifact
```

## What to send back into ChatGPT after the smoke-test

After it finishes, send the run link and ask:

```text
Сними smoke-test smart-search-13-cover-stitch-cache. Проверь, что prepare/compile/run/check прошли, открой artifact cover-stitch-cache-smoke-shard-0, посмотри covered_count, mode, missing, worker_summaries, cache_rejects и wall_rejects. Если smoke зелёный, подготовь полный 20-shard запуск.
```

## What is the next step after green smoke

If the smoke-test is green, prepare the full workflow or expand this workflow to 20 shards:

```text
seconds: 21000
threads: 4
seed: 20260704
min_covered_to_save: 56
jobs/shards: 20
max-parallel: 20
```

The full run should keep the same engine but run all 20 shard roles:

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

Do not judge this smoke-test by coverage alone. Its first job is to prove that the new engine compiles and that the cache/anti-wall fields appear in worker summaries. The real coverage test comes only after the full 20-shard run.
