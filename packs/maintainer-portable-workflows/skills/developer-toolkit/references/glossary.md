# developer-toolkit — 术语表（精简）

| 术语 | 一句话 |
|------|--------|
| **OpenSpec** | 把「变更」收成 proposal/specs/design/tasks，并可 **archive** 进主规格的工具链；CLI 常在 `~/.openclaw` 下用。 |
| **change / change-id** | 一次变更的目录名（kebab-case），在 `openspec/changes/<id>/`。 |
| **spec-driven** | OpenSpec 默认工作流：proposal → specs → design → tasks。 |
| **Apply（openspec apply）** | 按 `tasks.md` 实装并勾选任务；常通过 **`openspec-apply-change`** skill 执行。 |
| **apply-ready** | `openspec status` 显示可进入实现：齐件满足 schema 要求。 |
| **archive** | 变更完成后收进 `openspec/changes/archive/` 并同步主 `specs/`（流程以 CLI/skill 为准）。 |
| **gstack** | 一套以 **slash**（`/review`、`/qa`…）组织的工程化技能集，多在 Claude Code / 已加载的 Cursor Agent 里用。 |
| **gstack-lite / gstack-full / gstack-plan** | OpenClaw 向 CC 会话注入的提示档位：轻纪律 / 全流程 / 只规划 — 见 gstack `docs/OPENCLAW.md`。 |
| **slash** | 以 `/` 开头的 gstack 命令，**不是**终端 shell 命令，需在对应 Agent 环境触发。 |
| **Superpowers skill** | `~/.cursor/skills/<name>/SKILL.md` 一类可组合技能（如 `writing-plans`、`test-driven-development`）。 |
| **developer-toolkit** | 本编排 skill：在阶段间指路，**不**替代各工具正文。 |
| **OpenClaw 派发** | 按任务轻重选 Simple～Plan，决定 spawn 时带多少 gstack 方法论。 |
| **guardrails（硬规则）** | 动 `openclaw.json`/多 agent/协议前必须先有 **OpenSpec change** 等本机约定。 |
