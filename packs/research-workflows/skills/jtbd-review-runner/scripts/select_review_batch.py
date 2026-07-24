#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import math
from collections import Counter, defaultdict
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Select a deterministic review batch.")
    parser.add_argument("--reviews-file", required=True, help="Path to clean_reviews.csv")
    parser.add_argument("--existing-output-dir", default="", help="Optional dir with existing JSON outputs to include")
    parser.add_argument("--total", type=int, required=True, help="Target batch size")
    parser.add_argument("--num-shards", type=int, default=3, help="How many shard files to write")
    parser.add_argument("--output-dir", required=True, help="Directory for shard id files and manifest")
    return parser.parse_args()


def load_reviews(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def load_existing_ids(path: Path) -> set[str]:
    if not path.exists():
        return set()
    return {item.stem for item in path.glob("*.json") if item.name != "batch_summary.json"}


def choose_evenly(items: list[str], count: int) -> list[str]:
    if count <= 0 or not items:
        return []
    if count >= len(items):
        return items[:]
    selected = []
    for i in range(count):
        idx = math.floor(i * len(items) / count)
        selected.append(items[idx])
    # de-dupe in case floor collisions happen on small buckets
    deduped = []
    seen = set()
    for item in selected:
        if item not in seen:
            seen.add(item)
            deduped.append(item)
    for item in items:
        if len(deduped) >= count:
            break
        if item not in seen:
            seen.add(item)
            deduped.append(item)
    return deduped


def main() -> None:
    args = parse_args()
    reviews = load_reviews(Path(args.reviews_file))
    existing_ids = load_existing_ids(Path(args.existing_output_dir)) if args.existing_output_dir else set()

    if len(existing_ids) > args.total:
        raise SystemExit(f"Existing outputs ({len(existing_ids)}) exceed target total ({args.total}).")

    by_rating: dict[int, list[str]] = defaultdict(list)
    all_ids = []
    for row in reviews:
        review_id = row["review_id"]
        all_ids.append(review_id)
        if review_id in existing_ids:
            continue
        by_rating[int(row["rating"] or 0)].append(review_id)

    total_reviews = len(reviews)
    remaining_slots = args.total - len(existing_ids)

    remaining_counts = {rating: len(ids) for rating, ids in by_rating.items()}
    target_counts: dict[int, int] = {}
    raw_targets = []
    for rating in sorted(remaining_counts):
        total_in_rating = sum(1 for row in reviews if int(row["rating"] or 0) == rating)
        proportion = total_in_rating / total_reviews
        raw = proportion * remaining_slots
        base = min(remaining_counts[rating], math.floor(raw))
        target_counts[rating] = base
        raw_targets.append((rating, raw - base))

    assigned = sum(target_counts.values())
    for rating, _frac in sorted(raw_targets, key=lambda item: item[1], reverse=True):
        if assigned >= remaining_slots:
            break
        if target_counts[rating] < remaining_counts[rating]:
            target_counts[rating] += 1
            assigned += 1

    selected_ids = list(sorted(existing_ids))
    for rating in sorted(target_counts):
        bucket = sorted(by_rating[rating])
        selected_ids.extend(choose_evenly(bucket, target_counts[rating]))

    selected_ids = selected_ids[: args.total]

    shard_count = args.num_shards
    shards = [[] for _ in range(shard_count)]
    for idx, review_id in enumerate(selected_ids):
        shards[idx % shard_count].append(review_id)

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    for idx, shard in enumerate(shards, start=1):
        (output_dir / f"shard{idx}.txt").write_text("\n".join(shard) + "\n", encoding="utf-8")

    manifest = {
        "total_selected": len(selected_ids),
        "existing_reused": len(existing_ids),
        "remaining_sampled": len(selected_ids) - len(existing_ids),
        "target_total": args.total,
        "rating_targets": target_counts,
        "shards": {f"shard{idx}": shard for idx, shard in enumerate(shards, start=1)},
        "selected_ids": selected_ids,
    }
    (output_dir / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(output_dir / "manifest.json")


if __name__ == "__main__":
    main()
