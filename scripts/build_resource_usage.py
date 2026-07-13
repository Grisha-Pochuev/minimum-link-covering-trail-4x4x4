#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


def parse_elapsed(text: str) -> float:
    m=re.search(r'Elapsed \(wall clock\) time.*?:\s*([0-9:.]+)',text)
    if not m: return 0.0
    parts=[float(x) for x in m.group(1).split(':')]
    if len(parts)==3:return parts[0]*3600+parts[1]*60+parts[2]
    if len(parts)==2:return parts[0]*60+parts[1]
    return parts[0]


def grab(text: str, pattern: str, default='0') -> str:
    m=re.search(pattern,text)
    return m.group(1).strip() if m else default


def main() -> None:
    ap=argparse.ArgumentParser();ap.add_argument('--raw',type=Path,required=True);ap.add_argument('--stats',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);args=ap.parse_args()
    text=args.raw.read_text(encoding='utf-8',errors='replace');stats=json.loads(args.stats.read_text())
    peak_kb=int(grab(text,r'Maximum resident set size \(kbytes\):\s*(\d+)'))
    user=float(grab(text,r'User time \(seconds\):\s*([0-9.]+)'))
    system=float(grab(text,r'System time \(seconds\):\s*([0-9.]+)'))
    elapsed=parse_elapsed(text);attempts=int(stats.get('attempts',0))
    row={'schema':'core-transplant-resource-usage-v1','shard':int(stats['shard']),'peak_ram_mib':round(peak_kb/1024,3),'peak_ram_gib':round(peak_kb/1024/1024,4),'elapsed_seconds':elapsed,'user_cpu_seconds':user,'system_cpu_seconds':system,'cpu_utilization_percent':round(100*(user+system)/elapsed,2) if elapsed else 0,'attempts':attempts,'attempts_per_second':round(attempts/elapsed,2) if elapsed else 0}
    args.out.write_text(json.dumps(row,indent=2)+'\n');print(json.dumps(row,indent=2))
if __name__=='__main__':main()
