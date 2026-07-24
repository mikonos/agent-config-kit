#!/usr/bin/env python3
"""Import licensed local snapshots only when every admitted file hash matches."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import stat
import sys
from pathlib import Path, PurePosixPath
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SPEC_PATH = ROOT / "catalog" / "snapshot_imports.json"


class SnapshotImportError(Exception):
    pass


COMPONENT_PATTERN = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]*")


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def safe_rel(value: str) -> PurePosixPath:
    path = PurePosixPath(value)
    if (
        not value
        or "\\" in value
        or path.is_absolute()
        or any(part in ("", ".", "..") for part in path.parts)
    ):
        raise SnapshotImportError(f"unsafe relative path: {value!r}")
    return path


def safe_component(value: str, label: str) -> str:
    if not isinstance(value, str) or not COMPONENT_PATTERN.fullmatch(value):
        raise SnapshotImportError(f"unsafe {label}: {value!r}")
    return value


def is_link_or_reparse(path: Path) -> bool:
    try:
        metadata = path.lstat()
    except OSError:
        return True
    reparse_flag = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400)
    attributes = getattr(metadata, "st_file_attributes", 0)
    return path.is_symlink() or bool(attributes & reparse_flag)


def ensure_regular_source(root: Path, path: Path, label: str) -> None:
    try:
        path.resolve(strict=True).relative_to(root.resolve(strict=True))
        relative = path.relative_to(root)
    except (OSError, ValueError) as exc:
        raise SnapshotImportError(f"source escapes its root: {label}") from exc
    current = root
    for part in relative.parts:
        current = current / part
        if is_link_or_reparse(current):
            raise SnapshotImportError(f"source link or reparse point: {label}")
    if not path.is_file():
        raise SnapshotImportError(f"source file is missing: {label}")


def ensure_safe_destination(path: Path) -> None:
    try:
        relative = path.relative_to(ROOT)
    except ValueError as exc:
        raise SnapshotImportError(f"destination escapes package root: {path}") from exc
    current = ROOT
    for part in relative.parts:
        current = current / part
        if current.exists() and is_link_or_reparse(current):
            raise SnapshotImportError(f"destination link or reparse point: {current}")


def load_specs() -> dict[str, Any]:
    document = json.loads(SPEC_PATH.read_text(encoding="utf-8"))
    if document.get("schema_version") != 1 or not isinstance(document.get("imports"), dict):
        raise SnapshotImportError("unsupported snapshot specification")
    return document["imports"]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", action="append", required=True, metavar="LABEL=PATH")
    parser.add_argument(
        "--only",
        action="append",
        metavar="IMPORT",
        help="limit the operation to one named import; repeat as needed",
    )
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    try:
        roots: dict[str, Path] = {}
        for value in args.source:
            if "=" not in value:
                raise SnapshotImportError("--source must use LABEL=PATH")
            label, raw_path = value.split("=", 1)
            if label in roots:
                raise SnapshotImportError(f"duplicate source label: {label}")
            roots[label] = Path(raw_path).expanduser().resolve()
        specs = load_specs()
        selected_keys = sorted(set(args.only or specs))
        unknown = sorted(set(selected_keys) - set(specs))
        if unknown:
            raise SnapshotImportError(
                "unknown snapshot import: " + ", ".join(unknown)
            )
        plan: list[tuple[Path, Path]] = []
        licenses: list[tuple[Path, Path]] = []
        for key in selected_keys:
            spec = specs[key]
            source_root = roots.get(spec["source"])
            if source_root is None:
                raise SnapshotImportError(f"missing source label for import: {key}")
            source_dir = source_root.joinpath(*safe_rel(spec["source_dir"]).parts)
            pack = safe_component(spec["pack"], "pack")
            if "skills" in spec:
                for name, expected_hash in sorted(spec["skills"].items()):
                    name = safe_component(name, "Skill name")
                    source = source_dir / name / "SKILL.md"
                    ensure_regular_source(source_root, source, f"{key}/{name}")
                    if digest(source) != expected_hash:
                        raise SnapshotImportError(f"snapshot differs: {key}/{name}")
                    destination = ROOT / "packs" / pack / "skills" / name / "SKILL.md"
                    ensure_safe_destination(destination)
                    plan.append((source, destination))
            else:
                skill = safe_component(spec["skill"], "Skill name")
                for record in spec["files"]:
                    rel = safe_rel(record["path"])
                    source = source_dir.joinpath(*rel.parts)
                    ensure_regular_source(source_root, source, f"{key}/{rel}")
                    if digest(source) != record["sha256"]:
                        raise SnapshotImportError(f"snapshot differs: {key}/{rel}")
                    destination = (
                        ROOT / "packs" / pack / "skills" / skill
                    ).joinpath(*rel.parts)
                    ensure_safe_destination(destination)
                    plan.append((source, destination))
            license_source_label = spec.get("license_source", spec["source"])
            license_root = roots.get(license_source_label)
            if license_root is None:
                raise SnapshotImportError(
                    f"missing license source label for import: {key}"
                )
            license_source = license_root.joinpath(
                *safe_rel(spec["license_path"]).parts
            )
            ensure_regular_source(license_root, license_source, f"{key}/LICENSE")
            if digest(license_source) != spec["license_sha256"]:
                raise SnapshotImportError(f"LICENSE differs: {key}")
            license_destination = ROOT / "packs" / pack / "LICENSE"
            ensure_safe_destination(license_destination)
            licenses.append((license_source, license_destination))
        print(f"Snapshot import plan: groups={len(licenses)} files={len(plan)}")
        print("Mode: apply" if args.apply else "Mode: dry-run (no files changed)")
        if args.apply:
            for source, destination in plan + licenses:
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source, destination)
            print("Snapshot imports applied. Run the source audit next.")
    except (SnapshotImportError, OSError, KeyError, TypeError, json.JSONDecodeError) as exc:
        print(f"SNAPSHOT IMPORT FAILED: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
