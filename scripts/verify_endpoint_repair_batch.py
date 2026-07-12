#!/usr/bin/env python3
"""Run both repository exact trail checkers over a JSON file or JSONL batch."""
from __future__ import annotations
import argparse,json,subprocess,sys,tempfile
from pathlib import Path

def run(cmd):
    p=subprocess.run(cmd,text=True,capture_output=True)
    if p.returncode:
        sys.stderr.write(p.stdout); sys.stderr.write(p.stderr); raise SystemExit(p.returncode)
    return json.loads(p.stdout)

def verify(path:Path, require_full=False):
    a=run([sys.executable,'scripts/check_rational_trail.py',str(path),'--expected-links','22','--min-covered','1']+(['--require-full'] if require_full else []))
    b=run([sys.executable,'scripts/verify_rational_trail_independent.py',str(path),'--expected-links','22']+(['--require-full'] if require_full else []))
    if a['covered_count']!=b['covered_count'] or a['missing']!=b['missing']:
        raise SystemExit(f'exact verifier disagreement for {path}')
    return a

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('path',type=Path); ap.add_argument('--jsonl',action='store_true')
    ap.add_argument('--min-covered',type=int,default=1); ap.add_argument('--require-full',action='store_true'); a=ap.parse_args()
    rows=[]
    if a.jsonl: rows=[json.loads(x) for x in a.path.read_text().splitlines() if x.strip()]
    else: rows=[json.loads(a.path.read_text())]
    checked=0
    with tempfile.TemporaryDirectory() as td:
        for i,row in enumerate(rows):
            if int(row.get('covered_count',0))<a.min_covered: continue
            p=Path(td)/f'candidate_{i}.json'; p.write_text(json.dumps(row))
            rep=verify(p,a.require_full or int(row.get('covered_count',0))==64)
            if int(row.get('covered_count',rep['covered_count']))!=rep['covered_count'] or row.get('missing',rep['missing'])!=rep['missing']:
                raise SystemExit(f'stored metadata mismatch in row {i}')
            checked+=1
    print(json.dumps({'checked':checked,'minimum':a.min_covered,'two_independent_repository_checkers':True},sort_keys=True))
if __name__=='__main__': raise SystemExit(main())
