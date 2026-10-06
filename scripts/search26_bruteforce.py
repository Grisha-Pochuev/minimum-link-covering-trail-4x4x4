#!/usr/bin/env python3
"""Independent unpruned reference enumeration of the search-26 contact model.

Used only by the preflight on tiny link budgets: it enumerates every trail of
the anchored class without any bound and reports the exact maximum coverage.
The C++ engine must reproduce that maximum exactly when its admissible bound is
active (target = max succeeds, target = max + 1 finds nothing).  This guards
against an inadmissible bound silently turning into a false negative.

Independent of the engine: own line enumeration (via search26_common lines but
own intersection/coverage code), Fraction arithmetic only.
"""
from __future__ import annotations

import argparse
import json
from fractions import Fraction as Q

from search26_common import LINES, ANCHORS, find_line


def meet_params(li: int, mj: int):
    a = LINES[li]["a"]; d = LINES[li]["d"]; b = LINES[mj]["a"]; e = LINES[mj]["d"]
    n = (d[1] * e[2] - d[2] * e[1], d[2] * e[0] - d[0] * e[2], d[0] * e[1] - d[1] * e[0])
    if n == (0, 0, 0):
        return None
    w = (b[0] - a[0], b[1] - a[1], b[2] - a[2])
    if w[0] * n[0] + w[1] * n[1] + w[2] * n[2] != 0:
        return None
    nn = n[0] ** 2 + n[1] ** 2 + n[2] ** 2
    we = (w[1] * e[2] - w[2] * e[1], w[2] * e[0] - w[0] * e[2], w[0] * e[1] - w[1] * e[0])
    wd = (w[1] * d[2] - w[2] * d[1], w[2] * d[0] - w[0] * d[2], w[0] * d[1] - w[1] * d[0])
    s = Q(we[0] * n[0] + we[1] * n[1] + we[2] * n[2], nn)
    t = Q(wd[0] * n[0] + wd[1] * n[1] + wd[2] * n[2], nn)
    return s, t


def bitmask(pt) -> int:
    return 1 << (pt[0] * 16 + pt[1] * 4 + pt[2])


def cov(li: int, sg: int, entry, exitp) -> int:
    """entry/exitp: None = infinite (free); else Fraction param (closed)."""
    m = 0
    for k, pt in enumerate(LINES[li]["points"]):
        if entry is not None and (Q(k) - entry) * sg < 0:
            continue
        if exitp is not None and (exitp - Q(k)) * sg < 0:
            continue
        m |= bitmask(pt)
    return m


def run(anchor: int, links: int, w2: int, kmax: int, allow_rich_only: bool) -> int:
    allowed = [i for i, ln in enumerate(LINES) if ln["n"] >= 3 or w2 > 0]
    adj = {}
    for i in allowed:
        lst = []
        for j in allowed:
            if i == j:
                continue
            r = meet_params(i, j)
            if r is not None:
                lst.append((j, r[0], r[1]))
        adj[i] = lst
    s_corner, s_dir, middle = ANCHORS[anchor]
    sl, sk, ssg = find_line(s_corner, s_dir)
    pl, pk, psg = find_line((0, 0, 0), (3, 3, 3))
    # anchor fixed coverage
    fixed_vertices = [(0, 0, 0)] + middle + [s_corner]
    C0 = 0
    for a, b in zip(fixed_vertices, fixed_vertices[1:]):
        li, ka, sga = find_line(a, b)
        kb = LINES[li]["points"].index(tuple(b))
        lo, hi = min(ka, kb), max(ka, kb)
        for k in range(lo, hi + 1):
            C0 |= bitmask(LINES[li]["points"][k])
    fixed_links = len(fixed_vertices) - 1
    best = 0

    def side(line, sg, entry, C, used, w2u, ku, prev_nl, phase):
        nonlocal best
        # end this side (free exit)
        Cend = C | cov(line, sg, entry, None)
        if phase == 0:
            if used + 1 <= links:
                side(pl, psg, Q(pk), Cend, used + 1, w2u, ku, False, 1)
        else:
            c = bin(Cend).count("1")
            if c > best:
                best = c
        if used >= links:
            return
        for (m, s, t) in adj[line]:
            if entry is not None and (s - entry) * sg <= 0:
                continue
            nw = w2u + (1 if LINES[m]["n"] == 2 else 0)
            if nw > w2:
                continue
            C2 = C | cov(line, sg, entry, s)
            for sg2 in (-1, 1):
                side(m, sg2, t, C2, used + 1, nw, ku, False, phase)
        if ku < kmax and used + 2 <= links:
            C2 = C | cov(line, sg, entry, None)
            for m in allowed:
                if m == line:
                    continue
                nw = w2u + (1 if LINES[m]["n"] == 2 else 0)
                if nw > w2:
                    continue
                for sg2 in (-1, 1):
                    side(m, sg2, None, C2, used + 2, nw, ku + 1, True, phase)

    side(sl, ssg, Q(sk), C0, fixed_links + 1, 0, 0, False, 0)
    return best


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--anchor", type=int, default=5)
    ap.add_argument("--links", type=int, required=True)
    ap.add_argument("--w2", type=int, default=0)
    ap.add_argument("--k", type=int, default=0)
    args = ap.parse_args()
    best = run(args.anchor, args.links, args.w2, args.k, True)
    print(json.dumps({"anchor": args.anchor, "links": args.links, "w2": args.w2, "k": args.k, "max_model_covered": best}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
