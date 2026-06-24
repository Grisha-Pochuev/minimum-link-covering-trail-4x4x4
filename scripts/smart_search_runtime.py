from __future__ import annotations

import argparse
import heapq
import json
import math
import random
import time
from collections import Counter, defaultdict
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

GRID = [(2*x, 2*y, 2*z) for x in range(4) for y in range(4) for z in range(4)]
FULL = (1 << 64) - 1
V = []
ADJ = {}
STARTS = []
WEIGHTS = [1.0] * 64
SEEDS = []


def sub(a, b):
    return (a[0]-b[0], a[1]-b[1], a[2]-b[2])


def dot(a, b):
    return a[0]*b[0] + a[1]*b[1] + a[2]*b[2]


def cross(a, b):
    return (a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0])


def onseg(a, b, p):
    d = sub(b, a)
    if d == (0, 0, 0):
        return p == a
    ap = sub(p, a)
    return cross(d, ap) == (0, 0, 0) and 0 <= dot(ap, d) <= dot(d, d)


def maskseg(a, b):
    minx, maxx = sorted((a[0], b[0]))
    miny, maxy = sorted((a[1], b[1]))
    minz, maxz = sorted((a[2], b[2]))
    if maxx < 0 or maxy < 0 or maxz < 0 or minx > 6 or miny > 6 or minz > 6:
        return 0
    m = 0
    for i, p in enumerate(GRID):
        if p[0] < minx or p[0] > maxx or p[1] < miny or p[1] > maxy or p[2] < minz or p[2] > maxz:
            continue
        if onseg(a, b, p):
            m |= 1 << i
    return m


def missing(m):
    return [[p[0]//2, p[1]//2, p[2]//2] for i, p in enumerate(GRID) if not ((m >> i) & 1)]


def pidx(p):
    return int(p[0])*16 + int(p[1])*4 + int(p[2])


def wgain(m):
    s = 0.0
    while m:
        b = m & -m
        i = b.bit_length() - 1
        s += WEIGHTS[i]
        m ^= b
    return s


def scaled_vertices(d):
    if d.get("vertices2"):
        scale = int(d.get("coordinate_scale", 2) or 2)
        out = []
        for p in d.get("vertices2") or []:
            if scale == 2:
                out.append((int(p[0]), int(p[1]), int(p[2])))
            else:
                out.append((round(2*int(p[0])/scale), round(2*int(p[1])/scale), round(2*int(p[2])/scale)))
        return out
    if d.get("vertices"):
        return [(2*int(p[0]), 2*int(p[1]), 2*int(p[2])) for p in d.get("vertices") or []]
    return []


def read_prior(root):
    rows = []
    freq = Counter()
    seen = set()
    seeds = []
    for f in Path(root).glob("**/*.json"):
        try:
            d = json.loads(f.read_text())
        except Exception:
            continue
        if "covered_count" not in d or "missing" not in d:
            continue
        verts = scaled_vertices(d)
        rows.append((int(d.get("covered_count", 0)), str(f), verts))
        for p in d.get("missing", []):
            try:
                freq[tuple(int(x) for x in p)] += 1
            except Exception:
                pass
    rows.sort(key=lambda r: r[0], reverse=True)
    for cov, src, verts in rows:
        key = json.dumps(verts, sort_keys=True)
        if cov < 50 or not verts or key in seen:
            continue
        seen.add(key)
        seeds.append(verts)
        if len(seeds) >= 96:
            break
    weights = [1.0] * 64
    for p, c in freq.items():
        if len(p) == 3 and all(0 <= x < 4 for x in p):
            weights[pidx(p)] += min(3.5, 0.08*c)
    return seeds, weights, rows[:8]


def mode_for(shard):
    if shard <= 5:
        return "warm22", 22
    if shard <= 7:
        return "targeted_warm22", 22
    if shard <= 9:
        return "fractional22", 22
    if shard <= 11:
        return "catalog22", 22
    if shard == 12:
        return "strict21", 21
    if shard <= 14:
        return "layer_cube22", 22
    return "integer22_control", 22


def make_vertices(mode, seeds):
    pts = set()
    if mode in ("fractional22", "catalog22", "layer_cube22"):
        for x in range(-2, 9):
            for y in range(-2, 9):
                for z in range(-2, 9):
                    pts.add((x, y, z))
        for sp in seeds:
            for p in sp:
                if all(-4 <= c <= 10 for c in p):
                    pts.add(p)
    else:
        for x in range(-6, 15, 2):
            for y in range(-6, 15, 2):
                for z in range(-6, 15, 2):
                    pts.add((x, y, z))
        for sp in seeds:
            for p in sp:
                pts.add(p)
    return sorted(pts)


def build(mode, cap):
    adj = defaultdict(list)
    starts = []
    for i, a in enumerate(V):
        for j in range(i+1, len(V)):
            b = V[j]
            m = maskseg(a, b)
            hits = m.bit_count()
            if not hits:
                continue
            length = dot(sub(b, a), sub(b, a))
            base = int(hits*4000 + wgain(m)*450 - min(length, 500))
            if mode == "strict21" and hits < 3:
                base -= 3000
            if mode == "targeted_warm22":
                base += int(wgain(m)*500)
            if mode == "layer_cube22":
                layers = set()
                blocks = set()
                for k, p in enumerate(GRID):
                    if (m >> k) & 1:
                        x, y, z = p[0]//2, p[1]//2, p[2]//2
                        layers.update((("x", x), ("y", y), ("z", z)))
                        blocks.add((x//2, y//2, z//2))
                base += 120*len(layers) + 260*len(blocks)
            adj[i].append((j, m, base, hits))
            adj[j].append((i, m, base, hits))
            starts += [(i, j, m, base, hits), (j, i, m, base, hits)]
    for u in list(adj):
        adj[u].sort(key=lambda t: (t[1].bit_count(), t[2]), reverse=True)
        if cap and len(adj[u]) > cap:
            adj[u] = adj[u][:cap]
    starts.sort(key=lambda t: (t[2].bit_count(), t[3]), reverse=True)
    if cap and len(starts) > cap*max(1, len(V)):
        starts = starts[:cap*max(1, len(V))]
    return adj, starts


def choose(rng, cands, topk):
    if not cands:
        return None
    cands.sort(key=lambda x: x[0], reverse=True)
    pool = cands[:min(topk, len(cands))]
    weights = [1.0/math.sqrt(i+1) for i in range(len(pool))]
    _, v, m, b, h = rng.choices(pool, weights=weights, k=1)[0]
    return v, m, b, h


def seed_start(rng, seed_idx, links):
    if not seed_idx:
        return None
    s = rng.choice(seed_idx)
    mx = min(len(s), links+1)
    ln = rng.randint(2, mx) if mx > 2 else 2
    if rng.random() < 0.55 and mx > 3:
        ln = rng.randint(max(2, mx//2), mx)
    path = list(s[:ln])
    m = 0
    for a, b in zip(path, path[1:]):
        m |= maskseg(V[a], V[b])
    return m, path


def complete(rng, path, m, links, topk, mode):
    used = set(zip(path, path[1:]))
    while len(path)-1 < links:
        depth = len(path)-1
        cur = path[-1]
        last = path[-2]
        rem = links-depth-1
        c = []
        for nxt, mm, base, hits in ADJ.get(cur, []):
            if nxt == last:
                continue
            gm = mm & ~m
            gain = gm.bit_count()
            if gain == 0 and rng.random() > (0.08 if mode in ("warm22", "targeted_warm22") else 0.02):
                continue
            if mode == "strict21" and m.bit_count()+gain+4*rem < 64:
                continue
            if mode == "strict21" and depth < 12 and gain < 3:
                continue
            score = gain*16000 + wgain(gm)*1800 + hits*700 + base + rng.random()*2200
            if mode == "targeted_warm22":
                score += wgain(gm)*1200
            if mode == "fractional22" and any(x % 2 for x in V[nxt]):
                score += 550
            if mode == "catalog22":
                score += 350*hits
            if nxt in path:
                score -= 120
            if (cur, nxt) in used:
                score -= 240
            c.append((score, nxt, mm, base, hits))
        mv = choose(rng, c, topk)
        if mv is None:
            break
        nxt, mm, _, _ = mv
        used.add((path[-1], nxt))
        path.append(nxt)
        m |= mm
        if m == FULL:
            break
    return m, path


def pack(m, path, params, worker, attempts, elapsed):
    return {
        "schema": "smart-mlct-worker-v2",
        "coordinate_scale": 2,
        "status": "complete_candidate" if m == FULL else "partial_candidate",
        "mode": params["mode"],
        "links_target": params["links"],
        "links": len(path)-1,
        "covered_count": m.bit_count(),
        "missing": missing(m),
        "vertices2": [list(V[i]) for i in path],
        "worker_id": worker,
        "attempts": attempts,
        "elapsed_seconds": round(elapsed, 3),
        "parameters": params,
    }


def worker(w, params):
    rng = random.Random(params["seed"] + 1000003*params["shard"] + 7919*w)
    t0 = time.time()
    best = (0, [])
    attempts = 0
    top = []
    parts = params["workers"] * params["shards"]
    group = params["shard"]*params["workers"] + w
    starts = [s for i, s in enumerate(STARTS) if i % parts == group] or STARTS
    idx = {p: i for i, p in enumerate(V)}
    seed_idx = [[idx[p] for p in sp if p in idx] for sp in SEEDS]
    seed_idx = [s for s in seed_idx if len(s) > 1]
    print(f'worker={w} mode={params["mode"]} starts={len(starts)} seeds={len(seed_idx)}', flush=True)
    while time.time() - t0 < params["seconds"]:
        attempts += 1
        warmish = params["mode"] in ("warm22", "targeted_warm22")
        init = seed_start(rng, seed_idx, params["links"]) if warmish and seed_idx and rng.random() < 0.82 else None
        if init:
            m, path = init
        else:
            u, v, m, _, _ = rng.choice(starts[:min(len(starts), 20000)])
            path = [u, v]
        m, path = complete(rng, path, m, params["links"], params["top_k"], params["mode"])
        if m.bit_count() > best[0] or (m.bit_count() == best[0] and len(path) > len(best[1])):
            best = (m.bit_count(), path)
            print(f'worker={w} new_best={m.bit_count()}/64 links={len(path)-1} missing={missing(m)}', flush=True)
        if m.bit_count() >= 50:
            item = pack(m, path, params, w, attempts, time.time()-t0)
            key = (item["covered_count"], -len(item["missing"]), -item["links"], attempts)
            if len(top) < 30:
                heapq.heappush(top, (key, item))
            elif key > top[0][0]:
                heapq.heapreplace(top, (key, item))
        if m == FULL:
            break
    m = 0
    for a, b in zip(best[1], best[1][1:]):
        m |= maskseg(V[a], V[b])
    out = pack(m, best[1], params, w, attempts, time.time()-t0)
    out["top_results"] = [x[1] for x in sorted(top, reverse=True)]
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--prior", default="prior-artifacts")
    ap.add_argument("--seconds", type=int, default=600)
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--shard", type=int, default=0)
    ap.add_argument("--shards", type=int, default=16)
    ap.add_argument("--top-k", type=int, default=48)
    ap.add_argument("--seed", type=int, default=20260624)
    ap.add_argument("--out", type=Path, default=Path("results/smart_best.json"))
    ap.add_argument("--worker-dir", type=Path, default=Path("results/smart_workers"))
    args = ap.parse_args()
    global V, ADJ, STARTS, WEIGHTS, SEEDS
    mode, links = mode_for(args.shard)
    SEEDS, WEIGHTS, prior_best = read_prior(args.prior)
    V = make_vertices(mode, SEEDS)
    ADJ, STARTS = build(mode, 120)
    params = {
        "mode": mode,
        "links": links,
        "seconds": args.seconds,
        "workers": args.workers,
        "shard": args.shard,
        "shards": args.shards,
        "top_k": args.top_k,
        "seed": args.seed,
        "vertex_count": len(V),
        "directed_start_count": len(STARTS),
        "prior_seed_count": len(SEEDS),
        "prior_best": [x[0] for x in prior_best[:8]],
    }
    print("smart_parameters:")
    print(json.dumps(params, indent=2), flush=True)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.worker_dir.mkdir(parents=True, exist_ok=True)
    results = []
    t0 = time.time()
    with ProcessPoolExecutor(max_workers=args.workers) as ex:
        for fut in as_completed([ex.submit(worker, w, params) for w in range(args.workers)]):
            r = fut.result()
            results.append(r)
            (args.worker_dir / f'shard_{args.shard}_worker_{r["worker_id"]}.json').write_text(json.dumps(r, indent=2, sort_keys=True))
            print(f'worker_done={r["worker_id"]} covered={r["covered_count"]}/64', flush=True)
    best = max(results, key=lambda r: (r["covered_count"], -r["links"], r["attempts"]))
    top = []
    for r in results:
        top.extend(r.get("top_results", []))
        q = dict(r)
        q.pop("top_results", None)
        top.append(q)
    uniq = {json.dumps(r.get("vertices2", [])): r for r in sorted(top, key=lambda r: (r["covered_count"], -r["links"], r["attempts"]), reverse=True)}
    merged = {
        "schema": "smart-mlct-shard-v2",
        "coordinate_scale": 2,
        "status": "complete_candidate" if best["covered_count"] == 64 and best["links"] <= links else "partial_candidate",
        "mode": mode,
        "links_target": links,
        "links": best["links"],
        "covered_count": best["covered_count"],
        "missing": best["missing"],
        "vertices2": best["vertices2"],
        "best_worker_id": best["worker_id"],
        "parameters": params,
        "total_attempts": sum(r["attempts"] for r in results),
        "elapsed_seconds": round(time.time()-t0, 3),
        "worker_summaries": [{k: v for k, v in r.items() if k != "top_results"} for r in results],
        "top_results": list(uniq.values())[:40],
    }
    args.out.write_text(json.dumps(merged, indent=2, sort_keys=True))
    print("final_smart_best:")
    print(json.dumps(merged, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
