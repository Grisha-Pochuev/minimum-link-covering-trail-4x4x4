#pragma once
#include "common.hpp"

namespace search23 {

template<class Rng>
MutationResult rebuild_window(const std::vector<Point>&base,int start,int len,const std::vector<Seed>&donors,const std::vector<Point>&pool,Rng&r,bool force_donor){
    MutationResult mr;mr.vertices=base;
    bool use_donor=force_donor||chance(r,0.70);
    if(use_donor){
        const Seed& d=donors[randint(r,0,static_cast<int>(donors.size())-1)];mr.donor_id=d.id;
        auto tv=transformed_vertices(d.vertices,randint(r,0,47),chance(r,0.5));
        int needed=len-1;int ds=randint(r,0,static_cast<int>(tv.size())-needed);
        for(int j=0;j<needed;++j)mr.vertices[start+1+j]=tv[ds+j];
        mr.operation="donor_window_"+std::to_string(len);
    }else{
        for(int j=1;j<len;++j)mr.vertices[start+j]=pool[randint(r,0,static_cast<int>(pool.size())-1)];
        mr.operation="catalog_window_"+std::to_string(len);
    }
    return mr;
}

template<class Rng>
MutationResult mutate_for_shard(const State&base,const std::vector<Seed>&donors,const std::vector<Point>&pool,int shard,Rng&r){
    if(shard==19){MutationResult m;m.vertices=base.vertices;m.operation="no_core_break_control";return m;}
    if(shard<=13){
        int len=4;
        if(shard>=4&&shard<=7)len=5;else if(shard>=8&&shard<=11)len=6;else if(shard==12)len=7;else if(shard==13)len=8;
        int region=shard<=11?shard%4:randint(r,0,3);auto [lo,hi]=region_range(region,len);int start=randint(r,lo,hi);
        return rebuild_window(base.vertices,start,len,donors,pool,r,false);
    }
    if(shard>=14&&shard<=16){
        MutationResult m;m.vertices=base.vertices;m.operation="paired_core_transplant";
        int l1=randint(r,2,4),l2=randint(r,2,4);
        std::pair<int,int> rr1,rr2;
        if(shard==14){rr1=region_range(0,l1);rr2=region_range(2,l2);}else if(shard==15){rr1=region_range(0,l1);rr2=region_range(3,l2);}else{rr1=region_range(1,l1);rr2=region_range(3,l2);}
        int s1=randint(r,rr1.first,rr1.second),s2=randint(r,rr2.first,rr2.second);
        if(s1>s2){std::swap(s1,s2);std::swap(l1,l2);}if(s1+l1>=s2){s2=std::min(22-l2,s1+l1+1);}
        State tmp=base;tmp.vertices=m.vertices;auto a=rebuild_window(tmp.vertices,s1,l1,donors,pool,r,chance(r,0.7));tmp.vertices=a.vertices;auto b=rebuild_window(tmp.vertices,s2,l2,donors,pool,r,chance(r,0.7));
        m.vertices=b.vertices;m.donor_id=a.donor_id.empty()?b.donor_id:a.donor_id+"+"+b.donor_id;return m;
    }
    if(shard==17){int len=randint(r,4,8),start=randint(r,0,22-len);return rebuild_window(base.vertices,start,len,donors,pool,r,true);}
    MutationResult m;m.vertices=base.vertices;m.operation="two_line_transplant_reorder";
    const Seed& d=donors[randint(r,0,static_cast<int>(donors.size())-1)];m.donor_id=d.id;auto tv=transformed_vertices(d.vertices,randint(r,0,47),chance(r,0.5));
    int i=randint(r,1,20),j=randint(r,1,20);while(std::abs(i-j)<3)j=randint(r,1,20);m.vertices[i]=tv[randint(r,1,21)];m.vertices[j]=tv[randint(r,1,21)];
    int a=randint(r,1,7),b=randint(r,a+2,14),c=randint(r,b+2,21);
    if(chance(r,0.5)){std::reverse(m.vertices.begin()+a,m.vertices.begin()+b);std::reverse(m.vertices.begin()+b,m.vertices.begin()+c);}else{
        std::vector<Point> nv;nv.insert(nv.end(),m.vertices.begin(),m.vertices.begin()+a);nv.insert(nv.end(),m.vertices.begin()+b,m.vertices.begin()+c);nv.insert(nv.end(),m.vertices.begin()+a,m.vertices.begin()+b);nv.insert(nv.end(),m.vertices.begin()+c,m.vertices.end());m.vertices=std::move(nv);
    }
    return m;
}

} // namespace search23
