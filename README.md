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

## Current status

This repository is starting as a working space. The first tasks are:

- define the grid and the verification format;
- collect simple candidate trails;
- write a checker for whether a trail covers all 64 points;
- search for good upper bounds;
- formulate lower-bound obstacles.

## License

This project is released under the MIT License.
