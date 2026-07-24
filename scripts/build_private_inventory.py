#!/usr/bin/env python3
"""Build a private, Git-ignored disposition ledger from a detailed Skill audit."""

from __future__ import annotations

import argparse
import json
import os
import sys
import tempfile
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


SOURCE_PRIORITY = {
    "cursor-vault": 0,
    "agents-global": 1,
    "codex-global": 2,
}


class InventoryError(Exception):
    pass


def load_object(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise InventoryError(f"invalid JSON: {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise InventoryError(f"expected JSON object: {path}")
    return value


def manifest_catalog(manifest: dict[str, Any]) -> tuple[dict[str, str], set[str]]:
    packs = manifest.get("skill_packs")
    profiles = manifest.get("profiles")
    if not isinstance(packs, dict) or not isinstance(profiles, dict):
        raise InventoryError("invalid manifest")
    pack_by_skill: dict[str, str] = {}
    for pack, names in packs.items():
        if not isinstance(pack, str) or not isinstance(names, list):
            raise InventoryError("invalid manifest Skill pack")
        for name in names:
            if not isinstance(name, str) or name in pack_by_skill:
                raise InventoryError(f"invalid or duplicate manifest Skill: {name}")
            pack_by_skill[name] = pack
    daily = profiles.get("daily-work", {}).get("skill_packs", [])
    default_skills: set[str] = set()
    for pack in daily:
        if pack not in packs:
            raise InventoryError(f"daily-work references unknown pack: {pack}")
        default_skills.update(packs[pack])
    return pack_by_skill, default_skills


def selected_entries(audit: dict[str, Any]) -> dict[str, dict[str, Any]]:
    if (
        audit.get("schema_version") != 1
        or audit.get("sensitivity") != "private_intake"
        or audit.get("entry_mode") != "top-level"
        or not isinstance(audit.get("entries"), list)
    ):
        raise InventoryError("input must be a schema v1 private top-level audit")
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for entry in audit["entries"]:
        if not isinstance(entry, dict) or not isinstance(entry.get("name"), str):
            raise InventoryError("invalid audit entry")
        grouped[entry["name"]].append(entry)
    return {
        name: sorted(
            candidates,
            key=lambda item: (
                SOURCE_PRIORITY.get(item.get("source"), 99),
                item.get("path", ""),
            ),
        )[0]
        for name, candidates in grouped.items()
    }


def external_catalog(
    external: dict[str, Any] | None,
) -> dict[str, dict[str, str]]:
    if external is None:
        return {}
    packs = external.get("packs")
    if external.get("schema_version") != 1 or not isinstance(packs, dict):
        raise InventoryError("invalid external Skill catalog")
    result: dict[str, dict[str, str]] = {}
    for pack_name, pack in packs.items():
        if (
            not isinstance(pack_name, str)
            or not isinstance(pack, dict)
            or not isinstance(pack.get("skills"), list)
        ):
            raise InventoryError("invalid external Skill pack")
        for entry in pack["skills"]:
            if (
                not isinstance(entry, dict)
                or not isinstance(entry.get("name"), str)
                or not isinstance(entry.get("url"), str)
                or entry["name"] in result
            ):
                raise InventoryError("invalid or duplicate external Skill")
            result[entry["name"]] = {
                "pack": pack_name,
                "origin": entry["url"],
            }
    return result


def build_ledger(
    audit: dict[str, Any],
    admissions: dict[str, Any],
    manifest: dict[str, Any],
    previous: dict[str, Any] | None = None,
    external: dict[str, Any] | None = None,
) -> dict[str, Any]:
    selected = selected_entries(audit)
    groups = admissions.get("provenance_groups")
    admitted = admissions.get("skills")
    if not isinstance(groups, dict) or not isinstance(admitted, dict):
        raise InventoryError("invalid admissions catalog")
    pack_by_skill, default_skills = manifest_catalog(manifest)
    external_by_skill = external_catalog(external)
    overlap = set(admitted) & set(external_by_skill)
    if overlap:
        raise InventoryError(
            "Skill cannot be both bundled and external: " + ", ".join(sorted(overlap))
        )
    previous_skills = previous.get("skills", {}) if isinstance(previous, dict) else {}
    duplicate_counts = Counter(entry["name"] for entry in audit["entries"])
    skills: dict[str, Any] = {}
    for name, entry in sorted(selected.items()):
        group_name = admitted.get(name)
        group = groups.get(group_name) if isinstance(group_name, str) else None
        external_record = external_by_skill.get(name)
        if group_name is not None and not isinstance(group, dict):
            raise InventoryError(f"Skill references invalid provenance group: {name}")
        prior = previous_skills.get(name, {})
        decision = prior.get("decision", {}) if isinstance(prior, dict) else {}
        decision_status = decision.get("status")
        if decision_status not in (None, "blocked", "review"):
            raise InventoryError(f"invalid manual disposition status: {name}")
        status = (
            "bundled"
            if group_name is not None
            else (
                "fetch_from_origin"
                if external_record is not None
                else (
                    decision_status
                    or ("blocked" if entry.get("technical_status") == "blocked" else "review")
                )
            )
        )
        skills[name] = {
            "selected_source": entry.get("source"),
            "selected_path": entry.get("path"),
            "content_sha256": entry.get("content_sha256"),
            "duplicate_candidates": duplicate_counts[name],
            "technical_status": entry.get("technical_status"),
            "blocker_codes": sorted(
                {
                    issue.get("code")
                    for issue in entry.get("blockers", [])
                    if isinstance(issue, dict) and isinstance(issue.get("code"), str)
                }
            ),
            "review_codes": sorted(
                {
                    issue.get("code")
                    for issue in entry.get("reviews", [])
                    if isinstance(issue, dict) and isinstance(issue.get("code"), str)
                }
            ),
            "commands": entry.get("dependencies", {}).get("commands", []),
            "environment": entry.get("dependencies", {}).get("environment", []),
            "side_effects": entry.get("side_effects", []),
            "decision": {
                "status": decision_status,
                "os_requirements": decision.get("os_requirements", []),
                "notes": decision.get("notes"),
            },
            "disposition": {
                "status": status,
                "delivery": (
                    "bundled"
                    if group_name is not None
                    else ("fetch_from_origin" if external_record is not None else None)
                ),
                "category": (
                    pack_by_skill.get(name)
                    if group_name is not None
                    else (external_record.get("pack") if external_record else None)
                ),
                "default_install": name in default_skills,
                "provenance_group": group_name,
                "origin": (
                    group.get("origin")
                    if group
                    else (external_record.get("origin") if external_record else None)
                ),
                "license": group.get("license") if group else None,
                "os_requirements": decision.get("os_requirements", []),
                "notes": decision.get("notes"),
            },
        }
    catalog_only = sorted(set(admitted) - set(selected))
    external_only = sorted(set(external_by_skill) - set(selected))
    counts = Counter(item["disposition"]["status"] for item in skills.values())
    return {
        "schema_version": 1,
        "sensitivity": "private_do_not_publish",
        "description": (
            "Local disposition ledger. It may contain private Skill names and paths "
            "and is intentionally excluded from Git."
        ),
        "summary": {
            "audit_entries": len(audit["entries"]),
            "unique_top_level_skills": len(skills),
            "duplicate_names": sum(1 for count in duplicate_counts.values() if count > 1),
            "bundled_from_inventory": counts["bundled"],
            "fetch_from_origin": counts["fetch_from_origin"],
            "blocked": counts["blocked"],
            "review": counts["review"],
            "catalog_only_skills": len(catalog_only),
            "external_catalog_only_skills": len(external_only),
        },
        "catalog_only_skills": catalog_only,
        "external_catalog_only_skills": external_only,
        "skills": skills,
    }


def atomic_private_write(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(dir=path.parent, prefix=f".{path.name}.")
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            json.dump(payload, handle, ensure_ascii=False, indent=2, sort_keys=True)
            handle.write("\n")
        os.chmod(temporary, 0o600)
        os.replace(temporary, path)
    except BaseException:
        try:
            os.unlink(temporary)
        except OSError:
            pass
        raise


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--audit", required=True, type=Path)
    parser.add_argument("--admissions", required=True, type=Path)
    parser.add_argument("--external-catalog", required=True, type=Path)
    parser.add_argument("--manifest", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    try:
        previous = load_object(args.output) if args.output.exists() else None
        ledger = build_ledger(
            load_object(args.audit),
            load_object(args.admissions),
            load_object(args.manifest),
            previous,
            load_object(args.external_catalog),
        )
        atomic_private_write(args.output, ledger)
        summary = ledger["summary"]
        print(
            "PRIVATE INVENTORY OK: "
            f"unique={summary['unique_top_level_skills']} "
            f"bundled={summary['bundled_from_inventory']} "
            f"external={summary['fetch_from_origin']} "
            f"review={summary['review']} blocked={summary['blocked']}"
        )
    except (InventoryError, OSError, TypeError, KeyError) as exc:
        print(f"PRIVATE INVENTORY FAILED: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
