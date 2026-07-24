#!/usr/bin/env python3
"""Build a path-free public disposition ledger for every local top-level Skill."""

from __future__ import annotations

import argparse
import json
import os
import re
import tempfile
from collections import Counter
from pathlib import Path
from typing import Any, Iterable


class InventoryError(Exception):
    pass


MANUAL_EXCLUSIONS: dict[str, dict[str, str]] = {
    "advisory-board": {
        "status": "license_blocked",
        "reason": (
            "The verified upstream repository states MIT in its README but does "
            "not include the complete license text. Redistribution waits for a "
            "LICENSE file or explicit permission."
        ),
        "origin": "https://github.com/Backtthefuture/huangshu",
    },
    "cc-shield": {
        "status": "safety_blocked",
        "reason": (
            "Contains post-ban identity-link evasion, device-identifier reset, "
            "credential or cache deletion, and unverified platform claims. It is "
            "not safe for a beginner bundle."
        ),
    },
    "cursor-jtbd-review": {
        "status": "superseded",
        "reason": "Replaced by the portable JTBD review workflow.",
        "replacement": "jtbd-review-runner",
    },
    "darwin-skill": {
        "status": "license_blocked",
        "reason": (
            "The verified upstream repository states MIT in its README but does "
            "not include the complete license text. Redistribution waits for a "
            "LICENSE file or explicit permission."
        ),
        "origin": "https://github.com/alchaincyf/darwin-skill",
    },
    "feishu-bitable": {
        "status": "superseded",
        "reason": "Use the official Lark Base Skill fetched from its origin.",
        "replacement": "lark-base",
    },
    "feishu-calendar": {
        "status": "superseded",
        "reason": "Use the official Lark Calendar Skill fetched from its origin.",
        "replacement": "lark-calendar",
    },
    "feishu-channel-rules": {
        "status": "superseded",
        "reason": "Use the official shared Lark conventions fetched from its origin.",
        "replacement": "lark-shared",
    },
    "feishu-create-doc": {
        "status": "superseded",
        "reason": "Use the official Lark document Skill fetched from its origin.",
        "replacement": "lark-doc",
    },
    "feishu-fetch-doc": {
        "status": "superseded",
        "reason": "Use the official Lark document Skill fetched from its origin.",
        "replacement": "lark-doc",
    },
    "feishu-im-read": {
        "status": "superseded",
        "reason": "Use the official Lark messaging Skill fetched from its origin.",
        "replacement": "lark-im",
    },
    "feishu-task": {
        "status": "superseded",
        "reason": "Use the official Lark task Skill fetched from its origin.",
        "replacement": "lark-task",
    },
    "feishu-troubleshoot": {
        "status": "superseded",
        "reason": "Use the official Lark API explorer fetched from its origin.",
        "replacement": "lark-openapi-explorer",
    },
    "feishu-update-doc": {
        "status": "superseded",
        "reason": "Use the official Lark document Skill fetched from its origin.",
        "replacement": "lark-doc",
    },
    "interview-designer": {
        "status": "license_blocked",
        "reason": (
            "The source repository does not include a redistribution license. "
            "Publish only after the owner adds a license or grants permission."
        ),
    },
    "jtbd-amazon-corpus": {
        "status": "superseded",
        "reason": "Replaced by the portable, source-agnostic JTBD research workflow.",
        "replacement": "jtbd-amazon-research",
    },
    "source-command-gsd-join-discord": {
        "status": "platform_internal",
        "reason": (
            "This is a platform-internal command adapter rather than an "
            "independent redistributable Skill."
        ),
    },
    "writing-x-posts": {
        "status": "license_blocked",
        "reason": (
            "The upstream course repository does not provide an open-source "
            "redistribution license."
        ),
        "origin": "https://github.com/jamesgray007/hoai-course",
    },
}


PRIVATE_CODES = {
    "macos_home_path",
    "openai_style_secret_candidate",
    "windows_home_path",
}
LEGACY_CODES = {
    "backup_or_recovery_artifact",
    "duplicate_name",
    "excluded_artifact_directory",
    "folder_name_mismatch",
}
NONPORTABLE_CODES = {
    "binary_asset_review",
    "oversized_file",
}
REDACTED_PRIVATE_PREFIX = "redacted-private-project-"


def parse_source(value: str) -> tuple[str, Path]:
    if "=" not in value:
        raise argparse.ArgumentTypeError("source must use LABEL=PATH")
    label, raw_path = value.split("=", 1)
    if not re.fullmatch(r"[a-z0-9][a-z0-9_-]*", label):
        raise argparse.ArgumentTypeError("invalid source label")
    path = Path(raw_path).expanduser().resolve()
    if not path.is_dir():
        raise argparse.ArgumentTypeError(f"source directory does not exist: {raw_path}")
    return label, path


def read_skill_name(path: Path) -> str:
    text = path.read_text(encoding="utf-8", errors="ignore")[:8000]
    match = re.search(r"(?m)^name:\s*[\"']?([^\n\"']+)", text)
    return match.group(1).strip() if match else path.parent.name


def discover_source_scope(
    sources: Iterable[tuple[str, Path]],
) -> dict[str, Any]:
    occurrences: Counter[str] = Counter()
    properties: dict[str, dict[str, bool]] = {}
    for _, root in sources:
        for skill_file in sorted(root.rglob("SKILL.md")):
            name = read_skill_name(skill_file)
            relative = skill_file.relative_to(root)
            record = properties.setdefault(
                name,
                {
                    "top_level": False,
                    "nested": False,
                    "platform_builtin": False,
                },
            )
            occurrences[name] += 1
            if len(relative.parts) == 2:
                record["top_level"] = True
            elif relative.parts and relative.parts[0] == ".system":
                record["platform_builtin"] = True
            else:
                record["nested"] = True
    return {
        "raw_entry_count": sum(occurrences.values()),
        "duplicate_names": sum(1 for count in occurrences.values() if count > 1),
        "names": properties,
    }


def load_object(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise InventoryError(f"invalid JSON: {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise InventoryError(f"expected JSON object: {path}")
    return value


def bundled_catalog(manifest: dict[str, Any]) -> dict[str, str]:
    packs = manifest.get("skill_packs")
    if manifest.get("schema_version") != 1 or not isinstance(packs, dict):
        raise InventoryError("invalid manifest")
    result: dict[str, str] = {}
    for pack_name, names in packs.items():
        if not isinstance(pack_name, str) or not isinstance(names, list):
            raise InventoryError("invalid manifest Skill pack")
        for name in names:
            if not isinstance(name, str) or name in result:
                raise InventoryError(f"invalid or duplicate bundled Skill: {name}")
            result[name] = pack_name
    return result


def external_catalog(external: dict[str, Any]) -> dict[str, str]:
    packs = external.get("packs")
    if external.get("schema_version") != 1 or not isinstance(packs, dict):
        raise InventoryError("invalid external Skill catalog")
    result: dict[str, str] = {}
    for pack_name, pack in packs.items():
        if not isinstance(pack_name, str) or not isinstance(pack, dict):
            raise InventoryError("invalid external Skill pack")
        entries = pack.get("skills")
        if not isinstance(entries, list):
            raise InventoryError("invalid external Skill pack entries")
        for entry in entries:
            name = entry.get("name") if isinstance(entry, dict) else None
            if not isinstance(name, str) or name in result:
                raise InventoryError(f"invalid or duplicate external Skill: {name}")
            result[name] = pack_name
    return result


def classify_blocked(name: str, record: dict[str, Any]) -> dict[str, str]:
    codes = {
        code
        for code in record.get("blocker_codes", [])
        if isinstance(code, str)
    }
    if name == "xlsx":
        return {
            "status": "license_restricted",
            "reason": (
                "The source license explicitly prohibits third-party "
                "redistribution."
            ),
        }
    if any(code.startswith("private_term_") for code in codes) or codes & PRIVATE_CODES:
        return {
            "status": "private_project",
            "reason": (
                "Contains private-project names, local paths, or secret-like "
                "material and is not part of the public kit."
            ),
        }
    if codes & LEGACY_CODES:
        return {
            "status": "legacy_or_duplicate",
            "reason": (
                "The local entry is a duplicate, recovery artifact, mismatched "
                "folder, or other non-canonical copy."
            ),
        }
    if codes & NONPORTABLE_CODES:
        return {
            "status": "nonportable_artifact",
            "reason": (
                "Contains oversized or binary artifacts that are not suitable for "
                "the portable source bundle."
            ),
        }
    return {
        "status": "technical_block",
        "reason": (
            "The local entry did not pass the portable release gate and no safe "
            "redistributable version is available."
        ),
    }


def build_inventory(
    source: dict[str, Any],
    manifest: dict[str, Any],
    external: dict[str, Any],
    source_scope: dict[str, Any] | None = None,
) -> dict[str, Any]:
    source_skills = source.get("skills")
    if source.get("schema_version") != 1 or not isinstance(source_skills, dict):
        raise InventoryError("invalid private source inventory")
    bundled = bundled_catalog(manifest)
    fetched = external_catalog(external)
    overlap = set(bundled) & set(fetched)
    if overlap:
        raise InventoryError(
            "Skill cannot be bundled and fetched: " + ", ".join(sorted(overlap))
        )

    if source_scope is None:
        scope_names = {
            name: {
                "top_level": True,
                "nested": False,
                "platform_builtin": False,
            }
            for name in source_skills
        }
        raw_entry_count = len(scope_names)
        duplicate_names = 0
    else:
        scope_names = source_scope.get("names")
        raw_entry_count = source_scope.get("raw_entry_count")
        duplicate_names = source_scope.get("duplicate_names")
        if (
            not isinstance(scope_names, dict)
            or not isinstance(raw_entry_count, int)
            or not isinstance(duplicate_names, int)
        ):
            raise InventoryError("invalid recursive source scope")
        discovered_top_level = {
            name
            for name, record in scope_names.items()
            if isinstance(record, dict) and record.get("top_level")
        }
        if discovered_top_level != set(source_skills):
            missing = sorted(set(source_skills) - discovered_top_level)
            added = sorted(discovered_top_level - set(source_skills))
            raise InventoryError(
                "top-level source scope differs from private inventory: "
                f"missing={missing} added={added}"
            )

    skills: dict[str, dict[str, str]] = {}
    redacted_private_projects = 0
    for name, source_record in sorted(source_skills.items()):
        if not isinstance(name, str) or not isinstance(source_record, dict):
            raise InventoryError("invalid source Skill record")
        if name in bundled:
            skills[name] = {
                "scope": "top_level",
                "delivery": "bundled",
                "pack": bundled[name],
            }
            continue
        if name in fetched:
            skills[name] = {
                "scope": "top_level",
                "delivery": "fetch_from_origin",
                "pack": fetched[name],
            }
            continue
        if name in MANUAL_EXCLUSIONS:
            skills[name] = {
                "scope": "top_level",
                "delivery": "not_distributed",
                **MANUAL_EXCLUSIONS[name],
            }
            continue
        disposition = source_record.get("disposition")
        old_status = disposition.get("status") if isinstance(disposition, dict) else None
        if old_status != "blocked":
            raise InventoryError(
                f"unresolved local Skill needs an explicit disposition: {name}"
            )
        blocked = classify_blocked(name, source_record)
        public_name = name
        if blocked["status"] == "private_project":
            redacted_private_projects += 1
            public_name = (
                f"{REDACTED_PRIVATE_PREFIX}{redacted_private_projects:03d}"
            )
            if public_name in source_skills or public_name in bundled or public_name in fetched:
                raise InventoryError(
                    f"reserved redacted private-project name is already used: {public_name}"
                )
        skills[public_name] = {
            "scope": "top_level",
            "delivery": "not_distributed",
            **blocked,
        }

    for name, scope_record in sorted(scope_names.items()):
        if name in source_skills:
            continue
        if not isinstance(scope_record, dict):
            raise InventoryError(f"invalid source scope record: {name}")
        if scope_record.get("platform_builtin") and not scope_record.get("nested"):
            skills[name] = {
                "scope": "platform_builtin",
                "delivery": "not_distributed",
                "status": "platform_builtin",
                "reason": (
                    "Provided by the local AI platform runtime. The kit does not "
                    "copy or claim ownership of platform-built-in Skills."
                ),
            }
        elif scope_record.get("nested"):
            if name in bundled:
                skills[name] = {
                    "scope": "nested_promoted",
                    "delivery": "bundled",
                    "pack": bundled[name],
                }
            elif name in fetched:
                skills[name] = {
                    "scope": "nested_promoted",
                    "delivery": "fetch_from_origin",
                    "pack": fetched[name],
                }
            else:
                skills[name] = {
                    "scope": "nested_component",
                    "delivery": "not_distributed",
                    "status": "nested_component",
                    "reason": (
                        "Discovered only inside another Skill package as an "
                        "example or sub-workflow, not as an independent top-level "
                        "release source."
                    ),
                }
        else:
            raise InventoryError(f"unclassified non-top-level Skill: {name}")

    counts = Counter(record["delivery"] for record in skills.values())
    scope_counts = Counter(record["scope"] for record in skills.values())
    catalog_only = sorted(set(bundled) - set(source_skills))
    catalog_only = sorted(set(catalog_only) - set(skills))
    external_only = sorted(set(fetched) - set(skills))
    return {
        "schema_version": 1,
        "description": (
            "Path-free release disposition for every unique Skill found in the "
            "maintainer's three local source trees. Private-project names are "
            "replaced by anonymous entries. No entry remains pending review."
        ),
        "summary": {
            "raw_source_entry_count": raw_entry_count,
            "raw_source_unique_count": len(skills),
            "raw_duplicate_names": duplicate_names,
            "top_level_unique_count": scope_counts["top_level"],
            "nested_only_unique_count": (
                scope_counts["nested_promoted"] + scope_counts["nested_component"]
            ),
            "platform_builtin_only_unique_count": scope_counts["platform_builtin"],
            "bundled_from_source_scope": counts["bundled"],
            "fetch_from_origin": counts["fetch_from_origin"],
            "not_distributed": counts["not_distributed"],
            "catalog_only_bundled": len(catalog_only),
            "catalog_only_external": len(external_only),
            "public_bundled_total": len(bundled),
            "external_fetch_total": len(fetched),
            "redacted_private_projects": redacted_private_projects,
        },
        "catalog_only_bundled_skills": catalog_only,
        "catalog_only_external_skills": external_only,
        "skills": skills,
    }


def atomic_write(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(dir=path.parent, prefix=f".{path.name}.")
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            json.dump(payload, handle, ensure_ascii=False, indent=2, sort_keys=True)
            handle.write("\n")
        os.replace(temporary, path)
    except BaseException:
        try:
            os.unlink(temporary)
        except OSError:
            pass
        raise


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-inventory", required=True, type=Path)
    parser.add_argument("--manifest", required=True, type=Path)
    parser.add_argument("--external", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument(
        "--source",
        action="append",
        required=True,
        type=parse_source,
        metavar="LABEL=PATH",
        help="original Skill source root used to account for nested and platform entries",
    )
    args = parser.parse_args()
    try:
        inventory = build_inventory(
            load_object(args.source_inventory),
            load_object(args.manifest),
            load_object(args.external),
            discover_source_scope(args.source),
        )
        atomic_write(args.output, inventory)
        summary = inventory["summary"]
        print(
            "LOCAL RELEASE INVENTORY OK: "
            f"source={summary['raw_source_unique_count']} "
            f"bundled={summary['bundled_from_source_scope']} "
            f"external={summary['fetch_from_origin']} "
            f"not_distributed={summary['not_distributed']}"
        )
    except (InventoryError, OSError, TypeError, KeyError) as exc:
        print(f"LOCAL RELEASE INVENTORY FAILED: {exc}", file=os.sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
