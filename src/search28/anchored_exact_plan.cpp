// smart-search-26-anchored-exact
// Exhaustive exact branch-and-bound over 22-link trails that contain the
// Ripa corner chain  (outer)->000->300->033->(outer)  where the two outer links
// lie on the space diagonal through 000/333 and on the edge line x=0,z=3.
//
// Exact contact model (see docs/smart-search-26-anchored-exact-launch.md):
//   R link : supporting line is a lattice line (>=2 grid points); consecutive
//            R links meet at their exact rational intersection point.
//   T link : supporting line contains exactly one grid point p; it joins the
//            previous lattice line L and the next lattice line M.  All
//            combinatorially distinct (exit cell on L, entry cell on M) are
//            enumerated exactly (non-coplanar: unique transversal; coplanar:
//            exact breakpoint cells).
//   F link : supporting line contains no grid point.  Represented by its
//            dominating form (full extension on L and on M).
//   End-T  : outermost link through one grid point (dominating form).
// Class budgets: total links 22, at most W2 links on 2-point lattice lines,
// at most K non-lattice links (T/F/end-T), non-lattice links never adjacent.
// Only the C++ standard library is used.
#include <algorithm>
#include <array>
#include <atomic>
#include <chrono>
#include <cinttypes>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <fstream>
#include <map>
#include <mutex>
#include <numeric>
#include <random>
#include <set>
#include <sstream>
#include <stdexcept>
#include <string>
#include <thread>
#include <vector>

using std::int64_t;
using std::uint64_t;
typedef __int128 i128;

// ---------------------------------------------------------------- rationals
struct Q {
  int64_t n = 0, d = 1;
};
static const i128 QLIM = ((i128)1) << 60;
static Q mkq(i128 n, i128 d) {
  if (d == 0) throw std::runtime_error("zero denominator");
  if (d < 0) { n = -n; d = -d; }
  i128 a = n < 0 ? -n : n, b = d;
  while (b) { i128 t = a % b; a = b; b = t; }
  if (a == 0) a = 1;
  n /= a; d /= a;
  if (n > QLIM || n < -QLIM || d > QLIM) throw std::runtime_error("rational overflow");
  return Q{(int64_t)n, (int64_t)d};
}
static Q qi(int64_t v) { return Q{v, 1}; }
static Q qadd(Q a, Q b) { return mkq((i128)a.n * b.d + (i128)b.n * a.d, (i128)a.d * b.d); }
static Q qsub(Q a, Q b) { return mkq((i128)a.n * b.d - (i128)b.n * a.d, (i128)a.d * b.d); }
static Q qmul(Q a, Q b) { return mkq((i128)a.n * b.n, (i128)a.d * b.d); }
static Q qdiv(Q a, Q b) { return mkq((i128)a.n * b.d, (i128)a.d * b.n); }
static int qcmp(Q a, Q b) { i128 l = (i128)a.n * b.d, r = (i128)b.n * a.d; return l < r ? -1 : (l > r ? 1 : 0); }
static bool qeq(Q a, Q b) { return a.n == b.n && a.d == b.d; }
static int qsign(Q a) { return a.n > 0 ? 1 : (a.n < 0 ? -1 : 0); }
static std::string qstr(Q a) { return a.d == 1 ? std::to_string(a.n) : std::to_string(a.n) + "/" + std::to_string(a.d); }

struct P3 { Q x, y, z; };
static P3 padd(P3 a, P3 b) { return {qadd(a.x, b.x), qadd(a.y, b.y), qadd(a.z, b.z)}; }
static P3 psub(P3 a, P3 b) { return {qsub(a.x, b.x), qsub(a.y, b.y), qsub(a.z, b.z)}; }
static P3 pscale(P3 a, Q t) { return {qmul(a.x, t), qmul(a.y, t), qmul(a.z, t)}; }
static Q pdot(P3 a, P3 b) { return qadd(qadd(qmul(a.x, b.x), qmul(a.y, b.y)), qmul(a.z, b.z)); }
static P3 pcross(P3 a, P3 b) { return {qsub(qmul(a.y, b.z), qmul(a.z, b.y)), qsub(qmul(a.z, b.x), qmul(a.x, b.z)), qsub(qmul(a.x, b.y), qmul(a.y, b.x))}; }
static bool pzero(P3 a) { return a.x.n == 0 && a.y.n == 0 && a.z.n == 0; }
static P3 pint(int64_t x, int64_t y, int64_t z) { return {qi(x), qi(y), qi(z)}; }

// Intersection of lines A + s*u and B + t*v. Returns false when parallel or skew.
static bool line_meet(P3 A, P3 u, P3 B, P3 v, Q& s, Q& t) {
  P3 n = pcross(u, v);
  if (pzero(n)) return false;
  P3 w = psub(B, A);
  if (qsign(pdot(w, n)) != 0) return false;
  Q nn = pdot(n, n);
  s = qdiv(pdot(pcross(w, v), n), nn);
  t = qdiv(pdot(pcross(w, u), n), nn);
  return true;
}

// ------------------------------------------------------------ lattice lines
static int bitof(int x, int y, int z) { return x * 16 + y * 4 + z; }
struct Line {
  int ax, ay, az, dx, dy, dz;  // grid point k = a + k*d, k = 0..n-1
  int n;
  uint64_t pm[4];
  uint64_t mask;
};
static std::vector<Line> LINES;
static std::vector<std::vector<int>> THRU;      // grid bit -> lattice lines through it
static std::vector<std::vector<int>> RICH_THRU; // grid bit -> lines with >=3 points through it
static std::vector<int> RICH;                   // lines with >=3 points
struct Adj { int m; Q s, t; };
static std::vector<std::vector<Adj>> ADJ;
static std::vector<std::vector<Adj>> ADJ_RICH;

static P3 lineA(const Line& l) { return pint(l.ax, l.ay, l.az); }
static P3 lineD(const Line& l) { return pint(l.dx, l.dy, l.dz); }

static void build_lines() {
  std::set<std::array<int, 6>> seen;
  for (int i = 0; i < 64; i++)
    for (int j = i + 1; j < 64; j++) {
      int px = i / 16, py = (i / 4) % 4, pz = i % 4, qx = j / 16, qy = (j / 4) % 4, qz = j % 4;
      int dx = qx - px, dy = qy - py, dz = qz - pz;
      int g = std::gcd(std::gcd(std::abs(dx), std::abs(dy)), std::abs(dz));
      dx /= g; dy /= g; dz /= g;
      if (dx < 0 || (dx == 0 && (dy < 0 || (dy == 0 && dz < 0)))) { dx = -dx; dy = -dy; dz = -dz; }
      int ax = px, ay = py, az = pz;
      while (true) {
        int bx = ax - dx, by = ay - dy, bz = az - dz;
        if (bx < 0 || by < 0 || bz < 0 || bx > 3 || by > 3 || bz > 3) break;
        ax = bx; ay = by; az = bz;
      }
      std::array<int, 6> key{ax, ay, az, dx, dy, dz};
      if (seen.count(key)) continue;
      seen.insert(key);
      Line l{ax, ay, az, dx, dy, dz, 0, {0, 0, 0, 0}, 0};
      int cx = ax, cy = ay, cz = az;
      while (cx >= 0 && cy >= 0 && cz >= 0 && cx <= 3 && cy <= 3 && cz <= 3) {
        if (l.n >= 4) throw std::runtime_error("line with more than 4 points");
        l.pm[l.n++] = 1ULL << bitof(cx, cy, cz);
        cx += dx; cy += dy; cz += dz;
      }
      for (int k = 0; k < l.n; k++) l.mask |= l.pm[k];
      LINES.push_back(l);
    }
  THRU.assign(64, {});
  RICH_THRU.assign(64, {});
  for (int i = 0; i < (int)LINES.size(); i++) {
    if (LINES[i].n >= 3) RICH.push_back(i);
    for (int k = 0; k < LINES[i].n; k++) {
      int b = __builtin_ctzll(LINES[i].pm[k]);
      THRU[b].push_back(i);
      if (LINES[i].n >= 3) RICH_THRU[b].push_back(i);
    }
  }
  ADJ.assign(LINES.size(), {});
  ADJ_RICH.assign(LINES.size(), {});
  for (int i = 0; i < (int)LINES.size(); i++)
    for (int j = 0; j < (int)LINES.size(); j++) {
      if (i == j) continue;
      Q s, t;
      if (line_meet(lineA(LINES[i]), lineD(LINES[i]), lineA(LINES[j]), lineD(LINES[j]), s, t)) { ADJ[i].push_back({j, s, t}); if (LINES[j].n >= 3) ADJ_RICH[i].push_back({j, s, t}); }
    }
}
static int find_line(int px, int py, int pz, int qx, int qy, int qz, int& kp, int& kq) {
  uint64_t bp = 1ULL << bitof(px, py, pz), bq = 1ULL << bitof(qx, qy, qz);
  for (int i = 0; i < (int)LINES.size(); i++) {
    if ((LINES[i].mask & bp) && (LINES[i].mask & bq)) {
      for (int k = 0; k < LINES[i].n; k++) { if (LINES[i].pm[k] == bp) kp = k; if (LINES[i].pm[k] == bq) kq = k; }
      return i;
    }
  }
  return -1;
}

// ------------------------------------------------------------------ entries
// Position on a line: parameter value e (original orientation), closed flag,
// or "inf" meaning the link starts before every grid point (free entry).
struct Ent { bool inf = true; Q e; bool closed = true; };

// grid points k on line l covered by a link travelling in direction sg from
// entry en to exit x (exit closed rational) or to infinity (xinf).
static uint64_t cover(int li, int sg, const Ent& en, bool xinf, Q x) {
  const Line& l = LINES[li];
  uint64_t m = 0;
  for (int k = 0; k < l.n; k++) {
    if (!en.inf) {
      i128 c = (i128)k * en.e.d - en.e.n; c *= sg;
      if (c < 0 || (c == 0 && !en.closed)) continue;
    }
    if (!xinf) {
      i128 c = (i128)x.n - (i128)k * x.d; c *= sg;
      if (c < 0) continue;
    }
    m |= l.pm[k];
  }
  return m;
}
// is parameter s strictly ahead of entry en in direction sg
static bool ahead(int sg, const Ent& en, Q s) {
  if (en.inf) return true;
  return qcmp(s, en.e) * sg > 0;
}

// ------------------------------------------------------------------- moves
enum MoveKind : int { MV_START = 0, MV_R = 1, MV_F = 2, MV_T = 3, MV_TC = 4, MV_END = 5, MV_ENDT = 6, MV_SWITCH = 7 };
// A move records how the current link on line `from` ends and the next link starts.
struct Move {
  int kind;
  int from, to;   // lattice line ids
  int sg_to;      // direction on `to`
  int p;          // grid bit for T / end-T
  Q s, t;         // exact exit param on from, entry param on to (R, T)
  Q lo, hi;       // coplanar T cell on `from` (lo,hi) in increasing param; flags below
  bool lo_inf, hi_inf;
  Ent entry;      // entry on `to` as used by the search
};

// --------------------------------------------------------- T move generator
struct TOut { uint64_t covL; uint64_t covT; Move mv; };

static bool tparam_of(const P3& A, const P3& d, const P3& p, const Line& M, Q s, Q& t, P3& X, P3& Y) {
  // X = A + s d ; line through X and p ; intersect with M
  X = padd(A, pscale(d, s));
  P3 u = psub(p, X);
  Q lam, tt;
  if (!line_meet(X, u, lineA(M), lineD(M), lam, tt)) return false;
  Y = padd(X, pscale(u, lam));
  t = tt;
  // p strictly between X and Y  <=>  lam > 1
  return qcmp(lam, qi(1)) > 0;
}
static uint64_t seg_mask_exact(const P3& X, const P3& Y) {
  uint64_t m = 0;
  P3 dv = psub(Y, X);
  if (pzero(dv)) return 0;
  Q dd = pdot(dv, dv);
  for (int b = 0; b < 64; b++) {
    P3 g = pint(b / 16, (b / 4) % 4, b % 4);
    P3 w = psub(g, X);
    if (!pzero(pcross(dv, w))) continue;
    Q t = pdot(w, dv);
    if (qsign(t) >= 0 && qcmp(t, dd) <= 0) m |= 1ULL << b;
  }
  return m;
}

static void gen_T(int li, int sg, const Ent& en, int pbit, int mi, std::vector<TOut>& out) {
  const Line& L = LINES[li];
  const Line& M = LINES[mi];
  if ((L.mask >> pbit) & 1) return;
  if ((M.mask >> pbit) & 1) return;
  P3 A = lineA(L), d = lineD(L), B = lineA(M), e = lineD(M);
  P3 p = pint(pbit / 16, (pbit / 4) % 4, pbit % 4);
  P3 nrm = pcross(d, psub(p, A));
  Q ne = pdot(nrm, e);
  Q nb = pdot(nrm, psub(B, A));
  if (qsign(ne) != 0) {
    // non-coplanar: unique transversal through p
    Q t = qdiv(qsub(qi(0), nb), ne);  // nrm.(B + t e - A) = 0
    P3 Y = padd(B, pscale(e, t));
    P3 u = psub(p, Y);
    Q mu, s;
    if (!line_meet(Y, u, A, d, mu, s)) return;
    P3 X = padd(A, pscale(d, s));
    // p strictly between X and Y : Y + mu u = X, need mu > 1
    if (qcmp(mu, qi(1)) <= 0) return;
    if (!ahead(sg, en, s)) return;
    TOut o;
    o.covL = cover(li, sg, en, false, s);
    o.covT = seg_mask_exact(X, Y);
    for (int sg2 = -1; sg2 <= 1; sg2 += 2) {
      Move mv{}; mv.kind = MV_T; mv.from = li; mv.to = mi; mv.sg_to = sg2; mv.p = pbit; mv.s = s; mv.t = t;
      mv.entry.inf = false; mv.entry.e = t; mv.entry.closed = true;
      o.mv = mv; out.push_back(o);
    }
    return;
  }
  if (qsign(nb) != 0) return;  // M parallel to the plane, not in it
  // coplanar: breakpoints in s
  std::vector<Q> bp;
  for (int k = 0; k < L.n; k++) bp.push_back(qi(k));
  if (!en.inf) bp.push_back(en.e);
  for (int j = 0; j < M.n; j++) {
    P3 Yj = padd(B, pscale(e, qi(j)));
    Q a, s;
    if (line_meet(Yj, psub(p, Yj), A, d, a, s)) bp.push_back(s);
  }
  for (int q = 0; q < 64; q++) {  // other grid points of the plane
    if (q == pbit) continue;
    P3 g = pint(q / 16, (q / 4) % 4, q % 4);
    if (qsign(pdot(nrm, psub(g, A))) != 0) continue;
    Q a, s;
    if (line_meet(g, psub(p, g), A, d, a, s)) bp.push_back(s);
  }
  bool has_pole = false; Q pole;
  {
    Q a, s;
    if (line_meet(p, e, A, d, a, s)) { has_pole = true; pole = s; bp.push_back(s); }
  }
  std::sort(bp.begin(), bp.end(), [](Q a, Q b) { return qcmp(a, b) < 0; });
  bp.erase(std::unique(bp.begin(), bp.end(), [](Q a, Q b) { return qeq(a, b); }), bp.end());
  // t at infinity: line through p with direction d meets M
  bool tinf_ok = false; Q tinf;
  {
    Q a, tt;
    if (line_meet(p, d, B, e, a, tt)) { tinf_ok = true; tinf = tt; }
  }
  auto t_at = [&](Q s, Q& t, P3& X, P3& Y) -> bool { return tparam_of(A, d, p, M, s, t, X, Y); };
  // point cells
  for (size_t i = 0; i < bp.size(); i++) {
    Q s = bp[i];
    if (has_pole && qeq(s, pole)) continue;
    if (!ahead(sg, en, s)) continue;
    Q t; P3 X, Y;
    if (!t_at(s, t, X, Y)) continue;
    TOut o;
    o.covL = cover(li, sg, en, false, s);
    o.covT = seg_mask_exact(X, Y);
    for (int sg2 = -1; sg2 <= 1; sg2 += 2) {
      Move mv{}; mv.kind = MV_T; mv.from = li; mv.to = mi; mv.sg_to = sg2; mv.p = pbit; mv.s = s; mv.t = t;
      mv.entry.inf = false; mv.entry.e = t; mv.entry.closed = true;
      o.mv = mv; out.push_back(o);
    }
  }
  // open cells: (-inf,bp0), (bp_i,bp_{i+1}), (bp_last,+inf)
  for (size_t i = 0; i <= bp.size(); i++) {
    bool loinf = (i == 0), hiinf = (i == bp.size());
    Q lo = loinf ? Q{} : bp[i - 1];
    Q hi = hiinf ? Q{} : bp[i];
    Q rep;
    if (loinf && hiinf) rep = qi(0);
    else if (loinf) rep = qsub(hi, qi(1));
    else if (hiinf) rep = qadd(lo, qi(1));
    else rep = qdiv(qadd(lo, hi), qi(2));
    if (!ahead(sg, en, rep)) continue;
    Q trep; P3 X, Y;
    if (!t_at(rep, trep, X, Y)) continue;
    // back endpoint of the cell in direction sg determines coverage on L
    uint64_t covL;
    if (sg > 0) covL = loinf ? 0ULL : cover(li, sg, en, false, lo);
    else covL = hiinf ? 0ULL : cover(li, sg, en, false, hi);
    // image endpoints in t
    auto endpoint_t = [&](bool isinf, Q sv, bool& tinfinite, Q& tv) {
      if (isinf) {
        if (tinf_ok) { tinfinite = false; tv = tinf; } else tinfinite = true;
        return;
      }
      if (has_pole && qeq(sv, pole)) { tinfinite = true; return; }
      Q tt; P3 X2, Y2;
      Q a2, tt2;
      // limit of t at a finite non-pole breakpoint equals t at that point
      P3 X3 = padd(A, pscale(d, sv));
      if (!line_meet(X3, psub(p, X3), B, e, a2, tt2)) { tinfinite = true; return; }
      tinfinite = false; tv = tt2;
      (void)tt; (void)X2; (void)Y2;
    };
    bool t1inf, t2inf; Q t1, t2;
    endpoint_t(loinf, lo, t1inf, t1);
    endpoint_t(hiinf, hi, t2inf, t2);
    for (int sg2 = -1; sg2 <= 1; sg2 += 2) {
      // back endpoint on M in direction sg2: the one on the "behind" side of trep
      Ent ent;
      // candidate endpoints; infinite ones lie on the side determined by trep ordering
      // choose endpoint such that sg2*(trep - endpoint) > 0
      bool found = false;
      for (int c = 0; c < 2 && !found; c++) {
        bool ti = c == 0 ? t1inf : t2inf;
        Q tv = c == 0 ? t1 : t2;
        if (ti) continue;
        if (qcmp(trep, tv) * sg2 > 0) { ent.inf = false; ent.e = tv; ent.closed = false; found = true; }
      }
      if (!found) {
        // the behind side is unbounded (an infinite endpoint) -> free entry
        if (t1inf || t2inf) { ent.inf = true; ent.closed = true; found = true; }
      }
      if (!found) continue;  // degenerate (both endpoints ahead): impossible for monotone map
      Move mv{}; mv.kind = MV_TC; mv.from = li; mv.to = mi; mv.sg_to = sg2; mv.p = pbit;
      mv.lo = lo; mv.hi = hi; mv.lo_inf = loinf; mv.hi_inf = hiinf; mv.s = rep; mv.t = trep;
      mv.entry = ent;
      TOut o; o.covL = covL; o.covT = 1ULL << pbit; o.mv = mv;
      out.push_back(o);
    }
  }
}

// ---------------------------------------------------------------- the search
struct Config {
  int total_links = 22;
  int w2 = 3;
  int kmax = 3;
  int unit_depth = 2;
  int shards = 20, shard = 0, threads = 4;
  double seconds = 60;
  uint64_t tt_mb = 512;  // per thread
  int save_min = 63;
  int max_saved = 2000;
  std::string out_dir = "out";
  int64_t unit_node_limit = -1;
  int target = 64;
  int allow_t = 1;  // 0: connectors are F only
  std::string plan_file;  // search27: work-item plan (empty = classic round-robin units)
};

struct State {
  int side;      // 0 = suffix (from 033 along x=0,z=3 toward 003), 1 = prefix (from 000 along diagonal)
  int line, sg;
  Ent en;
  uint64_t C;    // covered by completed links (current link excluded)
  int links;     // links used in total, including the current one and the 2 fixed middle links
  int w2u, ku;
  bool prev_nonlattice;  // informational: current link was entered through a T/F link (non-lattice links are never adjacent by construction)
};

static uint64_t ANCHOR_C0;
static int ANCHOR_ID = 5;
static int ANCHOR_FIXED_LINKS = 2;
static int SUFFIX_LINE, SUFFIX_K, SUFFIX_SG, PREFIX_LINE, PREFIX_K, PREFIX_SG;

static State suffix_start() {
  State s{};
  s.side = 0; s.line = SUFFIX_LINE; s.sg = SUFFIX_SG; s.en.inf = false; s.en.e = qi(SUFFIX_K); s.en.closed = true;
  s.C = ANCHOR_C0; s.links = ANCHOR_FIXED_LINKS + 1; s.w2u = 0; s.ku = 0; s.prev_nonlattice = false;
  return s;
}
static State prefix_start(uint64_t C, int links, int w2u, int ku) {
  State s{};
  s.side = 1; s.line = PREFIX_LINE; s.sg = PREFIX_SG; s.en.inf = false; s.en.e = qi(PREFIX_K); s.en.closed = true;
  s.C = C; s.links = links + 1; s.w2u = w2u; s.ku = ku; s.prev_nonlattice = false;
  return s;
}

// Admissible feasibility bound.
// U: uncovered points after completed links. cur: points the current link can
// still cover (ahead on its line). r: number of links still to be created
// after the current one. w2l/kl: remaining budgets.
static int SLACK = 0;  // number of points allowed to stay uncovered (64 - target)
static bool feasible(uint64_t C, uint64_t curAhead, bool curRich, int r, int w2l, int kl) {
  uint64_t U = ~C;
  int cnt = __builtin_popcountll(U);
  if (cnt <= SLACK) return true;
  if (cnt > 4 * (r + 1) + SLACK) return false;
  int curCnt = __builtin_popcountll(curAhead & U);
  int cc[5] = {0, 0, 0, 0, 0};
  for (int li : RICH) cc[__builtin_popcountll(LINES[li].mask & U)]++;
  // quick counting test with the most generous allocation
  {
    int best = 0;
    for (int b2 = 0; b2 <= std::min(w2l, r); b2++)
      for (int bt = 0; bt <= std::min(kl, r - b2); bt++) {
        int capacity = curCnt + 2 * b2 + bt + SLACK, rr = r - b2 - bt;
        for (int g = 4; g >= 1 && rr > 0; g--) { int t = std::min(rr, cc[g]); capacity += t * g; rr -= t; }
        if (capacity > best) best = capacity;
      }
    if (best < cnt) return false;
  }
  // fractional (LP-dual) bound: y_p = 1/m(p), m(p) = max uncovered points on a rich line through p
  int hist[5] = {0, 0, 0, 0, 0};
  uint64_t x = U;
  while (x) {
    int p = __builtin_ctzll(x); x &= x - 1;
    int m = 1;
    for (int li : RICH_THRU[p]) { int c = __builtin_popcountll(LINES[li].mask & U); if (c > m) m = c; }
    hist[m]++;
  }
  // y values sorted descending: hist[1] ones, hist[2] halves, hist[3] thirds, hist[4] quarters (scaled by 12)
  int yv[65]; int np = 0;
  for (int m = 1; m <= 4; m++) for (int i = 0; i < hist[m]; i++) yv[np++] = 12 / m;
  int prefix[66]; prefix[0] = 0; for (int i = 0; i < np; i++) prefix[i + 1] = prefix[i] + yv[i];
  int total = prefix[np];
  int curFrac = curRich ? 12 : 12 * std::min(curCnt, 2);
  for (int b2 = 0; b2 <= std::min(w2l, r); b2++)
    for (int bt = 0; bt <= std::min(kl, r - b2); bt++) {
      int a = r - b2 - bt;
      int capacity = curCnt + 2 * b2 + bt + SLACK;
      int rr = a;
      for (int g = 4; g >= 1 && rr > 0; g--) { int t = std::min(rr, cc[g]); capacity += t * g; rr -= t; }
      if (capacity < cnt) continue;
      int weakPts = std::min(np, 2 * b2 + bt + SLACK);
      int rest = total - prefix[weakPts];
      if (rest <= curFrac + 12 * a) return true;
    }
  return false;
}

struct Leaf { std::vector<Move> path; uint64_t C; int links; };

struct TTEntry { uint64_t C; int64_t en_n, en_d; uint32_t line_sg_flags; uint16_t links_w2_k; uint16_t used; };
struct TTable {
  std::vector<TTEntry> tab; uint64_t maskv = 0; uint64_t nslots = 0; bool pow2 = true; uint64_t hits = 0, stores = 0;
  // search28: the table uses the whole tt_mb budget.  A power-of-two size keeps the
  // search-26/27 mask indexing bit-for-bit; any other size uses multiply-shift range
  // reduction.  Entries store the full key, so the index map never affects soundness.
  void init(uint64_t mb) {
    uint64_t n = mb * 1024ULL * 1024ULL / sizeof(TTEntry); if (n < 1) n = 1;
    pow2 = (n & (n - 1)) == 0;
    tab.assign(n, TTEntry{0, 0, 0, 0, 0, 0}); maskv = n - 1; nslots = n;
  }
  uint64_t slot(uint64_t hv) const { return pow2 ? (hv & maskv) : (uint64_t)(((unsigned __int128)hv * nslots) >> 64); }
  static uint64_t mix(uint64_t z) { z += 0x9e3779b97f4a7c15ULL; z = (z ^ (z >> 30)) * 0xbf58476d1ce4e5b9ULL; z = (z ^ (z >> 27)) * 0x94d049bb133111ebULL; return z ^ (z >> 31); }
  static void key(const State& s, TTEntry& k) {
    k.C = s.C; k.en_n = s.en.inf ? INT64_MIN : s.en.e.n; k.en_d = s.en.inf ? 0 : s.en.e.d;
    k.line_sg_flags = (uint32_t)s.line << 4 | (s.sg > 0 ? 1u : 0u) << 3 | (s.en.closed ? 1u : 0u) << 2 | (s.prev_nonlattice ? 1u : 0u) << 1 | (uint32_t)s.side;
    k.links_w2_k = (uint16_t)(s.links << 8 | s.w2u << 4 | s.ku);
    k.used = 1;
  }
  uint64_t h(const TTEntry& k) const { return mix(k.C ^ mix((uint64_t)k.en_n * 31 + (uint64_t)k.en_d) ^ mix(((uint64_t)k.line_sg_flags << 16) | k.links_w2_k)); }
  bool probe(const State& s) {
    if (tab.empty()) return false;
    TTEntry k; key(s, k); const TTEntry& e = tab[slot(h(k))];
    if (e.used && e.C == k.C && e.en_n == k.en_n && e.en_d == k.en_d && e.line_sg_flags == k.line_sg_flags && e.links_w2_k == k.links_w2_k) { hits++; return true; }
    return false;
  }
  void store(const State& s) { if (tab.empty()) return; TTEntry k; key(s, k); tab[slot(h(k))] = k; stores++; }
};

struct Worker {
  const Config* cfg;
  int64_t nodes = 0;
  int best = 0;
  std::vector<Leaf> saved;   // >= save_min
  std::vector<Leaf> full;    // 64/64
  std::vector<Move> path;
  TTable tt;
  bool abort = false;
  std::chrono::steady_clock::time_point deadline;
  int64_t unit_nodes = 0;
  int64_t unit_limit = -1;
  int64_t pruned_bound = 0, pruned_tt = 0;
  std::mt19937_64* rng = nullptr;   // Knuth probe mode when non-null

  void children(const State& s, std::vector<std::pair<State, Move>>& ch, std::vector<std::pair<uint64_t, Move>>* leaves);
  bool dfs(const State& s);  // returns true if subtree produced a 64/64 leaf
  void record_leaf(uint64_t C, int links, const Move& last);
};

static int remaining_after(const Config& c, int links) { return c.total_links - links; }

void Worker::record_leaf(uint64_t C, int links, const Move& last) {
  int cnt = __builtin_popcountll(C);
  if (cnt > best) best = cnt;
  if (cnt >= cfg->save_min || cnt == 64) {
    Leaf lf; lf.path = path; lf.path.push_back(last); lf.C = C; lf.links = links;
    if (cnt == 64) full.push_back(lf);
    else if ((int)saved.size() < cfg->max_saved) saved.push_back(lf);
  }
}

// Generate successor states. Terminal completions are reported through `leaves`
// (final covered mask, terminal move) instead of states.
struct FeasMemo {
  struct E { uint64_t C; int key; bool v; };
  std::vector<E> e;
  bool get(uint64_t C, uint64_t ahead, bool rich, int r, int w2l, int kl) {
    int cnt = __builtin_popcountll(ahead & ~C);
    int key = cnt | (rich ? 8 : 0) | (r << 4) | (w2l << 10) | (kl << 15);
    for (const E& x : e) if (x.C == C && x.key == key) return x.v;
    // the bound depends on ahead only through its uncovered count and richness
    bool v = feasible(C, ahead, rich, r, w2l, kl);
    e.push_back({C, key, v});
    return v;
  }
};
void Worker::children(const State& s, std::vector<std::pair<State, Move>>& ch, std::vector<std::pair<uint64_t, Move>>* leaves) {
  const Config& c = *cfg;
  FeasMemo memo;
  const Line& L = LINES[s.line];
  int r_after = remaining_after(c, s.links);  // links still available after the current one
  uint64_t fullCov = cover(s.line, s.sg, s.en, true, Q{});
  // ---- end of side: current link exits freely
  {
    uint64_t C2 = s.C | fullCov;
    if (s.side == 0) {
      // switch to prefix side: prefix's first link is one more link
      if (r_after >= 1) {
        State t = prefix_start(C2, s.links, s.w2u, s.ku);
        uint64_t ahead2 = cover(t.line, t.sg, t.en, true, Q{});
        if (feasible(t.C, ahead2, true, remaining_after(c, t.links), c.w2 - t.w2u, c.kmax - t.ku)) {
          Move mv{}; mv.kind = MV_SWITCH; mv.from = s.line; mv.to = t.line; mv.sg_to = t.sg; mv.entry = t.en;
          ch.push_back({t, mv});
        } else pruned_bound++;
      }
      // end-T on the suffix side then switch
      if (c.allow_t && s.ku < c.kmax && r_after >= 2) {
        uint64_t U = ~C2;
        uint64_t x = U & ~L.mask;
        while (x) {
          int p = __builtin_ctzll(x); x &= x - 1;
          uint64_t C3 = C2 | (1ULL << p);
          State t = prefix_start(C3, s.links + 1, s.w2u, s.ku + 1);
          uint64_t ahead2 = cover(t.line, t.sg, t.en, true, Q{});
          if (!feasible(t.C, ahead2, true, remaining_after(c, t.links), c.w2 - t.w2u, c.kmax - t.ku)) { pruned_bound++; continue; }
          Move mv{}; mv.kind = MV_ENDT; mv.from = s.line; mv.p = p; mv.to = t.line; mv.sg_to = t.sg; mv.entry = t.en;
          ch.push_back({t, mv});
        }
      }
    } else if (leaves) {
      Move mv{}; mv.kind = MV_END; mv.from = s.line;
      leaves->push_back({C2, mv});
      if (c.allow_t && s.ku < c.kmax && r_after >= 1) {
        uint64_t x = ~C2 & ~L.mask;
        while (x) {
          int p = __builtin_ctzll(x); x &= x - 1;
          Move m2{}; m2.kind = MV_ENDT; m2.from = s.line; m2.p = p;
          leaves->push_back({C2 | (1ULL << p), m2});
        }
      }
    }
  }
  if (r_after < 1) return;
  // ---- R moves
  const std::vector<Adj>& adjl = (s.w2u >= c.w2) ? ADJ_RICH[s.line] : ADJ[s.line];
  for (const Adj& a : adjl) {
    if (!ahead(s.sg, s.en, a.s)) continue;
    const Line& M = LINES[a.m];
    int w2u = s.w2u + (M.n == 2 ? 1 : 0);
    if (w2u > c.w2) continue;
    uint64_t C2 = s.C | cover(s.line, s.sg, s.en, false, a.s);
    for (int sg2 = -1; sg2 <= 1; sg2 += 2) {
      State t{s.side, a.m, sg2, Ent{false, a.t, true}, C2, s.links + 1, w2u, s.ku, false};
      uint64_t ahead2 = cover(t.line, t.sg, t.en, true, Q{});
      if (!memo.get(t.C, ahead2, M.n >= 3, remaining_after(c, t.links), c.w2 - t.w2u, c.kmax - t.ku)) { pruned_bound++; continue; }
      Move mv{}; mv.kind = MV_R; mv.from = s.line; mv.to = a.m; mv.sg_to = sg2; mv.s = a.s; mv.t = a.t; mv.entry = t.en;
      ch.push_back({t, mv});
    }
  }
  if (s.ku >= c.kmax || r_after < 2) return;
  // ---- F moves (dominating zero-point connector)
  {
    uint64_t C2 = s.C | fullCov;
    for (int mi = 0; mi < (int)LINES.size(); mi++) {
      if (mi == s.line) continue;
      const Line& M = LINES[mi];
      int w2u = s.w2u + (M.n == 2 ? 1 : 0);
      if (w2u > c.w2) continue;
      for (int sg2 = -1; sg2 <= 1; sg2 += 2) {
        State t{s.side, mi, sg2, Ent{true, Q{}, true}, C2, s.links + 2, w2u, s.ku + 1, true};
        uint64_t ahead2 = M.mask;
        if (!memo.get(t.C, ahead2, M.n >= 3, remaining_after(c, t.links), c.w2 - t.w2u, c.kmax - t.ku)) { pruned_bound++; continue; }
        Move mv{}; mv.kind = MV_F; mv.from = s.line; mv.to = mi; mv.sg_to = sg2; mv.entry = t.en;
        ch.push_back({t, mv});
      }
    }
  }
  // ---- T moves (exact one-point transversals)
  if (c.allow_t) {
    uint64_t U = ~s.C & ~L.mask;  // p uncovered and not on L
    std::vector<TOut> outs;
    uint64_t x = U;
    while (x) {
      int p = __builtin_ctzll(x); x &= x - 1;
      for (int mi = 0; mi < (int)LINES.size(); mi++) {
        const Line& M = LINES[mi];
        if (mi == s.line) continue;
        if ((M.mask >> p) & 1) continue;
        int w2u = s.w2u + (M.n == 2 ? 1 : 0);
        if (w2u > c.w2) continue;
        outs.clear();
        gen_T(s.line, s.sg, s.en, p, mi, outs);
        for (const TOut& o : outs) {
          State t{s.side, mi, o.mv.sg_to, o.mv.entry, s.C | o.covL | o.covT, s.links + 2, w2u, s.ku + 1, true};
          uint64_t ahead2 = cover(t.line, t.sg, t.en, true, Q{});
          if (!memo.get(t.C, ahead2, M.n >= 3, remaining_after(c, t.links), c.w2 - t.w2u, c.kmax - t.ku)) { pruned_bound++; continue; }
          ch.push_back({t, o.mv});
        }
      }
    }
  }
}

bool Worker::dfs(const State& s) {
  if (abort) return false;
  nodes++; unit_nodes++;
  if ((nodes & 1023) == 0) {
    if (std::chrono::steady_clock::now() >= deadline) { abort = true; return false; }
  }
  if (unit_limit >= 0 && unit_nodes > unit_limit) { abort = true; return false; }
  if (tt.probe(s)) { pruned_tt++; return false; }
  std::vector<std::pair<State, Move>> ch;
  std::vector<std::pair<uint64_t, Move>> leaves;
  children(s, ch, &leaves);
  bool found = false;
  for (auto& lf : leaves) {
    int links = s.links + (lf.second.kind == MV_ENDT ? 1 : 0);
    record_leaf(lf.first, links, lf.second);
    if (lf.first == ~0ULL) found = true;
  }
  // better children first (more coverage)
  std::stable_sort(ch.begin(), ch.end(), [](const std::pair<State, Move>& a, const std::pair<State, Move>& b) { return __builtin_popcountll(a.first.C) > __builtin_popcountll(b.first.C); });
  for (auto& cm : ch) {
    path.push_back(cm.second);
    bool f = dfs(cm.first);
    path.pop_back();
    if (abort) return found || f;
    found = found || f;
  }
  if (!found && !abort) tt.store(s);
  return found;
}

// ----------------------------------------------------------- serialization
static std::string ent_json(const Ent& e) {
  if (e.inf) return "{\"inf\":true}";
  return std::string("{\"inf\":false,\"e\":\"") + qstr(e.e) + "\",\"closed\":" + (e.closed ? "true" : "false") + "}";
}
static std::string move_json(const Move& m) {
  std::ostringstream o;
  o << "{\"kind\":" << m.kind << ",\"from\":" << m.from << ",\"to\":" << m.to << ",\"sg_to\":" << m.sg_to << ",\"p\":" << m.p
    << ",\"s\":\"" << qstr(m.s) << "\",\"t\":\"" << qstr(m.t) << "\",\"lo\":\"" << qstr(m.lo) << "\",\"hi\":\"" << qstr(m.hi)
    << "\",\"lo_inf\":" << (m.lo_inf ? "true" : "false") << ",\"hi_inf\":" << (m.hi_inf ? "true" : "false") << ",\"entry\":" << ent_json(m.entry) << "}";
  return o.str();
}
static std::string leaf_json(const Leaf& lf, int shard, int unit, const char* bank) {
  std::ostringstream o;
  char hx[32]; snprintf(hx, sizeof hx, "0x%016" PRIx64, lf.C);
  o << "{\"schema\":\"search26-leaf-v1\",\"anchor\":" << ANCHOR_ID << ",\"bank\":\"" << bank << "\",\"shard\":" << shard << ",\"unit\":" << unit << ",\"model_covered\":" << __builtin_popcountll(lf.C)
    << ",\"model_mask_hex\":\"" << hx << "\",\"model_links\":" << lf.links << ",\"path\":[";
  for (size_t i = 0; i < lf.path.size(); i++) { if (i) o << ","; o << move_json(lf.path[i]); }
  o << "]}";
  return o.str();
}

// ---------------------------------------------------------------- anchor
static void setup_anchor() {
  int k0, k1, a, b;
  // prefix (reversed): space diagonal from 000 toward 333 (both anchors)
  PREFIX_LINE = find_line(0, 0, 0, 3, 3, 3, k0, k1);
  PREFIX_K = k0; PREFIX_SG = k1 > k0 ? 1 : -1;
  int ex = find_line(0, 0, 0, 3, 0, 0, a, b);
  int dg = find_line(3, 0, 0, 0, 3, 3, a, b);
  if (ANCHOR_ID == 4) {
    // 000->300->033 fixed; suffix on edge line x=0,z=3 from 033 toward 003
    SUFFIX_LINE = find_line(0, 3, 3, 0, 0, 3, k0, k1);
    SUFFIX_K = k0; SUFFIX_SG = k1 > k0 ? 1 : -1;
    ANCHOR_C0 = LINES[ex].mask | LINES[dg].mask;
    ANCHOR_FIXED_LINKS = 2;
  } else if (ANCHOR_ID == 5) {
    // 000->300->033->003 fixed; suffix on diagonal through 003 and 330 from 003 toward 330
    int ey = find_line(0, 3, 3, 0, 0, 3, a, b);
    SUFFIX_LINE = find_line(0, 0, 3, 3, 3, 0, k0, k1);
    SUFFIX_K = k0; SUFFIX_SG = k1 > k0 ? 1 : -1;
    ANCHOR_C0 = LINES[ex].mask | LINES[dg].mask | LINES[ey].mask;
    ANCHOR_FIXED_LINKS = 3;
  } else throw std::runtime_error("unknown anchor");
  if (SUFFIX_LINE < 0 || PREFIX_LINE < 0 || ex < 0 || dg < 0) throw std::runtime_error("anchor lines missing");
}

// ------------------------------------------------------------- work units
struct Unit { State st; std::vector<Move> path; };
static void make_units(const Config& c, std::vector<Unit>& units) {
  Worker w; w.cfg = &c; w.deadline = std::chrono::steady_clock::time_point::max();
  std::vector<Unit> frontier{Unit{suffix_start(), {}}};
  for (int d = 0; d < c.unit_depth; d++) {
    std::vector<Unit> next;
    for (auto& u : frontier) {
      std::vector<std::pair<State, Move>> ch;
      w.children(u.st, ch, nullptr);  // leaves at shallow depth are re-generated inside units' parents? (no: depth>=1 leaves only exist on prefix side)
      for (auto& cm : ch) { Unit v{cm.first, u.path}; v.path.push_back(cm.second); next.push_back(v); }
    }
    frontier.swap(next);
  }
  units.swap(frontier);
}

// ------------------------------------------------- search27 work-item plans
// A plan line is "PARENT SUBPATH EXTRA": PARENT indexes the classic unit
// frontier at depth unit_depth, SUBPATH ("." or dot-separated child indices)
// descends along children() in their deterministic order, and EXTRA further
// levels are expanded breadth-first.  Every node passed through on the way is
// checked to carry no terminal leaf that could matter (popcount >= save_min),
// so the produced units partition the item's subtree exactly.
struct UnitMeta { int item; int parent; std::string sub; };
static void expand_node(Worker& w, const Unit& u, std::vector<std::pair<Unit, std::string>>& out, const std::string& sub, int extra) {
  if (extra == 0) { out.push_back({u, sub}); return; }
  std::vector<std::pair<State, Move>> ch; std::vector<std::pair<uint64_t, Move>> leaves;
  w.children(u.st, ch, &leaves);
  for (auto& lf : leaves)
    if (__builtin_popcountll(lf.first) >= w.cfg->save_min || __builtin_popcountll(lf.first) >= w.cfg->target)
      throw std::runtime_error("plan split would drop a relevant leaf at " + sub);
  for (int i = 0; i < (int)ch.size(); i++) {
    Unit v{ch[i].first, u.path}; v.path.push_back(ch[i].second);
    expand_node(w, v, out, sub == "." ? std::to_string(i) : sub + "." + std::to_string(i), extra - 1);
  }
}
static void make_plan_units(const Config& c, std::vector<Unit>& units, std::vector<UnitMeta>& meta, int& items) {
  std::vector<Unit> parents; make_units(c, parents);
  Worker w; w.cfg = &c; w.deadline = std::chrono::steady_clock::time_point::max();
  std::ifstream in(c.plan_file);
  if (!in) throw std::runtime_error("cannot open plan " + c.plan_file);
  std::string line; items = 0;
  while (std::getline(in, line)) {
    if (line.empty() || line[0] == '#') continue;
    std::istringstream ls(line); int parent = -1, extra = -1; std::string sub;
    if (!(ls >> parent >> sub >> extra) || parent < 0 || parent >= (int)parents.size() || extra < 0 || extra > 3)
      throw std::runtime_error("bad plan line: " + line);
    Unit cur = parents[parent];
    if (sub != ".") {
      std::stringstream ss(sub); std::string tok;
      while (std::getline(ss, tok, '.')) {
        int idx = std::stoi(tok);
        std::vector<std::pair<State, Move>> ch; std::vector<std::pair<uint64_t, Move>> leaves;
        w.children(cur.st, ch, &leaves);
        for (auto& lf : leaves)
          if (__builtin_popcountll(lf.first) >= c.save_min || __builtin_popcountll(lf.first) >= c.target)
            throw std::runtime_error("plan descent passes a relevant leaf: " + line);
        if (idx < 0 || idx >= (int)ch.size()) throw std::runtime_error("plan child index out of range: " + line);
        Unit v{ch[idx].first, cur.path}; v.path.push_back(ch[idx].second); cur = v;
      }
    }
    std::vector<std::pair<Unit, std::string>> out;
    expand_node(w, cur, out, sub, extra);
    for (auto& o : out) { units.push_back(o.first); meta.push_back({items, parent, o.second}); }
    items++;
  }
}

// ------------------------------------------------------------- self tests
static int selftest() {
  int fails = 0;
  // 1. line census
  int n2 = 0, n3 = 0, n4 = 0;
  for (auto& l : LINES) { if (l.n == 2) n2++; else if (l.n == 3) n3++; else if (l.n == 4) n4++; }
  printf("selftest: lines=%zu n2=%d n3=%d n4=%d\n", LINES.size(), n2, n3, n4);
  if (LINES.size() != 1492 || n2 != 1344 || n3 != 72 || n4 != 76) { printf("FAIL line census\n"); fails++; }
  // 2. T generator vs dense numeric sampling (sound completeness check)
  std::mt19937_64 rng(2026);
  int checked = 0, missing = 0;
  for (int trial = 0; trial < 4000; trial++) {
    int li = (int)(rng() % LINES.size()), mi = (int)(rng() % LINES.size());
    if (li == mi) continue;
    int p = (int)(rng() % 64);
    if ((LINES[li].mask >> p) & 1 || (LINES[mi].mask >> p) & 1) continue;
    // prefer coplanar configurations half of the time
    P3 A = lineA(LINES[li]), d = lineD(LINES[li]), pp = pint(p / 16, (p / 4) % 4, p % 4);
    P3 nrm = pcross(d, psub(pp, A));
    bool cop = qsign(pdot(nrm, lineD(LINES[mi]))) == 0 && qsign(pdot(nrm, psub(lineA(LINES[mi]), A))) == 0;
    if (!cop && (trial % 2 == 0)) continue;
    int sg = (rng() & 1) ? 1 : -1;
    Ent en; en.inf = true;
    std::vector<TOut> outs; gen_T(li, sg, en, p, mi, outs);
    // sample s on a fine grid of rationals
    for (int si = -80; si <= 120; si++) {
      Q s = mkq(si, 16);
      Q t; P3 X, Y;
      if (!tparam_of(A, d, pp, LINES[mi], s, t, X, Y)) continue;
      uint64_t covL = cover(li, sg, en, false, s);
      for (int sg2 = -1; sg2 <= 1; sg2 += 2) {
        uint64_t covT = seg_mask_exact(X, Y);
        // future coverage on M from entry t (closed) to infinity
        Ent e2; e2.inf = false; e2.e = t; e2.closed = true;
        uint64_t covM = cover(mi, sg2, e2, true, Q{});
        checked++;
        bool dominated = false;
        for (const TOut& o : outs) {
          if (o.mv.sg_to != sg2) continue;
          uint64_t cm = cover(mi, sg2, o.mv.entry, true, Q{});
          if ((covL & ~o.covL) == 0 && (covT & ~o.covT) == 0 && (covM & ~cm) == 0) {
            // entry must not be strictly ahead of the sampled t
            if (o.mv.entry.inf || qcmp(o.mv.entry.e, t) * sg2 <= 0) { dominated = true; break; }
          }
        }
        if (!dominated) missing++;
      }
    }
  }
  printf("selftest: T samples checked=%d undominated=%d\n", checked, missing);
  if (missing) { printf("FAIL T generator completeness\n"); fails++; }
  if (checked < 1000) { printf("FAIL too few T samples\n"); fails++; }
  return fails;
}

// -------------------------------------------------------------- replay test
// Replays an explicit move list (JSON-free compact form given by the Python
// preflight) and prints the final model coverage, to prove that known trails
// are members of the searched class.
static int replay(const Config& c, const char* file) {
  std::ifstream in(file);
  if (!in) { printf("cannot open %s\n", file); return 2; }
  // format: lines of "R toLine sgTo" | "F toLine sgTo" | "T p toLine sgTo" | "SWITCH" | "END" | "ENDT p"
  Worker w; w.cfg = &c; w.deadline = std::chrono::steady_clock::time_point::max();
  State s = suffix_start();
  std::string op;
  std::vector<Move> rpath;
  while (in >> op) {
    std::vector<std::pair<State, Move>> ch; std::vector<std::pair<uint64_t, Move>> leaves;
    w.children(s, ch, &leaves);
    if (op == "END" || op == "ENDTL") {
      int p = -1; if (op == "ENDTL") in >> p;
      for (auto& lf : leaves) if ((op == "END" && lf.second.kind == MV_END) || (op == "ENDTL" && lf.second.kind == MV_ENDT && lf.second.p == p)) {
        printf("replay: final model coverage %d links %d\n", __builtin_popcountll(lf.first), s.links + (op == "ENDTL" ? 1 : 0));
        Leaf L1; L1.path = rpath; L1.path.push_back(lf.second); L1.C = lf.first; L1.links = s.links;
        printf("LEAF %s\n", leaf_json(L1, -1, -1, "replay").c_str());
        return 0;
      }
      printf("replay: END not available (pruned)\n"); return 1;
    }
    int want_kind = -1, to = -1, sg2 = 0, p = -1;
    if (op == "R") { want_kind = MV_R; in >> to >> sg2; }
    else if (op == "F") { want_kind = MV_F; in >> to >> sg2; }
    else if (op == "T") { want_kind = -2; in >> p >> to >> sg2; }
    else if (op == "SWITCH") { want_kind = MV_SWITCH; }
    else if (op == "ENDT") { want_kind = MV_ENDT; in >> p; }
    bool ok = false; uint64_t bestC = 0; State bestS{}; Move bestM{};
    for (auto& cm : ch) {
      const Move& m = cm.second;
      bool match = false;
      if (want_kind == MV_SWITCH) match = m.kind == MV_SWITCH;
      else if (want_kind == MV_ENDT) match = m.kind == MV_ENDT && m.p == p;
      else if (want_kind == -2) match = (m.kind == MV_T || m.kind == MV_TC) && m.p == p && m.to == to && m.sg_to == sg2;
      else match = m.kind == want_kind && m.to == to && m.sg_to == sg2;
      if (match && (!ok || __builtin_popcountll(cm.first.C) > __builtin_popcountll(bestC) || (cm.first.C == bestC && cm.first.en.inf))) { ok = true; bestC = cm.first.C; bestS = cm.first; bestM = cm.second; }
    }
    if (!ok) { printf("replay: move %s %d %d %d not generated (links=%d)\n", op.c_str(), to, sg2, p, s.links); return 1; }
    s = bestS; rpath.push_back(bestM);
    printf("replay: %s -> covered %d links %d w2 %d k %d\n", op.c_str(), __builtin_popcountll(s.C), s.links, s.w2u, s.ku);
  }
  return 1;
}

// -------------------------------------------------------------- knuth mode
static double knuth_from(const Config& c, const State& root, int probes, std::mt19937_64& rng, int& bestseen) {
  Worker w; w.cfg = &c; w.deadline = std::chrono::steady_clock::time_point::max();
  std::vector<double> lev(64, 0.0);
  double total = 0;
  for (int pr = 0; pr < probes; pr++) {
    State s = root;
    double prod = 1; int depth = 0; lev[0] += 1;
    while (true) {
      std::vector<std::pair<State, Move>> ch; std::vector<std::pair<uint64_t, Move>> leaves;
      w.children(s, ch, &leaves);
      for (auto& lf : leaves) bestseen = std::max(bestseen, __builtin_popcountll(lf.first));
      if (ch.empty()) break;
      prod *= (double)ch.size(); depth++; lev[depth] += prod;
      s = ch[rng() % ch.size()].first;
    }
  }
  for (int i = 0; i < 64; i++) if (lev[i] > 0) total += lev[i] / probes;
  return total;
}
struct Unit;
static void make_units(const Config& c, std::vector<Unit>& units);
static void knuth(const Config& c, int probes, uint64_t seed) {
  std::mt19937_64 rng(seed); int bestseen = 0;
  double total = knuth_from(c, suffix_start(), probes, rng, bestseen);
  printf("{\"mode\":\"knuth\",\"anchor\":%d,\"w2\":%d,\"k\":%d,\"allow_t\":%d,\"links\":%d,\"target\":%d,\"probes\":%d,\"estimated_nodes\":%.6g,\"best_leaf_seen\":%d}\n", ANCHOR_ID, c.w2, c.kmax, c.allow_t, c.total_links, c.target, probes, total, bestseen);
}

// --------------------------------------------------------------------- main
static void usage() {
  fprintf(stderr,
          "usage: anchored_exact MODE [key=value ...]\n"
          "  MODE: selftest | knuth | replay | units | plancount | search\n"
          "  keys: anchor=5 links=22 w2=0 k=1 allow_t=0 target=64 unit_depth=3 shards=20 shard=0 threads=4\n"
          "        seconds=60 tt_mb=512 save_min=63 max_saved=2000 out=DIR unit_node_limit=-1\n"
          "        probes=1000 seed=1 (knuth)  file=PATH (replay)  plan=PATH (search/plancount: work items)\n");
}
int main(int argc, char** argv) {
  try {
    if (argc < 2) { usage(); return 2; }
    std::string mode = argv[1];
    Config c;
    int probes = 1000; uint64_t seed = 1; std::string file;
    for (int i = 2; i < argc; i++) {
      std::string a = argv[i]; auto eq = a.find('=');
      if (eq == std::string::npos) { usage(); return 2; }
      std::string k = a.substr(0, eq), v = a.substr(eq + 1);
      if (k == "anchor") ANCHOR_ID = std::stoi(v);
      else if (k == "links") c.total_links = std::stoi(v);
      else if (k == "w2") c.w2 = std::stoi(v);
      else if (k == "k") c.kmax = std::stoi(v);
      else if (k == "allow_t") c.allow_t = std::stoi(v);
      else if (k == "target") { c.target = std::stoi(v); }
      else if (k == "unit_depth") c.unit_depth = std::stoi(v);
      else if (k == "shards") c.shards = std::stoi(v);
      else if (k == "shard") c.shard = std::stoi(v);
      else if (k == "threads") c.threads = std::stoi(v);
      else if (k == "seconds") c.seconds = std::stod(v);
      else if (k == "tt_mb") c.tt_mb = std::stoull(v);
      else if (k == "save_min") c.save_min = std::stoi(v);
      else if (k == "max_saved") c.max_saved = std::stoi(v);
      else if (k == "out") c.out_dir = v;
      else if (k == "unit_node_limit") c.unit_node_limit = std::stoll(v);
      else if (k == "probes") probes = std::stoi(v);
      else if (k == "seed") seed = std::stoull(v);
      else if (k == "file") file = v;
      else if (k == "plan") c.plan_file = v;
      else { fprintf(stderr, "unknown option %s\n", k.c_str()); usage(); return 2; }
    }
    if (c.w2 < 0 || c.w2 > 15 || c.kmax < 0 || c.kmax > 15 || c.total_links < 8 || c.total_links > 30 || c.threads < 1 || c.threads > 16 ||
        c.target < 1 || c.target > 64 || c.shards < 1 || c.shard < 0 || c.shard >= c.shards || c.unit_depth < 0 || c.unit_depth > 4) {
      fprintf(stderr, "bad config\n"); return 2;
    }
    SLACK = 64 - c.target;
    build_lines();
    setup_anchor();
    if (mode == "selftest") { int f = selftest(); printf("selftest %s\n", f ? "FAIL" : "PASS"); return f ? 1 : 0; }
    if (mode == "knuth") { knuth(c, probes, seed); return 0; }
    if (mode == "replay") return replay(c, file.c_str());
    if (mode == "unitsizes") {
      std::vector<Unit> u; make_units(c, u);
      std::mt19937_64 rng(seed); int bs = 0;
      std::vector<double> est;
      int sample = std::min<int>(probes, (int)u.size());
      for (int i = 0; i < sample; i++) { size_t idx = (size_t)(rng() % u.size()); est.push_back(knuth_from(c, u[idx].st, 200, rng, bs)); }
      std::sort(est.begin(), est.end());
      double sum = 0; for (double e : est) sum += e;
      printf("{\"units\":%zu,\"sampled\":%d,\"mean\":%.4g,\"median\":%.4g,\"p90\":%.4g,\"p99\":%.4g,\"max\":%.4g,\"total_est\":%.4g}\n", u.size(), sample,
             sum / sample, est[sample / 2], est[(int)(sample * 0.9)], est[(int)(sample * 0.99)], est.back(), sum / sample * u.size());
      return 0;
    }
    if (mode == "units") { std::vector<Unit> u; make_units(c, u); printf("{\"units\":%zu}\n", u.size()); return 0; }
    if (mode == "plancount") {
      std::vector<Unit> u; std::vector<UnitMeta> m; int items = 0; make_plan_units(c, u, m, items);
      printf("{\"items\":%d,\"units\":%zu}\n", items, u.size()); return 0;
    }
    if (mode != "search") { usage(); return 2; }
    auto t0 = std::chrono::steady_clock::now();
    std::vector<Unit> units; std::vector<UnitMeta> meta; int planItems = 0;
    if (c.plan_file.empty()) make_units(c, units); else make_plan_units(c, units, meta, planItems);
    std::vector<int> mine;
    for (int i = 0; i < (int)units.size(); i++) if (i % c.shards == c.shard) mine.push_back(i);
    std::atomic<int> next{0};
    std::mutex io;
    std::string unitsPath = c.out_dir + "/units.jsonl", leavesPath = c.out_dir + "/leaves.jsonl";
    FILE* fu = fopen(unitsPath.c_str(), "w"); FILE* fl = fopen(leavesPath.c_str(), "w");
    if (!fu || !fl) { fprintf(stderr, "cannot open outputs in %s\n", c.out_dir.c_str()); return 3; }
    auto deadline = t0 + std::chrono::milliseconds((int64_t)(c.seconds * 1000));
    std::vector<Worker> ws(c.threads);
    int64_t totNodes = 0, totBound = 0, totTT = 0; int completed = 0, open = 0, notStarted = 0, globalBest = 0, nFull = 0, nSaved = 0;
    std::vector<std::thread> th;
    for (int ti = 0; ti < c.threads; ti++) {
      th.emplace_back([&, ti]() {
        Worker& w = ws[ti]; w.cfg = &c; w.deadline = deadline; w.tt.init(c.tt_mb); w.unit_limit = c.unit_node_limit;
        while (true) {
          int idx = next.fetch_add(1);
          if (idx >= (int)mine.size()) break;
          int u = mine[idx];
          if (std::chrono::steady_clock::now() >= deadline) {
            std::lock_guard<std::mutex> g(io);
            if (meta.empty()) fprintf(fu, "{\"unit\":%d,\"status\":\"not_started\",\"nodes\":0}\n", u);
            else fprintf(fu, "{\"unit\":%d,\"item\":%d,\"parent\":%d,\"sub\":\"%s\",\"status\":\"not_started\",\"nodes\":0}\n", u, meta[u].item, meta[u].parent, meta[u].sub.c_str());
            notStarted++;
            continue;
          }
          w.abort = false; w.unit_nodes = 0; w.best = 0; w.saved.clear(); w.full.clear();
          w.path = units[u].path;
          auto ts = std::chrono::steady_clock::now();
          w.dfs(units[u].st);
          double sec = std::chrono::duration<double>(std::chrono::steady_clock::now() - ts).count();
          std::lock_guard<std::mutex> g(io);
          bool done = !w.abort;
          if (done) completed++; else open++;
          globalBest = std::max(globalBest, w.best);
          if (meta.empty())
            fprintf(fu, "{\"unit\":%d,\"status\":\"%s\",\"nodes\":%" PRId64 ",\"seconds\":%.3f,\"best_model_covered\":%d,\"full_leaves\":%zu,\"saved_leaves\":%zu}\n",
                    u, done ? "complete" : "open", w.unit_nodes, sec, w.best, w.full.size(), w.saved.size());
          else
            fprintf(fu, "{\"unit\":%d,\"item\":%d,\"parent\":%d,\"sub\":\"%s\",\"status\":\"%s\",\"nodes\":%" PRId64 ",\"seconds\":%.3f,\"best_model_covered\":%d,\"full_leaves\":%zu,\"saved_leaves\":%zu}\n",
                    u, meta[u].item, meta[u].parent, meta[u].sub.c_str(), done ? "complete" : "open", w.unit_nodes, sec, w.best, w.full.size(), w.saved.size());
          for (auto& lf : w.full) { fprintf(fl, "%s\n", leaf_json(lf, c.shard, u, "full").c_str()); nFull++; }
          for (auto& lf : w.saved) { if (nSaved < c.max_saved) { fprintf(fl, "%s\n", leaf_json(lf, c.shard, u, "near").c_str()); nSaved++; } }
          fflush(fu); fflush(fl);
        }
      });
    }
    for (auto& t : th) t.join();
    for (auto& w : ws) { totNodes += w.nodes; totBound += w.pruned_bound; totTT += w.pruned_tt; }
    fclose(fu); fclose(fl);
    double el = std::chrono::duration<double>(std::chrono::steady_clock::now() - t0).count();
    std::string sp = c.out_dir + "/engine_summary.json";
    FILE* fs = fopen(sp.c_str(), "w");
    if (!fs) return 3;
    fprintf(fs, "{\"schema\":\"search26-engine-summary-v1\",\"anchor\":%d,\"allow_t\":%d,\"target\":%d,\"links\":%d,\"w2\":%d,\"k\":%d,\"unit_depth\":%d,\"shards\":%d,\"shard\":%d,\"threads\":%d,\"seconds_budget\":%.1f,\"elapsed\":%.3f,"
                "\"units_total\":%zu,\"units_assigned\":%zu,\"units_complete\":%d,\"units_open\":%d,\"units_not_started\":%d,\"nodes\":%" PRId64 ",\"pruned_bound\":%" PRId64 ",\"pruned_tt\":%" PRId64 ","
                "\"best_model_covered\":%d,\"full_leaves\":%d,\"saved_leaves\":%d,\"tt_mb_per_thread\":%" PRIu64 "}\n",
            ANCHOR_ID, c.allow_t, c.target, c.total_links, c.w2, c.kmax, c.unit_depth, c.shards, c.shard, c.threads, c.seconds, el, units.size(), mine.size(), completed, open, notStarted, totNodes, totBound, totTT, globalBest, nFull, nSaved, c.tt_mb);
    fclose(fs);
    printf("done: units %zu complete %d open %d not_started %d nodes %" PRId64 " best %d full %d\n", mine.size(), completed, open, notStarted, totNodes, globalBest, nFull);
    return 0;
  } catch (const std::exception& ex) {
    fprintf(stderr, "fatal: %s\n", ex.what());
    return 4;
  }
}
