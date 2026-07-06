#include <bits/stdc++.h>
using namespace std;

struct Pt { int x, y, z; };
static inline bool operator==(const Pt& a, const Pt& b) { return a.x == b.x && a.y == b.y && a.z == b.z; }
static inline bool operator<(const Pt& a, const Pt& b) { if (a.x != b.x) return a.x < b.x; if (a.y != b.y) return a.y < b.y; return a.z < b.z; }
static inline Pt subp(Pt a, Pt b) { return {a.x-b.x, a.y-b.y, a.z-b.z}; }
static inline long long dotp(Pt a, Pt b) { return 1LL*a.x*b.x + 1LL*a.y*b.y + 1LL*a.z*b.z; }
static inline Pt crossp(Pt a, Pt b) { return {a.y*b.z - a.z*b.y, a.z*b.x - a.x*b.z, a.x*b.y - a.y*b.x}; }
static inline bool is_zero(Pt a) { return a.x == 0 && a.y == 0 && a.z == 0; }

string pt_json(Pt p) { return "[" + to_string(p.x) + "," + to_string(p.y) + "," + to_string(p.z) + "]"; }
string pt_unscaled_json(Pt p) { return "[" + to_string(p.x/2) + "," + to_string(p.y/2) + "," + to_string(p.z/2) + "]"; }

bool on_segment(Pt a, Pt b, Pt p) {
    Pt d = subp(b, a);
    if (is_zero(d)) return p == a;
    Pt ap = subp(p, a);
    if (!is_zero(crossp(d, ap))) return false;
    long long t = dotp(ap, d);
    return 0 <= t && t <= dotp(d, d);
}

vector<Pt> make_grid() {
    vector<Pt> g;
    for (int x = 0; x < 4; ++x)
        for (int y = 0; y < 4; ++y)
            for (int z = 0; z < 4; ++z)
                g.push_back({2*x, 2*y, 2*z});
    return g;
}
const vector<Pt> GRID = make_grid();

uint64_t cover_mask(Pt a, Pt b) {
    uint64_t m = 0;
    for (int i = 0; i < (int)GRID.size(); ++i) if (on_segment(a, b, GRID[i])) m |= (1ULL << i);
    return m;
}

string norm_line_key(Pt a, Pt b) {
    if (b < a) swap(a, b);
    return pt_json(a) + "-" + pt_json(b);
}

struct Line {
    Pt a, b;
    uint64_t mask = 0;
    int pop = 0;
    bool seed = false;
    string key;
};

vector<pair<Pt, Pt>> seed_cover64_lines() {
    return {
        {{0,8,8},{0,0,0}}, {{0,0,0},{0,6,0}}, {{0,6,0},{0,0,6}},
        {{6,6,0},{6,0,0}}, {{6,0,0},{6,0,6}}, {{6,0,6},{6,8,6}},
        {{6,8,6},{-2,0,6}}, {{-2,0,6},{4,0,0}}, {{4,0,0},{4,0,8}},
        {{4,0,8},{4,8,0}}, {{4,8,0},{4,2,0}}, {{0,6,4},{8,6,4}},
        {{8,6,4},{2,0,4}}, {{2,0,4},{2,0,8}}, {{2,0,8},{2,8,0}},
        {{2,8,0},{2,0,0}}, {{2,6,6},{6,2,6}}, {{6,2,6},{6,2,2}},
        {{6,2,2},{6,8,2}},
        {{0,6,2},{6,0,2}}, {{0,0,2},{6,6,2}}, {{0,4,6},{4,0,2}}
    };
}

uint64_t old_wall_mask() {
    uint64_t m = 0;
    vector<Pt> holes = {{0,0,2},{0,4,6},{0,6,2},{4,2,2}};
    for (Pt h : holes) for (int i = 0; i < (int)GRID.size(); ++i) if (GRID[i] == h) m |= (1ULL << i);
    return m;
}

struct GraphStats { int edges = 0, components = 0, largest_component = 0, greedy_path = 0; };

GraphStats graph_stats(const vector<vector<int>>& adj, mt19937_64& rng) {
    int n = (int)adj.size();
    GraphStats st;
    vector<int> seen(n, 0);
    for (int i = 0; i < n; ++i) {
        st.edges += (int)adj[i].size();
        if (seen[i]) continue;
        st.components++;
        int cnt = 0;
        queue<int> q; q.push(i); seen[i] = 1;
        while (!q.empty()) {
            int v = q.front(); q.pop(); cnt++;
            for (int w : adj[v]) if (!seen[w]) { seen[w] = 1; q.push(w); }
        }
        st.largest_component = max(st.largest_component, cnt);
    }
    st.edges /= 2;

    auto greedy_once = [&](int start, bool shuffled) {
        vector<int> used(n, 0);
        int v = start, len = 1;
        used[v] = 1;
        for (;;) {
            vector<int> cand;
            for (int w : adj[v]) if (!used[w]) cand.push_back(w);
            if (cand.empty()) break;
            if (shuffled) {
                shuffle(cand.begin(), cand.end(), rng);
                sort(cand.begin(), cand.end(), [&](int a, int b) { return adj[a].size() > adj[b].size(); });
                int take = min<int>(3, cand.size());
                v = cand[(int)(rng() % take)];
            } else {
                sort(cand.begin(), cand.end(), [&](int a, int b) { return adj[a].size() > adj[b].size(); });
                v = cand[0];
            }
            used[v] = 1; len++;
        }
        return len;
    };
    for (int s = 0; s < n; ++s) st.greedy_path = max(st.greedy_path, greedy_once(s, false));
    for (int t = 0; t < 96; ++t) st.greedy_path = max(st.greedy_path, greedy_once((int)(rng() % n), true));
    return st;
}

struct Eval { int covered = 0, old_holes_covered = 0; GraphStats endpoint, overlap; long long score = LLONG_MIN; };

bool share_endpoint(const Line& A, const Line& B) {
    return A.a == B.a || A.a == B.b || A.b == B.a || A.b == B.b;
}

Eval evaluate(const vector<int>& ids, const vector<Line>& pool, mt19937_64& rng, const string& mode) {
    uint64_t cov = 0;
    for (int id : ids) cov |= pool[id].mask;
    int n = (int)ids.size();
    vector<vector<int>> endpoint_adj(n), overlap_adj(n);
    for (int i = 0; i < n; ++i) {
        const Line& A = pool[ids[i]];
        for (int j = i + 1; j < n; ++j) {
            const Line& B = pool[ids[j]];
            if (share_endpoint(A, B)) { endpoint_adj[i].push_back(j); endpoint_adj[j].push_back(i); }
            if ((A.mask & B.mask) != 0) { overlap_adj[i].push_back(j); overlap_adj[j].push_back(i); }
        }
    }
    Eval e;
    e.covered = __builtin_popcountll(cov);
    e.old_holes_covered = __builtin_popcountll(cov & old_wall_mask());
    e.endpoint = graph_stats(endpoint_adj, rng);
    e.overlap = graph_stats(overlap_adj, rng);

    long long cover_bonus = 100000000000LL * e.covered;
    long long full_bonus = (e.covered == 64 ? 10000000000000LL : 0LL);
    long long old_hole_bonus = 1000000000LL * e.old_holes_covered;
    long long overlap_bonus = 100000000LL * e.overlap.largest_component + 20000000LL * e.overlap.greedy_path + 1000000LL * e.overlap.edges;
    long long endpoint_bonus = 30000000LL * e.endpoint.largest_component + 10000000LL * e.endpoint.greedy_path + 2000000LL * e.endpoint.edges;
    long long connected_bonus = (e.overlap.largest_component == n ? 5000000000LL : 0LL) + (e.endpoint.largest_component == n ? 20000000000LL : 0LL);
    if (mode == "endpoint_stitch_pressure") { endpoint_bonus *= 3; connected_bonus *= 2; }
    else if (mode == "overlap_stitch_pressure") { overlap_bonus *= 3; }
    else if (mode == "cover64_diversity") { cover_bonus += 500000000LL * e.old_holes_covered; }
    e.score = cover_bonus + full_bonus + old_hole_bonus + overlap_bonus + endpoint_bonus + connected_bonus;
    return e;
}

vector<Line> build_pool(vector<int>& seed_ids) {
    vector<Line> pool;
    unordered_map<string, int> seen;
    auto add_line = [&](Pt a, Pt b, bool seed) {
        if (a == b) return -1;
        string key = norm_line_key(a, b);
        auto it = seen.find(key);
        if (it != seen.end()) { if (seed) pool[it->second].seed = true; return it->second; }
        uint64_t m = cover_mask(a, b);
        int pc = __builtin_popcountll(m);
        if (pc < 2) return -1;
        Line L; L.a = a; L.b = b; L.mask = m; L.pop = pc; L.seed = seed; L.key = key;
        int id = (int)pool.size(); seen[key] = id; pool.push_back(L); return id;
    };
    vector<int> coords = {-2, 0, 2, 4, 6, 8};
    vector<Pt> pts;
    for (int x : coords) for (int y : coords) for (int z : coords) pts.push_back({x,y,z});
    for (int i = 0; i < (int)pts.size(); ++i) for (int j = i + 1; j < (int)pts.size(); ++j) add_line(pts[i], pts[j], false);
    for (auto [a, b] : seed_cover64_lines()) {
        int id = add_line(a, b, true);
        if (id < 0) { cerr << "bad seed line\n"; exit(2); }
        seed_ids.push_back(id);
    }
    return pool;
}

string missing_json(uint64_t cov) {
    string s = "["; bool first = true;
    for (int i = 0; i < (int)GRID.size(); ++i) if (((cov >> i) & 1ULL) == 0) {
        if (!first) s += ","; first = false; s += pt_unscaled_json(GRID[i]);
    }
    s += "]"; return s;
}

string lines_json(const vector<int>& ids, const vector<Line>& pool) {
    string s = "[";
    for (int i = 0; i < (int)ids.size(); ++i) {
        if (i) s += ",";
        const Line& L = pool[ids[i]];
        s += "[" + pt_json(L.a) + "," + pt_json(L.b) + "]";
    }
    s += "]"; return s;
}

string mode_for(int shard) {
    if (shard < 4) return "seed64_stitch_improve";
    if (shard < 8) return "overlap_stitch_pressure";
    if (shard < 12) return "endpoint_stitch_pressure";
    if (shard < 16) return "cover64_diversity";
    if (shard < 19) return "old60_escape_mix";
    return "seed64_control";
}

int arg_int(int argc, char** argv, const string& name, int def) { for (int i = 1; i + 1 < argc; ++i) if (argv[i] == name) return stoi(argv[i+1]); return def; }
string arg_str(int argc, char** argv, const string& name, const string& def) { for (int i = 1; i + 1 < argc; ++i) if (argv[i] == name) return argv[i+1]; return def; }

int main(int argc, char** argv) {
    int seconds = arg_int(argc, argv, "--seconds", 180);
    int threads = arg_int(argc, argv, "--threads", 4);
    int seed = arg_int(argc, argv, "--seed", 20260717);
    int shard = arg_int(argc, argv, "--shard", 0);
    int shards = arg_int(argc, argv, "--shards", 20);
    string out = arg_str(argc, argv, "--out", "cover64_stitch_best.json");
    (void)shards;
    string mode = mode_for(shard);

    vector<int> seed_ids;
    vector<Line> pool = build_pool(seed_ids);
    if ((int)seed_ids.size() != 22) { cerr << "seed should have 22 lines\n"; return 3; }

    vector<vector<int>> by_point(64);
    for (int i = 0; i < (int)pool.size(); ++i) for (int p = 0; p < 64; ++p) if ((pool[i].mask >> p) & 1ULL) by_point[p].push_back(i);

    mt19937_64 rng((uint64_t)seed * 1000003ULL + (uint64_t)shard * 9176ULL + 12345ULL);
    vector<int> best = seed_ids, cur = seed_ids;
    Eval best_eval = evaluate(best, pool, rng, mode), cur_eval = best_eval;
    auto t0 = chrono::steady_clock::now();
    long long iterations = 0, accepted = 0;
    (void)threads;

    while (true) {
        if ((iterations & 4095LL) == 0) {
            double elapsed = chrono::duration<double>(chrono::steady_clock::now() - t0).count();
            if (elapsed >= seconds) break;
        }
        iterations++;
        vector<int> cand = cur;
        unordered_set<int> used(cand.begin(), cand.end());
        int k = 1; uint64_t r = rng() % 100; if (r < 15) k = 2; if (r < 3) k = 3;
        for (int step = 0; step < k; ++step) {
            int pos = (int)(rng() % cand.size());
            used.erase(cand[pos]);
            uint64_t cov_without = 0;
            for (int id : cand) if (id != cand[pos]) cov_without |= pool[id].mask;
            vector<int> missing_points;
            for (int p = 0; p < 64; ++p) if (((cov_without >> p) & 1ULL) == 0) missing_points.push_back(p);
            int new_id = -1;
            for (int tries = 0; tries < 200; ++tries) {
                int id;
                if (!missing_points.empty() && (rng() % 100) < 78) {
                    int p = missing_points[(int)(rng() % missing_points.size())];
                    const vector<int>& choices = by_point[p]; id = choices[(int)(rng() % choices.size())];
                } else if (mode == "endpoint_stitch_pressure" && (rng() % 100) < 45) {
                    const Line& base = pool[cand[(int)(rng() % cand.size())]];
                    Pt anchor = (rng() & 1) ? base.a : base.b;
                    vector<int> hits;
                    for (int i = 0; i < (int)pool.size(); ++i) if (pool[i].a == anchor || pool[i].b == anchor) hits.push_back(i);
                    id = hits.empty() ? (int)(rng() % pool.size()) : hits[(int)(rng() % hits.size())];
                } else id = (int)(rng() % pool.size());
                if (!used.count(id)) { new_id = id; break; }
            }
            if (new_id < 0) continue;
            cand[pos] = new_id; used.insert(new_id);
        }
        Eval ev = evaluate(cand, pool, rng, mode);
        bool accept = false;
        if (ev.score >= cur_eval.score) accept = true;
        else {
            long long diff = cur_eval.score - ev.score;
            long long temp = max<long long>(100000000LL, 2000000000LL - iterations / 5000);
            if (diff < temp && (rng() % 1000) < 8) accept = true;
        }
        if (accept) { cur = cand; cur_eval = ev; accepted++; }
        if (ev.score > best_eval.score) { best = cand; best_eval = ev; }
        if ((iterations % 200000) == 0 && cur_eval.covered < 63) { cur = seed_ids; cur_eval = evaluate(cur, pool, rng, mode); }
    }

    uint64_t cov = 0; for (int id : best) cov |= pool[id].mask;
    ofstream fp(out);
    fp << "{\n";
    fp << "  \"schema\": \"cover64-stitch-graph-shard-v1\",\n";
    fp << "  \"source_workflow\": \"smart-search-17-cover64-stitch-graph\",\n";
    fp << "  \"source_shard\": " << shard << ",\n";
    fp << "  \"mode\": \"" << mode << "\",\n";
    fp << "  \"coordinate_scale\": 2,\n";
    fp << "  \"line_count\": " << best.size() << ",\n";
    fp << "  \"links_target\": 22,\n";
    fp << "  \"covered_count\": " << best_eval.covered << ",\n";
    fp << "  \"missing_count\": " << (64 - best_eval.covered) << ",\n";
    fp << "  \"missing\": " << missing_json(cov) << ",\n";
    fp << "  \"old_wall_covered\": " << best_eval.old_holes_covered << ",\n";
    fp << "  \"endpoint_components\": " << best_eval.endpoint.components << ",\n";
    fp << "  \"endpoint_largest_component\": " << best_eval.endpoint.largest_component << ",\n";
    fp << "  \"endpoint_edges\": " << best_eval.endpoint.edges << ",\n";
    fp << "  \"endpoint_greedy_path\": " << best_eval.endpoint.greedy_path << ",\n";
    fp << "  \"overlap_components\": " << best_eval.overlap.components << ",\n";
    fp << "  \"overlap_largest_component\": " << best_eval.overlap.largest_component << ",\n";
    fp << "  \"overlap_edges\": " << best_eval.overlap.edges << ",\n";
    fp << "  \"overlap_greedy_path\": " << best_eval.overlap.greedy_path << ",\n";
    fp << "  \"score\": " << best_eval.score << ",\n";
    fp << "  \"iterations\": " << iterations << ",\n";
    fp << "  \"accepted\": " << accepted << ",\n";
    fp << "  \"parameters\": {\"seconds\": " << seconds << ", \"threads\": " << threads << ", \"seed\": " << seed << ", \"shard\": " << shard << ", \"shards\": " << shards << "},\n";
    fp << "  \"interpretation\": \"unordered 22-line cover/stitch skeleton; not a verified polygonal trail\",\n";
    fp << "  \"lines2\": " << lines_json(best, pool) << "\n";
    fp << "}\n";
    fp.close();
    cerr << "pool_size=" << pool.size() << " best_covered=" << best_eval.covered << " overlap_path=" << best_eval.overlap.greedy_path << " endpoint_path=" << best_eval.endpoint.greedy_path << " iterations=" << iterations << "\n";
    return 0;
}
