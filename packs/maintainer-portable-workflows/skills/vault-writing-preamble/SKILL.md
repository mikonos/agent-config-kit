---
name: vault-writing-preamble
description: ZK 核心 Skill 通用协议（Iron Law、YAML 规范、indexed 标记、归位快查）。所有核心 ZK Skill 执行前读取。
---

# ZK Skill 通用协议

> 本文件由所有核心 ZK Skill 在执行前读取，提供统一行为约束。低频目录、compiled-wiki、网络分层与 L1 细节见 `references/vault-operating-contract.md`。

---

## Iron Law（强制，不可跳过）

1. **读文件前不修改**：遇路径歧义或文件不存在，先用 Glob/Grep 查证，不允许基于假设修改
2. **三次失败停止**：连续 3 次工具调用失败，立即停止并向用户说明原因，不继续猜测

## 图谱写入授权

仅当用户已授权创建或修改 Vault 知识笔记时，以下属于该任务内常规、非破坏性知识网络维护，**不需要逐项重复确认**：
- 链接写入：在目标笔记和相关笔记中添加 `[[双链]]`
- 索引更新：向 `03_索引/` 与 `03_索引/00_索引_关键词总表.md` 添加或调整入口
- 入网标记：在已完成入网校验的笔记 frontmatter 写入 `indexed: true`

需要暂停询问的情况：删除文件、移动/重命名大量文件、归属明显不确定、会覆盖用户原文、或连续 3 次校验失败。

---

## YAML 必填字段（快速参考）

```yaml
date: YYYYMMDD
source_skill: [skill 名，无 skill 时写「无」]
epistemic_status: borrowed   # 五档见下
description: ...             # 费曼式洞察，100字内
type: Atomic_Note            # 按笔记类型填写
tags: [领域1, 领域2]
links:
  - "[[相关笔记]]"
title: ...                   # 可选
```

必填字段：`date`、`source_skill`、`epistemic_status`、`description`、`type`、`tags`、`links`；`title` 可选。键名与 `epistemic_status` 枚举使用英文。

**epistemic_status 五档**（键名和取值均用英文）：
- `borrowed`：引用他人结论，未亲测
- `empirical`：基于一手数据
- `working`：有支撑的工作假设
- `speculative`：推测，依据薄弱
- `confident`：多次验证，高度可信

低频边界见 `references/vault-operating-contract.md`；不得把 runtime mirror 当作本规范的上游真源。

---

## indexed 标记规范

入网完成后：在 YAML frontmatter 添加 `indexed: true`
**禁止**：在文档末尾写「归网：✅」

---

## 归位快查

```
闪念/未消化       → 000_收件箱/
用户指定项目名    → 00_收件箱_工作区/projects/[项目名]/
MOC/索引笔记      → 03_索引/
编译/当前共识层   → 04_compiled-wiki/[主题]/（先读局部 AGENTS/schema/index 并核对 raw truth）
日志/记忆（统一条目、deep-reading Intent 等） → memory/daily/<machine-id>/YYYY-MM-DD.md
Hook 面包屑       → memory/hook-logs/<machine-id>/YYYY-MM-DD.md（仅 Hook，勿手改）
其他所有笔记      → 05_每日记录/YYYY/MM/YYYYMMDD/  ← 默认
```

- **`<machine-id>`**：与 Hook 共用规则——优先环境变量 `ZK_MACHINE_ID`，否则为清洗后的 hostname，空则 `unknown`。
- **解析本机当日路径**：在 Vault 根执行 `node .cursor/scripts/print-daily-memory-path.js`（stdout 即为应写入的绝对路径）。
- **历史**：`memory/` 根目录下旧版 `YYYY-MM-DD.md` 仅作归档只读；**新写入不得**再用根路径，以免多机坚果云冲突。

命名：`YYYYMMDD_具体描述.md`

---

## GTD 承诺检查

新承诺统一走 **GTD**；旧 open loops 只作 legacy 查询/参考。

- **非 GTD 主任务带出的新承诺**：凡需老板本人执行、等待、确认、追踪的事项 → 调用 `dry run gtd-capture`，只输出 GTD 归位建议；老板确认后调用正式 `gtd-harness` capture / update 写入 `memory/gtd/`。
- **显式 GTD 请求**：直接按 `.cursor/skills/gtd-harness/SKILL.md` 路由；写前读取目标清单，写后读回验证。
- **旧 open loops 查询**：用户明确要看历史 `memory/open loops.md` → 调用 `open-loops` skill 的 legacy query，只读输出。
- **旧议程参考**：1:1 或项目会前若需要旧条目上下文 → 调用 legacy agenda 生成参考；会后新行动仍走 `dry run gtd-capture`。
- **旧条目闭环**：用户明确指向旧 open loops 条目并宣告完成 → 先给 legacy close proposal，老板确认后再处理；未确认不改文件。
