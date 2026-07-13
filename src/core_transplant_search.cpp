#include "search23/search.hpp"

using namespace search23;

int main(int argc,char**argv){
    try{
        Options opt=parse_args(argc,argv);ensure_dir(opt.outdir);std::string build=opt.repo+"/build/search23";
        auto parents=load_seeds(build+"/parents.tsv"),families=load_seeds(build+"/family_representatives.tsv"),donors=load_seeds(build+"/donors.tsv");auto core=load_core(build+"/frozen_core.tsv");
        std::unordered_set<Point,PointHash>ps;for(const auto&rows:{parents,families,donors})for(const auto&s:rows)for(const auto&p:s.vertices)ps.insert(p);
        for(int x=-6;x<=12;++x)for(int y=-6;y<=12;++y)for(int z=-6;z<=12;++z)if((x%2==0&&y%2==0)||(x%2==0&&z%2==0)||(y%2==0&&z%2==0))ps.insert({x,y,z});
        std::vector<Point>pool(ps.begin(),ps.end());
        SharedProgress shared;auto start=Clock::now();auto deadline=start+std::chrono::seconds(opt.seconds);std::vector<WorkerResult>results(opt.workers);std::vector<std::thread>threads;
        for(int w=0;w<opt.workers;++w)threads.emplace_back([&,w]{results[w]=run_worker(w,opt,parents,families,donors,pool,core,shared,deadline);});
        auto next_checkpoint=start+std::chrono::seconds(opt.checkpoint_seconds);
        while(Clock::now()<deadline&&!shared.found64.load()){
            std::this_thread::sleep_for(std::chrono::seconds(1));auto now=Clock::now();if(now>=next_checkpoint){write_checkpoint(opt,shared,std::chrono::duration<double>(now-start).count());next_checkpoint=now+std::chrono::seconds(opt.checkpoint_seconds);}
            bool done=true;for(auto&t:threads)if(t.joinable()){done=false;break;}if(done)break;
        }
        for(auto&t:threads)if(t.joinable())t.join();double elapsed=std::chrono::duration<double>(Clock::now()-start).count();write_checkpoint(opt,shared,elapsed);
        std::vector<State>saved,diagnostics,worker_bests;State best;bool has=false;std::uint64_t attempts=0,valid=0,changed=0;int min_overlap=22;
        for(auto&r:results){attempts+=r.attempts;valid+=r.valid_attempts;changed+=r.changed_core_attempts;min_overlap=std::min(min_overlap,r.min_core_overlap);saved.insert(saved.end(),r.saved.begin(),r.saved.end());diagnostics.insert(diagnostics.end(),r.diagnostics.begin(),r.diagnostics.end());worker_bests.push_back(r.best);worker_bests.push_back(r.best_escape);if(!has||better_cov(r.best,best)){best=r.best;has=true;}}
        if(!has)throw std::runtime_error("no best candidate");trim_beam(saved,opt.top_diverse,false);trim_beam(diagnostics,opt.top_diverse,true);
        write_state_file(opt.outdir+"/best_candidate_"+std::to_string(opt.shard)+".json",best,opt.shard);write_jsonl(opt.outdir+"/verified_62plus_"+std::to_string(opt.shard)+".jsonl",saved,opt.shard);write_jsonl(opt.outdir+"/core_escape_diagnostics_"+std::to_string(opt.shard)+".jsonl",diagnostics,opt.shard);write_jsonl(opt.outdir+"/raw_worker_bests_"+std::to_string(opt.shard)+".jsonl",worker_bests,opt.shard);
        {
            std::ofstream f(opt.outdir+"/search_stats_"+std::to_string(opt.shard)+".json");f<<"{\"schema\":\"core-transplant-search-stats-v1\",\"shard\":"<<opt.shard<<",\"mode\":\""<<mode_name(opt.shard)<<"\",\"elapsed_seconds\":"<<elapsed<<",\"attempts\":"<<attempts<<",\"valid_attempts\":"<<valid<<",\"changed_core_attempts\":"<<changed<<",\"min_core_overlap\":"<<min_overlap<<",\"best_covered\":"<<best.eval.covered<<",\"best_core_overlap\":"<<best.eval.core_overlap<<",\"saved_count\":"<<saved.size()<<",\"diagnostic_count\":"<<diagnostics.size()<<",\"states_per_second\":"<<(elapsed>0?attempts/elapsed:0)<<"}\n";
        }
        {
            std::ofstream f(opt.outdir+"/mode_manifest_"+std::to_string(opt.shard)+".json");f<<"{\"schema\":\"core-transplant-mode-manifest-v1\",\"shard\":"<<opt.shard<<",\"mode\":\""<<mode_name(opt.shard)<<"\",\"seconds\":"<<opt.seconds<<",\"workers\":"<<opt.workers<<",\"base_seed\":"<<opt.seed<<",\"effective_seed_formula\":\"base+shard*1000003+worker*10007\",\"beam_width_per_worker\":"<<opt.beam_width<<",\"state_cap_per_worker\":"<<opt.state_cap<<",\"parent_count\":"<<parents.size()<<",\"family_representative_count\":"<<families.size()<<",\"donor_count\":"<<donors.size()<<",\"requires_core_break\":"<<(opt.shard<19?"true":"false")<<",\"changed_core_attempts\":"<<changed<<",\"min_core_overlap\":"<<min_overlap<<"}\n";
        }
        std::cout<<"shard="<<opt.shard<<" mode="<<mode_name(opt.shard)<<" attempts="<<attempts<<" best="<<best.eval.covered<<" core_overlap="<<best.eval.core_overlap<<" min_overlap="<<min_overlap<<"\n";
        return 0;
    }catch(const std::exception&e){std::cerr<<"error: "<<e.what()<<"\n";return 2;}
}
