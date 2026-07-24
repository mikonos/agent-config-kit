#!/usr/bin/env python3
"""Require an explicit decision for every low-confidence secret-shaped match."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any


CANDIDATE = re.compile(r"sk-[A-Za-z0-9_-]{20,}")
HIGH_CONFIDENCE = re.compile(r"(?<![A-Za-z0-9])sk-[A-Za-z0-9_-]{20,}")
DIGEST = re.compile(r"[0-9a-f]{64}")


class ReviewError(Exception):
    pass


def load_object(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ReviewError(f"invalid JSON: {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise ReviewError(f"expected JSON object: {path}")
    return value


def scan(root: Path) -> tuple[set[tuple[str, int, str]], list[str]]:
    candidates: set[tuple[str, int, str]] = set()
    high_confidence: list[str] = []
    packs = root / "packs"
    for path in sorted(packs.rglob("*")):
        if (
            not path.is_file()
            or path.is_symlink()
            or path.stat().st_size > 2_000_000
        ):
            continue
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except (OSError, UnicodeDecodeError):
            continue
        relative = path.relative_to(root).as_posix()
        for number, line in enumerate(lines, 1):
            if HIGH_CONFIDENCE.search(line):
                high_confidence.append(f"{relative}:{number}")
            elif CANDIDATE.search(line):
                digest = hashlib.sha256(line.encode("utf-8")).hexdigest()
                candidates.add((relative, number, digest))
    return candidates, high_confidence


def verify(root: Path, ledger: dict[str, Any]) -> tuple[int, int]:
    reviews = ledger.get("reviews")
    if ledger.get("schema_version") != 1 or not isinstance(reviews, list):
        raise ReviewError("invalid sensitive review ledger")
    expected: set[tuple[str, int, str]] = set()
    for review in reviews:
        if not isinstance(review, dict):
            raise ReviewError("invalid sensitive review entry")
        path = review.get("path")
        line = review.get("line")
        digest = review.get("line_sha256")
        if (
            set(review)
            != {
                "decision",
                "line",
                "line_sha256",
                "path",
                "pattern",
                "reason",
            }
            or review.get("decision") != "false_positive"
            or review.get("pattern") != "openai_style_secret_candidate"
            or not isinstance(path, str)
            or not path.startswith("packs/")
            or Path(path).is_absolute()
            or ".." in Path(path).parts
            or not isinstance(line, int)
            or line < 1
            or not isinstance(digest, str)
            or DIGEST.fullmatch(digest) is None
            or not isinstance(review.get("reason"), str)
            or not review["reason"].strip()
        ):
            raise ReviewError("invalid sensitive review entry")
        key = (path, line, digest)
        if key in expected:
            raise ReviewError(f"duplicate sensitive review: {path}:{line}")
        expected.add(key)
    actual, high_confidence = scan(root)
    if high_confidence:
        raise ReviewError(
            "high-confidence secret-shaped matches remain: "
            + ", ".join(high_confidence)
        )
    missing = sorted(actual - expected)
    stale = sorted(expected - actual)
    if missing or stale:
        raise ReviewError(
            f"sensitive review ledger differs: unresolved={missing} stale={stale}"
        )
    return len(high_confidence), len(actual)


def main() -> int:
    root_default = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=root_default)
    args = parser.parse_args()
    try:
        high_confidence, reviewed = verify(
            args.root,
            load_object(args.root / "catalog" / "sensitive_reviews.json"),
        )
    except (ReviewError, OSError, TypeError) as exc:
        print(f"SENSITIVE REVIEW FAILED: {exc}", file=sys.stderr)
        return 2
    print(
        "SENSITIVE REVIEW OK: "
        f"high_confidence={high_confidence} "
        f"reviewed_false_positives={reviewed} unresolved=0"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
