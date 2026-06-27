from __future__ import annotations

import argparse
import re
from pathlib import Path

# smart-search-7-core5 targets the stable 59/64 obstruction from run 28275850889.
# Dominant 5-point pattern, scaled by coordinate_scale=2:
#   (1,2,2), (2,0,2), (2,0,3), (3,1,0), (3,1,2)
# Close variant observed in the best fractional candidate also uses (3,1,3).
# We keep (3,1,3) as an auxiliary target so the search does not overfit only one
# tradeoff pattern.
CORE5_DEFECTS_CPP = "vector<Pt> defects = {{2,4,4},{4,0,4},{4,0,6},{6,2,0},{6,2,4},{6,2,6}};"

CORE5_MODE_FOR_CPP = r'''string mode_for(int shard) {
    // Spend most budget on transition-aware and fractional repair around the 59/64 core.
    if (shard < 6) return "transition_penalty22";
    if (shard < 12) return "fractional_bridge22";
    if (shard < 16) return "subcube_stitch22";
    if (shard < 18) return "repair56_target8";
    if (shard == 18) return "rich_segment_catalog";
    return "integer_control22";
}'''

CORE5_WEIGHT_CPP = r'''for (int i = 0; i < 64; ++i) if ((TARGET_MASK >> i) & 1ULL) POINT_WEIGHT[i] = 6.0;
    auto boost_point = [&](Pt p, double w) {
        auto it = GRID_INDEX.find(p);
        if (it != GRID_INDEX.end()) POINT_WEIGHT[it->second] = w;
    };
    // Main recurring core from 17/20 shard-best results.
    boost_point({2,4,4}, 10.0); // (1,2,2), missed in 20/20
    boost_point({4,0,4}, 8.0);  // (2,0,2)
    boost_point({4,0,6}, 8.0);  // (2,0,3)
    boost_point({6,2,0}, 8.0);  // (3,1,0)
    boost_point({6,2,4}, 8.0);  // (3,1,2)
    // Nearby swap point from the rare best fractional variant.
    boost_point({6,2,6}, 5.0);  // (3,1,3)'''


def replace_once(text: str, pattern: str, repl: str, label: str, flags: int = 0) -> str:
    text2, n = re.subn(pattern, repl, text, count=1, flags=flags)
    if n != 1:
        raise SystemExit(f"Could not replace {label}")
    return text2


def main() -> int:
    ap = argparse.ArgumentParser(description="Generate a core5 repair engine for smart-search-7-core5.")
    ap.add_argument("--source", default="cpp/repair56_search.cpp")
    ap.add_argument("--out", default="build/core5_search.cpp")
    args = ap.parse_args()

    src = Path(args.source)
    out = Path(args.out)
    text = src.read_text()

    text = replace_once(text, r"vector<Pt> defects = \{\{[^;]+;", CORE5_DEFECTS_CPP, "core5 defect list")
    text = replace_once(text, r"string mode_for\(int shard\) \{.*?\n\}", CORE5_MODE_FOR_CPP, "core5 mode_for", flags=re.S)
    text = replace_once(
        text,
        r"for \(int i = 0; i < 64; \+\+i\) if \(\(TARGET_MASK >> i\) & 1ULL\) POINT_WEIGHT\[i\] = 6\.0;",
        CORE5_WEIGHT_CPP,
        "core5 point weights",
    )

    # Use a wider seed bank now that candidates/bank.jsonl contains the 7 unique 59/64 candidates.
    text = text.replace("if (seeds.size() > 256) seeds.resize(256);", "if (seeds.size() > 1024) seeds.resize(1024);")

    # Prefer the 59/64 seeds much more strongly, while still keeping 56/57/58 memory available.
    text = text.replace(
        "for (auto& s : seeds) sw.push_back(pow(max(1, s.covered - 39), 2.0));",
        "for (auto& s : seeds) sw.push_back(pow(max(1, s.covered - 52), 3.0));",
    )

    # Try slightly larger local replacement windows around the last bad transitions.
    text = text.replace("int minK = 2, maxK = min(6, L);", "int minK = 2, maxK = min(8, L);")

    # This run is meant to repair, not restart. Increase local repair probability.
    text = text.replace("(rng() % 100) < 88", "(rng() % 100) < 94")

    text = text.replace("repair56_search parameters:", "core5_search parameters:")
    text = text.replace(r'\"schema\": \"repair-mlct-shard-v1\"', r'\"schema\": \"repair59-core5-shard-v1\"')

    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(text)
    print(f"wrote {out} with smart-search-7-core5 defect target, weights, and repair distribution")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
