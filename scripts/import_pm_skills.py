#!/usr/bin/env python3
"""Import the pinned PM Skill set file-by-file after provenance and hash checks."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
IMPORTS_PATH = ROOT / "catalog" / "imports.json"


class ImportError(Exception):
    pass


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_spec() -> dict[str, Any]:
    try:
        document = json.loads(IMPORTS_PATH.read_text(encoding="utf-8"))
        spec = document["imports"]["pm-skills-2.1.0"]
    except (OSError, KeyError, json.JSONDecodeError, TypeError) as exc:
        raise ImportError(f"invalid import specification: {exc}") from exc
    return spec


def git_head(root: Path) -> str:
    result = subprocess.run(
        ["git", "-C", str(root), "rev-parse", "HEAD"],
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode:
        raise ImportError("upstream must be a Git checkout")
    return result.stdout.strip()


def read_frontmatter_name(path: Path) -> str:
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0] != "---":
        raise ImportError(f"missing frontmatter: {path}")
    for line in lines[1:]:
        if line == "---":
            break
        if line.startswith("name:"):
            return line.split(":", 1)[1].strip().strip("\"'")
    raise ImportError(f"missing Skill name: {path}")


def build_plan(upstream: Path, local: Path, spec: dict[str, Any]) -> list[tuple[Path, Path, str]]:
    if git_head(upstream) != spec["commit"]:
        raise ImportError("upstream checkout does not match the pinned commit")
    license_path = upstream / "LICENSE"
    if not license_path.is_file() or sha256(license_path) != spec["license_sha256"]:
        raise ImportError("upstream LICENSE does not match the pinned hash")

    upstream_skills = sorted(upstream.glob(spec["skill_glob"]))
    if len(upstream_skills) != 68:
        raise ImportError(f"expected 68 upstream Skills, found {len(upstream_skills)}")
    overlays = spec.get("approved_overlays", {})
    plan: list[tuple[Path, Path, str]] = []
    names: set[str] = set()
    for upstream_skill in upstream_skills:
        name = upstream_skill.parent.name
        if name in names or read_frontmatter_name(upstream_skill) != name:
            raise ImportError(f"duplicate or mismatched upstream Skill: {name}")
        names.add(name)
        local_skill = local / name / "SKILL.md"
        if not local_skill.is_file() or read_frontmatter_name(local_skill) != name:
            raise ImportError(f"local Skill is missing or mismatched: {name}")
        upstream_hash = sha256(upstream_skill)
        local_hash = sha256(local_skill)
        overlay = overlays.get(name)
        if overlay:
            if upstream_hash != overlay.get("upstream_sha256"):
                raise ImportError(f"upstream overlay base changed: {name}")
            if local_hash != overlay.get("local_sha256"):
                raise ImportError(f"approved local overlay changed: {name}")
            source = local_skill
        elif local_hash == upstream_hash:
            source = upstream_skill
        else:
            raise ImportError(f"unapproved local difference: {name}")
        destination = ROOT / "packs" / spec["pack"] / "skills" / name / "SKILL.md"
        plan.append((source, destination, name))
    return plan


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--upstream", type=Path, required=True)
    parser.add_argument("--local", type=Path, required=True)
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    try:
        spec = load_spec()
        plan = build_plan(args.upstream.resolve(), args.local.resolve(), spec)
        print(f"Import plan: skills={len(plan)} pack={spec['pack']}")
        print("Mode: apply" if args.apply else "Mode: dry-run (no files changed)")
        if args.apply:
            for source, destination, _ in plan:
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source, destination)
            license_target = ROOT / "packs" / spec["pack"] / "LICENSE"
            shutil.copy2(args.upstream.resolve() / "LICENSE", license_target)
            print("Import applied. Run the source audit and package verification next.")
    except (ImportError, OSError, KeyError, TypeError) as exc:
        print(f"IMPORT FAILED: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
