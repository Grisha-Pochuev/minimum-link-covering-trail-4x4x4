#!/usr/bin/env python3
from __future__ import annotations
import argparse,json
from fractions import Fraction
from pathlib import Path

ALL64=(1<<64)-1
GRID=[(x,y,z) for x in range(4) for y in range(4) for z in range(4)]

def cross(a,b):return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def sub(a,b):return tuple(a[i]-b[i] for i in range(3))
def dot(a,b):return sum(a[i]*b[i] for i in range(3))

def parse_rat_point(row):
    return tuple(Fraction(int(x[0]),int(x[1]))/2 for x in row)

def segment_mask(a,b):
    v=sub(b,a);norm=dot(v,v)
    if norm==0:raise ValueError('zero link')
    m=0
    for i,q in enumerate(GRID):
        w=sub(tuple(Fraction(x) for x in q),a)
        if cross(w,v)!=(0,0,0):continue
        t=dot(w,v)
        if 0<=t<=norm:m|=1<<i
    return m

def line_mask(a2,b2):
    a=tuple(Fraction(int(x),2) for x in a2);b=tuple(Fraction(int(x),2) for x in b2);v=sub(b,a)
    if v==(0,0,0):raise ValueError('zero line')
    m=0
    for i,q in enumerate(GRID):
        if cross(sub(tuple(Fraction(x) for x in q),a),v)==(0,0,0):m|=1<<i
    return m

def line_intersects(a2,b2,c2,d2):
    a=tuple(Fraction(int(x),2) for x in a2);b=tuple(Fraction(int(x),2) for x in b2)
    c=tuple(Fraction(int(x),2) for x in c2);d=tuple(Fraction(int(x),2) for x in d2)
    u=sub(b,a);v=sub(d,c);n=cross(u,v)
    if n==(0,0,0):return False
    return dot(sub(c,a),n)==0

def verify_row(r,min_covered):
    kind=r.get('kind')
    if kind=='trail':
        verts=[parse_rat_point(p) for p in r['vertices_scaled_rational']]
        assert len(verts)==23
        mask=0
        for a,b in zip(verts,verts[1:]):mask|=segment_mask(a,b)
        assert mask.bit_count()==int(r['covered_count'])
        assert f'0x{mask:016x}'==r['coverage_mask_hex']
        assert len(r.get('missing',[]))==64-mask.bit_count()
    elif kind in ('line_set','hamiltonian_order'):
        lines=r['lines'];assert len(lines)==22
        keys={tuple(x['key']) for x in lines};assert len(keys)==22
        mask=0
        for l in lines:
            lm=line_mask(l['a2'],l['b2']);assert f'0x{lm:016x}'==l['mask_hex'];mask|=lm
        assert mask.bit_count()==int(r['covered_count'])
        if kind=='hamiltonian_order':
            order=r['line_order'];assert sorted(order)==list(range(22))
            for i,j in zip(order,order[1:]):
                assert line_intersects(lines[i]['a2'],lines[i]['b2'],lines[j]['a2'],lines[j]['b2'])
    else:raise AssertionError(f'unknown kind {kind}')
    assert int(r['covered_count'])>=min_covered

def main():
    ap=argparse.ArgumentParser();ap.add_argument('path',type=Path);ap.add_argument('--jsonl',action='store_true');ap.add_argument('--min-covered',type=int,default=1);args=ap.parse_args()
    if args.jsonl:
        rows=[json.loads(x) for x in args.path.read_text().splitlines() if x.strip()]
    else:rows=[json.loads(args.path.read_text())]
    for r in rows:verify_row(r,args.min_covered)
    print(json.dumps({'verified':len(rows),'path':str(args.path),'implementation':'fraction_cross_dot'}))
if __name__=='__main__':main()
