#!/usr/bin/env python3
"""Resolve runtime source tree hashes to exact current GitHub commits."""

from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.request
from collections import defaultdict
from pathlib import Path, PurePosixPath
from typing import Any, Callable, Optional


JsonLoader = Callable[[str], dict[str, Any]]


def github_repository(source_url: str) -> Optional[str]:
    prefix = "https://github.com/"
    if not source_url.startswith(prefix):
        return None
    repository = source_url[len(prefix):].removesuffix(".git").strip("/")
    if repository.count("/") != 1:
        return None
    return repository


def fetch_json(url: str) -> dict[str, Any]:
    request = urllib.request.Request(
        url,
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "agent-config-kit-runtime-pin-resolver",
            "X-GitHub-Api-Version": "2022-11-28",
        },
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        payload = json.load(response)
    if not isinstance(payload, dict):
        raise ValueError(f"expected JSON object from {url}")
    return payload


def resolve_catalog(catalog: dict[str, Any], loader: JsonLoader) -> dict[str, Any]:
    entries = catalog.get("skills")
    if not isinstance(entries, list):
        raise ValueError("runtime source catalog must contain a skills list")
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    results: dict[str, dict[str, Any]] = {}
    repositories: dict[str, dict[str, Any]] = {}
    for entry in entries:
        name = entry["name"]
        repository = github_repository(entry["source_url"])
        if repository is None:
            results[name] = {
                "name": name,
                "status": "live_origin_unpinned",
                "commit": None,
            }
        elif entry.get("tree_sha") is None:
            results[name] = {
                "name": name,
                "status": "missing_tree_sha",
                "commit": None,
            }
        else:
            grouped[repository].append(entry)

    for repository, repo_entries in sorted(grouped.items()):
        try:
            metadata = loader(f"https://api.github.com/repos/{repository}")
            default_branch = metadata.get("default_branch")
            if not isinstance(default_branch, str) or not default_branch:
                raise ValueError("repository has no default branch")
            commit_payload = loader(
                f"https://api.github.com/repos/{repository}/commits/{default_branch}"
            )
            commit = commit_payload.get("sha")
            if not isinstance(commit, str) or len(commit) != 40:
                raise ValueError("repository commit is invalid")
            tree_payload = loader(
                f"https://api.github.com/repos/{repository}/git/trees/{commit}?recursive=1"
            )
            if tree_payload.get("truncated"):
                raise ValueError("repository tree response is truncated")
            tree = tree_payload.get("tree")
            if not isinstance(tree, list):
                raise ValueError("repository tree response is invalid")
            root_tree_sha = tree_payload.get("sha")
            if not isinstance(root_tree_sha, str):
                raise ValueError("repository root tree SHA is invalid")
            tree_by_path = {
                item["path"]: item["sha"]
                for item in tree
                if isinstance(item, dict)
                and item.get("type") == "tree"
                and isinstance(item.get("path"), str)
                and isinstance(item.get("sha"), str)
            }
            license_data = metadata.get("license")
            license_spdx = (
                license_data.get("spdx_id")
                if isinstance(license_data, dict)
                and isinstance(license_data.get("spdx_id"), str)
                else None
            )
            repositories[repository] = {
                "default_branch": default_branch,
                "current_commit": commit,
                "repository_license_spdx": license_spdx,
                "license_scope": "repository_only_requires_skill_level_review",
            }
            for entry in repo_entries:
                folder = PurePosixPath(entry["skill_path"]).parent.as_posix()
                actual = (
                    root_tree_sha
                    if folder == "."
                    else tree_by_path.get(folder)
                )
                results[entry["name"]] = {
                    "name": entry["name"],
                    "status": (
                        "exact_current"
                        if actual == entry["tree_sha"]
                        else "current_tree_mismatch"
                    ),
                    "commit": commit if actual == entry["tree_sha"] else None,
                }
        except (KeyError, ValueError, urllib.error.URLError) as exc:
            repositories[repository] = {
                "error": type(exc).__name__,
                "license_scope": "unresolved",
            }
            for entry in repo_entries:
                results[entry["name"]] = {
                    "name": entry["name"],
                    "status": "lookup_failed",
                    "commit": None,
                }

    ordered = [results[entry["name"]] for entry in entries]
    counts: dict[str, int] = defaultdict(int)
    for result in ordered:
        counts[result["status"]] += 1
    return {
        "schema_version": 1,
        "description": (
            "Exact pins are emitted only when a runtime lock tree SHA matches "
            "the repository default branch. Repository licenses are not "
            "Skill-level redistribution approvals."
        ),
        "summary": dict(sorted(counts.items())),
        "repositories": repositories,
        "skills": ordered,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--catalog", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--require-exact", action="store_true")
    args = parser.parse_args()
    catalog = json.loads(args.catalog.read_text(encoding="utf-8"))
    resolved = resolve_catalog(catalog, fetch_json)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(resolved, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(resolved["summary"], sort_keys=True))
    unresolved = sum(
        count
        for status, count in resolved["summary"].items()
        if status != "exact_current"
    )
    if args.require_exact and unresolved:
        print(f"unresolved runtime source pins: {unresolved}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
