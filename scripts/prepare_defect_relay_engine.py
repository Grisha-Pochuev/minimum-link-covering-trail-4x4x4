from __future__ import annotations

import argparse
import importlib.util
import re
import sys
from pathlib import Path

MODE_REPLACEMENTS = {
    "local60_lns": "window2_relay_from_official60",
    "rich_line_transition": "window3_relay_from_official60",
    "missing4_pressure": "relay_then_push61",
    "weak_bridge_surgery": "old59_to_relay60",
    "integer_line_control": "integer_control",
    "old59_vs_60_control": "old60_and_local_relay_control",
    "rich-line-transition-shard-v1": "defect-relay-shard-v1",
    "rich_line_transition_search parameters:": "defect_relay_search parameters:",
    "rich-line transition": "defect relay",
    "rich_line_transition": "defect_relay",
}

MODE_FOR_CPP = r'''string mode_for(int shard) {
    // 0-3: local two-internal-vertex relay around the official 60/64 seed.
    if (shard < 4) return "window2_relay_from_official60";
    // 4-7: wider local windows around the official 60/64 seed.
    if (shard < 8) return "window3_relay_from_official60";
    // 8-10: use archived 59/64 families as alternate skeleton sources.
    if (shard < 11) return "old59_to_relay60";
    // 11-13: mixed bank relay; implemented with the window2 relay scoring core.
    if (shard < 14) return "window2_relay_from_official60";
    // 14-17: first create a non-old 60-family, then try to push it to 61+.
    if (shard < 18) return "relay_then_push61";
    // 18: conservative integer-coordinate control.
    if (shard == 18) return "integer_control";
    // 19: old 60 and local relay seed control.
    return "old60_and_local_relay_control";
}'''

DEFECTS_CPP = (
    "vector<Pt> defects = {{0,0,2},{0,4,6},{0,6,2},{4,2,2},"
    "{4,4,6},{6,2,4},"
    "{2,4,4},{4,0,4},{4,0,6},{6,2,6},{4,4,4},"
    "{2,4,2},{2,6,4},{4,2,4},{4,2,6},{0,2,4}};"
)

RELAY_PATCH_CPP = r'''    // search16 defect-relay target walls.
    // Official 60/64 wall from run 28618565146:
    boost_point({0,0,2}, 30.0); // (0,0,1)
    boost_point({0,4,6}, 30.0); // (0,2,3)
    boost_point({0,6,2}, 30.0); // (0,3,1)
    boost_point({4,2,2}, 30.0); // (2,1,1)
    BAD_WALL_MASKS.push_back(points_mask({{0,0,2},{0,4,6},{0,6,2},{4,2,2}}));
    // Local relay-60 wall found in chat by a two-vertex window replacement:
    boost_point({4,4,6}, 28.0); // (2,2,3)
    boost_point({6,2,4}, 28.0); // (3,1,2)
    BAD_WALL_MASKS.push_back(points_mask({{0,0,2},{0,4,6},{4,4,6},{6,2,4}}));'''


def replace_once(text: str, pattern: str, repl: str, label: str, flags: int = 0) -> str:
    text2, n = re.subn(pattern, repl, text, count=1, flags=flags)
    if n != 1:
        raise SystemExit(f"Could not replace {label}; replacements={n}")
    return text2


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Generate smart-search-16 defect-relay C++ engine from the successful smart-search-15 generator."
    )
    ap.add_argument("--base-generator", default="scripts/prepare_rich_line_transition_engine.py")
    ap.add_argument("--source", default="cpp/repair56_search.cpp")
    ap.add_argument("--out", default="build/defect_relay_search.cpp")
    args = ap.parse_args()

    base_path = Path(args.base_generator)
    if not base_path.exists():
        raise SystemExit(f"base generator not found: {base_path}")

    spec = importlib.util.spec_from_file_location("rich_line_transition_base", base_path)
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
    text = replace_once(text, r"vector<Pt> defects = \{\{[^;]+;", DEFECTS_CPP, "defects")

    marker = "BAD_WALL_MASKS.push_back(points_mask({{0,0,2},{0,4,6},{0,6,2},{4,2,2}}));"
    if marker in text:
        text = text.replace(marker, marker + "\n" + RELAY_PATCH_CPP, 1)
    else:
        marker2 = "BAD_WALL_MASKS.push_back(points_mask({{0,2,4},{2,4,2},{2,6,4},{4,2,6},{4,4,4}}));"
        if marker2 not in text:
            raise SystemExit("Could not find a bad-wall marker for defect-relay patch")
        text = text.replace(marker2, marker2 + "\n" + RELAY_PATCH_CPP, 1)

    text = text.replace("auto adj = build_adj(V, mode, 420);", "auto adj = build_adj(V, mode, 460);")

    out.write_text(text)
    print(f"wrote {out} with smart-search-16 defect-relay modes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
