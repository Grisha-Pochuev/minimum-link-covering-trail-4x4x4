#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import math
from collections import Counter
from pathlib import Path
from typing import Iterable

Point = tuple[int, int, int]
LineKey = tuple[int, int, int, int, int, int]

REQUIRED_FAMILY_IDS = [
    "mlct22-er-1b9d545440a3ee2b",
    "mlct22-er-44b7464ef2bba268",
    "mlct22-er-763db4ef21aeba80",
    "mlct22-er-7671ee46bd711a25",
    "mlct22-er-592cdba87b09cf5e",
    "mlct22-er-84b471c2367a34e7",
    "mlct22-er-579fc6ba3b315bf0",
]
REQUIRED_DONOR_IDS = [
    "mlct22-er-7617f3333d5bd4a7",
    "mlct22-er-222e6539aa735a14",
    "mlct22-er-8636131b79055dbe",
    "mlct22-er-6ea2d43af05081b7",
    "mlct22-er-cf89ed8c63871970",
]


def load_jsonl(paths: Iterable[Path]) -> list[dict]:
    rows: list[dict] = []
    for path in paths:
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                rows.append(json.loads(line))
    return rows


def primitive_direction(a: Point, b: Point) -> Point:
    d = [b[i] - a[i] for i in range(3)]
    g = math.gcd(math.gcd(abs(d[0]), abs(d[1])), abs(d[2]))
    if g == 0:
        raise ValueError("zero-length segment")
    d = [x // g for x in d]
    for x in d:
        if x:
            if x < 0:
                d = [-v for v in d]
            break
    return tuple(d)


def line_key(a: Point, b: Point) -> LineKey:
    dx, dy, dz = primitive_direction(a, b)
    x, y, z = a
    cx = y * dz - z * dy
    cy = z * dx - x * dz
    cz = x * dy - y * dx
    return dx, dy, dz, cx, cy, cz


def row_lines(row: dict) -> set[LineKey]:
    vertices = [tuple(map(int, p)) for p in row["vertices2"]]
    if len(vertices) != 23:
        raise ValueError(f"{row['candidate_id']}: expected 23 vertices")
    return {line_key(vertices[i], vertices[i + 1]) for i in range(22)}


def mask_for_segment(a: Point, b: Point) -> int:
    vx, vy, vz = (b[i] - a[i] for i in range(3))
    norm = vx * vx + vy * vy + vz * vz
    if norm == 0:
        return 0
    mask = 0
    idx = 0
    for x in range(4):
        for y in range(4):
            for z in range(4):
                p = (2 * x, 2 * y, 2 * z)
                wx, wy, wz = (p[i] - a[i] for i in range(3))
                cross = (
                    wy * vz - wz * vy,
                    wz * vx - wx * vz,
                    wx * vy - wy * vx,
                )
                dot = wx * vx + wy * vy + wz * vz
                if cross == (0, 0, 0) and 0 <= dot <= norm:
                    mask |= 1 << idx
                idx += 1
    return mask


def write_tsv(path: Path, kind: str, rows: list[dict]) -> None:
    with path.open("w", encoding="utf-8") as fh:
        for row in rows:
            vertices = ";".join(",".join(str(int(v)) for v in p) for p in row["vertices2"])
            missing = ";".join(",".join(str(int(v)) for v in p) for p in row.get("missing", []))
            fh.write("\t".join([kind, row["candidate_id"], str(int(row["covered_count"])), missing, vertices]) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", default=".")
    parser.add_argument("--outdir", default="build/search23")
    args = parser.parse_args()

    repo = Path(args.repo)
    out = repo / args.outdir
    out.mkdir(parents=True, exist_ok=True)

    parent_paths = sorted((repo / "data/search23_verified62_seed_parts").glob("part-*.jsonlpart"))
    if not parent_paths:
        raise SystemExit("no search23 parent seed parts found")
    parents = load_jsonl(parent_paths)
    donors = load_jsonl([repo / "data/search23_core_diverse_donors.jsonl"])

    if len(parents) != 1053:
        raise AssertionError(f"expected 1053 parents, got {len(parents)}")
    if any(int(r["covered_count"]) != 62 for r in parents):
        raise AssertionError("all parents must be 62/64")

    by_id = {r["candidate_id"]: r for r in parents + donors}
    missing_required = [x for x in REQUIRED_FAMILY_IDS + REQUIRED_DONOR_IDS if x not in by_id]
    if missing_required:
        raise AssertionError(f"missing required seed ids: {missing_required}")

    counts: Counter[LineKey] = Counter()
    for row in parents:
        counts.update(row_lines(row))
    core = sorted(k for k, count in counts.items() if count == len(parents))
    if len(core) != 18:
        raise AssertionError(f"expected frozen core of 18 lines, got {len(core)}")

    core_mask = 0
    representative = parents[0]
    verts = [tuple(map(int, p)) for p in representative["vertices2"]]
    rep_map = {line_key(verts[i], verts[i + 1]): (verts[i], verts[i + 1]) for i in range(22)}
    for key in core:
        a, b = rep_map[key]
        core_mask |= mask_for_segment(a, b)
    if core_mask.bit_count() != 58:
        raise AssertionError(f"expected core coverage 58, got {core_mask.bit_count()}")

    residual = []
    idx = 0
    for x in range(4):
        for y in range(4):
            for z in range(4):
                if not (core_mask >> idx) & 1:
                    residual.append([x, y, z])
                idx += 1
    expected_residual = [[0, 2, 1], [1, 2, 1], [1, 3, 1], [2, 1, 2], [2, 3, 1], [3, 3, 1]]
    if residual != expected_residual:
        raise AssertionError(f"unexpected residual set: {residual}")

    parent_reps = [by_id[x] for x in REQUIRED_FAMILY_IDS]
    donor_reps = [by_id[x] for x in REQUIRED_DONOR_IDS]

    write_tsv(out / "parents.tsv", "P", parents)
    write_tsv(out / "family_representatives.tsv", "R", parent_reps)
    write_tsv(out / "donors.tsv", "D", donor_reps)
    with (out / "frozen_core.tsv").open("w", encoding="utf-8") as fh:
        for key in core:
            fh.write("\t".join(map(str, key)) + "\n")

    manifest = {
        "schema": "search23-seed-manifest-v1",
        "parent_count": len(parents),
        "family_representative_count": len(parent_reps),
        "donor_count": len(donor_reps),
        "frozen_core_line_count": len(core),
        "frozen_core_coverage": core_mask.bit_count(),
        "frozen_core_mask_hex": f"0x{core_mask:016x}",
        "residual_points": residual,
        "required_family_ids": REQUIRED_FAMILY_IDS,
        "required_donor_ids": REQUIRED_DONOR_IDS,
        "donor_coverage": {r["candidate_id"]: int(r["covered_count"]) for r in donor_reps},
    }
    (out / "seed_manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
