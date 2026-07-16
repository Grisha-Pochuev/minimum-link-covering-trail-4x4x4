#!/usr/bin/env python3
"""Static and executable release gate for numbered GitHub searches."""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
import tarfile
import zipfile
from pathlib import Path
from typing import Any


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def validate_archive(path: Path, kind: str, required_members: list[str]) -> list[str]:
    if kind == "zip":
        with zipfile.ZipFile(path) as archive:
            bad_member = archive.testzip()
            require(bad_member is None, f"{path}: bad ZIP member {bad_member}")
            members = archive.namelist()
    elif kind in {"tar", "tar.gz", "tgz"}:
        mode = "r:gz" if kind in {"tar.gz", "tgz"} else "r:"
        with tarfile.open(path, mode) as archive:
            members = archive.getnames()
            for member in archive.getmembers():
                if member.isfile():
                    stream = archive.extractfile(member)
                    require(stream is not None, f"{path}: cannot read {member.name}")
                    while stream.read(1024 * 1024):
                        pass
    elif kind in {"none", ""}:
        members = []
    else:
        raise RuntimeError(f"{path}: unsupported archive kind {kind!r}")

    missing = sorted(set(required_members) - set(members))
    require(not missing, f"{path}: missing archive members: {missing}")
    return members


def run_command(repo: Path, command: list[str]) -> None:
    require(
        command and all(isinstance(part, str) and part for part in command),
        f"invalid command array: {command!r}",
    )
    completed = subprocess.run(command, cwd=repo, check=False)
    require(
        completed.returncode == 0,
        f"command failed with exit {completed.returncode}: {command!r}",
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", required=True, type=Path)
    parser.add_argument("--repo", type=Path, default=Path("."))
    parser.add_argument("--report", type=Path)
    parser.add_argument("--skip-commands", action="store_true")
    args = parser.parse_args()

    repo = args.repo.resolve()
    manifest_path = args.manifest if args.manifest.is_absolute() else repo / args.manifest
    data: dict[str, Any] = json.loads(manifest_path.read_text(encoding="utf-8"))
    require(data.get("schema") == "step3-release-v1", "manifest schema must be step3-release-v1")

    workflow_rel = data["workflow_path"]
    trigger_rel = data["trigger_path"]
    workflow_path = repo / workflow_rel
    trigger_path = repo / trigger_rel
    require(workflow_path.is_file(), f"missing workflow: {workflow_rel}")
    require(trigger_path.is_file(), f"missing trigger: {trigger_rel}")

    workflow_text = workflow_path.read_text(encoding="utf-8")
    require(trigger_rel in workflow_text, f"workflow does not contain trigger path: {trigger_rel}")
    for literal in data.get("required_workflow_literals", []):
        require(literal in workflow_text, f"workflow is missing required literal: {literal!r}")
    for literal in data.get("forbidden_workflow_literals", []):
        require(literal not in workflow_text, f"workflow contains forbidden literal: {literal!r}")

    checked_files: list[dict[str, Any]] = []
    for item in data.get("files", []):
        relative_path = item["path"]
        path = repo / relative_path
        require(path.is_file(), f"missing release file: {relative_path}")
        actual_hash = sha256_file(path)
        expected_hash = item.get("sha256")
        if expected_hash:
            require(
                actual_hash == expected_hash,
                f"{relative_path}: sha256 mismatch: expected {expected_hash}, got {actual_hash}",
            )
        if item.get("max_bytes") is not None:
            require(
                path.stat().st_size <= int(item["max_bytes"]),
                f"{relative_path}: {path.stat().st_size} bytes exceeds {item['max_bytes']}",
            )
        archive_kind = item.get("archive", "none")
        members = validate_archive(path, archive_kind, list(item.get("required_members", [])))
        checked_files.append(
            {
                "path": relative_path,
                "sha256": actual_hash,
                "bytes": path.stat().st_size,
                "archive": archive_kind,
                "members": len(members),
            }
        )

    for group in data.get("concatenations", []):
        parts = [repo / relative_path for relative_path in group["parts"]]
        for part in parts:
            require(part.is_file(), f"missing concatenation part: {part}")
        payload = b"".join(part.read_bytes() for part in parts)
        actual_hash = hashlib.sha256(payload).hexdigest()
        require(
            actual_hash == group["sha256"],
            f"{group['name']}: concatenated sha256 mismatch: expected {group['sha256']}, got {actual_hash}",
        )
        if group.get("max_part_bytes") is not None:
            oversized = [
                str(part.relative_to(repo))
                for part in parts
                if part.stat().st_size > int(group["max_part_bytes"])
            ]
            require(not oversized, f"{group['name']}: oversized parts: {oversized}")

    if not args.skip_commands:
        for command in data.get("commands", []):
            run_command(repo, command)

    report = {
        "schema": "step3-release-report-v1",
        "manifest": str(manifest_path.relative_to(repo)),
        "workflow_path": workflow_rel,
        "trigger_path": trigger_rel,
        "checked_files": checked_files,
        "commands_run": 0 if args.skip_commands else len(data.get("commands", [])),
        "status": "pass",
    }
    encoded = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.report:
        report_path = args.report if args.report.is_absolute() else repo / args.report
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(encoded, encoding="utf-8")
    print(encoded, end="")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (
        KeyError,
        OSError,
        RuntimeError,
        json.JSONDecodeError,
        zipfile.BadZipFile,
        tarfile.TarError,
    ) as exc:
        print(f"release gate failed: {exc}", file=sys.stderr)
        raise SystemExit(1)
