#!/usr/bin/env python3
"""Deterministic release verification for Agent Config Kit."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PYTHON = sys.executable
EXCLUDED_ARTIFACT_DIRS = {
    ".cache",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".venv",
    "node_modules",
    "venv",
    "vendor",
}
PORTABLE_OMISSION_REASONS = {
    "dependency_cache",
    "generation_material",
    "local_state",
    "recovery_artifact",
    "test_metadata",
}
BINARY_ASSET_CATALOG = ROOT / "catalog" / "binary_assets.json"


def is_recovery_artifact(name: str) -> bool:
    return (
        "NSConflict" in name
        or ".bak-" in name
        or name.startswith(("backup-", "archive-"))
    )


def is_excluded_artifact_dir(path: Path) -> bool:
    return path.name.lower() in EXCLUDED_ARTIFACT_DIRS


def run(*args: str) -> None:
    result = subprocess.run(
        [PYTHON, *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode:
        raise RuntimeError(
            f"command failed: {' '.join(args)}\n{result.stdout}{result.stderr}"
        )


def approved_binary_assets(
    root: Path,
    catalog: dict | None = None,
) -> dict[str, str]:
    value = (
        catalog
        if catalog is not None
        else json.loads(BINARY_ASSET_CATALOG.read_text(encoding="utf-8"))
    )
    assets = value.get("assets") if isinstance(value, dict) else None
    if value.get("schema_version") != 1 or not isinstance(assets, list):
        raise RuntimeError("invalid binary asset catalog")
    approved: dict[str, str] = {}
    for asset in assets:
        path = asset.get("path") if isinstance(asset, dict) else None
        digest = asset.get("sha256") if isinstance(asset, dict) else None
        description = asset.get("description") if isinstance(asset, dict) else None
        relative = Path(path) if isinstance(path, str) else None
        if (
            relative is None
            or relative.is_absolute()
            or ".." in relative.parts
            or not isinstance(digest, str)
            or not re.fullmatch(r"[0-9a-f]{64}", digest)
            or not isinstance(description, str)
            or not description.strip()
            or path in approved
        ):
            raise RuntimeError("invalid binary asset record")
        file_path = root / relative
        if (
            not file_path.is_file()
            or file_path.is_symlink()
            or hashlib.sha256(file_path.read_bytes()).hexdigest() != digest
        ):
            raise RuntimeError(f"binary asset digest mismatch: {path}")
        approved[path] = digest
    return approved


def check_tree() -> None:
    sensitive_patterns = {
        "absolute macOS home path": re.compile(
            re.escape("/" + "Users" + "/") + r"[^/\s]+/"
        ),
        "absolute Linux home path": re.compile(
            re.escape("/" + "home" + "/") + r"[^/\s]+/"
        ),
        "absolute Windows home path": re.compile(
            r"[A-Za-z]:\\Users\\[^\\\s]+\\"
        ),
        "private key": re.compile(
            r"BEGIN (?:(?:RSA|OPENSSH|EC|DSA|ENCRYPTED) )?PRIVATE KEY"
        ),
        "PGP private key": re.compile("BEGIN " + r"PGP PRIVATE KEY BLOCK"),
        "AWS access key": re.compile(r"AKIA[0-9A-Z]{16}"),
        "AWS temporary access key": re.compile(r"ASIA[0-9A-Z]{16}"),
        "OpenAI-style secret": re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b"),
        "GitHub token": re.compile(r"\b(?:ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9]{20,}\b"),
        "GitHub fine-grained token": re.compile(r"\bgithub_pat_[A-Za-z0-9_]{20,}\b"),
        "Slack token": re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{20,}\b"),
    }
    approved_binaries = approved_binary_assets(ROOT)
    seen_binaries: set[str] = set()
    problems: list[str] = []
    for path in sorted(ROOT.rglob("*")):
        rel = path.relative_to(ROOT)
        if (
            ".git" in rel.parts
            or ".agent-config-kit" in rel.parts
            or ".agent-config-kit-workbench" in rel.parts
            or "__pycache__" in rel.parts
        ):
            continue
        if path.is_dir() and is_excluded_artifact_dir(path):
            problems.append(f"excluded dependency or cache directory: {rel}")
            continue
        if path.is_symlink():
            problems.append(f"symlink: {rel}")
            continue
        if is_recovery_artifact(path.name):
            problems.append(f"recovery or backup artifact: {rel}")
        if path.is_file():
            try:
                text = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                portable_path = rel.as_posix()
                if portable_path in approved_binaries:
                    seen_binaries.add(portable_path)
                else:
                    problems.append(f"binary file: {rel}")
                continue
            if ("[" + "TODO") in text:
                problems.append(f"unfinished placeholder: {rel}")
            for label, pattern in sensitive_patterns.items():
                if pattern.search(text):
                    problems.append(f"{label}: {rel}")
    for stale in sorted(set(approved_binaries) - seen_binaries):
        problems.append(f"binary asset is no longer binary: {stale}")
    if problems:
        raise RuntimeError("\n".join(problems))


def check_json_and_hook() -> None:
    manifest = json.loads((ROOT / "manifest.json").read_text(encoding="utf-8"))
    python_command = subprocess.list2cmdline([PYTHON])
    for profile_name in manifest["profiles"]:
        for runtime, runtime_spec in manifest["runtimes"].items():
            hook_items = runtime_spec["hooks_by_profile"][profile_name]
            if len(hook_items) != 1:
                raise RuntimeError(f"invalid Hook adapter count: {runtime}/{profile_name}")
            hook = json.loads(
                (ROOT / hook_items[0]["source"]).read_text(encoding="utf-8")
            )
            if runtime == "cursor":
                command = hook["hooks"]["sessionStart"][0]["command"]
            else:
                command = hook["hooks"]["SessionStart"][0]["hooks"][0]["command"]
            executable = command.replace("python3", python_command, 1)
            result = subprocess.run(
                executable,
                cwd=ROOT,
                input="{}",
                text=True,
                capture_output=True,
                shell=True,
                check=True,
            )
            payload = json.loads(result.stdout)
            if runtime == "cursor":
                context = payload.get("additional_context")
                if not payload.get("continue") or not context:
                    raise RuntimeError("Cursor hook output is invalid")
            else:
                output = payload["hookSpecificOutput"]
                context = output["additionalContext"]
                if output["hookEventName"] != "SessionStart" or not context:
                    raise RuntimeError(f"{runtime} hook output is invalid")
            if profile_name == "knowledge-vault" and "Knowledge Vault" not in context:
                raise RuntimeError(f"layered Hook context is missing: {runtime}")
            if profile_name == "full" and "Full profile is active" not in context:
                raise RuntimeError(f"full Hook context is missing: {runtime}")

    for runtime in ("codex", "cursor", "claude-code"):
        result = subprocess.run(
            [
                PYTHON,
                str(ROOT / "packs/safe-hooks/start_here.py"),
                "--format",
                runtime,
            ],
            text=True,
            capture_output=True,
            check=True,
        )
        json.loads(result.stdout)


def check_portable_patches() -> None:
    catalog = json.loads(
        (ROOT / "catalog" / "portable_patches.json").read_text(encoding="utf-8")
    )
    admissions = json.loads(
        (ROOT / "catalog" / "admissions.json").read_text(encoding="utf-8")
    )
    snapshots = json.loads(
        (ROOT / "catalog" / "snapshot_imports.json").read_text(encoding="utf-8")
    )
    maintainer_snapshot_path = ROOT / "catalog" / "maintainer_source_snapshot.json"
    if maintainer_snapshot_path.is_file():
        maintainer_snapshot = json.loads(
            maintainer_snapshot_path.read_text(encoding="utf-8")
        )
        if (
            maintainer_snapshot.get("schema_version") != 1
            or not isinstance(maintainer_snapshot.get("imports"), dict)
        ):
            raise RuntimeError("invalid maintainer source snapshot")
        maintainer_import = maintainer_snapshot["imports"].get(
            "maintainer-current-portable"
        )
        maintainer_files = (
            maintainer_import.get("files")
            if isinstance(maintainer_import, dict)
            else None
        )
        if (
            set(maintainer_snapshot["imports"])
            != {"maintainer-current-portable"}
            or not isinstance(maintainer_import, dict)
            or maintainer_import.get("origin") != "this-repository"
            or not isinstance(maintainer_files, list)
            or any(
                not isinstance(record, dict)
                or set(record) != {"sha256"}
                or re.fullmatch(r"[0-9a-f]{64}", str(record["sha256"]))
                is None
                for record in maintainer_files
            )
        ):
            raise RuntimeError(
                "maintainer source snapshot must contain hash-only records"
            )
        snapshots = {
            **snapshots,
            "imports": {
                **snapshots.get("imports", {}),
                **maintainer_snapshot["imports"],
            },
        }
    provenance = registered_source_anchors(admissions, snapshots)
    patches = catalog.get("patches")
    omissions = catalog.get("omissions", [])
    omission_summary = catalog.get("omission_summary")
    if (
        catalog.get("schema_version") != 1
        or not isinstance(patches, list)
        or not isinstance(omissions, list)
        or omissions
        or not isinstance(omission_summary, dict)
        or not isinstance(omission_summary.get("total"), int)
        or omission_summary["total"] < 0
        or not isinstance(omission_summary.get("by_reason"), dict)
        or sum(omission_summary["by_reason"].values())
        != omission_summary["total"]
        or any(
            reason not in PORTABLE_OMISSION_REASONS
            or not isinstance(count, int)
            or count < 0
            for reason, count in omission_summary["by_reason"].items()
        )
    ):
        raise RuntimeError("invalid portable patch catalog")
    seen: set[str] = set()
    digest_pattern = re.compile(r"[0-9a-f]{64}")
    commit_pattern = re.compile(r"[0-9a-f]{40}")
    for patch in patches:
        if not isinstance(patch, dict):
            raise RuntimeError("portable patch entry must be an object")
        relative = patch.get("packaged_path")
        if (
            not isinstance(relative, str)
            or not relative.startswith("packs/")
            or Path(relative).is_absolute()
            or ".." in Path(relative).parts
            or relative in seen
        ):
            raise RuntimeError(f"unsafe or duplicate portable patch path: {relative}")
        seen.add(relative)
        source_digest = patch.get("source_sha256")
        packaged_digest = patch.get("packaged_sha256")
        if (
            not isinstance(source_digest, str)
            or not digest_pattern.fullmatch(source_digest)
            or not isinstance(packaged_digest, str)
            or not digest_pattern.fullmatch(packaged_digest)
            or source_digest == packaged_digest
        ):
            raise RuntimeError(f"invalid portable patch digests: {relative}")
        upstream_commit = patch.get("upstream_commit")
        source_snapshot = patch.get("source_snapshot")
        if (upstream_commit is None) == (source_snapshot is None):
            raise RuntimeError(
                f"portable patch needs one source anchor: {relative}"
            )
        if upstream_commit is not None and not commit_pattern.fullmatch(
            str(upstream_commit)
        ):
            raise RuntimeError(f"invalid portable patch commit: {relative}")
        upstream_origin = patch.get("upstream_origin")
        if not is_registered_source_anchor(
            upstream_origin=upstream_origin,
            upstream_commit=upstream_commit,
            source_snapshot=source_snapshot,
            source_sha256=source_digest,
            provenance=provenance,
        ):
            raise RuntimeError(
                f"portable patch source anchor is not registered: {relative}"
            )
        if source_snapshot is not None:
            if (
                not isinstance(source_snapshot, str)
                or not source_snapshot.startswith("catalog/")
                or Path(source_snapshot).is_absolute()
                or ".." in Path(source_snapshot).parts
            ):
                raise RuntimeError(
                    f"invalid portable patch snapshot: {relative}"
                )
            snapshot_path = ROOT / source_snapshot
            if not snapshot_path.is_file():
                raise RuntimeError(
                    f"portable patch snapshot is missing: {relative}"
                )
            snapshot = snapshot_path.read_text(encoding="utf-8")
            if source_digest not in snapshot:
                raise RuntimeError(
                    f"portable patch source digest is not anchored: {relative}"
                )
        if source_snapshot == "catalog/maintainer_source_snapshot.json":
            transformation = patch.get("transformation")
            if "source_path" in patch or transformation not in {
                "deterministic_portability_sanitizer",
                "package_generator:scripts/build_full_router_index.py",
                "reviewed_manual_portable_derivative",
            }:
                raise RuntimeError(
                    f"invalid maintainer-private portable patch: {relative}"
                )
            if (
                transformation
                == "package_generator:scripts/build_full_router_index.py"
                and relative
                != (
                    "packs/full-routing/skills/all-skills-router/"
                    "references/skill-index.json"
                )
            ):
                raise RuntimeError(
                    f"invalid package generator target: {relative}"
                )
        path = ROOT / relative
        if not path.is_file():
            raise RuntimeError(f"portable patched file is missing: {relative}")
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        if actual != packaged_digest:
            raise RuntimeError(f"portable patched file differs: {relative}")
    seen_omissions: set[tuple[str, str]] = set()
    for omission in omissions:
        validate_portable_omission(omission, provenance=provenance)
        key = (omission["skill"], omission["source_path"])
        if key in seen_omissions:
            raise RuntimeError(
                f"duplicate portable omission: {key[0]}/{key[1]}"
            )
        seen_omissions.add(key)
        snapshot_path = ROOT / omission["source_snapshot"]
        if not snapshot_path.is_file():
            raise RuntimeError(
                f"portable omission snapshot is missing: {key[0]}/{key[1]}"
            )
        if omission["source_sha256"] not in snapshot_path.read_text(encoding="utf-8"):
            raise RuntimeError(
                f"portable omission source digest is not anchored: {key[0]}/{key[1]}"
            )


def validate_portable_omission(
    omission: object,
    *,
    provenance: dict[str, set[object]],
) -> None:
    if not isinstance(omission, dict):
        raise RuntimeError("portable omission entry must be an object")
    skill = omission.get("skill")
    source_path = omission.get("source_path")
    digest = omission.get("source_sha256")
    reason = omission.get("reason")
    description = omission.get("description")
    source_snapshot = omission.get("source_snapshot")
    origin = omission.get("upstream_origin")
    safe_component = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]*")
    digest_pattern = re.compile(r"[0-9a-f]{64}")
    if not isinstance(skill, str) or not safe_component.fullmatch(skill):
        raise RuntimeError(f"invalid portable omission skill: {skill}")
    if (
        not isinstance(source_path, str)
        or Path(source_path).is_absolute()
        or "\\" in source_path
        or ".." in Path(source_path).parts
    ):
        raise RuntimeError(f"invalid portable omission path: {skill}/{source_path}")
    if not isinstance(digest, str) or not digest_pattern.fullmatch(digest):
        raise RuntimeError(f"invalid portable omission digest: {skill}/{source_path}")
    if reason not in PORTABLE_OMISSION_REASONS:
        raise RuntimeError(f"invalid portable omission reason: {skill}/{source_path}")
    if not isinstance(description, str) or not description.strip():
        raise RuntimeError(
            f"portable omission description is missing: {skill}/{source_path}"
        )
    if (
        not isinstance(source_snapshot, str)
        or not source_snapshot.startswith("catalog/")
        or Path(source_snapshot).is_absolute()
        or ".." in Path(source_snapshot).parts
    ):
        raise RuntimeError(
            f"invalid portable omission snapshot: {skill}/{source_path}"
        )
    if not is_registered_source_anchor(
        upstream_origin=origin,
        upstream_commit=None,
        source_snapshot=source_snapshot,
        source_sha256=digest,
        provenance=provenance,
    ):
        raise RuntimeError(
            f"portable omission source anchor is not registered: {skill}/{source_path}"
        )


def registered_source_anchors(
    admissions: dict[str, object],
    snapshots: dict[str, object],
) -> dict[str, set[object]]:
    groups = admissions.get("provenance_groups")
    imports = snapshots.get("imports")
    if (
        admissions.get("schema_version") != 1
        or not isinstance(groups, dict)
        or snapshots.get("schema_version") != 1
        or not isinstance(imports, dict)
    ):
        raise RuntimeError("invalid source provenance catalogs")
    origins: set[object] = set()
    commits: set[object] = set()
    source_hashes: set[object] = set()
    for group in groups.values():
        if not isinstance(group, dict):
            raise RuntimeError("invalid provenance group")
        origin = group.get("origin")
        if isinstance(origin, str):
            origins.add(origin)
            commit = group.get("commit")
            if isinstance(commit, str):
                commits.add((origin, commit))
    for snapshot in imports.values():
        if not isinstance(snapshot, dict):
            raise RuntimeError("invalid snapshot import")
        origin = snapshot.get("origin")
        files = snapshot.get("files")
        if not isinstance(origin, str):
            continue
        if isinstance(files, list):
            for file_record in files:
                digest = (
                    file_record.get("sha256")
                    if isinstance(file_record, dict)
                    else None
                )
                if isinstance(digest, str):
                    source_hashes.add((origin, digest))
        skills = snapshot.get("skills")
        if isinstance(skills, dict):
            for digest in skills.values():
                if isinstance(digest, str):
                    source_hashes.add((origin, digest))
    return {
        "origins": origins,
        "commits": commits,
        "source_hashes": source_hashes,
    }


def is_registered_source_anchor(
    *,
    upstream_origin: object,
    upstream_commit: object,
    source_snapshot: object,
    source_sha256: str,
    provenance: dict[str, set[object]],
) -> bool:
    if (
        not isinstance(upstream_origin, str)
        or upstream_origin not in provenance["origins"]
    ):
        return False
    if isinstance(upstream_commit, str):
        if upstream_commit == "0" * 40:
            return False
        return (upstream_origin, upstream_commit) in provenance["commits"]
    if isinstance(source_snapshot, str):
        return (upstream_origin, source_sha256) in provenance["source_hashes"]
    return False


def main() -> int:
    try:
        check_tree()
        run("scripts/build_adapters.py", "--check")
        run("scripts/build_full_router_index.py", "--check")
        run(
            "scripts/audit_skill_sources.py",
            "--source",
            f"public-packs={ROOT / 'packs'}",
            "--fail-on-blockers",
        )
        run("scripts/build_skill_catalog.py", "--check")
        run("scripts/check_sensitive_reviews.py")
        run("scripts/live_runtime_smoke.py", "check-contract")
        run("scripts/check_admissions.py")
        run("scripts/check_local_release_inventory.py")
        run("install/scripts/configctl.py", "verify-package")
        run("install/scripts/externalctl.py", "verify-catalog")
        check_portable_patches()
        check_json_and_hook()
    except (OSError, KeyError, json.JSONDecodeError, RuntimeError) as exc:
        print(f"VERIFY FAILED: {exc}", file=sys.stderr)
        return 1
    print(
        "PACKAGE VERIFY OK: tree, adapters, manifest, release inventory, skills, "
        "live Runtime contract, JSON, and safe hook; source alignment requires "
        "the maintainer gate"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
