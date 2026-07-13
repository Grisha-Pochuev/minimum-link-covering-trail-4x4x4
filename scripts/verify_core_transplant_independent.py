#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from fractions import Fraction
from pathlib import Path
from typing import Iterable


def iter_rows(path: Path, jsonl: bool) -> Iterable[dict]:
    if jsonl:
        for line in path.read_text(encoding='utf-8').splitlines():
            if line.strip(): yield json.loads(line)
    else: yield json.loads(path.read_text(encoding='utf-8'))


def on_segment(p: tuple[int,int,int], a: tuple[int,int,int], b: tuple[int,int,int]) -> bool:
    if a == b: raise AssertionError('zero-length link')
    t = None
    for i in range(3):
        d = b[i]-a[i]
        if d:
            ti = Fraction(p[i]-a[i], d)
            if t is None: t = ti
            elif t != ti: return False
        elif p[i] != a[i]: return False
    assert t is not None
    return Fraction(0) <= t <= Fraction(1)


def verify(row: dict, min_covered: int) -> None:
    vertices=[tuple(map(int,p)) for p in row['vertices2']]
    assert len(vertices)==23
    for a,b in zip(vertices,vertices[1:]): assert a!=b
    covered=[]
    for x in range(4):
        for y in range(4):
            for z in range(4):
                p=(2*x,2*y,2*z)
                if any(on_segment(p,a,b) for a,b in zip(vertices,vertices[1:])):
                    covered.append([x,y,z])
    covered_set={tuple(p) for p in covered}
    missing=[[x,y,z] for x in range(4) for y in range(4) for z in range(4) if (x,y,z) not in covered_set]
    assert len(covered)==int(row['covered_count'])
    assert missing==row['missing']
    assert int(row['links'])==22
    assert len(covered)>=min_covered


def main() -> None:
    ap=argparse.ArgumentParser();ap.add_argument('path',type=Path);ap.add_argument('--jsonl',action='store_true');ap.add_argument('--min-covered',type=int,default=1);args=ap.parse_args()
    n=0
    for row in iter_rows(args.path,args.jsonl): verify(row,args.min_covered);n+=1
    print(json.dumps({'checker':'fraction-parametric','verified':n,'min_covered':args.min_covered}))

if __name__=='__main__': main()
