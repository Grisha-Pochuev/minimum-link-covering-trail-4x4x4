from __future__ import annotations

import argparse
import re
from pathlib import Path

# smart-search-8-orbit-bridge targets the relationship between distinct 59/64
# defect orbits, not just one 5-point missing set.
#
# Old selected 59/64 best from run 28275850889 missed:
#   (1,2,2), (2,0,2), (2,0,3), (3,1,2), (3,1,3)
# New selected 59/64 best from run 28292425390 missed:
#   (0,1,0), (1,2,3), (2,1,0), (3,1,1), (3,1,3)
# Latest dominant 13/20 pattern missed:
#   (1,2,1), (2,1,2), (2,2,3), (3,1,0), (3,1,3)
#
# Coordinate scale is 2 in the C++ engine.
ORBIT_BRIDGE_DEFECTS_CPP = "vector<Pt> defects = {{6,2,6},{6,2,0},{6,2,2},{6,2,4},{2,4,4},{4,0,4},{4,0,6},{0,2,0},{2,4,6},{4,2,0},{2,4,2},{4,2,4},{4,4,6}};"

ORBIT_BRIDGE_MODE_FOR_CPP = r'''string mode_for(int shard) {
    // The previous core5 recipe saturated at 59/64 in every mode.
    // Allocate most budget to transition/fractional/subcube repair, while keeping
    // a small integer/rich-segment control tail.
    if (shard < 5) return "transition_penalty22";
    if (shard < 10) return "fractional_bridge22";
    if (shard < 15) return "subcube_stitch22";
    if (shard < 18) return "repair56_target8";
    if (shard == 18) return "rich_segment_catalog";
    return "integer_control22";
}'''

ORBIT_BRIDGE_WEIGHT_CPP = r'''for (int i = 0; i < 64; ++i) if ((TARGET_MASK >> i) & 1ULL) POINT_WEIGHT[i] = 5.0;
    auto boost_point = [&](Pt p, double w) {
        auto it = GRID_INDEX.find(p);
        if (it != GRID_INDEX.end()) POINT_WEIGHT[it->second] = w;
    };
    // Shared anchor: it is the only point missed by both old and new selected bests.
    boost_point({6,2,6}, 14.0); // (3,1,3)
    // x=3,y=1 transition column/near-column: repeatedly appears in the obstruction.
    boost_point({6,2,0}, 11.0); // (3,1,0)
    boost_point({6,2,2}, 11.0); // (3,1,1)
    boost_point({6,2,4}, 11.0); // (3,1,2)
    // Old 59/64 defect orbit from run 28275850889.
    boost_point({2,4,4}, 9.0);  // (1,2,2)
    boost_point({4,0,4}, 9.0);  // (2,0,2)
    boost_point({4,0,6}, 9.0);  // (2,0,3)
    // New selected 59/64 orbit from run 28292425390.
    boost_point({0,2,0}, 8.0);  // (0,1,0)
    boost_point({2,4,6}, 8.0);  // (1,2,3)
    boost_point({4,2,0}, 8.0);  // (2,1,0)
    // Latest dominant 13/20 pattern.
    boost_point({2,4,2}, 8.0);  // (1,2,1)
    boost_point({4,2,4}, 8.0);  // (2,1,2)
    boost_point({4,4,6}, 8.0);  // (2,2,3)'''


def replace_once(text: str, pattern: str, repl: str, label: str, flags: int = 0) -> str:
    text2, n = re.subn(pattern, repl, text, count=1, flags=flags)
    if n != 1:
        raise SystemExit(f"Could not replace {label}")
    return text2


def main() -> int:
    ap = argparse.ArgumentParser(description="Generate an orbit-bridge repair engine for smart-search-8-orbit-bridge.")
    ap.add_argument("--source", default="cpp/repair56_search.cpp")
    ap.add_argument("--out", default="build/orbit_bridge_search.cpp")
    args = ap.parse_args()

    src = Path(args.source)
    out = Path(args.out)
    text = src.read_text()

    text = replace_once(text, r"vector<Pt> defects = \{\{[^;]+;", ORBIT_BRIDGE_DEFECTS_CPP, "orbit-bridge defect list")
    text = replace_once(text, r"string mode_for\(int shard\) \{.*?\n\}", ORBIT_BRIDGE_MODE_FOR_CPP, "orbit-bridge mode_for", flags=re.S)
    text = replace_once(
        text,
        r"for \(int i = 0; i < 64; \+\+i\) if \(\(TARGET_MASK >> i\) & 1ULL\) POINT_WEIGHT\[i\] = 6\.0;",
        ORBIT_BRIDGE_WEIGHT_CPP,
        "orbit-bridge point weights",
    )

    # Wider seed memory: include bank, bank-additions, original shard candidates, and artifacts.
    text = text.replace("if (seeds.size() > 256) seeds.resize(256);", "if (seeds.size() > 2048) seeds.resize(2048);")

    # Strongly prefer 59/64 material, but retain 56/57/58 fallback structure.
    text = text.replace(
        "for (auto& s : seeds) sw.push_back(pow(max(1, s.covered - 39), 2.0));",
        "for (auto& s : seeds) sw.push_back(pow(max(1, s.covered - 52), 4.0));",
    )

    # Repair larger local transitions: the obstruction now looks like a bridge/transition problem.
    text = text.replace("int minK = 2, maxK = min(6, L);", "int minK = 3, maxK = min(10, L);")

    # Spend almost all effort on local surgery rather than cold starts.
    text = text.replace("(rng() % 100) < 88", "(rng() % 100) < 96")

    text = text.replace("repair56_search parameters:", "orbit_bridge_search parameters:")
    text = text.replace(r'\"schema\": \"repair-mlct-shard-v1\"', r'\"schema\": \"repair59-orbit-bridge-shard-v1\"')

    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(text)
    print(f"wrote {out} with smart-search-8-orbit-bridge targets, weights, and repair distribution")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
