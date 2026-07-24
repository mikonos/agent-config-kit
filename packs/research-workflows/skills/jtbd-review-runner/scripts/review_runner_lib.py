#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
import re
import subprocess
import time
from pathlib import Path


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def find_review(path: Path, review_id: str) -> dict[str, str]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            if row.get("review_id") == review_id:
                return row
    raise SystemExit(f"Review not found: {review_id}")


def build_review_block(review: dict[str, str]) -> str:
    return "\n".join(
        [
            f"review_id: {review.get('review_id', '')}",
            f"rating: {review.get('rating', '')}",
            f"verified_purchase: {review.get('verified_purchase', '')}",
            f"date: {review.get('date', '')}",
            f"title: {review.get('title_raw', '')}",
            f"content: {review.get('content_raw', '')}",
        ]
    )


def build_payload(prompt_text: str, codebook_text: str, review: dict[str, str]) -> str:
    return (
        f"{prompt_text.strip()}\n\n"
        "## 码本参考\n\n"
        f"{codebook_text.strip()}\n\n"
        "## 输入\n\n"
        "```text\n"
        f"{build_review_block(review)}\n"
        "```"
    )


def _workspace_slug_prefix(workspace: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9]+", "-", workspace).strip("-")
    return cleaned[:48]


def _cursor_project_roots(workspace: str) -> list[Path]:
    projects_dir = Path.home() / ".cursor" / "projects"
    if not projects_dir.exists():
        return []
    prefix = _workspace_slug_prefix(workspace)
    roots = [path for path in projects_dir.iterdir() if path.is_dir() and path.name.startswith(prefix)]
    roots.sort(key=lambda p: p.stat().st_mtime, reverse=True)
    return roots


def _latest_heartbeat_mtime(workspace: str) -> float:
    latest = 0.0
    for root in _cursor_project_roots(workspace):
        for candidate in [root / "worker.log"]:
            if candidate.exists():
                latest = max(latest, candidate.stat().st_mtime)
        for base in [root / "agent-transcripts", root / "chats"]:
            if not base.exists():
                continue
            for path in base.rglob("*"):
                if not path.is_file():
                    continue
                if path.name == "worker.log" or path.suffix == ".jsonl" or path.name.startswith("store.db"):
                    latest = max(latest, path.stat().st_mtime)
    return latest


def run_agent(
    payload: str,
    workspace: str,
    model: str = "",
    timeout: int = 0,
    heartbeat_timeout: int = 30,
    max_runtime: int = 0,
    poll_interval: int = 5,
) -> str:
    command = [
        "agent",
        "-p",
        "--output-format",
        "text",
        "--trust",
        "--workspace",
        workspace,
        payload,
    ]
    if model:
        command[1:1] = ["--model", model]

    try:
        process = subprocess.Popen(
            command,
            text=True,
            encoding="utf-8",
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    except FileNotFoundError as exc:
        raise SystemExit("`agent` CLI not found. Please install Cursor Agent first.") from exc

    started_at = time.time()
    last_heartbeat = max(started_at, _latest_heartbeat_mtime(workspace))

    while process.poll() is None:
        now = time.time()
        heartbeat = _latest_heartbeat_mtime(workspace)
        if heartbeat > last_heartbeat:
            last_heartbeat = heartbeat

        if max_runtime > 0 and (now - started_at) > max_runtime:
            process.kill()
            process.communicate()
            raise SystemExit(f"Agent exceeded max runtime of {max_runtime} seconds.")

        if timeout > 0 and (now - started_at) > timeout:
            if (now - last_heartbeat) > heartbeat_timeout:
                process.kill()
                process.communicate()
                raise SystemExit(
                    f"Agent run timed out after {timeout} seconds with no heartbeat for {heartbeat_timeout} seconds."
                )

        time.sleep(max(1, poll_interval))

    stdout, stderr = process.communicate()
    stdout = stdout.strip()
    stderr = stderr.strip()
    if process.returncode != 0:
        raise SystemExit(stderr or stdout or f"Agent exited with code {process.returncode}")
    if stderr and not stdout:
        raise SystemExit(stderr)
    return stdout


def validate_json(text: str) -> str:
    try:
        parsed = json.loads(text)
    except json.JSONDecodeError as exc:
        raise SystemExit(
            "Agent output is not valid JSON. Re-run with payload output enabled to inspect the full prompt."
        ) from exc
    return json.dumps(parsed, ensure_ascii=False, indent=2)


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
