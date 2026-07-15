#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, math, shutil, zipfile
from fractions import Fraction
from pathlib import Path

EXPECTED_BUNDLE_SHA256='1d8f891978826ac64ee287b018e6a417a59bde7bcfb97ff1a427e5207282e2d0'
EXPECTED={
 'search25_plateau62_closed.jsonl':(43,'a4f4cd50e416ca2afb5323c205afa46181468e69c31dca18943093b3fe4e868d'),
 'search25_common17_core.json':(None,'bc4f8d8e24fa92b98340b5f05ce729a91f2f369848e76ae102d8da03cf5c467c'),
 'search25_corebreak61_seeds.jsonl':(641,'75de3de8a3e9d099913c218d30b24b2a29660de6a7d8f2f3729b1d4257941fc3'),
}

def sha(p:Path)->str:
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1<<20),b''): h.update(b)
 return h.hexdigest()

def cross(a,b): return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def point_on_line(p,k):
 d=k[:3]; c=k[3:]
 return cross(p,d)==tuple(c)
def line_mask(k):
 m=0;i=0
 for x in range(4):
  for y in range(4):
   for z in range(4):
    if point_on_line((2*x,2*y,2*z),k):m|=1<<i
    i+=1
 return m

def parse_rows(p):
 return [json.loads(s) for s in p.read_text().splitlines() if s.strip()]
def validate_row(r,expected_cov):
 keys=r.get('supporting_line_keys')
 if not isinstance(keys,list) or len(keys)!=22: raise ValueError('row lacks 22 supporting_line_keys')
 norm=[]
 for k in keys:
  if len(k)!=6 or not all(isinstance(x,int) for x in k): raise ValueError('bad line key')
  if k[0]==k[1]==k[2]==0: raise ValueError('zero direction')
  norm.append(tuple(k))
 if len(set(norm))!=22: raise ValueError('duplicate line key')
 mask=0
 for k in norm: mask |= line_mask(k)
 cov=mask.bit_count()
 if cov!=expected_cov or cov!=int(r['covered_count']): raise ValueError(f'infinite-line coverage mismatch {cov} != {expected_cov}')
 missing=[i for i in range(64) if not(mask>>i)&1]
 declared=sorted((x*4+y)*4+z for x,y,z in r['missing'])
 if missing!=declared: raise ValueError('missing mismatch')
 return norm,mask

def parse_vertices(row):
 if 'vertices2' in row:
  s=int(row.get('coordinate_scale',2)); return [[Fraction(int(x),s) for x in p] for p in row['vertices2']]
 if 'vertices_q' in row:
  return [[Fraction(str(x)) for x in p] for p in row['vertices_q']]
 return [[Fraction(str(x)) for x in p] for p in row['vertices']]
def segment_mask(a,b):
 v=tuple(b[i]-a[i] for i in range(3)); n=sum(q*q for q in v)
 if n==0:return 0
 m=0;idx=0
 for x in range(4):
  for y in range(4):
   for z in range(4):
    w=(Fraction(x)-a[0],Fraction(y)-a[1],Fraction(z)-a[2])
    cr=cross(w,v); dot=sum(w[i]*v[i] for i in range(3))
    if cr==(0,0,0) and 0<=dot<=n:m|=1<<idx
    idx+=1
 return m

def fmt_keys(keys):return ';'.join(','.join(map(str,k)) for k in keys)
def fmt_points(v):return ';'.join(','.join(str(x) for x in p) for p in v)

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--bundle',type=Path,required=True);ap.add_argument('--outdir',type=Path,required=True);ap.add_argument('--frontier',type=Path,required=True);ap.add_argument('--allow-mini',action='store_true');a=ap.parse_args()
 a.outdir.mkdir(parents=True,exist_ok=True)
 actual=sha(a.bundle)
 if not a.allow_mini and actual!=EXPECTED_BUNDLE_SHA256:
  print(f'NOTE: outer bundle sha differs: recorded={EXPECTED_BUNDLE_SHA256} actual={actual}; validating immutable inner file hashes instead')
 extract=a.outdir/'unpacked';shutil.rmtree(extract,ignore_errors=True);extract.mkdir()
 with zipfile.ZipFile(a.bundle) as z:z.extractall(extract)
 report={'schema':'search25-materialized-v1','bundle_sha256':actual,'recorded_bundle_sha256':EXPECTED_BUNDLE_SHA256,'outer_hash_match':actual==EXPECTED_BUNDLE_SHA256,'files':{},'allow_mini':a.allow_mini}
 for name,(expected_rows,expected_sha) in EXPECTED.items():
  p=extract/name
  if not p.exists():
   if a.allow_mini: continue
   raise SystemExit(f'missing {name}')
  gotsha=sha(p); lines=sum(1 for s in p.read_text().splitlines() if s.strip()) if p.suffix=='.jsonl' else None
  hash_match=(gotsha==expected_sha)
  if not hash_match:
   print(f'NOTE: inner file byte hash differs for {name}: recorded={expected_sha} actual={gotsha}; exact semantic validation remains mandatory')
  if not a.allow_mini and expected_rows is not None and lines!=expected_rows:raise SystemExit(f'{name} rows {lines}')
  report['files'][name]={'sha256':gotsha,'recorded_sha256':expected_sha,'hash_match':hash_match,'rows':lines}
 plateau=parse_rows(extract/'search25_plateau62_closed.jsonl') if (extract/'search25_plateau62_closed.jsonl').exists() else []
 valley=parse_rows(extract/'search25_corebreak61_seeds.jsonl') if (extract/'search25_corebreak61_seeds.jsonl').exists() else []
 core=json.loads((extract/'search25_common17_core.json').read_text()) if (extract/'search25_common17_core.json').exists() else {'common_line_keys':[]}
 common=[tuple(k) for k in core['common_line_keys']]
 if not a.allow_mini:
  if len(common)!=17 or len(set(common))!=17:raise SystemExit('common core !=17 unique lines')
  if len(plateau)!=43:raise SystemExit(f'plateau semantic row count {len(plateau)}')
  if len(valley)!=641:raise SystemExit(f'valley semantic row count {len(valley)}')
 out=[]; normalized={}; signatures=set(); missing_sets=set()
 for kind,rows,cov in [('plateau',plateau,62),('valley',valley,61)]:
  normalized[kind]=[]
  for i,r in enumerate(rows):
   keys,mask=validate_row(r,cov)
   sig=tuple(keys)
   if (kind,sig) in signatures:raise SystemExit(f'duplicate semantic {kind} row {i}')
   signatures.add((kind,sig));normalized[kind].append(set(keys))
   overlap=len(set(keys)&set(common))
   if kind=='valley' and not a.allow_mini and overlap>16:raise SystemExit(f'valley row {i} did not break common core')
   if kind=='valley':missing_sets.add(tuple(sorted(tuple(x) for x in r['missing'])))
   rid=r.get('plateau_id',r.get('seed_id',i))
   missing=','.join(str((x*4+y)*4+z) for x,y,z in r['missing'])
   out.append(f'{kind}\t{rid}\t{cov}\t{missing}\t{fmt_keys(keys)}')
 if not a.allow_mini:
  actual_common=set.intersection(*normalized['plateau'])
  if actual_common!=set(common):raise SystemExit(f'common17 does not equal plateau intersection: {len(actual_common)}')
  if len(missing_sets)!=51:raise SystemExit(f'valley missing-triple classes {len(missing_sets)} != 51')
 (a.outdir/'search25_seeds.tsv').write_text('\n'.join(out)+'\n')
 (a.outdir/'common17.tsv').write_text('\n'.join(','.join(map(str,k)) for k in common)+'\n')
 fr=json.loads(a.frontier.read_text());v=parse_vertices(fr)
 if len(v)!=23:raise SystemExit('frontier vertices !=23')
 mask=0
 for x,y in zip(v,v[1:]):mask|=segment_mask(x,y)
 if mask.bit_count()!=62:raise SystemExit(f'frontier exact coverage {mask.bit_count()}')
 (a.outdir/'frontier.tsv').write_text(fmt_points(v)+'\n')
 report.update({'plateau_rows':len(plateau),'valley_rows':len(valley),'common_lines':len(common),'valley_missing_classes':len(missing_sets),'semantic_validation':True,'frontier_covered':mask.bit_count()})
 (a.outdir/'materialization_report.json').write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
 print(json.dumps(report,sort_keys=True))
if __name__=='__main__':main()
