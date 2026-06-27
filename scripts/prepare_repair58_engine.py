from __future__ import annotations

import argparse
import re
from pathlib import Path

# New best frontier after smart-search-6-defect smoke run 28275666411 has 5 missing points:
# (1,2,1), (2,1,2), (2,2,3), (3,1,0), (3,1,3).
# The C++ engine works in coordinate_scale=2, so these become:
NEW_DEFECTS_CPP = "vector<Pt> defects = {{2,4,2},{4,2,4},{4,4,6},{6,2,0},{6,2,6}};"

# Do not split the 20 jobs evenly. The smoke run showed that subcube stitching,
# fractional bridge, and local repair all reached 59/64, so the full run spends
# most shards in those modes while keeping transition/control probes.
NEW_MODE_FOR_CPP = r'''string mode_for(int shard) {
    if (shard < 5) return "subcube_stitch22";
    if (shard < 10) return "fractional_bridge22";
    if (shard < 15) return "repair56_target8";
    if (shard < 18) return "transition_penalty22";
    if (shard == 18) return "rich_segment_catalog";
    return "integer_control22";
}'''


def main() -> int:
    ap = argparse.ArgumentParser(description="Generate a repair engine aimed at the current high-frontier defect set.")
    ap.add_argument("--source", default="cpp/repair56_search.cpp")
    ap.add_argument("--out", default="build/repair58_search.cpp")
    args = ap.parse_args()

    src = Path(args.source)
    out = Path(args.out)
    text = src.read_text()

    text, n = re.subn(r"vector<Pt> defects = \{\{[^;]+;", NEW_DEFECTS_CPP, text, count=1)
    if n != 1:
        raise SystemExit("Could not replace target defect list in C++ source")

    text, n = re.subn(r"string mode_for\(int shard\) \{.*?\n\}", NEW_MODE_FOR_CPP, text, count=1, flags=re.S)
    if n != 1:
        raise SystemExit("Could not replace mode_for shard allocation")

    # Keep more diverse bank and smoke-run seeds now that candidates/bank.jsonl is exported into seed JSON files.
    text = text.replace("if (seeds.size() > 256) seeds.resize(256);", "if (seeds.size() > 512) seeds.resize(512);")
    text = text.replace("repair56_search parameters:", "repair59_defect_search parameters:")
    text = text.replace(r'\"schema\": \"repair-mlct-shard-v1\"', r'\"schema\": \"repair59-defect-shard-v1\"')
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(text)
    print(f"wrote {out} with current high-frontier target defects and smart mode allocation")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
