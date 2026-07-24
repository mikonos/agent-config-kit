#!/usr/bin/env python3
"""Conflict-safe project installer for Agent Config Kit."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import stat
import sys
import tempfile
import time
import uuid
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any


if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")


PACKAGE_ROOT = Path(__file__).resolve().parents[2]
MANIFEST_PATH = PACKAGE_ROOT / "manifest.json"
STATE_REL = PurePosixPath(".agent-config-kit/install-state.json")


class ConfigError(Exception):
    pass


@dataclass(frozen=True)
class PlannedFile:
    source: Path
    source_rel: str
    target_rel: str
    sha256: str
    mode: int


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def is_link_or_reparse(path: Path) -> bool:
    try:
        metadata = path.lstat()
    except OSError:
        return True
    reparse_flag = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400)
    attributes = getattr(metadata, "st_file_attributes", 0)
    return path.is_symlink() or bool(attributes & reparse_flag)


def ensure_contained(path: Path, root: Path, label: str) -> None:
    try:
        path.resolve(strict=False).relative_to(root.resolve(strict=True))
    except (OSError, ValueError) as exc:
        raise ConfigError(f"{label} escapes its root: {path}") from exc


def safe_rel(value: str, label: str) -> PurePosixPath:
    if not isinstance(value, str) or not value or "\\" in value:
        raise ConfigError(f"{label} must be a non-empty POSIX relative path: {value!r}")
    path = PurePosixPath(value)
    if path.is_absolute() or any(part in ("", ".", "..") for part in path.parts):
        raise ConfigError(f"unsafe {label}: {value!r}")
    return path


def ensure_source(path_value: str) -> Path:
    rel = safe_rel(path_value, "source path")
    current = PACKAGE_ROOT
    for part in rel.parts:
        current = current / part
        if is_link_or_reparse(current):
            raise ConfigError(f"source link or reparse point is not allowed: {rel}")
    ensure_contained(current, PACKAGE_ROOT, "source")
    if not current.is_file():
        raise ConfigError(f"source file is missing: {rel}")
    return current


def prepare_target(value: str) -> Path:
    target = Path(value).expanduser()
    if not target.is_absolute():
        target = (Path.cwd() / target).absolute()
    if target.exists() and is_link_or_reparse(target):
        raise ConfigError(f"target root may not be a link or reparse point: {target}")
    if not target.exists() or not target.is_dir():
        raise ConfigError(f"target must be an existing directory: {target}")
    return target.resolve()


def target_path(root: Path, rel_value: str) -> Path:
    rel = safe_rel(rel_value, "target path")
    current = root
    for part in rel.parts[:-1]:
        current = current / part
        if current.exists() and is_link_or_reparse(current):
            raise ConfigError(f"target parent link or reparse point is not allowed: {current}")
        if current.exists() and not current.is_dir():
            raise ConfigError(f"target parent is not a directory: {current}")
    final = root.joinpath(*rel.parts)
    if final.exists() and is_link_or_reparse(final):
        raise ConfigError(f"target link or reparse point is not allowed: {final}")
    ensure_contained(final, root, "target")
    return final


def load_manifest() -> dict[str, Any]:
    if is_link_or_reparse(MANIFEST_PATH) or not MANIFEST_PATH.is_file():
        raise ConfigError("manifest.json is missing or is a symlink")
    try:
        manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ConfigError(f"invalid manifest.json: {exc}") from exc
    if manifest.get("schema_version") != 1:
        raise ConfigError("unsupported manifest schema_version")
    if not isinstance(manifest.get("release"), str):
        raise ConfigError("manifest release must be a string")
    for key in (
        "profiles",
        "skill_packs",
        "capability_requirements",
        "runtimes",
        "common_files",
    ):
        if key not in manifest:
            raise ConfigError(f"manifest is missing {key}")
    return manifest


def parse_skill_name(skill_file: Path) -> str:
    text = skill_file.read_text(encoding="utf-8")
    lines = text.splitlines()
    if len(lines) < 4 or lines[0] != "---":
        raise ConfigError(f"skill has no YAML frontmatter: {skill_file}")
    try:
        end = lines.index("---", 1)
    except ValueError as exc:
        raise ConfigError(f"skill frontmatter is not closed: {skill_file}") from exc
    fields: dict[str, str] = {}
    for line in lines[1:end]:
        if not line.strip():
            continue
        if line[:1].isspace():
            continue
        if ":" not in line:
            raise ConfigError(f"unsupported skill frontmatter line in {skill_file}: {line}")
        key, value = line.split(":", 1)
        fields[key.strip()] = value.strip()
    if not fields.get("name") or not fields.get("description"):
        raise ConfigError(f"skill frontmatter must contain name and description: {skill_file}")
    return fields["name"].strip("\"'")


def iter_source_dir(source_dir: Path) -> list[Path]:
    if is_link_or_reparse(source_dir) or not source_dir.is_dir():
        raise ConfigError(f"skill directory is missing or unsafe: {source_dir}")
    ensure_contained(source_dir, PACKAGE_ROOT, "Skill source")
    files: list[Path] = []
    for path in sorted(source_dir.rglob("*")):
        if is_link_or_reparse(path):
            raise ConfigError(
                "source link or reparse point is not allowed: "
                + path.relative_to(PACKAGE_ROOT).as_posix()
            )
        ensure_contained(path, source_dir, "Skill source entry")
        if path.is_file():
            files.append(path)
        elif not path.is_dir():
            raise ConfigError(f"unsupported source entry: {path}")
    return files


def add_file(
    planned: list[PlannedFile],
    seen_targets: set[str],
    source_value: str,
    target_value: str,
) -> None:
    source = ensure_source(source_value)
    target_rel = str(safe_rel(target_value, "target path"))
    if target_rel in seen_targets:
        raise ConfigError(f"duplicate target in manifest: {target_rel}")
    seen_targets.add(target_rel)
    planned.append(
        PlannedFile(
            source=source,
            source_rel=source.relative_to(PACKAGE_ROOT).as_posix(),
            target_rel=target_rel,
            sha256=sha256_file(source),
            mode=stat.S_IMODE(source.stat().st_mode),
        )
    )


def build_plan(
    manifest: dict[str, Any],
    runtime_name: str,
    profile_name: str,
    hooks_enabled: bool,
) -> list[PlannedFile]:
    runtimes = manifest["runtimes"]
    profiles = manifest["profiles"]
    if runtime_name not in runtimes:
        raise ConfigError(f"unknown runtime: {runtime_name}")
    if profile_name not in profiles:
        raise ConfigError(f"unknown profile: {profile_name}")

    runtime = runtimes[runtime_name]
    profile = profiles[profile_name]
    planned: list[PlannedFile] = []
    seen_targets: set[str] = set()

    rule = runtime["rule"]
    add_file(planned, seen_targets, rule["source"], rule["target"])
    for item in manifest["common_files"]:
        add_file(planned, seen_targets, item["source"], item["target"])

    skills_root = safe_rel(runtime["skills_root"], "skills_root")
    seen_skills: set[str] = set()
    for pack_name in profile["skill_packs"]:
        if pack_name not in manifest["skill_packs"]:
            raise ConfigError(f"profile references unknown skill pack: {pack_name}")
        for skill_name in manifest["skill_packs"][pack_name]:
            if skill_name in seen_skills:
                raise ConfigError(f"duplicate skill in profile: {skill_name}")
            seen_skills.add(skill_name)
            source_dir = PACKAGE_ROOT / "packs" / pack_name / "skills" / skill_name
            entry_name = parse_skill_name(source_dir / "SKILL.md")
            if entry_name != skill_name:
                raise ConfigError(
                    f"skill folder/name mismatch: {skill_name!r} != {entry_name!r}"
                )
            for source in iter_source_dir(source_dir):
                subpath = source.relative_to(source_dir)
                target = skills_root / skill_name / PurePosixPath(subpath.as_posix())
                add_file(
                    planned,
                    seen_targets,
                    source.relative_to(PACKAGE_ROOT).as_posix(),
                    str(target),
                )

    if hooks_enabled and profile.get("include_hooks", False):
        hooks_by_profile = runtime.get("hooks_by_profile", {})
        if profile_name not in hooks_by_profile:
            raise ConfigError(
                f"runtime has no Hook adapter for profile: {runtime_name}/{profile_name}"
            )
        for item in hooks_by_profile[profile_name]:
            add_file(planned, seen_targets, item["source"], item["target"])

    return sorted(planned, key=lambda item: item.target_rel)


def validate_skill_pack(manifest: dict[str, Any], pack_name: str) -> int:
    names = manifest["skill_packs"].get(pack_name)
    if not isinstance(names, list) or not names:
        raise ConfigError(f"invalid or empty skill pack: {pack_name}")
    if len(names) != len(set(names)):
        raise ConfigError(f"duplicate Skill name in pack: {pack_name}")
    skills_root = PACKAGE_ROOT / "packs" / pack_name / "skills"
    if is_link_or_reparse(skills_root) or not skills_root.is_dir():
        raise ConfigError(f"skill pack directory is missing or unsafe: {pack_name}")
    actual = {
        child.name
        for child in skills_root.iterdir()
        if child.is_dir() and not is_link_or_reparse(child)
    }
    expected = set(names)
    if actual != expected:
        missing = sorted(expected - actual)
        extra = sorted(actual - expected)
        raise ConfigError(
            f"skill pack contents differ from manifest: {pack_name} "
            f"missing={missing} extra={extra}"
        )
    files = 0
    for name in names:
        source_dir = skills_root / name
        if parse_skill_name(source_dir / "SKILL.md") != name:
            raise ConfigError(f"skill folder/name mismatch in pack: {pack_name}/{name}")
        files += len(iter_source_dir(source_dir))
    return files


def validate_package(manifest: dict[str, Any]) -> dict[str, int]:
    counts = {"profiles": 0, "plans": 0, "files": 0, "catalog_skills": 0}
    if set(manifest["capability_requirements"]) != set(manifest["skill_packs"]):
        raise ConfigError("capability_requirements must cover every skill pack")
    for pack_name, names in manifest["skill_packs"].items():
        validate_skill_pack(manifest, pack_name)
        counts["catalog_skills"] += len(names)
        requirements = manifest["capability_requirements"][pack_name]
        if not isinstance(requirements, list):
            raise ConfigError(f"invalid capability requirements: {pack_name}")
        seen_requirements: set[str] = set()
        for requirement in requirements:
            command = requirement.get("command") if isinstance(requirement, dict) else None
            commands = requirement.get("commands") if isinstance(requirement, dict) else None
            environment = (
                requirement.get("environment") if isinstance(requirement, dict) else None
            )
            connection = (
                requirement.get("connection") if isinstance(requirement, dict) else None
            )
            label = requirement.get("label") if isinstance(requirement, dict) else None
            valid_command = isinstance(command, str) and bool(command)
            valid_alternatives = (
                isinstance(commands, list)
                and len(commands) >= 2
                and all(isinstance(item, str) and item for item in commands)
                and len(commands) == len(set(commands))
            )
            valid_environment = (
                isinstance(environment, str)
                and re.fullmatch(r"[A-Z][A-Z0-9_]{1,127}", environment) is not None
            )
            valid_connection = (
                isinstance(connection, str)
                and re.fullmatch(r"[a-z0-9][a-z0-9_-]{1,127}", connection) is not None
                and isinstance(label, str)
                and bool(label.strip())
            )
            valid_keys = set(requirement) if isinstance(requirement, dict) else set()
            if (
                not isinstance(requirement, dict)
                or valid_keys not in (
                    {"command", "required", "used_by"},
                    {"commands", "required", "used_by"},
                    {"environment", "required", "used_by"},
                    {"connection", "label", "required", "used_by"},
                )
                or sum(
                    (
                        valid_command,
                        valid_alternatives,
                        valid_environment,
                        valid_connection,
                    )
                )
                != 1
                or not isinstance(requirement["required"], bool)
                or not isinstance(requirement["used_by"], list)
                or not requirement["used_by"]
                or not all(name in names for name in requirement["used_by"])
            ):
                raise ConfigError(f"invalid capability requirement: {pack_name}")
            if valid_command:
                requirement_key = f"command:{command}"
            elif valid_alternatives:
                requirement_key = "commands:" + "|".join(commands)
            elif valid_environment:
                requirement_key = f"environment:{environment}"
            else:
                requirement_key = f"connection:{connection}"
            if requirement_key in seen_requirements:
                raise ConfigError(f"duplicate capability requirement: {pack_name}")
            seen_requirements.add(requirement_key)
    for profile_name, profile in manifest["profiles"].items():
        if (
            not isinstance(profile, dict)
            or not isinstance(profile.get("skill_packs"), list)
            or not isinstance(profile.get("include_hooks"), bool)
            or not isinstance(profile.get("hook_messages"), list)
            or not profile.get("hook_messages")
        ):
            raise ConfigError(f"invalid profile: {profile_name}")
        for message_path in profile["hook_messages"]:
            ensure_source(message_path)
        notices = profile.get("notices", [])
        if (
            not isinstance(notices, list)
            or not all(isinstance(notice, str) and notice.strip() for notice in notices)
        ):
            raise ConfigError(f"invalid profile notices: {profile_name}")
        for runtime_name in manifest["runtimes"]:
            for hooks_enabled in (False, True):
                plan = build_plan(manifest, runtime_name, profile_name, hooks_enabled)
                counts["plans"] += 1
                counts["files"] += len(plan)
        counts["profiles"] += 1
    return counts


def read_state(root: Path) -> dict[str, Any] | None:
    path = target_path(root, str(STATE_REL))
    if not path.exists():
        return None
    if not path.is_file():
        raise ConfigError(f"install state is not a regular file: {path}")
    try:
        state = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ConfigError(f"invalid install state: {exc}") from exc
    validate_state_object(state)
    return state


def re_full_hash(value: Any) -> bool:
    return (
        isinstance(value, str)
        and len(value) == 64
        and all(character in "0123456789abcdef" for character in value)
    )


def validate_state_object(state: dict[str, Any]) -> None:
    if state.get("schema_version") != 1 or not isinstance(state.get("files"), list):
        raise ConfigError("unsupported or malformed install state")
    if state.get("status") not in ("installed", "uninstalled"):
        raise ConfigError("install state has an invalid status")
    if state.get("status") == "installed":
        if not isinstance(state.get("runtime"), str):
            raise ConfigError("install state has an invalid runtime")
        if not isinstance(state.get("profile"), str):
            raise ConfigError("install state has an invalid profile")
        if not isinstance(state.get("hooks_enabled"), bool):
            raise ConfigError("install state has an invalid hook setting")
    seen: set[str] = set()
    for record in state["files"]:
        if not isinstance(record, dict):
            raise ConfigError("install state contains a non-object file record")
        required = {"target", "source", "installed_sha256", "owned"}
        if not required.issubset(record):
            raise ConfigError("install state contains an incomplete file record")
        target = str(safe_rel(record["target"], "state target"))
        safe_rel(record["source"], "state source")
        if target in seen:
            raise ConfigError(f"install state contains a duplicate target: {target}")
        seen.add(target)
        if not re_full_hash(record["installed_sha256"]):
            raise ConfigError(f"install state contains an invalid hash: {target}")
        if not isinstance(record["owned"], bool):
            raise ConfigError(f"install state contains invalid ownership: {target}")


def validate_state_against_plan(
    state: dict[str, Any], plan: list[PlannedFile]
) -> None:
    desired = {item.target_rel: item for item in plan}
    for record in state["files"]:
        item = desired.get(record["target"])
        if item is None:
            raise ConfigError(
                "install state contains a target outside the current package plan: "
                + record["target"]
            )
        if record["source"] != item.source_rel:
            raise ConfigError(
                "install state source/target mapping does not match the package plan: "
                + record["target"]
            )


def atomic_write(path: Path, data: bytes, mode: int = 0o644) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if is_link_or_reparse(path.parent):
        raise ConfigError(f"refusing to write through link or reparse point: {path.parent}")
    fd, temp_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    temp_path = Path(temp_name)
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.chmod(temp_path, mode)
        os.replace(temp_path, path)
    finally:
        if temp_path.exists():
            temp_path.unlink()


def write_state(root: Path, state: dict[str, Any]) -> None:
    data = (json.dumps(state, indent=2, sort_keys=True) + "\n").encode("utf-8")
    atomic_write(target_path(root, str(STATE_REL)), data)


def print_plan(title: str, actions: list[tuple[str, str]], apply: bool) -> None:
    print(title)
    for action, rel in actions:
        print(f"  {action:10} {rel}")
    counts: dict[str, int] = {}
    for action, _ in actions:
        counts[action] = counts.get(action, 0) + 1
    summary = ", ".join(f"{key}={counts[key]}" for key in sorted(counts)) or "no files"
    print(f"Summary: {summary}")
    print("Mode: apply" if apply else "Mode: dry-run (no files changed)")


def print_profile_notices(manifest: dict[str, Any], profile_name: str) -> None:
    for notice in manifest["profiles"][profile_name].get("notices", []):
        print(f"Notice: {notice}")


def state_record(item: PlannedFile, owned: bool) -> dict[str, Any]:
    return {
        "target": item.target_rel,
        "source": item.source_rel,
        "installed_sha256": item.sha256,
        "owned": owned,
    }


def apply_changes(
    root: Path,
    writes: list[PlannedFile],
    new_state: dict[str, Any],
) -> None:
    created: list[Path] = []
    replaced: list[tuple[Path, bytes, int]] = []
    try:
        for item in writes:
            destination = target_path(root, item.target_rel)
            if destination.exists():
                if not destination.is_file():
                    raise ConfigError(f"target is not a regular file: {item.target_rel}")
                replaced.append(
                    (
                        destination,
                        destination.read_bytes(),
                        stat.S_IMODE(destination.stat().st_mode),
                    )
                )
            else:
                created.append(destination)
            source_data = item.source.read_bytes()
            if sha256_bytes(source_data) != item.sha256:
                raise ConfigError(f"package source changed during apply: {item.source_rel}")
            atomic_write(destination, source_data, item.mode)
        write_state(root, new_state)
    except Exception:
        for path, data, mode in reversed(replaced):
            atomic_write(path, data, mode)
        for path in reversed(created):
            if path.exists() and path.is_file() and not is_link_or_reparse(path):
                path.unlink()
        raise


def command_install(args: argparse.Namespace, manifest: dict[str, Any]) -> int:
    root = prepare_target(args.target)
    hooks_enabled = (
        not args.without_hooks
        and bool(manifest["profiles"][args.profile].get("include_hooks", False))
    )
    plan = build_plan(manifest, args.runtime, args.profile, hooks_enabled)
    print_profile_notices(manifest, args.profile)
    existing_state = read_state(root)
    actions: list[tuple[str, str]] = []
    writes: list[PlannedFile] = []
    records: list[dict[str, Any]] = []
    conflicts: list[str] = []

    if existing_state and existing_state.get("status") == "installed":
        expected = (
            existing_state.get("runtime"),
            existing_state.get("profile"),
            existing_state.get("hooks_enabled"),
        )
        requested = (args.runtime, args.profile, hooks_enabled)
        if expected != requested:
            raise ConfigError(
                "a different installation already exists; uninstall it before changing "
                "runtime, profile, or hook choice"
            )
        old = {item["target"]: item for item in existing_state["files"]}
        if set(old) != {item.target_rel for item in plan}:
            raise ConfigError("package contents changed; use update instead of install")
        for item in plan:
            destination = target_path(root, item.target_rel)
            record = old[item.target_rel]
            if not destination.exists():
                conflicts.append(f"missing installed file: {item.target_rel}")
                actions.append(("conflict", item.target_rel))
            elif not destination.is_file() or sha256_file(destination) != item.sha256:
                conflicts.append(f"installed file differs: {item.target_rel}")
                actions.append(("conflict", item.target_rel))
            else:
                action = "current" if record.get("owned") else "adopted"
                actions.append((action, item.target_rel))
        print_plan("Install plan", actions, args.apply)
        if conflicts:
            raise ConfigError("; ".join(conflicts))
        print("Already installed; no changes required.")
        return 0

    if existing_state and existing_state.get("status") != "uninstalled":
        raise ConfigError("an uninstall tombstone or unsupported state already exists")

    for item in plan:
        destination = target_path(root, item.target_rel)
        if not destination.exists():
            actions.append(("create", item.target_rel))
            writes.append(item)
            records.append(state_record(item, True))
        elif destination.is_file() and sha256_file(destination) == item.sha256:
            actions.append(("adopted", item.target_rel))
            records.append(state_record(item, False))
        else:
            actions.append(("conflict", item.target_rel))
            conflicts.append(item.target_rel)

    print_plan("Install plan", actions, args.apply)
    if conflicts:
        raise ConfigError(
            "conflicting targets stop the whole install: " + ", ".join(conflicts)
        )
    if args.apply:
        new_state = {
            "schema_version": 1,
            "status": "installed",
            "release": manifest["release"],
            "runtime": args.runtime,
            "profile": args.profile,
            "hooks_enabled": hooks_enabled,
            "files": records,
        }
        apply_changes(root, writes, new_state)
        print("Install applied. Run doctor next.")
    return 0


def command_update(args: argparse.Namespace, manifest: dict[str, Any]) -> int:
    root = prepare_target(args.target)
    state = read_state(root)
    if not state or state.get("status") != "installed":
        raise ConfigError("no active installation found")
    runtime = state["runtime"]
    profile = state["profile"]
    hooks_enabled = bool(state["hooks_enabled"])
    plan = build_plan(manifest, runtime, profile, hooks_enabled)
    print_profile_notices(manifest, profile)
    old = {item["target"]: item for item in state["files"]}
    desired = {item.target_rel: item for item in plan}
    actions: list[tuple[str, str]] = []
    writes: list[PlannedFile] = []
    records: list[dict[str, Any]] = []
    conflicts: list[str] = []

    for item in plan:
        destination = target_path(root, item.target_rel)
        record = old.get(item.target_rel)
        if record is None:
            if not destination.exists():
                actions.append(("create", item.target_rel))
                writes.append(item)
                records.append(state_record(item, True))
            elif destination.is_file() and sha256_file(destination) == item.sha256:
                actions.append(("adopted", item.target_rel))
                records.append(state_record(item, False))
            else:
                actions.append(("conflict", item.target_rel))
                conflicts.append(item.target_rel)
            continue

        if not destination.exists() or not destination.is_file():
            actions.append(("conflict", item.target_rel))
            conflicts.append(item.target_rel)
            continue
        current_hash = sha256_file(destination)
        old_hash = record["installed_sha256"]
        if record.get("owned"):
            if current_hash != old_hash:
                actions.append(("drifted", item.target_rel))
                conflicts.append(item.target_rel)
            elif item.sha256 != old_hash:
                actions.append(("update", item.target_rel))
                writes.append(item)
                records.append(state_record(item, True))
            else:
                actions.append(("current", item.target_rel))
                records.append(state_record(item, True))
        else:
            if current_hash == item.sha256:
                actions.append(("adopted", item.target_rel))
                records.append(state_record(item, False))
            else:
                actions.append(("conflict", item.target_rel))
                conflicts.append(item.target_rel)

    for rel, record in old.items():
        if rel not in desired:
            actions.append(("orphaned", rel))
            records.append(record)

    print_plan("Update plan", actions, args.apply)
    if conflicts:
        raise ConfigError(
            "drift or collision stops the whole update: " + ", ".join(conflicts)
        )
    if args.apply:
        new_state = {
            **state,
            "release": manifest["release"],
            "files": records,
        }
        apply_changes(root, writes, new_state)
        print("Update applied. Run doctor next.")
    return 0


def doctor_counts(root: Path, state: dict[str, Any], plan: list[PlannedFile]) -> dict[str, int]:
    desired = {item.target_rel: item for item in plan}
    recorded = {item["target"]: item for item in state["files"]}
    counts = {
        "current": 0,
        "adopted": 0,
        "outdated": 0,
        "drifted": 0,
        "missing": 0,
        "orphaned": 0,
    }
    for rel, record in recorded.items():
        item = desired.get(rel)
        if item is None:
            counts["orphaned"] += 1
            continue
        destination = target_path(root, rel)
        if not destination.exists() or not destination.is_file():
            counts["missing"] += 1
            continue
        current_hash = sha256_file(destination)
        if current_hash != record["installed_sha256"]:
            counts["drifted"] += 1
        elif item.sha256 != record["installed_sha256"]:
            counts["outdated"] += 1
        elif record.get("owned"):
            counts["current"] += 1
        else:
            counts["adopted"] += 1
    for rel in desired.keys() - recorded.keys():
        counts["missing"] += 1
    return counts


def command_doctor(args: argparse.Namespace, manifest: dict[str, Any]) -> int:
    root = prepare_target(args.target)
    state = read_state(root)
    if not state or state.get("status") != "installed":
        if args.json:
            print(json.dumps({"status": "not_installed"}, sort_keys=True))
        else:
            print("Status: not installed")
            print("No runtime or Hook smoke was performed.")
        return 1
    plan = build_plan(
        manifest,
        state["runtime"],
        state["profile"],
        bool(state["hooks_enabled"]),
    )
    counts = doctor_counts(root, state, plan)
    runtime_commands = {
        "codex": "codex",
        "cursor": "cursor",
        "claude-code": "claude",
    }
    runtime_command = runtime_commands[state["runtime"]]
    runtime_cli = {
        "command": runtime_command,
        "status": "available" if shutil.which(runtime_command) else "not_on_path",
        "required": False,
    }
    hooks_enabled = bool(state["hooks_enabled"])
    if not hooks_enabled:
        hook_capability = {
            "status": "disabled",
            "interpreter": None,
            "required": False,
        }
    elif os.name == "nt":
        hook_capability = {
            "status": "unsupported_native_windows",
            "interpreter": None,
            "required": True,
        }
    else:
        interpreter = shutil.which("python3")
        hook_capability = {
            "status": "ready" if interpreter else "missing_interpreter",
            "interpreter": interpreter,
            "required": True,
        }
    dependency_capabilities = []
    environment_capabilities = []
    connection_capabilities = []
    for pack_name in manifest["profiles"][state["profile"]]["skill_packs"]:
        for requirement in manifest["capability_requirements"].get(pack_name, []):
            if "connection" in requirement:
                connection_capabilities.append(
                    {
                        "connection": requirement["connection"],
                        "label": requirement["label"],
                        "status": "not_verified",
                        "required": bool(requirement["required"]),
                        "used_by": requirement["used_by"],
                    }
                )
                continue
            if "environment" in requirement:
                environment = requirement["environment"]
                environment_capabilities.append(
                    {
                        "environment": environment,
                        "status": "present" if environment in os.environ else "missing",
                        "required": bool(requirement["required"]),
                        "used_by": requirement["used_by"],
                    }
                )
                continue
            candidates = (
                [requirement["command"]]
                if "command" in requirement
                else requirement["commands"]
            )
            resolved = next(
                (command for command in candidates if shutil.which(command)),
                None,
            )
            dependency_capabilities.append(
                {
                    "command": "|".join(candidates),
                    "resolved_command": resolved,
                    "status": "available" if resolved else "missing",
                    "required": bool(requirement["required"]),
                    "used_by": requirement["used_by"],
                }
            )
    capabilities = {
        "runtime_cli": runtime_cli,
        "hook": hook_capability,
        "skill_commands": dependency_capabilities,
        "skill_environment": environment_capabilities,
        "skill_connections": connection_capabilities,
    }
    result = {
        "status": "installed",
        "runtime": state["runtime"],
        "profile": state["profile"],
        "release": state["release"],
        "hooks_enabled": hooks_enabled,
        "files": counts,
        "capabilities": capabilities,
        "live_runtime_smoke": "not_performed",
    }
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(
            f"Status: runtime={state['runtime']} profile={state['profile']} "
            f"release={state['release']} hooks={hooks_enabled}"
        )
        print("Files: " + " ".join(f"{key}={value}" for key, value in counts.items()))
        print(
            f"Capability runtime-cli: {runtime_cli['status']} "
            f"({runtime_cli['command']}, informational)"
        )
        print(f"Capability hook: {hook_capability['status']}")
        for capability in dependency_capabilities:
            level = "required" if capability["required"] else "optional"
            print(
                f"Capability skill-command: {capability['command']}="
                f"{capability['status']} ({level}; "
                f"used by {','.join(capability['used_by'])})"
            )
        for capability in environment_capabilities:
            level = "required" if capability["required"] else "optional"
            print(
                f"Capability skill-environment: {capability['environment']}="
                f"{capability['status']} ({level}; "
                f"used by {','.join(capability['used_by'])})"
            )
        for capability in connection_capabilities:
            level = "required" if capability["required"] else "optional"
            print(
                f"Capability skill-connection: {capability['connection']}="
                f"{capability['status']} ({level}; {capability['label']}; "
                f"used by {','.join(capability['used_by'])})"
            )
        print("Live runtime smoke: not performed")
    unhealthy = counts["outdated"] + counts["drifted"] + counts["missing"] + counts["orphaned"]
    if hooks_enabled and hook_capability["status"] != "ready":
        unhealthy += 1
    unhealthy += sum(
        1
        for capability in dependency_capabilities
        if capability["required"] and capability["status"] != "available"
    )
    return 1 if unhealthy else 0


def command_uninstall(args: argparse.Namespace, manifest: dict[str, Any]) -> int:
    root = prepare_target(args.target)
    state = read_state(root)
    if not state or state.get("status") != "installed":
        raise ConfigError("no active installation found")
    plan = build_plan(
        manifest,
        state["runtime"],
        state["profile"],
        bool(state["hooks_enabled"]),
    )
    validate_state_against_plan(state, plan)
    actions: list[tuple[str, str]] = []
    removable: list[tuple[str, Path, str]] = []
    for record in state["files"]:
        rel = record["target"]
        destination = target_path(root, rel)
        if not record.get("owned"):
            actions.append(("preserve", rel))
        elif not destination.exists():
            actions.append(("missing", rel))
        elif destination.is_file() and sha256_file(destination) == record["installed_sha256"]:
            actions.append(("remove", rel))
            removable.append((rel, destination, record["installed_sha256"]))
        else:
            actions.append(("drifted", rel))

    print_plan("Uninstall plan", actions, args.apply)
    if not args.apply:
        return 0
    if not args.confirm_uninstall:
        raise ConfigError("uninstall apply requires --confirm-uninstall")

    recovery_rel = PurePosixPath(
        ".agent-config-kit/recovery/"
        + time.strftime("%Y%m%d-%H%M%S")
        + "-"
        + uuid.uuid4().hex[:8]
    )
    recovery_root = target_path(root, str(recovery_rel))
    recovery_root.mkdir(parents=True, exist_ok=False)
    removed: list[tuple[Path, Path]] = []
    try:
        for rel, source, expected_hash in removable:
            if sha256_file(source) != expected_hash:
                raise ConfigError(f"file changed during uninstall preflight: {rel}")
            backup = recovery_root.joinpath(*PurePosixPath(rel).parts)
            backup.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, backup)
        state_path = target_path(root, str(STATE_REL))
        shutil.copy2(state_path, recovery_root / "install-state.json")
        for rel, source, expected_hash in removable:
            if sha256_file(source) != expected_hash:
                raise ConfigError(f"file changed during uninstall backup: {rel}")
            backup = recovery_root.joinpath(*PurePosixPath(rel).parts)
            source.unlink()
            removed.append((source, backup))
        tombstone = {
            "schema_version": 1,
            "status": "uninstalled",
            "release": state.get("release"),
            "runtime": state.get("runtime"),
            "profile": state.get("profile"),
            "hooks_enabled": state.get("hooks_enabled"),
            "recovery": str(recovery_rel),
            "files": [],
        }
        write_state(root, tombstone)
    except Exception:
        for destination, backup in reversed(removed):
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(backup, destination)
        raise
    print(f"Uninstall applied. Recovery: {recovery_rel}")
    return 0


def command_restore(args: argparse.Namespace, manifest: dict[str, Any]) -> int:
    root = prepare_target(args.target)
    tombstone = read_state(root)
    if not tombstone or tombstone.get("status") != "uninstalled":
        raise ConfigError("no recoverable uninstall found")
    recovery_rel = safe_rel(tombstone.get("recovery"), "recovery path")
    recovery_root = target_path(root, str(recovery_rel))
    backup_state_path = recovery_root / "install-state.json"
    if is_link_or_reparse(backup_state_path) or not backup_state_path.is_file():
        raise ConfigError("recovery state is missing or unsafe")
    try:
        backup_state = json.loads(backup_state_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ConfigError(f"invalid recovery state: {exc}") from exc
    if backup_state.get("schema_version") != 1 or backup_state.get("status") != "installed":
        raise ConfigError("recovery state is not an active installation snapshot")

    validate_state_object(backup_state)
    plan = build_plan(
        manifest,
        backup_state["runtime"],
        backup_state["profile"],
        bool(backup_state["hooks_enabled"]),
    )
    validate_state_against_plan(backup_state, plan)

    actions: list[tuple[str, str]] = []
    writes: list[PlannedFile] = []
    conflicts: list[str] = []
    for record in backup_state["files"]:
        rel = record["target"]
        backup = target_path(recovery_root, rel)
        destination = target_path(root, rel)
        if backup.is_file():
            backup_hash = sha256_file(backup)
            if backup_hash != record["installed_sha256"]:
                actions.append(("conflict", rel))
                conflicts.append(rel)
            elif not destination.exists():
                actions.append(("restore", rel))
                writes.append(
                    PlannedFile(
                        source=backup,
                        source_rel=f"{recovery_rel}/{rel}",
                        target_rel=rel,
                        sha256=backup_hash,
                        mode=stat.S_IMODE(backup.stat().st_mode),
                    )
                )
            elif destination.is_file() and sha256_file(destination) == backup_hash:
                actions.append(("current", rel))
            else:
                actions.append(("conflict", rel))
                conflicts.append(rel)
        elif destination.exists():
            actions.append(("preserved", rel))
        else:
            actions.append(("missing", rel))
            conflicts.append(rel)

    print_plan("Restore plan", actions, args.apply)
    if conflicts:
        raise ConfigError(
            "restore is incomplete or collides with current files: "
            + ", ".join(conflicts)
        )
    if args.apply:
        apply_changes(root, writes, backup_state)
        print("Restore applied. Run doctor next.")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("verify-package", help="validate manifest and package sources")

    install = subparsers.add_parser("install", help="preview or apply installation")
    install.add_argument("--runtime", required=True, choices=("codex", "cursor", "claude-code"))
    install.add_argument(
        "--profile",
        default="daily-work",
        choices=("daily-work", "knowledge-vault", "full"),
    )
    install.add_argument("--target", required=True)
    install.add_argument("--without-hooks", action="store_true")
    install.add_argument("--apply", action="store_true")

    update = subparsers.add_parser("update", help="preview or apply a same-profile update")
    update.add_argument("--target", required=True)
    update.add_argument("--apply", action="store_true")

    doctor = subparsers.add_parser("doctor", help="diagnose an installed target")
    doctor.add_argument("--target", required=True)
    doctor.add_argument("--json", action="store_true")

    uninstall = subparsers.add_parser("uninstall", help="preview or apply recoverable uninstall")
    uninstall.add_argument("--target", required=True)
    uninstall.add_argument("--apply", action="store_true")
    uninstall.add_argument("--confirm-uninstall", action="store_true")

    restore = subparsers.add_parser("restore", help="preview or restore the last uninstall")
    restore.add_argument("--target", required=True)
    restore.add_argument("--apply", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        manifest = load_manifest()
        counts = validate_package(manifest)
        if args.command == "verify-package":
            print(
                f"Package OK: release={manifest['release']} profiles={counts['profiles']} "
                f"catalog_skills={counts['catalog_skills']} "
                f"plans={counts['plans']} planned_files={counts['files']}"
            )
            return 0
        if args.command == "install":
            return command_install(args, manifest)
        if args.command == "update":
            return command_update(args, manifest)
        if args.command == "doctor":
            return command_doctor(args, manifest)
        if args.command == "uninstall":
            return command_uninstall(args, manifest)
        if args.command == "restore":
            return command_restore(args, manifest)
        raise ConfigError(f"unsupported command: {args.command}")
    except (ConfigError, KeyError, OSError, TypeError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
