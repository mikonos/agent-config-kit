#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from review_runner_lib import (
    build_payload,
    find_review,
    read_text,
    run_agent,
    validate_json,
    write_text,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run one review through Cursor Agent.")
    parser.add_argument("review_id", help="Review ID, e.g. skylight15-0067")
    parser.add_argument("--reviews-file", required=True, help="Path to clean_reviews.csv")
    parser.add_argument("--prompt-file", required=True, help="Path to prompt markdown")
    parser.add_argument("--codebook-file", required=True, help="Path to codebook markdown")
    parser.add_argument("--workspace", default=".", help="Workspace path passed to Cursor Agent")
    parser.add_argument("--output", default="", help="Output JSON path")
    parser.add_argument("--payload-out", default="", help="Optional full payload output path")
    parser.add_argument("--model", default="", help="Optional Cursor model name")
    parser.add_argument("--timeout", type=int, default=0, help="Optional timeout in seconds")
    parser.add_argument("--heartbeat-timeout", type=int, default=30, help="Heartbeat stall threshold in seconds")
    parser.add_argument("--max-runtime", type=int, default=0, help="Optional hard runtime cap in seconds")
    parser.add_argument("--poll-interval", type=int, default=5, help="Heartbeat polling interval in seconds")
    parser.add_argument("--dry-run", action="store_true", help="Only print payload")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    review = find_review(Path(args.reviews_file), args.review_id)
    payload = build_payload(
        prompt_text=read_text(Path(args.prompt_file)),
        codebook_text=read_text(Path(args.codebook_file)),
        review=review,
    )

    if args.payload_out:
        write_text(Path(args.payload_out), payload)

    if args.dry_run:
        print(payload)
        return

    raw_output = run_agent(
        payload=payload,
        workspace=args.workspace,
        model=args.model,
        timeout=args.timeout,
        heartbeat_timeout=args.heartbeat_timeout,
        max_runtime=args.max_runtime,
        poll_interval=args.poll_interval,
    )
    normalized_output = validate_json(raw_output)

    output_path = Path(args.output) if args.output else Path("agent_runs") / f"{args.review_id}.json"
    write_text(output_path, normalized_output + "\n")
    print(str(output_path))


if __name__ == "__main__":
    main()
