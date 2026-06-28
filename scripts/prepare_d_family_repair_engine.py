from __future__ import annotations

import argparse
import re
from pathlib import Path

# smart-search-10-d-family-repair targets the wall exposed by run 28327372242.
# smart-search-9 reached 59/64 in all 20 shard-best candidates, but no shard
# reached 60/64. It moved the obstruction into a dominant D-family.
#
# Dominant D-family, 12/20 in run 28327372242:
#   (1,2,2), (1,3,1), (1,3,2), (2,0,2), (2,0,3)
# Prior A-family guardrail, 4/20 in run 28327372242 and dominant in run 28304497479:
#   (0,2,2), (2,1,3), (2,2,3), (3,1,0), (3,1,2)
# Secondary E-family, 3/20 in run 28327372242:
#   (0,0,2), (1,2,3), (2,0,1), (2,1,0), (3,1,1)
# Control family, 1/20 in run 28327372242:
#   (1,3,1), (2,1,2), (2,2,3), (3,1,0), (3,1,3)
#
# Coordinate scale is 2 in the C++ engine.
D_FAMILY_DEFECTS_CPP = "vector<Pt> defects = {{2,4,4},{2,6,2},{2,6,4},{4,0,4},{4,0,6},{0,4,4},{4,2,6},{4,4,6},{6,2,0},{6,2,4},{0,0,4},{2,4,6},{4,0,2},{4,2,0},{6,2,2},{4,2,4},{6,2,6}};"

D_FAMILY_MODE_FOR_CPP = r'''string mode_for(int shard) {
    // Most budget goes to D-family surgery. Keep rich/integer controls so that
    // a smoke-test can still reveal whether catalog/control variants compete.
    if (shard < 6) return "transition_penalty22";
    if (shard < 11) return "fractional_bridge22";
    if (shard < 14) return "subcube_stitch22";
    if (shard < 17) return "repair56_target8";
    if (shard < 19) return "rich_segment_catalog";
    return "integer_control22";
}'''

D_FAMILY_WEIGHT_CPP = r'''for (int i = 0; i < 64; ++i) if ((TARGET_MASK >> i) & 1ULL) POINT_WEIGHT[i] = 4.0;
    auto boost_point = [&](Pt p, double w) {
        auto it = GRID_INDEX.find(p);
        if (it != GRID_INDEX.end()) POINT_WEIGHT[it->second] = w;
    };
    // New D-family wall from smart-search-9. These are the primary target.
    boost_point({2,6,2}, 19.0); // (1,3,1), appeared 13/20
    boost_point({2,4,4}, 18.0); // (1,2,2), appeared 12/20
    boost_point({2,6,4}, 18.0); // (1,3,2), appeared 12/20
    boost_point({4,0,4}, 18.0); // (2,0,2), appeared 12/20
    boost_point({4,0,6}, 18.0); // (2,0,3), appeared 12/20
    // A-family guardrail: avoid simply rotating back to the old obstruction.
    boost_point({0,4,4}, 10.0); // (0,2,2)
    boost_point({4,2,6}, 10.0); // (2,1,3)
    boost_point({4,4,6}, 11.0); // (2,2,3)
    boost_point({6,2,0}, 11.0); // (3,1,0)
    boost_point({6,2,4}, 10.0); // (3,1,2)
    // E-family and controls from the local preflight.
    boost_point({0,0,4}, 8.0);  // (0,0,2)
    boost_point({2,4,6}, 8.0);  // (1,2,3)
    boost_point({4,0,2}, 8.0);  // (2,0,1)
    boost_point({4,2,0}, 8.0);  // (2,1,0)
    boost_point({6,2,2}, 8.0);  // (3,1,1)
    boost_point({4,2,4}, 7.0);  // (2,1,2)
    boost_point({6,2,6}, 7.0);  // (3,1,3), control only'''


def replace_once(text: str, pattern: str, repl: str, label: str, flags: int = 0) -> str:
    text2, n = re.subn(pattern, repl, text, count=1, flags=flags)
    if n != 1:
        raise SystemExit(f"Could not replace {label}")
    return text2


def main() -> int:
    ap = argparse.ArgumentParser(description="Generate a D-family repair engine for smart-search-10-d-family-repair.")
    ap.add_argument("--source", default="cpp/repair56_search.cpp")
    ap.add_argument("--out", default="build/d_family_repair_search.cpp")
    args = ap.parse_args()

    src = Path(args.source)
    out = Path(args.out)
    text = src.read_text()

    text = replace_once(text, r"vector<Pt> defects = \{\{[^;]+;", D_FAMILY_DEFECTS_CPP, "D-family defect list")
    text = replace_once(text, r"string mode_for\(int shard\) \{.*?\n\}", D_FAMILY_MODE_FOR_CPP, "D-family mode_for", flags=re.S)
    text = replace_once(
        text,
        r"for \(int i = 0; i < 64; \+\+i\) if \(\(TARGET_MASK >> i\) & 1ULL\) POINT_WEIGHT\[i\] = 6\.0;",
        D_FAMILY_WEIGHT_CPP,
        "D-family point weights",
    )

    # Keep broad seed memory; the frontier is now several distinct 59/64 families.
    text = text.replace("if (seeds.size() > 256) seeds.resize(256);", "if (seeds.size() > 8192) seeds.resize(8192);")

    # Strongly prefer 59/64 material while keeping 56/57/58 as scaffolding.
    text = text.replace(
        "for (auto& s : seeds) sw.push_back(pow(max(1, s.covered - 39), 2.0));",
        "for (auto& s : seeds) sw.push_back(pow(max(1, s.covered - 52), 4.8));",
    )

    # Multi-segment surgery: local preflight suggests D-family repair needs a
    # bridge swap, not another tiny two-link mutation.
    text = text.replace("int minK = 2, maxK = min(6, L);", "int minK = 4, maxK = min(12, L);")

    # Spend nearly all effort on surgery from known strong seeds.
    text = text.replace("(rng() % 100) < 88", "(rng() % 100) < 99")

    text = text.replace("repair56_search parameters:", "d_family_repair_search parameters:")
    text = text.replace(r'\"schema\": \"repair-mlct-shard-v1\"', r'\"schema\": \"repair59-d-family-shard-v1\"')

    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(text)
    print(f"wrote {out} with smart-search-10 D-family targets, weights, and repair distribution")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
