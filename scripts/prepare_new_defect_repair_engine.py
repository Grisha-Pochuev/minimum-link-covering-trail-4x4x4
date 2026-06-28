from __future__ import annotations

import argparse
import re
from pathlib import Path

# smart-search-9-new-defect-repair targets the wall exposed by run 28304497479.
# smart-search-8 reached 59/64 in all 20 shard-best candidates, but no shard
# reached 60/64. It suppressed the old hard point (3,1,3) to 2/20 and exposed
# two new dominant defect families.
#
# Pattern A, 11/20 in run 28304497479:
#   (0,2,2), (2,1,3), (2,2,3), (3,1,0), (3,1,2)
# Pattern B, 7/20 in run 28304497479:
#   (1,0,1), (1,2,2), (1,3,2), (2,0,3), (2,2,2)
# Pattern C/control, 2/20 in run 28304497479:
#   (1,2,1), (2,1,2), (2,2,3), (3,1,0), (3,1,3)
#
# Coordinate scale is 2 in the C++ engine.
NEW_DEFECTS_CPP = "vector<Pt> defects = {{0,4,4},{4,2,6},{4,4,6},{6,2,0},{6,2,4},{2,0,2},{2,4,4},{2,6,4},{4,0,6},{4,4,4},{2,4,2},{4,2,4},{6,2,6},{0,2,0},{2,4,6},{4,2,0},{6,2,2},{4,0,4}};"

NEW_DEFECT_MODE_FOR_CPP = r'''string mode_for(int shard) {
    // More budget goes to local transition repair. Keep a control tail so that
    // the smoke-test shows whether integer/rich-segment variants still compete.
    if (shard < 4) return "transition_penalty22";
    if (shard < 8) return "fractional_bridge22";
    if (shard < 12) return "subcube_stitch22";
    if (shard < 16) return "repair56_target8";
    if (shard < 18) return "rich_segment_catalog";
    return "integer_control22";
}'''

NEW_DEFECT_WEIGHT_CPP = r'''for (int i = 0; i < 64; ++i) if ((TARGET_MASK >> i) & 1ULL) POINT_WEIGHT[i] = 5.0;
    auto boost_point = [&](Pt p, double w) {
        auto it = GRID_INDEX.find(p);
        if (it != GRID_INDEX.end()) POINT_WEIGHT[it->second] = w;
    };
    // New dominant A/B wall from smart-search-8. These two appeared in 13/20.
    boost_point({4,4,6}, 17.0); // (2,2,3), A and C
    boost_point({6,2,0}, 17.0); // (3,1,0), A and C
    // Pattern A, 11/20. This is the main target.
    boost_point({0,4,4}, 14.0); // (0,2,2)
    boost_point({4,2,6}, 14.0); // (2,1,3)
    boost_point({6,2,4}, 14.0); // (3,1,2)
    // Pattern B, 7/20. Force diversity instead of only chasing A.
    boost_point({2,0,2}, 12.0); // (1,0,1)
    boost_point({2,4,4}, 12.0); // (1,2,2)
    boost_point({2,6,4}, 12.0); // (1,3,2)
    boost_point({4,0,6}, 12.0); // (2,0,3)
    boost_point({4,4,4}, 12.0); // (2,2,2)
    // Pattern C and previous core5 controls.
    boost_point({2,4,2}, 9.0);  // (1,2,1)
    boost_point({4,2,4}, 9.0);  // (2,1,2)
    boost_point({6,2,6}, 8.0);  // (3,1,3), control only, not the sole center
    boost_point({0,2,0}, 7.0);  // (0,1,0), previous selected best defect
    boost_point({2,4,6}, 7.0);  // (1,2,3), previous selected best defect
    boost_point({4,2,0}, 7.0);  // (2,1,0), previous selected best defect
    boost_point({6,2,2}, 7.0);  // (3,1,1), previous selected best defect
    boost_point({4,0,4}, 7.0);  // (2,0,2), old 59/64 defect control'''


def replace_once(text: str, pattern: str, repl: str, label: str, flags: int = 0) -> str:
    text2, n = re.subn(pattern, repl, text, count=1, flags=flags)
    if n != 1:
        raise SystemExit(f"Could not replace {label}")
    return text2


def main() -> int:
    ap = argparse.ArgumentParser(description="Generate a new-defect repair engine for smart-search-9-new-defect-repair.")
    ap.add_argument("--source", default="cpp/repair56_search.cpp")
    ap.add_argument("--out", default="build/new_defect_repair_search.cpp")
    args = ap.parse_args()

    src = Path(args.source)
    out = Path(args.out)
    text = src.read_text()

    text = replace_once(text, r"vector<Pt> defects = \{\{[^;]+;", NEW_DEFECTS_CPP, "new-defect defect list")
    text = replace_once(text, r"string mode_for\(int shard\) \{.*?\n\}", NEW_DEFECT_MODE_FOR_CPP, "new-defect mode_for", flags=re.S)
    text = replace_once(
        text,
        r"for \(int i = 0; i < 64; \+\+i\) if \(\(TARGET_MASK >> i\) & 1ULL\) POINT_WEIGHT\[i\] = 6\.0;",
        NEW_DEFECT_WEIGHT_CPP,
        "new-defect point weights",
    )

    # Keep more seed memory because we now have several distinct 59/64 families.
    text = text.replace("if (seeds.size() > 256) seeds.resize(256);", "if (seeds.size() > 4096) seeds.resize(4096);")

    # Strongly prefer 59/64 material, but keep 56/57/58 as scaffolding.
    text = text.replace(
        "for (auto& s : seeds) sw.push_back(pow(max(1, s.covered - 39), 2.0));",
        "for (auto& s : seeds) sw.push_back(pow(max(1, s.covered - 52), 4.5));",
    )

    # Larger surgery window: 59/64 appears stable, so the next jump likely needs
    # a multi-segment bridge swap rather than a tiny two-link mutation.
    text = text.replace("int minK = 2, maxK = min(6, L);", "int minK = 4, maxK = min(12, L);")

    # Spend almost all effort on surgery from known strong seeds.
    text = text.replace("(rng() % 100) < 88", "(rng() % 100) < 98")

    text = text.replace("repair56_search parameters:", "new_defect_repair_search parameters:")
    text = text.replace(r'\"schema\": \"repair-mlct-shard-v1\"', r'\"schema\": \"repair59-new-defect-shard-v1\"')

    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(text)
    print(f"wrote {out} with smart-search-9-new-defect targets, weights, and repair distribution")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
