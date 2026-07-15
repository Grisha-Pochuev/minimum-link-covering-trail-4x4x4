# search-25 local exact inputs

`search25_local_inputs.zip` is the permanent input bundle produced by the Step-2 local exact
experiments for `smart-search-25-core-valley`.

Bundle SHA-256:

```text
1d8f891978826ac64ee287b018e6a417a59bde7bcfb97ff1a427e5207282e2d0
```

It contains:

- `search25_plateau62_closed.jsonl` — 43 exact closed plateau states;
- `search25_common17_core.json` — the common 17 supporting lines;
- `search25_corebreak61_seeds.jsonl` — 641 exact core-break 61/64 states;
- `search25_local_experiment_manifest.json` — row counts and hashes of the unpacked files.

Step-3 preflight must verify the bundle hash, unpack it into a temporary build directory, and then
verify every inner file hash and row count before compiling or running the search engine.
