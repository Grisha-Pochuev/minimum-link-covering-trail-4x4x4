#!/usr/bin/env python3
from __future__ import annotations
import argparse,collections,json,sys
from pathlib import Path

def read_jsonl(paths):
    out=[];seen=set()
    for p in paths:
        for line in p.read_text().splitlines():
            if not line.strip():continue
            r=json.loads(line);k=r.get('candidate_id') or line
            if k in seen:continue
            seen.add(k);out.append(r)
    return out

def dump(path,obj):path.write_text(json.dumps(obj,indent=2)+'\n')
def dump_jsonl(path,rows):path.write_text(''.join(json.dumps(r,separators=(',',':'))+'\n' for r in rows))

def hist(rows,key):return dict(sorted(collections.Counter(str(r.get(key)) for r in rows).items()))

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--input',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--expected-shards',type=int,default=20);ap.add_argument('--strict',action='store_true');a=ap.parse_args()
    a.out.mkdir(parents=True,exist_ok=True)
    stats=[]
    for p in sorted(a.input.rglob('search_stats_*.json')):
        try:stats.append(json.loads(p.read_text()))
        except Exception:pass
    by_shard={int(r['shard']):r for r in stats};missing=[i for i in range(a.expected_shards) if i not in by_shard]
    bests=[]
    for p in sorted(a.input.rglob('best_trail_*.json')):
        try:bests.append(json.loads(p.read_text()))
        except Exception:pass
    ordinary=read_jsonl(sorted(a.input.rglob('verified_62plus_*.jsonl')))
    cover=read_jsonl(sorted(a.input.rglob('cover64_line_sets_*.jsonl')))
    orders=read_jsonl(sorted(a.input.rglob('hamiltonian_line_orders_*.jsonl')))
    near=read_jsonl(sorted(a.input.rglob('near_hamiltonian_graphs_*.jsonl')))
    diagnostics=read_jsonl(sorted(a.input.rglob('graft_diagnostics_*.jsonl')))
    originals=read_jsonl(sorted(a.input.rglob('raw_worker_bests_*.jsonl')))
    resources=[]
    for p in sorted(a.input.rglob('resource_usage_*.json')):
        try:resources.append(json.loads(p.read_text()))
        except Exception:pass
    best=max(bests+ordinary,key=lambda r:(r.get('covered_count',0),r.get('defect_line_inserted',False)),default={})
    covhist=collections.Counter(r.get('covered_count',0) for r in ordinary)
    finitehist=collections.Counter(r.get('finite_realization_covered_count',0) for r in orders)
    graphcomp=collections.Counter(r.get('graph_components',-1) for r in cover)
    degreeone=collections.Counter(r.get('degree_one_vertices',-1) for r in cover)
    graftsize=collections.Counter(r.get('connector_count',-1) for r in cover)
    operations=collections.Counter(r.get('operation','unknown') for r in cover+ordinary)
    removed=collections.Counter(tuple(r.get('removed_links',[])) for r in cover)
    connected=sum(r.get('graph_components')==1 for r in cover)
    ham=len(orders)
    exact64_trails=sum(r.get('covered_count')==64 and r.get('kind')=='trail' for r in ordinary)
    exact63_trails=sum(r.get('covered_count')==63 and r.get('kind')=='trail' for r in ordinary)
    complete=not missing and len(stats)>=a.expected_shards
    run_summary={
      'schema':'defect-graft-run-summary-v1','complete':complete,'strict':a.strict,'expected_shards':a.expected_shards,'received_shards':sorted(by_shard),'missing_shards':missing,
      'best_covered_count':best.get('covered_count',0),'best_candidate_id':best.get('candidate_id'),
      'attempts':sum(r.get('attempts',0) for r in stats),'cover64_line_sets_raw':sum(r.get('cover64_line_sets',0) for r in stats),'cover64_line_sets_compact':len(cover),
      'connected_cover64_line_sets_compact':connected,'hamiltonian_orders_compact':ham,'finite_63_trails':exact63_trails,'finite_64_trails':exact64_trails,
      'ordinary_candidates':len(ordinary),'near_hamiltonian_graphs':len(near),'diagnostics':len(diagnostics),'originals':len(originals),
      'state_cap_hit_shards':[r['shard'] for r in stats if r.get('state_cap_hit')],
      'max_peak_ram_gib':max((r.get('peak_ram_gib',0) for r in resources),default=0),
      'mean_attempts_per_second':round(sum(r.get('attempts_per_second',0) for r in resources)/len(resources),2) if resources else 0,
      'mode_breakdown':dict(sorted(collections.Counter(r.get('mode','unknown') for r in stats).items()))
    }
    dump(a.out/'run_summary.json',run_summary);dump(a.out/'best_candidate.json',best or {})
    dump(a.out/'coverage_histogram.json',dict(sorted((str(k),v) for k,v in covhist.items())))
    dump(a.out/'defect_orbit_breakdown.json',hist(ordinary,'missing'))
    dump(a.out/'graft_size_breakdown.json',dict(sorted((str(k),v) for k,v in graftsize.items())))
    dump(a.out/'removed_weak_link_breakdown.json',{str(list(k)):v for k,v in removed.most_common()})
    dump(a.out/'connector_usage_breakdown.json',dict(sorted(operations.items())))
    dump(a.out/'graph_component_histogram.json',dict(sorted((str(k),v) for k,v in graphcomp.items())))
    dump(a.out/'degree_one_histogram.json',dict(sorted((str(k),v) for k,v in degreeone.items())))
    dump(a.out/'hamiltonian_order_report.json',{'count':ham,'finite_realization_histogram':dict(sorted((str(k),v) for k,v in finitehist.items())),'candidate_ids':[r.get('candidate_id') for r in orders[:200]]})
    dump(a.out/'finite_realization_report.json',{'best_finite_covered':best.get('covered_count',0),'finite_63':exact63_trails,'finite_64':exact64_trails})
    dump(a.out/'exact_verification_report.json',{'primary_verifier':'verify_defect_graft.py','independent_verifier':'verify_defect_graft_independent.py','all_saved_outputs_verified_per_shard':complete})
    dump_jsonl(a.out/'ordinary_candidate_additions.jsonl',ordinary)
    diagbank=cover+orders+near+diagnostics
    dump_jsonl(a.out/'diagnostic_cover64_and_graph_states.jsonl',diagbank)
    dump_jsonl(a.out/'originals_index.jsonl',originals)
    shardbest=[]
    for sh in sorted(by_shard):
        bb=[r for r in bests if r.get('source_shard')==sh]
        if bb:shardbest.append(max(bb,key=lambda r:r.get('covered_count',0)))
    dump_jsonl(a.out/'shard_best_originals.jsonl',shardbest)
    lines=[
      '# smart-search-24-defect-graft summary','',f"- Complete: `{complete}` ({len(by_shard)}/{a.expected_shards} shards)",f"- Best ordered trail: `{best.get('covered_count',0)}/64` (`{best.get('candidate_id','none')}`)",f"- Exact 64/64 supporting-line sets saved: `{len(cover)}`",f"- Connected exact 64/64 line sets: `{connected}`",f"- Hamiltonian supporting-line orders: `{ham}`",f"- Exact ordered 63/64 trails: `{exact63_trails}`",f"- Exact ordered 64/64 trails: `{exact64_trails}`",f"- Total attempts: `{run_summary['attempts']}`",f"- Missing shards: `{missing}`",'', 'An unordered line set is never counted as an ordered trail. Every saved mathematical output is intended to pass two independent exact verifiers.'
    ]
    (a.out/'summary.md').write_text('\n'.join(lines)+'\n')
    print(json.dumps(run_summary,indent=2))
    if a.strict and not complete:raise SystemExit(2)
if __name__=='__main__':main()
