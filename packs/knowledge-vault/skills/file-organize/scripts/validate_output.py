#!/usr/bin/env python3
"""
Validate the markdown output of the file-organize skill.

Usage:
  python3 scripts/validate_output.py "<markdown-output>"

Exit codes:
  0 = OK
  1 = Missing required sections / insufficient links
"""

import re
import sys


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: validate_output.py \"<markdown-output>\"", file=sys.stderr)
        return 1

    text = sys.argv[1]

    required_markers = [
        "📁 归类结果",
        "🔗 连接建立",
        "✅ 质量检查",
    ]
    missing = [m for m in required_markers if m not in text]
    if missing:
        print("MISSING sections:", ", ".join(missing))
        return 1

    # Require at least 2 wiki-style links [[...]]
    links = re.findall(r"\[\[[^\]]+\]\]", text)
    if len(links) < 2:
        print(f"NOT ENOUGH LINKS: found {len(links)}, require >= 2")
        return 1

    # Require file/path/type fields
    must_have_fields = [
        "文件：`",
        "类型：[",
        "路径：`",
    ]
    missing_fields = [f for f in must_have_fields if f not in text]
    if missing_fields:
        print("MISSING fields:", ", ".join(missing_fields))
        return 1

    print("OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

