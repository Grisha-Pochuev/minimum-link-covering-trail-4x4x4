#!/usr/bin/env python3
"""Exact rational geometry helpers for smart-search-21 bridge compression."""
from __future__ import annotations

import hashlib
import itertools
import json
from fractions import Fraction
from pathlib import Path
from typing import Iterable, Sequence

Q = Fraction
Point = tuple[Q, Q, Q]
GRID: tuple[Point, ...] = tuple((Q(x), Q(y), Q(z)) for x in range(4) for y in range(4) for z in range(4))
GRID_INDEX = {p: i for i, p in enumerate(GRID)}


def fq(v: object) -> Q:
    if isinstance(v, Fraction):
        return v
    if isinstance(v, int):
        return Q(v)
    if isinstance(v, float):
        return Q(str(v))
    s = str(v).strip()
    return Q(s)


def point(raw: Sequence[object]) -> Point:
    if len(raw) != 3:
        raise ValueError(f"bad point {raw!r}")
    return (fq(raw[0]), fq(raw[1]), fq(raw[2]))


def qstr(x: Q) -> str:
    return str(x.numerator) if x.denominator == 1 else f"{x.numerator}/{x.denominator}"


def pjson(p: Point) -> list[str]:
    return [qstr(x) for x in p]


def sub(a: Point, b: Point) -> Point:
    return (a[0]-b[0], a[1]-b[1], a[2]-b[2])


def add(a: Point, b: Point) -> Point:
    return (a[0]+b[0], a[1]+b[1], a[2]+b[2])


def mul(a: Point, t: Q) -> Point:
    return (a[0]*t, a[1]*t, a[2]*t)


def dot(a: Point, b: Point) -> Q:
    return a[0]*b[0] + a[1]*b[1] + a[2]*b[2]


def cross(a: Point, b: Point) -> Point:
    return (a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0])


def on_segment(a: Point, b: Point, p: Point) -> bool:
    d = sub(b, a)
    if d == (Q(0), Q(0), Q(0)):
        return False
    ap = sub(p, a)
    return cross(d, ap) == (Q(0), Q(0), Q(0)) and Q(0) <= dot(ap, d) <= dot(d, d)


def segment_mask(a: Point, b: Point) -> int:
    if a == b:
        return 0
    m = 0
    for p in GRID:
        if on_segment(a, b, p):
            m |= 1 << GRID_INDEX[p]
    return m


def trail_mask(vertices: Sequence[Point]) -> int:
    m = 0
    for a, b in zip(vertices, vertices[1:]):
        m |= segment_mask(a, b)
    return m


def missing_from_mask(mask: int) -> list[list[int]]:
    return [[int(p[0]), int(p[1]), int(p[2])] for p in GRID if not ((mask >> GRID_INDEX[p]) & 1)]


def load_vertices(data: object) -> list[Point]:
    if isinstance(data, list):
        return [point(x) for x in data]
    if not isinstance(data, dict):
        raise ValueError("candidate must be a JSON object or vertex list")
    if data.get("vertices_q") is not None:
        return [point(x) for x in data["vertices_q"]]
    if data.get("vertices2") is not None:
        scale = int(data.get("coordinate_scale", 2))
        return [tuple(Q(int(c), scale) for c in raw) for raw in data["vertices2"]]
    if data.get("vertices") is not None:
        return [point(x) for x in data["vertices"]]
    raise ValueError("candidate has no vertices_q, vertices2, or vertices")


def read_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def serialize_vertices(vertices: Sequence[Point]) -> dict:
    out: dict = {"vertices_q": [pjson(p) for p in vertices]}
    den = 1
    for p in vertices:
        for x in p:
            den = den * x.denominator // __import__("math").gcd(den, x.denominator)
            if den > 2:
                break
        if den > 2:
            break
    if den <= 2:
        out["coordinate_scale"] = 2
        out["vertices2"] = [[int(x*2) for x in p] for p in vertices]
        out["vertices"] = [[int(x) if x.denominator == 1 else float(x) for x in p] for p in vertices]
    return out


def analyze(vertices: Sequence[Point], source_vertices: Sequence[Point] | None = None) -> dict:
    covered = 0
    rich4 = rich3 = productive = pure = direct_outside_hubs = 0
    gains: list[int] = []
    link_masks: list[int] = []
    link_classes: list[str] = []
    for a, b in zip(vertices, vertices[1:]):
        m = segment_mask(a, b)
        gain = (m & ~covered).bit_count()
        total = m.bit_count()
        gains.append(gain)
        link_masks.append(m)
        if total >= 4:
            rich4 += 1; cls = "rich4"
        elif total >= 3:
            rich3 += 1; cls = "rich3"
        elif gain >= 1:
            productive += 1; cls = "productive_connector"
        else:
            pure += 1; cls = "pure_bridge"
        if any(x < 0 or x > 3 for x in a) and any(x < 0 or x > 3 for x in b):
            direct_outside_hubs += 1
        link_classes.append(cls)
        covered |= m
    missing = missing_from_mask(covered)
    lost = 0
    if source_vertices:
        source_mask = trail_mask(source_vertices)
        lost = (source_mask & ~covered).bit_count()
    return {
        "links": max(0, len(vertices)-1),
        "covered_count": covered.bit_count(),
        "coverage_percent": 100.0*covered.bit_count()/64.0,
        "missing_count": len(missing),
        "missing": missing,
        "covered_mask_hex": hex(covered),
        "rich4_count": rich4,
        "rich3_count": rich3,
        "productive_connector_count": productive,
        "pure_bridge_count": pure,
        "direct_outside_hub_links": direct_outside_hubs,
        "lost_points_vs_source": lost,
        "link_gains": gains,
        "link_point_counts": [m.bit_count() for m in link_masks],
        "link_classes": link_classes,
    }


def score_tuple(row: dict) -> tuple:
    return (
        int(row.get("links") == 22 and row.get("covered_count") == 64),
        int(row.get("covered_count", 0)),
        -int(row.get("pure_bridge_count", 99)),
        int(row.get("rich4_count", 0)),
        int(row.get("productive_connector_count", 0)),
        int(row.get("rich3_count", 0)),
        int(row.get("direct_outside_hub_links", 0)),
        -int(row.get("lost_points_vs_source", 99)),
        int(row.get("novelty_score", 0)),
    )


def fraction_key(x: Q) -> tuple[int, int]:
    return (x.numerator, x.denominator)


def raw_path_key(vertices: Sequence[Point]) -> str:
    payload = [[fraction_key(x) for x in p] for p in vertices]
    return hashlib.sha256(json.dumps(payload, separators=(",", ":")).encode()).hexdigest()


def symmetry_variants(vertices: Sequence[Point]) -> Iterable[tuple[Point, ...]]:
    for perm in itertools.permutations(range(3)):
        for flips in itertools.product((False, True), repeat=3):
            transformed = []
            for p in vertices:
                q = []
                for j in range(3):
                    v = p[perm[j]]
                    q.append(Q(3)-v if flips[j] else v)
                transformed.append(tuple(q))
            yield tuple(transformed)


def canonical_path_key(vertices: Sequence[Point]) -> str:
    best: str | None = None
    for base in (tuple(vertices), tuple(reversed(vertices))):
        for variant in symmetry_variants(base):
            s = json.dumps([[qstr(x) for x in p] for p in variant], separators=(",", ":"))
            if best is None or s < best:
                best = s
    return hashlib.sha256((best or "").encode()).hexdigest()


def trail_row(vertices: Sequence[Point], *, source: str, mode: str, source_vertices: Sequence[Point] | None = None, extra: dict | None = None) -> dict:
    row = {
        "schema": "bridge-compress-candidate-v1",
        "source_candidate": source,
        "mode": mode,
        **serialize_vertices(vertices),
        **analyze(vertices, source_vertices),
    }
    row["raw_path_key_sha256"] = raw_path_key(vertices)
    row["canonical_key_sha256"] = canonical_path_key(vertices)
    row["candidate_id"] = "mlct22-bc-" + row["raw_path_key_sha256"][:16]
    if extra:
        row.update(extra)
    return row


def atomic_json(path: Path, obj: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(obj, indent=2, sort_keys=True), encoding="utf-8")
    tmp.replace(path)


def line_intersection(a: Point, b: Point, c: Point, d: Point) -> Point | None:
    u, v, w = sub(b, a), sub(d, c), sub(c, a)
    uxv = cross(u, v)
    if uxv == (Q(0), Q(0), Q(0)):
        return None
    if dot(w, uxv) != 0:
        return None
    axes = ((0, 1), (0, 2), (1, 2))
    for i, j in axes:
        det = u[j]*v[i] - u[i]*v[j]
        if det != 0:
            t = (w[j]*v[i] - w[i]*v[j]) / det
            p = add(a, mul(u, t))
            if cross(sub(p, c), v) == (Q(0), Q(0), Q(0)):
                return p
    return None
