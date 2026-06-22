#!/usr/bin/env python3
"""Exploratory search for a 22-link trail in an integer box.

This is not a proof program. It is an anytime heuristic search. It is designed
for GitHub Actions: run many shards, keep the best candidate from each shard,
and then inspect the repeated missing-point patterns.

A complete success is easy to recognize and verify:
covered_count = 64, missing = [], links = 22.
"""
from __future__ import annotations

import argparse
import json
import math
import random
import time
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Tuple

Point = Tuple[int, int, int]
GRID: List[Point] = [(x, y, z) for x in range(4) for y in range(4) for z in range(4)]
FULL_MASK = (1 << 64) - 1


def sub(a: Point, b: Point) -> Point:
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def dot(a: Point, b: Point) -> int:
    return a[0]*b[0] + a[1]*b[1] + a[2]*b[2]


def cross(a: Point, b: Point) -> Point:
    return (
        a[1]*b[2] - a[2]*b[1],
        a[2]*b[0] - a[0]*b[2],
        a[0]*b[1] - a[1]*b[0],
    )


def on_segment(a: Point, b: Point, p: Point) -> bool:
    d = sub(b, a)
    if d == (0, 0, 0):
        return p == a
    ap = sub(p, a)
    if cross(d, ap) != (0, 0, 0):
        return False
    t = dot(ap, d)
    return 0 <= t <= dot(d, d)


def mask_for_segment(a: Point, b: Point) -> int:
    mask = 0
    for i, p in enumerate(GRID):
        if on_segment(a, b, p):
            mask |= 1 << i
    return mask


def bitcount(x: int) -> int:
    return x.bit_count()


def missing_from_mask(mask: int) -> List[List[int]]:
    return [list(p) for i, p in enumerate(GRID) if not (mask >> i) & 1]


def make_vertices(box_min: int, box_max: int) -> List[Point]:
    return [(x, y, z) for x in range(box_min, box_max + 1)
                    for y in range(box_min, box_max + 1)
                    for z in range(box_min, box_max + 1)]


def build_moves(vertices: List[Point]) -> Tuple[Dict[int, List[Tuple[int, int, int]]], List[Tuple[int, int, int, int]]]:
    """Return adjacency and directed start moves.

    adjacency[u] contains (v, mask, base_score).
    start_moves contains (u, v, mask, base_score).
    """
    adjacency: Dict[int, List[Tuple[int, int, int]]] = defaultdict(list)
    starts: List[Tuple[int, int, int, int]] = []
    n = len(vertices)
    for i in range(n):
        a = vertices[i]
        for j in range(i + 1, n):
            b = vertices[j]
            mask = mask_for_segment(a, b)
            if mask == 0:
                continue
            c = bitcount(mask)
            # Prefer segments covering many grid points. A tiny length penalty
            # avoids uselessly huge jumps when two candidates cover the same points.
            length2 = dot(sub(b, a), sub(b, a))
            score = c * 1000 - min(length2, 200)
            adjacency[i].append((j, mask, score))
            adjacency[j].append((i, mask, score))
            starts.append((i, j, mask, score))
            starts.append((j, i, mask, score))
    for u in list(adjacency):
        adjacency[u].sort(key=lambda item: (bitcount(item[1]), item[2]), reverse=True)
    starts.sort(key=lambda item: (bitcount(item[2]), item[3]), reverse=True)
    return adjacency, starts


def choose_next(rng: random.Random, candidates: List[Tuple[float, int, int, int]], top_k: int) -> Tuple[int, int, int] | None:
    if not candidates:
        return None
    candidates.sort(reverse=True, key=lambda x: x[0])
    pool = candidates[:max(1, min(top_k, len(candidates)))]
    # Soft preference to the top without making the search deterministic.
    weights = [1.0 / (i + 1) for i in range(len(pool))]
    pick = rng.choices(pool, weights=weights, k=1)[0]
    _, v, mask, base_score = pick
    return v, mask, base_score


def one_walk(
    rng: random.Random,
    vertices: List[Point],
    adjacency: Dict[int, List[Tuple[int, int, int]]],
    start: Tuple[int, int, int, int],
    links: int,
    top_k: int,
) -> Tuple[int, List[int], int]:
    u, v, mask, _ = start
    path = [u, v]
    covered = mask
    last = u
    current = v
    used_edges = {(u, v)}

    for depth in range(1, links):
        cand: List[Tuple[float, int, int, int]] = []
        for nxt, m, base_score in adjacency.get(current, []):
            if nxt == last:
                # Immediate backtracking almost never helps.
                continue
            gain = bitcount(m & ~covered)
            if gain == 0 and rng.random() > 0.05:
                continue
            revisit_penalty = 70 if nxt in path else 0
            edge_penalty = 120 if (current, nxt) in used_edges else 0
            # Need strong preference for new grid points, but keep some noise.
            score = gain * 10000 + bitcount(m) * 650 + base_score - revisit_penalty - edge_penalty + rng.random() * 1000
            cand.append((score, nxt, m, base_score))
        nxt_choice = choose_next(rng, cand, top_k)
        if nxt_choice is None:
            break
        nxt, m, _ = nxt_choice
        used_edges.add((current, nxt))
        last, current = current, nxt
        path.append(current)
        covered |= m
        if covered == FULL_MASK and len(path) == links + 1:
            break
    return covered, path, len(path) - 1


def save_result(path: Path, result: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(result, indent=2, sort_keys=True), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--links", type=int, default=22)
    parser.add_argument("--seconds", type=int, default=600)
    parser.add_argument("--box-min", type=int, default=-3)
    parser.add_argument("--box-max", type=int, default=7)
    parser.add_argument("--top-k", type=int, default=32)
    parser.add_argument("--shard", type=int, default=0)
    parser.add_argument("--shards", type=int, default=1)
    parser.add_argument("--seed", type=int, default=20260623)
    parser.add_argument("--out", type=Path, default=Path("results/best_22.json"))
    args = parser.parse_args()

    t0 = time.time()
    rng = random.Random(args.seed + 1000003 * args.shard)
    vertices = make_vertices(args.box_min, args.box_max)
    adjacency, starts_all = build_moves(vertices)
    starts = [s for i, s in enumerate(starts_all) if i % args.shards == args.shard]
    if not starts:
        raise SystemExit("this shard has no start moves")

    print(f"vertices_in_box: {len(vertices)}")
    print(f"directed_start_moves_all: {len(starts_all)}")
    print(f"directed_start_moves_this_shard: {len(starts)}")
    print(f"links: {args.links}")
    print(f"seconds: {args.seconds}")
    print(f"box: [{args.box_min}, {args.box_max}]^3")

    best_mask = 0
    best_path: List[int] = []
    attempts = 0
    next_report = t0 + 60

    # Cycle through shuffled starts repeatedly. This gives every shard coverage,
    # but still keeps the run random enough to explore different paths.
    while time.time() - t0 < args.seconds:
        rng.shuffle(starts)
        for start in starts:
            if time.time() - t0 >= args.seconds:
                break
            mask, path, used_links = one_walk(rng, vertices, adjacency, start, args.links, args.top_k)
            attempts += 1
            if bitcount(mask) > bitcount(best_mask) or (bitcount(mask) == bitcount(best_mask) and len(path) > len(best_path)):
                best_mask = mask
                best_path = path
                result = {
                    "schema": "minimum-link-covering-trail-search-result-v1",
                    "status": "complete_22_found" if best_mask == FULL_MASK and len(best_path) == args.links + 1 else "partial_candidate",
                    "links_target": args.links,
                    "links": max(0, len(best_path) - 1),
                    "covered_count": bitcount(best_mask),
                    "missing": missing_from_mask(best_mask),
                    "vertices": [list(vertices[i]) for i in best_path],
                    "parameters": {k: str(v) if isinstance(v, Path) else v for k, v in vars(args).items()},
                    "attempts": attempts,
                    "elapsed_seconds": round(time.time() - t0, 3),
                }
                save_result(args.out, result)
                print(f"new_best: covered={result['covered_count']} links={result['links']} missing={result['missing']}", flush=True)
                if best_mask == FULL_MASK and len(best_path) == args.links + 1:
                    print("FOUND A COMPLETE 22-LINK CANDIDATE")
                    return 0
            if time.time() >= next_report:
                print(f"progress: attempts={attempts} best={bitcount(best_mask)}/64 elapsed={round(time.time()-t0,1)}s", flush=True)
                next_report = time.time() + 60

    result = {
        "schema": "minimum-link-covering-trail-search-result-v1",
        "status": "complete_22_found" if best_mask == FULL_MASK and len(best_path) == args.links + 1 else "partial_candidate",
        "links_target": args.links,
        "links": max(0, len(best_path) - 1),
        "covered_count": bitcount(best_mask),
        "missing": missing_from_mask(best_mask),
        "vertices": [list(vertices[i]) for i in best_path],
        "parameters": {k: str(v) if isinstance(v, Path) else v for k, v in vars(args).items()},
        "attempts": attempts,
        "elapsed_seconds": round(time.time() - t0, 3),
    }
    save_result(args.out, result)
    print("final_best:")
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
