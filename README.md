# Minimum-Link Covering Trail for the 4×4×4 Cubic Grid

This repository is part of my personal project **The Open Mathematics Project**.

## What is this problem about?

Imagine a cube made from a regular `4 × 4 × 4` grid of points. There are 64 points in total. The challenge is to draw one continuous broken line through space so that every grid point is touched at least once.

But there is a catch: we want to use as few straight pieces as possible.

Each straight piece of the broken line is called a **link**. The whole broken line is called a **trail**. So the question is:

> What is the minimum number of straight links needed to cover all 64 points of the `4 × 4 × 4` cubic grid?

At first the problem looks like a drawing puzzle. But it quickly becomes a finite geometric optimization problem. A single straight link can pass through several grid points, and good solutions depend on finding the right long lines, joining them in the right order, and avoiding wasteful moves. The hard part is not just covering the points. The hard part is proving that no shorter trail can exist.

## Repository goal

The goal of this repository is to study the **minimum-link covering trail problem for the `4 × 4 × 4` cubic grid** step by step.

The repository is meant to contain:

- candidate constructions;
- lower-bound ideas;
- search experiments;
- reproducible scripts;
- notes on failed approaches;
- partial reductions and proof attempts.

The final target is to determine the exact minimum number of links, or at least to narrow the problem enough that the remaining cases are clearly visible and checkable.

## Why this problem is interesting

This is a small finite problem, but it has the typical shape of many hard mathematical puzzles:

- the object is easy to describe;
- brute force is possible only with good reductions;
- a nice construction is not enough without a matching lower bound;
- the boundary between computation and proof is important.

The `4 × 4 × 4` case is especially attractive because it is small enough to visualize, but large enough that naive search quickly becomes messy.

## Basic definitions

Let

```text
G = {0,1,2,3} × {0,1,2,3} × {0,1,2,3}.
```

This is the set of 64 grid points in the cubic grid.

A **link** is one straight segment in three-dimensional space.

A **covering trail** is a continuous polygonal chain made of links such that every point of `G` lies on at least one link.

The main quantity of interest is:

```text
L(4,4,4) = the minimum number of links in a covering trail for G.
```

## Working principle

The work in this repository follows two complementary directions.

First, we look for short explicit trails. This gives upper bounds: if we construct a trail with `k` links, then the answer is at most `k`.

Second, we try to prove that shorter trails are impossible. This gives lower bounds: if we prove that no trail with fewer than `k` links can cover all points, then the answer is at least `k`.

When the upper bound and lower bound meet, the problem is solved.

## Reproducibility

The repository should be useful not only as a personal notebook, but also as a checkable record. Whenever possible, scripts and results should be organized so that another person can reproduce the search or verify a proposed construction.

A good result should include:

- the exact list of links or trail vertices;
- the set of covered grid points;
- the number of covered points;
- a verification script;
- a short explanation of what the result proves.

## Current progress

As of **16 July 2026**:

- an exact covering trail with `23` links is known, so `L(4,4,4) ≤ 23`;
- the `22`-link case remains open;
- the best exactly checked ordered `22`-link trail covers `62/64` points (`96.875%`);
- its two missing points are `(1,0,2)` and `(3,3,1)`;
- no verified ordered `63/64` or `64/64` trail with `22` links has been found;
- the latest completed strict 20-shard search found thousands of unordered `64/64` line sets, but none could be realized as a valid finite ordered trail. This indicates that joining strong covering lines into one continuous trail is the central obstruction.

The current search studies atomic replacements of two core lines. Exact local analysis showed that changing only one rich line cannot escape the present `62/64` neighborhood. This is strong bounded evidence, but not a proof that a `22`-link solution is impossible.

## Best verified 22-link trail

Candidate: [`mlct22-ct-c64aebf0ed34cdf4`](runs/2026-07-13-smart-search-23-core-transplant-full/best_candidate.json)

It has `23` vertices and therefore `22` consecutive links. Vertices outside the cube and half-integer coordinates are allowed. The trail is followed in this order:

```text
P0  = ( 2.0,  3.0, 1.0)
P1  = (-1.0,  0.0, 1.0)
P2  = ( 5.5,  0.0, 1.0)
P3  = ( 3.0, -1.0, 3.0)
P4  = ( 3.0,  3.0, 3.0)
P5  = ( 0.0,  0.0, 0.0)
P6  = ( 3.0,  0.0, 0.0)
P7  = ( 0.0,  3.0, 3.0)
P8  = ( 0.0,  0.0, 3.0)
P9  = ( 3.0,  3.0, 0.0)
P10 = (-1.0,  3.0, 0.0)
P11 = ( 2.0,  0.0, 3.0)
P12 = ( 2.0,  5.0, 3.0)
P13 = (-1.0,  2.0, 0.0)
P14 = ( 4.0,  2.0, 0.0)
P15 = ( 1.0, -1.0, 3.0)
P16 = ( 1.0,  4.0, 3.0)
P17 = ( 4.0,  1.0, 0.0)
P18 = (-1.0,  1.0, 0.0)
P19 = ( 3.0,  5.0, 2.0)
P20 = ( 3.0, -1.0, 2.0)
P21 = ( 0.0,  5.0, 2.0)
P22 = ( 0.0,  0.0, 2.0)
```

This candidate passed both exact CI verifiers and two additional independent exact incidence checks. It is a verified **partial** trail, not yet a complete solution.

For the detailed and continuously updated research state, see [`START_HERE.md`](START_HERE.md) and [`frontier/latest.md`](frontier/latest.md).

## License

This project is released under the MIT License.
