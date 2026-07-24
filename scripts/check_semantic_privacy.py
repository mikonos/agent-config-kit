#!/usr/bin/env python3
"""Reject reviewed private terms using a Git-ignored maintainer ledger."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[1]
ASCII_TOKEN = re.compile(r"[A-Za-z0-9_.-]+")
ASCII_PART = re.compile(r"[A-Za-z0-9]+")
CJK_RUN = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]+")
DIGEST = re.compile(r"[0-9a-f]{64}")
EXPECTED_TERM_IDS = {
    f"private_term_{index:03d}" for index in range(1, 8)
}
EXCLUDED_DIRS = {
    ".agent-config-kit",
    ".agent-config-kit-workbench",
    ".cache",
    ".git",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".venv",
    "__pycache__",
    "node_modules",
    "test-output",
    "venv",
    "vendor",
}


class PrivacyError(Exception):
    pass


def load_object(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise PrivacyError(f"invalid JSON: {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise PrivacyError(f"expected JSON object: {path}")
    return value


def load_terms(
    ledger: dict[str, Any],
) -> tuple[dict[int, dict[str, str]], dict[int, dict[str, str]]]:
    terms = ledger.get("terms")
    if ledger.get("schema_version") != 1 or not isinstance(terms, list):
        raise PrivacyError("invalid semantic privacy ledger")
    ascii_terms: dict[int, dict[str, str]] = {}
    cjk_terms: dict[int, dict[str, str]] = {}
    seen_ids: set[str] = set()
    for term in terms:
        if not isinstance(term, dict):
            raise PrivacyError("invalid semantic privacy term")
        term_id = term.get("id")
        matcher = term.get("matcher")
        digest = term.get("sha256")
        length = term.get("length")
        if (
            set(term) != {"id", "length", "matcher", "sha256"}
            or not isinstance(term_id, str)
            or re.fullmatch(r"private_term_[0-9]{3}", term_id) is None
            or term_id in seen_ids
            or matcher not in {"ascii_token", "cjk_substring"}
            or not isinstance(length, int)
            or length < 1
            or not isinstance(digest, str)
            or DIGEST.fullmatch(digest) is None
        ):
            raise PrivacyError("invalid semantic privacy term")
        seen_ids.add(term_id)
        target = (
            ascii_terms.setdefault(length, {})
            if matcher == "ascii_token"
            else cjk_terms.setdefault(length, {})
        )
        if digest in target:
            raise PrivacyError("duplicate semantic privacy digest")
        target[digest] = term_id
    if seen_ids != EXPECTED_TERM_IDS:
        raise PrivacyError("semantic privacy term set is incomplete or unexpected")
    return ascii_terms, cjk_terms


def digest(value: str) -> str:
    return hashlib.sha256(value.casefold().encode("utf-8")).hexdigest()


def candidate_digests(
    text: str,
    ascii_lengths: Iterable[int],
    cjk_lengths: Iterable[int],
) -> Iterable[str]:
    for token in ASCII_TOKEN.findall(text):
        candidates = {token, *ASCII_PART.findall(token)}
        for candidate in candidates:
            for length in ascii_lengths:
                if len(candidate) < length:
                    continue
                for start in range(len(candidate) - length + 1):
                    yield digest(candidate[start : start + length])
    for run in CJK_RUN.findall(text):
        for length in cjk_lengths:
            if len(run) < length:
                continue
            for start in range(len(run) - length + 1):
                yield digest(run[start : start + length])


def iter_public_files(root: Path) -> Iterable[Path]:
    for path in sorted(root.rglob("*")):
        relative = path.relative_to(root)
        if any(part in EXCLUDED_DIRS for part in relative.parts):
            continue
        if path.is_file() and not path.is_symlink():
            yield path


def load_private_aliases(private_inventory: dict[str, Any]) -> dict[str, str]:
    if (
        private_inventory.get("schema_version") != 1
        or private_inventory.get("sensitivity") != "private_do_not_publish"
        or not isinstance(private_inventory.get("skills"), dict)
    ):
        raise PrivacyError("invalid private Skill inventory")
    aliases: set[str] = set()
    shared = private_inventory.get("portable_reference_aliases", {})
    if not isinstance(shared, dict):
        raise PrivacyError("invalid private reference aliases")
    for private, public in shared.items():
        if not isinstance(private, str) or not private or not isinstance(public, str):
            raise PrivacyError("invalid private reference aliases")
        aliases.add(private.casefold())
    for record in private_inventory["skills"].values():
        if not isinstance(record, dict):
            raise PrivacyError("invalid private Skill inventory")
        record_aliases = record.get("portable_aliases", {})
        if not isinstance(record_aliases, dict):
            raise PrivacyError("invalid private Skill aliases")
        for private, public in record_aliases.items():
            if not isinstance(private, str) or not private or not isinstance(public, str):
                raise PrivacyError("invalid private Skill aliases")
            aliases.add(private.casefold())
    ordered = sorted(aliases, key=digest)
    return {
        private: f"private_alias_{index:03d}"
        for index, private in enumerate(ordered, 1)
    }


def load_binary_approvals(value: dict[str, Any], *, private: bool) -> dict[str, str]:
    if not isinstance(value, dict):
        raise PrivacyError("invalid binary asset approval")
    assets = value.get("assets")
    if (
        value.get("schema_version") != 1
        or not isinstance(assets, list)
        or (private and value.get("sensitivity") != "private_do_not_publish")
    ):
        raise PrivacyError("invalid binary asset approval")
    result: dict[str, str] = {}
    for asset in assets:
        path = asset.get("path") if isinstance(asset, dict) else None
        sha256 = asset.get("sha256") if isinstance(asset, dict) else None
        if (
            not isinstance(path, str)
            or not path
            or Path(path).is_absolute()
            or ".." in Path(path).parts
            or not isinstance(sha256, str)
            or DIGEST.fullmatch(sha256) is None
            or path in result
        ):
            raise PrivacyError("invalid binary asset approval")
        result[path] = sha256
    return result


def verify(
    root: Path,
    ledger: dict[str, Any],
    *,
    private_inventory: dict[str, Any] | None = None,
    reviewed_binary_assets: dict[str, Any] | None = None,
) -> list[str]:
    ascii_terms, cjk_terms = load_terms(ledger)
    aliases = (
        load_private_aliases(private_inventory)
        if private_inventory is not None
        else {}
    )
    problems: list[str] = []

    def matching_terms(text: str) -> set[str]:
        matches: set[str] = set()
        for candidate in candidate_digests(text, ascii_terms, cjk_terms):
            term_id = next(
                (
                    terms[candidate]
                    for terms in ascii_terms.values()
                    if candidate in terms
                ),
                None,
            )
            if term_id is None:
                term_id = next(
                    (
                        terms[candidate]
                        for terms in cjk_terms.values()
                        if candidate in terms
                    ),
                    None,
                )
            if term_id is not None:
                matches.add(term_id)
        return matches

    def matching_aliases(text: str) -> set[str]:
        folded = text.casefold()
        return {
            alias_id
            for private, alias_id in aliases.items()
            if re.search(alias_pattern(private), folded) is not None
        }

    def alias_pattern(private: str) -> str:
        escaped = re.escape(private)
        if re.fullmatch(r"_[a-z0-9]+", private):
            return rf"(?<![a-z0-9_]){escaped}(?![a-z0-9_])"
        return escaped

    for path in iter_public_files(root):
        relative = path.relative_to(root).as_posix()
        path_matches = matching_terms(relative) | matching_aliases(relative)
        if path_matches:
            path_reference = "path_sha256=" + hashlib.sha256(
                relative.encode("utf-8")
            ).hexdigest()
            problems.extend(
                f"{term_id}: {path_reference}" for term_id in path_matches
            )
        else:
            path_reference = relative
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except UnicodeDecodeError:
            continue
        for line_number, text in enumerate(lines, 1):
            problems.extend(
                f"{term_id}: {path_reference}:{line_number}"
                for term_id in matching_terms(text) | matching_aliases(text)
            )
    if reviewed_binary_assets is not None:
        public_catalog_path = root / "catalog" / "binary_assets.json"
        if not public_catalog_path.is_file():
            problems.append("binary_asset_approval: public catalog missing")
        else:
            public_assets = load_binary_approvals(
                load_object(public_catalog_path),
                private=False,
            )
            private_assets = load_binary_approvals(
                reviewed_binary_assets,
                private=True,
            )
            if public_assets != private_assets:
                problems.append("binary_asset_approval: catalog differs from private review")
    return sorted(set(problems))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--ledger", type=Path)
    parser.add_argument("--private-inventory", type=Path)
    parser.add_argument("--reviewed-binary-assets", type=Path)
    args = parser.parse_args()
    ledger_path = (
        args.ledger
        or args.root
        / ".agent-config-kit-workbench"
        / "private-term-hashes.json"
    )
    private_inventory_path = (
        args.private_inventory
        or args.root
        / ".agent-config-kit-workbench"
        / "private-skill-inventory.json"
    )
    reviewed_binary_assets_path = (
        args.reviewed_binary_assets
        or args.root
        / ".agent-config-kit-workbench"
        / "reviewed-binary-assets.json"
    )
    try:
        problems = verify(
            args.root,
            load_object(ledger_path),
            private_inventory=load_object(private_inventory_path),
            reviewed_binary_assets=load_object(reviewed_binary_assets_path),
        )
    except (OSError, PrivacyError, TypeError) as exc:
        print(f"SEMANTIC PRIVACY FAILED: {exc}", file=sys.stderr)
        return 2
    if problems:
        print(
            "SEMANTIC PRIVACY FAILED: private terms remain:\n"
            + "\n".join(problems),
            file=sys.stderr,
        )
        return 2
    print("SEMANTIC PRIVACY OK: reviewed private terms absent")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
