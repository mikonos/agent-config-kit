#!/usr/bin/env python3
"""Build or verify the unified metadata catalog for every bundled Skill."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import tempfile
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "catalog" / "skill_catalog.json"
OS_REQUIREMENTS_BY_PACK = {
    "macos-integrations": ["macOS"],
}
SIDE_EFFECT_PATTERNS = {
    "deletion": re.compile(r"\brm\s+-rf\b|\bunlink\b|\bdelete\b|删除", re.IGNORECASE),
    "deployment_or_publish": re.compile(
        r"\bdeploy(?:ment)?\b|\bpublish\b|部署|发布",
        re.IGNORECASE,
    ),
    "external_message": re.compile(
        r"\bsend(?:ing)?\s+(?:an?\s+)?(?:email|message)\b|发消息|发送邮件",
        re.IGNORECASE,
    ),
    "payment": re.compile(r"\bpayment\b|\bcharge\b|付款|支付", re.IGNORECASE),
    "repository_change": re.compile(
        r"\bgit\s+(?:commit|tag|push)\b"
        r"|\b(?:commit|tag|push)(?:s|es|ed|ing)?\b"
        r"|\b(?:create|open|update|merge)(?:s|d|ing)?\s+"
        r"(?:a\s+)?(?:branch|issue|pull request|release)\b",
        re.IGNORECASE,
    ),
}


class CatalogError(Exception):
    pass


def load_object(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise CatalogError(f"invalid JSON: {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise CatalogError(f"expected JSON object: {path}")
    return value


def source_attribution(origin: str) -> str:
    if origin == "this-repository":
        return "Agent Config Kit contributors"
    parsed = urlparse(origin)
    parts = [part for part in parsed.path.split("/") if part]
    if parsed.netloc.lower() == "github.com" and len(parts) >= 2:
        return f"{parts[0]}/{parts[1]} contributors"
    return parsed.netloc or origin


def scan_side_effects(skill_dir: Path) -> list[str]:
    signals: set[str] = set()
    for path in sorted(skill_dir.rglob("*")):
        if (
            skill_dir.name == "all-skills-router"
            and path.relative_to(skill_dir).as_posix()
            == "references/skill-index.json"
        ):
            continue
        if not path.is_file() or path.is_symlink() or path.stat().st_size > 2_000_000:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        for label, pattern in SIDE_EFFECT_PATTERNS.items():
            if pattern.search(text):
                signals.add(label)
    return sorted(signals)


def capability_index(
    manifest: dict[str, Any],
) -> dict[str, dict[str, list[dict[str, Any]]]]:
    result: dict[str, dict[str, list[dict[str, Any]]]] = defaultdict(
        lambda: {
            "commands": [],
            "environment": [],
            "connections": [],
        }
    )
    for pack_name, requirements in manifest["capability_requirements"].items():
        for requirement in requirements:
            for skill_name in requirement["used_by"]:
                if skill_name not in manifest["skill_packs"][pack_name]:
                    raise CatalogError(
                        f"capability references a Skill outside its pack: {skill_name}"
                    )
                if "environment" in requirement:
                    result[skill_name]["environment"].append(
                        {
                            "name": requirement["environment"],
                            "required": requirement["required"],
                        }
                    )
                elif "connection" in requirement:
                    result[skill_name]["connections"].append(
                        {
                            "id": requirement["connection"],
                            "label": requirement["label"],
                            "required": requirement["required"],
                            "verification": "runtime_or_user_check",
                        }
                    )
                else:
                    candidates = (
                        [requirement["command"]]
                        if "command" in requirement
                        else requirement["commands"]
                    )
                    result[skill_name]["commands"].append(
                        {
                            "alternatives": candidates,
                            "required": requirement["required"],
                        }
                    )
    return result


def build_catalog(root: Path = ROOT) -> dict[str, Any]:
    manifest = load_object(root / "manifest.json")
    admissions = load_object(root / "catalog" / "admissions.json")
    packs = manifest.get("skill_packs")
    profiles = manifest.get("profiles")
    requirements = manifest.get("capability_requirements")
    admitted = admissions.get("skills")
    groups = admissions.get("provenance_groups")
    if (
        manifest.get("schema_version") != 1
        or admissions.get("schema_version") != 1
        or not isinstance(packs, dict)
        or not isinstance(profiles, dict)
        or not isinstance(requirements, dict)
        or not isinstance(admitted, dict)
        or not isinstance(groups, dict)
    ):
        raise CatalogError("invalid manifest or admissions catalog")

    by_skill = capability_index(manifest)
    profiles_by_skill: dict[str, list[str]] = defaultdict(list)
    for profile_name, profile in profiles.items():
        for pack_name in profile["skill_packs"]:
            for skill_name in packs[pack_name]:
                profiles_by_skill[skill_name].append(profile_name)

    skills: dict[str, dict[str, Any]] = {}
    for pack_name, names in packs.items():
        for name in names:
            if name in skills:
                raise CatalogError(f"duplicate bundled Skill: {name}")
            group_name = admitted.get(name)
            group = groups.get(group_name)
            if not isinstance(group_name, str) or not isinstance(group, dict):
                raise CatalogError(f"missing admission metadata: {name}")
            origin = group.get("origin")
            license_name = group.get("license")
            if not isinstance(origin, str) or not isinstance(license_name, str):
                raise CatalogError(f"incomplete provenance metadata: {name}")
            relative_dir = Path("packs") / pack_name / "skills" / name
            skill_dir = root / relative_dir
            if not (skill_dir / "SKILL.md").is_file():
                raise CatalogError(f"missing packaged Skill: {name}")
            dependencies = by_skill[name]
            for values in dependencies.values():
                values.sort(key=lambda value: json.dumps(value, sort_keys=True))
            skills[name] = {
                "pack": pack_name,
                "packaged_path": relative_dir.as_posix(),
                "profiles": sorted(profiles_by_skill[name]),
                "default_install": "daily-work" in profiles_by_skill[name],
                "source": {
                    "provenance_group": group_name,
                    "origin": origin,
                    "attribution": source_attribution(origin),
                    "license": license_name,
                },
                "os_requirements": OS_REQUIREMENTS_BY_PACK.get(pack_name, []),
                "dependencies": dependencies,
                "side_effects": scan_side_effects(skill_dir),
            }

    side_effect_counts = Counter(
        effect for record in skills.values() for effect in record["side_effects"]
    )
    return {
        "schema_version": 1,
        "description": (
            "Unified metadata for bundled Skills. Side-effect fields are "
            "conservative text-review signals, not permission grants or proof that "
            "an action will occur."
        ),
        "summary": {
            "bundled_skills": len(skills),
            "packs": len(packs),
            "default_install_skills": sum(
                1 for record in skills.values() if record["default_install"]
            ),
            "skills_with_explicit_os_requirements": sum(
                1 for record in skills.values() if record["os_requirements"]
            ),
            "declared_command_requirements": sum(
                len(record["dependencies"]["commands"]) for record in skills.values()
            ),
            "declared_environment_requirements": sum(
                len(record["dependencies"]["environment"]) for record in skills.values()
            ),
            "declared_connection_requirements": sum(
                len(record["dependencies"]["connections"]) for record in skills.values()
            ),
            "side_effect_signal_counts": dict(sorted(side_effect_counts.items())),
        },
        "skills": dict(sorted(skills.items())),
    }


def encoded(payload: dict[str, Any]) -> str:
    return json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def atomic_write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(dir=path.parent, prefix=f".{path.name}.")
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            handle.write(text)
        os.replace(temporary, path)
    except BaseException:
        try:
            os.unlink(temporary)
        except OSError:
            pass
        raise


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--output", type=Path)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    args = parser.parse_args()
    output = args.output or args.root / "catalog" / "skill_catalog.json"
    try:
        payload = build_catalog(args.root)
        expected = encoded(payload)
        if args.check:
            try:
                actual = output.read_text(encoding="utf-8")
            except OSError as exc:
                raise CatalogError(f"missing Skill catalog: {output}") from exc
            if actual != expected:
                raise CatalogError("Skill catalog is stale; run with --write")
        else:
            atomic_write(output, expected)
    except (CatalogError, OSError, KeyError, TypeError) as exc:
        print(f"SKILL CATALOG FAILED: {exc}", file=sys.stderr)
        return 2
    print(
        "SKILL CATALOG OK: "
        f"skills={payload['summary']['bundled_skills']} "
        f"packs={payload['summary']['packs']} "
        f"connections={payload['summary']['declared_connection_requirements']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
