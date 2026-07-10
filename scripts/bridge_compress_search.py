#!/usr/bin/env python3
"""smart-search-21: compress bridge cost while retaining rich coverage.

The engine has three families:
A) 23->22 local compression of the known full trail;
B) one/two-window repair of strong ordered 22-link candidates;
C) endpoint-aware simultaneous selection and ordering of rich scaffold lines.

All geometry and coverage tests use fractions.Fraction through bridge_compress_common.
"""
from __future__ import annotations

import argparse
import json
import multiprocessing as mp
import random
import time
from collections import Counter
from fractions import Fraction
from pathlib import Path
from typing import Iterable, Sequence

import bridge_compress_common as bc

Point = bc.Point
Line = tuple[Point, Point]
OFFICIAL_HOLES = [(0,0,1),(0,2,3),(0,3,1),(2,1,1)]
SEARCH20_HOLES = [(0,2,0),(0,2,2),(2,1,0),(2,1,2),(2,3,0),(3,2,0)]


def mode_for_shard(shard: int) -> str:
    table = [
        "ripa_5to4_fixed", "ripa_5to4_fixed",
        "ripa_6to5_slide", "ripa_6to5_slide",
        "ripa_outside_hub", "ripa_outside_hub",
        "official60_single_window", "official60_single_window",
        "official60_double_window", "official60_double_window",
        "official60_productive_bridge", "official60_productive_bridge",
        "scaffold_endpoint_zero_mutation", "scaffold_endpoint_zero_mutation",
        "scaffold_endpoint_one_mutation", "scaffold_endpoint_one_mutation",
        "scaffold_endpoint_two_mutations", "scaffold_endpoint_two_mutations",
        "search20_control", "mixed_compression",
    ]
    return table[shard % 20]


def candidate_files(repo: Path) -> Iterable[Path]:
    preferred = [
        repo / "data/ripa_23_trail.json",
        repo / "runs/2026-07-03-smart-search-16-defect-relay-60-full/best_candidate.json",
        repo / "runs/2026-07-09-smart-search-20-line-bridge-full/best_line_bridge_candidate.json",
    ]
    yielded = set()
    for p in preferred:
        if p.exists():
            yielded.add(p.resolve()); yield p
    for root in (repo / "runs", repo / "candidates/originals"):
        if not root.exists(): continue
        for p in root.rglob("*.json"):
            if p.resolve() not in yielded:
                yielded.add(p.resolve()); yield p
        for p in root.rglob("*.jsonl"):
            if p.resolve() not in yielded:
                yielded.add(p.resolve()); yield p


def load_ordered_seeds(repo: Path) -> list[dict]:
    seeds: list[dict] = []
    seen = set()
    for path in candidate_files(repo):
        try:
            if path.suffix == ".jsonl":
                rows = [json.loads(x) for x in path.read_text(encoding="utf-8").splitlines() if x.strip()]
            else:
                rows = [json.loads(path.read_text(encoding="utf-8"))]
            for d in rows:
                if not isinstance(d, dict) or not any(k in d for k in ("vertices_q","vertices2","vertices")):
                    continue
                v = bc.load_vertices(d)
                links = len(v)-1
                cov = bc.trail_mask(v).bit_count()
                is_ripa = path.name == "ripa_23_trail.json"
                if not is_ripa and not (links == 22 and cov >= 56):
                    continue
                key = bc.raw_path_key(v)
                if key in seen: continue
                seen.add(key)
                seeds.append({"id":d.get("candidate_id") or d.get("name") or path.stem, "path":str(path.relative_to(repo)), "vertices":v, "covered_count":cov, "links":links})
        except Exception:
            continue
    seeds.sort(key=lambda d: (d["links"] == 23, d["covered_count"]), reverse=True)
    return seeds


def load_scaffolds(repo: Path) -> list[dict]:
    paths = [
        repo / "runs/2026-07-07-smart-search-17-cover64-stitch-graph-full/best_line_set.json",
        repo / "candidates/line-set-additions-run28825060197-cover64-stitch.jsonl",
    ]
    rows=[]; seen=set()
    for p in paths:
        if not p.exists(): continue
        raw_rows = [json.loads(p.read_text())] if p.suffix==".json" else [json.loads(x) for x in p.read_text().splitlines() if x.strip()]
        for d in raw_rows:
            raw=d.get("line_set2") or d.get("line_set")
            if not raw: continue
            scale=2 if d.get("line_set2") else 1
            lines=[]
            for a,b in raw:
                if scale==2:
                    lines.append((tuple(Fraction(int(x),2) for x in a), tuple(Fraction(int(x),2) for x in b)))
                else:
                    lines.append((bc.point(a),bc.point(b)))
            key=tuple(sorted((min(a,b),max(a,b)) for a,b in lines))
            if key in seen: continue
            seen.add(key); rows.append({"id":d.get("candidate_id") or p.stem,"path":str(p.relative_to(repo)),"lines":lines,"covered_count":64})
    return rows[:8]


def segments(vertices: Sequence[Point]) -> list[Line]:
    return list(zip(vertices,vertices[1:]))


def make_point_universe(seeds: Sequence[dict], scaffolds: Sequence[dict], args, rng: random.Random, mode: str) -> list[Point]:
    lo,hi=(args.outside_box_min,args.outside_box_max) if mode=="ripa_outside_hub" else (args.box_min,args.box_max)
    pts=set(bc.GRID)
    all_half=[(Fraction(x,2),Fraction(y,2),Fraction(z,2)) for x in range(2*lo,2*hi+1) for y in range(2*lo,2*hi+1) for z in range(2*lo,2*hi+1)]
    rng.shuffle(all_half)
    pts.update(all_half[:max(1000,args.candidate_lines)])
    rich_lines=[]
    for s in seeds[:12]:
        pts.update(s["vertices"])
        for a,b in segments(s["vertices"]):
            if bc.segment_mask(a,b).bit_count()>=3: rich_lines.append((a,b))
    for sc in scaffolds[:4]:
        for a,b in sc["lines"]:
            pts.add(a);pts.add(b)
            if bc.segment_mask(a,b).bit_count()>=3: rich_lines.append((a,b))
    rng.shuffle(rich_lines)
    for i,(a,b) in enumerate(rich_lines[:100]):
        for c,d in rich_lines[i+1:i+45]:
            p=bc.line_intersection(a,b,c,d)
            if p is not None and all(Fraction(lo-2)<=x<=Fraction(hi+2) for x in p): pts.add(p)
    pts.update(bc.point(p) for p in OFFICIAL_HOLES+SEARCH20_HOLES)
    out=list(pts); rng.shuffle(out)
    def quality(p):
        incid=sum(1 for a,b in rich_lines[:300] if bc.cross(bc.sub(b,a),bc.sub(p,a))==(0,0,0))
        outside=sum(1 for x in p if x<0 or x>3)
        den=sum(x.denominator for x in p)
        return (incid,-outside,-den,rng.random())
    out.sort(key=quality,reverse=True)
    return out[:max(args.candidate_lines,1200)]


def repair_window(vertices: Sequence[Point], start: int, length: int, new_internal: Sequence[Point]) -> list[Point]:
    return list(vertices[:start+1])+list(new_internal)+list(vertices[start+length:])


def random_internal(base_internal: Sequence[Point], count: int, universe: Sequence[Point], rng: random.Random, max_mutations: int, force: Point|None=None) -> list[Point]:
    cur=list(base_internal[:count])
    while len(cur)<count: cur.append(universe[rng.randrange(len(universe))])
    muts=max(1 if force is not None else 0, rng.randint(0,max_mutations))
    positions=list(range(count));rng.shuffle(positions)
    for pos in positions[:muts]: cur[pos]=universe[rng.randrange(len(universe))]
    if force is not None and count:
        cur[rng.randrange(count)]=force
    return cur


def window_metadata(source: Sequence[Point], candidate: Sequence[Point], starts: list[int], old_lengths: list[int], new_lengths: list[int]) -> dict:
    return {
        "changed_window_starts":starts,
        "old_window_link_lengths":old_lengths,
        "new_window_link_lengths":new_lengths,
        "old_windows_q":[[bc.pjson(p) for p in source[s:s+l+1]] for s,l in zip(starts,old_lengths)],
        "new_path_links":len(candidate)-1,
    }


def mutate_ordered(seed: dict, universe: Sequence[Point], rng: random.Random, mode: str, args) -> tuple[list[Point],dict]:
    v=seed["vertices"]
    if mode.startswith("ripa_"):
        length=5 if mode=="ripa_5to4_fixed" else 6
        if mode=="ripa_outside_hub": length=rng.choice([4,5,6])
        start=rng.randrange(0,len(v)-length)
        old_internal=v[start+1:start+length]
        base=list(old_internal)
        if base: del base[rng.randrange(len(base))]
        force=None
        if mode=="ripa_outside_hub":
            outside=[p for p in universe if any(x<0 or x>3 for x in p)]
            if outside: force=outside[rng.randrange(len(outside))]
        new_internal=random_internal(base,length-2,universe,rng,args.max_mutations,force)
        if mode=="ripa_6to5_slide" and new_internal and rng.random()<0.7:
            new_internal[0 if rng.random()<0.5 else -1]=universe[rng.randrange(len(universe))]
        cand=repair_window(v,start,length,new_internal)
        return cand,window_metadata(v,cand,[start],[length],[length-1])

    if mode=="official60_double_window":
        lengths=[rng.randint(2,4),rng.randint(2,4)]
        s1=rng.randrange(0,len(v)-sum(lengths)-2)
        s2=rng.randrange(s1+lengths[0]+1,len(v)-lengths[1])
        cand=list(v)
        starts=[s1,s2]
        for s,l in sorted(zip(starts,lengths),reverse=True):
            old=cand[s+1:s+l]
            new=random_internal(old,l-1,universe,rng,args.max_mutations)
            cand=repair_window(cand,s,l,new)
        return cand,window_metadata(v,cand,starts,lengths,lengths)

    length=rng.randint(args.window_min,args.window_max)
    length=min(length,len(v)-1)
    start=rng.randrange(0,len(v)-length)
    old=v[start+1:start+length]
    force=None
    if mode=="official60_productive_bridge": force=bc.point(rng.choice(OFFICIAL_HOLES))
    elif mode=="search20_control" and rng.random()<0.5: force=bc.point(rng.choice(SEARCH20_HOLES))
    new=random_internal(old,length-1,universe,rng,args.max_mutations,force)
    cand=repair_window(v,start,length,new)
    return cand,window_metadata(v,cand,[start],[length],[length])


def mutate_scaffold_lines(lines: Sequence[Line], universe_points: Sequence[Point], rng: random.Random, count: int) -> list[Line]:
    out=list(lines)
    used={(min(a,b),max(a,b)) for a,b in out}
    for _ in range(count):
        pos=rng.randrange(len(out)); old=out[pos]
        for _ in range(100):
            a=universe_points[rng.randrange(len(universe_points))]; b=universe_points[rng.randrange(len(universe_points))]
            if a==b: continue
            line=(min(a,b),max(a,b)); m=bc.segment_mask(*line)
            if m.bit_count()<3 or line in used: continue
            used.discard((min(old),max(old))); out[pos]=line; used.add(line); break
    return out


def scaffold_chain(sc: dict, universe: Sequence[Point], rng: random.Random, mode: str, args) -> tuple[list[Point],dict]:
    mut=0 if "zero" in mode else (1 if "one" in mode else 2)
    lines=mutate_scaffold_lines(sc["lines"],universe,rng,min(mut,args.max_mutations))
    remaining=set(range(len(lines)))
    starts=sorted(remaining,key=lambda i:bc.segment_mask(*lines[i]).bit_count(),reverse=True)[:max(1,args.start_limit)]
    i=rng.choice(starts); a,b=lines[i]
    if rng.random()<0.5:a,b=b,a
    vertices=[a,b];remaining.remove(i);chosen=[i];bridge_records=[]
    covered=bc.segment_mask(a,b);pure=0
    while remaining and len(vertices)-1<22:
        current=vertices[-1]; opts=[]
        for j in remaining:
            x,y=lines[j]
            for entry,exit in ((x,y),(y,x)):
                bridge=bc.segment_mask(current,entry) if current!=entry else 0
                full=bc.segment_mask(entry,exit)
                bridge_gain=(bridge&~covered).bit_count(); full_gain=(full&~(covered|bridge)).bit_count()
                cost=1+(current!=entry);pure_add=int(current!=entry and bridge_gain==0)
                if pure+pure_add>args.max_pure_bridges: continue
                score=(bridge_gain+full_gain,-pure_add,full.bit_count(),-cost,rng.random())
                opts.append((score,j,entry,exit,bridge,full,pure_add))
        if not opts: break
        opts.sort(reverse=True,key=lambda x:x[0]); _,j,entry,exit,bm,fm,padd=opts[0]
        if current!=entry:
            if len(vertices)-1+2>22: break
            vertices.append(entry);covered|=bm;bridge_records.append([bc.pjson(current),bc.pjson(entry)]);pure+=padd
        if len(vertices)-1+1>22: break
        vertices.append(exit);covered|=fm;chosen.append(j);remaining.remove(j)
    while len(vertices)-1<22:
        current=vertices[-1]
        missing=[p for p in bc.GRID if not ((covered>>bc.GRID_INDEX[p])&1)]
        candidates=missing or universe[:200]
        best=None
        for p in candidates:
            if p==current:continue
            m=bc.segment_mask(current,p); gain=(m&~covered).bit_count()
            key=(gain,m.bit_count(),rng.random())
            if best is None or key>best[0]:best=(key,p,m)
        if best is None: break
        _,p,m=best;vertices.append(p);covered|=m
    meta={"source_scaffold_id":sc["id"],"source_scaffold_file":sc["path"],"selected_scaffold_line_indices":chosen,"scaffold_line_mutations":mut,"bridge_records_q":bridge_records}
    return vertices,meta


def choose_seed(seeds: Sequence[dict], mode: str, rng: random.Random) -> dict:
    if mode.startswith("ripa_"):
        return next(s for s in seeds if s["links"]==23)
    if mode.startswith("official60"):
        matches=[s for s in seeds if s["covered_count"]>=60 and "3cf45" in s["id"]]
        return (matches or [s for s in seeds if s["covered_count"]>=60])[0]
    if mode=="search20_control":
        matches=[s for s in seeds if "flbridge" in s["id"] or "line-bridge" in s["path"]]
        return (matches or seeds)[0]
    strong=[s for s in seeds if s["links"]==22 and s["covered_count"]>=59]
    return rng.choice(strong or [s for s in seeds if s["links"]==22])


def attempt(seeds,scaffolds,universe,rng,mode,args) -> dict:
    if mode.startswith("scaffold_endpoint"):
        sc=rng.choice(scaffolds[:4]); vertices,meta=scaffold_chain(sc,universe,rng,mode,args); source=sc["id"]; source_v=None
    else:
        actual=mode
        if mode=="mixed_compression":
            actual=rng.choice(["ripa_5to4_fixed","ripa_6to5_slide","official60_single_window","official60_double_window","official60_productive_bridge","search20_control"])
        seed=choose_seed(seeds,actual,rng);vertices,meta=mutate_ordered(seed,universe,rng,actual,args);source=seed["id"];source_v=seed["vertices"]
        meta["source_candidate_file"]=seed["path"];meta["submode"]=actual
    row=bc.trail_row(vertices,source=source,mode=mode,source_vertices=source_v,extra=meta)
    row["target_min_rich_or_productive_met"]=(row["rich4_count"]+row["rich3_count"]+row["productive_connector_count"]>=args.target_min_rich_or_productive)
    old_holes=OFFICIAL_HOLES if "official60" in mode else SEARCH20_HOLES if mode=="search20_control" else []
    row["old_holes_closed"]=[list(p) for p in old_holes if list(p) not in row["missing"]]
    source_missing=[]
    if source_v is not None: source_missing=bc.missing_from_mask(bc.trail_mask(source_v))
    row["new_holes_opened"]=[p for p in row["missing"] if p not in source_missing]
    row["novelty_score"]=len(set(map(tuple,row["missing"])))+int(row["canonical_key_sha256"][-2:],16)
    return row


def worker_chunk(payload):
    wid,cycle,chunk_seconds,base_seed,shard,mode,seeds,scaffolds,universe,args_dict=payload
    args=argparse.Namespace(**args_dict)
    rng=random.Random(base_seed+shard*1000003+wid*10007+cycle*10000019)
    deadline=time.time()+chunk_seconds; attempts=0; best=None; top={}
    while time.time()<deadline:
        row=attempt(seeds,scaffolds,universe,rng,mode,args);attempts+=1
        key=row["canonical_key_sha256"]
        if key not in top or bc.score_tuple(row)>bc.score_tuple(top[key]): top[key]=row
        if len(top) > min(args.beam_width, args.state_cap):
            keep = sorted(top.values(), key=bc.score_tuple, reverse=True)[:args.beam_width]
            top = {r["canonical_key_sha256"]: r for r in keep}
        if best is None or bc.score_tuple(row)>bc.score_tuple(best):best=row
        if attempts >= args.state_cap or (row["links"]==22 and row["covered_count"]==64):break
    vals=sorted(top.values(),key=bc.score_tuple,reverse=True)[:12]
    return {"worker_id":wid,"attempts":attempts,"best":best,"top":vals}


def report_for(best: dict, source_before: dict|None=None) -> dict:
    return {
        "candidate_id":best.get("candidate_id"),"mode":best.get("mode"),"source_candidate":best.get("source_candidate"),
        "changed_window_starts":best.get("changed_window_starts",[]),"old_window_link_lengths":best.get("old_window_link_lengths",[]),
        "new_window_link_lengths":best.get("new_window_link_lengths",[]),"old_windows_q":best.get("old_windows_q",[]),"new_path_vertices_q":best.get("vertices_q"),
        "covered_count_before":source_before.get("covered_count") if source_before else None,"covered_count_after":best.get("covered_count"),
        "missing_before":source_before.get("missing") if source_before else None,"missing_after":best.get("missing"),
        "rich4_count":best.get("rich4_count"),"rich3_count":best.get("rich3_count"),"productive_connector_count":best.get("productive_connector_count"),
        "pure_bridge_count":best.get("pure_bridge_count"),"old_holes_closed":best.get("old_holes_closed"),"new_holes_opened":best.get("new_holes_opened"),
    }


def main() -> int:
    ap=argparse.ArgumentParser()
    ap.add_argument("--repo",type=Path,default=Path("."));ap.add_argument("--seconds",type=int,default=180);ap.add_argument("--workers",type=int,default=4)
    ap.add_argument("--seed",type=int,default=20260721);ap.add_argument("--shard",type=int,default=0);ap.add_argument("--shards",type=int,default=20)
    ap.add_argument("--beam-width",type=int,default=2048);ap.add_argument("--state-cap",type=int,default=200000);ap.add_argument("--candidate-lines",type=int,default=3000);ap.add_argument("--start-limit",type=int,default=24)
    ap.add_argument("--window-min",type=int,default=3);ap.add_argument("--window-max",type=int,default=5);ap.add_argument("--max-mutations",type=int,default=1);ap.add_argument("--max-pure-bridges",type=int,default=7)
    ap.add_argument("--target-min-rich-or-productive",type=int,default=14);ap.add_argument("--save-min-covered",type=int,default=48)
    ap.add_argument("--box-min",type=int,default=-1);ap.add_argument("--box-max",type=int,default=4);ap.add_argument("--outside-box-min",type=int,default=-2);ap.add_argument("--outside-box-max",type=int,default=5)
    ap.add_argument("--out",type=Path,required=True);ap.add_argument("--preferred-out",type=Path,required=True);ap.add_argument("--report-out",type=Path,required=True);ap.add_argument("--stats-out",type=Path,required=True);ap.add_argument("--checkpoint-out",type=Path,required=True)
    args=ap.parse_args();repo=args.repo.resolve();mode=mode_for_shard(args.shard)
    seeds=load_ordered_seeds(repo);scaffolds=load_scaffolds(repo)
    if not seeds:raise SystemExit("no ordered seeds found")
    if mode.startswith("scaffold_endpoint") and not scaffolds:raise SystemExit("no line-set scaffolds found")
    rng=random.Random(args.seed+args.shard*1000003)
    universe=make_point_universe(seeds,scaffolds,args,rng,mode)
    args_dict={k:v for k,v in vars(args).items() if k not in {"repo","out","preferred_out","report_out","stats_out","checkpoint_out"}}
    deadline=time.time()+max(1,args.seconds);cycle=0;all_top={};worker_totals=Counter();best=None
    while time.time()<deadline:
        chunk=min(300.0,max(1.0,deadline-time.time()))
        payloads=[(w,cycle,chunk,args.seed,args.shard,mode,seeds,scaffolds,universe,args_dict) for w in range(max(1,args.workers))]
        if args.workers<=1: results=[worker_chunk(payloads[0])]
        else:
            with mp.Pool(processes=args.workers) as pool: results=pool.map(worker_chunk,payloads)
        for res in results:
            worker_totals[res["worker_id"]]+=res["attempts"]
            for row in res["top"]:
                key=row["canonical_key_sha256"]
                if key not in all_top or bc.score_tuple(row)>bc.score_tuple(all_top[key]):all_top[key]=row
                if best is None or bc.score_tuple(row)>bc.score_tuple(best):best=row
        cycle+=1
        checkpoint={"schema":"bridge-compress-checkpoint-v1","shard":args.shard,"mode":mode,"cycle":cycle,"elapsed_seconds":args.seconds-max(0,deadline-time.time()),"best":best,"worker_attempts":dict(worker_totals),"unique_compact":len(all_top)}
        bc.atomic_json(args.checkpoint_out,checkpoint)
        if best and best["links"]==22 and best["covered_count"]==64:break
    if best is None:raise SystemExit("search produced no candidate")
    best.update({"source_workflow":"smart-search-21-bridge-compress","source_shard":args.shard,"source_artifact":f"smart-search-21-bridge-compress-22-shard-{args.shard}","parameters":args_dict,"mode_seed":args.seed+args.shard*1000003})
    args.out.parent.mkdir(parents=True,exist_ok=True);bc.atomic_json(args.out,best)
    preferred=sorted(all_top.values(),key=bc.score_tuple,reverse=True)
    preferred=[r for r in preferred if r.get("covered_count",0)>=args.save_min_covered][:100]
    args.preferred_out.parent.mkdir(parents=True,exist_ok=True);args.preferred_out.write_text("".join(json.dumps(r,sort_keys=True)+"\n" for r in preferred),encoding="utf-8")
    source_before=None
    for s in seeds:
        if s["id"]==best.get("source_candidate"):
            source_before=bc.analyze(s["vertices"]);break
    bc.atomic_json(args.report_out,report_for(best,source_before))
    stats={"schema":"bridge-compress-search-stats-v1","shard":args.shard,"mode":mode,"profile_seconds":args.seconds,"workers":args.workers,"worker_attempts":dict(worker_totals),"total_attempts":sum(worker_totals.values()),"unique_compact_candidates":len(all_top),"point_universe_size":len(universe),"ordered_seed_count":len(seeds),"scaffold_count":len(scaffolds),"best_score_tuple":bc.score_tuple(best),"best_candidate_id":best.get("candidate_id"),"best_covered_count":best.get("covered_count"),"best_pure_bridge_count":best.get("pure_bridge_count")}
    bc.atomic_json(args.stats_out,stats)
    print(json.dumps({"candidate_id":best["candidate_id"],"mode":mode,"links":best["links"],"covered_count":best["covered_count"],"pure_bridge_count":best["pure_bridge_count"],"attempts":stats["total_attempts"]},indent=2,sort_keys=True))
    return 0
if __name__=="__main__":raise SystemExit(main())
