#!/usr/bin/env python3
"""Build or verify the on-demand index used by the full-profile Skill router."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import tempfile
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
ROUTER_NAME = "all-skills-router"
DEFAULT_OUTPUT = (
    ROOT
    / "packs"
    / "full-routing"
    / "skills"
    / ROUTER_NAME
    / "references"
    / "skill-index.json"
)


class RouterIndexError(Exception):
    pass


def load_object(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise RouterIndexError(f"invalid JSON: {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise RouterIndexError(f"expected JSON object: {path}")
    return value


def parse_frontmatter(path: Path) -> tuple[str, str]:
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise RouterIndexError(f"cannot read Skill: {path}: {exc}") from exc
    if not text.startswith("---\n"):
        raise RouterIndexError(f"missing frontmatter: {path}")
    end = text.find("\n---", 4)
    if end < 0:
        raise RouterIndexError(f"unterminated frontmatter: {path}")
    lines = text[4:end].splitlines()
    values: dict[str, str] = {}
    index = 0
    while index < len(lines):
        match = re.fullmatch(r"([A-Za-z0-9_-]+):(?:\s*(.*))?", lines[index])
        if match is None:
            index += 1
            continue
        key, raw = match.group(1), (match.group(2) or "").strip()
        if raw in {"|", "|-", ">", ">-"}:
            parts: list[str] = []
            index += 1
            while index < len(lines) and (
                not lines[index].strip() or lines[index][0].isspace()
            ):
                if lines[index].strip():
                    parts.append(lines[index].strip())
                index += 1
            values[key] = " ".join(parts)
            continue
        values[key] = raw.strip("\"'")
        index += 1
    name = values.get("name", "").strip()
    description = values.get("description", "").strip()
    if not name or not description:
        raise RouterIndexError(f"missing Skill name or description: {path}")
    return name, description


def build_index(root: Path = ROOT) -> dict[str, Any]:
    manifest = load_object(root / "manifest.json")
    packs = manifest.get("skill_packs")
    full = manifest.get("profiles", {}).get("full")
    if (
        manifest.get("schema_version") != 1
        or not isinstance(packs, dict)
        or not isinstance(full, dict)
        or not isinstance(full.get("skill_packs"), list)
        or not full["skill_packs"]
        or full["skill_packs"][0] != "full-routing"
        or packs.get("full-routing") != [ROUTER_NAME]
    ):
        raise RouterIndexError("full profile must lead with the all-skills router")

    records: list[dict[str, str]] = []
    seen: set[str] = set()
    for pack_name in full["skill_packs"]:
        names = packs.get(pack_name)
        if not isinstance(names, list):
            raise RouterIndexError(f"invalid Skill pack: {pack_name}")
        for name in names:
            if not isinstance(name, str) or not name or name in seen:
                raise RouterIndexError(f"invalid or duplicate Skill: {name}")
            seen.add(name)
            skill_path = root / "packs" / pack_name / "skills" / name / "SKILL.md"
            parsed_name, description = parse_frontmatter(skill_path)
            if parsed_name != name:
                raise RouterIndexError(f"Skill folder/name mismatch: {name}")
            if name == ROUTER_NAME:
                continue
            records.append(
                {
                    "description": description,
                    "name": name,
                    "sibling_skill_path": f"../{name}/SKILL.md",
                }
            )
    records.sort(key=lambda record: record["name"])
    return {
        "schema_version": 1,
        "description": (
            "On-demand routing metadata for every non-router Skill installed by "
            "the full profile. Read the selected sibling SKILL.md before use."
        ),
        "summary": {
            "indexed_skills": len(records),
            "path_base": "router_skill_dir",
            "router_skill": ROUTER_NAME,
        },
        "skills": records,
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
    output = args.output or (
        args.root
        / "packs"
        / "full-routing"
        / "skills"
        / ROUTER_NAME
        / "references"
        / "skill-index.json"
    )
    try:
        expected = encoded(build_index(args.root))
        if args.check:
            actual = output.read_text(encoding="utf-8")
            if actual != expected:
                raise RouterIndexError(f"router index is stale: {output}")
        else:
            atomic_write(output, expected)
    except (OSError, RouterIndexError) as exc:
        print(f"FULL ROUTER INDEX FAILED: {exc}", file=sys.stderr)
        return 1
    payload = json.loads(expected)
    print(
        "FULL ROUTER INDEX OK: "
        f"skills={payload['summary']['indexed_skills']} "
        f"router={payload['summary']['router_skill']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
