# Failure analysis: `core-transplant (11)`

See `summary.md` for the full evidence. The concise diagnosis is:

- no shard-11 artifact from the first attempt;
- available sibling shards were far below the memory cap;
- successful search executables consumed the full 21,000 seconds;
- only 540 seconds remained inside a 359-minute job for all non-search work;
- the exact old log became unavailable after the retry started.

Therefore the defensible conclusion is **probable job-time/runner interruption caused by inadequate headroom**, not OOM and not a checker error. Future workflows must pass `scripts/check_long_run_budget.py` with at least 900 seconds of headroom and should use 20,400 seconds for a 359-minute job.
