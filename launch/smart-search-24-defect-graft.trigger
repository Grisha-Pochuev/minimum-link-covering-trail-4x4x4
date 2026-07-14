workflow: smart-search-24-defect-graft
launch_date: 2026-07-14
launch_mode: automatic_precheck_smoke_then_full
source_search23_run_id: 29249275103
source_minimum_shards: 19
source_shard11_retry_job_id: 87086816523
smoke_seconds: 180
full_seconds: 20400
timeout_minutes: 359
minimum_headroom_seconds: 900
shards: 20
workers_per_shard: 4
max_parallel: 20
base_seed: 20260724
hypothesis: exact defect-line graft plus two-or-three exact connector lines, followed by exact Hamiltonian support-line ordering and finite-segment realization
safety: full starts only after all 20 smoke shards and both exact verifiers pass; final aggregate is strict 20/20
