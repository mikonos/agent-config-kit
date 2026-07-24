#!/usr/bin/env python3
"""Reject reviewed private terms without storing their plaintext in the repository."""

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
    f"private_term_{index:03d}" for index in range(1, 6)
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


def load_terms(ledger: dict[str, Any]) -> tuple[dict[str, str], dict[int, dict[str, str]]]:
    terms = ledger.get("terms")
    if ledger.get("schema_version") != 1 or not isinstance(terms, list):
        raise PrivacyError("invalid semantic privacy ledger")
    ascii_terms: dict[str, str] = {}
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
        target = ascii_terms if matcher == "ascii_token" else cjk_terms.setdefault(length, {})
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
    cjk_lengths: Iterable[int],
) -> Iterable[str]:
    for token in ASCII_TOKEN.findall(text):
        yield digest(token)
        for part in ASCII_PART.findall(token):
            if part != token:
                yield digest(part)
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


def verify(root: Path, ledger: dict[str, Any]) -> list[str]:
    ascii_terms, cjk_terms = load_terms(ledger)
    problems: list[str] = []

    def matching_terms(text: str) -> set[str]:
        matches: set[str] = set()
        for candidate in candidate_digests(text, cjk_terms):
            term_id = ascii_terms.get(candidate)
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

    for path in iter_public_files(root):
        relative = path.relative_to(root).as_posix()
        path_matches = matching_terms(relative)
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
                for term_id in matching_terms(text)
            )
    return sorted(set(problems))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--ledger", type=Path)
    args = parser.parse_args()
    ledger_path = args.ledger or args.root / "catalog" / "private_term_hashes.json"
    try:
        problems = verify(args.root, load_object(ledger_path))
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
