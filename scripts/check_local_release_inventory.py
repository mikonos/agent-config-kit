#!/usr/bin/env python3
"""Verify the public local-Skill release disposition ledger."""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any


ALLOWED_DELIVERIES = {"bundled", "fetch_from_origin", "not_distributed"}
ALLOWED_STATUSES = {
    "legacy_or_duplicate",
    "license_blocked",
    "license_restricted",
    "nonportable_artifact",
    "nested_component",
    "platform_internal",
    "platform_builtin",
    "private_project",
    "safety_blocked",
    "superseded",
    "technical_block",
}
ALLOWED_SCOPES = {
    "nested_component",
    "nested_promoted",
    "platform_builtin",
    "top_level",
}
FORBIDDEN_FIELDS = {
    "blocker_codes",
    "commands",
    "content_sha256",
    "environment",
    "path",
    "review_codes",
    "selected_path",
    "selected_source",
    "side_effects",
}
REDACTED_PRIVATE_PREFIX = "redacted-private-project-"
REDACTED_PRIVATE_NAME = re.compile(
    rf"{re.escape(REDACTED_PRIVATE_PREFIX)}[0-9]{{3}}"
)


class CheckError(Exception):
    pass


def load_object(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise CheckError(f"invalid JSON: {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise CheckError(f"expected JSON object: {path}")
    return value


def bundled_catalog(manifest: dict[str, Any]) -> dict[str, str]:
    packs = manifest.get("skill_packs")
    if manifest.get("schema_version") != 1 or not isinstance(packs, dict):
        raise CheckError("invalid manifest")
    result: dict[str, str] = {}
    for pack_name, names in packs.items():
        if not isinstance(pack_name, str) or not isinstance(names, list):
            raise CheckError("invalid manifest Skill pack")
        for name in names:
            if not isinstance(name, str) or name in result:
                raise CheckError(f"invalid or duplicate bundled Skill: {name}")
            result[name] = pack_name
    return result


def external_catalog(external: dict[str, Any]) -> dict[str, str]:
    packs = external.get("packs")
    if external.get("schema_version") != 1 or not isinstance(packs, dict):
        raise CheckError("invalid external Skill catalog")
    result: dict[str, str] = {}
    for pack_name, pack in packs.items():
        entries = pack.get("skills") if isinstance(pack, dict) else None
        if not isinstance(pack_name, str) or not isinstance(entries, list):
            raise CheckError("invalid external Skill pack")
        for entry in entries:
            name = entry.get("name") if isinstance(entry, dict) else None
            if not isinstance(name, str) or name in result:
                raise CheckError(f"invalid or duplicate external Skill: {name}")
            result[name] = pack_name
    return result


def verify_inventory(
    inventory: dict[str, Any],
    manifest: dict[str, Any],
    external: dict[str, Any],
) -> dict[str, int]:
    if inventory.get("schema_version") != 1:
        raise CheckError("invalid local release inventory schema")
    skills = inventory.get("skills")
    summary = inventory.get("summary")
    catalog_only_bundled = inventory.get("catalog_only_bundled_skills")
    catalog_only_external = inventory.get("catalog_only_external_skills")
    if (
        not isinstance(skills, dict)
        or not isinstance(summary, dict)
        or not isinstance(catalog_only_bundled, list)
        or not isinstance(catalog_only_external, list)
    ):
        raise CheckError("invalid local release inventory structure")

    bundled = bundled_catalog(manifest)
    fetched = external_catalog(external)
    if set(bundled) & set(fetched):
        raise CheckError("bundled and external Skill catalogs overlap")

    counts: Counter[str] = Counter()
    scope_counts: Counter[str] = Counter()
    source_bundled: set[str] = set()
    source_fetched: set[str] = set()
    redacted_private_names: list[str] = []
    for name, record in skills.items():
        if not isinstance(name, str) or not isinstance(record, dict):
            raise CheckError("invalid local Skill disposition")
        forbidden = FORBIDDEN_FIELDS & set(record)
        if forbidden:
            raise CheckError(
                f"private fields leaked for {name}: {', '.join(sorted(forbidden))}"
            )
        delivery = record.get("delivery")
        scope = record.get("scope")
        if scope not in ALLOWED_SCOPES:
            raise CheckError(f"invalid source scope for {name}: {scope}")
        if delivery not in ALLOWED_DELIVERIES:
            raise CheckError(f"unresolved or invalid delivery for {name}: {delivery}")
        counts[delivery] += 1
        scope_counts[scope] += 1
        if scope == "nested_promoted" and delivery == "not_distributed":
            raise CheckError(f"nested promoted Skill is not delivered: {name}")
        if scope == "nested_component" and (
            delivery != "not_distributed"
            or record.get("status") != "nested_component"
        ):
            raise CheckError(f"invalid nested component disposition: {name}")
        if scope == "platform_builtin" and (
            delivery != "not_distributed"
            or record.get("status") != "platform_builtin"
        ):
            raise CheckError(f"invalid platform built-in disposition: {name}")
        if delivery == "bundled":
            if set(record) != {"scope", "delivery", "pack"}:
                raise CheckError(f"invalid bundled disposition fields: {name}")
            if bundled.get(name) != record.get("pack"):
                raise CheckError(f"bundled disposition differs from manifest: {name}")
            source_bundled.add(name)
        elif delivery == "fetch_from_origin":
            if set(record) != {"scope", "delivery", "pack"}:
                raise CheckError(f"invalid external disposition fields: {name}")
            if fetched.get(name) != record.get("pack"):
                raise CheckError(
                    f"external disposition differs from external catalog: {name}"
                )
            source_fetched.add(name)
        else:
            required = {"delivery", "status", "reason"}
            if not required <= set(record):
                raise CheckError(f"incomplete not-distributed disposition: {name}")
            if record.get("status") not in ALLOWED_STATUSES:
                raise CheckError(f"invalid not-distributed status: {name}")
            if record.get("status") == "private_project":
                if REDACTED_PRIVATE_NAME.fullmatch(name) is None:
                    raise CheckError(
                        f"private-project name is not redacted: {name}"
                    )
                redacted_private_names.append(name)
            elif name.startswith(REDACTED_PRIVATE_PREFIX):
                raise CheckError(
                    f"reserved redacted private-project name has wrong status: {name}"
                )
            if not isinstance(record.get("reason"), str) or not record["reason"].strip():
                raise CheckError(f"missing not-distributed reason: {name}")
            replacement = record.get("replacement")
            if replacement is not None:
                if (
                    record.get("status") != "superseded"
                    or not isinstance(replacement, str)
                    or replacement not in bundled
                    and replacement not in fetched
                ):
                    raise CheckError(f"invalid replacement: {name}")
            if set(record) - {
                "scope",
                "delivery",
                "origin",
                "reason",
                "replacement",
                "status",
            }:
                raise CheckError(f"unexpected not-distributed fields: {name}")

    expected_redacted_names = [
        f"{REDACTED_PRIVATE_PREFIX}{index:03d}"
        for index in range(1, len(redacted_private_names) + 1)
    ]
    if sorted(redacted_private_names) != expected_redacted_names:
        raise CheckError("redacted private-project entries are not consecutive")

    expected_catalog_only_bundled = sorted(set(bundled) - source_bundled)
    expected_catalog_only_external = sorted(set(fetched) - source_fetched)
    if catalog_only_bundled != expected_catalog_only_bundled:
        raise CheckError("catalog-only bundled Skill list differs from manifest")
    if catalog_only_external != expected_catalog_only_external:
        raise CheckError("catalog-only external Skill list differs from catalog")

    expected_summary = {
        "raw_source_entry_count": summary.get("raw_source_entry_count"),
        "raw_source_unique_count": len(skills),
        "raw_duplicate_names": summary.get("raw_duplicate_names"),
        "top_level_unique_count": scope_counts["top_level"],
        "nested_only_unique_count": (
            scope_counts["nested_promoted"] + scope_counts["nested_component"]
        ),
        "platform_builtin_only_unique_count": scope_counts["platform_builtin"],
        "bundled_from_source_scope": counts["bundled"],
        "fetch_from_origin": counts["fetch_from_origin"],
        "not_distributed": counts["not_distributed"],
        "catalog_only_bundled": len(expected_catalog_only_bundled),
        "catalog_only_external": len(expected_catalog_only_external),
        "public_bundled_total": len(bundled),
        "external_fetch_total": len(fetched),
        "redacted_private_projects": len(redacted_private_names),
    }
    if summary != expected_summary:
        raise CheckError("local release inventory summary is stale")
    if (
        not isinstance(summary["raw_source_entry_count"], int)
        or summary["raw_source_entry_count"] < len(skills)
        or not isinstance(summary["raw_duplicate_names"], int)
        or summary["raw_duplicate_names"] < 0
    ):
        raise CheckError("invalid raw source counts")
    if sum(counts.values()) != len(skills):
        raise CheckError("local release inventory count mismatch")
    return expected_summary


def main() -> int:
    root_default = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=root_default)
    args = parser.parse_args()
    try:
        summary = verify_inventory(
            load_object(args.root / "catalog" / "local_release_inventory.json"),
            load_object(args.root / "manifest.json"),
            load_object(args.root / "catalog" / "external_skills.json"),
        )
    except (CheckError, OSError, TypeError, KeyError) as exc:
        print(f"LOCAL RELEASE INVENTORY FAILED: {exc}", file=sys.stderr)
        return 2
    print(
        "LOCAL RELEASE INVENTORY OK: "
        f"source={summary['raw_source_unique_count']} "
        f"bundled={summary['bundled_from_source_scope']} "
        f"external={summary['fetch_from_origin']} "
        f"not_distributed={summary['not_distributed']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
