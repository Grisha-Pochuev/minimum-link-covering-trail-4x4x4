#!/usr/bin/env python3
"""Aggregate smart-search-21 shard artifacts into compact scientific summaries."""
from __future__ import annotations
import json
from collections import Counter, defaultdict
from pathlib import Path
import bridge_compress_common as bc

ROOT=Path("collected")
OUT=ROOT


def read_jsons(pattern):
    out=[]
    for p in ROOT.rglob(pattern):
        try:
            d=json.loads(p.read_text(encoding="utf-8"));d["_file"]=str(p);out.append(d)
        except Exception: pass
    return out


def main():
    best_rows=read_jsons("best_candidate_*.json")
    reports=read_jsons("compression_report_*.json")
    stats=read_jsons("search_stats_*.json")
    preferred=[]
    for p in ROOT.rglob("preferred_candidates_*.jsonl"):
        for raw in p.read_text(encoding="utf-8").splitlines():
            if raw.strip():
                try: preferred.append(json.loads(raw))
                except Exception: pass
    unique={}
    for row in preferred+best_rows:
        key=row.get("canonical_key_sha256") or row.get("candidate_id")
        if key not in unique or bc.score_tuple(row)>bc.score_tuple(unique[key]):unique[key]=row
    compact=sorted(unique.values(),key=bc.score_tuple,reverse=True)
    best=max(best_rows,key=bc.score_tuple) if best_rows else (compact[0] if compact else {})
    mode_rows=defaultdict(list)
    for r in best_rows:mode_rows[r.get("mode","unknown")].append(r)
    mode_breakdown={}
    for mode,rows in sorted(mode_rows.items()):
        b=max(rows,key=bc.score_tuple)
        mode_breakdown[mode]={"shard_best_count":len(rows),"best_candidate_id":b.get("candidate_id"),"best_covered_count":b.get("covered_count"),"best_links":b.get("links"),"best_pure_bridge_count":b.get("pure_bridge_count"),"best_rich4_count":b.get("rich4_count"),"best_rich3_count":b.get("rich3_count"),"best_productive_connector_count":b.get("productive_connector_count")}
    cov_hist=Counter(int(r.get("covered_count",0)) for r in best_rows)
    bridge_hist=Counter(int(r.get("pure_bridge_count",99)) for r in best_rows)
    miss=Counter()
    for r in best_rows:
        for p in r.get("missing",[]):miss[tuple(p)]+=1
    window_success=Counter()
    for r in reports:
        after=r.get("covered_count_after") or 0;before=r.get("covered_count_before")
        for old,new in zip(r.get("old_window_link_lengths",[]),r.get("new_window_link_lengths",[]) or r.get("old_window_link_lengths",[])):
            window_success[f"{old}->{new}"]+=max(0,int(after)-int(before or 0))+1
    counts={str(k):sum(1 for r in compact if int(r.get("covered_count",0))==k) for k in range(56,65)}
    ordinary=[];diagnostic=[]
    existing_60=set()
    for r in compact:
        c=int(r.get("covered_count",0))
        if c>=61:ordinary.append(r)
        elif c==60 and r.get("canonical_key_sha256") not in existing_60:
            rr=dict(r);rr["ordinary_bank_review_required"]=True;ordinary.append(rr)
        elif 56<=c<=59:diagnostic.append(r)
    originals=[]
    for r in best_rows:
        originals.append({"schema":"mlct-originals-index-v1","candidate_id":r.get("candidate_id"),"canonical_key_sha256":r.get("canonical_key_sha256"),"covered_count":r.get("covered_count"),"links":r.get("links"),"missing":r.get("missing"),"missing_count":r.get("missing_count"),"mode":r.get("mode"),"pure_bridge_count":r.get("pure_bridge_count"),"source_shard":r.get("source_shard"),"source_artifact":r.get("source_artifact"),"source_workflow":"smart-search-21-bridge-compress"})
    summary={
        "schema":"bridge-compress-run-summary-v1","workflow":"smart-search-21-bridge-compress",
        "shard_best_count":len(best_rows),"compact_candidate_count":len(compact),"best":best,
        "exact_coverage_counts":counts,"at_most_six_pure_bridges":sum(1 for r in compact if int(r.get("pure_bridge_count",99))<=6),
        "mode_breakdown":mode_breakdown,
        "coverage_histogram":[{"covered_count":k,"count":v} for k,v in sorted(cov_hist.items(),reverse=True)],
        "bridge_count_histogram":[{"pure_bridge_count":k,"count":v} for k,v in sorted(bridge_hist.items())],
        "missing_point_frequency":[{"point":list(k),"count":v} for k,v in miss.most_common()],
        "window_success":dict(window_success),"ordinary_addition_count":len(ordinary),"diagnostic_addition_count":len(diagnostic),
        "originals_index_count":len(originals),"total_attempts":sum(int(s.get("total_attempts",0)) for s in stats),
    }
    OUT.mkdir(parents=True,exist_ok=True)
    (OUT/"run_summary.json").write_text(json.dumps(summary,indent=2,sort_keys=True),encoding="utf-8")
    (OUT/"mode_breakdown.json").write_text(json.dumps(mode_breakdown,indent=2,sort_keys=True),encoding="utf-8")
    (OUT/"coverage_histogram.json").write_text(json.dumps(summary["coverage_histogram"],indent=2),encoding="utf-8")
    (OUT/"missing_point_frequency.json").write_text(json.dumps(summary["missing_point_frequency"],indent=2),encoding="utf-8")
    (OUT/"bridge_count_histogram.json").write_text(json.dumps(summary["bridge_count_histogram"],indent=2),encoding="utf-8")
    (OUT/"compact_candidates.jsonl").write_text("".join(json.dumps(r,sort_keys=True)+"\n" for r in compact),encoding="utf-8")
    (OUT/"ordinary_candidate_additions.jsonl").write_text("".join(json.dumps(r,sort_keys=True)+"\n" for r in ordinary),encoding="utf-8")
    (OUT/"diagnostic_bridge_compress.jsonl").write_text("".join(json.dumps(r,sort_keys=True)+"\n" for r in diagnostic),encoding="utf-8")
    (OUT/"originals_index.jsonl").write_text("".join(json.dumps(r,sort_keys=True)+"\n" for r in originals),encoding="utf-8")
    lines=["# smart-search-21-bridge-compress summary","",f"- shard-best: `{len(best_rows)}`",f"- compact classes: `{len(compact)}`",f"- best: `{best.get('covered_count',0)}/64`, `{best.get('links',0)}` links",f"- best pure bridges: `{best.get('pure_bridge_count')}`",f"- 61/64+: `{sum(int(r.get('covered_count',0))>=61 for r in compact)}`",f"- 64/64: `{sum(int(r.get('covered_count',0))==64 for r in compact)}`",f"- <=6 pure bridges: `{summary['at_most_six_pure_bridges']}`","","## Best by mode","","| mode | best | links | pure bridges | rich4 | productive |","|---|---:|---:|---:|---:|---:|"]
    for mode,d in mode_breakdown.items():lines.append(f"| `{mode}` | {d['best_covered_count']}/64 | {d['best_links']} | {d['best_pure_bridge_count']} | {d['best_rich4_count']} | {d['best_productive_connector_count']} |")
    (OUT/"summary.md").write_text("\n".join(lines)+"\n",encoding="utf-8")
    print(json.dumps({"best":best.get("covered_count"),"shard_best":len(best_rows),"compact":len(compact),"ordinary":len(ordinary),"diagnostic":len(diagnostic)},indent=2))
if __name__=="__main__":main()
