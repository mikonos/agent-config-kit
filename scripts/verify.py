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
    problems: list[str] = []
    for path in sorted(ROOT.rglob("*")):
        rel = path.relative_to(ROOT)
        if ".git" in rel.parts or "__pycache__" in rel.parts:
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
                problems.append(f"binary file: {rel}")
                continue
            if ("[" + "TODO") in text:
                problems.append(f"unfinished placeholder: {rel}")
            for label, pattern in sensitive_patterns.items():
                if pattern.search(text):
                    problems.append(f"{label}: {rel}")
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
    patches = catalog.get("patches")
    if catalog.get("schema_version") != 1 or not isinstance(patches, list):
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
        path = ROOT / relative
        if not path.is_file():
            raise RuntimeError(f"portable patched file is missing: {relative}")
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        if actual != packaged_digest:
            raise RuntimeError(f"portable patched file differs: {relative}")


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
        run("scripts/check_semantic_privacy.py")
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
        "VERIFY OK: tree, adapters, manifest, release inventory, skills, "
        "live Runtime contract, JSON, and safe hook"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
