#!/usr/bin/env python3
"""Find the newest reachable commit containing an exact Git subtree SHA."""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path, PurePosixPath
from typing import Optional


SHA_PATTERN = re.compile(r"[0-9a-f]{40}")


def git(repository: Path, *args: str, check: bool = True) -> str:
    result = subprocess.run(
        ["git", "-C", str(repository), *args],
        text=True,
        capture_output=True,
        check=False,
    )
    if check and result.returncode:
        raise RuntimeError(result.stderr.strip() or f"git failed: {' '.join(args)}")
    return result.stdout.strip() if result.returncode == 0 else ""


def find_commit(repository: Path, skill_path: str, tree_sha: str) -> Optional[str]:
    if not SHA_PATTERN.fullmatch(tree_sha):
        raise ValueError("tree SHA must be 40 lowercase hex characters")
    path = PurePosixPath(skill_path)
    if path.is_absolute() or ".." in path.parts or path.name != "SKILL.md":
        raise ValueError("skill path must be a safe path ending in SKILL.md")
    folder = path.parent.as_posix()
    revision_args = ["rev-list", "--date-order", "--all"]
    if folder != ".":
        revision_args.extend(["--", folder])
    commits = git(repository, *revision_args).splitlines()
    for commit in commits:
        if folder == ".":
            candidate = git(repository, "show", "-s", "--format=%T", commit)
        else:
            candidate = git(
                repository,
                "rev-parse",
                "--verify",
                f"{commit}:{folder}",
                check=False,
            )
        if candidate == tree_sha:
            return commit
    return None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", required=True, type=Path)
    parser.add_argument("--skill-path", required=True)
    parser.add_argument("--tree-sha", required=True)
    args = parser.parse_args()
    try:
        commit = find_commit(args.repo.resolve(), args.skill_path, args.tree_sha)
    except (OSError, RuntimeError, ValueError) as exc:
        print(f"TREE LOOKUP FAILED: {exc}", file=sys.stderr)
        return 2
    if commit is None:
        print("TREE LOOKUP FAILED: no reachable commit matches", file=sys.stderr)
        return 2
    print(commit)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
