---
name: project-issue-workflow
description: "sunsetyyun/project 仓库（product）issue 提交规范——8 种类型、3 档优先级、13 字段模板、label 决策树、行为红线与命令清单。基于 85 条实证 issue + product_issue.yml 模板蒸馏。"
metadata:
  {
    "openclaw":
      {
        "emoji": "🪐",
        "requires": { "bins": ["gh"], "env": ["GH_TOKEN"] },
        "install":
          [
            {
              "id": "brew",
              "kind": "brew",
              "formula": "gh",
              "bins": ["gh"],
              "label": "Install GitHub CLI (brew)",
            },
          ],
      },
  }
---

# project Issue（product 仓库 issue 提交规范）

> **真源**：`05_每日记录/2026/07/20260701_project_issue提交标准实证.md`（基于 85 条 issue + `.github/ISSUE_TEMPLATE/product_issue.yml` + 32 个 label 蒸馏，2026-07-01）。
> **本 skill 是指南针，报告是地图**——详细归纳、反例、命令样板在真源；本卡只放决策框架与高频陷阱。当本 skill 与真源不一致时，**以真源为准**。

## 何时用

- 给 `sunsetyyun/project` 仓库**创建/编辑/评审** issue
- 评估某条 issue 提交是否符合 product 团队的提交规范
- 把 `gh issue create` 输出套上仓库特有的 body / label 模板

**不要用**：通用 GitHub CLI 速查（用 `github` skill）；issue→PR 自动化（用 `gh-issues` skill）。

## 1. 8 种类型（按出现频率排序）

| # | 类型 | 前缀 | 占比 | 必备段落 |
|---|---|---|---|---|
| 1 | Bug / 回归 | `Bug/` | ~46% | 研发修改项 / 验收口径 / 解决记录 |
| 2 | 需求 / 增强 | `需求/` | ~19% | + 背景 / Target Outcome / 不做清单 |
| 3 | UX / 文案 / IA | `UX Copy/` 或 `UX/` | ~10% | + 建议文案候选 + 具体落点（页面/弹窗/i18n key） |
| 4 | 对话 / Agent Chat / AI 输出 | `对话/` | ~10% | **必贴原话**（用户 + product）+ 代码层根因 + `area: 对话Agent` 必带 |
| 5 | 调研 / Spike | `调研/` 或 `LLM/` | ~5% | 方向列表 + 结论 + 风险 + 建议 |
| 6 | 测试任务 / SOP 验证 | `[TEST][可关闭]` | ~4% | 测试目的 + 完成即关 |
| 7 | 迁移 / 验证记录 | `[#<飞书原编号>]` | ~6% | 保留飞书 rid + 跳过 GitHub 默认 type |
| 8 | 文档 / 原型同步 | （不开新 issue） | 隐性高 | 以 changelog comment 形式挂主 issue |

详细定义、反例、样例 issue 号 → 真源报告 §2。

## 2. 标题规范

**格式**：`<类型前缀>/<模块>[/<子模块>]: <一句话现象/outcome>`

| 维度 | 规则 |
|---|---|
| 类型前缀 | `Bug/` `需求/` `UX Copy/` `UX/` `对话/` `LLM/` `[#N]` `[TEST][可关闭]` |
| 模块 | 取 `area: *` label 中文模块名 |
| 一句话 | 动词短语，**不写「优化一下」「改一下」**（评审会被打回） |
| 老 issue 兼容 | 保留 `[#<飞书原编号>]` 前缀，方便追溯 |

## 3. 三大必备段落（与 `.github/ISSUE_TEMPLATE/product_issue.yml` 对齐）

模板 markdown 说明原话：

> 请把 Issue 写成研发和产品都能验收的工作单元。正文里的 **`研发修改项`** 与 **`验收口径`** 是核心，不要只写"优化一下"。

| 段落 | 必填？ | 写法 |
|---|---|---|
| `研发修改项` | **必** | 写"改什么"，不是"目标"；范围包括……不包括…… |
| `验收口径` | **必** | 可验证断言：Given/When/Then 或「当 X 时，必须 Y；不应再 Z；回归覆盖 W」 |
| `解决记录` | 必 | 新建时「待处理/待定位」；修复后补根因/修复/验证/改动/commit/剩余风险 |

需求类额外必备：`背景` / `Target Outcome` / `不做清单（MVP 边界）` / `分阶段验收（A/B/C/...）`。
对话/Agent 类额外必备：**原话原文**（用户 + product）+ 代码层根因（不只是产品解释）。

## 4. 优先级（P0/P1/P2，无 P3）

| 档位 | 触发 |
|---|---|
| **P0** | 阻断核心流程 / 数据丢失 / 串家庭 / 权限隐私 |
| **P1** | 重要功能受损但有绕路（默认） |
| **P2** | 体验 / 边角 / 视觉（默认） |

## 5. Label 决策树

```
新 issue
├─ 类型？
│  ├─ Bug        → bug + area:* + P?
│  ├─ 需求/增强   → enhancement + product + area:* + P?
│  └─ 迁移记录    → 跳过 GitHub 默认 type，只打 P? + area:* + 状态
├─ area（1-3 个，可叠加；最多 3 个）
├─ P 几？P0/P1/P2（三档决策见 §4）
└─ 状态？
   ├─ 待人工拍板  → 待确认（默认）
   ├─ 修复完成待验 → 待验收
   ├─ 重复/非缺陷  → duplicate / wontfix
   └─ 长期 parked → 保持 待确认（不切走）
```

**label 全集**（32 个）：
- area（14）：账号 / 成员家庭 / 首页 / 任务GTD / 日历 / 对话Agent / 语音 / 通知 / 记忆 / 安装构建 / 集成OAuth / 测试 / 儿童Routine / 开发者工具
- priority（3）：P0 / P1 / P2（**无 P3**）
- type（兼容 GitHub 默认）：bug / enhancement / documentation / question / duplicate / invalid / wontfix / product（自加）/ help wanted / good first issue
- workflow（自加 2）：**待确认**（parked）、**待验收**（已修复待人工验）

## 6. 行为红线（反模式）

- ❌ 把"想要未存在的能力"写成 Bug——是 enhancement/需求
- ❌ body 只写「优化一下」「改一下」——评审被立刻打回
- ❌ 多 Bug 拼成一条——验收口径失焦
- ❌ HTML / JS 直接粘 body 期望可交互——**GitHub 安全过滤** `<script>` / `<iframe>` / `<button onclick>`，只保留 `<details><summary>`
- ❌ 对话/Agent 类不贴原话——LLM 行为偏差不可复现
- ❌ 不挂 `area: 对话Agent`——领域路由丢失
- ❌ 迁移 issue 没保留飞书 rid——失去源头可追溯
- ❌ 改造 issue 跳过默认 type（迁移类除外）

## 7. assignees / milestone 处理

- 仓库**未使用** assignees / milestones（85 条全空）。
- 闭环路径：研发 comment 写「【Claude MMDD】已修复·待验收」+commit → OWNER 真机验 → 写「真机验证通过」 → 协作者 close。
- issue 与 PR 当前**不联动**（无 `Fixes #N` / `Closes #N` 关联）；修复记录写在 comment 里。

## 8. HTML 原型怎么办

可被 GitHub 保留的：**`<details><summary>`**（静态折叠）。
被安全过滤：`<script>` / `<iframe>` / `<button onclick>` / 任意事件处理器。

可交互原型必须用：GitHub Pages 预览 URL / preview artifact 链接——**不能 inline JS**。真源报告 §4.2 有实测样例。

## 9. 实战工作流（2026-07 复盘沉淀）

### 9.1 先判工作单元，再判 label

| 用户输入 | 默认处理 |
|---|---|
| “提交 bug / 无法点击 / 同步出错” | 先按 `Bug/` 写；若只是口径不清，改为 `调研/` + `question` |
| “提交需求 / 增加能力 / 希望可以” | `需求/` + `enhancement,product`，必须写 Target Outcome 和不做清单 |
| “可能有问题 / 不一定是 bug / 需要核对” | `调研/` 或 `UX/` + `question,product,待确认`，正文写“需要核对的问题” |
| “文案 / 命名 / 信息架构” | `UX Copy/` 或 `UX/`，写文案候选、具体页面和交互落点 |
| “prompt / Agent / LLM 行为 / harness” | `LLM/` 或 `对话/`，优先挂 `area: 对话Agent`；涉及 CLI、MCP、Codex、skill 时叠加 `area: 开发者工具` |

不要为了显得严重，把未确认的产品口径写成 Bug。不确定时，把它写成可验收的 spike / question。

### 9.2 创建前查重并核对证据

1. 至少用中文、英文和模块词各查一次已有 issue：

   ```bash
   gh issue list --repo sunsetyyun/project --state all --search "<keywords>" --limit 20 \
     --json number,title,state,labels,url,updatedAt
   ```

2. 若已有主 issue，优先追加 changelog comment 或同步最新版文件，不新开重复 issue。
3. 用户给出截图、PRD、原型或代码行时，先核对关键事实：
   - 截图：正文描述可见现象、触发动作和影响，不默认要求把图片上传到 GitHub。
   - PRD / 代码：写仓库相对路径和行号，不把本地绝对路径当作研发可访问链接。
   - PRD / 原型更新：比较本地与远端内容或 hash；只上传缺失或过期文件，更新后再做一次远端回读。
   - HTML：不要期待 issue 内联交互。用户明确“不需要 GitHub Pages”时，只提交仓库文件链接和静态说明。

### 9.3 把正文写成研发可执行的工作单元

优先使用这套骨架；按 issue 类型删去不适用段落：

```markdown
## 背景
## Target Outcome / 需要核对的问题
## 研发修改项
## 验收口径
## 不做清单 / MVP 边界
## 风险与开放问题
## 解决记录
```

- `背景`：写用户看到什么、为什么重要，不写抽象愿望。
- `Target Outcome`：写用户、家庭或研发最终要得到的状态。
- `研发修改项`：写改动面和排除面，避免只写“优化一下”。
- `验收口径`：用 Given / When / Then 或等价的可观察断言；每条都能真机或代码验证。
- `不做清单`：主动控制权限系统、复杂同步、完整重构等范围膨胀。
- `解决记录`：新 issue 写 `待处理`、`待产品确认` 或 `待定位`。

### 9.4 Label 与优先级经验

- 普通产品需求：`enhancement,product,P2,area:<模块>,待确认`。
- 核心流程受损但有绕路：P1。
- 权限、隐私、数据丢失、串家庭、阻断创建或同步：P0。
- 产品口径不确定：加 `question,product,待确认`，不要加 `bug`。
- LLM、prompt、harness：常用 `area: 对话Agent`；涉及 CLI / MCP / Codex / skill 时再加 `area: 开发者工具`。
- Tasks、GTD、Waiting For：`area: 任务GTD`。
- 外部日历、忙碌状态、日历同步：`area: 日历`；涉及家庭可见隐私时上调优先级。

### 9.5 创建或更新后必须回读

```bash
gh issue view <number> --repo sunsetyyun/project \
  --json number,title,url,labels,body
```

逐项检查：

- 标题前缀、模块和现象是否准确。
- labels 是否包含 type、priority、area 和状态。
- `研发修改项`、`验收口径`、`解决记录` 是否存在。
- 同步 PRD / 原型 / skill 时，issue body、comment 或仓库链接是否已指向最新版。
- 不要只凭 `gh issue create` 返回 URL 就宣告完成。

### 9.6 群通知边界

通知前必须先拿到已回读验证的 issue 号和 URL。通知只放：

- 新 issue 或 issue 更新标题。
- GitHub 链接。
- 1-4 条本次提交、更新内容或验收重点。
- 明确需要研发评审或验收的事项。

不要把完整 PRD、长验收清单或敏感截图刷进群。发送后记录 `message_id`，避免重复通知；具体发送门禁与模板见 §11。

## 10. 命令清单

```bash
# 提交 issue（body 用 --body-file，避免反引号/中文/多行被 shell 吞）
gh issue create --repo sunsetyyun/project \
  --title "Bug/Tasks: In progress 不应展示 Waiting For 等待他人的项目项" \
  --body-file /tmp/issue.md \
  --label "bug,P1,area: 任务GTD,待确认"

# 修改 labels
gh issue edit <n> --repo sunsetyyun/project --add-label "待验收"
gh issue edit <n> --repo sunsetyyun/project --remove-label "待确认"

# 转 wontfix
gh issue edit <n> --repo sunsetyyun/project --add-label "wontfix" --remove-label "待确认"

# 验收通过后关闭
gh issue close <n> --repo sunsetyyun/project --comment "真机验证通过，关闭。"

# 列出当前仓库的待处理（待确认 / 待验收）
gh issue list --repo sunsetyyun/project --state open --label "待确认" --limit 20 \
  --json number,title,labels,url
```

## 11. 提交/更新后飞书通知

**默认动作（2026-07-04 老板授权；2026-07-06 扩展）**：以后给 `sunsetyyun/project` 新建/正式提交 issue 后，必须在飞书 `产品开发` 群发一条简短通知。对已有 issue 做**实质更新**后也要通知，尤其是同步 PRD / 原型 / 运行时 skill / references / dry-run fixtures / changelog / 验收口径这类会影响研发理解或执行的更新。

通知规则：

- 先校验 GitHub issue 已创建或更新成功，拿到 `#number`、title、url、labels；若是更新，先确认更新内容已出现在 issue body / comment / 附件链接中。
- 目标群固定为飞书群 `产品开发`；发送身份固定用 bot。
- 运行时用 `lark-cli im +chat-search --query "产品开发" --as bot --format json` 精确查群，必须只命中一个 `normal` 群且群名等于 `产品开发` 才发送；否则停下让老板确认。
- 通知内容只放：issue 标题、链接、1-4 条本次提交/更新内容或验收重点。不要把 PRD 全文、长验收清单、截图大图直接刷进群。
- 用稳定 `--idempotency-key`，新 issue 建议格式：`project-issue-workflow-<number>-notify-<YYYYMMDD>`；更新通知建议格式：`project-issue-workflow-<number>-update-<YYYYMMDD>-<slug>`，避免重试重复发。
- 若 issue 涉及隐私、账号、家庭成员敏感截图、未公开 token/链接等，不自动群发，先问老板是否需要脱敏版通知。
- 不必通知的轻微操作：只改错别字、只改 label、只修一个失效链接且不影响研发判断、重复执行但没有内容变化。

新 issue 通知模板：

```markdown
## 新 issue：<title>

已提交，请研发评审：
<issue-url>

本次提交内容：
- <要点 1>
- <要点 2>
- <要点 3>
```

已有 issue 更新通知模板：

```markdown
## Issue 更新：<title>

已同步更新，请研发按最新版评审：
<issue-url>

本次更新：
- <变更 1>
- <变更 2>
- <变更 3>
```

## 12. 与其他 skill 的分工

| Skill | 视角 | 何时用 |
|---|---|---|
| `github` | 通用 gh CLI 速查（issue / PR / CI / API） | 任何仓库的 gh 命令查询 |
| `gh-issues` | issue→PR 自动化工作流 | 批量 watch issue 派 worker 修 |
| **`project-issue-workflow`** | **product 项目特定提交规范** | 给 sunsetyyun/project 写 issue 时 |

## 13. 演化约定

- product 团队若改 issue template 或 label 全集，**先回真源报告追加修订**，再回本 skill 同步。
- 真源报告每 30 天或累计 30 条新 issue 时重抽样一次。
