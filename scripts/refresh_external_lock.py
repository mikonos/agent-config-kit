#!/usr/bin/env python3
"""Review and refresh hash locks for mutable official Skill endpoints."""

from __future__ import annotations

import argparse
import json
import os
import sys
import tempfile
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
CATALOG_PATH = ROOT / "catalog" / "external_skills.json"
sys.path.insert(0, str(ROOT / "install" / "scripts"))

import externalctl  # noqa: E402


class RefreshError(Exception):
    pass


def load_catalog(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise RefreshError(f"invalid external Skill catalog: {exc}") from exc
    if not isinstance(value, dict):
        raise RefreshError("external Skill catalog must contain an object")
    externalctl.validate_catalog(value)
    return value


def refresh_catalog(
    catalog: dict[str, Any],
    updates: list[externalctl.ExternalUpdate],
) -> int:
    by_name = {
        entry["name"]: entry
        for pack in catalog["packs"].values()
        for entry in pack["skills"]
    }
    if set(by_name) != {item.name for item in updates}:
        raise RefreshError("update result does not cover the selected catalog")
    changed = 0
    for item in updates:
        entry = by_name[item.name]
        if item.status == "current":
            continue
        if item.status == "rollback_detected":
            raise RefreshError(
                f"refusing to approve a previously served version: {item.name}"
            )
        if (
            item.status != "update_available"
            or entry["sha256"] != item.approved_sha256
            or entry["url"] != item.url
        ):
            raise RefreshError(f"invalid update result: {item.name}")
        history = [
            *entry.get("previous_sha256", []),
            item.approved_sha256,
        ]
        entry["previous_sha256"] = list(dict.fromkeys(history))
        entry["sha256"] = item.observed_sha256
        changed += 1
    externalctl.validate_catalog(catalog)
    return changed


def report_markdown(updates: list[externalctl.ExternalUpdate]) -> str:
    changed = [item for item in updates if item.status == "update_available"]
    lines = [
        "# External Skill lock refresh",
        "",
        "This change updates only the reviewed hash lock for official mutable "
        "endpoints. Bundled Skills are unaffected.",
        "",
        "Before merging, open every changed official source URL, review the "
        "current Skill instructions, and rerun the lock check. The hash in this "
        "pull request binds the reviewed bytes.",
        "",
    ]
    if not changed:
        lines.append("No upstream changes detected.")
    else:
        lines.extend(
            [
                "| Skill | Official source | Previous hash | Proposed hash |",
                "|---|---|---|---|",
            ]
        )
        for item in changed:
            lines.append(
                f"| `{item.name}` | [review source]({item.url}) | "
                f"`{item.approved_sha256}` | `{item.observed_sha256}` |"
            )
    lines.extend(
        [
            "",
            "Merge gate:",
            "",
            "- Every changed URL was reviewed as current official content.",
            "- `python3 install/scripts/externalctl.py check-updates` reports no "
            "remaining update.",
            "- Package verification and external lifecycle tests pass.",
            "",
        ]
    )
    return "\n".join(lines)


def atomic_write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(
        prefix=f".{path.name}.",
        dir=path.parent,
    )
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            handle.write(text)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    except BaseException:
        try:
            os.unlink(temporary)
        except OSError:
            pass
        raise


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--catalog", type=Path, default=CATALOG_PATH)
    parser.add_argument("--pack", action="append")
    parser.add_argument("--report", type=Path)
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    try:
        catalog = load_catalog(args.catalog)
        packs = sorted(externalctl.validate_catalog(catalog))
        selected_packs = args.pack or packs
        if set(selected_packs) != set(packs):
            raise RefreshError(
                "lock refresh must cover every external pack atomically"
            )
        updates = externalctl.check_update_plan(catalog, selected_packs)
        rollback = [
            item.name
            for item in updates
            if item.status == "rollback_detected"
        ]
        if rollback:
            raise RefreshError(
                "manual rollback review required: " + ", ".join(rollback)
            )
        changed = sum(
            item.status == "update_available" for item in updates
        )
        if args.report is not None:
            atomic_write(args.report, report_markdown(updates))
        if args.apply and changed:
            applied = refresh_catalog(catalog, updates)
            if applied != changed:
                raise RefreshError("lock refresh changed an unexpected count")
            atomic_write(
                args.catalog,
                json.dumps(
                    catalog,
                    ensure_ascii=False,
                    indent=2,
                    sort_keys=True,
                )
                + "\n",
            )
        print(
            "EXTERNAL LOCK "
            + ("UPDATED" if args.apply and changed else "CHECKED")
            + f": current={len(updates) - changed} update_available={changed}"
        )
        if changed and not args.apply:
            print(
                "No files changed. Review the official sources, then rerun "
                "with --apply or use the scheduled pull-request workflow."
            )
            return 1
        return 0
    except (
        RefreshError,
        externalctl.configctl.ConfigError,
        OSError,
        TypeError,
        ValueError,
    ) as exc:
        print(f"EXTERNAL LOCK FAILED: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
