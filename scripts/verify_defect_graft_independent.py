#!/usr/bin/env python3
from __future__ import annotations
import argparse,json
from fractions import Fraction
from pathlib import Path

GRID=[(x,y,z) for x in range(4) for y in range(4) for z in range(4)]

def p(row):return tuple(Fraction(int(x[0]),int(x[1]))/2 for x in row)
def p2(row):return tuple(Fraction(int(x),2) for x in row)

def point_on_segment(q,a,b):
    ds=[b[i]-a[i] for i in range(3)]
    axis=next((i for i,x in enumerate(ds) if x),None)
    if axis is None:raise ValueError('zero link')
    t=(q[axis]-a[axis])/ds[axis]
    return 0<=t<=1 and all(a[i]+t*ds[i]==q[i] for i in range(3))

def point_on_line(q,a,b):
    ds=[b[i]-a[i] for i in range(3)]
    axis=next((i for i,x in enumerate(ds) if x),None)
    if axis is None:raise ValueError('zero line')
    t=(q[axis]-a[axis])/ds[axis]
    return all(a[i]+t*ds[i]==q[i] for i in range(3))

def mask_segment(a,b):
    m=0
    for i,q in enumerate(GRID):
        if point_on_segment(tuple(Fraction(x) for x in q),a,b):m|=1<<i
    return m

def mask_line(a,b):
    m=0
    for i,q in enumerate(GRID):
        if point_on_line(tuple(Fraction(x) for x in q),a,b):m|=1<<i
    return m

def line_meets(a,b,c,d):
    # Solve using two coordinates and verify the third; all exact Fractions.
    u=[b[i]-a[i] for i in range(3)];v=[d[i]-c[i] for i in range(3)];w=[c[i]-a[i] for i in range(3)]
    for i,j in ((0,1),(0,2),(1,2)):
        det=u[j]*v[i]-u[i]*v[j]
        if det:
            t=(w[j]*v[i]-w[i]*v[j])/det
            s=(u[i]*w[j]-u[j]*w[i])/det
            return all(a[k]+t*u[k]==c[k]+s*v[k] for k in range(3))
    return False

def verify(r,minc):
    kind=r['kind']
    if kind=='trail':
        vv=[p(x) for x in r['vertices_scaled_rational']];assert len(vv)==23
        m=0
        for a,b in zip(vv,vv[1:]):m|=mask_segment(a,b)
    else:
        lines=r['lines'];assert len(lines)==22 and len({tuple(x['key']) for x in lines})==22
        m=0
        for l in lines:
            lm=mask_line(p2(l['a2']),p2(l['b2']));assert f'0x{lm:016x}'==l['mask_hex'];m|=lm
        if kind=='hamiltonian_order':
            order=r['line_order'];assert sorted(order)==list(range(22))
            for i,j in zip(order,order[1:]):
                li,lj=lines[i],lines[j];assert line_meets(p2(li['a2']),p2(li['b2']),p2(lj['a2']),p2(lj['b2']))
    assert m.bit_count()==r['covered_count'] and f'0x{m:016x}'==r['coverage_mask_hex'] and r['covered_count']>=minc

def main():
    ap=argparse.ArgumentParser();ap.add_argument('path',type=Path);ap.add_argument('--jsonl',action='store_true');ap.add_argument('--min-covered',type=int,default=1);a=ap.parse_args()
    rows=[json.loads(x) for x in a.path.read_text().splitlines() if x.strip()] if a.jsonl else [json.loads(a.path.read_text())]
    for r in rows:verify(r,a.min_covered)
    print(json.dumps({'verified':len(rows),'implementation':'independent_parametric'}))
if __name__=='__main__':main()
