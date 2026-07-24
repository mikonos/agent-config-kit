#!/usr/bin/env python3
"""Run the private source-alignment gate before package verification."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from collections.abc import Callable
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
Runner = Callable[[list[str]], int]
IgnoredChecker = Callable[[Path], bool]
REQUIRED_SOURCE_LABELS = {
    "cursor-vault",
    "agents-global",
    "codex-global",
}
PRIVATE_WORKBENCH = ROOT / ".agent-config-kit-workbench"
PRIVATE_INPUTS = {
    "private inventory": PRIVATE_WORKBENCH / "private-skill-inventory.json",
    "privacy ledger": PRIVATE_WORKBENCH / "private-term-hashes.json",
    "private omissions": PRIVATE_WORKBENCH / "private-portable-omissions.json",
    "private reviewed derivatives": (
        PRIVATE_WORKBENCH / "reviewed-portable-derivatives.json"
    ),
    "private source roots": PRIVATE_WORKBENCH / "private-source-roots.json",
    "reviewed binary assets": PRIVATE_WORKBENCH / "reviewed-binary-assets.json",
}


def default_runner(command: list[str]) -> int:
    return subprocess.run(command, cwd=ROOT, check=False).returncode


def run_preflight(
    *,
    privacy_command: list[str] | None = None,
    alignment_command: list[str],
    verification_command: list[str],
    runner: Runner = default_runner,
) -> int:
    if privacy_command is not None:
        privacy_result = runner(privacy_command)
        if privacy_result:
            return privacy_result
    alignment_result = runner(alignment_command)
    if alignment_result:
        return alignment_result
    return runner(verification_command)


def load_private_source_roots(path: Path) -> dict[str, Path]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError("private source-root ledger is invalid") from exc
    if not isinstance(value, dict):
        raise ValueError("private source-root ledger is invalid")
    sources = value.get("sources")
    if (
        value.get("schema_version") != 1
        or value.get("sensitivity") != "private_do_not_publish"
        or not isinstance(sources, dict)
        or set(sources) != REQUIRED_SOURCE_LABELS
    ):
        raise ValueError("private source-root ledger is invalid")
    result: dict[str, Path] = {}
    for label, raw_path in sources.items():
        path_value = Path(raw_path).expanduser() if isinstance(raw_path, str) else None
        if (
            path_value is None
            or not path_value.is_absolute()
            or path_value.is_symlink()
            or not path_value.is_dir()
        ):
            raise ValueError("private source-root ledger is invalid")
        result[label] = path_value.resolve()
    return result


def validate_source_args(
    values: list[str],
    *,
    canonical_roots: dict[str, Path] | None = None,
    package_root: Path = ROOT,
) -> list[str]:
    parsed: dict[str, Path] = {}
    for value in values:
        if "=" not in value:
            raise ValueError("source must use LABEL=PATH")
        label, path = value.split("=", 1)
        if not label or not path:
            raise ValueError("source must use non-empty LABEL=PATH")
        if label in parsed:
            raise ValueError("source labels must be unique")
        supplied = Path(path).expanduser()
        if supplied.is_symlink() or not supplied.is_dir():
            raise ValueError(f"source root is missing or invalid: {label}")
        resolved = supplied.resolve()
        try:
            resolved.relative_to(package_root.resolve())
        except ValueError:
            pass
        else:
            raise ValueError("release source roots must be outside the package")
        parsed[label] = resolved
    if set(parsed) != REQUIRED_SOURCE_LABELS:
        expected = ", ".join(sorted(REQUIRED_SOURCE_LABELS))
        raise ValueError(f"release requires exactly these source labels: {expected}")
    if canonical_roots is not None and parsed != canonical_roots:
        raise ValueError("release source roots do not match the private canonical ledger")
    return values


def git_ignored(path: Path) -> bool:
    try:
        relative = path.relative_to(ROOT)
    except ValueError:
        return False
    result = subprocess.run(
        ["git", "check-ignore", "-q", "--", relative.as_posix()],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    return result.returncode == 0


def validate_private_path(
    value: Path,
    *,
    expected: Path,
    label: str,
    ignored_checker: IgnoredChecker = git_ignored,
) -> Path:
    supplied = value.expanduser()
    if (
        supplied.is_symlink()
        or expected.parent.is_symlink()
        or supplied.resolve() != expected.resolve()
    ):
        raise ValueError(
            f"{label} must use the fixed Git-ignored maintainer workbench path"
        )
    if not expected.is_file() or not ignored_checker(expected):
        raise ValueError(
            f"{label} is missing or is not Git-ignored in the maintainer workbench"
        )
    return expected


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", action="append", required=True)
    parser.add_argument("--private-inventory", required=True, type=Path)
    parser.add_argument(
        "--privacy-ledger",
        type=Path,
        default=ROOT
        / ".agent-config-kit-workbench"
        / "private-term-hashes.json",
    )
    parser.add_argument(
        "--private-omissions",
        type=Path,
        default=ROOT
        / ".agent-config-kit-workbench"
        / "private-portable-omissions.json",
    )
    parser.add_argument(
        "--private-reviewed-derivatives",
        type=Path,
        default=ROOT
        / ".agent-config-kit-workbench"
        / "reviewed-portable-derivatives.json",
    )
    parser.add_argument(
        "--private-source-roots",
        type=Path,
        default=PRIVATE_INPUTS["private source roots"],
    )
    parser.add_argument(
        "--reviewed-binary-assets",
        type=Path,
        default=PRIVATE_INPUTS["reviewed binary assets"],
    )
    args = parser.parse_args()
    try:
        private_inventory = validate_private_path(
            args.private_inventory,
            expected=PRIVATE_INPUTS["private inventory"],
            label="private inventory",
        )
        privacy_ledger = validate_private_path(
            args.privacy_ledger,
            expected=PRIVATE_INPUTS["privacy ledger"],
            label="privacy ledger",
        )
        private_omissions = validate_private_path(
            args.private_omissions,
            expected=PRIVATE_INPUTS["private omissions"],
            label="private omissions",
        )
        private_reviewed_derivatives = validate_private_path(
            args.private_reviewed_derivatives,
            expected=PRIVATE_INPUTS["private reviewed derivatives"],
            label="private reviewed derivatives",
        )
        private_source_roots = validate_private_path(
            args.private_source_roots,
            expected=PRIVATE_INPUTS["private source roots"],
            label="private source roots",
        )
        reviewed_binary_assets = validate_private_path(
            args.reviewed_binary_assets,
            expected=PRIVATE_INPUTS["reviewed binary assets"],
            label="reviewed binary assets",
        )
        sources = validate_source_args(
            args.source,
            canonical_roots=load_private_source_roots(private_source_roots),
        )
    except ValueError as exc:
        parser.error(str(exc))

    alignment_command = [
        sys.executable,
        str(ROOT / "scripts" / "check_source_alignment.py"),
    ]
    for source in sources:
        alignment_command.extend(["--source", source])
    alignment_command.extend(
        [
            "--private-inventory",
            str(private_inventory),
            "--manifest",
            str(ROOT / "manifest.json"),
            "--portable-patches",
            str(ROOT / "catalog" / "portable_patches.json"),
            "--private-omissions",
            str(private_omissions),
            "--private-reviewed-derivatives",
            str(private_reviewed_derivatives),
        ]
    )
    result = run_preflight(
        privacy_command=[
            sys.executable,
            str(ROOT / "scripts" / "check_semantic_privacy.py"),
            "--ledger",
            str(privacy_ledger),
            "--private-inventory",
            str(private_inventory),
            "--reviewed-binary-assets",
            str(reviewed_binary_assets),
        ],
        alignment_command=alignment_command,
        verification_command=[
            sys.executable,
            str(ROOT / "scripts" / "verify.py"),
        ],
    )
    if result == 0:
        print("RELEASE PREFLIGHT OK: source alignment and package verification passed")
    return result


if __name__ == "__main__":
    raise SystemExit(main())
