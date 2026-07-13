#pragma once
#include "mutation.hpp"

namespace search23 {

std::string json_escape(const std::string&s){std::ostringstream o;for(char c:s){switch(c){case'\\':o<<"\\\\";break;case'\"':o<<"\\\"";break;case'\n':o<<"\\n";break;default:o<<c;}}return o.str();}

void write_points(std::ostream&o,const std::vector<Point>&v,bool scaled){o<<"[";for(std::size_t i=0;i<v.size();++i){if(i)o<<",";o<<"[";if(scaled)o<<v[i].x<<","<<v[i].y<<","<<v[i].z;else{o<<std::setprecision(12)<<v[i].x/2.0<<","<<v[i].y/2.0<<","<<v[i].z/2.0;}o<<"]";}o<<"]";}

void write_int_array(std::ostream&o,const std::array<int,22>&a){o<<"[";for(int i=0;i<22;++i){if(i)o<<",";o<<a[i];}o<<"]";}

void write_candidate(std::ostream&o,const State&s,int shard,const std::string&mode){
    o<<"{";
    o<<"\"schema\":\"core-transplant-candidate-v1\",";
    o<<"\"candidate_id\":\"mlct22-ct-"<<hex16(s.raw_hash)<<"\",";
    o<<"\"raw_path_key_sha256\":\"fnv64-"<<hex16(s.raw_hash)<<"\",";
    o<<"\"coordinate_scale\":2,";
    o<<"\"covered_count\":"<<s.eval.covered<<",\"coverage_percent\":"<<std::fixed<<std::setprecision(3)<<(100.0*s.eval.covered/64.0)<<",";
    o<<"\"links\":22,\"vertices_count\":23,";
    o<<"\"missing\":";write_points(o,s.eval.missing,true);o<<",";
    o<<"\"missing_count\":"<<s.eval.missing.size()<<",";
    o<<"\"covered_mask_hex\":\"0x"<<std::hex<<std::setw(16)<<std::setfill('0')<<s.eval.mask<<std::dec<<"\",";
    o<<"\"mode\":\""<<json_escape(mode)<<"\",\"operation\":\""<<json_escape(s.operation)<<"\",";
    o<<"\"parent_candidate_id\":\""<<json_escape(s.parent_id)<<"\",\"donor_candidate_id\":\""<<json_escape(s.donor_id)<<"\",";
    o<<"\"source_shard\":"<<shard<<",\"source_worker\":"<<s.worker<<",\"effective_seed\":"<<s.effective_seed<<",";
    o<<"\"frozen_core_overlap\":"<<s.eval.core_overlap<<",\"frozen_core_lines_changed\":"<<(18-s.eval.core_overlap)<<",";
    o<<"\"parent_defects_closed\":"<<s.parent_defects_closed<<",\"unique_link_count\":"<<s.eval.unique_link_count<<",\"unique_coverage_points\":"<<s.eval.unique_point_count<<",\"zero_exclusive_links\":"<<s.eval.zero_exclusive_links<<",";
    o<<"\"link_point_counts\":";write_int_array(o,s.eval.point_counts);o<<",\"link_gains\":";write_int_array(o,s.eval.gains);o<<",";
    o<<"\"vertices2\":";write_points(o,s.vertices,true);o<<",\"vertices\":";write_points(o,s.vertices,false);
    o<<"}";
}

std::string mode_name(int shard){
    if(shard<=3)return "core_window_4";if(shard<=7)return "core_window_5";if(shard<=11)return "core_window_6";if(shard==12)return "core_window_7";if(shard==13)return "core_window_8";if(shard<=16)return "paired_core_transplant";if(shard==17)return "donor_block_transplant";if(shard==18)return "support_transplant_reorder";return "no_core_break_control";
}

void write_state_file(const std::string&path,const State&s,int shard){std::ofstream o(path);if(!o)throw std::runtime_error("cannot write "+path);write_candidate(o,s,shard,mode_name(shard));o<<"\n";}

void write_jsonl(const std::string&path,const std::vector<State>&rows,int shard){std::ofstream o(path);if(!o)throw std::runtime_error("cannot write "+path);std::unordered_set<std::uint64_t>seen;for(const auto&s:rows)if(seen.insert(s.raw_hash).second){write_candidate(o,s,shard,mode_name(shard));o<<"\n";}}

void update_atomic_min(std::atomic<int>&target,int value){int cur=target.load();while(value<cur&&!target.compare_exchange_weak(cur,value)){} }

void trim_beam(std::vector<State>&beam,std::size_t cap,bool escape){
    std::sort(beam.begin(),beam.end(),[&](const State&a,const State&b){return escape?better_escape(a,b):better_cov(a,b);});
    std::unordered_set<std::uint64_t>seen;std::vector<State>out;out.reserve(std::min(cap,beam.size()));
    for(auto&s:beam){if(seen.insert(s.raw_hash).second){out.push_back(std::move(s));if(out.size()>=cap)break;}}
    beam=std::move(out);
}

WorkerResult run_worker(int wid,const Options&opt,const std::vector<Seed>&parents,const std::vector<Seed>&families,const std::vector<Seed>&donors,const std::vector<Point>&pool,const std::unordered_set<LineKey,LineKeyHash>&core,SharedProgress&shared,Clock::time_point deadline){
    WorkerResult wr;std::uint64_t effective=opt.seed+static_cast<std::uint64_t>(opt.shard)*1000003ULL+static_cast<std::uint64_t>(wid)*10007ULL;
    std::mt19937_64 rng(effective);
    std::uint64_t flushed_valid=0, flushed_changed=0;
    std::unordered_map<std::string,const Seed*> parent_by_id;
    for (const auto& s : parents) parent_by_id.emplace(s.id, &s);
    std::vector<State>cov_beam,esc_beam;
    auto make_seed_state=[&](const Seed&s,const std::string&op){State st;st.parent_id=s.id;st.operation=op;st.worker=wid;st.effective_seed=effective;st.vertices=s.vertices;st.eval=evaluate(st.vertices,core);st.raw_hash=raw_hash(st.vertices);return st;};
    for(const auto&s:families)cov_beam.push_back(make_seed_state(s,"parent_seed"));
    for(const auto&s:donors){auto st=make_seed_state(s,"donor_seed");esc_beam.push_back(st);wr.diagnostics.push_back(st);}
    wr.best=*std::max_element(cov_beam.begin(),cov_beam.end(),[](const State&a,const State&b){return better_cov(b,a);});
    wr.best_escape=*std::max_element(esc_beam.begin(),esc_beam.end(),[](const State&a,const State&b){return better_escape(b,a);});
    std::uint64_t batch=0;
    while(Clock::now()<deadline && !shared.found64.load()){
        const Seed* parent=nullptr;State base;
        double u=std::generate_canonical<double,10>(rng);
        if(opt.shard==19 || u<0.50){parent=&parents[randint(rng,0,static_cast<int>(parents.size())-1)];base=make_seed_state(*parent,"parent_seed");}
        else if(u<0.78 && !cov_beam.empty()){base=cov_beam[randint(rng,0,std::min<int>(static_cast<int>(cov_beam.size())-1,255))];}
        else if(!esc_beam.empty()){base=esc_beam[randint(rng,0,std::min<int>(static_cast<int>(esc_beam.size())-1,255))];}
        else {parent=&families[randint(rng,0,static_cast<int>(families.size())-1)];base=make_seed_state(*parent,"parent_seed");}
        if(!parent){auto it=parent_by_id.find(base.parent_id);parent=(it!=parent_by_id.end()?it->second:&families[0]);}
        MutationResult mr=mutate_for_shard(base,donors,pool,opt.shard,rng);
        ++wr.attempts;
        if(!nonzero_path(mr.vertices))continue;
        State child;child.parent_id=parent->id;child.donor_id=mr.donor_id;child.operation=mr.operation;child.worker=wid;child.effective_seed=effective;child.vertices=std::move(mr.vertices);child.eval=evaluate(child.vertices,core);if(!child.eval.valid)continue;child.raw_hash=raw_hash(child.vertices);child.parent_defects_closed=defects_closed(*parent,child.eval.mask);
        ++wr.valid_attempts;wr.min_core_overlap=std::min(wr.min_core_overlap,child.eval.core_overlap);
        if(child.eval.core_overlap<18){++wr.changed_core_attempts;}
        if(better_cov(child,wr.best))wr.best=child;
        if(child.eval.core_overlap<=16 && better_escape(child,wr.best_escape))wr.best_escape=child;
        if(child.eval.covered>=opt.save_min_covered)wr.saved.push_back(child);
        if(child.eval.covered>=58 && child.eval.core_overlap<=16)wr.diagnostics.push_back(child);
        if(child.eval.covered>=57)cov_beam.push_back(child);
        if(child.eval.core_overlap<=16 && child.eval.covered>=55)esc_beam.push_back(child);
        if(child.eval.covered==64){shared.found64.store(true);}
        if(++batch%2000==0){trim_beam(cov_beam,opt.beam_width,false);trim_beam(esc_beam,opt.beam_width,true);if(wr.saved.size()>static_cast<std::size_t>(opt.top_diverse*8))trim_beam(wr.saved,opt.top_diverse*4,false);if(wr.diagnostics.size()>static_cast<std::size_t>(opt.top_diverse*8))trim_beam(wr.diagnostics,opt.top_diverse*4,true);
            shared.attempts.fetch_add(2000);shared.valid_attempts.fetch_add(wr.valid_attempts-flushed_valid);shared.changed_core_attempts.fetch_add(wr.changed_core_attempts-flushed_changed);flushed_valid=wr.valid_attempts;flushed_changed=wr.changed_core_attempts;update_atomic_min(shared.min_core_overlap,wr.min_core_overlap);
            std::lock_guard<std::mutex>lk(shared.mutex);if(!shared.has_best||better_cov(wr.best,shared.best)){shared.best=wr.best;shared.has_best=true;}
        }
    }
    shared.attempts.fetch_add(wr.attempts%2000);shared.valid_attempts.fetch_add(wr.valid_attempts-flushed_valid);shared.changed_core_attempts.fetch_add(wr.changed_core_attempts-flushed_changed);update_atomic_min(shared.min_core_overlap,wr.min_core_overlap);
    {std::lock_guard<std::mutex>lk(shared.mutex);if(!shared.has_best||better_cov(wr.best,shared.best)){shared.best=wr.best;shared.has_best=true;}}
    trim_beam(wr.saved,opt.top_diverse,false);trim_beam(wr.diagnostics,opt.top_diverse,true);return wr;
}

Options parse_args(int argc,char**argv){Options o;auto need=[&](int&i){if(i+1>=argc)throw std::runtime_error("missing arg value");return std::string(argv[++i]);};for(int i=1;i<argc;++i){std::string a=argv[i];if(a=="--repo")o.repo=need(i);else if(a=="--outdir")o.outdir=need(i);else if(a=="--seconds")o.seconds=std::stoi(need(i));else if(a=="--workers")o.workers=std::stoi(need(i));else if(a=="--seed")o.seed=std::stoull(need(i));else if(a=="--shard")o.shard=std::stoi(need(i));else if(a=="--shards")o.shards=std::stoi(need(i));else if(a=="--beam-width")o.beam_width=std::stoi(need(i));else if(a=="--state-cap")o.state_cap=std::stoull(need(i));else if(a=="--save-min-covered")o.save_min_covered=std::stoi(need(i));else if(a=="--top-diverse")o.top_diverse=std::stoi(need(i));else if(a=="--checkpoint-seconds")o.checkpoint_seconds=std::stoi(need(i));else throw std::runtime_error("unknown arg "+a);}return o;}

void ensure_dir(const std::string&path){std::string cmd="mkdir -p '"+path+"'";if(std::system(cmd.c_str())!=0)throw std::runtime_error("mkdir failed");}

void write_checkpoint(const Options&o,const SharedProgress&s,double elapsed){std::ofstream f(o.outdir+"/checkpoint_"+std::to_string(o.shard)+".json");f<<"{\"schema\":\"core-transplant-checkpoint-v1\",\"shard\":"<<o.shard<<",\"elapsed_seconds\":"<<elapsed<<",\"attempts\":"<<s.attempts.load()<<",\"valid_attempts\":"<<s.valid_attempts.load()<<",\"changed_core_attempts\":"<<s.changed_core_attempts.load()<<",\"min_core_overlap\":"<<s.min_core_overlap.load()<<",\"found64\":"<<(s.found64.load()?"true":"false")<<"}\n";}

} // namespace search23
