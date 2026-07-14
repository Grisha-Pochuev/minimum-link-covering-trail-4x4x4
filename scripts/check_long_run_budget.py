#!/usr/bin/env python3
"""Fail preflight when a GitHub Actions search leaves too little job headroom."""
from __future__ import annotations

import argparse


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--search-seconds", type=int, required=True)
    parser.add_argument("--timeout-minutes", type=int, required=True)
    parser.add_argument("--minimum-headroom-seconds", type=int, default=900)
    args = parser.parse_args()

    if args.search_seconds <= 0 or args.timeout_minutes <= 0:
        raise SystemExit("search seconds and timeout minutes must be positive")
    headroom = args.timeout_minutes * 60 - args.search_seconds
    print({
        "search_seconds": args.search_seconds,
        "timeout_minutes": args.timeout_minutes,
        "headroom_seconds": headroom,
        "minimum_headroom_seconds": args.minimum_headroom_seconds,
    })
    if headroom < args.minimum_headroom_seconds:
        raise SystemExit(
            f"unsafe long-run budget: only {headroom}s headroom; "
            f"need at least {args.minimum_headroom_seconds}s for setup, final trim, "
            "exact verification and artifact upload"
        )


if __name__ == "__main__":
    main()
