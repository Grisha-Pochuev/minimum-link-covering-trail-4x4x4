#!/usr/bin/env python3
"""Build the search-27 work-item plan for closing stage B (Python stdlib only).

Input: a B ledger (docs/search27/B-ledger-from-search26.json, or a later
next-ledger.json written by build_search27_summary.py).
Output: a plan file for src/search27/anchored_exact_plan.cpp, one item per
line: "PARENT SUBPATH EXTRA".

Ordering (largest-work-first so the heavy pieces spread over all shards):
  1. every open item, split one level deeper (EXTRA=1);
  2. every not-started item, whole (EXTRA=0).
The plan covers exactly the B work that is not yet complete; every parent of
the depth-2 frontier is either complete in the ledger or reachable from one
or more plan items whose subtrees partition what is left of it.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def items_from_ledger(led: dict) -> tuple[list[tuple[int, str]], list[tuple[int, str]]]:
    if led.get("schema") == "search27-B-ledger-v1":
        return [(p, ".") for p in led["open_parents"]], [(p, ".") for p in led["not_started_parents"]]
    if led.get("schema") == "search27-B-ledger-v2":
        return [tuple(x) for x in led["open_items"]], [tuple(x) for x in led["not_started_items"]]
    raise SystemExit(f"unknown ledger schema {led.get('schema')}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--ledger", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--check", action="store_true", help="fail if --out differs from the regenerated plan")
    args = ap.parse_args()
    led = json.loads(args.ledger.read_text())
    open_items, ns_items = items_from_ledger(led)
    seen = set()
    for it in open_items + ns_items:
        if it in seen:
            raise SystemExit(f"duplicate item {it}")
        seen.add(it)
    lines = [f"# search27 stage-B plan from {args.ledger.name}: {len(open_items)} open items split +1, {len(ns_items)} not-started items whole"]
    lines += [f"{p} {s} 1" for p, s in open_items]
    lines += [f"{p} {s} 0" for p, s in ns_items]
    text = "\n".join(lines) + "\n"
    if args.check:
        if not args.out.exists() or args.out.read_text() != text:
            raise SystemExit(f"{args.out} is not the plan regenerated from {args.ledger}")
        print(f"plan check ok: {len(open_items) + len(ns_items)} items")
        return 0
    args.out.write_text(text)
    print(json.dumps({"items": len(open_items) + len(ns_items), "open_split": len(open_items), "whole": len(ns_items)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
