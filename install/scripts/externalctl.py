#!/usr/bin/env python3
"""Fetch hash-pinned official Skills without redistributing their contents."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request
import uuid
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any, Callable

import configctl


PACKAGE_ROOT = Path(__file__).resolve().parents[2]
CATALOG_PATH = PACKAGE_ROOT / "catalog" / "external_skills.json"
STATE_REL = PurePosixPath(".agent-config-kit/external-state.json")
MAX_SKILL_BYTES = 1024 * 1024
NAME_PATTERN = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]*")
HASH_PATTERN = re.compile(r"[0-9a-f]{64}")
WINDOWS_RESERVED_NAMES = {
    "AUX",
    "CON",
    "NUL",
    "PRN",
    *(f"COM{index}" for index in range(1, 10)),
    *(f"LPT{index}" for index in range(1, 10)),
}


class RejectRedirects(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, request, file_pointer, code, message, headers, new_url):
        return None


HTTPS_OPENER = urllib.request.build_opener(RejectRedirects())


def is_safe_name(value: Any) -> bool:
    return (
        isinstance(value, str)
        and NAME_PATTERN.fullmatch(value) is not None
        and not value.endswith(".")
        and value.split(".", 1)[0].upper() not in WINDOWS_RESERVED_NAMES
    )


@dataclass(frozen=True)
class ExternalSkill:
    name: str
    url: str
    sha256: str
    target_rel: str
    data: bytes


def load_json(path: Path) -> dict[str, Any]:
    if configctl.is_link_or_reparse(path) or not path.is_file():
        raise configctl.ConfigError(f"catalog is missing or unsafe: {path.name}")
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise configctl.ConfigError(f"invalid {path.name}: {exc}") from exc
    if not isinstance(payload, dict):
        raise configctl.ConfigError(f"{path.name} must contain an object")
    return payload


def validate_catalog(catalog: dict[str, Any]) -> dict[str, dict[str, Any]]:
    if catalog.get("schema_version") != 1 or not isinstance(catalog.get("packs"), dict):
        raise configctl.ConfigError("unsupported external Skill catalog")
    packs = catalog["packs"]
    if not packs:
        raise configctl.ConfigError("external Skill catalog has no packs")
    seen_names: set[str] = set()
    for pack_name, pack in packs.items():
        if not is_safe_name(pack_name):
            raise configctl.ConfigError(f"unsafe external pack name: {pack_name!r}")
        if (
            not isinstance(pack, dict)
            or set(pack) != {"description", "source_host", "skills"}
            or not isinstance(pack["description"], str)
            or not pack["description"]
            or not isinstance(pack["source_host"], str)
            or not pack["source_host"]
            or not isinstance(pack["skills"], list)
            or not pack["skills"]
        ):
            raise configctl.ConfigError(f"invalid external pack: {pack_name}")
        host = pack["source_host"]
        for entry in pack["skills"]:
            if (
                not isinstance(entry, dict)
                or set(entry)
                not in (
                    {"name", "sha256", "url"},
                    {"name", "previous_sha256", "sha256", "url"},
                )
            ):
                raise configctl.ConfigError(f"invalid external Skill entry: {pack_name}")
            name = entry["name"]
            digest = entry["sha256"]
            url = entry["url"]
            if not is_safe_name(name):
                raise configctl.ConfigError(f"unsafe external Skill name: {name!r}")
            folded_name = name.casefold()
            if folded_name in seen_names:
                raise configctl.ConfigError(f"duplicate external Skill name: {name}")
            seen_names.add(folded_name)
            if not isinstance(digest, str) or HASH_PATTERN.fullmatch(digest) is None:
                raise configctl.ConfigError(f"invalid external Skill hash: {name}")
            previous = entry.get("previous_sha256", [])
            if (
                not isinstance(previous, list)
                or len(previous) != len(set(previous))
                or digest in previous
                or not all(
                    isinstance(value, str) and HASH_PATTERN.fullmatch(value) is not None
                    for value in previous
                )
            ):
                raise configctl.ConfigError(
                    f"invalid external Skill hash history: {name}"
                )
            if not isinstance(url, str):
                raise configctl.ConfigError(f"invalid external Skill URL: {name}")
            parsed = urllib.parse.urlsplit(url)
            expected_path = f"/.well-known/skills/{name}/SKILL.md"
            if (
                parsed.scheme != "https"
                or parsed.hostname != host
                or parsed.port is not None
                or parsed.username is not None
                or parsed.password is not None
                or parsed.path != expected_path
                or parsed.query
                or parsed.fragment
            ):
                raise configctl.ConfigError(f"unsafe external Skill URL: {name}")
    return packs


def parse_skill_name(data: bytes) -> str:
    try:
        lines = data.decode("utf-8").splitlines()
    except UnicodeDecodeError as exc:
        raise configctl.ConfigError("external SKILL.md is not UTF-8") from exc
    if not lines or lines[0].strip() != "---":
        raise configctl.ConfigError("external SKILL.md has no YAML frontmatter")
    closing = next(
        (index for index, line in enumerate(lines[1:], start=1) if line.strip() == "---"),
        None,
    )
    if closing is None:
        raise configctl.ConfigError("external SKILL.md frontmatter is not closed")
    names = [
        line
        for line in lines[1:closing]
        if re.match(r"^\s*name\s*:", line) is not None
    ]
    if len(names) != 1:
        raise configctl.ConfigError("external SKILL.md must declare one plain name")
    match = re.fullmatch(
        r"\s*name\s*:\s*([A-Za-z0-9][A-Za-z0-9._-]*)\s*",
        names[0],
    )
    if match is None:
        raise configctl.ConfigError("external SKILL.md name is not a safe plain value")
    return match.group(1)


def fetch_entry(entry: dict[str, str], expected_host: str) -> bytes:
    request = urllib.request.Request(
        entry["url"],
        headers={"User-Agent": "agent-config-kit-externalctl/0.1"},
    )
    with HTTPS_OPENER.open(request, timeout=20) as response:
        if getattr(response, "status", 200) != 200:
            raise configctl.ConfigError(
                f"external Skill returned HTTP {response.status}: {entry['name']}"
            )
        final = urllib.parse.urlsplit(response.geturl())
        original = urllib.parse.urlsplit(entry["url"])
        if (
            final.scheme != "https"
            or final.hostname != expected_host
            or final.port is not None
            or final.username is not None
            or final.password is not None
            or final.path != original.path
            or final.query
            or final.fragment
        ):
            raise configctl.ConfigError(
                f"external Skill redirected outside its approved endpoint: {entry['name']}"
            )
        data = response.read(MAX_SKILL_BYTES + 1)
    if len(data) > MAX_SKILL_BYTES:
        raise configctl.ConfigError(f"external Skill exceeds size limit: {entry['name']}")
    digest = hashlib.sha256(data).hexdigest()
    if digest != entry["sha256"]:
        raise configctl.ConfigError(
            f"external Skill changed upstream; review and repin before installing: {entry['name']}"
        )
    declared = parse_skill_name(data)
    if declared != entry["name"]:
        raise configctl.ConfigError(
            f"external Skill name differs: {entry['name']!r} != {declared!r}"
        )
    return data


def selected_entries(
    catalog: dict[str, Any],
    pack_names: list[str],
) -> list[tuple[str, dict[str, str]]]:
    packs = validate_catalog(catalog)
    if len(pack_names) != len(set(pack_names)):
        raise configctl.ConfigError("external pack was selected more than once")
    selected: list[tuple[str, dict[str, str]]] = []
    for pack_name in pack_names:
        if pack_name not in packs:
            raise configctl.ConfigError(f"unknown external pack: {pack_name}")
        selected.extend(
            (packs[pack_name]["source_host"], entry)
            for entry in packs[pack_name]["skills"]
        )
    return selected


def fetch_plan(
    manifest: dict[str, Any],
    catalog: dict[str, Any],
    runtime: str,
    pack_names: list[str],
    fetcher: Callable[[dict[str, str], str], bytes] | None = None,
) -> list[ExternalSkill]:
    if runtime not in manifest["runtimes"]:
        raise configctl.ConfigError(f"unknown runtime: {runtime}")
    skills_root = configctl.safe_rel(
        manifest["runtimes"][runtime]["skills_root"],
        "skills_root",
    )
    plan: list[ExternalSkill] = []
    active_fetcher = fetch_entry if fetcher is None else fetcher
    for host, entry in selected_entries(catalog, pack_names):
        name = entry["name"]
        plan.append(
            ExternalSkill(
                name=name,
                url=entry["url"],
                sha256=entry["sha256"],
                target_rel=str(skills_root / name / "SKILL.md"),
                data=active_fetcher(entry, host),
            )
        )
    return sorted(plan, key=lambda item: item.name)


def expected_state_files(
    manifest: dict[str, Any],
    catalog: dict[str, Any],
    runtime: str,
    pack_names: list[str],
) -> dict[str, dict[str, Any]]:
    if runtime not in manifest["runtimes"]:
        raise configctl.ConfigError("external state has an unknown runtime")
    skills_root = configctl.safe_rel(
        manifest["runtimes"][runtime]["skills_root"],
        "skills_root",
    )
    expected: dict[str, dict[str, Any]] = {}
    for _, entry in selected_entries(catalog, pack_names):
        name = entry["name"]
        expected[name] = {
            "name": name,
            "target": str(skills_root / name / "SKILL.md"),
            "url": entry["url"],
            "approved_sha256": {
                entry["sha256"],
                *entry.get("previous_sha256", []),
            },
        }
    return expected


def validate_state(
    state: dict[str, Any],
    manifest: dict[str, Any],
    catalog: dict[str, Any],
) -> None:
    if state.get("schema_version") != 1:
        raise configctl.ConfigError("unsupported external state")
    if state.get("status") == "uninstalled":
        if set(state) != {
            "schema_version",
            "status",
            "recovery",
            "previous",
        }:
            raise configctl.ConfigError("invalid external uninstall state")
        recovery = configctl.safe_rel(state["recovery"], "recovery path")
        if recovery.parts[:2] != (".agent-config-kit", "recovery") or len(recovery.parts) < 3:
            raise configctl.ConfigError("external recovery path is outside recovery root")
        if not isinstance(state["previous"], dict):
            raise configctl.ConfigError("external previous state is invalid")
        validate_state(state["previous"], manifest, catalog)
        if state["previous"].get("status") != "installed":
            raise configctl.ConfigError("external previous state is not installed")
        return
    if state.get("status") != "installed" or set(state) != {
        "schema_version",
        "status",
        "runtime",
        "packs",
        "files",
    }:
        raise configctl.ConfigError("unsupported external state")
    runtime = state["runtime"]
    packs = state["packs"]
    files = state["files"]
    if (
        not isinstance(runtime, str)
        or not isinstance(packs, list)
        or not packs
        or packs != sorted(packs)
        or len(packs) != len(set(packs))
        or not all(isinstance(pack, str) for pack in packs)
        or not isinstance(files, list)
    ):
        raise configctl.ConfigError("external installed state is invalid")
    expected = expected_state_files(manifest, catalog, runtime, packs)
    actual: dict[str, dict[str, Any]] = {}
    for record in files:
        if (
            not isinstance(record, dict)
            or set(record)
            != {
                "name",
                "target",
                "url",
                "installed_sha256",
            }
            or not isinstance(record.get("name"), str)
            or record["name"] in actual
        ):
            raise configctl.ConfigError("external file state is invalid")
        actual[record["name"]] = record
    if set(actual) != set(expected):
        raise configctl.ConfigError("external file state does not match selected packs")
    for name, approved in expected.items():
        record = actual[name]
        if any(
            record[key] != approved[key]
            for key in ("name", "target", "url")
        ) or record["installed_sha256"] not in approved["approved_sha256"]:
            raise configctl.ConfigError(
                f"external file state differs from approved Catalog: {name}"
            )


def read_state(
    root: Path,
    manifest: dict[str, Any],
    catalog: dict[str, Any],
) -> dict[str, Any] | None:
    path = configctl.target_path(root, str(STATE_REL))
    if not path.exists():
        return None
    if not path.is_file():
        raise configctl.ConfigError("external state is not a regular file")
    state = load_json(path)
    validate_state(state, manifest, catalog)
    return state


def write_state(root: Path, state: dict[str, Any]) -> None:
    data = (json.dumps(state, indent=2, sort_keys=True) + "\n").encode("utf-8")
    configctl.atomic_write(configctl.target_path(root, str(STATE_REL)), data)


def target_collision(root: Path, item: ExternalSkill) -> str | None:
    destination = configctl.target_path(root, item.target_rel)
    skill_dir = destination.parent
    if skill_dir.exists():
        return item.target_rel
    return item.target_rel if destination.exists() else None


def install_records(
    root: Path,
    plan: list[ExternalSkill],
) -> tuple[list[tuple[str, str]], list[ExternalSkill], list[dict[str, Any]]]:
    actions: list[tuple[str, str]] = []
    writes: list[ExternalSkill] = []
    records: list[dict[str, Any]] = []
    for item in plan:
        collision = target_collision(root, item)
        if collision:
            actions.append(("conflict", item.target_rel))
            continue
        actions.append(("create", item.target_rel))
        writes.append(item)
        records.append(
            {
                "name": item.name,
                "target": item.target_rel,
                "url": item.url,
                "installed_sha256": item.sha256,
            }
        )
    return actions, writes, records


def exclusive_write(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if configctl.is_link_or_reparse(path.parent):
        raise configctl.ConfigError(
            f"refusing to write through link or reparse point: {path.parent}"
        )
    try:
        descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)
    except FileExistsError as exc:
        raise configctl.ConfigError(
            f"external Skill target appeared after preview: {path}"
        ) from exc
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
    except BaseException:
        if path.exists() and path.is_file() and not configctl.is_link_or_reparse(path):
            path.unlink()
        raise


def move_file(source: Path, destination: Path) -> None:
    os.replace(source, destination)


def apply_install(
    root: Path,
    writes: list[ExternalSkill],
    state: dict[str, Any],
) -> None:
    created: list[Path] = []
    try:
        for item in writes:
            destination = configctl.target_path(root, item.target_rel)
            if hashlib.sha256(item.data).hexdigest() != item.sha256:
                raise configctl.ConfigError(
                    f"external Skill changed after verification: {item.name}"
                )
            exclusive_write(destination, item.data)
            created.append(destination)
        write_state(root, state)
    except Exception:
        for path in reversed(created):
            if path.exists() and path.is_file() and not configctl.is_link_or_reparse(path):
                path.unlink()
        raise


def command_install(args: argparse.Namespace, manifest: dict[str, Any], catalog: dict[str, Any]) -> int:
    root = configctl.prepare_target(args.target)
    existing = read_state(root, manifest, catalog)
    if existing and existing.get("status") == "installed":
        raise configctl.ConfigError(
            "external Skills are already installed; run external doctor first"
        )
    plan = fetch_plan(manifest, catalog, args.runtime, args.pack)
    actions, writes, records = install_records(root, plan)
    configctl.print_plan("External Skill install plan", actions, args.apply)
    conflicts = [target for action, target in actions if action == "conflict"]
    if conflicts:
        raise configctl.ConfigError(
            "conflicting targets stop the whole external install: " + ", ".join(conflicts)
        )
    if args.apply:
        state = {
            "schema_version": 1,
            "status": "installed",
            "runtime": args.runtime,
            "packs": sorted(args.pack),
            "files": records,
        }
        apply_install(root, writes, state)
        print("External Skill install applied. Run external doctor next.")
    return 0


def command_doctor(
    args: argparse.Namespace,
    manifest: dict[str, Any],
    catalog: dict[str, Any],
) -> int:
    root = configctl.prepare_target(args.target)
    state = read_state(root, manifest, catalog)
    if not state or state.get("status") != "installed":
        raise configctl.ConfigError("no active external Skill installation found")
    actions: list[tuple[str, str]] = []
    for record in state.get("files", []):
        destination = configctl.target_path(root, record["target"])
        if not destination.exists():
            action = "missing"
        elif not destination.is_file() or configctl.is_link_or_reparse(destination):
            action = "drifted"
        elif configctl.sha256_file(destination) != record["installed_sha256"]:
            action = "drifted"
        else:
            action = "current"
        actions.append((action, record["target"]))
    configctl.print_plan("External Skill health", actions, False)
    print(
        "Capability skill-connection: lark-account=not_verified "
        "(authenticate and verify in the selected Runtime)"
    )
    print("Live runtime smoke: not performed")
    return 0 if all(action == "current" for action, _ in actions) else 2


def command_uninstall(
    args: argparse.Namespace,
    manifest: dict[str, Any],
    catalog: dict[str, Any],
) -> int:
    root = configctl.prepare_target(args.target)
    state = read_state(root, manifest, catalog)
    if not state or state.get("status") != "installed":
        raise configctl.ConfigError("no active external Skill installation found")
    actions: list[tuple[str, str]] = []
    removable: list[tuple[Path, dict[str, Any]]] = []
    for record in state.get("files", []):
        destination = configctl.target_path(root, record["target"])
        if not destination.exists():
            actions.append(("missing", record["target"]))
        elif (
            not destination.is_file()
            or configctl.is_link_or_reparse(destination)
            or configctl.sha256_file(destination) != record["installed_sha256"]
        ):
            actions.append(("drifted", record["target"]))
        else:
            actions.append(("remove", record["target"]))
            removable.append((destination, record))
    configctl.print_plan("External Skill uninstall plan", actions, args.apply)
    if args.apply and not args.confirm_uninstall:
        raise configctl.ConfigError("uninstall requires --confirm-uninstall")
    if args.apply:
        recovery_rel = PurePosixPath(
            ".agent-config-kit",
            "recovery",
            f"external-{int(time.time())}-{uuid.uuid4().hex[:8]}",
        )
        moves: list[tuple[Path, Path]] = []
        try:
            for destination, record in removable:
                backup = configctl.target_path(
                    root,
                    str(recovery_rel / PurePosixPath(record["target"])),
                )
                data = destination.read_bytes()
                if hashlib.sha256(data).hexdigest() != record["installed_sha256"]:
                    raise configctl.ConfigError(
                        f"external Skill changed during uninstall: {record['name']}"
                    )
                backup.parent.mkdir(parents=True, exist_ok=True)
                if configctl.is_link_or_reparse(backup.parent) or backup.exists():
                    raise configctl.ConfigError(
                        f"external recovery target is unsafe: {record['target']}"
                    )
                move_file(destination, backup)
                moves.append((backup, destination))
                if configctl.sha256_file(backup) != record["installed_sha256"]:
                    raise configctl.ConfigError(
                        f"external Skill changed while moving to recovery: {record['name']}"
                    )
            write_state(
                root,
                {
                    "schema_version": 1,
                    "status": "uninstalled",
                    "recovery": str(recovery_rel),
                    "previous": state,
                },
            )
        except Exception:
            rollback_errors: list[str] = []
            for backup, destination in reversed(moves):
                try:
                    if backup.exists() and not destination.exists():
                        move_file(backup, destination)
                except OSError:
                    rollback_errors.append(str(destination))
            if rollback_errors:
                raise configctl.ConfigError(
                    "external uninstall rollback needs manual recovery: "
                    + ", ".join(rollback_errors)
                )
            raise
        print(f"External Skill uninstall applied. Recovery: {recovery_rel}")
    return 0


def command_restore(
    args: argparse.Namespace,
    manifest: dict[str, Any],
    catalog: dict[str, Any],
) -> int:
    root = configctl.prepare_target(args.target)
    state = read_state(root, manifest, catalog)
    if not state or state.get("status") != "uninstalled":
        raise configctl.ConfigError("no external Skill uninstall recovery found")
    previous = state.get("previous")
    if not isinstance(previous, dict) or previous.get("status") != "installed":
        raise configctl.ConfigError("external Skill recovery state is invalid")
    recovery_rel = configctl.safe_rel(state["recovery"], "recovery path")
    actions: list[tuple[str, str]] = []
    restores: list[tuple[Path, Path, dict[str, Any]]] = []
    conflicts: list[str] = []
    for record in previous.get("files", []):
        destination = configctl.target_path(root, record["target"])
        backup = configctl.target_path(
            root,
            str(recovery_rel / PurePosixPath(record["target"])),
        )
        if destination.exists():
            actions.append(("conflict", record["target"]))
            conflicts.append(record["target"])
        elif (
            not backup.is_file()
            or configctl.is_link_or_reparse(backup)
            or configctl.sha256_file(backup) != record["installed_sha256"]
        ):
            actions.append(("missing", record["target"]))
            conflicts.append(record["target"])
        else:
            actions.append(("restore", record["target"]))
            restores.append((backup, destination, record))
    configctl.print_plan("External Skill restore plan", actions, args.apply)
    if conflicts:
        raise configctl.ConfigError(
            "external Skill restore conflicts: " + ", ".join(conflicts)
        )
    if args.apply:
        written: list[Path] = []
        try:
            for backup, destination, record in restores:
                data = backup.read_bytes()
                if hashlib.sha256(data).hexdigest() != record["installed_sha256"]:
                    raise configctl.ConfigError(
                        f"external recovery changed during restore: {record['name']}"
                    )
                exclusive_write(destination, data)
                written.append(destination)
            write_state(root, previous)
        except Exception:
            for path in reversed(written):
                if path.exists() and path.is_file() and not configctl.is_link_or_reparse(path):
                    path.unlink()
            raise
        print("External Skill restore applied. Run external doctor next.")
    return 0


def build_parser(catalog: dict[str, Any]) -> argparse.ArgumentParser:
    packs = sorted(validate_catalog(catalog))
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("verify-catalog", help="validate official Skill pins")

    install = subparsers.add_parser("install", help="preview or apply official Skill fetch")
    install.add_argument("--runtime", required=True, choices=("codex", "cursor", "claude-code"))
    install.add_argument("--pack", action="append", choices=packs, required=True)
    install.add_argument("--target", required=True)
    install.add_argument("--apply", action="store_true")

    doctor = subparsers.add_parser("doctor", help="diagnose fetched official Skills")
    doctor.add_argument("--target", required=True)

    uninstall = subparsers.add_parser("uninstall", help="preview or recoverably uninstall")
    uninstall.add_argument("--target", required=True)
    uninstall.add_argument("--apply", action="store_true")
    uninstall.add_argument("--confirm-uninstall", action="store_true")

    restore = subparsers.add_parser("restore", help="preview or restore the last uninstall")
    restore.add_argument("--target", required=True)
    restore.add_argument("--apply", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    try:
        catalog = load_json(CATALOG_PATH)
        args = build_parser(catalog).parse_args(argv)
        manifest = configctl.load_manifest()
        configctl.validate_package(manifest)
        if args.command == "verify-catalog":
            packs = validate_catalog(catalog)
            skill_count = sum(len(pack["skills"]) for pack in packs.values())
            print(f"External catalog OK: packs={len(packs)} skills={skill_count}")
            return 0
        if args.command == "install":
            return command_install(args, manifest, catalog)
        if args.command == "doctor":
            return command_doctor(args, manifest, catalog)
        if args.command == "uninstall":
            return command_uninstall(args, manifest, catalog)
        if args.command == "restore":
            return command_restore(args, manifest, catalog)
        raise configctl.ConfigError(f"unsupported command: {args.command}")
    except (
        configctl.ConfigError,
        KeyError,
        OSError,
        TypeError,
        ValueError,
    ) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
