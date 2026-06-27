from __future__ import annotations

from fractions import Fraction
from itertools import permutations, product
from typing import Any, Iterable


def _as_fraction(value: Any) -> Fraction:
    """Convert JSON numeric coordinates to an exact comparable value."""
    return Fraction(str(value))


def _format_fraction(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def _candidate_vertices_and_cube_max(record: dict[str, Any]) -> tuple[list[list[Any]], Fraction]:
    """Return candidate vertices and the cube maximum used by coordinate reflections.

    `vertices2` is the preferred project format: ordinary grid coordinates are doubled,
    so the 4x4x4 cube is [0, 6]^3. If only `vertices` is present, assume ordinary
    coordinates and reflect around [0, 3]^3.
    """
    vertices2 = record.get("vertices2")
    if vertices2:
        return vertices2, Fraction(6)
    vertices = record.get("vertices") or []
    return vertices, Fraction(3)


def canonical_path_key(record: dict[str, Any]) -> str:
    """Canonical key modulo cube symmetries and trail reversal.

    Two candidates get the same key if one can be turned into the other by:
    - permuting x/y/z axes;
    - reflecting any coordinate across the cube;
    - reversing the order of the trail vertices.

    This is intentionally based on the trail vertices, not on the candidate id or run id.
    """
    raw_vertices, cube_max = _candidate_vertices_and_cube_max(record)
    if not raw_vertices:
        return ""

    vertices = tuple(tuple(_as_fraction(coord) for coord in point) for point in raw_vertices)
    if any(len(point) != 3 for point in vertices):
        return ""

    best: str | None = None
    for perm in permutations((0, 1, 2)):
        for flips in product((False, True), repeat=3):
            transformed = []
            for point in vertices:
                new_point = []
                for out_axis, src_axis in enumerate(perm):
                    value = point[src_axis]
                    if flips[out_axis]:
                        value = cube_max - value
                    new_point.append(value)
                transformed.append(tuple(new_point))

            for candidate in (tuple(transformed), tuple(reversed(transformed))):
                key = ";".join(
                    ",".join(_format_fraction(coord) for coord in point)
                    for point in candidate
                )
                if best is None or key < best:
                    best = key

    return best or ""


def has_usable_vertices(record: dict[str, Any]) -> bool:
    vertices, _ = _candidate_vertices_and_cube_max(record)
    return bool(vertices)


def inferred_links(record: dict[str, Any]) -> int | None:
    links = record.get("links")
    if links is not None:
        try:
            return int(links)
        except (TypeError, ValueError):
            return None
    vertices, _ = _candidate_vertices_and_cube_max(record)
    if vertices:
        return max(0, len(vertices) - 1)
    return None
