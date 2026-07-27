#!/usr/bin/env python3
"""Verify portable Rule profiles against a private reviewed source snapshot."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "manifest.json"
BASE_MARKERS = (
    "老板",
    "授权矩阵",
    "最强大脑",
    "删除前必须",
    "外部账号、凭证、登录、扫码和授权",
)
PROFILE_MARKERS = {
    "daily-work": (),
    "knowledge-vault": (
        "Knowledge Vault working contract",
        "可接续性",
    ),
    "full": (
        "Knowledge Vault working contract",
        "Unknown Management Gate",
        "Common Failure Modes",
        "Document Restraint",
        "Output Self-Explanation Restraint",
    ),
}
FORBIDDEN_MARKERS = (
    "\u6600\u5ce4",
    "/Users/",
    "@/Users/",
    "AI-Zettelkasten",
    ".agent-config-kit-workbench",
    "rtk ",
)


class RuleAlignmentError(Exception):
    pass


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def load_json(path: Path, label: str) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise RuleAlignmentError(f"{label} is invalid") from exc
    if not isinstance(value, dict):
        raise RuleAlignmentError(f"{label} is invalid")
    return value


def compose_rule(package_root: Path, sources: list[str]) -> str:
    parts: list[str] = []
    for source in sources:
        rel = Path(source)
        if (
            rel.is_absolute()
            or ".." in rel.parts
            or not source.startswith("packs/core/rules/")
        ):
            raise RuleAlignmentError(f"unsafe portable Rule source: {source}")
        path = package_root / rel
        if path.is_symlink() or not path.is_file():
            raise RuleAlignmentError(f"portable Rule source is missing: {source}")
        parts.append(path.read_text(encoding="utf-8").strip())
    return "\n\n".join(parts) + "\n"


def check_alignment(
    review_path: Path,
    *,
    package_root: Path = ROOT,
    manifest_path: Path = MANIFEST_PATH,
) -> dict[str, int]:
    review = load_json(review_path, "private Rule review")
    manifest = load_json(manifest_path, "manifest")
    if (
        set(review)
        != {
            "profiles",
            "reviewed_transformations",
            "schema_version",
            "sensitivity",
            "source",
        }
        or review.get("schema_version") != 1
        or review.get("sensitivity") != "private_do_not_publish"
    ):
        raise RuleAlignmentError("private Rule review has an invalid schema")

    source = review["source"]
    if (
        not isinstance(source, dict)
        or set(source) != {"label", "path", "sha256"}
        or source.get("label") != "workspace-agents"
        or not isinstance(source.get("path"), str)
        or not isinstance(source.get("sha256"), str)
    ):
        raise RuleAlignmentError("private Rule source record is invalid")
    source_path = Path(source["path"]).expanduser()
    if (
        not source_path.is_absolute()
        or source_path.is_symlink()
        or not source_path.is_file()
    ):
        raise RuleAlignmentError("private Rule source is missing or unsafe")
    try:
        source_path.resolve().relative_to(package_root.resolve())
    except ValueError:
        pass
    else:
        raise RuleAlignmentError("private Rule source must be outside the package")
    if sha256_bytes(source_path.read_bytes()) != source["sha256"]:
        raise RuleAlignmentError(
            "live AGENTS.md changed after the portable Rule review"
        )

    transformations = review["reviewed_transformations"]
    if (
        not isinstance(transformations, list)
        or not transformations
        or not all(
            isinstance(item, str) and item.strip()
            for item in transformations
        )
    ):
        raise RuleAlignmentError("portable Rule transformations are not reviewed")

    manifest_profiles = manifest.get("profiles")
    reviewed_profiles = review["profiles"]
    if (
        not isinstance(manifest_profiles, dict)
        or not isinstance(reviewed_profiles, dict)
        or set(manifest_profiles) != set(PROFILE_MARKERS)
        or set(reviewed_profiles) != set(PROFILE_MARKERS)
    ):
        raise RuleAlignmentError("portable Rule profiles are incomplete")

    checked_sources: set[str] = set()
    for profile_name, markers in PROFILE_MARKERS.items():
        manifest_sources = manifest_profiles[profile_name].get("rule_sources")
        record = reviewed_profiles[profile_name]
        if (
            not isinstance(manifest_sources, list)
            or not isinstance(record, dict)
            or set(record) != {"composed_sha256", "rule_sources"}
            or record.get("rule_sources") != manifest_sources
            or not isinstance(record.get("composed_sha256"), str)
        ):
            raise RuleAlignmentError(
                f"portable Rule review differs from manifest: {profile_name}"
            )
        body = compose_rule(package_root, manifest_sources)
        digest = sha256_bytes(body.encode("utf-8"))
        if digest != record["composed_sha256"]:
            raise RuleAlignmentError(
                f"portable Rule changed after review: {profile_name}"
            )
        for marker in (*BASE_MARKERS, *markers):
            if marker not in body:
                raise RuleAlignmentError(
                    f"portable Rule contract is missing: {profile_name}/{marker}"
                )
        for marker in FORBIDDEN_MARKERS:
            if marker in body:
                raise RuleAlignmentError(
                    f"portable Rule contains private or local marker: {profile_name}"
                )
        checked_sources.update(manifest_sources)

    return {
        "profiles": len(PROFILE_MARKERS),
        "sources": len(checked_sources),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--private-review", required=True, type=Path)
    args = parser.parse_args()
    try:
        counts = check_alignment(args.private_review)
    except (OSError, RuleAlignmentError) as exc:
        print(f"RULE SOURCE ALIGNMENT FAILED: {exc}", file=sys.stderr)
        return 2
    print(
        "RULE SOURCE ALIGNMENT OK: "
        f"profiles={counts['profiles']} sources={counts['sources']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
