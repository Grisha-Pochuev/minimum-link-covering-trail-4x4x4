# Manual Exploration and Overnight Search Summary — 2026-06-23

This note records the current state of the `4x4x4` minimum-link covering trail search after the first manual exploration phase and the first long GitHub Actions overnight run.

The note is not a proof and does not claim a new bound. It is a reproducibility and direction note: what was tried, what worked technically, what did not solve the problem, and what should be tried next.

## Current mathematical status

The working status remains:

```text
21 <= h(4,3) <= 23
```

The known 23-link covering trail is included in the repository and is verified by the checker. The overnight run also verified the known 23-link trail before launching the 22-link search shards.

No 22-link covering trail was found in the overnight run.

No proof of impossibility for 22 links was obtained.

So the exact value is still one of:

```text
h(4,3) = 21
h(4,3) = 22
h(4,3) = 23
```

## Manual exploratory work

The initial idea was to separate the problem into two layers:

1. cover the 64 grid points by good lines;
2. stitch those lines into one continuous trail.

This led to a useful correction. Covering by lines alone is not enough. A line may be rich as an infinite line, but the actual trail link only covers the grid points lying between its two neighboring trail vertices. Therefore the real condition is stronger than line coverage.

The important structural phrase for future work is:

```text
span condition
```

A useful link is not just a rich line. It must be sufficiently stretched between its two neighboring junctions so that it actually captures the intended grid points.

The manual exploration also suggested that a simple connected cover by 22 rich lines is too weak. It can look promising at the line-graph level while failing as an actual polygonal trail.

Another manual lead was local compression of the known 23-link trail. Small local edits came close but did not produce a full 22-link covering trail. The best manual/local leads were better than the first overnight search, but they are not yet recorded as formal certificates in this repository.

Main manual conclusion:

```text
A 22-link solution, if it exists, is probably not a tiny cosmetic edit of the known 23-link construction.
```

The next search should be seeded by strong known candidates and should test repairs and compressions, not only build paths from scratch.

## Overnight run

GitHub Actions run:

```text
run id: 27988186082
workflow: overnight-22-search
branch: main
head sha: 5f7771a50b97079323fcb61317ac888b6a63fc2f
date: 2026-06-23
```

Search parameters:

```text
links: 22
seconds per shard: 20400
box_min: -3
box_max: 7
top_k: 32
shards: 16
seed: 20260623
```

All jobs completed successfully. The known 23-link trail was verified first, and all 16 overnight shards uploaded result artifacts.

## Overnight results

The overnight run made approximately:

```text
69,161,798 total attempts
```

Best result:

```text
53 / 64 covered grid points
22 links
11 missing grid points
```

Distribution across shards:

```text
53 / 64: 5 shards
52 / 64: 11 shards
64 / 64: 0 shards
```

The best shards were:

```text
shard 0
shard 9
shard 10
shard 12
shard 15
```

All of them reached 53 covered points, not a full covering trail.

## Interpretation

The infrastructure works:

- GitHub Actions runs the checker;
- the known 23-link trail is verified;
- the search is split into independent shards;
- each shard saves an artifact;
- long runs can be reproduced.

But the first overnight search algorithm is too weak. It did not improve the known upper bound and did not approach the best manual leads.

Therefore simply rerunning the same overnight script is probably not the best next step.

## Recommended next step

The next script should not start blindly from scratch. It should use one of these stronger strategies:

1. **repair-from-23 search**

   Start from the known 23-link trail and search for 22-link compressions. Try deleting or merging one local bridge and repairing the lost points.

2. **seeded local repair search**

   Start from the best known 60/64 or 62/64 exploratory candidates and search for local replacements that cover the missing points without adding a 23rd link.

3. **span-aware line search**

   Keep the coverage/stitching separation, but add the span condition. A candidate line should be scored by how many grid points its actual segment covers between neighboring junctions, not by how many points the infinite line contains.

4. **full intersection-point model**

   Move beyond integer-box vertices and use the full intersection-point universe associated with the 4x4x4 grid. The current integer-box search is only a first exploratory model.

## Current progress estimate

This run does not change the mathematical bound:

```text
21 <= h(4,3) <= 23
```

But it improves the reproducible computational setup.

Approximate project progress:

```text
Before overnight run: 55-63%
After overnight run: 56-64%
```

The increase is small because no new bound was found. The gain is mainly infrastructural and diagnostic: the repository now has a working long-run pipeline, and the first blind 22-link search is shown to be weaker than the targeted local-compression direction.

## Short conclusion

The first overnight run was technically successful but mathematically negative.

It did not find a 22-link trail.

It did show that the current blind search strategy is not enough. The next meaningful improvement should be a seeded, span-aware repair search based on the known 23-link construction and the best near-miss candidates.
