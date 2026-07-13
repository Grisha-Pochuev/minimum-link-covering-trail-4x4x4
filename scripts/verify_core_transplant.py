#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Iterable


def iter_rows(path: Path, jsonl: bool) -> Iterable[dict]:
    if jsonl:
        for line in path.read_text(encoding='utf-8').splitlines():
            if line.strip():
                yield json.loads(line)
    else:
        yield json.loads(path.read_text(encoding='utf-8'))


def segment_mask(a: tuple[int,int,int], b: tuple[int,int,int]) -> int:
    v = tuple(b[i]-a[i] for i in range(3))
    norm = sum(x*x for x in v)
    if norm == 0:
        raise AssertionError('zero-length link')
    mask = 0
    idx = 0
    for x in range(4):
        for y in range(4):
            for z in range(4):
                p = (2*x,2*y,2*z)
                w = tuple(p[i]-a[i] for i in range(3))
                cross = (
                    w[1]*v[2]-w[2]*v[1],
                    w[2]*v[0]-w[0]*v[2],
                    w[0]*v[1]-w[1]*v[0],
                )
                dot = sum(w[i]*v[i] for i in range(3))
                if cross == (0,0,0) and 0 <= dot <= norm:
                    mask |= 1 << idx
                idx += 1
    return mask


def verify(row: dict, min_covered: int) -> None:
    vertices = [tuple(map(int,p)) for p in row['vertices2']]
    assert len(vertices) == 23
    mask = 0
    for a,b in zip(vertices,vertices[1:]):
        mask |= segment_mask(a,b)
    covered = mask.bit_count()
    missing=[]
    idx=0
    for x in range(4):
        for y in range(4):
            for z in range(4):
                if not (mask>>idx)&1:
                    missing.append([x,y,z])
                idx += 1
    assert covered == int(row['covered_count']), (row.get('candidate_id'), covered, row['covered_count'])
    assert missing == row['missing'], (row.get('candidate_id'), missing, row['missing'])
    assert int(row['links']) == 22
    assert covered >= min_covered


def main() -> None:
    ap=argparse.ArgumentParser()
    ap.add_argument('path', type=Path)
    ap.add_argument('--jsonl', action='store_true')
    ap.add_argument('--min-covered', type=int, default=1)
    args=ap.parse_args()
    n=0
    for row in iter_rows(args.path,args.jsonl):
        verify(row,args.min_covered); n+=1
    print(json.dumps({'checker':'integer-cross-product','verified':n,'min_covered':args.min_covered}))

if __name__=='__main__': main()
