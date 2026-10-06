#!/usr/bin/env python3
"""Shared exact helpers for smart-search-26-anchored-exact (Python stdlib only).

The lattice-line enumeration order is identical to src/search26/anchored_exact.cpp,
so line ids written by the engine can be decoded here.  All geometry uses
fractions.Fraction; no floating point is used for any decision.
"""
from __future__ import annotations

import json
import math
from fractions import Fraction as Q
from typing import Any, Iterable

Point = tuple[Q, Q, Q]


def bit_point(b: int) -> tuple[int, int, int]:
    return (b // 16, (b // 4) % 4, b % 4)


def build_lines() -> list[dict[str, Any]]:
    seen: set[tuple[int, ...]] = set()
    lines: list[dict[str, Any]] = []
    for i in range(64):
        for j in range(i + 1, 64):
            p = bit_point(i)
            q = bit_point(j)
            d = [q[k] - p[k] for k in range(3)]
            g = math.gcd(math.gcd(abs(d[0]), abs(d[1])), abs(d[2]))
            d = [c // g for c in d]
            if d[0] < 0 or (d[0] == 0 and (d[1] < 0 or (d[1] == 0 and d[2] < 0))):
                d = [-c for c in d]
            a = list(p)
            while True:
                b = [a[k] - d[k] for k in range(3)]
                if min(b) < 0 or max(b) > 3:
                    break
                a = b
            key = (a[0], a[1], a[2], d[0], d[1], d[2])
            if key in seen:
                continue
            seen.add(key)
            pts = []
            c = list(a)
            while min(c) >= 0 and max(c) <= 3:
                pts.append(tuple(c))
                c = [c[k] + d[k] for k in range(3)]
            lines.append({"a": tuple(a), "d": tuple(d), "n": len(pts), "points": pts})
    return lines


LINES = build_lines()


def line_point(li: int, s: Q) -> Point:
    ln = LINES[li]
    return tuple(Q(ln["a"][k]) + s * ln["d"][k] for k in range(3))  # type: ignore[return-value]


def find_line(p: Iterable[int], q: Iterable[int]) -> tuple[int, int, int]:
    p = tuple(p)
    q = tuple(q)
    for li, ln in enumerate(LINES):
        if p in ln["points"] and q in ln["points"]:
            kp = ln["points"].index(p)
            kq = ln["points"].index(q)
            return li, kp, (1 if kq > kp else -1)
    raise ValueError(f"no lattice line through {p} {q}")


def qparse(s: str) -> Q:
    return Q(s)


def sub(a: Point, b: Point) -> Point:
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def add(a: Point, b: Point) -> Point:
    return (a[0] + b[0], a[1] + b[1], a[2] + b[2])


def scale(a: Point, t: Q) -> Point:
    return (a[0] * t, a[1] * t, a[2] * t)


def dot(a: Point, b: Point) -> Q:
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def cross(a: Point, b: Point) -> Point:
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


def meet(A: Point, u: Point, B: Point, v: Point) -> tuple[Q, Q] | None:
    n = cross(u, v)
    if n == (0, 0, 0):
        return None
    w = sub(B, A)
    if dot(w, n) != 0:
        return None
    nn = dot(n, n)
    return dot(cross(w, v), n) / nn, dot(cross(w, u), n) / nn


def tparam(li: int, pbit: int, mi: int, s: Q) -> tuple[Q, Point, Point] | None:
    A = line_point(li, Q(0))
    d = tuple(Q(c) for c in LINES[li]["d"])
    X = add(A, scale(d, s))  # type: ignore[arg-type]
    p = tuple(Q(c) for c in bit_point(pbit))
    u = sub(p, X)  # type: ignore[arg-type]
    B = line_point(mi, Q(0))
    e = tuple(Q(c) for c in LINES[mi]["d"])
    r = meet(X, u, B, e)  # type: ignore[arg-type]
    if r is None:
        return None
    lam, t = r
    if lam <= 1:
        return None
    return t, X, add(X, scale(u, lam))  # type: ignore[arg-type]


def far_param(li: int, sg: int, entry: dict | None) -> Q:
    """A parameter strictly beyond every grid point ahead and beyond the entry."""
    n = LINES[li]["n"]
    if sg > 0:
        base = Q(n - 1)
        if entry is not None and not entry.get("inf", True):
            base = max(base, Q(entry["e"]))
        return base + 1
    base = Q(0)
    if entry is not None and not entry.get("inf", True):
        base = min(base, Q(entry["e"]))
    return base - 1


def behind_param(li: int, sg: int, exit_param: Q | None) -> Q:
    """A free entry parameter strictly behind every grid point and the exit."""
    n = LINES[li]["n"]
    if sg > 0:
        base = Q(0)
        if exit_param is not None:
            base = min(base, exit_param)
        return base - 1
    base = Q(n - 1)
    if exit_param is not None:
        base = max(base, exit_param)
    return base + 1


ANCHOR_FIXED = [(0, 0, 0), (3, 0, 0), (0, 3, 3)]


ANCHORS = {
    # anchor id: (suffix start corner, suffix direction point, fixed middle vertices after 000)
    4: ((0, 3, 3), (0, 0, 3), [(3, 0, 0)]),
    5: ((0, 0, 3), (3, 3, 0), [(3, 0, 0), (0, 3, 3)]),
}


def reconstruct(path: list[dict[str, Any]], total_links: int = 22, anchor: int = 5) -> list[Point]:
    """Rebuild exact vertices from an engine leaf path.

    Path semantics: suffix side starts on line x=0,z=3 at 033; moves describe how
    each link ends and the next one starts.  A SWITCH (kind 7) or ENDT (kind 6)
    on the suffix side ends the suffix and starts the prefix (space diagonal from
    000 outward).  The last move is END (5) or ENDT (6) on the prefix side.
    """
    sides: list[list[dict[str, Any]]] = [[], []]
    side = 0
    for mv in path:
        sides[side].append(mv)
        if side == 0 and mv["kind"] in (6, 7):
            side = 1
    if side != 1:
        raise ValueError("path never switched to the prefix side")
    s_corner, s_dir, middle = ANCHORS[anchor]
    suffix_line, sk, ssg = find_line(s_corner, s_dir)
    prefix_line, pk, psg = find_line((0, 0, 0), (3, 3, 3))

    def build(start_line: int, start_k: int, start_sg: int, moves: list[dict[str, Any]]) -> list[Point]:
        # Returns vertices starting at the anchor corner going outward.
        verts: list[Point] = [line_point(start_line, Q(start_k))]
        cur_line, cur_sg = start_line, start_sg
        cur_entry: dict[str, Any] | None = {"inf": False, "e": str(start_k), "closed": True}
        pending_free_entry = False  # current line entered by F/T-cell whose concrete point is not yet fixed
        pending: dict[str, Any] | None = None
        for idx, mv in enumerate(moves):
            kind = mv["kind"]
            exit_param: Q | None
            if kind == 1:  # R
                exit_param = Q(mv["s"])
            elif kind == 3:  # T exact
                exit_param = Q(mv["s"])
            elif kind == 4:  # T coplanar cell: choose concrete s later
                exit_param = None
            else:
                exit_param = None
            # fix pending entry of the current line now that the exit is known
            if pending is not None:
                verts.extend(resolve_pending(pending, cur_line, cur_sg, exit_param, mv))
                pending = None
            if kind == 1:
                verts.append(line_point(cur_line, exit_param))
                cur_line, cur_sg = mv["to"], mv["sg_to"]
                cur_entry = mv["entry"]
            elif kind == 3:
                verts.append(line_point(cur_line, exit_param))
                to = mv["to"]
                verts.append(line_point(to, Q(mv["t"])))
                cur_line, cur_sg = to, mv["sg_to"]
                cur_entry = mv["entry"]
            elif kind == 2:  # F
                verts.append(line_point(cur_line, far_param(cur_line, cur_sg, cur_entry)))
                pending = {"type": "F"}
                cur_line, cur_sg = mv["to"], mv["sg_to"]
                cur_entry = {"inf": True}
            elif kind == 4:  # coplanar T cell
                pending = {"type": "TC", "mv": mv, "from": cur_line}
                cur_line, cur_sg = mv["to"], mv["sg_to"]
                cur_entry = mv["entry"]
            elif kind in (5, 7):  # end of side: free exit
                verts.append(line_point(cur_line, far_param(cur_line, cur_sg, cur_entry)))
                return verts
            elif kind == 6:  # end-T through p
                X = line_point(cur_line, far_param(cur_line, cur_sg, cur_entry))
                verts.append(X)
                p = tuple(Q(c) for c in bit_point(mv["p"]))
                verts.append(add(p, sub(p, X)))  # type: ignore[arg-type]
                return verts
            else:
                raise ValueError(f"unexpected move kind {kind}")
        raise ValueError("side ended without END/SWITCH")

    def resolve_pending(pending: dict[str, Any], line: int, sg: int, exit_param: Q | None, nextmv: dict[str, Any]) -> list[Point]:
        if pending["type"] == "F":
            return [line_point(line, behind_param(line, sg, exit_param))]
        mv = pending["mv"]
        frm = pending["from"]
        lo = None if mv["lo_inf"] else Q(mv["lo"])
        hi = None if mv["hi_inf"] else Q(mv["hi"])
        # candidate s values inside the open cell approaching the endpoint whose image is the entry bound
        rep = Q(mv["s"])
        cands = [rep]
        for end in (lo, hi):
            if end is None:
                for k in range(1, 60):
                    cands.append(rep + (Q(2) ** k) * (1 if end is hi else -1) * (1 if True else 1))
                continue
            for k in range(1, 60):
                cands.append(end + (rep - end) / (Q(2) ** k))
        for s in cands:
            if lo is not None and not s > lo:
                continue
            if hi is not None and not s < hi:
                continue
            r = tparam(frm, mv["p"], line, s)
            if r is None:
                continue
            t, X, Y = r
            if exit_param is not None and not ((exit_param - t) * sg > 0):
                continue
            # also require Y ahead of the bound semantics automatically satisfied (inside image)
            return [X, Y]
        raise ValueError("could not realise coplanar T cell")

    # fixups: the suffix/prefix exits of a pending F at the very end are handled in build
    suf = build(suffix_line, sk, ssg, sides[0])
    pre = build(prefix_line, pk, psg, sides[1])
    verts = list(reversed(pre)) + [tuple(Q(c) for c in v) for v in middle] + suf  # type: ignore[misc]
    # pad to exactly total_links nonzero links if the search used fewer
    links = len(verts) - 1
    while links < total_links:
        last = verts[-1]
        prev = verts[-2]
        d = sub(last, prev)
        # a small step in a direction not parallel to the last link
        for cand in ((Q(1, 7), Q(2, 7), Q(3, 7)), (Q(3, 7), Q(1, 7), Q(2, 7))):
            if cross(d, cand) != (0, 0, 0):
                verts.append(add(last, cand))  # type: ignore[arg-type]
                break
        links += 1
    return verts


def qs(x: Q) -> str:
    return str(x.numerator) if x.denominator == 1 else f"{x.numerator}/{x.denominator}"


def vertices_json(verts: list[Point]) -> list[list[str]]:
    return [[qs(c) for c in v] for v in verts]


def load_jsonl(path) -> list[dict[str, Any]]:
    rows = []
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows
