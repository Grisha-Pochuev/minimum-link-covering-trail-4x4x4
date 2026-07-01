from __future__ import annotations

import argparse
import importlib.util
import sys
from pathlib import Path

RICH_HELPERS_CPP = r'''
uint64_t point_mask(const Pt& p) {
    auto it = GRID_INDEX.find(p);
    if (it == GRID_INDEX.end()) return 0ULL;
    return 1ULL << it->second;
}

uint64_t points_mask(initializer_list<Pt> pts) {
    uint64_t m = 0;
    for (const auto& p : pts) m |= point_mask(p);
    return m;
}

uint64_t splitmix64(uint64_t x) {
    x += 0x9e3779b97f4a7c15ULL;
    x = (x ^ (x >> 30)) * 0xbf58476d1ce4e5b9ULL;
    x = (x ^ (x >> 27)) * 0x94d049bb133111ebULL;
    return x ^ (x >> 31);
}

uint64_t pt_code(const Pt& p) {
    uint64_t x = (uint64_t)(p.x + 1024);
    uint64_t y = (uint64_t)(p.y + 2048);
    uint64_t z = (uint64_t)(p.z + 4096);
    return (x << 42) ^ (y << 21) ^ z;
}

uint64_t state_key(uint64_t mask, int links, const Pt& last) {
    return splitmix64(mask ^ (uint64_t)links * 0x9e3779b97f4a7c15ULL ^ splitmix64(pt_code(last)));
}

uint64_t missing_family_key(uint64_t mask) {
    return FULL_MASK & ~mask;
}

int worst_wall_overlap(uint64_t mask) {
    uint64_t miss = FULL_MASK & ~mask;
    int best = 0;
    for (uint64_t w : BAD_WALL_MASKS) best = max(best, pop64(miss & w));
    return best;
}

bool is_cover_set_mode(const string& mode) {
    return mode == "new_skeleton_rich4";
}

bool is_stitch_mode(const string& mode) {
    return mode == "endpoint_feasible_stitch" || mode == "bridge_budget_compress";
}

bool is_cached_repair_mode(const string& mode) {
    return mode == "endpoint_feasible_stitch" || mode == "bridge_budget_compress" ||
           mode == "defect_spread_novelty" || mode == "seed_window_control";
}

bool is_fractional_mode(const string& mode) {
    return mode != "integer_rich_control";
}

bool is_anti_wall_mode(const string& mode) {
    return mode == "new_skeleton_rich4" || mode == "endpoint_feasible_stitch" ||
           mode == "bridge_budget_compress" || mode == "defect_spread_novelty";
}

bool is_novelty_mode(const string& mode) {
    return mode == "new_skeleton_rich4" || mode == "defect_spread_novelty";
}
'''

RICH_MODE_FOR_CPP = r'''string mode_for(int shard) {
    // 0-5: build new rich 3/4-point material before old 59 families dominate.
    if (shard < 6) return "new_skeleton_rich4";
    // 6-10: stitch only through intervals actually covered between chosen endpoints.
    if (shard < 11) return "endpoint_feasible_stitch";
    // 11-14: spend bridge budget on longer window replacements and compression.
    if (shard < 15) return "bridge_budget_compress";
    // 15-17: novelty pressure away from archived 59/64 missing-set walls.
    if (shard < 18) return "defect_spread_novelty";
    // 18: conservative old-seed window control.
    if (shard == 18) return "seed_window_control";
    // 19: integer-coordinate rich-line control.
    return "integer_rich_control";
}'''

RICH_WEIGHTS_CPP = r'''for (int i = 0; i < 64; ++i) if ((TARGET_MASK >> i) & 1ULL) POINT_WEIGHT[i] = 4.0;
    auto boost_point = [&](Pt p, double w) {
        auto it = GRID_INDEX.find(p);
        if (it != GRID_INDEX.end()) POINT_WEIGHT[it->second] = w;
    };
    // Recurring walls from runs 9-13. They remain useful targets, but the new
    // engine is judged by endpoint-feasible coverage, not by simply recreating
    // one old 59/64 family.
    boost_point({2,4,4}, 12.0); // (1,2,2)
    boost_point({2,6,2}, 12.0); // (1,3,1)
    boost_point({2,6,4}, 13.0); // (1,3,2)
    boost_point({4,0,4}, 12.0); // (2,0,2)
    boost_point({4,0,6}, 13.0); // (2,0,3)
    boost_point({2,0,2}, 11.0); // (1,0,1)
    boost_point({4,4,4}, 11.0); // (2,2,2)
    boost_point({4,2,4}, 14.0); // (2,1,2)
    boost_point({4,4,6}, 14.0); // (2,2,3)
    boost_point({6,2,0}, 11.0); // (3,1,0)
    boost_point({6,2,4}, 11.0); // (3,1,2)
    boost_point({6,2,6}, 10.0); // (3,1,3)
    boost_point({0,4,4}, 9.0);  // (0,2,2)
    boost_point({4,2,6}, 9.0);  // (2,1,3)
    boost_point({0,2,0}, 8.0);  // (0,1,0)
    boost_point({2,4,6}, 8.0);  // (1,2,3)
    boost_point({4,2,0}, 8.0);  // (2,1,0)
    BAD_WALL_MASKS.clear();
    BAD_WALL_MASKS.push_back(points_mask({{2,4,4},{2,6,2},{2,6,4},{4,0,4},{4,0,6}}));
    BAD_WALL_MASKS.push_back(points_mask({{2,0,2},{2,4,4},{2,6,4},{4,0,6},{4,4,4}}));
    BAD_WALL_MASKS.push_back(points_mask({{4,2,4},{4,4,6},{6,2,0},{6,2,4},{6,2,6}}));
    BAD_WALL_MASKS.push_back(points_mask({{0,4,4},{4,2,4},{4,4,6},{6,2,0},{6,2,4}}));
    BAD_WALL_MASKS.push_back(points_mask({{0,2,4},{2,4,2},{2,6,4},{4,2,6},{4,4,4}}));'''


def main() -> int:
    ap = argparse.ArgumentParser(description="Generate smart-search-14 rich-cover / endpoint-feasible stitch C++ engine.")
    ap.add_argument("--base-generator", default="scripts/prepare_cover_stitch_cache_engine.py")
    ap.add_argument("--source", default="cpp/repair56_search.cpp")
    ap.add_argument("--out", default="build/rich_cover_stitch_search.cpp")
    args = ap.parse_args()

    base_path = Path(args.base_generator)
    if not base_path.exists():
        raise SystemExit(f"base generator not found: {base_path}")
    spec = importlib.util.spec_from_file_location("cover_stitch_base", base_path)
    if spec is None or spec.loader is None:
        raise SystemExit(f"cannot import base generator: {base_path}")
    base = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(base)

    base.COVER_STITCH_HELPERS_CPP = RICH_HELPERS_CPP
    base.COVER_STITCH_MODE_FOR_CPP = RICH_MODE_FOR_CPP
    base.COVER_STITCH_WEIGHTS_CPP = RICH_WEIGHTS_CPP

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
    replacements = {
        "stitch_with_transposition": "endpoint_feasible_stitch",
        "bridge_compression": "bridge_budget_compress",
        "cover_set_beam_cache": "new_skeleton_rich4",
        "repair_window_cache": "bridge_budget_compress",
        "anti_wall_archive": "defect_spread_novelty",
        "novelty_56_58": "defect_spread_novelty",
        "old_59_control": "seed_window_control",
        "integer_control22": "integer_rich_control",
        "cover-stitch-cache-shard-v1": "rich-cover-stitch-shard-v1",
        "cover_stitch_cache_search parameters:": "rich_cover_stitch_search parameters:",
    }
    for a, b in replacements.items():
        text = text.replace(a, b)
    out.write_text(text)
    print(f"wrote {out} with smart-search-14 rich-cover endpoint-feasible modes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
