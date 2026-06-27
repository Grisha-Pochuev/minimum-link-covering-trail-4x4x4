from __future__ import annotations

import argparse
import re
from pathlib import Path

# New best frontier after repair-search-5 has 6 missing points:
# (1,1,0), (1,2,1), (2,1,0), (3,1,1), (3,1,2), (3,1,3).
# The C++ engine works in coordinate_scale=2, so these become:
NEW6_DEFECTS_CPP = "vector<Pt> defects = {{2,2,0},{2,4,2},{4,2,0},{6,2,2},{6,2,4},{6,2,6}};"


def main() -> int:
    ap = argparse.ArgumentParser(description="Generate a repair engine aimed at the 58/64 six-point defect frontier.")
    ap.add_argument("--source", default="cpp/repair56_search.cpp")
    ap.add_argument("--out", default="build/repair58_search.cpp")
    args = ap.parse_args()

    src = Path(args.source)
    out = Path(args.out)
    text = src.read_text()

    text, n = re.subn(r"vector<Pt> defects = \{\{[^;]+;", NEW6_DEFECTS_CPP, text, count=1)
    if n != 1:
        raise SystemExit("Could not replace target defect list in C++ source")

    text = text.replace("repair56_search parameters:", "repair58_defect_search parameters:")
    text = text.replace('"schema": "repair-mlct-shard-v1"', '"schema": "repair58-defect-shard-v1"')
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(text)
    print(f"wrote {out} with new 6-point target defects")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
