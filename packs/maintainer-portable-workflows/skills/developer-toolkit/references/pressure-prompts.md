# developer-toolkit — 压测用例（TDD for skills）

用法：在**加载 / 不加载** `developer-toolkit` 各跑一轮，观察模型是否仍读主 `SKILL.md` 里的**七阶段表**与**四行输出**，且不把 description 当唯一指令。

## A. 应主要依赖 developer-toolkit（编排 / 阶段 / 安装自检）

1. 「三栈我现在算哪一步？下一步只给一个。」
2. 「developer-toolkit 看一下：要做 OpenSpec change 还是先 /autoplan？」
3. 「openspec、gstack、Superpowers 我现在该动哪一个？」
4. 「刚换电脑，帮我看下这三样装齐没有，缺什么给最短安装命令。」
5. 「产品从想法到上线，按你的表我现在卡在阶段几？」

**期望**：输出 **四行格式**；阶段号 1～7；**唯一**下一步；缺工具时先 **2～4 行** 安装句（可指向 `references/install.md`）。

## B. 应直达具体 skill / 工具，不应只靠 developer-toolkit 糊一层

1. 「按 `openspec-propose` 流程，帮我新建 change `foo-bar`，补齐 proposal 到可 apply。」→ 应 **`openspec-propose`**，而非只给 developer-toolkit 阶段建议。
2. 「对 `https://staging.example.com` 跑 gstack QA，截屏回归。」→ 应 **`gstack-qa` 或 `/qa`**，而非只写「阶段 6」。
3. 「严格按 Superpowers 的 TDD 改这个函数：先写失败测试。」→ 应 **`test-driven-development`**。
4. 「把 `openspec/changes/x/tasks.md` 里未勾项做完并更新 spec。」→ 应 **`openspec-apply-change`**。
5. 「帮我 brainstorm 这个需求的边界，不要阶段表。」→ 应 **`brainstorming`**。

**期望**：模型**选用对应 skill** 并执行其流程；若误用 developer-toolkit，表现为只给阶段号、不打开目标 skill 的步骤。

## C. 回归判据（GREEN）

- A 类：四行输出 + 阶段与「唯一下一步」一致。
- B 类：首轮即选对 skill 名或 slash，且深入该 skill 正文。
- 两类均：**未**用 description 替代阅读 `SKILL.md` 正文（表仍在）。

## D. 基线（RED，可选）

- 故意用**旧版** description（含完整流程摘要）跑一次 A-1，记录模型是否跳过七阶段表 — 用于对比 CSO 修复前后。

## E. 迭代记录（跑测后填）

| 日期 | 用例 | PASS/FAIL | 失败表现（一句） | 改动（ SKILL / description / 其它） |
|------|------|-----------|------------------|--------------------------------------|
| 2026-04-05 | A-1 | PASS | — | 无；无上下文时四行内用「待澄清」+ 唯一追问 |
| 2026-04-05 | A-2 | PASS | — | 无 |
| 2026-04-05 | A-3 | PASS | — | 无 |
| 2026-04-05 | A-4 | PASS | — | 无；本机 openspec+gstack+SP 已齐 |
| 2026-04-05 | A-5 | PASS | — | 同 A-1 |
| 2026-04-05 | B-1 | PASS | — | 无；首轮声明走 `openspec-propose` |
| 2026-04-05 | B-2 | PASS | — | 无；首轮声明 `gstack-qa` / `/qa` |
| 2026-04-05 | B-3 | PASS | — | 无；首轮声明 `test-driven-development` |
| 2026-04-05 | B-4 | PASS | — | 无；首轮声明 `openspec-apply-change` |
| 2026-04-05 | B-5 | PASS | — | 无；首轮声明 `brainstorming`、禁阶段表 |

**单次只改一处**，改完重跑同一用例直到 GREEN；重大行为变更在 `CHANGELOG-skill.md` 记一行。
