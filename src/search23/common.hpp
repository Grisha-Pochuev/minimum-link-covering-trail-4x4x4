#pragma once
#include <algorithm>
#include <array>
#include <atomic>
#include <chrono>
#include <cmath>
#include <cstdint>
#include <cstdlib>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <limits>
#include <map>
#include <mutex>
#include <numeric>
#include <optional>
#include <random>
#include <set>
#include <sstream>
#include <stdexcept>
#include <string>
#include <thread>
#include <tuple>
#include <unordered_map>
#include <unordered_set>
#include <utility>
#include <vector>

namespace search23 {

using Clock = std::chrono::steady_clock;

struct Point {
    int x{}, y{}, z{};
    bool operator==(const Point& o) const { return x == o.x && y == o.y && z == o.z; }
    bool operator!=(const Point& o) const { return !(*this == o); }
    bool operator<(const Point& o) const { return std::tie(x,y,z) < std::tie(o.x,o.y,o.z); }
};

struct PointHash {
    std::size_t operator()(const Point& p) const noexcept {
        std::size_t h = 1469598103934665603ULL;
        for (int v : {p.x,p.y,p.z}) { h ^= static_cast<std::uint64_t>(static_cast<std::int64_t>(v)); h *= 1099511628211ULL; }
        return h;
    }
};

struct LineKey {
    int dx{},dy{},dz{},cx{},cy{},cz{};
    bool operator==(const LineKey& o) const {
        return std::tie(dx,dy,dz,cx,cy,cz)==std::tie(o.dx,o.dy,o.dz,o.cx,o.cy,o.cz);
    }
    bool operator<(const LineKey& o) const {
        return std::tie(dx,dy,dz,cx,cy,cz)<std::tie(o.dx,o.dy,o.dz,o.cx,o.cy,o.cz);
    }
};

struct LineKeyHash {
    std::size_t operator()(const LineKey& k) const noexcept {
        std::size_t h=1469598103934665603ULL;
        for(int v:{k.dx,k.dy,k.dz,k.cx,k.cy,k.cz}){h^=static_cast<std::uint64_t>(static_cast<std::int64_t>(v));h*=1099511628211ULL;}
        return h;
    }
};

struct Seed {
    std::string kind;
    std::string id;
    int covered{};
    std::vector<Point> missing;
    std::vector<Point> vertices;
};

struct Eval {
    bool valid{false};
    std::uint64_t mask{0};
    int covered{0};
    std::vector<Point> missing;
    std::array<int,22> point_counts{};
    std::array<int,22> gains{};
    int core_overlap{0};
    int unique_link_count{0};
    int unique_point_count{0};
    int zero_exclusive_links{0};
};

struct State {
    std::string parent_id;
    std::string donor_id;
    std::string operation;
    int worker{-1};
    std::uint64_t effective_seed{0};
    std::vector<Point> vertices;
    Eval eval;
    int parent_defects_closed{0};
    std::uint64_t raw_hash{0};
};

struct Options {
    std::string repo{"."};
    std::string outdir{"results/core_transplant"};
    int seconds{180};
    int workers{4};
    std::uint64_t seed{20260723};
    int shard{0};
    int shards{20};
    int beam_width{2000};
    std::uint64_t state_cap{100000};
    int save_min_covered{60};
    int top_diverse{200};
    int checkpoint_seconds{60};
};

struct WorkerResult {
    State best;
    State best_escape;
    std::uint64_t attempts{0};
    std::uint64_t valid_attempts{0};
    std::uint64_t changed_core_attempts{0};
    int min_core_overlap{22};
    std::vector<State> saved;
    std::vector<State> diagnostics;
};

struct SharedProgress {
    std::mutex mutex;
    State best;
    bool has_best{false};
    std::atomic<std::uint64_t> attempts{0};
    std::atomic<std::uint64_t> valid_attempts{0};
    std::atomic<std::uint64_t> changed_core_attempts{0};
    std::atomic<int> min_core_overlap{22};
    std::atomic<bool> found64{false};
};

int gcd3(int a,int b,int c){return std::gcd(std::gcd(std::abs(a),std::abs(b)),std::abs(c));}

LineKey line_key(const Point& a,const Point& b){
    int dx=b.x-a.x,dy=b.y-a.y,dz=b.z-a.z;
    int g=gcd3(dx,dy,dz);
    if(g==0) throw std::runtime_error("zero line");
    dx/=g;dy/=g;dz/=g;
    if(dx<0 || (dx==0&&dy<0) || (dx==0&&dy==0&&dz<0)){dx=-dx;dy=-dy;dz=-dz;}
    int cx=a.y*dz-a.z*dy;
    int cy=a.z*dx-a.x*dz;
    int cz=a.x*dy-a.y*dx;
    return {dx,dy,dz,cx,cy,cz};
}

std::uint64_t segment_mask(const Point& a,const Point& b){
    long long vx=b.x-a.x,vy=b.y-a.y,vz=b.z-a.z;
    long long norm=vx*vx+vy*vy+vz*vz;
    if(norm==0) return 0;
    std::uint64_t mask=0;
    int idx=0;
    for(int x=0;x<4;++x) for(int y=0;y<4;++y) for(int z=0;z<4;++z,++idx){
        long long wx=2*x-a.x,wy=2*y-a.y,wz=2*z-a.z;
        long long c1=wy*vz-wz*vy,c2=wz*vx-wx*vz,c3=wx*vy-wy*vx;
        long long dot=wx*vx+wy*vy+wz*vz;
        if(c1==0&&c2==0&&c3==0&&dot>=0&&dot<=norm) mask|=(1ULL<<idx);
    }
    return mask;
}

std::vector<Point> missing_from_mask(std::uint64_t mask){
    std::vector<Point> out;
    int idx=0;
    for(int x=0;x<4;++x) for(int y=0;y<4;++y) for(int z=0;z<4;++z,++idx)
        if(((mask>>idx)&1ULL)==0) out.push_back({x,y,z});
    return out;
}

std::uint64_t raw_hash(const std::vector<Point>& v){
    std::uint64_t h=1469598103934665603ULL;
    for(const auto&p:v) for(int x:{p.x,p.y,p.z}) {h^=static_cast<std::uint64_t>(static_cast<std::int64_t>(x));h*=1099511628211ULL;}
    return h;
}

std::string hex16(std::uint64_t x){std::ostringstream o;o<<std::hex<<std::setw(16)<<std::setfill('0')<<x;return o.str();}

std::vector<std::string> split(const std::string&s,char d){
    std::vector<std::string> out;std::string cur;std::istringstream in(s);while(std::getline(in,cur,d))out.push_back(cur);return out;
}

Point parse_point(const std::string&s){auto p=split(s,',');if(p.size()!=3)throw std::runtime_error("bad point: "+s);return {std::stoi(p[0]),std::stoi(p[1]),std::stoi(p[2])};}

std::vector<Point> parse_points(const std::string&s){std::vector<Point> v;if(s.empty())return v;for(auto&t:split(s,';'))v.push_back(parse_point(t));return v;}

std::vector<Seed> load_seeds(const std::string& path){
    std::ifstream in(path);if(!in)throw std::runtime_error("cannot open "+path);
    std::vector<Seed> rows;std::string line;
    while(std::getline(in,line)){
        if(line.empty())continue;auto f=split(line,'\t');if(f.size()!=5)throw std::runtime_error("bad seed tsv");
        Seed s;s.kind=f[0];s.id=f[1];s.covered=std::stoi(f[2]);s.missing=parse_points(f[3]);s.vertices=parse_points(f[4]);
        if(s.vertices.size()!=23)throw std::runtime_error("seed does not have 23 vertices: "+s.id);
        rows.push_back(std::move(s));
    }
    return rows;
}

std::unordered_set<LineKey,LineKeyHash> load_core(const std::string& path){
    std::ifstream in(path);if(!in)throw std::runtime_error("cannot open core "+path);
    std::unordered_set<LineKey,LineKeyHash> s;int a,b,c,d,e,f;while(in>>a>>b>>c>>d>>e>>f)s.insert({a,b,c,d,e,f});
    if(s.size()!=18)throw std::runtime_error("frozen core must have 18 lines");return s;
}

Eval evaluate(const std::vector<Point>& v,const std::unordered_set<LineKey,LineKeyHash>& core){
    Eval e;if(v.size()!=23)return e;
    std::array<std::uint64_t,22> masks{};
    for(int i=0;i<22;++i){
        if(v[i]==v[i+1])return e;
        masks[i]=segment_mask(v[i],v[i+1]);
        e.point_counts[i]=__builtin_popcountll(masks[i]);
        try{if(core.count(line_key(v[i],v[i+1])))++e.core_overlap;}catch(...){return e;}
    }
    std::uint64_t covered=0;
    for(int i=0;i<22;++i){e.gains[i]=__builtin_popcountll(masks[i]&~covered);covered|=masks[i];}
    e.mask=covered;e.covered=__builtin_popcountll(covered);e.missing=missing_from_mask(covered);
    std::array<int,64> occurrence{};
    for(auto m:masks) for(int b=0;b<64;++b) if((m>>b)&1ULL) occurrence[b]++;
    for(int i=0;i<22;++i){int ex=0;for(int b=0;b<64;++b)if(((masks[i]>>b)&1ULL)&&occurrence[b]==1)++ex;if(ex>0){++e.unique_link_count;e.unique_point_count+=ex;}else ++e.zero_exclusive_links;}
    e.valid=true;return e;
}

int defects_closed(const Seed& parent,std::uint64_t mask){
    int n=0;for(const auto&p:parent.missing){int idx=(p.x*4+p.y)*4+p.z;if((mask>>idx)&1ULL)++n;}return n;
}

long long score_coverage(const State&s){
    return static_cast<long long>(s.eval.covered)*1000000000LL + static_cast<long long>(s.parent_defects_closed)*10000000LL + static_cast<long long>(18-s.eval.core_overlap)*100000LL + static_cast<long long>(s.eval.unique_link_count)*1000LL - static_cast<long long>(s.eval.zero_exclusive_links)*100LL;
}

long long score_escape(const State&s){
    return static_cast<long long>(s.eval.covered)*1000000LL + static_cast<long long>(18-s.eval.core_overlap)*10000LL + static_cast<long long>(s.eval.unique_link_count)*100LL - s.eval.zero_exclusive_links;
}

bool better_cov(const State&a,const State&b){return score_coverage(a)>score_coverage(b);}
bool better_escape(const State&a,const State&b){return score_escape(a)>score_escape(b);}

std::array<int,3> permute_coords(const Point&p,int perm){
    static const int ps[6][3]={{0,1,2},{0,2,1},{1,0,2},{1,2,0},{2,0,1},{2,1,0}};
    int a[3]={p.x,p.y,p.z};return {a[ps[perm][0]],a[ps[perm][1]],a[ps[perm][2]]};
}

Point transform_point(const Point&p,int sym){
    int perm=sym/8, refl=sym%8;auto q=permute_coords(p,perm);Point r{q[0],q[1],q[2]};
    if(refl&1)r.x=6-r.x;if(refl&2)r.y=6-r.y;if(refl&4)r.z=6-r.z;return r;
}

std::vector<Point> transformed_vertices(const std::vector<Point>&v,int sym,bool reverse){
    std::vector<Point> o;o.reserve(v.size());for(auto&p:v)o.push_back(transform_point(p,sym));if(reverse)std::reverse(o.begin(),o.end());return o;
}

template<class Rng> int randint(Rng&r,int lo,int hi){std::uniform_int_distribution<int>d(lo,hi);return d(r);}
template<class Rng> bool chance(Rng&r,double p){std::bernoulli_distribution d(p);return d(r);}

std::pair<int,int> region_range(int region,int len){
    int max_start=22-len;
    int lo=(max_start+1)*region/4;
    int hi=(max_start+1)*(region+1)/4-1;
    if(region==3)hi=max_start;
    if(hi<lo)hi=lo;
    return {lo,hi};
}

bool nonzero_path(const std::vector<Point>&v){for(std::size_t i=0;i+1<v.size();++i)if(v[i]==v[i+1])return false;return v.size()==23;}

struct MutationResult {std::vector<Point> vertices;std::string donor_id;std::string operation;};

} // namespace search23
