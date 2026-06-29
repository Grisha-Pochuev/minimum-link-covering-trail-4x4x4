from __future__ import annotations

import argparse
import re
from pathlib import Path

# smart-search-12-skeleton-diversity is deliberately broader than
# smart-search-11-d2-bridge-repair.
#
# The last full run (28378489636) again reached 59/64 in all shard-best
# candidates, but did not reach 60/64. Its useful signal was diversity:
# 16 compact representatives and a new common wall centered on:
#   (2,1,2), (2,2,3), with companions near (3,1,0), (3,1,2), (3,1,3).
#
# Hypothesis for this run:
#   The current 59/64 ceiling is not just a local D2 repair failure. The search
#   may need different 22-link skeletons and better transitions between rich
#   3/4-point segments. Therefore this generator spreads shards across fresh
#   rich skeletons, transition-graph search, diversity repair, anti-wall search,
#   cross-family search, and two controls.

SKELETON_DEFECTS_CPP = "vector<Pt> defects = {{4,2,4},{4,4,6},{6,2,0},{6,2,4},{6,2,6},{2,4,4},{2,4,2},{2,6,4},{4,0,6},{2,0,2},{4,4,4},{0,4,4},{2,6,2},{2,6,6},{4,0,4},{4,2,6},{0,0,4},{2,4,6},{4,0,2},{4,2,0},{6,2,2},{4,2,2},{0,2,0},{2,2,0},{2,0,6}};"

SKELETON_MODE_FOR_CPP = r"""bool is_rich_mode(const string& mode) {
    return mode == "fresh_rich_skeleton" || mode == "rich_segment_catalog";
}

bool is_transition_mode(const string& mode) {
    return mode == "transition_graph22" || mode == "transition_penalty22" || mode == "anti_wall22";
}

bool is_subcube_mode(const string& mode) {
    return mode == "subcube_stitch22";
}

bool is_fractional_mode(const string& mode) {
    return mode != "integer_control22";
}

bool is_fractional_bonus_mode(const string& mode) {
    return mode == "fractional_bridge22" || mode == "transition_graph22" ||
           mode == "diversity_repair22" || mode == "anti_wall22" ||
           mode == "cross_family22" || mode == "d2_control22";
}

bool is_cross_family_mode(const string& mode) {
    return mode == "cross_family22";
}

bool is_d2_control_mode(const string& mode) {
    return mode == "d2_control22";
}

bool is_repair_mode_name(const string& mode) {
    return mode == "repair56_target8" || mode == "transition_penalty22" ||
           mode == "fractional_bridge22" || mode == "subcube_stitch22" ||
           mode == "transition_graph22" || mode == "diversity_repair22" ||
           mode == "anti_wall22" || mode == "cross_family22" ||
           mode == "d2_control22";
}

string mode_for(int shard) {
    // 0-5: fresh rich-segment skeletons. These use walk attempts, not just repair.
    if (shard < 6) return "fresh_rich_skeleton";
    // 6-9: transition graph around rich segments and fractional bridge vertices.
    if (shard < 10) return "transition_graph22";
    // 10-13: mutate diverse 59/64 representatives with long bridge windows.
    if (shard < 14) return "diversity_repair22";
    // 14-16: anti-wall pressure against the repeated D/D2/A defect sets.
    if (shard < 17) return "anti_wall22";
    // 17: cross-family stitch between old A/D/D2 material and the latest run.
    if (shard == 17) return "cross_family22";
    // 18: conservative integer-coordinate control.
    if (shard == 18) return "integer_control22";
    // 19: D2-like control, so the broad run can be compared to smart-search-11.
    return "d2_control22";
}"""

SKELETON_WEIGHT_CPP = r"""for (int i = 0; i < 64; ++i) if ((TARGET_MASK >> i) & 1ULL) POINT_WEIGHT[i] = 3.0;
    auto boost_point = [&](Pt p, double w) {
        auto it = GRID_INDEX.find(p);
        if (it != GRID_INDEX.end()) POINT_WEIGHT[it->second] = w;
    };
    // New wall from smart-search-11: important, but avoid overfitting to it.
    boost_point({4,2,4}, 17.0); // (2,1,2), appeared 16/20
    boost_point({4,4,6}, 17.0); // (2,2,3), appeared 16/20
    boost_point({6,2,0}, 13.0); // (3,1,0)
    boost_point({6,2,4}, 13.0); // (3,1,2)
    boost_point({6,2,6}, 11.0); // (3,1,3)
    // D2 wall from smart-search-10 / smart-search-11 ancestors.
    boost_point({2,0,2}, 12.0); // (1,0,1)
    boost_point({2,4,2}, 11.0); // (1,2,1)
    boost_point({2,4,4}, 12.0); // (1,2,2)
    boost_point({2,6,4}, 12.0); // (1,3,2)
    boost_point({4,0,6}, 12.0); // (2,0,3)
    boost_point({4,4,4}, 12.0); // (2,2,2)
    // Older A/D/E guardrails. Keep them in view without letting them dominate.
    boost_point({0,4,4}, 9.0);  // (0,2,2)
    boost_point({2,6,2}, 9.0);  // (1,3,1)
    boost_point({4,0,4}, 9.0);  // (2,0,2)
    boost_point({4,2,6}, 9.0);  // (2,1,3)
    boost_point({0,0,4}, 7.0);  // (0,0,2)
    boost_point({2,4,6}, 7.0);  // (1,2,3)
    boost_point({4,0,2}, 7.0);  // (2,0,1)
    boost_point({4,2,0}, 7.0);  // (2,1,0)
    boost_point({6,2,2}, 7.0);  // (3,1,1)
    boost_point({4,2,2}, 6.0);  // (2,1,1)
    boost_point({0,2,0}, 6.0);  // (0,1,0)
    boost_point({2,2,0}, 6.0);  // (1,1,0)
    boost_point({2,0,6}, 6.0);  // (1,0,3)"""


def replace_once(text: str, pattern: str, repl: str, label: str, flags: int = 0) -> str:
    text2, n = re.subn(pattern, repl, text, count=1, flags=flags)
    if n != 1:
        raise SystemExit(f"Could not replace {label}; replacements={n}")
    return text2


def main() -> int:
    ap = argparse.ArgumentParser(description="Generate a broad skeleton-diversity engine for smart-search-12.")
    ap.add_argument("--source", default="cpp/repair56_search.cpp")
    ap.add_argument("--out", default="build/skeleton_diversity_search.cpp")
    args = ap.parse_args()

    src = Path(args.source)
    out = Path(args.out)
    text = src.read_text()

    text = replace_once(text, r"vector<Pt> defects = \{\{[^;]+;", SKELETON_DEFECTS_CPP, "skeleton defect list")
    text = replace_once(text, r"string mode_for\(int shard\) \{.*?\n\}", SKELETON_MODE_FOR_CPP, "skeleton mode_for", flags=re.S)
    text = replace_once(
        text,
        r"for \(int i = 0; i < 64; \+\+i\) if \(\(TARGET_MASK >> i\) & 1ULL\) POINT_WEIGHT\[i\] = 6\.0;",
        SKELETON_WEIGHT_CPP,
        "skeleton point weights",
    )

    # Keep much more seed memory because the point of this run is diversity.
    text = text.replace("if (seeds.size() > 256) seeds.resize(256);", "if (seeds.size() > 24576) seeds.resize(24576);")

    # Prefer strong material, but slightly less aggressively than D2 repair to
    # avoid selecting only one old family.
    text = text.replace(
        "for (auto& s : seeds) sw.push_back(pow(max(1, s.covered - 39), 2.0));",
        "for (auto& s : seeds) sw.push_back(pow(max(1, s.covered - 50), 3.6));",
    )

    # Long bridge surgery. The web-chat preflight did not find 60/64 via tiny swaps.
    text = text.replace("int minK = 2, maxK = min(6, L);", "int minK = 5, maxK = min(14, L);")

    # Make new named modes actually affect the inherited C++ scoring code.
    text = text.replace(
        'bool fractional = (mode == "fractional_bridge22" || mode == "repair56_target8" || mode == "transition_penalty22");',
        'bool fractional = is_fractional_mode(mode);',
    )
    text = text.replace('if (mode == "rich_segment_catalog" && hits < 3) base -= 2500;', 'if (is_rich_mode(mode) && hits < 3) base -= 3200;')
    text = text.replace('if (mode == "subcube_stitch22") {', 'if (is_subcube_mode(mode)) {')
    text = text.replace('if (mode == "fractional_bridge22" && ((V[i].x|V[i].y|V[i].z|V[j].x|V[j].y|V[j].z)&1)) base += 700;', 'if (is_fractional_bonus_mode(mode) && ((V[i].x|V[i].y|V[i].z|V[j].x|V[j].y|V[j].z)&1)) base += 1050;')

    text = text.replace('if (mode == "rich_segment_catalog" && e.hits >= 3) score += 3000;', 'if (is_rich_mode(mode) && e.hits >= 3) score += 3800;')
    text = text.replace('if (mode == "transition_penalty22" && target_gain > 0) score += 5000;', 'if (is_transition_mode(mode) && target_gain > 0) score += 6500;')
    text = text.replace('if (mode == "subcube_stitch22") score += 300 * min(4, e.hits);', 'if (is_subcube_mode(mode)) score += 300 * min(4, e.hits);')
    text = text.replace('if (mode == "rich_segment_catalog" && e.hits >= 3) score += 4000;', 'if (is_rich_mode(mode) && e.hits >= 3) score += 5200;')

    text = text.replace("auto adj = build_adj(V, mode, 180);", "auto adj = build_adj(V, mode, 320);")
    text = text.replace("if ((int)cands.size() > 96) break;", "if ((int)cands.size() > 224) break;")
    text = text.replace("int pool = min<int>(24, cands.size());", "int pool = min<int>(56, cands.size());")
    text = text.replace("if ((int)cands.size() > 128) break;", "if ((int)cands.size() > 224) break;")
    text = text.replace("int pool = min<int>(32, cands.size());", "int pool = min<int>(64, cands.size());")

    text = text.replace(
        'bool repair_mode = (mode == "repair56_target8" || mode == "transition_penalty22" || mode == "fractional_bridge22" || mode == "subcube_stitch22");\n'
        '        if (repair_mode && !seeds.empty() && (rng() % 100) < 88) p = repair_attempt(seeds, V, vidx, adj, mode, rng);',
        'bool repair_mode = is_repair_mode_name(mode);\n'
        '        int repair_chance = is_d2_control_mode(mode) ? 97 : (is_cross_family_mode(mode) ? 92 : 95);\n'
        '        if (repair_mode && !seeds.empty() && (rng() % 100) < repair_chance) p = repair_attempt(seeds, V, vidx, adj, mode, rng);',
    )

    text = text.replace("repair56_search parameters:", "skeleton_diversity_search parameters:")
    text = text.replace(r'\"schema\": \"repair-mlct-shard-v1\"', r'\"schema\": \"skeleton-diversity-shard-v1\"')

    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(text)
    print(f"wrote {out} with smart-search-12 skeleton-diversity modes and broad defect memory")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
