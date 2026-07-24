#!/usr/bin/env python3
"""Fail closed when packaged Skills lack redistribution evidence."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit


class AdmissionError(Exception):
    pass


TREE_SHA_PATTERN = re.compile(r"[0-9a-f]{40}")


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise AdmissionError(f"invalid JSON: {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise AdmissionError(f"expected JSON object: {path}")
    return value


def manifest_skills(manifest: dict[str, Any]) -> set[str]:
    packs = manifest.get("skill_packs")
    if not isinstance(packs, dict):
        raise AdmissionError("manifest skill_packs must be an object")
    result: set[str] = set()
    for pack_name, names in packs.items():
        if not isinstance(pack_name, str) or not isinstance(names, list):
            raise AdmissionError("manifest skill_packs contains an invalid pack")
        for name in names:
            if not isinstance(name, str) or not name:
                raise AdmissionError(f"invalid Skill name in pack: {pack_name}")
            if name in result:
                raise AdmissionError(f"Skill appears in more than one pack: {name}")
            result.add(name)
    return result


def full_profile_skills(manifest: dict[str, Any]) -> set[str] | None:
    profiles = manifest.get("profiles")
    packs = manifest.get("skill_packs")
    if not isinstance(profiles, dict) or "full" not in profiles:
        return None
    profile = profiles["full"]
    if not isinstance(profile, dict) or not isinstance(profile.get("skill_packs"), list):
        raise AdmissionError("full profile is invalid")
    result: set[str] = set()
    for pack_name in profile["skill_packs"]:
        if pack_name not in packs:
            raise AdmissionError(f"full profile references unknown pack: {pack_name}")
        result.update(packs[pack_name])
    return result


def check_runtime_sources(root: Path, packaged: set[str]) -> int:
    catalog = load_json(root / "catalog" / "runtime_sources.json")
    if catalog.get("schema_version") != 1 or not isinstance(catalog.get("skills"), list):
        raise AdmissionError("invalid runtime source catalog")
    seen: set[str] = set()
    for entry in catalog["skills"]:
        if not isinstance(entry, dict):
            raise AdmissionError("runtime source entry must be an object")
        name = entry.get("name")
        if not isinstance(name, str) or not name or name in seen:
            raise AdmissionError(f"invalid or duplicate runtime source name: {name}")
        seen.add(name)
        source_type = entry.get("source_type")
        source_url = entry.get("source_url")
        skill_path = entry.get("skill_path")
        tree_sha = entry.get("tree_sha")
        if source_type not in {"git", "github", "well-known"}:
            raise AdmissionError(f"unsupported runtime source type: {name}")
        try:
            parsed_url = urlsplit(source_url) if isinstance(source_url, str) else None
            parsed_port = parsed_url.port if parsed_url is not None else None
        except ValueError:
            parsed_url = None
            parsed_port = None
        if (
            parsed_url is None
            or parsed_url.scheme != "https"
            or not parsed_url.hostname
            or parsed_url.username is not None
            or parsed_url.password is not None
            or parsed_port is not None
            or parsed_url.query
            or parsed_url.fragment
        ):
            raise AdmissionError(f"runtime source is not a public HTTPS URL: {name}")
        ref = entry.get("ref")
        if ref is not None and (
            not isinstance(ref, str)
            or len(ref) > 200
            or "\\" in ref
            or ref.startswith("/")
            or re.match(r"^[A-Za-z]:", ref)
            or any(part in ("", ".", "..") for part in ref.split("/"))
            or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._/-]*", ref)
        ):
            raise AdmissionError(f"unsafe runtime source ref: {name}")
        if tree_sha is not None and (
            not isinstance(tree_sha, str) or not TREE_SHA_PATTERN.fullmatch(tree_sha)
        ):
            raise AdmissionError(f"invalid runtime source tree SHA: {name}")
        if source_type == "well-known":
            if skill_path is not None:
                raise AdmissionError(f"well-known runtime source has a path: {name}")
        elif (
            not isinstance(skill_path, str)
            or "\\" in skill_path
            or re.match(r"^[A-Za-z]:", skill_path)
            or skill_path.startswith("//")
            or Path(skill_path).is_absolute()
            or ".." in Path(skill_path).parts
            or Path(skill_path).name != "SKILL.md"
        ):
            raise AdmissionError(f"unsafe runtime source path: {name}")
        expected_delivery = "bundled" if name in packaged else "fetch_from_origin"
        if entry.get("delivery") != expected_delivery:
            raise AdmissionError(f"stale runtime source delivery status: {name}")
    return len(seen)


def check_runtime_pins(root: Path, expected_names: set[str]) -> None:
    catalog = load_json(root / "catalog" / "runtime_pins.json")
    if (
        catalog.get("schema_version") != 1
        or not isinstance(catalog.get("skills"), list)
        or not isinstance(catalog.get("repositories"), dict)
    ):
        raise AdmissionError("invalid runtime pin catalog")
    seen: set[str] = set()
    allowed_statuses = {
        "current_tree_mismatch",
        "exact_current",
        "live_origin_unpinned",
        "lookup_failed",
        "missing_tree_sha",
    }
    for entry in catalog["skills"]:
        if not isinstance(entry, dict):
            raise AdmissionError("runtime pin entry must be an object")
        name = entry.get("name")
        status = entry.get("status")
        commit = entry.get("commit")
        if not isinstance(name, str) or name in seen or status not in allowed_statuses:
            raise AdmissionError(f"invalid runtime pin entry: {name}")
        seen.add(name)
        if commit is not None and (
            not isinstance(commit, str) or not TREE_SHA_PATTERN.fullmatch(commit)
        ):
            raise AdmissionError(f"invalid runtime pin commit: {name}")
        if (status == "exact_current") != (commit is not None):
            raise AdmissionError(f"runtime pin status/commit mismatch: {name}")
    if seen != expected_names:
        raise AdmissionError("runtime pin names differ from runtime source catalog")
    for repository in catalog["repositories"]:
        if not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", repository):
            raise AdmissionError(f"unsafe runtime pin repository: {repository}")


def check(root: Path, require_full: bool) -> dict[str, int]:
    manifest = load_json(root / "manifest.json")
    admissions = load_json(root / "catalog" / "admissions.json")
    if admissions.get("schema_version") != 1:
        raise AdmissionError("unsupported admissions schema_version")
    groups = admissions.get("provenance_groups")
    skill_records = admissions.get("skills")
    if not isinstance(groups, dict) or not isinstance(skill_records, dict):
        raise AdmissionError("admissions must contain provenance_groups and skills")

    packaged = manifest_skills(manifest)
    runtime_sources = check_runtime_sources(root, packaged)
    runtime_source_names = {
        entry["name"]
        for entry in load_json(root / "catalog" / "runtime_sources.json")["skills"]
    }
    check_runtime_pins(root, runtime_source_names)
    admitted = set(skill_records)
    missing = sorted(packaged - admitted)
    extra = sorted(admitted - packaged)
    if missing:
        raise AdmissionError("packaged Skills missing admission: " + ", ".join(missing))
    if extra:
        raise AdmissionError("admissions reference unpackaged Skills: " + ", ".join(extra))

    for name, group_name in sorted(skill_records.items()):
        if not isinstance(group_name, str) or group_name not in groups:
            raise AdmissionError(f"Skill {name} references unknown provenance group")
        group = groups[group_name]
        if not isinstance(group, dict):
            raise AdmissionError(f"invalid provenance group: {group_name}")
        redistribution = group.get("redistribution")
        if redistribution not in {"approved", "approved_noncommercial"}:
            raise AdmissionError(f"Skill {name} is not approved for redistribution")
        if not isinstance(group.get("license"), str) or not group["license"].strip():
            raise AdmissionError(f"Skill {name} has no license evidence")
        if (
            redistribution == "approved_noncommercial"
            and "NC" not in group["license"].upper()
        ):
            raise AdmissionError(
                f"Skill {name} has a noncommercial approval without an NC license"
            )
        origin = group.get("origin")
        if not isinstance(origin, str) or not origin.strip():
            raise AdmissionError(f"Skill {name} has no provenance origin")
        notice = group.get("notice")
        if notice is not None:
            if not isinstance(notice, str) or Path(notice).is_absolute() or ".." in Path(notice).parts:
                raise AdmissionError(f"unsafe notice path in group: {group_name}")
            if not (root / notice).is_file():
                raise AdmissionError(f"missing notice file in group: {group_name}")
        modifications = group.get("modifications")
        if modifications is not None:
            if (
                not isinstance(modifications, str)
                or Path(modifications).is_absolute()
                or ".." in Path(modifications).parts
            ):
                raise AdmissionError(f"unsafe modifications path in group: {group_name}")
            if not (root / modifications).is_file():
                raise AdmissionError(f"missing modifications file in group: {group_name}")

    full = full_profile_skills(manifest)
    if require_full and full is None:
        raise AdmissionError("release requires a full profile")
    if full is not None and full != admitted:
        missing_from_full = sorted(admitted - full)
        unexpected_in_full = sorted(full - admitted)
        detail = []
        if missing_from_full:
            detail.append("missing=" + ",".join(missing_from_full))
        if unexpected_in_full:
            detail.append("unexpected=" + ",".join(unexpected_in_full))
        raise AdmissionError("full profile does not equal the admitted catalog: " + " ".join(detail))

    return {
        "packaged_skills": len(packaged),
        "provenance_groups": len(groups),
        "full_profile": 1 if full is not None else 0,
        "runtime_sources": runtime_sources,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--require-full", action="store_true")
    args = parser.parse_args()
    try:
        counts = check(args.root.resolve(), args.require_full)
    except AdmissionError as exc:
        print(f"ADMISSION FAILED: {exc}", file=sys.stderr)
        return 2
    print(
        "ADMISSION OK: "
        f"skills={counts['packaged_skills']} "
        f"groups={counts['provenance_groups']} "
        f"runtime_sources={counts['runtime_sources']} "
        f"full={bool(counts['full_profile'])}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
