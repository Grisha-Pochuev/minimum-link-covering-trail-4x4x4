#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import itertools
import json
from collections import Counter
from pathlib import Path
from typing import Iterable

from verify_core_transplant import verify as verify_primary
from verify_core_transplant_independent import verify as verify_independent

ROOT = Path('collected')
EXPECTED_SHARDS = 20


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding='utf-8'))


def read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding='utf-8').splitlines() if line.strip()]


def sym_point(p: list[int], perm: tuple[int,int,int], refl: tuple[bool,bool,bool]) -> tuple[int,int,int]:
    q=[p[perm[0]],p[perm[1]],p[perm[2]]]
    return tuple(6-q[i] if refl[i] else q[i] for i in range(3))


def canonical_tuple(row: dict) -> tuple[int,...]:
    verts=row['vertices2']
    best=None
    for perm in itertools.permutations(range(3)):
        for bits in range(8):
            refl=tuple(bool(bits&(1<<i)) for i in range(3))
            tv=[sym_point(p,perm,refl) for p in verts]
            for seq in (tv,list(reversed(tv))):
                flat=tuple(x for p in seq for x in p)
                if best is None or flat<best: best=flat
    assert best is not None
    return best


def canonical_key(row: dict) -> str:
    flat=canonical_tuple(row)
    payload=','.join(map(str,flat)).encode()
    return hashlib.sha256(payload).hexdigest()


def missing_orbit(missing: list[list[int]]) -> str:
    best=None
    for perm in itertools.permutations(range(3)):
        for bits in range(8):
            transformed=[]
            for p in missing:
                q=[p[perm[0]],p[perm[1]],p[perm[2]]]
                transformed.append(tuple(3-q[i] if bits&(1<<i) else q[i] for i in range(3)))
            key=tuple(sorted(transformed))
            if best is None or key<best: best=key
    return json.dumps(best,separators=(',',':'))


def compact(rows: Iterable[dict]) -> list[dict]:
    kept={}
    for row in rows:
        key=canonical_key(row)
        row=dict(row);row['canonical_key_sha256']=key
        old=kept.get(key)
        rank=(int(row['covered_count']),-int(row.get('frozen_core_overlap',99)),int(row.get('unique_link_count',0)),-int(row.get('zero_exclusive_links',99)))
        if old is None or rank>old[0]:
            kept[key]=(rank,row)
    out=[x[1] for x in kept.values()]
    out.sort(key=lambda r:(-int(r['covered_count']),int(r.get('frozen_core_overlap',99)),r['canonical_key_sha256']))
    return out


def write_jsonl(path: Path, rows: Iterable[dict]) -> None:
    path.write_text(''.join(json.dumps(r,separators=(',',':'))+'\n' for r in rows),encoding='utf-8')


def histogram(counter: Counter) -> list[dict]:
    return [{'key':k,'count':v} for k,v in sorted(counter.items(),key=lambda kv:(-kv[1],str(kv[0])))]


def main() -> None:
    ROOT.mkdir(exist_ok=True)
    best_paths=sorted(ROOT.glob('best_candidate_*.json'))
    if len(best_paths)!=EXPECTED_SHARDS:
        raise AssertionError(f'expected {EXPECTED_SHARDS} shard bests, got {len(best_paths)}')
    shard_bests=[read_json(p) for p in best_paths]
    saved=[]; diagnostics=[]; originals=[]; manifests=[]; stats=[]; resources=[]
    for shard in range(EXPECTED_SHARDS):
        for pattern,target in [
            (f'verified_62plus_{shard}.jsonl',saved),
            (f'core_escape_diagnostics_{shard}.jsonl',diagnostics),
            (f'raw_worker_bests_{shard}.jsonl',originals),
        ]:
            p=ROOT/pattern
            if not p.exists(): raise AssertionError(f'missing {p}')
            target.extend(read_jsonl(p))
        mp=ROOT/f'mode_manifest_{shard}.json';sp=ROOT/f'search_stats_{shard}.json'
        if not mp.exists() or not sp.exists(): raise AssertionError(f'missing manifest/stats for shard {shard}')
        manifests.append(read_json(mp));stats.append(read_json(sp))
        rp=ROOT/f'resource_usage_{shard}.json'
        if rp.exists(): resources.append(read_json(rp))

    for m in manifests:
        shard=int(m['shard'])
        if shard<19:
            assert m['requires_core_break'] is True
            assert int(m['changed_core_attempts'])>0, m
            assert int(m['min_core_overlap'])<18, m
    if not diagnostics:
        raise AssertionError('diagnostic output is empty')

    verify_rows=[]
    seen_raw=set()
    for row in shard_bests+saved+diagnostics:
        key=row.get('raw_path_key_sha256') or json.dumps(row['vertices2'])
        if key in seen_raw: continue
        seen_raw.add(key);verify_rows.append(row)
    for row in verify_rows:
        verify_primary(row,1)
        verify_independent(row,1)

    compact_saved=compact(r for r in saved if int(r['covered_count'])>=62)
    old_orbits={missing_orbit([[2,3,1],[3,3,1]]),missing_orbit([[1,3,1],[2,3,1]]),missing_orbit([[1,3,1],[3,3,1]]),missing_orbit([[0,2,1],[3,3,1]]),missing_orbit([[1,2,1],[2,3,1]]),missing_orbit([[1,2,1],[3,3,1]]),missing_orbit([[0,2,1],[2,3,1]])}
    diagnostic_candidates=[]
    for r in diagnostics:
        covered=int(r['covered_count']); overlap=int(r.get('frozen_core_overlap',99)); orbit=missing_orbit(r['missing'])
        if covered in (60,61) and (overlap<=16 or orbit not in old_orbits): diagnostic_candidates.append(r)
    compact_diag=compact(diagnostic_candidates)

    best=max(shard_bests+compact_saved,key=lambda r:(int(r['covered_count']),-int(r.get('frozen_core_overlap',99)),int(r.get('unique_link_count',0))))
    best=dict(best);best['canonical_key_sha256']=canonical_key(best)

    cov=Counter(int(r['covered_count']) for r in compact_saved+compact_diag)
    defects=Counter((json.dumps(sorted(r['missing']),separators=(',',':')),missing_orbit(r['missing'])) for r in compact_saved+compact_diag)
    core_hist=Counter((int(r['covered_count']),int(r.get('frozen_core_overlap',99))) for r in compact_saved+compact_diag)
    operations=Counter(r.get('operation','') for r in compact_saved+compact_diag)
    donors=Counter(r.get('donor_candidate_id','') for r in compact_saved+compact_diag if r.get('donor_candidate_id'))
    windows=Counter()
    for r in compact_saved+compact_diag:
        op=r.get('operation','')
        for n in range(2,9):
            if op.endswith('_'+str(n)): windows[n]+=1

    write_jsonl(ROOT/'ordinary_candidate_additions.jsonl',compact_saved)
    write_jsonl(ROOT/'diagnostic_core_escape.jsonl',compact_diag)
    write_jsonl(ROOT/'shard_best_originals.jsonl',originals)
    originals_index=[]
    for r in originals:
        originals_index.append({
            'candidate_id':r['candidate_id'],'covered_count':r['covered_count'],'missing':r['missing'],
            'source_shard':r['source_shard'],'source_worker':r['source_worker'],'mode':r['mode'],
            'operation':r['operation'],'frozen_core_overlap':r.get('frozen_core_overlap'),
            'raw_path_key_sha256':r.get('raw_path_key_sha256'),
        })
    write_jsonl(ROOT/'originals_index.jsonl',originals_index)
    (ROOT/'best_candidate.json').write_text(json.dumps(best,indent=2)+'\n',encoding='utf-8')
    (ROOT/'coverage_histogram.json').write_text(json.dumps([{'covered_count':k,'count':v} for k,v in sorted(cov.items(),reverse=True)],indent=2)+'\n')
    (ROOT/'defect_pair_and_orbit_histogram.json').write_text(json.dumps([{'missing':json.loads(k[0]),'orbit':json.loads(k[1]),'count':v} for k,v in sorted(defects.items(),key=lambda kv:-kv[1])],indent=2)+'\n')
    (ROOT/'frozen_core_overlap_histogram.json').write_text(json.dumps([{'covered_count':k[0],'frozen_core_overlap':k[1],'count':v} for k,v in sorted(core_hist.items(),key=lambda kv:(-kv[0][0],kv[0][1]))],indent=2)+'\n')
    (ROOT/'window_length_breakdown.json').write_text(json.dumps([{'window_length':k,'count':v} for k,v in sorted(windows.items())],indent=2)+'\n')
    (ROOT/'donor_usage_breakdown.json').write_text(json.dumps(histogram(donors),indent=2)+'\n')
    (ROOT/'operation_breakdown.json').write_text(json.dumps(histogram(operations),indent=2)+'\n')
    exact_report={'primary_checker':'integer-cross-product','independent_checker':'fraction-parametric','unique_candidates_verified':len(verify_rows),'shard_bests_verified':len(shard_bests),'all_passed':True}
    (ROOT/'exact_verification_report.json').write_text(json.dumps(exact_report,indent=2)+'\n')

    summary={
        'schema':'core-transplant-run-summary-v1','received_shards':len(shard_bests),'expected_shards':EXPECTED_SHARDS,
        'best_candidate_id':best['candidate_id'],'best_covered_count':best['covered_count'],'best_missing':best['missing'],
        'best_frozen_core_overlap':best.get('frozen_core_overlap'),'compact_ordinary_62plus_count':len(compact_saved),
        'compact_diagnostic_count':len(compact_diag),'raw_original_count':len(originals),
        'compact_63_count':sum(int(r['covered_count'])==63 for r in compact_saved),
        'compact_64_count':sum(int(r['covered_count'])==64 for r in compact_saved),
        'compact_62_core_escape_count':sum(int(r['covered_count'])==62 and int(r.get('frozen_core_overlap',99))<=16 for r in compact_saved),
        'new_two_hole_orbit_count':len({missing_orbit(r['missing']) for r in compact_saved if len(r['missing'])==2}-old_orbits),
        'attempts':sum(int(s.get('attempts',0)) for s in stats),'changed_core_attempts':sum(int(s.get('changed_core_attempts',0)) for s in stats),
        'min_core_overlap_seen':min(int(s.get('min_core_overlap',99)) for s in stats),'resource_records':len(resources),
        'exact_verification':exact_report,
    }
    (ROOT/'run_summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    md=f"""# smart-search-23-core-transplant run summary

- Received shard bests: `{len(shard_bests)}/{EXPECTED_SHARDS}`
- Best: `{best['covered_count']}/64`
- Best candidate: `{best['candidate_id']}`
- Missing: `{best['missing']}`
- Best frozen-core overlap: `{best.get('frozen_core_overlap')}/18`
- Compact ordinary `62/64+`: `{len(compact_saved)}`
- Compact diagnostic core-escape states: `{len(compact_diag)}`
- Compact `63/64`: `{summary['compact_63_count']}`
- Compact `64/64`: `{summary['compact_64_count']}`
- Exact `62/64` with core overlap <=16: `{summary['compact_62_core_escape_count']}`
- New two-hole orbits: `{summary['new_two_hole_orbit_count']}`
- Raw worker-best originals: `{len(originals)}`
- Search attempts: `{summary['attempts']}`
- Core-changing attempts: `{summary['changed_core_attempts']}`
- Minimum core overlap observed: `{summary['min_core_overlap_seen']}`

Every shard best, ordinary candidate and diagnostic candidate was checked by two independent exact verifiers before bank construction.
"""
    (ROOT/'summary.md').write_text(md,encoding='utf-8')
    print(json.dumps(summary,indent=2))

if __name__=='__main__': main()
