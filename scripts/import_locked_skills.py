#!/usr/bin/env python3
"""Import small pinned upstream Skill subsets with exact file hashes."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path, PurePosixPath
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SPEC_PATH = ROOT / "catalog" / "locked_imports.json"


class LockedImportError(Exception):
    pass


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git_head(path: Path) -> str:
    result = subprocess.run(
        ["git", "-C", str(path), "rev-parse", "HEAD"],
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode:
        raise LockedImportError(f"not a Git checkout: {path}")
    return result.stdout.strip()


def safe_rel(value: str) -> PurePosixPath:
    path = PurePosixPath(value)
    if (
        not value
        or "\\" in value
        or path.is_absolute()
        or any(part in ("", ".", "..") for part in path.parts)
    ):
        raise LockedImportError(f"unsafe relative path: {value!r}")
    return path


def load_specs() -> dict[str, Any]:
    try:
        document = json.loads(SPEC_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise LockedImportError(f"invalid import specification: {exc}") from exc
    if document.get("schema_version") != 1 or not isinstance(document.get("imports"), dict):
        raise LockedImportError("unsupported import specification")
    return document["imports"]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", action="append", required=True, metavar="KEY=PATH")
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    try:
        specs = load_specs()
        sources: dict[str, Path] = {}
        for value in args.source:
            if "=" not in value:
                raise LockedImportError("--source must use KEY=PATH")
            key, raw_path = value.split("=", 1)
            if key in sources or key not in specs:
                raise LockedImportError(f"unknown or duplicate import key: {key}")
            sources[key] = Path(raw_path).expanduser().resolve()
        plan: list[tuple[Path, Path]] = []
        licenses: list[tuple[Path, Path]] = []
        for key, source_root in sorted(sources.items()):
            spec = specs[key]
            if git_head(source_root) != spec["commit"]:
                raise LockedImportError(f"checkout commit differs: {key}")
            license_source = source_root / "LICENSE"
            if not license_source.is_file() or digest(license_source) != spec["license_sha256"]:
                raise LockedImportError(f"LICENSE differs: {key}")
            skill_root = source_root.joinpath(*safe_rel(spec["source_dir"]).parts)
            destination_root = (
                ROOT / "packs" / spec["pack"] / "skills" / spec["skill"]
            )
            for record in spec["files"]:
                rel = safe_rel(record["path"])
                source = skill_root.joinpath(*rel.parts)
                if not source.is_file() or source.is_symlink():
                    raise LockedImportError(f"source file is missing or unsafe: {key}/{rel}")
                if digest(source) != record["sha256"]:
                    raise LockedImportError(f"source file hash differs: {key}/{rel}")
                plan.append((source, destination_root.joinpath(*rel.parts)))
            licenses.append(
                (license_source, ROOT / "packs" / spec["pack"] / "LICENSE")
            )
        print(f"Locked import plan: groups={len(sources)} files={len(plan)}")
        print("Mode: apply" if args.apply else "Mode: dry-run (no files changed)")
        if args.apply:
            for source, destination in plan + licenses:
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source, destination)
            print("Locked imports applied. Run the source audit next.")
    except (LockedImportError, KeyError, OSError, TypeError) as exc:
        print(f"LOCKED IMPORT FAILED: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
