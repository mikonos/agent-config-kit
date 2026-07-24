#!/usr/bin/env python3
"""Import exact Git tree-locked Skill directories from approved repositories."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import stat
import subprocess
import sys
import tempfile
from pathlib import Path, PurePosixPath
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
EXCLUDED_PARTS = {
    ".cache",
    ".git",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".venv",
    "__pycache__",
    "node_modules",
    "vendor",
    "venv",
}
COMPONENT_PATTERN = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]*")


class ImportError(Exception):
    pass


def load_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ImportError(f"expected JSON object: {path}")
    return payload


def safe_rel(value: str) -> PurePosixPath:
    path = PurePosixPath(value)
    if (
        not value
        or "\\" in value
        or path.is_absolute()
        or any(part in ("", ".", "..") for part in path.parts)
    ):
        raise ImportError(f"unsafe relative path: {value}")
    return path


def safe_tree_dir(value: str) -> PurePosixPath:
    if value == ".":
        return PurePosixPath(".")
    return safe_rel(value)


def safe_component(value: str, label: str) -> str:
    if not isinstance(value, str) or not COMPONENT_PATTERN.fullmatch(value):
        raise ImportError(f"unsafe {label}: {value!r}")
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
        raise ImportError(f"source escapes checkout: {label}") from exc
    current = root
    for part in relative.parts:
        current = current / part
        if is_link_or_reparse(current):
            raise ImportError(f"source link or reparse point: {label}")
    if not path.is_file():
        raise ImportError(f"source file is missing: {label}")


def ensure_safe_destination(path: Path) -> None:
    try:
        relative = path.relative_to(ROOT)
    except ValueError as exc:
        raise ImportError(f"destination escapes package root: {path}") from exc
    current = ROOT
    for part in relative.parts:
        current = current / part
        if current.exists() and is_link_or_reparse(current):
            raise ImportError(f"destination link or reparse point: {current}")


def git_value(repository: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(repository), *args],
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode:
        raise ImportError(result.stderr.strip() or f"git command failed: {' '.join(args)}")
    return result.stdout.strip()


def git_bytes(repository: Path, *args: str) -> bytes:
    result = subprocess.run(
        ["git", "-C", str(repository), *args],
        capture_output=True,
        check=False,
    )
    if result.returncode:
        raise ImportError(
            result.stderr.decode("utf-8", errors="replace").strip()
            or f"git command failed: {' '.join(args)}"
        )
    return result.stdout


def digest_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def git_tree_files(
    repository: Path,
    source_dir: PurePosixPath,
    include_files: set[str] | None = None,
) -> list[tuple[str, bytes, int]]:
    arguments = ["ls-tree", "-r", "-z", "HEAD"]
    if source_dir.as_posix() != ".":
        arguments.extend(("--", source_dir.as_posix()))
    raw = git_bytes(repository, *arguments)
    result: list[tuple[str, bytes, int]] = []
    for record in raw.split(b"\0"):
        if not record:
            continue
        try:
            header, path_raw = record.split(b"\t", 1)
            mode_raw, object_type, _ = header.split(b" ", 2)
            path = path_raw.decode("utf-8")
        except (UnicodeDecodeError, ValueError) as exc:
            raise ImportError("invalid Git tree record") from exc
        relative = (
            PurePosixPath(path).as_posix()
            if source_dir.as_posix() == "."
            else PurePosixPath(path).relative_to(source_dir).as_posix()
        )
        if include_files is not None and relative not in include_files:
            continue
        if object_type != b"blob" or mode_raw not in (b"100644", b"100755"):
            raise ImportError(f"unsupported Git tree entry: {path}")
        mode = 0o755 if mode_raw == b"100755" else 0o644
        result.append((relative, git_bytes(repository, "show", f"HEAD:{path}"), mode))
    return result


def skill_name_from_tree(files: list[tuple[str, bytes, int]]) -> str:
    entry = next((data for relative, data, _ in files if relative == "SKILL.md"), None)
    if entry is None:
        raise ImportError("Skill tree has no root SKILL.md")
    try:
        lines = entry.decode("utf-8").splitlines()
    except UnicodeDecodeError as exc:
        raise ImportError("Skill SKILL.md is not UTF-8") from exc
    if not lines or lines[0].strip() != "---":
        raise ImportError("Skill SKILL.md has no YAML frontmatter")
    closing = next(
        (index for index, line in enumerate(lines[1:], start=1) if line.strip() == "---"),
        None,
    )
    if closing is None:
        raise ImportError("Skill SKILL.md has unterminated YAML frontmatter")
    top_level_lines = [
        line
        for line in lines[1:closing]
        if line and not line[0].isspace()
    ]
    if any(
        (re.match(r"""^["']""", line) is not None and ":" in line)
        or re.match(r"^\?", line) is not None
        for line in top_level_lines
    ):
        raise ImportError("Skill SKILL.md uses an unsupported complex YAML key")
    name_lines = [
        line
        for line in top_level_lines
        if re.match(r"""^(?:name|"name"|'name')\s*:""", line)
    ]
    if len(name_lines) != 1:
        raise ImportError("Skill SKILL.md must declare one plain name")
    match = re.fullmatch(
        r"\s*name\s*:\s*([A-Za-z0-9][A-Za-z0-9._-]*)\s*",
        name_lines[0],
    )
    if match is None:
        raise ImportError("Skill SKILL.md name must be a plain safe component")
    return match.group(1)


def atomic_write(path: Path, data: bytes, mode: int) -> None:
    ensure_safe_destination(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temp_name = tempfile.mkstemp(
        dir=str(path.parent),
        prefix=f".{path.name}.",
    )
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(data)
        os.chmod(temp_name, mode)
        os.replace(temp_name, path)
    except BaseException:
        try:
            os.unlink(temp_name)
        except OSError:
            pass
        raise


def choose_pack(group: dict[str, Any], skill_path: str) -> str:
    direct = group.get("pack")
    if isinstance(direct, str) and direct:
        return safe_component(direct, "pack")
    rules = group.get("pack_by_source_prefix")
    if not isinstance(rules, dict):
        raise ImportError("import group has no pack mapping")
    matches = [
        (prefix, pack)
        for prefix, pack in rules.items()
        if isinstance(prefix, str)
        and isinstance(pack, str)
        and skill_path.startswith(prefix)
    ]
    if len(matches) != 1:
        raise ImportError(f"Skill path has no unique pack mapping: {skill_path}")
    return safe_component(matches[0][1], "pack")


def plan_imports(
    groups: dict[str, Any],
    sources: dict[str, Any],
    pins: dict[str, Any],
    checkouts: dict[str, Path],
) -> tuple[
    list[tuple[bytes, Path, int]],
    list[tuple[bytes, Path, int]],
    dict[str, dict[str, Any]],
]:
    pin_by_name = {entry["name"]: entry for entry in pins["skills"]}
    files: list[tuple[bytes, Path, int]] = []
    licenses: list[tuple[bytes, Path, int]] = []
    admitted: dict[str, dict[str, Any]] = {}
    destination_names: set[str] = set()
    for key, checkout in sorted(checkouts.items()):
        if key not in groups:
            raise ImportError(f"unknown import group: {key}")
        group = groups[key]
        commit = group["commit"]
        if git_value(checkout, "rev-parse", "HEAD") != commit:
            raise ImportError(f"checkout commit differs: {key}")
        license_rel = safe_rel(group["license_path"])
        license_data = git_bytes(
            checkout,
            "show",
            f"HEAD:{license_rel.as_posix()}",
        )
        if digest_bytes(license_data) != group["license_sha256"]:
            raise ImportError(f"license differs: {key}")
        explicit_skills = group.get("skills")
        if explicit_skills is not None:
            if not isinstance(explicit_skills, dict) or not explicit_skills:
                raise ImportError(f"invalid explicit skills: {key}")
            selected = []
            for name, record in sorted(explicit_skills.items()):
                name = safe_component(name, "Skill name")
                if not isinstance(record, dict):
                    raise ImportError(f"invalid explicit Skill record: {key}/{name}")
                source_dir = safe_tree_dir(record["source_dir"])
                tree_sha = record["tree_sha"]
                if not isinstance(tree_sha, str) or not re.fullmatch(r"[0-9a-f]{40}", tree_sha):
                    raise ImportError(f"invalid explicit Skill tree SHA: {key}/{name}")
                include_files = record.get("include_files")
                if include_files is not None:
                    if not isinstance(include_files, list) or not include_files:
                        raise ImportError(f"invalid include_files: {key}/{name}")
                    include_files = [safe_rel(value).as_posix() for value in include_files]
                    if len(include_files) != len(set(include_files)) or "SKILL.md" not in include_files:
                        raise ImportError(f"include_files must uniquely include SKILL.md: {key}/{name}")
                selected.append(
                    {
                        "name": name,
                        "skill_path": (
                            "SKILL.md"
                            if source_dir.as_posix() == "."
                            else f"{source_dir.as_posix()}/SKILL.md"
                        ),
                        "tree_sha": tree_sha,
                        "include_files": include_files,
                    }
                )
        else:
            configured_allowed = group.get("allow_skills")
            if configured_allowed is None:
                allowed = {
                    entry["name"]
                    for entry in sources["skills"]
                    if entry["source_url"] == group["origin"]
                    and pin_by_name.get(entry["name"], {}).get("status") == "exact_current"
                    and pin_by_name[entry["name"]].get("commit") == commit
                }
            elif isinstance(configured_allowed, list):
                allowed = set(configured_allowed)
            else:
                raise ImportError(f"invalid allow_skills: {key}")
            selected = [
                entry
                for entry in sources["skills"]
                if entry["name"] in allowed
                and entry["source_url"] == group["origin"]
                and pin_by_name.get(entry["name"], {}).get("status") == "exact_current"
                and pin_by_name[entry["name"]].get("commit") == commit
            ]
            if set(entry["name"] for entry in selected) != allowed:
                missing = sorted(allowed - {entry["name"] for entry in selected})
                raise ImportError(
                    f"approved Skill is not exactly pinned in {key}: {', '.join(missing)}"
                )
        used_packs: set[str] = set()
        for entry in sorted(selected, key=lambda item: item["name"]):
            name = safe_component(entry["name"], "Skill name")
            if name in destination_names:
                raise ImportError(f"duplicate destination Skill: {name}")
            destination_names.add(name)
            source_dir_rel = safe_tree_dir(
                PurePosixPath(entry["skill_path"]).parent.as_posix()
            )
            include_files = entry.get("include_files")
            if source_dir_rel.as_posix() == "." and include_files is None:
                raise ImportError(f"root Skill requires include_files: {key}/{name}")
            actual_tree = git_value(
                checkout,
                "rev-parse",
                (
                    "HEAD^{tree}"
                    if source_dir_rel.as_posix() == "."
                    else f"HEAD:{source_dir_rel.as_posix()}"
                ),
            )
            if actual_tree != entry["tree_sha"]:
                raise ImportError(f"tree SHA differs: {name}")
            if git_value(
                checkout,
                "status",
                "--porcelain",
                "--untracked-files=all",
                "--",
                source_dir_rel.as_posix(),
            ):
                raise ImportError(f"checkout subtree has local changes: {name}")
            pack = choose_pack(group, entry["skill_path"])
            used_packs.add(pack)
            destination_dir = ROOT / "packs" / pack / "skills" / name
            ensure_safe_destination(destination_dir)
            if destination_dir.exists():
                raise ImportError(f"destination already exists: {destination_dir.relative_to(ROOT)}")
            tree_files = git_tree_files(
                checkout,
                source_dir_rel,
                set(include_files) if include_files is not None else None,
            )
            if not tree_files:
                raise ImportError(f"checkout subtree has no tracked files: {name}")
            if include_files is not None:
                by_relative = {
                    relative: (relative, data, mode)
                    for relative, data, mode in tree_files
                }
                missing = sorted(set(include_files) - set(by_relative))
                if missing:
                    raise ImportError(
                        f"pinned include file is missing in {name}: {', '.join(missing)}"
                    )
                tree_files = [by_relative[relative] for relative in include_files]
            declared_name = skill_name_from_tree(tree_files)
            if declared_name != name:
                raise ImportError(
                    f"Skill tree name differs: {name!r} != {declared_name!r}"
                )
            for relative, data, mode in tree_files:
                rel = PurePosixPath(relative)
                if any(part in EXCLUDED_PARTS for part in rel.parts):
                    raise ImportError(f"excluded artifact in {name}: {rel}")
                destination = destination_dir.joinpath(*rel.parts)
                ensure_safe_destination(destination)
                files.append((data, destination, mode))
            admitted[name] = {
                "pack": pack,
                "group": key,
                "license": group["license"],
                "origin": group["origin"],
                "commit": commit,
            }
        for pack in sorted(used_packs):
            license_destination = ROOT / "packs" / pack / "LICENSE"
            ensure_safe_destination(license_destination)
            licenses.append((license_data, license_destination, 0o644))
    return files, licenses, admitted


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", action="append", required=True, metavar="GROUP=PATH")
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    try:
        spec = load_json(ROOT / "catalog" / "tree_import_groups.json")
        if spec.get("schema_version") != 1 or not isinstance(spec.get("groups"), dict):
            raise ImportError("unsupported tree import specification")
        checkouts: dict[str, Path] = {}
        for value in args.source:
            if "=" not in value:
                raise ImportError("--source must use GROUP=PATH")
            key, raw_path = value.split("=", 1)
            if key in checkouts:
                raise ImportError(f"duplicate source group: {key}")
            checkouts[key] = Path(raw_path).expanduser().resolve()
        files, licenses, admitted = plan_imports(
            spec["groups"],
            load_json(ROOT / "catalog" / "runtime_sources.json"),
            load_json(ROOT / "catalog" / "runtime_pins.json"),
            checkouts,
        )
        print(
            f"Tree import plan: groups={len(checkouts)} "
            f"skills={len(admitted)} files={len(files)}"
        )
        print("Mode: apply" if args.apply else "Mode: dry-run (no files changed)")
        if args.apply:
            for data, destination, mode in files + licenses:
                atomic_write(destination, data, mode)
            output = ROOT / "catalog" / "tree_import_result.json"
            atomic_write(
                output,
                (
                    json.dumps(
                        {"schema_version": 1, "skills": admitted},
                        ensure_ascii=False,
                        indent=2,
                        sort_keys=True,
                    )
                    + "\n"
                ).encode("utf-8"),
                0o644,
            )
            print("Tree-locked imports applied. Run the source audit next.")
    except (ImportError, KeyError, OSError, TypeError, json.JSONDecodeError) as exc:
        print(f"TREE IMPORT FAILED: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
