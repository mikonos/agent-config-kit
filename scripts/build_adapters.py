#!/usr/bin/env python3
"""Build runtime rule and hook adapters from canonical portable sources."""

from __future__ import annotations

import argparse
import base64
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "packs/core/rules/core.md"
MANIFEST = ROOT / "manifest.json"
RULE_TEMPLATES = {
    ROOT / "adapters/codex/AGENTS.md": (
        "<!-- Generated from packs/core/rules/core.md. -->\n\n{body}"
    ),
    ROOT / "adapters/claude-code/CLAUDE.md": (
        "<!-- Generated from packs/core/rules/core.md. -->\n\n{body}"
    ),
    ROOT / "adapters/cursor/agent-config-kit.mdc": (
        "---\n"
        "description: Safe, beginner-friendly working agreement for AI-assisted work\n"
        "alwaysApply: true\n"
        "---\n\n"
        "<!-- Generated from packs/core/rules/core.md. -->\n\n"
        "{body}"
    ),
}


def standard_hook(message: str, windows_command: bool) -> dict:
    standard_payload = {
        "hookSpecificOutput": {
            "hookEventName": "SessionStart",
            "additionalContext": message,
        }
    }
    encoded = base64.b64encode(
        json.dumps(standard_payload, ensure_ascii=False).encode("utf-8")
    ).decode("ascii")
    standard_code = (
        "import base64; print(base64.b64decode('"
        + encoded
        + "').decode('utf-8'))"
    )
    command = {
        "type": "command",
        "command": f'python3 -c "{standard_code}"',
        "timeout": 5,
        "statusMessage": "Loading Agent Config Kit",
    }
    if windows_command:
        command["commandWindows"] = f'py -3 -c "{standard_code}"'
    return {
        "hooks": {
            "SessionStart": [
                {
                    "matcher": "startup|resume|clear|compact",
                    "hooks": [command],
                }
            ]
        }
    }


def cursor_hook(message: str) -> dict:
    payload = {"continue": True, "additional_context": message}
    encoded = base64.b64encode(
        json.dumps(payload, ensure_ascii=False).encode("utf-8")
    ).decode("ascii")
    code = (
        "import base64; print(base64.b64decode('"
        + encoded
        + "').decode('utf-8'))"
    )
    return {
        "version": 1,
        "hooks": {
            "sessionStart": [
                {
                    "command": f'python3 -c "{code}"',
                    "timeout": 5,
                }
            ]
        },
    }


def render() -> dict[Path, str]:
    body = SOURCE.read_text(encoding="utf-8").rstrip() + "\n"
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    rendered = {
        path: template.format(body=body) for path, template in RULE_TEMPLATES.items()
    }
    for profile_name, profile in manifest["profiles"].items():
        message = "\n".join(
            (ROOT / path).read_text(encoding="utf-8").strip()
            for path in profile["hook_messages"]
        )
        for runtime_name, runtime in manifest["runtimes"].items():
            hook_items = runtime["hooks_by_profile"][profile_name]
            if len(hook_items) != 1:
                raise ValueError(
                    f"expected one Hook adapter: {runtime_name}/{profile_name}"
                )
            output = ROOT / hook_items[0]["source"]
            if runtime_name == "cursor":
                payload = cursor_hook(message)
            else:
                payload = standard_hook(message, windows_command=runtime_name == "codex")
                if runtime_name == "codex":
                    payload["description"] = "Agent Config Kit safe startup reminder."
                else:
                    payload = {
                        "$schema": "https://json.schemastore.org/claude-code-settings.json",
                        **payload,
                    }
            rendered[output] = json.dumps(payload, indent=2) + "\n"
    return rendered


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--apply", action="store_true")
    args = parser.parse_args()

    drift: list[Path] = []
    for path, expected in render().items():
        actual = path.read_text(encoding="utf-8") if path.exists() else None
        if actual != expected:
            drift.append(path)
            if args.apply:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(expected, encoding="utf-8")

    if args.check and drift:
        for path in drift:
            print(f"DRIFT: {path.relative_to(ROOT)}", file=sys.stderr)
        return 1
    if args.apply:
        print(f"Updated {len(drift)} adapter(s).")
    else:
        print(f"Adapters current: {len(render())}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
