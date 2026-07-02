from __future__ import annotations

import argparse
import importlib.util
import re
import sys
from pathlib import Path

MODE_REPLACEMENTS = {
    "new_skeleton_rich4": "local60_lns",
    "endpoint_feasible_stitch": "rich_line_transition",
    "bridge_budget_compress": "weak_bridge_surgery",
    "defect_spread_novelty": "missing4_pressure",
    "integer_rich_control": "integer_line_control",
    "seed_window_control": "old59_vs_60_control",
    "rich-cover-stitch-shard-v1": "rich-line-transition-shard-v1",
    "rich_cover_stitch_search parameters:": "rich_line_transition_search parameters:",
}

MODE_FOR_CPP = r"""string mode_for(int shard) {
    // 0-4: large-neighborhood search around the local 60/64 seed.
    if (shard < 5) return "local60_lns";
    // 5-8: rich-line transition walks, still using real stitched segment coverage.
    if (shard < 9) return "rich_line_transition";
    // 9-12: direct pressure on the four holes of the local 60/64 seed.
    if (shard < 13) return "missing4_pressure";
    // 13-15: weak bridge surgery; allow weak links if they connect rich material.
    if (shard < 16) return "weak_bridge_surgery";
    // 16-17: novelty pressure away from old 59/64 missing-set walls.
    if (shard < 18) return "missing4_pressure";
    // 18: conservative integer-coordinate line control.
    if (shard == 18) return "integer_line_control";
    // 19: old-family control, but now the 60/64 local seed is in the bank.
    return "old59_vs_60_control";
}"""

LOCAL60_PATCH = r"""    // smart-search-15 local 60/64 seed holes.
    // These four points are missing from mlct22-3cf45a2e21fe611c.
    boost_point({0,0,2}, 24.0); // (0,0,1)
    boost_point({0,4,6}, 24.0); // (0,2,3)
    boost_point({0,6,2}, 24.0); // (0,3,1)
    boost_point({4,2,2}, 24.0); // (2,1,1)
    BAD_WALL_MASKS.push_back(points_mask({{0,0,2},{0,4,6},{0,6,2},{4,2,2}}));"""

DEFECTS_CPP = (
    "vector<Pt> defects = {{0,0,2},{0,4,6},{0,6,2},{4,2,2},"
    "{2,4,4},{4,0,4},{4,0,6},{6,2,4},{6,2,6},{0,2,4},"
    "{2,4,2},{2,6,4},{4,2,4},{4,4,6},{4,4,4}};"
)


def replace_once(text: str, pattern: str, repl: str, label: str, flags: int = 0) -> str:
    text2, n = re.subn(pattern, repl, text, count=1, flags=flags)
    if n != 1:
        raise SystemExit(f"Could not replace {label}; replacements={n}")
    return text2


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Generate smart-search-15 rich-line transition engine around the local 60/64 seed."
    )
    ap.add_argument("--base-generator", default="scripts/prepare_rich_cover_stitch_engine.py")
    ap.add_argument("--source", default="cpp/repair56_search.cpp")
    ap.add_argument("--out", default="build/rich_line_transition_search.cpp")
    args = ap.parse_args()

    base_path = Path(args.base_generator)
    if not base_path.exists():
        raise SystemExit(f"base generator not found: {base_path}")

    spec = importlib.util.spec_from_file_location("rich_cover_stitch_base", base_path)
    if spec is None or spec.loader is None:
        raise SystemExit(f"cannot import base generator: {base_path}")
    base = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(base)

    old_argv = sys.argv[:]
    try:
        sys.argv = [str(base_path), "--source", args.source, "--out", args.out]
        rc = int(base.main())
    finally:
        sys.argv = old_argv
    if rc != 0:
        return rc

    out = Path(args.out)
    text = out.read_text()

    for old, new in MODE_REPLACEMENTS.items():
        text = text.replace(old, new)

    text = replace_once(text, r"string mode_for\(int shard\) \{.*?\n\}", MODE_FOR_CPP, "mode_for", flags=re.S)

    # Make the four local-60 holes the primary target while still keeping the old
    # 59-wall pressure as secondary context.
    text = replace_once(text, r"vector<Pt> defects = \{\{[^;]+;", DEFECTS_CPP, "defects")
    marker = "BAD_WALL_MASKS.push_back(points_mask({{0,2,4},{2,4,2},{2,6,4},{4,2,6},{4,4,4}}));"
    if marker not in text:
        raise SystemExit("Could not find old bad-wall marker for local60 patch")
    text = text.replace(marker, marker + "\n" + LOCAL60_PATCH, 1)

    # Slightly widen the graph for the 60-seed neighborhood, but keep compile/runtime
    # close to the previous successful smart-search workflow.
    text = text.replace("auto adj = build_adj(V, mode, 360);", "auto adj = build_adj(V, mode, 420);")

    out.write_text(text)
    print(f"wrote {out} with smart-search-15 rich-line transition modes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
