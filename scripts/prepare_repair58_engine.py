from __future__ import annotations

import argparse
import re
from pathlib import Path

# New best frontier after repair-search-5 has 6 missing points:
# (1,1,0), (1,2,1), (2,1,0), (3,1,1), (3,1,2), (3,1,3).
# The C++ engine works in coordinate_scale=2, so these become:
NEW6_DEFECTS_CPP = "vector<Pt> defects = {{2,2,0},{2,4,2},{4,2,0},{6,2,2},{6,2,4},{6,2,6}};"

# Do not split the 20 jobs evenly. The previous run showed that repair,
# transition penalty, fractional bridge, and subcube stitching were stronger
# than the broad rich/integer controls, so this run spends most shards there.
NEW_MODE_FOR_CPP = r'''string mode_for(int shard) {
    if (shard < 6) return "repair56_target8";
    if (shard < 11) return "transition_penalty22";
    if (shard < 15) return "fractional_bridge22";
    if (shard < 18) return "subcube_stitch22";
    if (shard == 18) return "rich_segment_catalog";
    return "integer_control22";
}'''


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

    text, n = re.subn(r"string mode_for\(int shard\) \{.*?\n\}", NEW_MODE_FOR_CPP, text, count=1, flags=re.S)
    if n != 1:
        raise SystemExit("Could not replace mode_for shard allocation")

    # Keep more diverse bank seeds now that candidates/bank.jsonl is exported into seed JSON files.
    text = text.replace("if (seeds.size() > 256) seeds.resize(256);", "if (seeds.size() > 512) seeds.resize(512);")
    text = text.replace("repair56_search parameters:", "repair58_defect_search parameters:")
    text = text.replace(r'\"schema\": \"repair-mlct-shard-v1\"', r'\"schema\": \"repair58-defect-shard-v1\"')
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(text)
    print(f"wrote {out} with new 6-point target defects and smart mode allocation")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
