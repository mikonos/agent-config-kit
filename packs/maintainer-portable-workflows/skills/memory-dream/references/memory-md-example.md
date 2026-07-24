# MEMORY.md 示例与 Demote 参考

> **何时读本文**：Phase 4A Demote 步骤执行前，或判断一行是否合规时。  
> **来源**：基于 CC 真实 MEMORY.md（`05_每日记录/2026/04/20260407/CC记忆参考_本机搬运/CC_HOME_MEMORY.md`）适配本库 L1 六文件架构。

---

## Part 1 — 目标形态（蒸馏后 MEMORY.md 应有的样子）

以下是本库 MEMORY.md 经过 dream 后的理想状态。每节只存指针，内容在 L1 文件里。**节标题**带 **（user|project|…）** 便于扫读（对齐 CC「行为偏好（feedback）」）；**一律 Obsidian**：`- [[仓库相对路径|短名]]：hook`（**中文冒号**）；落在**对应域小节**（不再单独开「原子卡」大节）。

```markdown
# MEMORY.md - 长期记忆索引

> 由 **memory-dream** 整理、**session-summary worker** 在抽取成功时追加原子指针。每行 ≤150 字符；内容在 L1 文件；禁止内联正文。

---

## 用户与协作（user）→ [[memory/topics/liuyunjiao_local/user.md|user]]

- [[memory/topics/liuyunjiao_local/user.md|原则与铁律]]：先验证再执行；根因优先；random-walk 不硬凑
- [[memory/topics/liuyunjiao_local/user.md|思维与决策模式]]：根因思维 + 反向排除；偏好假设→验证排除错误选项

---

## 项目上下文（project）→ [[memory/topics/liuyunjiao_local/project.md|project]]

- [[memory/topics/liuyunjiao_local/project.md|战略洞察（慢衰减）]]：代理人问题三战场、一人公司 AI 元认知、北美老年 AI
- [[memory/topics/liuyunjiao_local/project.md|515 product 家庭 AI 中心]]：当前主线，[[design-515-family-ai-hub]]
- [[memory/topics/liuyunjiao_local/project.md|Cursor 记忆分层落地（2026-04-06）]]：L0/L1/L2 三层；daily+hook-logs 为新写入通道
- [[memory/topics/liuyunjiao_local/project.md|CC 记忆架构逆向（2026-04-03）]]：四层架构，forked subagent 模式

---

## 知识库状态（vault）→ [[memory/topics/liuyunjiao_local/vault.md|vault]]

- [[memory/topics/liuyunjiao_local/vault.md|Karpathy LLM Wiki 深读]]：总入口 [[索引_记忆与记忆系统#子专题：编译式Markdown维基|索引_AI持久化知识库_编译式Markdown维基]]
- [[memory/topics/liuyunjiao_local/vault.md|ZK III 五层机制]]：产出→入网→归网→体检→修复

---

## 行为偏好（feedback）→ [[memory/topics/liuyunjiao_local/feedback.md|feedback]]

- 范式与纠正：正文在 [[memory/topics/liuyunjiao_local/feedback.md|feedback]]。

- [[memory/20260406_feedback_mdc_not_auto.md|mdc 非自动执行]]：规则只约束 Agent 何时跑 shell；非自动执行

---

## 运维与工具（reference）→ [[memory/topics/liuyunjiao_local/reference.md|reference]]

- [[memory/topics/liuyunjiao_local/reference.md|故障排障]]：飞书/模型常见错误；诊断顺序：进程→Auth→限流→日志
- [[memory/topics/liuyunjiao_local/reference.md|工作区与工具]]：OpenClaw 路径、dream 触发约定

---

## 情绪与协作节奏（affect）→ [[memory/topics/liuyunjiao_local/affect.md|affect]]

- [[memory/topics/liuyunjiao_local/affect.md|近期协作快照]]：当前节奏与语气偏好（周级有效）
```

---

## Part 2 — Before / After Demote（五种最常见场景）

### 场景 A：多行战略分析内联在 MEMORY.md

**Before（非法，>150 字/多行）**：
```markdown
**代理人问题（三战场共同底层）**：老年AI（老人=principal）、内容发布（创作者=principal）、Agent 协作（老板=principal）→ 核心都是「让 agent 服务 principal 真实意图」。

**一人公司 AI 瓶颈（元认知 > 边界）**：
- 真正瓶颈：「知道自己不知道」
- 协同：agent-router 分离
- 精确性幻觉：过度指定失败的根因
```

**After（合法，一行指针）**：
```markdown
- [[memory/topics/liuyunjiao_local/project.md|战略洞察（慢衰减）]]：代理人问题三战场、一人公司 AI 元认知
```
**内容去向**：保留在 `project.md § 慢衰减 — 战略洞察`（原已存在，无需重复写入）。

---

### 场景 B：近期快照长行（单行 >150 字符）

**Before（非法）**：
```markdown
- **Cursor 记忆分层落地（2026-04-06）**：L2 `memory/sessions/<machine-id>/index.md`（stop hook + worker）；L1 `memory/topics/<machine-id>/{user,project,feedback,reference}.md`；根目录 `memory/YYYY-MM-DD.md` **仅历史归档只读**，新写入走 `memory/daily/<machine-id>/` 与 `hook-logs`。旧顶层日志汇入 L0/L1 靠 `memory-dream` 或人工摘取，勿批量伪造 L2。
```

**After（合法）**：
```markdown
- [[memory/topics/liuyunjiao_local/project.md|Cursor 记忆分层落地（2026-04-06）]]：L0/L1/L2 三层；daily+hook-logs 为新写入通道
```
**内容去向**：`project.md § 近期快照`（已有，缩短 MEMORY.md 行即可）。

---

### 场景 C：Feedback 内容内联（最常见的 failure mode）

**Before（非法）**：
```markdown
### 确认的好做法
- **命令规则不等于自动执行**：规则只约束 Agent 行为，实际动作仍需由 Agent 在对应任务中调用。

### 纠正的行为
- **别把 `.mdc` 当成自动执行**：规则只约束 Agent 何时应跑 shell；用户不点、Agent 不调，命令不会自己跑。
```

**After（合法，`type` 与 atom frontmatter 一致；hook 为 `description` 的压缩版以满足每行 ≤~150 字符）**：
```markdown
## 行为偏好（feedback）→ [[memory/topics/liuyunjiao_local/feedback.md|feedback]]

- 范式与纠正：正文在 [[memory/topics/liuyunjiao_local/feedback.md|feedback]]。

- [[memory/20260406_feedback_mdc_not_auto.md|mdc 非自动执行]]：规则只约束 Agent 何时跑 shell；非自动执行
```
**内容去向**：新建对应原子卡（若未建则先建），内容已在 `feedback.md § 范式级`；MEMORY.md 在 **feedback 域小节**内改为指针行。

---

### 场景 D：完整故障表内联

**Before（非法，整张表 = 内容）**：
```markdown
## 五、故障与运维

- **诊断顺序**：进程 → Auth → Cooldown/限流 → 日志

| 症状 | 根因 | 解决 |
|------|------|------|
| All models failed | 多 provider 401/429 + cooldown | 重置 cooldown + 完整重启 |
| 读了消息不回复（飞书） | 缺 cardkit:card:write | 开放平台→权限→开通 |
...（7行）
```

**After（合法）**：
```markdown
## 运维与工具（reference）→ [[memory/topics/liuyunjiao_local/reference.md|reference]]

- [[memory/topics/liuyunjiao_local/reference.md|故障排障]]：飞书/模型常见错误；诊断顺序：进程→Auth→限流→日志
```
**内容去向**：完整表格已在 `reference.md § 故障与运维`，无需重复。

---

### 场景 E：工具说明内联（含详细触发条件）

**Before（非法）**：
```markdown
- **memory-dream（/dream）**：**默认不自动跑**；触发 = 用户说「做梦/整理记忆」、或 `weekly-report` 建议先做、或手动打开 skill。周频或积压时跑一次；详见 `.cursor/skills/memory-dream/SKILL.md`。
```

**After（合法）**：
```markdown
- [[memory/topics/liuyunjiao_local/reference.md|工作区与工具]]：OpenClaw 路径、dream 触发约定
```
**内容去向**：`reference.md § 工作区与工具`（原已有详细说明）。

---

## Part 3 — 行长自检（≤150 字符判断）

执行 Demote 前，可用以下 shell 快速找出超长行：

```bash
awk 'length > 150 {print NR": "length" chars: "$0}' MEMORY.md
```

输出有内容 = 有行需要 Demote。输出为空 = MEMORY.md 已合规。
