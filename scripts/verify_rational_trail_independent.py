#!/usr/bin/env python3
"""Independent exact verifier, intentionally not importing the primary geometry routines."""
from __future__ import annotations
import argparse, json
from fractions import Fraction
from pathlib import Path


def F(x): return Fraction(str(x))
def P(x): return tuple(F(v) for v in x)
def vec(a,b): return tuple(b[i]-a[i] for i in range(3))
def det2(a,b,i,j): return a[i]*b[j]-a[j]*b[i]

def collinear_between(a,b,p):
    d=vec(a,b); e=vec(a,p)
    if d==(0,0,0): return False
    if det2(d,e,0,1) or det2(d,e,0,2) or det2(d,e,1,2): return False
    dd=sum(x*x for x in d); t=sum(e[i]*d[i] for i in range(3))
    return 0 <= t <= dd

def load(path):
    d=json.loads(path.read_text())
    if d.get("vertices_q") is not None: return [P(x) for x in d["vertices_q"]]
    if d.get("vertices2") is not None:
        s=int(d.get("coordinate_scale",2)); return [tuple(Fraction(int(v),s) for v in x) for x in d["vertices2"]]
    return [P(x) for x in d["vertices"]]

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("json_file",type=Path); ap.add_argument("--expected-links",type=int,default=22); ap.add_argument("--require-full",action="store_true"); a=ap.parse_args()
    v=load(a.json_file)
    if any(x==y for x,y in zip(v,v[1:])): raise SystemExit("zero-length link")
    grid=[(Fraction(x),Fraction(y),Fraction(z)) for x in range(4) for y in range(4) for z in range(4)]
    cov={p for p in grid if any(collinear_between(x,y,p) for x,y in zip(v,v[1:]))}
    rep={"links":len(v)-1,"covered_count":len(cov),"missing":[[int(p[0]),int(p[1]),int(p[2])] for p in grid if p not in cov],"independent_verifier":True}
    print(json.dumps(rep,indent=2,sort_keys=True))
    return 0 if rep["links"]==a.expected_links and (not a.require_full or rep["covered_count"]==64) else 1
if __name__=="__main__": raise SystemExit(main())
