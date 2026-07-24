#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import time
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
    parser = argparse.ArgumentParser(description="Run a batch of reviews from a file through Cursor Agent.")
    parser.add_argument("--review-ids-file", required=True, help="Path to a newline-delimited review id file")
    parser.add_argument("--reviews-file", required=True, help="Path to clean_reviews.csv")
    parser.add_argument("--prompt-file", required=True, help="Path to prompt markdown")
    parser.add_argument("--codebook-file", required=True, help="Path to codebook markdown")
    parser.add_argument("--workspace", default=".", help="Workspace path passed to Cursor Agent")
    parser.add_argument("--output-dir", required=True, help="Directory for JSON outputs")
    parser.add_argument("--summary-out", required=True, help="Summary JSON path")
    parser.add_argument("--payload-dir", default="", help="Optional directory to save payloads")
    parser.add_argument("--model", default="", help="Optional Cursor model name")
    parser.add_argument("--timeout", type=int, default=0, help="Optional timeout in seconds")
    parser.add_argument("--heartbeat-timeout", type=int, default=30, help="Heartbeat stall threshold in seconds")
    parser.add_argument("--max-runtime", type=int, default=0, help="Optional hard runtime cap in seconds")
    parser.add_argument("--poll-interval", type=int, default=5, help="Heartbeat polling interval in seconds")
    parser.add_argument("--max-retries", type=int, default=0, help="Retry count for timeout/error cases")
    parser.add_argument("--retry-backoff-seconds", type=int, default=3, help="Seconds to wait before retrying")
    parser.add_argument("--force-rerun", action="store_true", help="Re-run reviews even if output JSON already exists")
    return parser.parse_args()


def build_result(review_id: str, status: str, output_path: str, payload_path: str, error: str) -> dict[str, str]:
    return {
        "review_id": review_id,
        "status": status,
        "output_path": output_path,
        "payload_path": payload_path,
        "error": error,
    }


def write_summary(summary_path: Path, output_dir: Path, review_ids: list[str], results: list[dict[str, str]]) -> None:
    summary = {
        "total_reviews": len(review_ids),
        "ok_count": sum(1 for item in results if item["status"] == "ok"),
        "error_count": sum(1 for item in results if item["status"] == "error"),
        "timeout_count": sum(1 for item in results if item["status"] == "timeout"),
        "skipped_count": sum(1 for item in results if item["status"] == "skipped"),
        "output_dir": str(output_dir),
        "results": results,
    }
    write_text(summary_path, json.dumps(summary, ensure_ascii=False, indent=2) + "\n")


def try_run_review(
    review_id: str,
    payload: str,
    output_path: Path,
    payload_path: str,
    workspace: str,
    model: str,
    timeout: int,
    heartbeat_timeout: int,
    max_runtime: int,
    poll_interval: int,
    max_retries: int,
    retry_backoff_seconds: int,
) -> dict[str, str]:
    attempt = 0
    last_error = ""
    while attempt <= max_retries:
        try:
            raw_output = run_agent(
                payload=payload,
                workspace=workspace,
                model=model,
                timeout=timeout,
                heartbeat_timeout=heartbeat_timeout,
                max_runtime=max_runtime,
                poll_interval=poll_interval,
            )
            normalized_output = validate_json(raw_output)
            write_text(output_path, normalized_output + "\n")
            return build_result(review_id, "ok", str(output_path), payload_path, "")
        except SystemExit as exc:
            last_error = str(exc)
            if attempt == max_retries:
                status = "timeout" if "timed out" in last_error.lower() else "error"
                return build_result(review_id, status, "", payload_path, last_error)
            time.sleep(retry_backoff_seconds)
            attempt += 1
    return build_result(review_id, "error", "", payload_path, last_error or "Unknown runner failure")


def main() -> None:
    args = parse_args()
    review_ids = [
        line.strip()
        for line in Path(args.review_ids_file).read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    reviews_path = Path(args.reviews_file)
    prompt_text = read_text(Path(args.prompt_file))
    codebook_text = read_text(Path(args.codebook_file))
    output_dir = Path(args.output_dir)
    payload_dir = Path(args.payload_dir) if args.payload_dir else None
    summary_path = Path(args.summary_out)
    results: list[dict[str, str]] = []

    for review_id in review_ids:
        output_path = output_dir / f"{review_id}.json"
        payload_path = str(payload_dir / f"{review_id}.txt") if payload_dir else ""

        if output_path.exists() and not args.force_rerun:
            results.append(build_result(review_id, "skipped", str(output_path), payload_path, ""))
            write_summary(summary_path, output_dir, review_ids, results)
            print(f"SKIP {review_id} -> {output_path}")
            continue

        review = find_review(reviews_path, review_id)
        payload = build_payload(prompt_text=prompt_text, codebook_text=codebook_text, review=review)

        if payload_dir:
            write_text(Path(payload_path), payload)

        result = try_run_review(
            review_id=review_id,
            payload=payload,
            output_path=output_path,
            payload_path=payload_path,
            workspace=args.workspace,
            model=args.model,
            timeout=args.timeout,
            heartbeat_timeout=args.heartbeat_timeout,
            max_runtime=args.max_runtime,
            poll_interval=args.poll_interval,
            max_retries=args.max_retries,
            retry_backoff_seconds=args.retry_backoff_seconds,
        )
        results.append(result)
        write_summary(summary_path, output_dir, review_ids, results)
        if result["status"] == "ok":
            print(f"OK {review_id} -> {output_path}")
        else:
            print(f"{result['status'].upper()} {review_id} -> {result['error']}")

    write_summary(summary_path, output_dir, review_ids, results)
    print(f"SUMMARY -> {summary_path}")


if __name__ == "__main__":
    main()
