#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import html
import re
from collections import Counter
from datetime import datetime
from pathlib import Path


WHITESPACE_RE = re.compile(r"\s+")
TAG_RE = re.compile(r"<[^>]+>")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Clean an Amazon reviews CSV into JTBD-ready review rows.")
    parser.add_argument("--input-file", required=True, help="Raw Amazon review CSV")
    parser.add_argument("--output-file", required=True, help="Cleaned output CSV")
    parser.add_argument("--report-file", required=True, help="Cleaning report markdown path")
    parser.add_argument("--review-prefix", default="review", help="Stable review_id prefix, e.g. skylight15")
    return parser.parse_args()


def clean_text(value: str) -> str:
    if not value:
        return ""
    text = html.unescape(value)
    text = text.replace("<br>", "\n").replace("<br/>", "\n").replace("<br />", "\n")
    text = TAG_RE.sub(" ", text)
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    lines = [WHITESPACE_RE.sub(" ", line).strip() for line in text.split("\n")]
    lines = [line for line in lines if line]
    return "\n".join(lines).strip()


def parse_date(value: str) -> str:
    if not value:
        return ""
    return datetime.strptime(value.strip(), "%Y/%m/%d").date().isoformat()


def parse_int(value: str) -> int:
    value = (value or "").strip()
    return int(value) if value else 0


def parse_verified(value: str) -> str:
    return "Y" if (value or "").strip().upper() == "Y" else "N"


def build_cleaned_rows(rows: list[dict[str, str]], input_name: str, review_prefix: str):
    dedupe_counter = Counter()
    empty_content_ids: list[str] = []
    cleaned_rows = []

    for idx, row in enumerate(rows, start=1):
        title = clean_text(row.get("Title", ""))
        content = clean_text(row.get("Content", ""))
        title_en = clean_text(row.get("English Title", ""))
        content_en = clean_text(row.get("English Content", ""))
        review_key = (title, content)
        dedupe_counter[review_key] += 1

        review_id = f"{review_prefix}-{idx:04d}"
        if not content:
            empty_content_ids.append(review_id)

        cleaned_rows.append(
            {
                "review_id": review_id,
                "source_file": input_name,
                "brand": clean_text(row.get("brand", "")),
                "asin": clean_text(row.get("Asin", "")),
                "title_raw": title,
                "title_en": title_en,
                "content_raw": content,
                "content_en": content_en,
                "verified_purchase": parse_verified(row.get("Verified Purchase", "")),
                "model": clean_text(row.get("Model", "")),
                "rating": parse_int(row.get("Rating", "")),
                "helpful": parse_int(row.get("Helpful", "")),
                "nation": clean_text(row.get("Nation", "")).lower(),
                "date": parse_date(row.get("Date", "")),
                "duplicate_group_size": 0,
                "is_duplicate": "N",
                "content_char_count": len(content),
            }
        )

    duplicate_rows = 0
    for row in cleaned_rows:
        key = (row["title_raw"], row["content_raw"])
        group_size = dedupe_counter[key]
        row["duplicate_group_size"] = group_size
        row["is_duplicate"] = "Y" if group_size > 1 else "N"
        if group_size > 1:
            duplicate_rows += 1

    return cleaned_rows, empty_content_ids, duplicate_rows, dedupe_counter


def write_report(
    report_path: Path,
    input_name: str,
    output_name: str,
    cleaned_rows: list[dict[str, str]],
    empty_content_ids: list[str],
    duplicate_rows: int,
    dedupe_counter: Counter,
) -> None:
    ratings = Counter(row["rating"] for row in cleaned_rows)
    verified = Counter(row["verified_purchase"] for row in cleaned_rows)

    report = f"""# AMZ Reviews Cleaning Report

- Input: `{input_name}`
- Output: `{output_name}`
- Total rows: {len(cleaned_rows)}
- Empty `content_raw`: {len(empty_content_ids)}
- Rows marked duplicate: {duplicate_rows}
- Unique duplicate groups: {sum(1 for size in dedupe_counter.values() if size > 1)}

## Rating Distribution

- 5 star: {ratings.get(5, 0)}
- 4 star: {ratings.get(4, 0)}
- 3 star: {ratings.get(3, 0)}
- 2 star: {ratings.get(2, 0)}
- 1 star: {ratings.get(1, 0)}

## Verified Purchase

- Y: {verified.get("Y", 0)}
- N: {verified.get("N", 0)}

## Cleaning Rules

- Kept original raw file unchanged
- Cleaned HTML and line breaks in title/content fields
- Normalized date to `YYYY-MM-DD`
- Normalized `verified_purchase` to `Y/N`
- Normalized `rating/helpful` to integers
- Added stable `review_id`
- Marked duplicate rows by exact `title_raw + content_raw`
- Preserved empty `content_en` when source was empty

## Empty Content Review IDs

{chr(10).join(f"- {review_id}" for review_id in empty_content_ids) if empty_content_ids else "- None"}
"""
    report_path.write_text(report, encoding="utf-8")


def main() -> None:
    args = parse_args()
    input_path = Path(args.input_file)
    output_path = Path(args.output_file)
    report_path = Path(args.report_file)

    with input_path.open(newline="", encoding="utf-8-sig") as f:
      rows = list(csv.DictReader(f))

    cleaned_rows, empty_content_ids, duplicate_rows, dedupe_counter = build_cleaned_rows(
        rows=rows,
        input_name=input_path.name,
        review_prefix=args.review_prefix,
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.parent.mkdir(parents=True, exist_ok=True)

    fieldnames = list(cleaned_rows[0].keys()) if cleaned_rows else []
    with output_path.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(cleaned_rows)

    write_report(
        report_path=report_path,
        input_name=input_path.name,
        output_name=output_path.name,
        cleaned_rows=cleaned_rows,
        empty_content_ids=empty_content_ids,
        duplicate_rows=duplicate_rows,
        dedupe_counter=dedupe_counter,
    )

    print(output_path)
    print(report_path)


if __name__ == "__main__":
    main()
