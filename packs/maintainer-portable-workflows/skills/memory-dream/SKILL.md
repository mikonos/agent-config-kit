---
name: memory-dream
description: 记忆蒸馏：按 Claude Code autoDream/consolidationPrompt 四阶段巩固 memory/、MEMORY.md 与 L1 topic 记忆。关键词：做梦、dream、蒸馏、记忆整理、记忆巩固。
---

# memory-dream

> 设计来源：Claude Code `autoDream.ts` + `consolidationPrompt.ts`。
> 当前实现：auto-dream 门限通过后由后台 `scripts/memory-dream-worker.js` 自动执行；本 skill 是人工/自动 dream 的同一执行协议。

## 边界

只能读写：
- `memory/**`
- 根目录 `MEMORY.md`

只读：
- `memory/open loops.md`
- Cursor/Codex transcript、hook logs、session indexes

禁止写：
- `05_每日记录/**`
- `.cursor/**`
- `.codex/**`
- 源码、项目文档、ZK 正文笔记、transcript 文件

完成后：
- 自动 worker 成功时由 `scripts/lib/auto-dream-core.js` 更新 `memory/dream/.consolidate-lock` 与 `memory/dream/state.json`
- 人工执行完整 Phase 4 后运行 `node scripts/record-memory-dream-consolidated.js`

## Phase 1 - Orient

- `ls memory/`，建立当前记忆层级画面
- 读 `MEMORY.md`，确认 L0 是否超限
- skim `memory/topics/<machine-id>/{user,project,feedback,reference,affect,vault}.md`
- 若 `memory/dream/checkpoint.json` 存在且 24h 内，按 checkpoint 缩小范围

## Phase 2 - Gather Signal

优先级：
1. `memory/YYYYMMDD_<type>_*.md` 原子卡与 `MEMORY.md` 指针
2. L1 topic 中 `## 原子卡索引（memory-dream 维护）` 与旧 `## 来自会话的摘录`
3. `memory/sessions/*/index.md` 近期会话
4. `memory/daily/`、`memory/hook-logs/` 近期条目
5. JSONL transcript 窄 grep，仅在需要具体上下文时使用

不要全量读 transcript；只查已经怀疑重要的线索。

## Phase 3 - Consolidate

- 合并近重复记忆，优先更新已有 L1/atom，不制造平行副本
- 修复被推翻的事实，必须改源文件，不只新增“更新说明”
- 相对日期改绝对日期
- feedback atom 需使用规则陈述 + `**Why:**` + `**How to apply:**`
- project atom 若保存决策/边界，需写事实或决策 + `**Why:**` + `**How to apply:**`
- vault 只保存 `[[链接]]` + hook，不贴整段 ZK 正文
- affect 仅保存短时协作节奏，不写临床化或稳定人格判断

需要体例时才加载：
- `references/cc-feedback-atom-examples-and-template.md`
- `references/l0-l1-six-files-layout.md`
- `references/六文件域L0L1整理执行指南.md`

## Phase 4 - Prune and Index

目标：
- `MEMORY.md` <= 200 行
- `MEMORY.md` <= 25KB
- 每条索引一行，尽量 <= 150 字符

动作：
- Demote 超长 L0 行：细节迁入 L1/atom，L0 留短指针
- 删除 stale、错误、已合并、重复指针
- 新增重要 L1/atom 指针
- 修复 L0/L1/atom 之间的矛盾
- 读取 `memory/open loops.md`，只在报告中列出 >=14 天未处理项，不自动改写

Demote 前按需加载：
- `references/memory-md-example.md`

## 自动触发

CC-style auto-dream 由共享 core 执行门限：
- enabled
- time gate，默认 24h
- scan throttle，默认 10min
- sessions gate，默认 5 sessions
- `.consolidate-lock`

配置来源：
- `memory/dream/config.json`
- `AUTO_MEMORY_DREAM`
- `AUTO_DREAM_MIN_HOURS`
- `AUTO_DREAM_MIN_SESSIONS`
- `AUTO_DREAM_SCAN_MIN_MS`
- `AUTO_DREAM_LOCK_STALE_MS`

观测：
- `memory/dream/status.json`
- `memory/dream/pending-run.json`
- `memory/dream/worker.log`
- `node scripts/codex-memory/check-codex-memory-health.js`

## Report

输出简短报告：
- Consolidated：合并/晋升了什么
- Pruned：修剪/降级/删除了什么
- Files touched：改了哪些文件
- Open loops：只列建议复审项
- Blockers：未完成原因

若无改动，明确写：记忆已整洁，无需修改。
