#include <algorithm>
#include <array>
#include <chrono>
#include <cmath>
#include <cstdint>
#include <filesystem>
#include <fstream>
#include <iostream>
#include <mutex>
#include <random>
#include <regex>
#include <sstream>
#include <set>
#include <iomanip>
#include <string>
#include <thread>
#include <unordered_map>
#include <unordered_set>
#include <vector>

using namespace std;
namespace fs = std::filesystem;

struct Pt {
    int x = 0, y = 0, z = 0;
    bool operator==(const Pt& o) const { return x == o.x && y == o.y && z == o.z; }
    bool operator<(const Pt& o) const {
        if (x != o.x) return x < o.x;
        if (y != o.y) return y < o.y;
        return z < o.z;
    }
};

struct PtHash {
    size_t operator()(const Pt& p) const {
        uint64_t a = (uint64_t)(p.x + 1009);
        uint64_t b = (uint64_t)(p.y + 2003);
        uint64_t c = (uint64_t)(p.z + 4001);
        return (a * 1000003ULL) ^ (b * 9176ULL) ^ (c * 1315423911ULL);
    }
};

struct Edge {
    int to = 0;
    uint64_t mask = 0;
    int hits = 0;
    int len2 = 0;
    int base = 0;
};

struct Candidate {
    vector<Pt> path;
    uint64_t mask = 0;
    int covered = 0;
    int links = 0;
    string source;
};

struct Result {
    vector<Pt> path;
    uint64_t mask = 0;
    int covered = 0;
    int links = 0;
    string mode;
    uint64_t attempts = 0;
    double elapsed = 0.0;
    int thread_id = 0;
};

static vector<Pt> GRID;
static unordered_map<Pt, int, PtHash> GRID_INDEX;
static uint64_t TARGET_MASK = 0;
static vector<double> POINT_WEIGHT(64, 1.0);

static inline Pt subp(const Pt& a, const Pt& b) { return {a.x - b.x, a.y - b.y, a.z - b.z}; }
static inline int dotp(const Pt& a, const Pt& b) { return a.x*b.x + a.y*b.y + a.z*b.z; }
static inline Pt crossp(const Pt& a, const Pt& b) {
    return {a.y*b.z - a.z*b.y, a.z*b.x - a.x*b.z, a.x*b.y - a.y*b.x};
}
static inline int dist2(const Pt& a, const Pt& b) {
    int dx = a.x-b.x, dy = a.y-b.y, dz = a.z-b.z;
    return dx*dx + dy*dy + dz*dz;
}
static inline int pop64(uint64_t x) { return __builtin_popcountll(x); }

bool onseg(const Pt& a, const Pt& b, const Pt& p) {
    Pt d = subp(b, a);
    if (d.x == 0 && d.y == 0 && d.z == 0) return p == a;
    Pt ap = subp(p, a);
    Pt cr = crossp(d, ap);
    if (cr.x != 0 || cr.y != 0 || cr.z != 0) return false;
    int dd = dotp(d, d);
    int t = dotp(ap, d);
    return 0 <= t && t <= dd;
}

uint64_t maskseg(const Pt& a, const Pt& b) {
    int minx = min(a.x, b.x), maxx = max(a.x, b.x);
    int miny = min(a.y, b.y), maxy = max(a.y, b.y);
    int minz = min(a.z, b.z), maxz = max(a.z, b.z);
    if (maxx < 0 || maxy < 0 || maxz < 0 || minx > 6 || miny > 6 || minz > 6) return 0;
    uint64_t m = 0;
    for (int i = 0; i < 64; ++i) {
        const auto& p = GRID[i];
        if (p.x < minx || p.x > maxx || p.y < miny || p.y > maxy || p.z < minz || p.z > maxz) continue;
        if (onseg(a, b, p)) m |= (1ULL << i);
    }
    return m;
}

uint64_t path_mask(const vector<Pt>& path) {
    uint64_t m = 0;
    for (size_t i = 1; i < path.size(); ++i) m |= maskseg(path[i-1], path[i]);
    return m;
}

vector<array<int,3>> missing_points(uint64_t m) {
    vector<array<int,3>> out;
    for (int i = 0; i < 64; ++i) {
        if (((m >> i) & 1ULL) == 0) out.push_back({GRID[i].x/2, GRID[i].y/2, GRID[i].z/2});
    }
    return out;
}

double weighted_gain(uint64_t m) {
    double s = 0.0;
    while (m) {
        uint64_t b = m & -m;
        int i = __builtin_ctzll(m);
        s += POINT_WEIGHT[i];
        m ^= b;
    }
    return s;
}

string read_file(const fs::path& p) {
    ifstream in(p, ios::binary);
    if (!in) return "";
    stringstream ss; ss << in.rdbuf();
    return ss.str();
}

size_t matching_bracket(const string& s, size_t pos) {
    int depth = 0;
    bool in_str = false, esc = false;
    for (size_t i = pos; i < s.size(); ++i) {
        char c = s[i];
        if (in_str) {
            if (esc) esc = false;
            else if (c == '\\') esc = true;
            else if (c == '"') in_str = false;
            continue;
        }
        if (c == '"') { in_str = true; continue; }
        if (c == '[') depth++;
        else if (c == ']') {
            depth--;
            if (depth == 0) return i;
        }
    }
    return string::npos;
}

vector<Pt> parse_vertices2(const string& text) {
    vector<Pt> out;
    size_t key = text.find("\"vertices2\"");
    if (key == string::npos) return out;
    size_t beg = text.find('[', key);
    if (beg == string::npos) return out;
    size_t end = matching_bracket(text, beg);
    if (end == string::npos || end <= beg) return out;
    string sub = text.substr(beg, end - beg + 1);
    regex triple(R"(\[\s*(-?\d+)\s*,\s*(-?\d+)\s*,\s*(-?\d+)\s*\])");
    for (sregex_iterator it(sub.begin(), sub.end(), triple), e; it != e; ++it) {
        out.push_back({stoi((*it)[1]), stoi((*it)[2]), stoi((*it)[3])});
    }
    return out;
}

vector<Pt> parse_vertices_old(const string& text) {
    vector<Pt> out;
    size_t key = text.find("\"vertices\"");
    if (key == string::npos) return out;
    size_t key2 = text.find("\"vertices2\"");
    if (key2 != string::npos && key2 <= key + 2) return out;
    size_t beg = text.find('[', key);
    if (beg == string::npos) return out;
    size_t end = matching_bracket(text, beg);
    if (end == string::npos || end <= beg) return out;
    string sub = text.substr(beg, end - beg + 1);
    regex triple(R"(\[\s*(-?\d+)\s*,\s*(-?\d+)\s*,\s*(-?\d+)\s*\])");
    for (sregex_iterator it(sub.begin(), sub.end(), triple), e; it != e; ++it) {
        out.push_back({2*stoi((*it)[1]), 2*stoi((*it)[2]), 2*stoi((*it)[3])});
    }
    return out;
}

void add_embedded_seed(vector<Candidate>& seeds) {
    vector<Pt> p = {
        {2,8,-4},{2,0,4},{8,6,4},{-2,6,4},{8,-4,4},{4,4,0},{4,4,8},{0,0,4},
        {0,0,0},{0,12,0},{6,-6,0},{6,10,0},{-2,-6,0},{6,2,8},{6,2,-4},{0,0,6},
        {0,6,6},{8,6,6},{0,-2,6},{0,6,2},{8,6,2},{0,-2,2},{0,4,2}
    };
    Candidate c; c.path = p; c.links = (int)p.size() - 1; c.mask = path_mask(c.path); c.covered = pop64(c.mask); c.source = "embedded_run_28103660449_best";
    seeds.push_back(c);
}

vector<Candidate> load_candidates(const vector<string>& dirs) {
    vector<Candidate> seeds;
    unordered_set<string> seen;
    for (const auto& d : dirs) {
        if (!fs::exists(d)) continue;
        for (auto const& ent : fs::recursive_directory_iterator(d)) {
            if (!ent.is_regular_file() || ent.path().extension() != ".json") continue;
            string txt = read_file(ent.path());
            vector<Pt> p = parse_vertices2(txt);
            if (p.empty()) p = parse_vertices_old(txt);
            if (p.size() < 2 || p.size() > 40) continue;
            uint64_t m = path_mask(p);
            int cov = pop64(m);
            if (cov < 40) continue;
            string key;
            for (auto& q : p) key += to_string(q.x)+","+to_string(q.y)+","+to_string(q.z)+";";
            if (seen.insert(key).second) {
                Candidate c; c.path = p; c.mask = m; c.covered = cov; c.links = (int)p.size()-1; c.source = ent.path().string();
                seeds.push_back(c);
            }
        }
    }
    add_embedded_seed(seeds);
    sort(seeds.begin(), seeds.end(), [](const Candidate& a, const Candidate& b){ return a.covered > b.covered; });
    if (seeds.size() > 256) seeds.resize(256);
    return seeds;
}

string mode_for(int shard) {
    if (shard < 8) return "repair56_target8";
    if (shard < 12) return "rich_segment_catalog";
    if (shard < 15) return "transition_penalty22";
    if (shard < 18) return "fractional_bridge22";
    if (shard == 18) return "subcube_stitch22";
    return "integer_control22";
}

vector<Pt> build_vertices(const vector<Candidate>& seeds, const string& mode) {
    unordered_set<Pt, PtHash> st;
    auto add = [&](Pt p){ st.insert(p); };
    bool fractional = (mode == "fractional_bridge22" || mode == "repair56_target8" || mode == "transition_penalty22");
    if (fractional) {
        for (int x = -2; x <= 8; ++x) for (int y = -2; y <= 8; ++y) for (int z = -2; z <= 8; ++z) add({x,y,z});
    } else {
        for (int x = -6; x <= 14; x += 2) for (int y = -6; y <= 14; y += 2) for (int z = -6; z <= 14; z += 2) add({x,y,z});
    }
    for (auto& c : seeds) for (auto& p : c.path) add(p);
    vector<Pt> v(st.begin(), st.end());
    sort(v.begin(), v.end());
    return v;
}

vector<vector<Edge>> build_adj(const vector<Pt>& V, const string& mode, int cap) {
    int n = (int)V.size();
    vector<vector<Edge>> adj(n);
    for (int i = 0; i < n; ++i) {
        for (int j = i+1; j < n; ++j) {
            uint64_t m = maskseg(V[i], V[j]);
            int hits = pop64(m);
            if (!hits) continue;
            int len = dist2(V[i], V[j]);
            int target = pop64(m & TARGET_MASK);
            int base = hits * 4000 + (int)(weighted_gain(m) * 900) + target * 5000 - min(len, 700);
            if (mode == "rich_segment_catalog" && hits < 3) base -= 2500;
            if (mode == "subcube_stitch22") {
                set<int> cubes;
                for (int k = 0; k < 64; ++k) if ((m >> k) & 1ULL) {
                    int x = GRID[k].x/2, y = GRID[k].y/2, z = GRID[k].z/2;
                    cubes.insert((x/2)*4 + (y/2)*2 + (z/2));
                }
                base += (int)cubes.size() * 900;
            }
            if (mode == "fractional_bridge22" && ((V[i].x|V[i].y|V[i].z|V[j].x|V[j].y|V[j].z)&1)) base += 700;
            Edge e1{j, m, hits, len, base};
            Edge e2{i, m, hits, len, base};
            adj[i].push_back(e1); adj[j].push_back(e2);
        }
    }
    for (auto& a : adj) {
        sort(a.begin(), a.end(), [](const Edge& x, const Edge& y){
            if (x.base != y.base) return x.base > y.base;
            return x.hits > y.hits;
        });
        if ((int)a.size() > cap) a.resize(cap);
    }
    return adj;
}

int pick_weighted(const vector<double>& w, mt19937_64& rng) {
    double s = 0.0; for (double x : w) s += max(0.0, x);
    if (s <= 0.0) return uniform_int_distribution<int>(0, (int)w.size()-1)(rng);
    uniform_real_distribution<double> U(0.0, s);
    double r = U(rng);
    for (int i = 0; i < (int)w.size(); ++i) { r -= max(0.0, w[i]); if (r <= 0) return i; }
    return (int)w.size() - 1;
}

vector<Pt> repair_attempt(const vector<Candidate>& seeds, const vector<Pt>& V, const unordered_map<Pt,int,PtHash>& vidx,
                          const vector<vector<Edge>>& adj, const string& mode, mt19937_64& rng) {
    vector<double> sw;
    for (auto& s : seeds) sw.push_back(pow(max(1, s.covered - 39), 2.0));
    const Candidate& seed = seeds[pick_weighted(sw, rng)];
    if (seed.path.size() < 4) return seed.path;
    int L = (int)seed.path.size() - 1;
    int minK = 2, maxK = min(6, L);
    int k = uniform_int_distribution<int>(minK, maxK)(rng);
    int s = uniform_int_distribution<int>(0, L-k)(rng);
    Pt A = seed.path[s], B = seed.path[s+k];
    auto ita = vidx.find(A), itb = vidx.find(B);
    if (ita == vidx.end() || itb == vidx.end()) return seed.path;
    int cur = ita->second, goal = itb->second;

    uint64_t fixed = 0;
    for (int i = 0; i < L; ++i) {
        if (s <= i && i < s+k) continue;
        fixed |= maskseg(seed.path[i], seed.path[i+1]);
    }

    vector<int> bridge;
    bridge.push_back(cur);
    uint64_t m = fixed;
    for (int step = 1; step <= k; ++step) {
        if (step == k) {
            m |= maskseg(V[cur], V[goal]);
            bridge.push_back(goal);
            cur = goal;
            break;
        }
        vector<pair<double,int>> cands;
        int rem = k - step;
        for (const auto& e : adj[cur]) {
            int v = e.to;
            if (v == cur) continue;
            uint64_t gainm = e.mask & ~m;
            int gain = pop64(gainm);
            int target_gain = pop64(gainm & TARGET_MASK);
            int dgoal = dist2(V[v], B);
            uint64_t finalm = maskseg(V[v], B);
            if (rem == 1 && finalm == 0) continue;
            double score = gain * 12000.0 + weighted_gain(gainm) * 2200.0 + target_gain * 9000.0 + e.hits * 600.0 + e.base;
            score -= 0.22 * dgoal;
            if (mode == "rich_segment_catalog" && e.hits >= 3) score += 3000;
            if (mode == "transition_penalty22" && target_gain > 0) score += 5000;
            if (mode == "subcube_stitch22") score += 300 * min(4, e.hits);
            if (mode == "integer_control22" && ((V[v].x | V[v].y | V[v].z) & 1)) score -= 5000;
            score += uniform_real_distribution<double>(0.0, 2500.0)(rng);
            cands.push_back({score, v});
            if ((int)cands.size() > 96) break;
        }
        if (cands.empty()) return seed.path;
        sort(cands.begin(), cands.end(), greater<pair<double,int>>());
        int pool = min<int>(24, cands.size());
        vector<double> weights(pool);
        for (int i = 0; i < pool; ++i) weights[i] = 1.0 / sqrt(i + 1.0);
        int picked = pick_weighted(weights, rng);
        int nxt = cands[picked].second;
        m |= maskseg(V[cur], V[nxt]);
        bridge.push_back(nxt);
        cur = nxt;
    }

    vector<Pt> out;
    for (int i = 0; i <= s; ++i) out.push_back(seed.path[i]);
    for (int i = 1; i+1 < (int)bridge.size(); ++i) out.push_back(V[bridge[i]]);
    for (int i = s+k; i < (int)seed.path.size(); ++i) out.push_back(seed.path[i]);
    return out;
}

vector<Pt> walk_attempt(const vector<Pt>& V, const vector<vector<Edge>>& adj, const string& mode, mt19937_64& rng) {
    int n = (int)V.size();
    vector<int> starts;
    for (int i = 0; i < n; ++i) if (!adj[i].empty()) starts.push_back(i);
    if (starts.empty()) return {};
    int cur = starts[uniform_int_distribution<int>(0, (int)starts.size()-1)(rng)];
    vector<Pt> path{V[cur]};
    uint64_t m = 0;
    for (int step = 0; step < 22; ++step) {
        vector<pair<double,int>> cands;
        for (const auto& e : adj[cur]) {
            uint64_t gainm = e.mask & ~m;
            int gain = pop64(gainm);
            if (step < 14 && mode != "integer_control22" && gain < 2) continue;
            int target_gain = pop64(gainm & TARGET_MASK);
            double score = gain * 14000.0 + weighted_gain(gainm) * 1800.0 + target_gain * 6000.0 + e.base;
            if (mode == "rich_segment_catalog" && e.hits >= 3) score += 4000;
            if (mode == "integer_control22" && ((V[e.to].x | V[e.to].y | V[e.to].z) & 1)) score -= 8000;
            score += uniform_real_distribution<double>(0.0, 3000.0)(rng);
            cands.push_back({score, e.to});
            if ((int)cands.size() > 128) break;
        }
        if (cands.empty()) break;
        sort(cands.begin(), cands.end(), greater<pair<double,int>>());
        int pool = min<int>(32, cands.size());
        vector<double> weights(pool);
        for (int i = 0; i < pool; ++i) weights[i] = 1.0 / sqrt(i + 1.0);
        int nxt = cands[pick_weighted(weights, rng)].second;
        m |= maskseg(V[cur], V[nxt]);
        path.push_back(V[nxt]);
        cur = nxt;
    }
    return path;
}

Result run_thread(int tid, int shard, uint64_t seed, int seconds, const string& mode,
                  const vector<Candidate>& seeds, const vector<Pt>& V, const unordered_map<Pt,int,PtHash>& vidx,
                  const vector<vector<Edge>>& adj) {
    mt19937_64 rng(seed + 1000003ULL * (uint64_t)shard + 7919ULL * (uint64_t)tid);
    auto t0 = chrono::steady_clock::now();
    Result best;
    best.mode = mode;
    best.thread_id = tid;
    if (!seeds.empty()) {
        best.path = seeds[0].path;
        best.mask = path_mask(best.path);
        best.covered = pop64(best.mask);
        best.links = (int)best.path.size() - 1;
    }
    uint64_t attempts = 0;
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
        bool better = false;
        if (cov > best.covered) better = true;
        else if (cov == best.covered && links <= 22 && best.links > 22) better = true;
        else if (cov == best.covered && pop64(m & TARGET_MASK) > pop64(best.mask & TARGET_MASK)) better = true;
        if (better) {
            best.path = p;
            best.mask = m;
            best.covered = cov;
            best.links = links;
            cerr << "thread=" << tid << " new_best=" << cov << "/64 links=" << links << " target_hits=" << pop64(m & TARGET_MASK) << "\n";
            if (cov == 64 && links <= 22) break;
        }
    }
    best.attempts = attempts;
    best.elapsed = chrono::duration<double>(chrono::steady_clock::now() - t0).count();
    return best;
}

string json_escape(const string& s) {
    string o;
    for (char c : s) {
        if (c == '\\' || c == '"') { o.push_back('\\'); o.push_back(c); }
        else if (c == '\n') o += "\\n";
        else o.push_back(c);
    }
    return o;
}

string to_json(const Result& r, const string& mode, int shard, int shards, uint64_t seed, int seconds, int threads, int seed_count, int vertex_count, int directed_edges, const vector<Result>& workers) {
    stringstream ss;
    ss << "{\n";
    ss << "  \"schema\": \"repair-mlct-shard-v1\",\n";
    ss << "  \"coordinate_scale\": 2,\n";
    ss << "  \"status\": \"" << (r.covered == 64 && r.links <= 22 ? "complete_candidate" : "partial_candidate") << "\",\n";
    ss << "  \"mode\": \"" << json_escape(mode) << "\",\n";
    ss << "  \"links_target\": 22,\n";
    ss << "  \"links\": " << r.links << ",\n";
    ss << "  \"covered_count\": " << r.covered << ",\n";
    ss << "  \"target_defect_hits\": " << pop64(r.mask & TARGET_MASK) << ",\n";
    ss << "  \"missing\": [";
    auto miss = missing_points(r.mask);
    for (size_t i = 0; i < miss.size(); ++i) {
        if (i) ss << ", ";
        ss << "[" << miss[i][0] << ", " << miss[i][1] << ", " << miss[i][2] << "]";
    }
    ss << "],\n";
    ss << "  \"vertices2\": [\n";
    for (size_t i = 0; i < r.path.size(); ++i) {
        ss << "    [" << r.path[i].x << ", " << r.path[i].y << ", " << r.path[i].z << "]";
        if (i + 1 < r.path.size()) ss << ",";
        ss << "\n";
    }
    ss << "  ],\n";
    ss << "  \"parameters\": {\n";
    ss << "    \"mode\": \"" << json_escape(mode) << "\",\n";
    ss << "    \"seconds\": " << seconds << ",\n";
    ss << "    \"threads\": " << threads << ",\n";
    ss << "    \"shard\": " << shard << ",\n";
    ss << "    \"shards\": " << shards << ",\n";
    ss << "    \"seed\": " << seed << ",\n";
    ss << "    \"prior_seed_count\": " << seed_count << ",\n";
    ss << "    \"vertex_count\": " << vertex_count << ",\n";
    ss << "    \"directed_edge_count\": " << directed_edges << "\n";
    ss << "  },\n";
    uint64_t total_attempts = 0; for (auto& w : workers) total_attempts += w.attempts;
    ss << "  \"total_attempts\": " << total_attempts << ",\n";
    ss << "  \"worker_summaries\": [\n";
    for (size_t i = 0; i < workers.size(); ++i) {
        const auto& w = workers[i];
        ss << "    {\"worker_id\": " << w.thread_id << ", \"covered_count\": " << w.covered << ", \"links\": " << w.links << ", \"attempts\": " << w.attempts << ", \"elapsed_seconds\": " << fixed << setprecision(3) << w.elapsed << "}";
        if (i + 1 < workers.size()) ss << ",";
        ss << "\n";
    }
    ss << "  ]\n";
    ss << "}\n";
    return ss.str();
}

int main(int argc, char** argv) {
    vector<string> input_dirs;
    string out_path = "repair_best.json";
    int seconds = 60, threads = 4, shard = 0, shards = 20;
    uint64_t seed = 20260625;
    for (int i = 1; i < argc; ++i) {
        string a = argv[i];
        auto need = [&](const string& name){ if (i + 1 >= argc) { cerr << "missing value for " << name << "\n"; exit(2); } return string(argv[++i]); };
        if (a == "--input-dir" || a == "--prior") input_dirs.push_back(need(a));
        else if (a == "--out") out_path = need(a);
        else if (a == "--seconds") seconds = stoi(need(a));
        else if (a == "--threads" || a == "--workers") threads = stoi(need(a));
        else if (a == "--shard") shard = stoi(need(a));
        else if (a == "--shards") shards = stoi(need(a));
        else if (a == "--seed") seed = stoull(need(a));
        else { cerr << "unknown argument: " << a << "\n"; return 2; }
    }
    if (input_dirs.empty()) input_dirs.push_back(".");
    threads = max(1, min(threads, 16));

    for (int x = 0; x < 4; ++x) for (int y = 0; y < 4; ++y) for (int z = 0; z < 4; ++z) {
        int idx = (int)GRID.size();
        Pt p{2*x,2*y,2*z};
        GRID.push_back(p); GRID_INDEX[p] = idx;
    }
    vector<Pt> defects = {{2,0,0},{2,4,2},{2,4,4},{2,4,6},{4,0,2},{4,2,0},{6,0,4},{6,0,6}};
    for (auto& p : defects) {
        auto it = GRID_INDEX.find(p);
        if (it != GRID_INDEX.end()) TARGET_MASK |= 1ULL << it->second;
    }
    for (int i = 0; i < 64; ++i) POINT_WEIGHT[i] = 1.0;
    for (int i = 0; i < 64; ++i) if ((TARGET_MASK >> i) & 1ULL) POINT_WEIGHT[i] = 6.0;

    auto seeds = load_candidates(input_dirs);
    if (seeds.empty()) { cerr << "no seeds loaded\n"; return 1; }
    string mode = mode_for(shard);
    auto V = build_vertices(seeds, mode);
    unordered_map<Pt,int,PtHash> vidx;
    for (int i = 0; i < (int)V.size(); ++i) vidx[V[i]] = i;
    auto adj = build_adj(V, mode, 180);
    int edge_count = 0; for (auto& a : adj) edge_count += (int)a.size();

    cerr << "repair56_search parameters: mode=" << mode << " shard=" << shard << "/" << shards
         << " seconds=" << seconds << " threads=" << threads << " seeds=" << seeds.size()
         << " best_seed=" << seeds[0].covered << "/64 vertices=" << V.size() << " directed_edges=" << edge_count << "\n";

    vector<thread> ts;
    vector<Result> results(threads);
    for (int t = 0; t < threads; ++t) {
        ts.emplace_back([&, t]() { results[t] = run_thread(t, shard, seed, seconds, mode, seeds, V, vidx, adj); });
    }
    for (auto& th : ts) th.join();
    Result best = results[0];
    for (auto& r : results) {
        if (r.covered > best.covered || (r.covered == best.covered && r.links < best.links)) best = r;
    }
    auto parent = fs::path(out_path).parent_path();
    if (!parent.empty()) fs::create_directories(parent);
    ofstream out(out_path);
    out << to_json(best, mode, shard, shards, seed, seconds, threads, (int)seeds.size(), (int)V.size(), edge_count, results);
    cerr << "final best: " << best.covered << "/64 links=" << best.links << " target_hits=" << pop64(best.mask & TARGET_MASK) << " out=" << out_path << "\n";
    return 0;
}
