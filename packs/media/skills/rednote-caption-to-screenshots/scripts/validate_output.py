#!/usr/bin/env python3
"""
Validate output contract for rednote-caption-to-screenshots.

Usage:
  python3 scripts/validate_output.py "<markdown text>"
  python3 scripts/validate_output.py /path/to/output.md

Exit codes:
  0 - pass
  2 - fail (missing required sections/items)
"""

from __future__ import annotations

import os
import re
import sys
from dataclasses import dataclass
from typing import List, Tuple


@dataclass(frozen=True)
class CheckResult:
    ok: bool
    name: str
    details: str = ""


def _read_input(arg: str) -> str:
    # If arg looks like an existing file path, read it; otherwise treat as inline markdown.
    if os.path.exists(arg) and os.path.isfile(arg):
        with open(arg, "r", encoding="utf-8") as f:
            return f.read()
    return arg


def _has(pattern: str, text: str, flags: int = re.IGNORECASE) -> bool:
    return re.search(pattern, text, flags) is not None


def _count(pattern: str, text: str, flags: int = re.IGNORECASE) -> int:
    return len(re.findall(pattern, text, flags))


def check_required_blocks(md: str) -> List[CheckResult]:
    # Accept flexible headings; focus on semantic anchors.
    required = [
        ("发布配文", r"发布配文|可直接粘贴|可直接发布"),
        ("轮播分镜", r"轮播分镜|分镜|Page\s*1|P1\b"),
        ("产出文件清单", r"产出文件清单|文件清单|HTML\s*文件名|截图命名"),
        ("截图步骤清单", r"截图步骤清单|截图步骤|如何逐页截图|浏览器缩放"),
        ("质量自检清单", r"质量自检清单|自检清单|封面.*3\s*秒|敏感词"),
    ]

    results: List[CheckResult] = []
    for name, pat in required:
        results.append(
            CheckResult(
                ok=_has(pat, md),
                name=name,
                details=("缺少对应段落/关键词锚点" if not _has(pat, md) else ""),
            )
        )
    return results


def check_publish_copy_items(md: str) -> List[CheckResult]:
    # Only run if "发布配文" exists; keep it forgiving.
    if not _has(r"发布配文|可直接粘贴|可直接发布", md):
        return [CheckResult(ok=False, name="发布配文-前置", details="未检测到“发布配文”段落，跳过细项检查")]

    checks: List[Tuple[str, str, str]] = [
        ("发布配文-标题", r"\b标题\b", "缺少“标题”字段（建议给 1-3 个候选）"),
        ("发布配文-正文", r"\b正文\b", "缺少“正文”字段（建议短段落+列表）"),
        ("发布配文-话题标签", r"话题|标签|#\S+", "缺少“话题标签”或未出现任何 #tag"),
        ("发布配文-评论区引导", r"评论区|评论引导|评论区引导", "缺少“评论区引导”字段"),
        ("发布配文-CTA", r"CTA|收藏|评论|私信", "缺少明确 CTA（收藏/评论/私信其一）"),
    ]

    results: List[CheckResult] = []
    for name, pat, hint in checks:
        results.append(CheckResult(ok=_has(pat, md), name=name, details=(hint if not _has(pat, md) else "")))

    # Soft checks (warnings): tag count and storyboard completeness.
    tag_count = _count(r"#([\w\u4e00-\u9fa5]+)", md)
    results.append(
        CheckResult(
            ok=tag_count >= 5,
            name="发布配文-标签数量(建议≥5)",
            details=(f"当前检测到 {tag_count} 个 #tag；建议 8-15 个（含 2-3 个长尾）" if tag_count < 5 else ""),
        )
    )
    return results


def check_storyboard_pages(md: str) -> CheckResult:
    # Look for P1.. or Page 1.. markers.
    p_markers = _count(r"\bP[1-9]\b", md) + _count(r"Page\s*[1-9]\b", md)
    ok = p_markers >= 6  # allow non-8-page variants, but require some structure
    return CheckResult(
        ok=ok,
        name="轮播分镜-页码结构(建议≥6页)",
        details=(f"检测到约 {p_markers} 个页码标记（P1/Page1 等）；建议按 8 页结构写清每页角色" if not ok else ""),
    )


def format_report(results: List[CheckResult]) -> Tuple[bool, str]:
    ok_all = all(r.ok for r in results if not r.name.endswith("前置"))
    lines: List[str] = []
    lines.append("✅ rednote-caption-to-screenshots 输出契约校验")
    lines.append("")
    for r in results:
        status = "PASS" if r.ok else "FAIL"
        lines.append(f"- {status}: {r.name}" + (f" — {r.details}" if (r.details and not r.ok) else ""))
    lines.append("")
    lines.append("提示：本脚本偏“结构完整性校验”，不评判文案好坏；若 FAIL，请补齐缺失字段/段落。")
    return ok_all, "\n".join(lines)


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage:")
        print('  python3 scripts/validate_output.py "<markdown text>"')
        print("  python3 scripts/validate_output.py /path/to/output.md")
        return 2

    md = _read_input(sys.argv[1])

    results: List[CheckResult] = []
    results.extend(check_required_blocks(md))
    results.extend(check_publish_copy_items(md))
    results.append(check_storyboard_pages(md))

    ok, report = format_report(results)
    print(report)
    return 0 if ok else 2


if __name__ == "__main__":
    raise SystemExit(main())

