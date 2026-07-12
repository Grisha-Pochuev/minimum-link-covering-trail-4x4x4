#!/usr/bin/env python3
from pathlib import Path
base=Path(__file__).with_name("endpoint_repair_parts")
source="".join(p.read_text(encoding="utf-8") for p in sorted(base.glob("part-*.pyfrag")))
exec(compile(source,str(base),"exec"),globals(),globals())
