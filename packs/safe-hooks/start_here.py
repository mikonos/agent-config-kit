#!/usr/bin/env python3
"""Emit fixed startup context without reading, storing, or transmitting user data."""

import argparse
import json
from pathlib import Path


MESSAGE_PATH = Path(__file__).with_name("message.txt")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--format",
        choices=("codex", "cursor", "claude-code"),
        default="codex",
    )
    args = parser.parse_args()
    message = MESSAGE_PATH.read_text(encoding="utf-8").strip()
    if args.format == "cursor":
        payload = {"continue": True, "additional_context": message}
    else:
        payload = {
            "hookSpecificOutput": {
                "hookEventName": "SessionStart",
                "additionalContext": message,
            }
        }
    print(json.dumps(payload, ensure_ascii=False))


if __name__ == "__main__":
    main()
