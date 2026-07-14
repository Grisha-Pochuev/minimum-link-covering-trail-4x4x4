#!/usr/bin/env python3
from __future__ import annotations
import argparse, glob, json, math
from collections import Counter
from pathlib import Path

ALL64=(1<<64)-1

def idx(x:int,y:int,z:int)->int: return (x*4+y)*4+z

def segment_mask(a,b):
    vx=b[0]-a[0]; vy=b[1]-a[1]; vz=b[2]-a[2]
    norm=vx*vx+vy*vy+vz*vz
    if norm==0: return 0
    m=0
    for x in range(4):
      for y in range(4):
       for z in range(4):
        wx=2*x-a[0]; wy=2*y-a[1]; wz=2*z-a[2]
        c1=wy*vz-wz*vy; c2=wz*vx-wx*vz; c3=wx*vy-wy*vx
        dot=wx*vx+wy*vy+wz*vz
        if c1==c2==c3==0 and 0<=dot<=norm: m |= 1<<idx(x,y,z)
    return m

def primitive(v):
    g=math.gcd(math.gcd(abs(v[0]),abs(v[1])),abs(v[2]))
    if not g: raise ValueError('zero direction')
    d=[x//g for x in v]
    if d[0]<0 or (d[0]==0 and d[1]<0) or (d[0]==0 and d[1]==0 and d[2]<0): d=[-x for x in d]
    return d

def line_key(a,b):
    d=primitive([b[i]-a[i] for i in range(3)])
    c=[a[1]*d[2]-a[2]*d[1], a[2]*d[0]-a[0]*d[2], a[0]*d[1]-a[1]*d[0]]
    return d+c

def analyze(row):
    v=row['vertices2']
    masks=[segment_mask(v[i],v[i+1]) for i in range(22)]
    occ=[0]*64
    for m in masks:
        for b in range(64): occ[b]+=bool((m>>b)&1)
    exclusive=[]
    for m in masks:
        exclusive.append(sum(1 for b in range(64) if ((m>>b)&1) and occ[b]==1))
    missing=row['missing']
    dm1=[2*x for x in missing[0]]; dm2=[2*x for x in missing[1]]
    defect_mask=segment_mask(dm1,dm2)
    zero_point=[i for i,m in enumerate(masks) if m==0]
    zero_exclusive=[i for i,x in enumerate(exclusive) if x==0]
    return {
      'schema':'defect-graft-seed-v1',
      'candidate_id':row['candidate_id'],
      'covered_count':row['covered_count'],
      'missing':missing,
      'vertices2':v,
      'link_masks_hex':[f'0x{m:016x}' for m in masks],
      'link_point_counts':[m.bit_count() for m in masks],
      'exclusive_counts':exclusive,
      'zero_point_links':zero_point,
      'zero_exclusive_links':zero_exclusive,
      'line_keys':[line_key(v[i],v[i+1]) for i in range(22)],
      'defect_line_key':line_key(dm1,dm2),
      'defect_segment_mask_hex':f'0x{defect_mask:016x}',
      'frozen_core_overlap':row.get('frozen_core_overlap'),
      'parent_candidate_id':row.get('parent_candidate_id'),
      'donor_candidate_id':row.get('donor_candidate_id'),
      'source_shard':row.get('source_shard'),
      'source_worker':row.get('source_worker'),
      'effective_seed':row.get('effective_seed'),
      'mode':row.get('mode'),
      'operation':row.get('operation'),
    }

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--artifacts-root',required=True)
    ap.add_argument('--outdir',required=True)
    ap.add_argument('--minimum-source-shards',type=int,default=19)
    args=ap.parse_args()
    root=Path(args.artifacts_root); out=Path(args.outdir); out.mkdir(parents=True,exist_ok=True)
    diag=sorted(root.rglob('core_escape_diagnostics_*.jsonl'))
    ordinary=sorted(root.rglob('verified_62plus_*.jsonl'))
    shard_ids=sorted({int(p.stem.rsplit('_',1)[1]) for p in diag})
    if len(shard_ids)<args.minimum_source_shards:
        raise SystemExit(f'only {len(shard_ids)} source shards found: {shard_ids}')
    raw=[]
    for p in diag:
        for line in p.read_text().splitlines():
            if line.strip(): raw.append(json.loads(line))
    primary={}
    for r in raw:
        if r.get('covered_count')==62 and int(r.get('frozen_core_overlap',99))<=16:
            primary[r['candidate_id']]=analyze(r)
    # Controls: one exact 62/64 representative per missing pair from all ordinary files.
    controls={}
    for p in ordinary:
        for line in p.read_text().splitlines():
            if not line.strip(): continue
            r=json.loads(line)
            if r.get('covered_count')!=62: continue
            key=tuple(tuple(x) for x in r.get('missing',[]))
            if key and key not in controls: controls[key]=analyze(r)
    seeds=list(primary.values())
    seeds.sort(key=lambda r:(tuple(tuple(x) for x in r['missing']),r['candidate_id']))
    control_rows=[]
    primary_ids=set(primary)
    for key,r in sorted(controls.items()):
        if r['candidate_id'] not in primary_ids:
            r['control_only']=True; control_rows.append(r)
    all_rows=seeds+control_rows
    (out/'search24_core_escape62_seeds.jsonl').write_text(''.join(json.dumps(r,separators=(',',':'))+'\n' for r in all_rows))
    tsv=[]
    for r in all_rows:
        verts=';'.join(','.join(map(str,p)) for p in r['vertices2'])
        missing=';'.join(','.join(str(2*x) for x in p) for p in r['missing'])
        zpt=','.join(map(str,r['zero_point_links']))
        zex=','.join(map(str,r['zero_exclusive_links']))
        exc=','.join(map(str,r['exclusive_counts']))
        masks=','.join(r['link_masks_hex'])
        ctrl='1' if r.get('control_only') else '0'
        tsv.append('\t'.join([r['candidate_id'],missing,verts,zpt,zex,exc,masks,str(r['frozen_core_overlap']),ctrl]))
    (out/'search24_seeds.tsv').write_text('\n'.join(tsv)+'\n')
    zpb=sum(bool(r['zero_point_links']) for r in seeds)
    zex=sum(not r['zero_point_links'] and bool(r['zero_exclusive_links']) for r in seeds)
    orbit=Counter(str(r['missing']) for r in seeds)
    # exact step-2 substitution check
    substitution=[]
    for r in seeds:
        if not r['zero_point_links']: continue
        masks=[int(x,16) for x in r['link_masks_hex']]
        D=int(r['defect_segment_mask_hex'],16)
        for p in r['zero_point_links']:
            u=D
            for i,m in enumerate(masks):
                if i!=p: u|=m
            substitution.append({'candidate_id':r['candidate_id'],'removed_link':p,'covered_count':u.bit_count(),'full':u==ALL64})
    if not substitution or not all(x['full'] for x in substitution):
        raise SystemExit('defect-line substitution invariant failed')
    manifest={
      'schema':'search24-defect-graft-manifest-v1',
      'source_run_id':29249275103,
      'source_shards':shard_ids,
      'source_shard_count':len(shard_ids),
      'strict_search23_20_of_20':len(shard_ids)==20,
      'primary_seed_count':len(seeds),
      'control_seed_count':len(control_rows),
      'zero_point_bridge_seed_count':zpb,
      'zero_exclusive_only_seed_count':zex,
      'defect_orbit_counts':dict(orbit),
      'zero_point_substitution_cases':len(substitution),
      'zero_point_substitution_full_cases':sum(x['full'] for x in substitution),
      'notes':'Primary seeds are all exact 62/64 search-23 candidates with frozen-core overlap <=16. A 19-shard source is allowed because all known primary seeds originate in shard 14; source completeness is recorded explicitly.'
    }
    (out/'search24_defect_graft_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    (out/'search24_substitution_check.json').write_text(json.dumps(substitution,indent=2)+'\n')
    print(json.dumps(manifest,indent=2))

if __name__=='__main__': main()
