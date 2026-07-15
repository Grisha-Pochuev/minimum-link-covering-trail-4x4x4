# search-25 versioned runtime

`data/search25_runtime.tar.gz` is the exact implementation bundle for
`smart-search-25-core-valley`.

SHA-256:

```text
edd133b3fccf61638100360c146e9bd4e903107fa3fa4f9f2c4c896f73f983d5
```

The workflow checks this hash before the shared preflight and smoke matrix, then extracts:

- `src/search25/core_valley_search.cpp` — C++20 atomic paired core-valley engine;
- `scripts/materialize_search25_inputs.py`;
- `scripts/verify_core_valley.py`;
- `scripts/verify_core_valley_independent.py`;
- `scripts/build_core_valley_summary.py`;
- `scripts/preflight_search25.py`;
- `scripts/run_search25_ci.py`.

Individual source SHA-256 hashes:

```text
ffc36f960dfad01c82b6e676c6dadf828fa1effbf054d06c4b28abaf59ff38f2  scripts/materialize_search25_inputs.py
58ff58ffad0093d6aaa32d7f1cda83e4aaf0995e1e39291a9c5f7a1b22879b45  src/search25/core_valley_search.cpp
a88884a9671478db8043a421289e6f922cc219835ff5af5d57ef285b4e1ffa5c  scripts/verify_core_valley.py
c3c9a3cfc4a382943ef29883606a2b95393081b39684aaff495eb605026ce448  scripts/verify_core_valley_independent.py
e571d45e1d6675c52cfb80c316ea0864d24b3a3371ec68204125e18e83b9949d  scripts/build_core_valley_summary.py
57bfd5236b4629507ce34efe21c70a7d319be7ec4d9b8be8ac63b7313bbf830e  scripts/preflight_search25.py
db7970dc9d90f220418808cbc0752a50ded0af0668c6b481b2e785597ab2c9e7  scripts/run_search25_ci.py
```

The archive is versioned in the launch commit, so every Actions job uses exactly the implementation
that passed the local and CI preflight.
