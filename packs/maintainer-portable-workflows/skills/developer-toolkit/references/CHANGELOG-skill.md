# developer-toolkit skill 变更日志

仅记 **行为/触发/结构** 变化，便于回归压测。

| 日期 | 摘要 |
|------|------|
| 2026-04-06 | Eval+Improve：Step 0 强化为强制前置；路由表加说明栏并指定具体 skill 名；输出格式加"永远只给一个工具"原则；CHANGELOG 更新。 |
| 2026-04-06 | 核心重构：从"七阶段+引导提问"改为"先读产出→推断缺口→路由工具"；去除最后 OpenClaw 残留引用；`install.md` 移除 OpenClaw 路径约定；SKILL.md 从67行缩至56行。 |
| 2026-04-05 | 初版；`references/install.md`、`pressure-prompts.md`、`examples.md`；主 SKILL &lt;50 行。 |
| 2026-04-05 | 增 `CHANGELOG-skill.md`、`pressure-prompts` §E 迭代表；`clawd/.cursor/context/active-files.json` 纳入 `developer-toolkit/SKILL.md`（易触发上下文）。 |
| 2026-04-05 | 按 `pressure-prompts` A-1…A-5、B-1…B-5 跑一轮，§E 全 PASS（本机 A-4 三件套已齐）。 |
| 2026-04-05 | 增 `references/onboarding.md`（三线）、`references/glossary.md`；主 SKILL 加读者引导两行，description 未改。 |
| 2026-04-05 | References 改为按 **skill 名** 指向 openspec-*，去掉 `../` 路径。 |
