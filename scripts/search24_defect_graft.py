#!/usr/bin/env python3
from __future__ import annotations

import argparse, hashlib, itertools, json, math, multiprocessing as mp, os, random, signal, sys, time
from collections import OrderedDict, deque
from fractions import Fraction
from pathlib import Path
from typing import Any, Iterable

ALL64=(1<<64)-1
GRID2=[(2*x,2*y,2*z) for x in range(4) for y in range(4) for z in range(4)]

def add(a,b): return (a[0]+b[0],a[1]+b[1],a[2]+b[2])
def sub(a,b): return (a[0]-b[0],a[1]-b[1],a[2]-b[2])
def mul(a,k): return (a[0]*k,a[1]*k,a[2]*k)
def dot(a,b): return a[0]*b[0]+a[1]*b[1]+a[2]*b[2]
def cross(a,b): return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def gcd3(a,b,c): return math.gcd(math.gcd(abs(a),abs(b)),abs(c))

def primitive(d):
    g=gcd3(*d)
    if not g: raise ValueError('zero direction')
    q=(d[0]//g,d[1]//g,d[2]//g)
    if q[0]<0 or (q[0]==0 and q[1]<0) or (q[0]==0 and q[1]==0 and q[2]<0): q=(-q[0],-q[1],-q[2])
    return q

def line_key(a,b):
    d=primitive(sub(b,a)); c=cross(a,d); return d+c

def on_line(q,a,d): return cross(sub(q,a),d)==(0,0,0)

def line_mask(a,d):
    m=0
    for i,q in enumerate(GRID2):
        if on_line(q,a,d): m |= 1<<i
    return m

def line_obj(a,b,role='retained',origin=-1):
    d=primitive(sub(b,a)); k=d+cross(a,d)
    return {'a':tuple(a),'b':tuple(b),'d':d,'key':k,'mask':line_mask(tuple(a),d),'role':role,'origin':origin}

def rat_point(nums,den):
    if den<0: nums=[-x for x in nums]; den=-den
    g=abs(den)
    for x in nums: g=math.gcd(g,abs(x))
    if g: nums=[x//g for x in nums]; den//=g
    return (nums[0],nums[1],nums[2],den)

def intersect_lines(l1,l2):
    d1=l1['d']; d2=l2['d']; n=cross(d1,d2)
    if n==(0,0,0): return None
    w=sub(l2['a'],l1['a'])
    if dot(w,n)!=0: return None
    den=dot(n,n); tnum=dot(cross(w,d2),n)
    nums=[l1['a'][i]*den+d1[i]*tnum for i in range(3)]
    p=rat_point(nums,den)
    qnum=p[:3]; qden=p[3]
    if cross(tuple(qnum[i]-l1['a'][i]*qden for i in range(3)),d1)!=(0,0,0): return None
    if cross(tuple(qnum[i]-l2['a'][i]*qden for i in range(3)),d2)!=(0,0,0): return None
    return p

def rat_to_json(p): return [[p[0],p[3]],[p[1],p[3]],[p[2],p[3]]]
def int_to_rat(p): return (p[0],p[1],p[2],1)

def segment_mask_rat(A,B):
    af=[Fraction(A[i],A[3]) for i in range(3)]; bf=[Fraction(B[i],B[3]) for i in range(3)]
    v=[bf[i]-af[i] for i in range(3)]
    norm=sum(x*x for x in v)
    if norm==0: return 0
    m=0
    for idx,q in enumerate(GRID2):
        w=[Fraction(q[i])-af[i] for i in range(3)]
        c=(w[1]*v[2]-w[2]*v[1],w[2]*v[0]-w[0]*v[2],w[0]*v[1]-w[1]*v[0])
        if c!=(0,0,0): continue
        t=sum(w[i]*v[i] for i in range(3))
        if 0<=t<=norm: m|=1<<idx
    return m

def missing_from_mask(mask):
    out=[]
    i=0
    for x in range(4):
      for y in range(4):
       for z in range(4):
        if not ((mask>>i)&1): out.append([x,y,z])
        i+=1
    return out

def stable_id(prefix,payload):
    raw=json.dumps(payload,sort_keys=True,separators=(',',':')).encode()
    return prefix+hashlib.sha256(raw).hexdigest()[:16]

def load_seeds(path):
    rows=[]
    for line in Path(path).read_text().splitlines():
        if line.strip():
            r=json.loads(line); r['vertices2']=[tuple(p) for p in r['vertices2']]
            rows.append(r)
    return rows

def baseline_trail(seed,shard,worker):
    verts=[int_to_rat(p) for p in seed['vertices2']]
    mask=0
    for i in range(22): mask |= segment_mask_rat(verts[i],verts[i+1])
    return {
      'schema':'defect-graft-candidate-v1','kind':'trail',
      'candidate_id':seed['candidate_id']+'-baseline',
      'source_seed':seed['candidate_id'],'source_shard':shard,'source_worker':worker,
      'operation':'baseline_seed','links':22,'covered_count':mask.bit_count(),
      'coverage_mask_hex':f'0x{mask:016x}','missing':missing_from_mask(mask),
      'vertices_scaled_rational':[rat_to_json(p) for p in verts],
      'removed_links':[],'connector_count':0,'defect_line_inserted':False,
    }

def seed_lines(seed):
    v=seed['vertices2']; return [line_obj(v[i],v[i+1],'retained',i) for i in range(22)]

def graph_for(lines):
    n=len(lines); adj=[0]*n; pts={}
    for i in range(n):
      for j in range(i+1,n):
        p=intersect_lines(lines[i],lines[j])
        if p is not None:
            adj[i]|=1<<j; adj[j]|=1<<i; pts[(i,j)]=p
    return adj,pts

def components(adj):
    n=len(adj); unseen=(1<<n)-1; comps=[]
    while unseen:
        bit=unseen & -unseen; start=bit.bit_length()-1; q=[start]; unseen^=bit; comp=[]
        while q:
            v=q.pop(); comp.append(v); nb=adj[v]&unseen
            while nb:
                b=nb&-nb; u=b.bit_length()-1; nb^=b; unseen^=b; q.append(u)
        comps.append(comp)
    return comps

def residual_connected(adj,current,unvisited):
    allowed=unvisited|(1<<current); seen=1<<current; stack=[current]
    while stack:
        v=stack.pop(); nb=adj[v]&allowed&~seen
        while nb:
            b=nb&-nb; nb^=b; seen|=b; stack.append(b.bit_length()-1)
    return seen==allowed

def hamiltonian_path(adj,original_positions,state_cap=200000):
    n=len(adj); full=(1<<n)-1; deg=[x.bit_count() for x in adj]
    leaves=[i for i,d in enumerate(deg) if d==1]
    if any(d==0 for d in deg) or len(leaves)>2: return None,0,False
    starts=leaves[:] if leaves else sorted(range(n),key=lambda i:deg[i])
    seen=set(); explored=0; cap_hit=False
    def dfs(last,visited,path):
        nonlocal explored,cap_hit
        explored+=1
        if explored>=state_cap: cap_hit=True; return None
        if visited==full: return path[:]
        key=(visited,last)
        if key in seen: return None
        seen.add(key)
        un=full^visited
        if not residual_connected(adj,last,un): return None
        temp=un
        endpoints=0
        while temp:
            b=temp&-temp; temp^=b; u=b.bit_length()-1
            rd=(adj[u]&(un|(1<<last))).bit_count()
            if rd==0: return None
            if rd==1: endpoints+=1
        if endpoints>1: return None
        cand=[]; nb=adj[last]&un
        while nb:
            b=nb&-nb; nb^=b; u=b.bit_length()-1
            preserve=1 if abs(original_positions.get(last,-99)-original_positions.get(u,-99))==1 else 0
            onward=(adj[u]&un).bit_count()
            cand.append((-preserve,onward,deg[u],u))
        cand.sort()
        for _,__,___,u in cand:
            path.append(u); r=dfs(u,visited|(1<<u),path); path.pop()
            if r is not None:return r
            if cap_hit:return None
        return None
    for s in starts:
        r=dfs(s,1<<s,[s])
        if r is not None:return r,explored,cap_hit
        if cap_hit:break
    return None,explored,cap_hit

def realize_order(lines,order):
    inter=[]
    for a,b in zip(order,order[1:]):
        p=intersect_lines(lines[a],lines[b])
        if p is None:return None
        inter.append(p)
    first=lines[order[0]]; last=lines[order[-1]]
    starts=[int_to_rat(q) for q in GRID2 if on_line(q,first['a'],first['d'])]
    ends=[int_to_rat(q) for q in GRID2 if on_line(q,last['a'],last['d'])]
    if not starts: starts=[int_to_rat(first['a'])]
    if not ends: ends=[int_to_rat(last['a'])]
    best=None
    for s in starts:
      for e in ends:
        verts=[s]+inter+[e]
        masks=[]; ok=True
        for i in range(22):
            m=segment_mask_rat(verts[i],verts[i+1])
            if verts[i]==verts[i+1]:ok=False;break
            masks.append(m)
        if not ok:continue
        union=0
        for m in masks:union|=m
        row=(union.bit_count(),union,verts,masks)
        if best is None or row[0]>best[0]:best=row
    return best

def make_line_record(l):
    return {'a2':list(l['a']),'b2':list(l['b']),'key':list(l['key']),'mask_hex':f"0x{l['mask']:016x}",'role':l['role'],'origin':l['origin']}

def line_set_record(seed,lines,removed,connectors,shard,worker,graph_meta,operation):
    payload={'seed':seed['candidate_id'],'keys':[list(l['key']) for l in lines],'removed':removed,'operation':operation}
    cid=stable_id('mlct22-dg-lines-',payload)
    union=0
    for l in lines:union|=l['mask']
    return {
      'schema':'defect-graft-candidate-v1','kind':'line_set','candidate_id':cid,
      'source_seed':seed['candidate_id'],'source_shard':shard,'source_worker':worker,
      'operation':operation,'links':22,'covered_count':union.bit_count(),'coverage_mask_hex':f'0x{union:016x}',
      'missing':missing_from_mask(union),'removed_links':removed,'connector_count':len(connectors),
      'defect_line_inserted':True,'lines':[make_line_record(l) for l in lines],**graph_meta
    }

def trail_record_from_order(seed,line_rec,lines,order,realized,shard,worker,explored,cap_hit):
    covered,mask,verts,masks=realized
    payload={'line_set':line_rec['candidate_id'],'order':order,'verts':[rat_to_json(p) for p in verts]}
    return {
      'schema':'defect-graft-candidate-v1','kind':'trail','candidate_id':stable_id('mlct22-dg-',payload),
      'source_seed':seed['candidate_id'],'source_line_set':line_rec['candidate_id'],'source_shard':shard,'source_worker':worker,
      'operation':line_rec['operation'],'links':22,'covered_count':covered,'coverage_mask_hex':f'0x{mask:016x}',
      'missing':missing_from_mask(mask),'vertices_scaled_rational':[rat_to_json(p) for p in verts],
      'line_order':order,'removed_links':line_rec['removed_links'],'connector_count':line_rec['connector_count'],
      'defect_line_inserted':True,'hamiltonian_states_explored':explored,'hamiltonian_cap_hit':cap_hit,
      'lines':line_rec['lines']
    }

def mode_for_shard(shard):
    if shard<=3:return {'name':'three_old','remove':3,'connectors':2,'orbit':'old','primary':'zero_point','weak_cap':1,'dspan':4,'ham_cap':120000}
    if shard<=7:return {'name':'three_new','remove':3,'connectors':2,'orbit':'new','primary':'zero_point','weak_cap':1,'dspan':4,'ham_cap':120000}
    if shard<=11:return {'name':'three_zero_exclusive','remove':3,'connectors':2,'orbit':'any','primary':'zero_exclusive','weak_cap':1,'dspan':5,'ham_cap':150000}
    if shard<=15:return {'name':'four_graft','remove':4,'connectors':3,'orbit':'any','primary':'zero_point','weak_cap':1 if shard<14 else 2,'dspan':5,'ham_cap':180000}
    if shard==16:return {'name':'catalog_expansion','remove':3,'connectors':2,'orbit':'any','primary':'zero_point','weak_cap':2,'dspan':9,'ham_cap':200000,'expand':True}
    if shard==17:return {'name':'deep_ordering','remove':3,'connectors':2,'orbit':'any','primary':'zero_point','weak_cap':2,'dspan':6,'ham_cap':1000000,'expand':True}
    if shard==18:return {'name':'finite_realization','remove':4,'connectors':3,'orbit':'any','primary':'zero_point','weak_cap':2,'dspan':7,'ham_cap':500000,'expand':True}
    return {'name':'one_connector_ablation','remove':2,'connectors':1,'orbit':'any','primary':'zero_point','weak_cap':1,'dspan':6,'ham_cap':200000}

def applicable_seeds(seeds,mode):
    out=[]
    for s in seeds:
        if s.get('control_only'):continue
        miss=s['missing']
        isnew=miss==[[1,0,2],[3,3,1]]
        if mode['orbit']=='new' and not isnew:continue
        if mode['orbit']=='old' and isnew:continue
        if mode['primary']=='zero_point' and not s['zero_point_links']:continue
        if mode['primary']=='zero_exclusive' and not s['zero_exclusive_links']:continue
        out.append(s)
    return out

def removal_sets(seed,mode,p):
    length=mode['remove']; out=[]; seen=set()
    for st in range(max(0,p-length+1),min(p,22-length)+1):
        r=tuple(range(st,st+length))
        if p in r and r not in seen:seen.add(r);out.append(r)
    near=sorted((i for i in range(22) if i!=p),key=lambda i:(abs(i-p),seed['exclusive_counts'][i],i))
    for q in itertools.combinations(near[:min(8,len(near))],length-1):
        r=tuple(sorted((p,)+q))
        if r not in seen:seen.add(r);out.append(r)
    weak=[i for i,x in enumerate(seed['exclusive_counts']) if i!=p and x<=mode['weak_cap']]
    for q in itertools.combinations(weak,length-1):
        r=tuple(sorted((p,)+q))
        if r not in seen:seen.add(r);out.append(r)
    out.sort(key=lambda r:(0 if max(r)-min(r)+1==len(r) else 1,sum(seed['exclusive_counts'][i] for i in r),sum(abs(i-p) for i in r)))
    return out

def build_context(seed,mode,rng,variant=0):
    orig=seed_lines(seed)
    ppool=seed['zero_point_links'] if mode['primary']=='zero_point' else seed['zero_exclusive_links']
    if not ppool:return None
    p=ppool[variant%len(ppool)]
    rsets=removal_sets(seed,mode,p)
    if not rsets:return None
    removed=list(rsets[(variant//max(1,len(ppool)))%len(rsets)])
    retained=[l for i,l in enumerate(orig) if i not in removed]
    m1=tuple(2*x for x in seed['missing'][0]); m2=tuple(2*x for x in seed['missing'][1])
    D=line_obj(m1,m2,'defect',-1)
    base_lines=retained+[D]
    badj,_=graph_for(base_lines); base_comps=components(badj); comp_of={v:ci for ci,c in enumerate(base_comps) for v in c}
    base_union=0
    for l in base_lines:base_union|=l['mask']
    lost=ALL64^base_union
    dd=primitive(sub(m2,m1)); dpoints=[]
    for k in range(-mode['dspan'],mode['dspan']+1):dpoints.append(add(m1,mul(dd,k)))
    dpoints.extend([m1,m2]);dpoints=list(dict.fromkeys(dpoints))
    point_comps={}
    def add_point(pt,ci=None):
        st=point_comps.setdefault(tuple(pt),set())
        if ci is not None:st.add(ci)
    for bi,l in enumerate(base_lines):
        ci=comp_of[bi]
        add_point(l['a'],ci);add_point(l['b'],ci)
        for q in GRID2:
            if on_line(q,l['a'],l['d']):add_point(q,ci)
    dci=comp_of[len(retained)]
    for dp in dpoints:add_point(dp,dci)
    lost_points=[]
    for gi,q in enumerate(GRID2):
        if (lost>>gi)&1:
            add_point(q,None);lost_points.append(q)
    if mode.get('expand'):
        for p0 in seed['vertices2']:add_point(p0,None)
        for q in GRID2:add_point(q,None)
    pts=list(point_comps)
    cat={}
    for ia in range(len(pts)):
      a=pts[ia]; ca=point_comps[a]
      for ib in range(ia+1,len(pts)):
        b=pts[ib]; cb=point_comps[b]
        if a==b:continue
        if not ca and not cb:continue
        try:c=line_obj(a,b,'connector',-1)
        except ValueError:continue
        if c['key']==D['key'] or any(c['key']==l['key'] for l in retained):continue
        touch=set(ca)|set(cb)
        if dci not in touch and intersect_lines(c,D) is not None:touch.add(dci)
        if not touch:continue
        c['touch_components']=tuple(sorted(touch));c['dpoint']=a if dci in ca else (b if dci in cb else a);c['attachpoint']=b;c['hint']=-1
        old=cat.get(c['key'])
        score=((c['mask']&lost).bit_count(),len(touch),c['mask'].bit_count())
        if old is None or score>((old['mask']&lost).bit_count(),len(old['touch_components']),old['mask'].bit_count()):cat[c['key']]=c
    catalog=list(cat.values())
    catalog.sort(key=lambda c:((c['mask']&lost).bit_count(),len(c['touch_components']),c['mask'].bit_count(),-abs(c['dpoint'][0])-abs(c['dpoint'][1])-abs(c['dpoint'][2])),reverse=True)
    limit=1200 if mode.get('expand') else 650
    catalog=catalog[:limit]
    return {'seed':seed,'removed':removed,'retained':retained,'D':D,'lost':lost,'catalog':catalog,'base_union':base_union,'variant':variant,'base_component_count':len(base_comps),'all_components':set(range(len(base_comps)))}

def choose_connectors(ctx,count,rng):
    cat=ctx['catalog'];lost=ctx['lost']
    if len(cat)<count:return None
    if count==1:
        good=[c for c in cat if (c['mask']&lost)==lost]
        return [rng.choice(good[:min(200,len(good))])] if good else None
    if count==2:
        pairs=ctx.get('feasible_pairs')
        if pairs is None:
            pairs=[]
            for i,a in enumerate(cat):
                rem=lost&~a['mask']
                for j,b in enumerate(cat[i+1:],start=i+1):
                    if rem&~b['mask']:continue
                    touch=set(a['touch_components'])|set(b['touch_components'])
                    score=(len(touch),len(set(a['touch_components'])&set(b['touch_components'])),(a['mask']&lost).bit_count()+(b['mask']&lost).bit_count(),a['mask'].bit_count()+b['mask'].bit_count())
                    pairs.append((score,i,j))
            pairs.sort(reverse=True)
            ctx['feasible_pairs']=pairs[:2000]
            pairs=ctx['feasible_pairs']
        if not pairs:return None
        top=min(len(pairs),300)
        _,i,j=rng.choice(pairs[:top] if rng.random()<0.9 else pairs)
        return [cat[i],cat[j]]
    for _ in range(80):
        a=rng.choice(cat[:min(250,len(cat))]);rem1=lost&~a['mask']
        bpool=[b for b in cat[:min(400,len(cat))] if b['key']!=a['key']]
        rng.shuffle(bpool)
        for b in bpool[:80]:
            rem2=rem1&~b['mask']
            cpool=[c for c in cat if c['key'] not in {a['key'],b['key']} and not (rem2&~c['mask'])]
            if cpool:
                cpool.sort(key=lambda c:(len(set(c['touch_components'])|set(a['touch_components'])|set(b['touch_components'])),c['mask'].bit_count()),reverse=True)
                return [a,b,rng.choice(cpool[:min(100,len(cpool))])]
    return None

def process_candidate(ctx,connectors,mode,shard,worker,ham_cap):
    lines=ctx['retained']+[ctx['D']]+connectors
    if len(lines)!=22 or len({l['key'] for l in lines})!=22:return None
    union=0
    for l in lines:union|=l['mask']
    if union!=ALL64:return {'stage':'not_full','covered':union.bit_count()}
    adj,pts=graph_for(lines); comps=components(adj); degrees=[x.bit_count() for x in adj]; leaves=sum(d==1 for d in degrees)
    meta={'graph_components':len(comps),'degree_one_vertices':leaves,'degree_zero_vertices':sum(d==0 for d in degrees),'graph_degrees':degrees}
    rec=line_set_record(ctx['seed'],lines,ctx['removed'],connectors,shard,worker,meta,mode['name'])
    if len(comps)!=1 or any(d==0 for d in degrees):return {'stage':'cover64','line':rec,'connected':False}
    if leaves>2:return {'stage':'connected_nonham','line':rec,'connected':True}
    original_positions={i:l['origin'] for i,l in enumerate(lines) if l['origin']>=0}
    order,explored,cap_hit=hamiltonian_path(adj,original_positions,ham_cap)
    if order is None:return {'stage':'near','line':rec,'explored':explored,'cap_hit':cap_hit}
    realized=realize_order(lines,order)
    if realized is None:return {'stage':'order','line':rec,'order':order,'explored':explored,'cap_hit':cap_hit}
    trail=trail_record_from_order(ctx['seed'],rec,lines,order,realized,shard,worker,explored,cap_hit)
    order_rec=dict(rec);order_rec.update({'kind':'hamiltonian_order','line_order':order,'finite_realization_covered_count':trail['covered_count'],'finite_trail_candidate_id':trail['candidate_id'],'hamiltonian_states_explored':explored,'hamiltonian_cap_hit':cap_hit})
    return {'stage':'trail','line':rec,'order_rec':order_rec,'trail':trail}

def write_jsonl(path,rows):
    Path(path).write_text(''.join(json.dumps(r,separators=(',',':'))+'\n' for r in rows))

def worker_main(wid,args,seeds,stop_event,tmpdir):
    signal.signal(signal.SIGINT,signal.SIG_IGN)
    mode=mode_for_shard(args.shard); app=applicable_seeds(seeds,mode)
    rng=random.Random(args.seed+args.shard*1000003+wid*10007)
    start=time.monotonic(); deadline=start+args.seconds
    base=[baseline_trail(s,args.shard,wid) for s in app[:max(1,min(8,len(app)))]]
    best=max(base,key=lambda r:r['covered_count']) if base else None
    ordinary=list(base); cover64=[]; orders=[]; near=[]; diagnostics=[]
    seen_line=set();seen_trail=set(r['candidate_id'] for r in ordinary)
    attempts=fullsets=connected=hamfound=0; cap_hits=0; contexts=OrderedDict(); last_cp=start; state_cap_hit=False
    variant_counter=0
    while time.monotonic()<deadline and not stop_event.is_set():
        if attempts>=args.state_cap:state_cap_hit=True;break
        if not app:break
        seed=rng.choice(app)
        variant=(variant_counter*args.workers+wid+args.shard)%128;variant_counter+=1
        ckey=(seed['candidate_id'],variant)
        ctx=contexts.get(ckey)
        if ctx is None:
            ctx=build_context(seed,mode,rng,variant)
            if ctx is None:continue
            contexts[ckey]=ctx
            if len(contexts)>48:contexts.popitem(last=False)
        else:contexts.move_to_end(ckey)
        con=choose_connectors(ctx,mode['connectors'],rng)
        if con is None:continue
        attempts+=1
        res=process_candidate(ctx,con,mode,args.shard,wid,min(mode['ham_cap'],args.hamiltonian_state_cap))
        if not res:continue
        st=res['stage']
        if st!='not_full':fullsets+=1
        if 'line' in res:
            rec=res['line'];cid=rec['candidate_id']
            if cid not in seen_line:
                seen_line.add(cid);cover64.append(rec)
                cover64.sort(key=lambda r:(r['graph_components']==1,-r['degree_one_vertices']),reverse=True)
                del cover64[args.top_diverse:]
        if st in ('connected_nonham','near','order','trail'):connected+=1
        if st=='connected_nonham':
            near.append(res['line']);near.sort(key=lambda r:r.get('degree_one_vertices',99));near=near[:args.top_diverse]
        elif st=='near':
            cap_hits+=bool(res.get('cap_hit')); near.append(res['line']);near.sort(key=lambda r:r.get('degree_one_vertices',99));near=near[:args.top_diverse]
        elif st=='order':
            o=dict(res['line']);o.update({'kind':'hamiltonian_order','line_order':res['order'],'finite_realization_covered_count':0,'hamiltonian_states_explored':res['explored'],'hamiltonian_cap_hit':res['cap_hit']});orders.append(o);orders=orders[-args.top_diverse:];hamfound+=1
        elif st=='trail':
            hamfound+=1;orders.append(res['order_rec']);orders=orders[-args.top_diverse:]
            t=res['trail']
            if t['candidate_id'] not in seen_trail:
                seen_trail.add(t['candidate_id'])
                if t['covered_count']>=62:ordinary.append(t);ordinary.sort(key=lambda r:r['covered_count'],reverse=True);ordinary=ordinary[:args.top_diverse]
                if best is None or t['covered_count']>best['covered_count']:best=t
                if t['covered_count']==64:stop_event.set()
        if st in ('not_full','cover64') and len(diagnostics)<args.top_diverse:
            diagnostics.append({'schema':'defect-graft-diagnostic-v1','source_seed':seed['candidate_id'],'stage':st,'covered_count':res.get('covered',64),'removed_links':ctx['removed'],'connector_count':len(con),'mode':mode['name']})
        now=time.monotonic()
        if now-last_cp>=args.checkpoint_seconds:
            cp={'schema':'defect-graft-worker-checkpoint-v1','shard':args.shard,'worker':wid,'mode':mode['name'],'elapsed_seconds':now-start,'attempts':attempts,'cover64_count':fullsets,'connected_count':connected,'hamiltonian_count':hamfound,'best_covered':best['covered_count'] if best else 0,'state_cap_hit':state_cap_hit}
            Path(tmpdir,f'checkpoint_worker_{wid}.json').write_text(json.dumps(cp,indent=2)+'\n');last_cp=now
    elapsed=time.monotonic()-start
    out=Path(tmpdir)
    (out/f'best_{wid}.json').write_text(json.dumps(best,indent=2)+'\n' if best else '{}\n')
    write_jsonl(out/f'ordinary_{wid}.jsonl',ordinary)
    write_jsonl(out/f'cover64_{wid}.jsonl',cover64)
    write_jsonl(out/f'orders_{wid}.jsonl',orders)
    write_jsonl(out/f'near_{wid}.jsonl',near)
    write_jsonl(out/f'diagnostics_{wid}.jsonl',diagnostics)
    stats={'schema':'defect-graft-worker-stats-v1','shard':args.shard,'worker':wid,'mode':mode['name'],'elapsed_seconds':elapsed,'attempts':attempts,'cover64_line_sets':fullsets,'connected_cover64_line_sets':connected,'hamiltonian_orders':hamfound,'hamiltonian_cap_hits':cap_hits,'best_covered':best['covered_count'] if best else 0,'state_cap':args.state_cap,'state_cap_hit':state_cap_hit,'context_cache_size':len(contexts)}
    (out/f'stats_{wid}.json').write_text(json.dumps(stats,indent=2)+'\n')

def merge_jsonl(paths,limit=None,key='candidate_id'):
    out=[];seen=set()
    for p in paths:
      for line in Path(p).read_text().splitlines():
        if not line.strip():continue
        r=json.loads(line);k=r.get(key) or hashlib.sha256(line.encode()).hexdigest()
        if k in seen:continue
        seen.add(k);out.append(r)
    if limit is not None:out=out[:limit]
    return out

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--seeds',required=True);ap.add_argument('--outdir',required=True)
    ap.add_argument('--seconds',type=int,default=180);ap.add_argument('--workers',type=int,default=4);ap.add_argument('--seed',type=int,default=20260724)
    ap.add_argument('--shard',type=int,required=True);ap.add_argument('--shards',type=int,default=20)
    ap.add_argument('--state-cap',type=int,default=5000000);ap.add_argument('--hamiltonian-state-cap',type=int,default=200000);ap.add_argument('--top-diverse',type=int,default=200);ap.add_argument('--checkpoint-seconds',type=int,default=60)
    args=ap.parse_args()
    if args.shards!=20 or not 0<=args.shard<20:raise SystemExit('search24 requires exactly 20 shards')
    out=Path(args.outdir);out.mkdir(parents=True,exist_ok=True);tmp=out/f'.workers_{args.shard}';tmp.mkdir(exist_ok=True)
    seeds=load_seeds(args.seeds);mode=mode_for_shard(args.shard);app=applicable_seeds(seeds,mode)
    if not app:raise SystemExit(f'no applicable seeds for shard {args.shard} mode {mode}')
    stop=mp.Event();procs=[]
    for wid in range(args.workers):
        p=mp.Process(target=worker_main,args=(wid,args,seeds,stop,tmp));p.start();procs.append(p)
    for p in procs:p.join()
    bad=[p.exitcode for p in procs if p.exitcode!=0]
    if bad:raise SystemExit(f'worker failures: {bad}')
    stats=[json.loads((tmp/f'stats_{w}.json').read_text()) for w in range(args.workers)]
    bests=[json.loads((tmp/f'best_{w}.json').read_text()) for w in range(args.workers)]
    best=max((b for b in bests if b),key=lambda r:r.get('covered_count',0))
    ordinary=merge_jsonl([tmp/f'ordinary_{w}.jsonl' for w in range(args.workers)])
    ordinary.sort(key=lambda r:(r.get('covered_count',0),r.get('defect_line_inserted',False)),reverse=True);ordinary=ordinary[:args.top_diverse]
    cover=merge_jsonl([tmp/f'cover64_{w}.jsonl' for w in range(args.workers)])[:args.top_diverse]
    orders=merge_jsonl([tmp/f'orders_{w}.jsonl' for w in range(args.workers)])[:args.top_diverse]
    near=merge_jsonl([tmp/f'near_{w}.jsonl' for w in range(args.workers)])[:args.top_diverse]
    diags=merge_jsonl([tmp/f'diagnostics_{w}.jsonl' for w in range(args.workers)],key='source_seed')[:args.top_diverse]
    (out/f'best_trail_{args.shard}.json').write_text(json.dumps(best,indent=2)+'\n')
    write_jsonl(out/f'raw_worker_bests_{args.shard}.jsonl',bests)
    write_jsonl(out/f'verified_62plus_{args.shard}.jsonl',ordinary)
    write_jsonl(out/f'cover64_line_sets_{args.shard}.jsonl',cover)
    write_jsonl(out/f'hamiltonian_line_orders_{args.shard}.jsonl',orders)
    write_jsonl(out/f'near_hamiltonian_graphs_{args.shard}.jsonl',near)
    write_jsonl(out/f'graft_diagnostics_{args.shard}.jsonl',diags)
    total={'schema':'defect-graft-search-stats-v1','shard':args.shard,'mode':mode['name'],'elapsed_seconds':max(s['elapsed_seconds'] for s in stats),'workers':args.workers,'attempts':sum(s['attempts'] for s in stats),'cover64_line_sets':sum(s['cover64_line_sets'] for s in stats),'connected_cover64_line_sets':sum(s['connected_cover64_line_sets'] for s in stats),'hamiltonian_orders':sum(s['hamiltonian_orders'] for s in stats),'hamiltonian_cap_hits':sum(s['hamiltonian_cap_hits'] for s in stats),'best_covered':best['covered_count'],'state_cap':args.state_cap,'state_cap_hit':any(s['state_cap_hit'] for s in stats),'applicable_seed_count':len(app),'saved_ordinary':len(ordinary),'saved_cover64':len(cover),'saved_orders':len(orders),'saved_near':len(near)}
    (out/f'search_stats_{args.shard}.json').write_text(json.dumps(total,indent=2)+'\n')
    cp={'schema':'defect-graft-checkpoint-v1','shard':args.shard,'complete':True,'best_covered':best['covered_count'],'attempts':total['attempts'],'mode':mode['name']}
    (out/f'checkpoint_{args.shard}.json').write_text(json.dumps(cp,indent=2)+'\n')
    manifest={'schema':'defect-graft-mode-manifest-v1','shard':args.shard,'mode':mode,'seconds':args.seconds,'workers':args.workers,'seed':args.seed,'state_cap':args.state_cap,'hamiltonian_state_cap':args.hamiltonian_state_cap,'top_diverse':args.top_diverse,'applicable_seed_count':len(app)}
    (out/f'mode_manifest_{args.shard}.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print(json.dumps(total,indent=2))

if __name__=='__main__':
    mp.set_start_method('fork' if sys.platform!='win32' else 'spawn')
    main()
