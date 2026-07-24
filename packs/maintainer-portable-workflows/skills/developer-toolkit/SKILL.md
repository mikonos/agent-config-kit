---
name: developer-toolkit
description: |
  Route product/engineering work to exactly one next step: gstack-first (ship/QA/design), OpenSpec (change-level .openspec/),
  GSD (project-level .planning/ + get-shit-done workflows), Superpowers (verify-output / workflow-audit).
  Use when unsure which stack; ask「三栈」「四栈」「到哪一步」「developer-toolkit」; or install hints. Not when a tool is already chosen.
  路由分两步：①用「用途明细表」定位工具体系 ②用「用途详解」确认差异并决定最终工具。
  完整命令对照表见 `references/command-systems-comparison.md`。
---

# developer-toolkit（gstack 为主 · OpenSpec / GSD / Superpowers 分层）

| 层级 | 管什么 | 典型落点 |
|------|--------|----------|
| **gstack** | 执行与交付：浏览器、调试、设计落地、QA、发版 | `~/.cursor/skills/gstack/**/SKILL.md` |
| **OpenSpec** | **变更级**规格：单条 change、提案—实现—归档 | `.openspec/` |
| **GSD** | **项目级**规划：路线图、阶段、里程碑、多 agent 编排 | `.planning/` + `.cursor/get-shit-done/workflows/*.md` |
| **Superpowers** | 对抗性验证与流程核对 | `verify-output`、`workflow-audit` |

**怎么选**：同一题里 **OpenSpec = 一条 change**；**GSD = 整仓库产品/里程碑节奏**。二者可并存：先有 GSD 里程碑，再在阶段内开 OpenSpec change。

**When NOT**：已锁定具体工具时直接跳转，不经过本 skill。

## 阶段一览（多阶段 skill：先定阶段再查子表）

| 阶段 | 一句话 | 跳转到 |
|------|--------|--------|
| 澄清 | 不知道做什么、要探索或立项 | 下文「澄清阶段」表 |
| 规划 | 方案/范围/架构/DX 未定 | 下文「规划阶段」表 |
| 设计 | 视觉、设计系统、稿转码、线上视觉 QA | 下文「设计阶段」表 |
| 执行 | 写代码、调试、浏览器验证、DX 实走 | 下文「执行阶段」表 |
| 评估 | 审查、测试、性能、安全、逻辑找茬 | 下文「评估阶段」表 |
| 发布 | PR、部署、文档同步、上线监控 | 下文「发布阶段」表 |
| 协同 | 多方对齐、change 归档 | 下文「协同阶段」表 |
| 方向 | open loops、周复盘 | 下文「方向阶段」表 |

---

## 诊断流程（强制：先读产出，再诊断阶段，再用大表差异确认）

**必须先执行 Step 0**，不允许跳过直接给结论。

### Step 0：读产出

不依赖用户的自我描述，直接读项目状态：

```bash
git log --oneline -10
ls .openspec/ 2>/dev/null || echo "no openspec"
ls .planning/ 2>/dev/null | head -8 || echo "no .planning (GSD)"
test -d .cursor/get-shit-done && echo "gsd workflows ok" || echo "no .cursor/get-shit-done"
cat memory/open\ loops.md 2>/dev/null | grep "^- \[" | wc -l
ls -t memory/YYYY-MM-DD.md 2>/dev/null | head -1 | xargs tail -50 2>/dev/null
```

### Step 1：从产出推断阶段

| 产出信号 | 阶段 |
|---------|------|
| 无 spec，无方向，用户说"不知道做什么" | 澄清 |
| 要做**软件项目**但无 `.planning/`、要路线图/里程碑/GSD 流程 | 澄清或规划（优先 GSD 立项） |
| 有想法/方向，但没技术方案或设计方案 | 规划 |
| 有方案，需要视觉/交互设计 | 设计 |
| 有 spec/任务，需要写代码/调试/实现 | 执行 |
| 有产出，需要验证质量/安全/性能 | 评估 |
| 代码完成，需要发布/部署/监控 | 发布 |
| 多方对齐困难，改动描述不清 | 协同 |
| open loops 长期悬着，决策卡住 | 方向 |

### Step 2：按阶段路由到具体工具

**原则：永远只给一个工具**（GSD 时「工具」= **一个** workflow 文件 + 按该文件执行）。多阶段并存时取最上游。
**优先级**：澄清 > 规划 > 设计 > 执行 > 评估 > 发布 > 协同/方向。
**GSD vs OpenSpec**：当前任务是「整项目/某 milestone/某 phase」→ 先 **GSD workflow**；是「实现已存在的某条 OpenSpec change」→ **openspec-apply-change**。

### Step 2.5：用大表差异确认工具选择（强制）

**在 Step 2 给定工具之后，必须查 `references/command-systems-comparison.md` 的「用途详解」确认该工具的适用差异。**

决策逻辑：

```
工具已选定（Step 2）
      ↓
查大表「用途详解」中该用途的小节
      ↓
看是否有该工具的差异说明
      ↓
无 → 直接输出
有 → 核对4个问题：
  ① 用户的场景是否匹配该工具的典型场景？
  ② 用户是否有特殊约束（如：时间紧、只需要报告不需要修、登录态）？
  ③ 是否需要替换为更合适的同用途备选？
  ④ 用户是否明确表达了偏好（如："不需要修bug" → qa-only 而非 qa）？
```

**同用途备选决策举例**：

| 用户场景信号 | 工具选择调整 | 原因 |
|-------------|-------------|------|
| "我只是想知道有什么bug，不急着修" | `qa-only` 替换 `qa` | 差异：只出报告不修 |
| "我要快速看一下，不用AI操作" | `review-read` 替换 `review` | 差异：读报告不重跑 |
| " startup创始人，方向不清晰" | `office-hours` (Startup) 替换 `brainstorming` | 差异：六问挑战 vs 探索性脑暴 |
| "我只要下一步该干啥" | `gsd-next` 替换 `gsd-plan-phase` | 差异：极简推荐 vs 完整规划 |
| "时间紧，先跑起来" | `gsd-fast` 或 `gsd-quick` | 差异：轻量执行，少流程验证 |
| "合PR等CI验生产要一次跑完" | `land-and-deploy` 替换 `ship` | 差异：完整流水线 vs 只是开PR |

---

#### 澄清阶段

| 子场景 | 工具 |
|--------|------|
| 问题空间模糊，需要探索 | `openspec-explore` |
| 有想法但未结构化，需要脑暴 | `office-hours` (gstack) |
| **从零立项**：需要 `.planning/`、ROADMAP、里程碑（GSD 项目壳） | **GSD** → `.cursor/get-shit-done/workflows/new-project.md`（Cursor 无 slash：对话里声明「按该 workflow 全文执行」） |
| **回到中断的 GSD 项目** | **GSD** → `resume-project.md` |
| **代码库索引/地图**（GSD 前置） | **GSD** → `map-codebase.md` |
| 探索完毕，需要出 proposal + design + tasks（**变更级**，非整项目路线图） | `openspec-propose` |

#### 规划阶段

| 子场景 | 工具 |
|--------|------|
| **GSD：阶段规划、里程碑缺口、讨论期假设** | **GSD** → `plan-phase.md`、`plan-milestone-gaps.md`、`discuss-phase.md`（依 `STATE.md`/`.planning/` 现况选一条） |
| **GSD：研究阶段** | **GSD** → `research-phase.md` |
| 战略/范围级决策，挑战前提（gstack 评审） | `plan-ceo-review` (gstack) |
| 工程架构、数据流、边界 | `plan-eng-review` (gstack) |
| DX / API 设计评审 | `plan-devex-review` (gstack) |
| 想串联所有评审一次跑完 | `autoplan` (gstack) |

#### 设计阶段

| 子场景 | 工具 |
|--------|------|
| 从零建立设计系统（色彩/字体/间距） | `design-consultation` (gstack) |
| 多方案视觉探索与对比 | `design-shotgun` (gstack) |
| 计划阶段的设计维度评审 | `plan-design-review` (gstack) |
| 设计稿/mockup 转生产级 HTML/CSS | `design-html` (gstack) |
| 线上视觉 QA，迭代修并截图验证 | `design-review` (gstack) |

#### 执行阶段

| 子场景 | 工具 |
|--------|------|
| **GSD：按阶段执行任务、跑 execute 计划** | **GSD** → `execute-phase.md` 或 `execute-plan.md` |
| 有 openspec change 待实现 | `openspec-apply-change` |
| 需要调试（报错/500/stack trace） | `investigate` (gstack) |
| 无头浏览器交互、截图、验证页面 | `browse` (gstack) |
| 需登录态测站，从本机 Chromium 导入 cookie | `setup-browser-cookies` (gstack) |
| 需可见浏览器窗口 + 侧栏观察 AI 操作 | `open-gstack-browser` (gstack) |
| 需要真实走 DX 流程测 onboarding | `devex-review` (gstack) |

#### 评估阶段

| 子场景 | 工具 |
|--------|------|
| **GSD：阶段/工作项验收** | **GSD** → `verify-phase.md`、`verify-work.md`；安全/合规阶段见 `secure-phase.md` |
| PR / diff 代码审查 | `review` (gstack) |
| 系统功能测试并修 bug | `qa` (gstack) |
| 只出 bug 报告不修代码 | `qa-only` (gstack) |
| 性能基线 / Core Web Vitals 对比 | `benchmark` (gstack) |
| 安全审计（供应链/密钥/OWASP/STRIDE） | `cso` (gstack) |
| 代码质量综合评分 | `health` (gstack) |
| 对抗性逻辑验证（找遗漏/找茬） | `verify-output` (Superpowers) |
| 多阶段 skill 执行完成度核对 | `workflow-audit` (Superpowers) |
| Codex 独立二次审查 | `codex` (gstack) |

#### 发布阶段

| 子场景 | 工具 |
|--------|------|
| 提交、推送、开 PR | `ship` (gstack) |
| 合 PR、等 CI、验生产 | `land-and-deploy` (gstack) |
| 首次配置部署环境 | `setup-deploy` (gstack) |
| 发版后同步 README/CHANGELOG 等文档 | `document-release` (gstack) |
| 部署后持续监控（错误/性能/截图） | `canary` (gstack) |

#### 协同阶段

| 子场景 | 工具 |
|--------|------|
| 需要规格作为多方共识载体 | `openspec-propose` |
| change 实现完毕，归档收尾 | `openspec-archive-change` |
| **GSD：里程碑完成、工作区/阶段收尾** | **GSD** → `complete-milestone.md`、`transition.md`、`cleanup.md`（按文档条件选用） |

#### 方向阶段

| 子场景 | 工具 |
|--------|------|
| 旧 open loops 长期悬着 | 只读旧 `memory/open loops.md` 做 legacy 分类参考；非 GTD 主任务带出的新承诺输出 `dry run gtd-capture` 建议 |
| 周维度复盘回顾 | `retro` (gstack) |

---

### 安全工具箱（随时可用，不需诊断）

| 工具 | 用途 |
|------|------|
| `careful` (gstack) | 危险命令前弹警告（rm -rf / force push / DROP TABLE） |
| `freeze` (gstack) | 限制编辑范围到指定目录 |
| `guard` (gstack) | careful + freeze 合体，最高安全模式 |
| `unfreeze` (gstack) | 解除 freeze 限制 |
| `checkpoint` (gstack) | 保存/恢复工作状态（git + 决策 + 剩余任务） |
| `learn` (gstack) | 管理跨会话 learnings |

#### 维护（不属诊断阶段，按需直达）

| 子场景 | 工具 |
|--------|------|
| 升级 gstack 到最新版 | `gstack-upgrade` (gstack) |

> 根技能名 **`gstack`** 与 **`browse`** 同属浏览器 QA 族；路由时优先给 `browse`，除非用户明确点名 `gstack`。

---

### Step 3：输出格式

**永远只给一个工具**。如果涉及多阶段，取最上游。

```
**阶段**：澄清 / 规划 / 设计 / 执行 / 评估 / 发布 / 协同 / 方向
**信号**：{从产出中观察到的具体症状}
**工具**：{唯一具体 skill 或 GSD workflow 文件名，如 execute-phase.md}
**差异确认**：{从大表「用途详解」中确认的关键差异，为什么选这个而非备选}
**下一步**：{唯一起点动作}
```

---

## 工具安装

| 工具 | 安装 |
|------|------|
| gstack | 参考 `references/install.md` |
| OpenSpec | `brew install openspec` |
| GSD | `npx get-shit-done-cc@latest --cursor --local`（已安装则本仓库已有 `.cursor/get-shit-done/`） |
| Superpowers | 激活对应 skill（`verify-output`、`workflow-audit`） |

---

## References

### 完整命令对照表
**必读**：`references/command-systems-comparison.md` — 用途→命令大表，同一用途对应 GSD / OpenSpec / Superpowers / GStack 的所有命令。

**大表使用时机**：
- **Step 2（路由）**：查「用途明细表」快速定位某用途有哪些工具
- **Step 2.5（差异确认）**：查「用途详解」中对应小节，确认选择理由和备选替换

### 各系统详情

| 系统 | 关键命令速查 |
|------|-------------|
| **GSD** | 工作流真源 `.cursor/get-shit-done/workflows/`；**`.agents/`** 内子 agent 由对应 workflow 引用。与 gstack 关系：**GSD 定节奏与验收清单，gstack 负责浏览器/QA/发版等具体动作** |
| **OpenSpec** | `openspec-explore` → `openspec-propose` → `openspec-apply-change` → `openspec-archive-change`；CLI：`openspec init`/`list`/`view`/`validate` |
| **gstack** | 上表覆盖常用路由；安装与版本见 `references/install.md`；执行时读对应子目录 `SKILL.md`（仓库内 gstack 技能与 `~/.cursor/skills/gstack/` 对齐时以本机为准；Claude Code 用户为 `~/.claude/skills/gstack/`） |
| **Superpowers** | 本 skill 仅路由到：`verify-output`、`workflow-audit` 等独立 skill；完整命令见 `references/command-systems-comparison.md` |
