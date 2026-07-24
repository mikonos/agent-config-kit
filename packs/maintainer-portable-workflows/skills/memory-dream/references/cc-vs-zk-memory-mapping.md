# Claude Code 与 ZK 本库 · 记忆流水线对应关系

> **用途**：说明 CC 源码中的记忆组件与本库（Cursor + `memory/` 目录）的**一一对应与扩展**，供 `memory-dream`、`_session-summary-worker.js`、规则 `core-ops` Step 4.x 对齐时查阅。  
> **真源**：CC 侧以 `claude-code` 仓库 `src/services/extractMemories/`、`services/autoDream/`、`memdir/memdir.ts` 为准；本库抽取 **SYSTEM_PROMPT** 以 **`scripts/lib/session-summary-system-prompt.js`** 为准（worker 与 `session-summary-extract-core.js` 共用）；运行编排另见 `.cursor/hooks/_session-summary-worker.js`、`.cursor/skills/memory-dream/SKILL.md`。

---

## 总览对比表（CC 记忆工作体系 ↔ ZK 本库）

### A. 分层与落点

| 维度 | Claude Code | ZK 本库（本 Vault） |
|---|---|---|
| **L0 入口索引** | 项目下 `MEMORY.md`（或等价入口），稀疏指针 | 仓库根 **`MEMORY.md`**；行长/体积上限对齐 consolidation 思路 |
| **L1 主题记忆** | **`memory/`** 内 **四文件**：`user` / `project` / `feedback` / `reference`（memdir 约定） | **`memory/topics/<machine-id>/`** 下 **六文件**：CC 四类型 + **`affect`** + **`vault`**（`core-ops` Step 4.2） |
| **原子/条目标** | 抽取结果写入 **独立 `.md` 文件**（带 YAML `type` 等），与 memdir 协同 | **`memory/YYYYMMDD_<type>_*.md`**（根目录，与 `YYYY-MM-DD` 日报区分）；frontmatter：`name`、`description`、`type`、`session_id`（+ `machine_id`） |
| **会话级视图** | 依赖会话与产品内状态机（具体 UI/路径随 CC 版本） | **`memory/sessions/<machine-id>/index.md`**（L2；worker 写摘要行） |
| **其他通道** | 以 CC 产品内实现为准 | **`memory/daily/`**、**`memory/hook-logs/`** 等（本库运维向） |

### B. 流水线阶段

| 阶段 | Claude Code | ZK 本库 |
|---|---|---|
| **抽取（从对话到结构化记忆）** | **`extractMemories`**：forked subagent，按策略在回合后执行 | **`_session-summary-worker.js`**：stop hook 写 pending → **debounce** → Cursor CLI 调模型 → 写 atoms + `MEMORY.md` 指针 |
| **巩固（整理、去重、降级长内容）** | **`autoDream`** + consolidation prompt / memdir 修剪 | **`memory-dream` skill**：Orient → Gather → Consolidate → **Prune & Index**（Demote 对齐 CC） |
| **入口维护** | 更新项目 `MEMORY.md` 与 memdir 文件 | 更新 **`MEMORY.md`** + **L1「原子卡索引」**：worker 与写 MEMORY **同条件**追加新行；dream **整理**（去重、排序、Demote） |

### C. 类型与路由

| 项目 | Claude Code | ZK 本库 |
|---|---|---|
| **memdir / 聚合类型数** | **4**：user, project, feedback, reference | **6**：上四者 + **affect**, **vault**（扩展类仅本库） |
| **单条记忆文件命名** | 由实现生成（语义化 slug 等） | **`YYYYMMDD_<type>_<slug>.md`**（`type` 为六类之一） |
| **`MEMORY.md` 原子行** | 指针行（随 CC 样本形态） | **Obsidian**：`- [[memory/…路径|短名]]：hook`（落在**对应域小节**；对齐 CC「见文件：一句」；类型由文件名 `_user_`/`_project_`/… 推断；过长则压缩） |

### D. 触发与成本

| 项目 | Claude Code | ZK 本库 |
|---|---|---|
| **抽取触发** | 回合结束 + 产品内节流/条件 | **每轮 stop** 更新 pending；**idle ≥10min** 才处理（debounce） |
| **巩固触发** | 自动 dream 条件（token/时间等，见 CC 配置） | **手动 / weekly-report / 日课约定**；skill 内「三重门限」改编 |
| **重活所在进程** | forked subagent，不阻塞主会话 | **独立 worker 进程**，主对话仅写 pending |

### E. 约束与禁忌（对齐意图）

| 项目 | Claude Code（常见约定） | ZK 本库 |
|---|---|---|
| **MEMORY 是索引不是正文** | 长内容进主题文件或 atom，MEMORY 保持短指针 | 同上 + **Demote** 超长行（见 `memory-md-example.md`） |
| **feedback 体例** | 纠正/确认 + 可含 Why / 如何应用 | 与 CC 对齐；原子卡见 `cc-feedback-atom-examples-and-template.md` |
| **禁止** | 把整段知识堆在 MEMORY 当正文 | **禁止** worker/dream 把 ZK 卡片正文整页贴进 `MEMORY.md`；**vault** 仅 `[[链接]]`+hook |

---

## 1. 组件级映射（谁做什么）

| Claude Code | 本库 | 职责摘要 |
|---|---|---|
| **extractMemories**（forked subagent，每轮或节流后） | **`_session-summary-worker.js`**（stop hook → pending → debounce → Cursor CLI） | 从**会话 transcript**抽结构化记忆，**一记忆一文件**落 `memory/YYYYMMDD_<type>_*.md`，frontmatter：`name` / `description` / `type` / `session_id`（+ 本库 `machine_id`）；并更新 **`MEMORY.md`** 对应域小节指针与 **对应 L1「原子卡索引」**（与 MEMORY 同条件）。 |
| **autoDream** | **`memory-dream` skill** | **不**从原始 JSONL 重抽；扫描已落盘信号，**巩固 / Demote / 修剪 MEMORY / 维护 L1「原子卡索引」**；对齐 CC consolidation 四阶段思路。 |
| **memdir** 四类型文件（项目目录下 `memory/`） | **`memory/topics/<machine-id>/{user,project,feedback,reference,affect,vault}.md`** | L1 主题聚合正文 +「原子卡索引」；本库在 CC 四类型上 **扩展 `affect` / `vault`**（见 `core-ops` Step 4.2）。 |
| **HOME / 入口 MEMORY** | **仓库根 `MEMORY.md`** | L0 稀疏索引；行长与体积上限对齐 CC `memdir` + `consolidationPrompt` 思路。 |
| **Session 级摘要（若 CC 有）** | **`memory/sessions/<machine-id>/index.md`** | 会话级标题/进展等，由 worker 写 L2，供 dream 与人工扫一眼。 |

**分工口诀**：**worker ≈ extractMemories（抽 + 原子文件 + L0 指针 + L1 原子索引行）**；**dream ≈ autoDream（整理 + 晋升 + Demote + L1 索引合并）**。

---

## 2. `type` 路由：CC 四类型 ↔ 本库六类型

| `type`（frontmatter / JSON） | CC 是否有同名 memdir | L1 聚合文件 | 典型内容（本库约定） |
|---|---|---|---|
| `user` | 是 | `user.md` | 叙事画像、偏好、责任、知识（忌无关评判） |
| `project` | 是 | `project.md` | 外部产品/战役、本库工具链决策；事实 + **Why** + **How to apply** |
| `feedback` | 是 | `feedback.md` | 对 Agent 的纠正/确认；正文 **Why** / **How to apply** |
| `reference` | 是 | `reference.md` | URL、项目名、「何时查哪」短指针 |
| `affect` | **否（本库扩展）** | `affect.md` | **短时、与协作相关**的节奏/语气/框架偏好；禁临床化（见 Step 4.2） |
| `vault` | **否（本库扩展）** | `vault.md` | **Zettelkasten 内**活跃 MOC/索引/主题线；`[[链接]]` + hook，禁贴原子正文 |

**文件名约定（worker）**：`memory/YYYYMMDD_<type>_<slug>.md`，`<type>` ∈ 上表六者。

**MEMORY.md 指针（worker）**：写入**对应域小节**（如「## 行为偏好（feedback）」）时为 `- [[20260407_feedback_Vault改名须验根last_saved_path|alias]]：hook`（Obsidian wikilink + **中文冒号**，对齐 CC `见 file：说明`）；**不写**行内 `[type]`，类型由文件名段推断。

---

## 3. 与 CC 的差异（刻意设计）

1. **六类型**：在 CC **四类型** 上增加 `affect`、`vault`，对应 L1 扩展文件；**不入** CC 官方 `memdir` 枚举，但与本库 `core-ops` Step 4.2 一致。  
2. **L1「原子卡索引」双通道**：**worker** 在写 `MEMORY.md` 时同步追加 `- [[memory/…\|hook]]`（按 `type` 写入六文件之一，路径去重）；**dream** 负责合并重复、排序与体例，避免仅靠人工跑 dream 时 L1 **滞后**。  
3. **钦天监等本库运维层**：本库独有；不属于 CC 默认行为。  

---

## 4. 流程阶段、产出物与差距（细表）

> 下表从「阶段 → 典型产出 → CC 怎么做 → 本库怎么做 → **仍存在的差距**」归纳，便于排期补齐。

### 4.1 抽取链路：`extractMemories` ↔ `_session-summary-worker.js`

| 阶段 | CC（典型行为） | 本库当前实现 | **差距 / 待加强** |
|---|---|---|---|
| **触发** | 回合结束后由产品调度；常配合**节流**（避免每轮都跑） | stop hook 写 pending；**默认 3min idle**（`SESSION_SUMMARY_DEBOUNCE_MS`）+ **manifest** + **互斥戳** | 与 CC 仍差「产品内统一 UI」，观测用 `memory/运维/memory-pipeline-status.md` |
| **输入** | 常取**最近 N 轮/字符**对话，控制 token | `readTranscriptCompact`（`SESSION_SUMMARY_MAX_TRANSCRIPT_CHARS`）+ **`buildAtomManifest` 注入** | 语义去重（embedding）仍为可选后置 |
| **推理** | 专用 **prompt + JSON schema**；子代理独立上下文 | Cursor CLI + **`SYSTEM_PROMPT`**（`scripts/lib/session-summary-system-prompt.js`），产出 `summary` + `memories[]`；`feedback`/`project` 可 **落盘前校验 Why/How**（`SESSION_SUMMARY_STRICT_WHYSHOW=0` 关闭）；可 **skip MEMORY**（env / pending / 互斥） | **无**与 CC 完全一致的 **成本预估** UI；失败重试依赖 pending |
| **产出 A：原子文件** | 一条记忆一文件，YAML 含 `name` / `description` / `type` | `memory/YYYYMMDD_<type>_<slug>.md`，字段对齐并多 **`machine_id`** | **规则去重**：全库 `name` + **manifest 注入** 降重复产出；**无语义级 embedding 去重**（可选后置） |
| **产出 B：L0 索引** | 更新入口 `MEMORY.md`（或等价） | 在对应域小节追加行，``- \`…\`：hook`` | **未**同步写 CC 式 **四文件 memdir 内联**（刻意省略，改由 dream）；**有** env / 互斥 **atoms_only** 跳过写 MEMORY |
| **产出 C：会话级摘要** | 依产品而定 | **`memory/sessions/<id>/index.md`** 条目 + `summary` 字段 | CC 是否在 UI 展示会话卡不确定；本库 **有** L2，但 **无**与 CC 产品内「会话列表」对等的统一入口 |
| **产出 D：主题聚合** | 部分流程会直接 merge 进 `user.md` 等 | worker **不写** L1 范式正文；**写**「原子卡索引」新行（与 MEMORY 同步） | worker 已补 L1 索引；正文晋升仍靠 dream / 人工 |
| **失败与观测** | 产品内日志/遥测 | `session-summary-worker.log`、`session-summary-failures.log`、pending、`memory/pipeline/status.json` | 人读汇总：`memory/运维/memory-pipeline-status.md`（脚本刷新） |

### 4.2 巩固链路：`autoDream` ↔ `memory-dream` skill

| 阶段 | CC（典型行为） | 本库（SKILL 四阶段 + Phase 4 Demote） | **差距 / 待加强** |
|---|---|---|---|
| **触发** | **自动**：满足 token/时间/间隔等条件即跑 | **手动** / 周报建议 / 日课约定；「三重门限」改编 | **最大差距**：无 **保证执行的定时器**（除非用户配 OpenClaw/cron 显式调 skill） |
| **Orient** | 读 MEMORY + memdir，有工具封装 | `ls`、`读 MEMORY`、扫 L1 header | 相当；本库多 **六文件 + vault/affect** 规则 |
| **Gather** | 扫描日志与漂移记忆 | 优先级：**atoms + MEMORY** → 摘录节 → L2 → daily… | 已文档化；**依赖执行者**是否真按表扫 |
| **Consolidate** | 合并、晋升、修矛盾；写回 memdir | 写 L1、**三处同步**（MEMORY + 原子卡索引 + 指针） | **无** CC 产品内「单按钮执行」；**长对话 skill 可能被截断**，大 vault 需分轮 |
| **Prune / Demote** | `consolidationPrompt` + memdir 修剪 | `memory-md-example` + awk 行长；≤200 行 / 25KB | 规则对齐；**无** CC 内置 **自动归档**到统一 archive 路径的强制实现（SKILL 有描述，依赖人跑） |
| **产出** | 更新后的 MEMORY + 四文件 + 可选报告 | 同上 + **六文件** + `memory/archive/` 约定 + 蒸馏报告模板 | **报告不自动投递**；**open loops** 本库要求不自动删（与 CC 可能不同） |

### 4.3 横切能力

| 能力 | CC | 本库 | **差距** |
|---|---|---|---|
| **与主对话互斥** | 可检测「本轮已写 memory」避免重复抽取 | `memory-touch` + `last-external-write.json` + worker `SESSION_SUMMARY_MUTEX_*` | 手改 Obsidian 仍不触发戳，靠 dream 合并 |
| **类型扩展** | 固定四 memdir | **affect / vault** + 六路 L1 | 已超出 CC；需 **自律**避免 type 滥用 |
| **可重复执行幂等** | 产品保证多次 dream 安全 | 依赖 **session 注释、索引去重** | 极端情况下 **重复指针**需 Demote 清理 |

---

## 5. 弥补计划（ZK 笔记）

- [[05_每日记录/2026/04/20260406/20260406_记忆流水线差距弥补计划_CC对照|20260406 记忆流水线差距弥补计划（CC 对照）]] — 分轨方案、三阶段路线图、开放问题。
- [[05_每日记录/2026/04/20260406/20260406_记忆流水线_CC式实现方案|20260406 记忆流水线 CC 式实现方案]] — **高度模仿 CC 的实现设计**：env、manifest、互斥、`skipIndex`、pipeline 状态、里程碑与验收。
- **L0 `MEMORY.md` 与 L1 六文件**（域映射、统一骨架、禁止项）：`references/l0-l1-six-files-layout.md`（与 CC memdir 四类型 + 本库 affect/vault 扩展对照使用）。

---

## 6. 修订记录

| 日期 | 变更 |
|---|---|
| 2026-04-06 | 初版：extractMemories ↔ worker、autoDream ↔ memory-dream、四类型 ↔ 六类型扩展说明 |
| 2026-04-06 | 增补 **总览对比表**（分层、流水线、类型、触发、约束五块） |
| 2026-04-06 | 增补 **§4 流程阶段、产出与差距**（抽取 / 巩固 / 横切） |
| 2026-04-06 | 增补 **§5**：「差距弥补计划」+「CC 式实现方案」ZK 笔记双链 |
| 2026-04-07 | 增补 **§7**：worker 环境变量表；互斥与 pipeline 落地后更新横切差距表述 |
| 2026-04-07 | worker 同步写 L1「原子卡索引」行（与 MEMORY 同条件）；更新 §3 差异与 §4.1 差距表 |
| 2026-04-07 | 增补 **§7.1**：`auto-memory-dream` 环境变量与 `record-memory-dream-consolidated` |
| 2026-04-06 | 增补 **§5** 链至 **l0-l1-six-files-layout**（L0/L1 分工规约） |
| 2026-04-07 | 对齐 CC 扫读：L0 节标题 **（user｜project｜…）**；`MEMORY.md` 原子行 ``- \`path\`：hook``；worker 落盘与之一致 |
| 2026-04-07 | 原子文件由 `memory/atoms/` 迁至 **`memory/` 根**（`YYYYMMDD_<type>_*.md`）；`MEMORY.md` 指针按域落在各 `## …（type）` 小节，不再单列「## 原子卡」 |
| 2026-04-07 | 全库 **L0 `MEMORY.md` 行**统一为 **Obsidian `[[20260407_feedback_Vault改名须验根last_saved_path|alias]]：hook`**（含 `.md` 路径），与 worker 追加格式一致 |

---

## 7. 附录：`_session-summary-worker` 环境变量（快速表）

| 变量 | 默认 | 含义 |
|---|---:|---|
| `SESSION_SUMMARY_DEBOUNCE_MS` | `180000` | pending 最短空闲等待（毫秒） |
| `SESSION_SUMMARY_DEBOUNCE_MS_OVERRIDE` | — | 写入 pending 的 `debounce_ms_override`（仅 stop hook 子进程继承 env 时生效） |
| `SESSION_SUMMARY_MAX_TRANSCRIPT_CHARS` | `14000` | 送入 CLI 的对话文本上限 |
| `SESSION_SUMMARY_MANIFEST_MAX_CHARS` | `6000` | `buildAtomManifest` 注入上限 |
| `SESSION_SUMMARY_SKIP_MEMORY_MD` | `0` | `1` 时本 pending 带 `skip_memory_md` 或不写 `MEMORY.md` |
| `SESSION_SUMMARY_CLI_TIMEOUT_SEC` | `240` | Cursor CLI 超时秒数 |
| `SESSION_SUMMARY_LLM_CONCURRENCY` | `5` | 同时进行的 CLI 抽取子进程数（1–32）；`WRITE` 仍串行 |
| `SESSION_SUMMARY_MUTEX_MS` | `120000` | 互斥窗口：近期 `memory/pipeline/last-external-write.json` 与 pending 冲突时 |
| `SESSION_SUMMARY_MUTEX_MODE` | `atoms_only` | `atoms_only`：仍抽 atoms，不写 MEMORY；`skip` / `skip_extraction`：本回合不跑 CLI |

互斥戳由 `.cursor/hooks/memory-touch.js`（`postToolUse`）在 Agent 写 `memory/**` 或 `MEMORY.md` 时更新。详设见 `05_每日记录/2026/04/20260406/20260406_记忆流水线_CC式实现方案.md`。

### 7.1 `auto-memory-dream.js`（stop 链，仿 CC autoDream 门限）

| 变量 | 默认 | 含义 |
|---|---:|---|
| `AUTO_MEMORY_DREAM` | （未设则看 config） | `1` 启用；`0` 强制关；未设时读 **`memory/dream/config.json`** 的 `enabled === true` 即启用（可入库免配 shell） |
| `MEMORY_PIPELINE_DISABLE` | — | `1` 时整段跳过（对齐 Bare/关流水线语义） |
| `AUTO_DREAM_MIN_HOURS` | `4` | 距 `memory/dream/state.json` 的 `last_consolidated_at` 最短间隔（CC 侧默认常为 24h，本库更激进） |
| `AUTO_DREAM_MIN_SESSIONS` | `3` | `memory/sessions/*/index.md` 内、巩固后的去重会话块数下限 |
| `AUTO_DREAM_SCAN_MIN_MS` | `600000` | 两次会话扫描间隔（毫秒） |
| `AUTO_DREAM_MUTEX_MS` | `120000` | 与 `last-external-write.json` 的互斥窗口 |
| `AUTO_DREAM_MODE` | `notify` | `notify`：写 `suggestion.json`；`queue`：写 `pending-run.json` |
| `AUTO_DREAM_NOTIFY_DEDUPE_SAME_DAY` | `1` | `0` 则同日可多次写 suggestion |
| `AUTO_DREAM_PENDING_BUSY_MS` | `300000` | worker 在跑且 **该毫秒内有 mtime 的** `.cursor/.session-summary-pending/*.json` 时才让路；`0` 表示不因 pending 挡（演示用） |
| `AUTO_DREAM_LOCK_STALE_SEC` | `120` | `consolidate.lock` 超过该秒数视为陈旧可抢 |

巩固完成后请在 **Vault 根**执行：`node scripts/record-memory-dream-consolidated.js`，以更新 `last_consolidated_at`。详设：`05_每日记录/2026/04/20260406/20260406_memory-dream_仿CC_autoDream调度_详细设计.md`。
