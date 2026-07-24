#!/usr/bin/env python3
"""Refresh current-source snapshots and portable transformation records."""

from __future__ import annotations

import argparse
import json
import os
import sys
import tempfile
from collections import Counter
from pathlib import Path
from typing import Any

import plan_portable_migration as planner


ROOT = Path(__file__).resolve().parents[1]
SNAPSHOT_PATH = ROOT / "catalog" / "maintainer_source_snapshot.json"
PATCH_PATH = ROOT / "catalog" / "portable_patches.json"
PRIVATE_OMISSIONS_PATH = (
    ROOT
    / ".agent-config-kit-workbench"
    / "private-portable-omissions.json"
)


class RefreshError(Exception):
    pass


def encoded(value: dict[str, Any]) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


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


def refresh(
    *,
    plan: dict[str, Any],
    current_catalog: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    operations = plan.get("operations")
    omissions = plan.get("omissions")
    current_patches = current_catalog.get("patches")
    if (
        not isinstance(operations, dict)
        or not isinstance(omissions, list)
        or current_catalog.get("schema_version") != 1
        or not isinstance(current_patches, list)
    ):
        raise RefreshError("invalid migration plan or portable patch catalog")
    pending = {
        key: len(operations.get(key, []))
        for key in ("add", "replace", "delete", "mode")
    }
    if any(pending.values()):
        raise RefreshError(
            "package tree is not the deterministic migration output: "
            + " ".join(f"{key}={value}" for key, value in pending.items())
        )
    existing = {
        patch["packaged_path"]: patch
        for patch in current_patches
        if isinstance(patch, dict) and isinstance(patch.get("packaged_path"), str)
    }
    patches: list[dict[str, Any]] = []
    snapshot_hashes: set[str] = set()
    for operation in sorted(
        [
            *operations.get("preserve_derivative", []),
            *operations.get("preserve_reviewed_derivative", []),
            *operations.get("register_derivative", []),
            *operations.get("register_generated", []),
        ],
        key=lambda item: item["packaged_path"],
    ):
        packaged_path = operation["packaged_path"]
        patch = existing.get(packaged_path)
        generator = operation.get("package_generator")
        deterministic_sanitizer_output = (
            operation.get("expected_packaged_sha256")
            == operation.get("packaged_sha256")
        )
        deterministic_generator_output = (
            generator == "scripts/build_full_router_index.py"
            and packaged_path
            == "packs/full-routing/skills/all-skills-router/references/skill-index.json"
        )
        reviewed_manual_output = operation.get("reviewed_manual") is True
        if (
            patch is not None
            and patch.get("source_sha256") == operation["source_sha256"]
            and patch.get("packaged_sha256") == operation["packaged_sha256"]
        ):
            if patch.get("source_snapshot") == (
                "catalog/maintainer_source_snapshot.json"
            ):
                if not (
                    deterministic_sanitizer_output
                    or deterministic_generator_output
                    or reviewed_manual_output
                ):
                    raise RefreshError(
                        "existing maintainer derivative lacks deterministic proof: "
                        f"{packaged_path}"
                    )
                patches.append(
                    {
                        "description": patch["description"],
                        "packaged_path": packaged_path,
                        "packaged_sha256": operation["packaged_sha256"],
                        "source_sha256": operation["source_sha256"],
                        "source_snapshot": (
                            "catalog/maintainer_source_snapshot.json"
                        ),
                        "upstream_origin": "this-repository",
                        "transformation": (
                            (
                                "reviewed_manual_portable_derivative"
                                if reviewed_manual_output
                                else f"package_generator:{generator}"
                            )
                            if reviewed_manual_output
                            or deterministic_generator_output
                            else "deterministic_portability_sanitizer"
                        ),
                    }
                )
                snapshot_hashes.add(operation["source_sha256"])
            else:
                patches.append(patch)
            continue
        if not (
            deterministic_sanitizer_output
            or deterministic_generator_output
            or reviewed_manual_output
        ):
            raise RefreshError(
                "deterministic output proof is missing for "
                f"{operation.get('packaged_path')}"
            )
        snapshot_hashes.add(operation["source_sha256"])
        patches.append(
            {
                "description": (
                    operation["description"]
                    if reviewed_manual_output
                    else (
                        "Publish the package router index generated and verified by "
                        "scripts/build_full_router_index.py."
                    )
                    if deterministic_generator_output
                    else (
                        "Publish the current maintainer-selected implementation after "
                        "deterministic privacy and portability rewrites."
                    )
                ),
                "packaged_path": packaged_path,
                "packaged_sha256": operation["packaged_sha256"],
                "source_sha256": operation["source_sha256"],
                "source_snapshot": "catalog/maintainer_source_snapshot.json",
                "upstream_origin": "this-repository",
                **(
                    {
                        "transformation": (
                            "reviewed_manual_portable_derivative"
                            if reviewed_manual_output
                            else f"package_generator:{generator}"
                        )
                    }
                    if reviewed_manual_output or deterministic_generator_output
                    else {"transformation": "deterministic_portability_sanitizer"}
                ),
            }
        )
    private_omissions: list[dict[str, Any]] = []
    for omission in sorted(
        omissions,
        key=lambda item: (item["skill"], item["source_path"]),
    ):
        private_omissions.append(omission)
    omission_counts = Counter(
        omission["reason"] for omission in private_omissions
    )
    snapshot = {
        "schema_version": 1,
        "description": (
            "Content hashes for maintainer-selected portable derivatives. "
            "Source paths and omission details remain in the Git-ignored workbench."
        ),
        "imports": {
            "maintainer-current-portable": {
                "origin": "this-repository",
                "files": [
                    {"sha256": digest}
                    for digest in sorted(snapshot_hashes)
                ],
            }
        },
    }
    catalog = {
        "schema_version": 1,
        "patches": patches,
        "omissions": [],
        "omission_summary": {
            "total": len(private_omissions),
            "by_reason": dict(sorted(omission_counts.items())),
        },
    }
    private_catalog = {
        "schema_version": 1,
        "sensitivity": "private_do_not_publish",
        "omissions": private_omissions,
    }
    return snapshot, catalog, private_catalog


def load_object(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise RefreshError(f"expected JSON object: {path.name}")
    return value


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", action="append", required=True, type=planner.parse_source)
    parser.add_argument("--private-inventory", required=True, type=Path)
    parser.add_argument(
        "--privacy-ledger",
        type=Path,
        default=ROOT
        / ".agent-config-kit-workbench"
        / "private-term-hashes.json",
    )
    parser.add_argument(
        "--reviewed-derivatives",
        type=Path,
        default=ROOT
        / ".agent-config-kit-workbench"
        / "reviewed-portable-derivatives.json",
    )
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    try:
        source_roots = dict(args.source)
        inventory = load_object(args.private_inventory)
        current_catalog = load_object(PATCH_PATH)
        plan = planner.build_plan(
            private_inventory=inventory,
            manifest=load_object(ROOT / "manifest.json"),
            source_roots=source_roots,
            package_root=ROOT,
            portable_patches=current_catalog,
            privacy_ledger=load_object(args.privacy_ledger),
            reviewed_derivatives=load_object(args.reviewed_derivatives),
        )
        snapshot, catalog, private_catalog = refresh(
            plan=plan,
            current_catalog=current_catalog,
        )
        if args.apply:
            atomic_write(PRIVATE_OMISSIONS_PATH, encoded(private_catalog))
            atomic_write(SNAPSHOT_PATH, encoded(snapshot))
            atomic_write(PATCH_PATH, encoded(catalog))
        print(
            "PORTABLE DERIVATIVES OK: "
            f"patches={len(catalog['patches'])} "
            f"omissions={len(private_catalog['omissions'])} "
            f"snapshot_hashes="
            f"{len(snapshot['imports']['maintainer-current-portable']['files'])}"
        )
        print("Mode: apply" if args.apply else "Mode: dry-run (no files changed)")
    except (RefreshError, planner.MigrationPlanError, OSError, KeyError, TypeError) as exc:
        print(f"PORTABLE DERIVATIVES FAILED: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
