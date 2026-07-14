#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,subprocess,sys
from pathlib import Path

def run(cmd):
    print('+',' '.join(map(str,cmd)),flush=True);subprocess.run([str(x) for x in cmd],check=True)

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,default=Path('.'));ap.add_argument('--prepared',type=Path,required=True);ap.add_argument('--workdir',type=Path,required=True);ap.add_argument('--seconds-per-mode',type=int,default=1);a=ap.parse_args()
    repo=a.repo.resolve();prepared=a.prepared.resolve();work=a.workdir.resolve();work.mkdir(parents=True,exist_ok=True)
    manifest=json.loads((prepared/'search24_defect_graft_manifest.json').read_text())
    assert manifest['primary_seed_count']>=40 and manifest['zero_point_substitution_cases']>=20
    assert manifest['zero_point_substitution_cases']==manifest['zero_point_substitution_full_cases']
    seeds=prepared/'search24_core_escape62_seeds.jsonl';engine=repo/'scripts/search24_defect_graft.py'
    for shard in range(20):
        out=work/f'shard-{shard}';out.mkdir(exist_ok=True)
        run([sys.executable,engine,'--seeds',seeds,'--outdir',out,'--seconds',a.seconds_per_mode,'--workers',1,'--seed',20260724,'--shard',shard,'--shards',20,'--state-cap',200,'--hamiltonian-state-cap',300,'--top-diverse',10,'--checkpoint-seconds',1])
        required=[f'best_trail_{shard}.json',f'verified_62plus_{shard}.jsonl',f'cover64_line_sets_{shard}.jsonl',f'hamiltonian_line_orders_{shard}.jsonl',f'near_hamiltonian_graphs_{shard}.jsonl',f'graft_diagnostics_{shard}.jsonl',f'search_stats_{shard}.json',f'checkpoint_{shard}.json',f'mode_manifest_{shard}.json',f'raw_worker_bests_{shard}.jsonl']
        assert all((out/n).exists() for n in required)
        best=json.loads((out/f'best_trail_{shard}.json').read_text());assert best['links']==22 and best['covered_count']>=62
    # Exercise both exact verifiers on one actual mode output. Full smoke verifies every saved row.
    sample=work/'shard-0'/'best_trail_0.json'
    run([sys.executable,repo/'scripts/verify_defect_graft.py',sample,'--min-covered',62])
    run([sys.executable,repo/'scripts/verify_defect_graft_independent.py',sample,'--min-covered',62])
    aggregate=work/'aggregate'
    run([sys.executable,repo/'scripts/build_defect_graft_summary.py','--input',work,'--out',aggregate,'--expected-shards',20,'--strict'])
    rs=json.loads((aggregate/'run_summary.json').read_text());assert rs['complete'] and rs['received_shards']==list(range(20))
    print(json.dumps({'preflight':'passed','modes':20,'primary_seeds':manifest['primary_seed_count'],'substitution_full':manifest['zero_point_substitution_full_cases']},indent=2))
if __name__=='__main__':main()
