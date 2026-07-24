#!/usr/bin/env python3
"""Export a local skills lock as a path-free public source catalog."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path, PurePosixPath
from typing import Any, Optional
from urllib.parse import urlsplit


NAME_PATTERN = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]*")
TREE_SHA_PATTERN = re.compile(r"[0-9a-f]{40}")
ALLOWED_SOURCE_TYPES = {"git", "github", "well-known"}


def normalize_source_url(source_type: str, value: str) -> str:
    if source_type == "git" and value.startswith("git@github.com:"):
        repository = value.removeprefix("git@github.com:").removesuffix(".git")
        if not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", repository):
            raise ValueError("invalid GitHub SSH source")
        return f"https://github.com/{repository}"
    if value.startswith("https://github.com/"):
        parsed = urlsplit(value)
        repository = parsed.path.strip("/").removesuffix(".git")
        if (
            parsed.scheme != "https"
            or parsed.hostname != "github.com"
            or parsed.username is not None
            or parsed.password is not None
            or parsed.port is not None
            or parsed.query
            or parsed.fragment
            or not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", repository)
        ):
            raise ValueError("unsafe GitHub source URL")
        return f"https://github.com/{repository}"
    if source_type == "well-known":
        parsed = urlsplit(value)
        if (
            parsed.scheme != "https"
            or not parsed.hostname
            or parsed.username is not None
            or parsed.password is not None
            or parsed.port is not None
            or parsed.query
            or parsed.fragment
        ):
            raise ValueError("unsafe well-known source URL")
        return value
    raise ValueError(f"unsupported public source URL: {value}")


def validate_skill_path(value: Optional[str]) -> Optional[str]:
    if value is None:
        return None
    path = PurePosixPath(value)
    if (
        "\\" in value
        or re.match(r"^[A-Za-z]:", value)
        or value.startswith("//")
        or path.is_absolute()
        or ".." in path.parts
        or path.name != "SKILL.md"
    ):
        raise ValueError(f"invalid skill path: {value}")
    return path.as_posix()


def admitted_skill_names(path: Optional[Path]) -> set[str]:
    if path is None:
        return set()
    payload = json.loads(path.read_text(encoding="utf-8"))
    skills = payload.get("skills")
    if not isinstance(skills, dict):
        raise ValueError("admissions catalog must contain a skills object")
    return set(skills)


def validate_ref(value: Any) -> Optional[str]:
    if value in (None, ""):
        return None
    if (
        not isinstance(value, str)
        or len(value) > 200
        or "\\" in value
        or value.startswith("/")
        or re.match(r"^[A-Za-z]:", value)
        or any(part in ("", ".", "..") for part in value.split("/"))
        or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._/-]*", value)
    ):
        raise ValueError("unsafe source ref")
    return value


def export_catalog(lock: dict[str, Any], admitted: set[str]) -> dict[str, Any]:
    if lock.get("version") != 3 or not isinstance(lock.get("skills"), dict):
        raise ValueError("unsupported runtime skill lock")
    exported: list[dict[str, Any]] = []
    for name, raw in sorted(lock["skills"].items()):
        if not isinstance(name, str) or not NAME_PATTERN.fullmatch(name):
            raise ValueError(f"invalid skill name: {name}")
        if not isinstance(raw, dict):
            raise ValueError(f"invalid lock entry: {name}")
        source_type = raw.get("sourceType")
        if source_type not in ALLOWED_SOURCE_TYPES:
            raise ValueError(f"unsupported source type for {name}: {source_type}")
        source_url = normalize_source_url(source_type, raw.get("sourceUrl", ""))
        skill_path = validate_skill_path(raw.get("skillPath"))
        tree_sha = raw.get("skillFolderHash") or None
        if tree_sha is not None and not TREE_SHA_PATTERN.fullmatch(tree_sha):
            raise ValueError(f"invalid tree SHA for {name}")
        if source_type == "well-known" and skill_path is not None:
            raise ValueError(f"well-known source must not include a skill path: {name}")
        if source_type != "well-known" and skill_path is None:
            raise ValueError(f"repository source is missing a skill path: {name}")
        exported.append(
            {
                "name": name,
                "source_type": source_type,
                "source_url": source_url,
                "skill_path": skill_path,
                "tree_sha": tree_sha,
                "ref": validate_ref(raw.get("ref")),
                "delivery": "bundled" if name in admitted else "fetch_from_origin",
            }
        )
    return {
        "schema_version": 1,
        "description": (
            "Public, path-free provenance exported from the maintainer runtime lock. "
            "A source entry is not a redistribution approval."
        ),
        "skills": exported,
    }


def encode(payload: dict[str, Any]) -> str:
    return json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--admissions", type=Path)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--apply", action="store_true")
    mode.add_argument("--check", action="store_true")
    args = parser.parse_args()

    lock = json.loads(args.input.read_text(encoding="utf-8"))
    payload = export_catalog(lock, admitted_skill_names(args.admissions))
    expected = encode(payload)
    if args.check:
        if not args.output.is_file():
            print(f"missing generated runtime source catalog: {args.output}", file=sys.stderr)
            return 2
        if args.output.read_text(encoding="utf-8") != expected:
            print(f"runtime source catalog is stale: {args.output}", file=sys.stderr)
            return 2
        print(f"Runtime source catalog current: {len(payload['skills'])} skills.")
        return 0
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(expected, encoding="utf-8")
    print(f"Exported {len(payload['skills'])} runtime sources to {args.output}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
