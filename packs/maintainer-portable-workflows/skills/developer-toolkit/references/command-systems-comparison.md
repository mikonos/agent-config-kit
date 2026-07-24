# 命令系统对比：GSD · OpenSpec · Superpowers · GStack

> 来源：AI-Zettelkasten 集成调研 | 更新：2026-04-12

---

## 用途明细表（命令可跨用途出现）

> 注：同一命令可在多个用途中出现，以 `·` 分隔表示跨用途复用

### A. 项目初始化

| 用途 | GSD | OpenSpec | Superpowers | GStack |
|------|-----|----------|-------------|--------|
| **从头开始新项目** | `/gsd-new-project` | `openspec init` | — | — |
| **建立项目节奏/里程碑** | `/gsd-new-milestone` · `/gsd-complete-milestone` · `/gsd-audit-milestone` · `/gsd-milestone-summary` · `/gsd-plan-milestone-gaps` | — | — | — |

---

### B. 需求与想法

| 用途 | GSD | OpenSpec | Superpowers | GStack |
|------|-----|----------|-------------|--------|
| **需求/想法描述** | — | `/openspec-propose` | `/superpowers:brainstorming` | `/gstack-office-hours` (Builder模式·设计伙伴) |
| **变更级提案** | — | `/openspec-propose` | — | — |
| **open loops收拢** | — | — | — | `/gstack-learn` (读open loops) |

---

### C. 规划与决策

| 用途 | GSD | OpenSpec | Superpowers | GStack |
|------|-----|----------|-------------|--------|
| **战略方向/创始人困惑** | — | — | — | `/gstack-office-hours` (Startup模式·六问聚焦) |
| **制定执行计划** | `/gsd-plan-phase` · `/gsd-next` | — | `/superpowers:writing-plans` | — |
| **多角度评审规划** | — | — | — | `/gstack-autoplan` |
| **战略评审** | — | — | — | `/gstack-plan-ceo-review` |
| **架构评审** | — | — | — | `/gstack-plan-eng-review` |
| **设计维度评审** | — | — | — | `/gstack-plan-design-review` · `/gstack-design-shotgun` |
| **开发者体验评审** | — | — | — | `/gstack-plan-devex-review` |
| **讨论/团队对齐** | `/gsd-discuss-phase` | — | — | — |

---

### D. 执行

| 用途 | GSD | OpenSpec | Superpowers | GStack |
|------|-----|----------|-------------|--------|
| **执行任务** | `/gsd-do` · `/gsd-execute-phase` · `/gsd-fast` · `/gsd-quick` | — | `/superpowers:executing-plans` | — |
| **实现OpenSpec变更** | — | `/openspec-apply-change` | — | — |
| **研究/调研** | `/gsd-research-phase` · `/gsd-intel` | — | — | — |
| **探索代码库** | `/gsd-explore` · `/gsd-map-codebase` · `/gsd-scan` | — | — | — |
| **依赖分析** | `/gsd-analyze-dependencies` | — | — | — |

---

### E. 调试与测试

| 用途 | GSD | OpenSpec | Superpowers | GStack |
|------|-----|----------|-------------|--------|
| **调试/问题排查** | `/gsd-debug` · `/gsd-forensics` | — | `/superpowers:systematic-debugging` | `/gstack-investigate` |
| **测试** | `/gsd-add-tests` | — | `/superpowers:test-driven-development` | `/gstack-qa` · `/gstack-qa-only` |

---

### F. 代码与质量

| 用途 | GSD | OpenSpec | Superpowers | GStack |
|------|-----|----------|-------------|--------|
| **代码审查** | `/gsd-code-review` · `/gsd-review` · `/gsd-eval-review` | — | `/superpowers:requesting-code-review` · `/superpowers:receiving-code-review` | `/gstack-review` · `/gstack-review-read` |
| **验证** | `/gsd-validate-phase` · `/gsd-audit-uat` | `openspec validate` | `/superpowers:verification-before-completion` | — |
| **健康检查** | `/gsd-health` · `/gsd-stats` | — | — | `/gstack-health` · `/gstack-benchmark` |
| **安全审查** | `/gsd-secure-phase` | — | — | `/gstack-cso` · `/gstack-careful` · `/gstack-guard` |

---

### G. 设计

| 用途 | GSD | OpenSpec | Superpowers | GStack |
|------|-----|----------|-------------|--------|
| **设计系统建立** | — | — | — | `/gstack-design-consultation` |
| **设计稿→代码** | — | — | — | `/gstack-design-html` |
| **视觉QA** | — | — | — | `/gstack-design-review` |
| **UI设计阶段** | `/gsd-ui-phase` | — | — | — |

---

### H. 交付与部署

| 用途 | GSD | OpenSpec | Superpowers | GStack |
|------|-----|----------|-------------|--------|
| **交付/开PR** | `/gsd-ship` | — | `/superpowers:finishing-a-development-branch` | `/gstack-ship` |
| **完整部署流水线** | — | — | — | `/gstack-land-and-deploy` |
| **发版后文档同步** | `/gsd-docs-update` | — | — | `/gstack-document-release` |
| **里程碑完成** | `/gsd-complete-milestone` | — | — | — |

---

### I. 协同与归档

| 用途 | GSD | OpenSpec | Superpowers | GStack |
|------|-----|----------|-------------|--------|
| **变更归档** | — | `/openspec-archive-change` | — | — |
| **规格管理** | — | `openspec spec` · `openspec view` · `openspec list` | — | — |
| **团队协作** | `/gsd-thread` · `/gsd-workstreams` | — | `/superpowers:dispatching-parallel-agents` · `/superpowers:subagent-driven-development` | — |
| **回顾/复盘** | — | — | — | `/gstack-retro` |

---

### J. 浏览器与QA

| 用途 | GSD | OpenSpec | Superpowers | GStack |
|------|-----|----------|-------------|--------|
| **无头浏览器QA** | — | — | — | `/gstack-browse` |
| **可见浏览器观察** | — | — | — | `/gstack-open-gstack-browser` |
| **金丝雀监控** | — | — | — | `/gstack-canary` |
| **Cookie导入** | — | — | — | `/gstack-setup-browser-cookies` |

---

### K. 安全与冻结

| 用途 | GSD | OpenSpec | Superpowers | GStack |
|------|-----|----------|-------------|--------|
| **冻结编辑范围** | — | — | — | `/gstack-freeze` · `/gstack-unfreeze` |
| **保存/恢复检查点** | — | — | — | `/gstack-checkpoint` |

---

### L. 知识与学习

| 用途 | GSD | OpenSpec | Superpowers | GStack |
|------|-----|----------|-------------|--------|
| **会话回顾/总结** | `/gsd-session-report` · `/gsd-extract_learnings` | — | — | `/gstack-learnings-log` · `/gstack-learnings-search` · `/gstack-timeline-read` |
| **学习管理** | — | — | — | `/gstack-learn` |
| **遥测/分析** | — | — | — | `/gstack-analytics` · `/gstack-telemetry-log` · `/gstack-telemetry-sync` |

---

### M. 分支与工作区

| 用途 | GSD | OpenSpec | Superpowers | GStack |
|------|-----|----------|-------------|--------|
| **分支管理** | `/gsd-pr-branch` · `/gsd-undo` · `/gsd-reapply-patches` | — | `/superpowers:using-git-worktrees` | — |
| **工作区管理** | `/gsd-new-workspace` · `/gsd-list-workspaces` · `/gsd-remove-workspace` | — | — | `/gstack-repo-mode` |
| **待办管理** | `/gsd-add-todo` · `/gsd-add-backlog` · `/gsd-check-todos` · `/gsd-review-backlog` | — | — | — |

---

### N. 工具与配置

| 用途 | GSD | OpenSpec | Superpowers | GStack |
|------|-----|----------|-------------|--------|
| **Help/设置** | `/gsd-help` · `/gsd-settings` | `openspec config` | `/superpowers:using-superpowers` · `/superpowers:writing-skills` | `/gstack-config` · `/gstack-upgrade` |
| **升级** | `/gsd-update` | `openspec update` | — | `/gstack-upgrade` |
| **导入/迁移** | `/gsd-import` · `/gsd-from-gsd2` | — | — | `/gstack-global-discover` · `/gstack-relink` |
| **部署配置** | — | — | — | `/gstack-setup-deploy` |
| **其他工具** | `/gsd-cleanup` · `/gsd-join-discord` | `openspec feedback` | — | `/gstack-slug` · `/gstack-patch-names` · `/gstack-extension` |

---

## 用途详解：同一用途下的工具差异

### 从头开始新项目

| 命令 | 差异 |
|------|------|
| `/gsd-new-project` | 创建完整的 GSD 项目结构（`.planning/` + 里程碑 + 工作流），适合有节奏感的项目驱动开发 |
| `openspec init` | 初始化 OpenSpec 规格目录，仅建规格框架，不管项目节奏 |

---

### 需求/想法描述

| 命令 | 差异 |
|------|------|
| `/openspec-propose` | 产出变更级 proposal（proposal.md + design.md + tasks.md 三件套），适合已明确的变更项 |
| `/superpowers:brainstorming` | 探索性对话，先理解再设计，适合需求模糊、需要多方收敛的场景 |
| `/gstack-office-hours` (Builder) | YC Builder 模式，设计思维脑暴，适合边做边想的黑客/开源/学习场景；产出 design doc |

---

### 战略方向/创始人困惑

| 命令 | 差异 |
|------|------|
| `/gstack-office-hours` (Startup) | YC Startup 模式，六问聚焦（需求现实/现状/最窄楔子/观察/未来适配），挑战创始人前提；使用前先跑 office-hours 再跑 plan-ceo-review |
| `/gstack-plan-ceo-review` | 战略评审，接在 office-hours 后跑，更激进的挑战和扩展 |

---

### 制定执行计划

| 命令 | 差异 |
|------|------|
| `/gsd-plan-phase` | GSD 项目内某阶段的规划（里程碑级），有明确产出文件 |
| `/gsd-next` | 极简下一步推荐，适合快速推进不需完整规划的场景 |
| `/superpowers:writing-plans` | 结构化执行计划，有验收标准，适合已定方向需拆解 |

---

### 多角度评审规划

| 命令 | 差异 |
|------|------|
| `/gstack-autoplan` | 多评审角度并行跑一次（CEO/Eng/Design/DX），适合重大决策前 |
| `/gstack-plan-ceo-review` | 战略级审查，挑战前提假设，适合创始人/高管视角 |
| `/gstack-plan-eng-review` | 架构与数据流审查，适合工程实现前 |
| `/gstack-plan-design-review` | 设计维度评审，适合设计方案未确认前 |
| `/gstack-plan-devex-review` | DX/API 设计评审，适合开发者体验相关的决策 |

---

### 执行任务

| 命令 | 差异 |
|------|------|
| `/gsd-do` | GSD 命令式执行，直接跑任务不管流程 |
| `/gsd-execute-phase` | 按 GSD 阶段计划执行，有检查点和验收 |
| `/gsd-fast` | 极简快速执行，少流程少验证 |
| `/gsd-quick` | 快速任务，轻量执行 |
| `/superpowers:executing-plans` | 按结构化计划执行，带验收标准 |

---

### 代码审查

| 命令 | 差异 |
|------|------|
| `/gsd-code-review` | 全面代码审查，有结构化 checklist |
| `/gsd-review` | 通用审查，较轻量 |
| `/gsd-eval-review` | 评估导向的审查，重点在质量打分 |
| `/superpowers:requesting-code-review` | 发起代码审查请求，适合自己做完找人 review |
| `/superpowers:receiving-code-review` | 接收审查反馈，适合被 review 时用 |
| `/gstack-review` | gstack 原生 review，覆盖设计与功能 |
| `/gstack-review-read` | 读已存在的 review 报告，不重新跑 |

---

### 调试/问题排查

| 命令 | 差异 |
|------|------|
| `/gsd-debug` | 开发调试，专注代码问题 |
| `/gsd-forensics` | 取证式深度分析，适合疑难杂症 |
| `/superpowers:systematic-debugging` | 四阶段系统调试（假设→验证→定位→修复），适合复杂 bug |
| `/gstack-investigate` | 调查模式，覆盖浏览器+服务器端+代码全链路 |

---

### 测试

| 命令 | 差异 |
|------|------|
| `/gsd-add-tests` | 在代码里新增测试用例 |
| `/superpowers:test-driven-development` | TDD 完整流程（红→绿→重构），适合新功能/核心逻辑 |
| `/gstack-qa` | 系统功能测试 + 发现 bug 自动修，适合完整验收 |
| `/gstack-qa-only` | 只测不修，输出 bug 报告，适合只做 QA 不动手修的场景 |

---

### 交付/部署

| 命令 | 差异 |
|------|------|
| `/gsd-ship` | GSD 风格提交+推送+开 PR |
| `/gsd-complete-milestone` | 里程碑完成，收尾该项目阶段 |
| `/superpowers:finishing-a-development-branch` | 分支收尾 + 检查清单，适合开发分支完成准备合并 |
| `/gstack-ship` | gstack 风格落地，合并 + 推送 |
| `/gstack-land-and-deploy` | 合 PR + 等 CI + 验生产，适合完整交付流 |

---

### 健康检查

| 命令 | 差异 |
|------|------|
| `/gsd-health` | 代码质量综合评分 |
| `/gsd-stats` | 工作量/速度统计 |
| `openspec validate` | 验证 OpenSpec 规格与实现一致性 |
| `/gstack-health` | gstack 健康检查，覆盖更广 |
| `/gstack-benchmark` | 性能基线对比，适合发版前性能验证 |

---

### 会话回顾/总结

| 命令 | 差异 |
|------|------|
| `/gsd-session-report` | 本次 Claude Code 会话的工作摘要 |
| `/gsd-extract_learnings` | 从会话中提取可重用的学习 |
| `/gstack-learnings-log` | 记录 learnings 到持久化存储 |
| `/gstack-learnings-search` | 搜索已有 learnings |
| `/gstack-timeline-read` | 读时间线记录，适合回顾历史操作 |

---

### 团队协作

| 命令 | 差异 |
|------|------|
| `/gsd-thread` | 将任务线程化，适合多人并行处理 |
| `/gsd-workstreams` | 管理工作流，适合多线并行 |
| `/superpowers:dispatching-parallel-agents` | 并行调度多个子 agent，适合复杂任务分解 |
| `/superpowers:subagent-driven-development` | 子 agent 驱动开发，适合大规模任务分解执行 |

---

### 安全审查

| 命令 | 差异 |
|------|------|
| `/gsd-secure-phase` | GSD 安全阶段，带检查清单 |
| `/gstack-cso` | 首席安全官模式，完整安全审计（供应链/密钥/OWASP/STRIDE） |
| `/gstack-careful` | 危险命令警告（rm -rf / force push / DROP TABLE） |
| `/gstack-guard` | careful + freeze 最高安全模式 |

---

### 设计

| 命令 | 差异 |
|------|------|
| `/gsd-ui-phase` | GSD UI 设计阶段 |
| `/gstack-design-consultation` | 从零建立设计系统（色彩/字体/间距） |
| `/gstack-design-shotgun` | 多方案视觉探索对比，适合方案未定时 |
| `/gstack-plan-design-review` | 设计计划评审，设计方向确认前 |
| `/gstack-design-html` | 设计稿/mockup → 生产级 HTML/CSS |
| `/gstack-design-review` | 线上视觉 QA，截图验证迭代 |

---

### 浏览器/QA

| 命令 | 差异 |
|------|------|
| `/gstack-browse` | 无头浏览器交互，适合自动化 QA |
| `/gstack-open-gstack-browser` | 可见浏览器窗口 + 侧栏观察 AI 操作，适合需要看 AI 在干啥 |
| `/gstack-canary` | 部署后持续监控（错误/性能/截图），适合金丝雀发布监控 |

---

### 冻结/检查点

| 命令 | 差异 |
|------|------|
| `/gstack-freeze` | 限制编辑范围到指定目录，防误改 |
| `/gstack-unfreeze` | 解除冻结 |
| `/gstack-checkpoint` | 保存+恢复工作状态（git + 决策 + 剩余任务） |

---

### 验证

| 命令 | 差异 |
|------|------|
| `/gsd-validate-phase` | GSD 阶段验收 |
| `/gsd-audit-uat` | UAT 测试审计 |
| `openspec validate` | OpenSpec 规格一致性验证 |
| `/superpowers:verification-before-completion` | 完成前对抗性验证，适合防止遗漏 |

---

### 讨论/评审

| 命令 | 差异 |
|------|------|
| `/gsd-discuss-phase` | GSD 讨论阶段，适合团队对齐 |
| `/gstack-plan-devex-review` | DevEx 计划评审，适合开发者体验决策 |

---

### YC办公室时间

| 命令 | 差异 |
|------|------|
| `/gstack-office-hours` | 两种模式：① **Startup**（六问聚焦战略方向，使用后接 plan-ceo-review） ② **Builder**（设计思维脑暴，适合边做边想） |

---

## 快速路由表（简化版）

| 用途 | 首选 | 备选 |
|------|------|------|
| 新项目 | `/gsd-new-project` | `openspec init` |
| 想法/需求 | `/superpowers:brainstorming` | `/gstack-office-hours` (Builder) |
| 战略方向/创始人困惑 | `/gstack-office-hours` (Startup) | `/gstack-plan-ceo-review` |
| 制定计划 | `/superpowers:writing-plans` | `/gsd-plan-phase` |
| 多角度评审 | `/gstack-autoplan` | — |
| 执行任务 | `/gsd-execute-phase` | `/gsd-do` |
| 代码审查 | `/gstack-review` | `/gsd-code-review` |
| 调试 | `/superpowers:systematic-debugging` | `/gsd-debug` |
| 测试+修bug | `/gstack-qa` | `/gsd-add-tests` |
| 交付部署 | `/gstack-land-and-deploy` | `/gsd-ship` |
| 设计系统 | `/gstack-design-consultation` | — |
| 视觉QA | `/gstack-design-review` | — |
| 安全审计 | `/gstack-cso` | `/gsd-secure-phase` |
| 浏览器QA | `/gstack-browse` | — |

---

## 系统定位

| 系统 | 命令数量 | 定位 |
|------|---------|------|
| **GSD** | 72条 | 开发工作流（规划→执行→交付） |
| **OpenSpec** | 4技能+15+CLI | Spec驱动的变更与规格管理 |
| **Superpowers** | 14个 | 核心开发流程（规划/执行/TDD/调试/审查） |
| **GStack** | 43+ | 完整产品开发周期（设计/QA/部署/监控） |

**GStack 是 Superpowers 的超集**，额外覆盖了设计、QA、部署、监控等环节。

---

## 安装来源

| 系统 | 位置 |
|------|------|
| GSD | `.claude/commands/gsd/` |
| OpenSpec | CLI `/opt/homebrew/bin/openspec` + `.cursor/skills/openspec-*` |
| Superpowers | `~/.claude/plugins/cache/superpowers-marketplace/.../skills/` |
| GStack | `AI-PM/.cursor/skills/gstack-*` |

---

## 关键复用关系

- **`/gstack-office-hours`** 出现于：需求/想法描述 + 战略方向 + （作为 plan-ceo-review 前置）
- **`/gstack-plan-ceo-review`** 出现于：多角度评审 + 战略方向（接在 office-hours 后）
- **`/gstack-review`** 出现于：代码审查
- **`/gstack-design-shotgun`** 出现于：设计维度评审
- **`openspec validate`** 出现于：健康检查 + 验证
- **`/gsd-complete-milestone`** 出现于：项目初始化（里程碑管理）+ 交付/部署
