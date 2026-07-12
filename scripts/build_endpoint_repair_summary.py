#!/usr/bin/env python3
"""Aggregate smart-search-22 endpoint-repair shard artifacts."""
from __future__ import annotations
import json
from collections import Counter, defaultdict
from pathlib import Path

ROOT=Path('collected')

def read_json(p): return json.loads(p.read_text())
def read_jsonl(p):
    return [json.loads(x) for x in p.read_text().splitlines() if x.strip()]
def write_json(name,obj): (ROOT/name).write_text(json.dumps(obj,indent=2,sort_keys=True)+'\n')
def write_jsonl(name,rows): (ROOT/name).write_text(''.join(json.dumps(r,sort_keys=True,separators=(',',':'))+'\n' for r in rows))
def score(r):
    return (r.get('covered_count',0),r.get('redundantly_covered_points',0),-r.get('unique_coverage_points',99),r.get('rich4_count',0),r.get('rich3_count',0),-r.get('pure_bridge_count',99))

bests=[]; allrows=[]; originals=[]; stats=[]; memory=[]
for p in sorted(ROOT.glob('best_candidate_*.json')): bests.append(read_json(p))
for p in sorted(ROOT.glob('verified_candidates_*.jsonl')): allrows.extend(read_jsonl(p))
for p in sorted(ROOT.glob('raw_originals_*.jsonl')): originals.extend(read_jsonl(p))
for p in sorted(ROOT.glob('mode_statistics_*.json')): stats.append(read_json(p))
for p in sorted(ROOT.glob('memory_statistics_*.json')): memory.append(read_json(p))
if not bests: raise SystemExit('no shard best candidates were downloaded')
compact={}
for r in allrows+bests:
    ck=r.get('canonical_key_sha256') or r.get('raw_path_key_sha256') or r['candidate_id']
    if ck not in compact or score(r)>score(compact[ck]): compact[ck]=r
rows=sorted(compact.values(),key=score,reverse=True)
best=max(bests,key=score)
coverage=Counter(r['covered_count'] for r in rows)
defects=Counter(tuple(tuple(p) for p in r['missing']) for r in rows)
mode_rows=defaultdict(list)
for r in rows: mode_rows[r.get('mode','unknown')].append(r)
mode_breakdown=[]
for mode,rr in sorted(mode_rows.items()):
    mode_breakdown.append({'mode':mode,'count':len(rr),'best_covered':max(x['covered_count'] for x in rr),
                           'count_62plus':sum(x['covered_count']>=62 for x in rr),
                           'count_63plus':sum(x['covered_count']>=63 for x in rr),
                           'count_64':sum(x['covered_count']==64 for x in rr)})
op_counts=Counter()
for s in stats:
    for w in s.get('worker_stats',[]): op_counts.update(w.get('operation_counts',{}))
original_index=[]
for r in originals:
    original_index.append({k:r.get(k) for k in ('candidate_id','covered_count','missing','mode','source_shard','source_worker','effective_seed','operation','raw_path_key_sha256','canonical_key_sha256')})
ordinary=[r for r in rows if r['covered_count']>=60]
diagnostic=[r for r in rows if 56<=r['covered_count']<=59]
verified62=[r for r in rows if r['covered_count']>=62]
report={
 'schema':'endpoint-repair-run-summary-v1','workflow':'smart-search-22-endpoint-repair',
 'received_shards':len({r.get('source_shard') for r in bests}),
 'expected_shards':20,'shard_best_count':len(bests),'raw_original_count':len(originals),
 'compact_candidate_count':len(rows),'best_candidate_id':best['candidate_id'],
 'best_covered_count':best['covered_count'],'best_missing':best['missing'],
 'compact_62_count':sum(r['covered_count']==62 for r in rows),
 'compact_63_count':sum(r['covered_count']==63 for r in rows),
 'compact_64_count':sum(r['covered_count']==64 for r in rows),
 'coverage_histogram':[{'covered_count':k,'count':v} for k,v in sorted(coverage.items(),reverse=True)],
 'defect_family_histogram':[{'missing':[list(x) for x in k],'count':v} for k,v in defects.most_common()],
 'mode_breakdown':mode_breakdown,'operation_counts':dict(op_counts),
 'worker_statistics':stats,'memory_statistics':memory,
 'verification_policy':'every shard best and every saved 62+ candidate checked by both exact rational verifiers in its shard job'
}
write_json('run_summary.json',report); write_json('best_candidate.json',best)
write_json('coverage_histogram.json',report['coverage_histogram'])
write_json('defect_family_histogram.json',report['defect_family_histogram'])
write_json('mode_breakdown.json',mode_breakdown)
write_json('endpoint_operation_statistics.json',dict(op_counts))
write_json('paired_transfer_statistics.json',{'paired_transfer_attempts':op_counts.get('paired_transfer',0)})
write_json('exact_verification_report.json',{'policy':report['verification_policy'],'verified_62plus_count':len(verified62),'shard_best_count':len(bests)})
write_jsonl('compact_candidates.jsonl',rows); write_jsonl('verified_62plus.jsonl',verified62)
write_jsonl('ordinary_candidate_additions.jsonl',ordinary); write_jsonl('diagnostic_endpoint_repair.jsonl',diagnostic)
write_jsonl('originals_index.jsonl',original_index); write_jsonl('shard_best_originals.jsonl',originals)
summary=f'''# smart-search-22-endpoint-repair run summary

- Received shard bests: `{len(bests)}/20`
- Compact candidates: `{len(rows)}`
- Best: `{best['covered_count']}/64`
- Best candidate: `{best['candidate_id']}`
- Missing: `{best['missing']}`
- Compact 62/64: `{sum(r['covered_count']==62 for r in rows)}`
- Compact 63/64: `{sum(r['covered_count']==63 for r in rows)}`
- Compact 64/64: `{sum(r['covered_count']==64 for r in rows)}`
- Raw shard-best originals: `{len(originals)}`

Every shard best and every saved candidate at 62/64 or above was checked by both exact rational verifiers before aggregation.
'''
(ROOT/'summary.md').write_text(summary)
print(json.dumps({'best':best['covered_count'],'missing':best['missing'],'shards':len(bests),'compact':len(rows)},sort_keys=True))
