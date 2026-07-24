#!/usr/bin/env python3
"""
扫描 ZK core skills，对缺少 vault-writing-preamble 声明的 SKILL.md 自动补入。
用法：python3 add_zk_preamble.py [--dry-run]
"""

import sys
import re
from pathlib import Path

SKILLS_DIR = Path(__file__).parent.parent.parent.parent / "skills"

# ZK core skills：产出笔记、操作知识网络、需要 Iron Law / YAML 规范 / 归位规则
ZK_SKILLS = [
    "deep-learning",
    "deep-reading",
    "file-organize",
    "fleeting-note",
    "index-note",
    "industry-research-os",
    "link-proposer",
    "meeting-note",
    "network-health",
    "note-split",
    "obsidian-cli",
    "open-loops",
    "random-walk",
    "strategic-advisor",
    "structure-note",
    "weekly-report",
]

PREAMBLE_LINE = '> **通用协议**：执行前读取 `.cursor/skills/vault-writing-preamble/SKILL.md`（Iron Law、YAML 规范、indexed 标记、归位快查）。'

def has_preamble(content: str) -> bool:
    return "vault-writing-preamble" in content

def insert_preamble(content: str) -> str:
    """在 frontmatter 结束后（第二个 '---' 之后）插入 preamble 行。"""
    lines = content.split("\n")
    # 找第二个 '---'（frontmatter 结束）
    dash_count = 0
    insert_at = None
    for i, line in enumerate(lines):
        if line.strip() == "---":
            dash_count += 1
            if dash_count == 2:
                insert_at = i + 1
                break

    if insert_at is None:
        print(f"  ⚠️  找不到 frontmatter 结束标记，跳过")
        return content

    # 插入空行 + preamble 行 + 空行
    lines.insert(insert_at, "")
    lines.insert(insert_at + 1, PREAMBLE_LINE)
    lines.insert(insert_at + 2, "")
    return "\n".join(lines)

def main():
    dry_run = "--dry-run" in sys.argv
    if dry_run:
        print("🔍 Dry run 模式（不写入文件）\n")

    fixed = []
    skipped = []
    already_ok = []

    for skill_name in ZK_SKILLS:
        skill_file = SKILLS_DIR / skill_name / "SKILL.md"
        if not skill_file.exists():
            skipped.append(f"{skill_name} (文件不存在)")
            continue

        content = skill_file.read_text(encoding="utf-8")
        if has_preamble(content):
            already_ok.append(skill_name)
            continue

        new_content = insert_preamble(content)
        if new_content == content:
            skipped.append(f"{skill_name} (插入失败)")
            continue

        if not dry_run:
            skill_file.write_text(new_content, encoding="utf-8")
        fixed.append(skill_name)
        print(f"{'[dry] ' if dry_run else ''}✅ 已补入 preamble：{skill_name}")

    print(f"\n📊 结果：补入 {len(fixed)} 个 | 已有 {len(already_ok)} 个 | 跳过 {len(skipped)} 个")
    if skipped:
        print(f"   跳过：{', '.join(skipped)}")

if __name__ == "__main__":
    main()
