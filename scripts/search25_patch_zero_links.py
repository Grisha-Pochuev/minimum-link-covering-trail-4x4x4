#!/usr/bin/env python3
from pathlib import Path
import sys

path = Path(sys.argv[1] if len(sys.argv) > 1 else "src/search25/core_valley_search.cpp")
text = path.read_text()
old_realize = """    for(auto&a:A)for(auto&b:B){uint64_t m=internal|segment_mask(a,joins[0])|segment_mask(joins[20],b);int cov=__builtin_popcountll(m);if(cov>best.covered){best.covered=cov;best.mask=m;best.vertices.clear();best.vertices.push_back(a);for(auto&q:joins)best.vertices.push_back(q);best.vertices.push_back(b);best.order.clear();for(int i:path)best.order.push_back(ls[i]);}}"""
new_realize = """    for(auto&a:A)for(auto&b:B){bool nonzero=!eq(a,joins[0])&&!eq(joins[20],b);for(int i=1;i<21&&nonzero;++i)nonzero=!eq(joins[i-1],joins[i]);if(!nonzero)continue;uint64_t m=internal|segment_mask(a,joins[0])|segment_mask(joins[20],b);int cov=__builtin_popcountll(m);if(cov>best.covered){best.covered=cov;best.mask=m;best.vertices.clear();best.vertices.push_back(a);for(auto&q:joins)best.vertices.push_back(q);best.vertices.push_back(b);best.order.clear();for(int i:path)best.order.push_back(ls[i]);}}"""
old_solve = """if(depth==22){++hr.paths;Trail t=realize(ls,g,path,core,mode,parent,op,attempt);if(!hr.any||t.covered>hr.best.covered){hr.any=true;hr.best=std::move(t);}return;}"""
new_solve = """if(depth==22){++hr.paths;Trail t=realize(ls,g,path,core,mode,parent,op,attempt);if(t.covered>=0&&(!hr.any||t.covered>hr.best.covered)){hr.any=true;hr.best=std::move(t);}return;}"""
if old_realize not in text:
    raise SystemExit("realize patch anchor not found")
if old_solve not in text:
    raise SystemExit("solve patch anchor not found")
text = text.replace(old_realize, new_realize, 1).replace(old_solve, new_solve, 1)
path.write_text(text)
print(f"patched zero-link rejection in {path}")
