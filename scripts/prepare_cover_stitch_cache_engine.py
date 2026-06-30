from __future__ import annotations

import argparse
import re
from pathlib import Path

# smart-search-13-cover-stitch-cache is a deliberate move away from simply
# repairing the latest 59/64 champion. The previous skeleton-diversity run
# collapsed to one exact 59/64 family in 18/20 shard-best artifacts. This
# generator keeps the inherited C++ repair engine, but changes the search
# policy in three ways:
#
# 1. Transposition cache: reject repeated end states inside each worker.
#    A state is roughly (coverage mask, last vertex, link count). This is not
#    a proof cache; it just stops the CPU from celebrating the same curve over
#    and over.
# 2. Anti-wall archive: missing-set families that dominated previous runs are
#    treated as known traps. Shards that are supposed to be novel probabilisticly
#    reject candidates that end in those same walls unless they improve above
#    59/64.
# 3. Cover/stitch/compress modes: shards are named by the intended pressure:
#    find rich covering material, stitch it as a connected trail, repair longer
#    windows with cache pressure, and keep controls for comparison.

COVER_STITCH_HELPERS_CPP = r'''
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
    return mode == "cover_set_beam_cache";
}

bool is_stitch_mode(const string& mode) {
    return mode == "stitch_with_transposition" || mode == "bridge_compression";
}

bool is_cached_repair_mode(const string& mode) {
    return mode == "repair_window_cache" || mode == "anti_wall_archive" ||
           mode == "novelty_56_58" || mode == "old_59_control" ||
           mode == "stitch_with_transposition" || mode == "bridge_compression";
}

bool is_fractional_mode(const string& mode) {
    return mode != "integer_control22";
}

bool is_anti_wall_mode(const string& mode) {
    return mode == "anti_wall_archive" || mode == "novelty_56_58" ||
           mode == "cover_set_beam_cache" || mode == "stitch_with_transposition" ||
           mode == "repair_window_cache";
}

bool is_novelty_mode(const string& mode) {
    return mode == "novelty_56_58" || mode == "anti_wall_archive";
}
'''

COVER_STITCH_MODE_FOR_CPP = r'''string mode_for(int shard) {
    // 0-4: search rich covering material while caching repeated coverage states.
    if (shard < 5) return "cover_set_beam_cache";
    // 5-8: stitch/transition pressure with a transposition table.
    if (shard < 9) return "stitch_with_transposition";
    // 9-12: long-window repair, but avoid revisiting the same end states.
    if (shard < 13) return "repair_window_cache";
    // 13-15: strong pressure away from archived 59/64 walls.
    if (shard < 16) return "anti_wall_archive";
    // 16-17: deliberately use weaker-but-different 56-58 material.
    if (shard < 18) return "novelty_56_58";
    // 18: old 59-family control.
    if (shard == 18) return "old_59_control";
    // 19: conservative integer-coordinate control.
    return "integer_control22";
}'''

COVER_STITCH_WEIGHTS_CPP = r'''for (int i = 0; i < 64; ++i) if ((TARGET_MASK >> i) & 1ULL) POINT_WEIGHT[i] = 4.0;
    auto boost_point = [&](Pt p, double w) {
        auto it = GRID_INDEX.find(p);
        if (it != GRID_INDEX.end()) POINT_WEIGHT[it->second] = w;
    };
    // Repeated walls from runs 10-12. They are important, but must not dominate.
    boost_point({2,4,4}, 13.0); // (1,2,2)
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
    // run 12 dominant wall, 18/20 shard-best artifacts.
    BAD_WALL_MASKS.push_back(points_mask({{2,4,4},{2,6,2},{2,6,4},{4,0,4},{4,0,6}}));
    // run 10/11 D2-style walls.
    BAD_WALL_MASKS.push_back(points_mask({{2,0,2},{2,4,4},{2,6,4},{4,0,6},{4,4,4}}));
    BAD_WALL_MASKS.push_back(points_mask({{4,2,4},{4,4,6},{6,2,0},{6,2,4},{6,2,6}}));
    BAD_WALL_MASKS.push_back(points_mask({{0,4,4},{4,2,4},{4,4,6},{6,2,0},{6,2,4}}));'''


def replace_once(text: str, pattern: str, repl: str, label: str, flags: int = 0) -> str:
    text2, n = re.subn(pattern, repl, text, count=1, flags=flags)
    if n != 1:
        raise SystemExit(f"Could not replace {label}; replacements={n}")
    return text2


def main() -> int:
    ap = argparse.ArgumentParser(description="Generate cover/stitch/cache C++ engine for smart-search-13.")
    ap.add_argument("--source", default="cpp/repair56_search.cpp")
    ap.add_argument("--out", default="build/cover_stitch_cache_search.cpp")
    args = ap.parse_args()

    src = Path(args.source)
    out = Path(args.out)
    text = src.read_text()
    if "#include <initializer_list>" not in text:
        text = text.replace("#include <iomanip>\n", "#include <iomanip>\n#include <initializer_list>\n")

    # Track cache/anti-wall rejections in worker summaries.
    text = text.replace(
        "    uint64_t attempts = 0;\n    double elapsed = 0.0;",
        "    uint64_t attempts = 0;\n    uint64_t cache_rejects = 0;\n    uint64_t wall_rejects = 0;\n    double elapsed = 0.0;",
    )

    # Add wall archive globals and state-hash helpers after pop64 is declared.
    text = text.replace(
        "static vector<double> POINT_WEIGHT(64, 1.0);\n",
        "static vector<double> POINT_WEIGHT(64, 1.0);\nstatic vector<uint64_t> BAD_WALL_MASKS;\nstatic const uint64_t FULL_MASK = ~0ULL;\n",
    )
    text = text.replace(
        "static inline int pop64(uint64_t x) { return __builtin_popcountll(x); }\n",
        "static inline int pop64(uint64_t x) { return __builtin_popcountll(x); }\n" + COVER_STITCH_HELPERS_CPP + "\n",
    )

    # Keep seed memory broad, but diversity-filter it by missing-family so the
    # latest 59/64 champion does not consume the whole seed bank.
    text = text.replace(
        "    sort(seeds.begin(), seeds.end(), [](const Candidate& a, const Candidate& b){ return a.covered > b.covered; });\n"
        "    if (seeds.size() > 256) seeds.resize(256);\n"
        "    return seeds;",
        "    sort(seeds.begin(), seeds.end(), [](const Candidate& a, const Candidate& b){ return a.covered > b.covered; });\n"
        "    vector<Candidate> diverse;\n"
        "    unordered_set<uint64_t> family_seen;\n"
        "    for (const auto& c : seeds) {\n"
        "        uint64_t fam = missing_family_key(c.mask);\n"
        "        if (family_seen.insert(fam).second || c.covered >= 59 || diverse.size() < 512) diverse.push_back(c);\n"
        "        if (diverse.size() >= 8192) break;\n"
        "    }\n"
        "    seeds.swap(diverse);\n"
        "    return seeds;",
    )

    text = replace_once(text, r"string mode_for\(int shard\) \{.*?\n\}", COVER_STITCH_MODE_FOR_CPP, "mode_for", flags=re.S)

    text = text.replace(
        'bool fractional = (mode == "fractional_bridge22" || mode == "repair56_target8" || mode == "transition_penalty22");',
        'bool fractional = is_fractional_mode(mode);',
    )

    text = text.replace(
        'if (mode == "rich_segment_catalog" && hits < 3) base -= 2500;',
        'if (is_cover_set_mode(mode) && hits < 3) base -= 3800;\n            if (is_stitch_mode(mode) && hits < 2) base -= 1200;'
    )
    text = text.replace(
        'if (mode == "subcube_stitch22") {',
        'if (mode == "stitch_with_transposition" || mode == "bridge_compression") {'
    )
    text = text.replace(
        'if (mode == "fractional_bridge22" && ((V[i].x|V[i].y|V[i].z|V[j].x|V[j].y|V[j].z)&1)) base += 700;',
        'if (is_fractional_mode(mode) && ((V[i].x|V[i].y|V[i].z|V[j].x|V[j].y|V[j].z)&1)) base += 900;\n'
        '            if (is_anti_wall_mode(mode) && worst_wall_overlap(m) >= 2) base += 1200;'
    )

    # Weighted seed selection: old control loves 59s; novelty shards deliberately
    # sample 56-58 more often.
    text = text.replace(
        "    for (auto& s : seeds) sw.push_back(pow(max(1, s.covered - 39), 2.0));",
        "    for (auto& s : seeds) {\n"
        "        double x = 1.0;\n"
        "        if (mode == \"novelty_56_58\") x = (s.covered >= 56 && s.covered <= 58) ? 20.0 : 1.0;\n"
        "        else if (mode == \"old_59_control\") x = pow(max(1, s.covered - 39), 2.4);\n"
        "        else x = pow(max(1, s.covered - 49), 3.0) + 2.0 * max(0, 59 - s.covered);\n"
        "        sw.push_back(x);\n"
        "    }"
    )
    text = text.replace("int minK = 2, maxK = min(6, L);", "int minK = 3, maxK = min(is_stitch_mode(mode) ? 16 : 12, L);")
    text = text.replace('if (mode == "rich_segment_catalog" && e.hits >= 3) score += 3000;', 'if (is_cover_set_mode(mode) && e.hits >= 3) score += 5200;')
    text = text.replace('if (mode == "transition_penalty22" && target_gain > 0) score += 5000;', 'if (is_stitch_mode(mode) && target_gain > 0) score += 7000;\n            if (is_anti_wall_mode(mode) && worst_wall_overlap(m | e.mask) < worst_wall_overlap(m)) score += 1200;')
    text = text.replace('if (mode == "subcube_stitch22") score += 300 * min(4, e.hits);', 'if (is_stitch_mode(mode)) score += 420 * min(4, e.hits);')
    text = text.replace('if ((int)cands.size() > 96) break;', 'if ((int)cands.size() > 240) break;')
    text = text.replace('int pool = min<int>(24, cands.size());', 'int pool = min<int>(72, cands.size());')
    text = text.replace('if (mode == "rich_segment_catalog" && e.hits >= 3) score += 4000;', 'if (is_cover_set_mode(mode) && e.hits >= 3) score += 6400;')
    text = text.replace('if ((int)cands.size() > 128) break;', 'if ((int)cands.size() > 260) break;')
    text = text.replace('int pool = min<int>(32, cands.size());', 'int pool = min<int>(80, cands.size());')

    # The main transposition table and anti-wall rejection live in run_thread.
    old = '''    uint64_t attempts = 0;
    while (true) {
        auto now = chrono::steady_clock::now();
        double elapsed = chrono::duration<double>(now - t0).count();
        if (elapsed >= seconds) break;
        attempts++;
        vector<Pt> p;
        bool repair_mode = (mode == "repair56_target8" || mode == "transition_penalty22" || mode == "fractional_bridge22" || mode == "subcube_stitch22");
        if (repair_mode && !seeds.empty() && (rng() % 100) < 88) p = repair_attempt(seeds, V, vidx, adj, mode, rng);
        else p = walk_attempt(V, adj, mode, rng);
        if (p.size() < 2) continue;
        uint64_t m = path_mask(p);
        int cov = pop64(m);
        int links = (int)p.size() - 1;
        bool better = false;'''
    new = '''    uint64_t attempts = 0;
    uint64_t cache_rejects = 0;
    uint64_t wall_rejects = 0;
    unordered_set<uint64_t> seen_states;
    seen_states.reserve(1 << 20);
    while (true) {
        auto now = chrono::steady_clock::now();
        double elapsed = chrono::duration<double>(now - t0).count();
        if (elapsed >= seconds) break;
        attempts++;
        vector<Pt> p;
        bool repair_mode = is_cached_repair_mode(mode);
        int repair_chance = mode == "old_59_control" ? 92 : (is_novelty_mode(mode) ? 68 : 86);
        if (repair_mode && !seeds.empty() && (rng() % 100) < repair_chance) p = repair_attempt(seeds, V, vidx, adj, mode, rng);
        else p = walk_attempt(V, adj, mode, rng);
        if (p.size() < 2) continue;
        uint64_t m = path_mask(p);
        int cov = pop64(m);
        int links = (int)p.size() - 1;
        uint64_t sk = state_key(m, links, p.back());
        if (!seen_states.insert(sk).second) {
            cache_rejects++;
            continue;
        }
        if (seen_states.size() > (1u << 22)) seen_states.clear();
        int wall = worst_wall_overlap(m);
        if (is_anti_wall_mode(mode) && cov <= 59 && wall >= 4 && (rng() % 100) < 82) {
            wall_rejects++;
            continue;
        }
        bool better = false;'''
    text = text.replace(old, new)

    text = text.replace(
        "    best.attempts = attempts;\n    best.elapsed = chrono::duration<double>(chrono::steady_clock::now() - t0).count();",
        "    best.attempts = attempts;\n    best.cache_rejects = cache_rejects;\n    best.wall_rejects = wall_rejects;\n    best.elapsed = chrono::duration<double>(chrono::steady_clock::now() - t0).count();",
    )

    text = text.replace(
        'ss << "    {\\"worker_id\\": " << w.thread_id << ", \\"covered_count\\": " << w.covered << ", \\"links\\": " << w.links << ", \\"attempts\\": " << w.attempts << ", \\"elapsed_seconds\\": " << fixed << setprecision(3) << w.elapsed << "}";',
        'ss << "    {\\"worker_id\\": " << w.thread_id << ", \\"covered_count\\": " << w.covered << ", \\"links\\": " << w.links << ", \\"attempts\\": " << w.attempts << ", \\"cache_rejects\\": " << w.cache_rejects << ", \\"wall_rejects\\": " << w.wall_rejects << ", \\"elapsed_seconds\\": " << fixed << setprecision(3) << w.elapsed << "}";'
    )

    # Replace target defects and weights after GRID is initialized.
    text = replace_once(text, r"vector<Pt> defects = \{\{[^;]+;", "vector<Pt> defects = {{2,4,4},{2,6,2},{2,6,4},{4,0,4},{4,0,6},{2,0,2},{4,4,4},{4,2,4},{4,4,6},{6,2,0},{6,2,4},{6,2,6},{0,4,4},{4,2,6},{0,2,0},{2,4,6},{4,2,0}};", "defects")
    text = replace_once(
        text,
        r"for \(int i = 0; i < 64; \+\+i\) if \(\(TARGET_MASK >> i\) & 1ULL\) POINT_WEIGHT\[i\] = 6\.0;",
        COVER_STITCH_WEIGHTS_CPP,
        "weights",
    )

    text = text.replace("auto adj = build_adj(V, mode, 180);", "auto adj = build_adj(V, mode, 360);")
    text = text.replace("repair56_search parameters:", "cover_stitch_cache_search parameters:")
    text = text.replace(r'\"schema\": \"repair-mlct-shard-v1\"', r'\"schema\": \"cover-stitch-cache-shard-v1\"')

    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(text)
    print(f"wrote {out} with cover/stitch/cache modes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
