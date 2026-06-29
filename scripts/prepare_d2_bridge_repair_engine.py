from __future__ import annotations

import argparse
import re
from pathlib import Path

# smart-search-11-d2-bridge-repair targets the D2 wall exposed by run 28338041580.
#
# Latest full run smart-search-10 reached 59/64 in all 20 shard-best candidates,
# but no shard reached 60/64. It moved pressure away from old D point (2,0,2)
# into a new D2-style wall:
#
# Dominant D2 wall:
#   9/20: (1,0,1), (1,2,2), (1,3,2), (2,0,3), (2,2,2)
#   7/20: (1,0,1), (1,2,1), (1,3,2), (2,0,3), (2,2,2)
#
# Guardrails:
#   old D-family from run 28327372242:
#     (1,2,2), (1,3,1), (1,3,2), (2,0,2), (2,0,3)
#   old A-family from run 28304497479:
#     (0,2,2), (2,1,3), (2,2,3), (3,1,0), (3,1,2)
#
# Local web-chat preflight after run 28338041580 tried simple swaps among existing
# shard-best vertices and did not beat 59/64. Therefore this generator widens bridge
# windows and candidate pools; it should create new D2 bridge material rather than
# merely repeat smart-search-10 with another seed.

D2_DEFECTS_CPP = "vector<Pt> defects = {{2,0,2},{2,4,4},{2,6,4},{4,0,6},{4,4,4},{2,4,2},{2,6,2},{4,0,4},{0,4,4},{4,2,6},{4,4,6},{6,2,0},{6,2,4},{0,0,4},{2,4,6},{4,0,2},{4,2,0},{6,2,2},{6,2,6}};"

D2_MODE_FOR_CPP = r'''string mode_for(int shard) {
    // 0-5: direct D2 window surgery around (1,0,1) and (2,2,2).
    if (shard < 6) return "repair56_target8";
    // 6-9: half-integer bridge search; best chance for new local connectors.
    if (shard < 10) return "fractional_bridge22";
    // 10-12: transition penalty, aimed at avoiding old A/D rotations.
    if (shard < 13) return "transition_penalty22";
    // 13-15: subcube/layer stitching with fractional vertices enabled below.
    if (shard < 16) return "subcube_stitch22";
    // 16-17: rich segment skeleton control.
    if (shard < 18) return "rich_segment_catalog";
    // 18: conservative integer-coordinate control.
    if (shard == 18) return "integer_control22";
    // 19: extra anti-rotation transition shard using the same internal mode.
    return "transition_penalty22";
}'''

D2_WEIGHT_CPP = r'''for (int i = 0; i < 64; ++i) if ((TARGET_MASK >> i) & 1ULL) POINT_WEIGHT[i] = 4.0;
    auto boost_point = [&](Pt p, double w) {
        auto it = GRID_INDEX.find(p);
        if (it != GRID_INDEX.end()) POINT_WEIGHT[it->second] = w;
    };
    // Primary D2 wall from smart-search-10. These four should be attacked hardest.
    boost_point({4,0,6}, 26.0); // (2,0,3), appeared 18/20
    boost_point({2,0,2}, 25.0); // (1,0,1), appeared 17/20
    boost_point({2,6,4}, 25.0); // (1,3,2), appeared 17/20
    boost_point({4,4,4}, 25.0); // (2,2,2), appeared 17/20
    // Variable fifth point in the two dominant D2 patterns.
    boost_point({2,4,4}, 17.0); // (1,2,2), appeared 10/20
    boost_point({2,4,2}, 15.0); // (1,2,1), appeared 7/20
    // Old D-family guardrail. Cover these so the repair does not reopen old holes.
    boost_point({2,6,2}, 12.0); // (1,3,1)
    boost_point({4,0,4}, 13.0); // (2,0,2), old D point almost eliminated in run 28338041580
    // Old A-family guardrail from orbit-bridge runs.
    boost_point({0,4,4}, 10.0); // (0,2,2)
    boost_point({4,2,6}, 10.0); // (2,1,3)
    boost_point({4,4,6}, 11.0); // (2,2,3)
    boost_point({6,2,0}, 11.0); // (3,1,0)
    boost_point({6,2,4}, 10.0); // (3,1,2)
    // Older E/control points get light pressure only.
    boost_point({0,0,4}, 7.0);  // (0,0,2)
    boost_point({2,4,6}, 7.0);  // (1,2,3)
    boost_point({4,0,2}, 7.0);  // (2,0,1)
    boost_point({4,2,0}, 7.0);  // (2,1,0)
    boost_point({6,2,2}, 7.0);  // (3,1,1)
    boost_point({6,2,6}, 6.0);  // (3,1,3)'''


def replace_once(text: str, pattern: str, repl: str, label: str, flags: int = 0) -> str:
    text2, n = re.subn(pattern, repl, text, count=1, flags=flags)
    if n != 1:
        raise SystemExit(f"Could not replace {label}; replacements={n}")
    return text2


def main() -> int:
    ap = argparse.ArgumentParser(description="Generate a D2 bridge repair engine for smart-search-11-d2-bridge-repair.")
    ap.add_argument("--source", default="cpp/repair56_search.cpp")
    ap.add_argument("--out", default="build/d2_bridge_repair_search.cpp")
    args = ap.parse_args()

    src = Path(args.source)
    out = Path(args.out)
    text = src.read_text()

    text = replace_once(text, r"vector<Pt> defects = \{\{[^;]+;", D2_DEFECTS_CPP, "D2 defect list")
    text = replace_once(text, r"string mode_for\(int shard\) \{.*?\n\}", D2_MODE_FOR_CPP, "D2 mode_for", flags=re.S)
    text = replace_once(
        text,
        r"for \(int i = 0; i < 64; \+\+i\) if \(\(TARGET_MASK >> i\) & 1ULL\) POINT_WEIGHT\[i\] = 6\.0;",
        D2_WEIGHT_CPP,
        "D2 point weights",
    )

    # Keep broad seed memory. The current frontier is not one shape but several
    # nearby 59/64 families; deleting weaker seeds too early can erase useful bridges.
    text = text.replace("if (seeds.size() > 256) seeds.resize(256);", "if (seeds.size() > 16384) seeds.resize(16384);")

    # Strongly prefer 59/64 material, while still allowing older 56/57/58 scaffolding.
    text = text.replace(
        "for (auto& s : seeds) sw.push_back(pow(max(1, s.covered - 39), 2.0));",
        "for (auto& s : seeds) sw.push_back(pow(max(1, s.covered - 52), 5.1));",
    )

    # The web-chat preflight showed that short swaps among existing vertices do not
    # beat 59/64. Use wider windows so a shard can replace a real bridge section.
    text = text.replace("int minK = 2, maxK = min(6, L);", "int minK = 5, maxK = min(14, L);")

    # Spend almost all effort on surgery from strong seeds, not cold walks.
    text = text.replace("(rng() % 100) < 88", "(rng() % 100) < 99")

    # Let subcube stitching use half-integer bridge vertices too; otherwise it mostly
    # repeats the old integer/layer obstruction.
    text = text.replace(
        'bool fractional = (mode == "fractional_bridge22" || mode == "repair56_target8" || mode == "transition_penalty22");',
        'bool fractional = (mode == "fractional_bridge22" || mode == "repair56_target8" || mode == "transition_penalty22" || mode == "subcube_stitch22");',
    )

    # Keep more outgoing choices per vertex and more bridge candidates per step.
    text = text.replace("auto adj = build_adj(V, mode, 180);", "auto adj = build_adj(V, mode, 260);")
    text = text.replace("if ((int)cands.size() > 96) break;", "if ((int)cands.size() > 192) break;")
    text = text.replace("int pool = min<int>(24, cands.size());", "int pool = min<int>(48, cands.size());")

    # Slightly raise target pressure in repair scoring.
    text = text.replace("target_gain * 9000.0", "target_gain * 12000.0")
    text = text.replace('if (mode == "transition_penalty22" && target_gain > 0) score += 5000;', 'if (mode == "transition_penalty22" && target_gain > 0) score += 7500;')
    text = text.replace('if (mode == "fractional_bridge22" && ((V[i].x|V[i].y|V[i].z|V[j].x|V[j].y|V[j].z)&1)) base += 700;', 'if (mode == "fractional_bridge22" && ((V[i].x|V[i].y|V[i].z|V[j].x|V[j].y|V[j].z)&1)) base += 1200;')

    text = text.replace("repair56_search parameters:", "d2_bridge_repair_search parameters:")
    text = text.replace(r'\"schema\": \"repair-mlct-shard-v1\"', r'\"schema\": \"repair59-d2-bridge-shard-v1\"')

    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(text)
    print(f"wrote {out} with smart-search-11 D2 bridge targets, weights, and repair distribution")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
