# smart-search-22-endpoint-repair

## Hypothesis

The 61/64 search-21 family is saturated around two three-hole lines.  A free endpoint changes only one link, so endpoint movement is cheaper than an internal vertex change.  Replacing the first endpoint of the strongest search-21 candidate already gives an exact local 62/64 seed with missing points `(2,3,1)` and `(3,3,1)`.

Search-22 combines endpoint rays with nearby window repair, forced defect-line links, coupled distant changes, two-end edits, and one search-21 control shard.  It always keeps exactly 23 vertices and 22 nonzero links.

## Inputs

- `data/search22_endpoint_62_seed.json`: independently exact local 62/64 seed.
- `data/search22_run21_60plus_seed_parts/part-*.jsonlpart`: all 103 compact 60/64 and 61/64 classes recovered from full run `29123493808`.

## Profiles

Smoke: 180 seconds, 20 shards, 4 workers per shard, 1500 beam states per worker, 100000 seen states per worker.

Full: 21000 seconds, 20 shards, 4 workers per shard, 12000 beam states per worker, 750000 seen states per worker, 600-second checkpoints.

All final coverage decisions use exact integer or rational arithmetic.  Every shard best and every saved 62+ candidate is checked by both repository verifiers.

## Shards

- 0-1 free start
- 2-3 free end
- 4-5 first 61/64 defect family
- 6-7 second 61/64 defect family
- 8-9 endpoint plus 2-3-link windows
- 10-11 endpoint plus 4-5-link windows
- 12-13 endpoint plus 6-8-link windows
- 14-16 coupled distant repair/compression
- 17 both free ends
- 18 forced link through current defects
- 19 search-21 control

The same single workflow handles smoke, full, manual dispatch, exact checking, aggregation, and artifacts.  No second launcher workflow is used.
