---
name: evidence-research-suite
description: 研究者用户研究方法论套件（10 工具六阶段流水线，从洞察到创新）。基于 2025-12-18 原稿《用户研究十大提示词工具集》。覆盖 Dichter 产品灵魂 / JAS 行为调查 / 四镜深度洞察 / JTBD 目标用户识别 / 文献阅读 / 情感+社交需求 / 功能需求 / 生态设计 / 20 类访谈 / 心理测量学问卷十个工具。Use when 启动新产品系统性用户研究 / 从访谈或评论提炼创新概念 / 品牌战略前的用户洞察前置 / 量化验证产品概念。触发词：研究者 / research / 用户研究方法论 / 十大工具 / 四镜洞察 / JAS / 产品灵魂 / 情感社交需求 / 功能需求 / 访谈设计 / 问卷设计 / Dichter / Jenkins Activity Survey / Jobs to be Done 套件。不触发：单点功能优先级（让位 marty-cagan-perspective）/ 纯切换访谈（让位 bob-moesta-perspective）/ 纯需求量化（让位 tony-ulwick-perspective）/ 品牌定位（让位 april-dunford-perspective）。
---

# 研究者用户研究方法论套件 · v3（split）

> **v3 设计原则**（k 神 review 后重构）：SKILL.md = 路由 + 触发 + 让位，**仅此**。执行规则、自检协议、产出 shape 全部下沉。**Show, don't tell**——agent 看 templates/ + examples/ 学 shape，比看 SKILL.md 文字 100 倍快。

## 何时使用

**显式触发**（关键词命中）：见 frontmatter description 触发词清单。

**隐式触发**（场景识别）：
- 新产品系统性用户研究（非 ad-hoc 单点问题）
- 从原始素材（用户访谈 / 亚马逊评论 / 社交媒体反馈）提取创新概念
- 既有产品做品牌定位前的用户洞察前置（让位 dunford/dichter 前先用本套件取证）
- 量化验证产品概念（结合 tool09 访谈 + tool10 问卷 + tool02 JAS）
- 系统性识别目标用户群与未满足需求

**不触发 / 让位**：
- 单点判断「这个功能该不该做」→ `marty-cagan-perspective`
- 纯切换 / 购买访谈 → `bob-moesta-perspective`
- 纯需求量化（outcome metric + opportunity score）→ `tony-ulwick-perspective`
- 品牌定位 / sales pitch → `april-dunford-perspective` / `positioning-statement`
- 早期假设拆解 → `lean-ux-canvas` / `problem-statement`
- 单工具触发其专家 perspective skill 即可时（如「用 Dichter 视角看」→ `dichter-perspective`）

## 六阶段总览（执行真源在 `references/execution.md` §一）

| Stage | 名称 | Tools | 关键交接 |
|---|---|---|---|
| 1 | 用户识别 | Tool 4 / 7 / 2 | Tool 4 锁版本 → Tool 7/6 inputs |
| 2 | 需求挖掘 | Tool 6 / 9 / 10 | Tool 6 反向类 → Tool 7 边界 + Tool 1 反触发 |
| 3 | 洞察分析 | Tool 3 → Tool 1 | Tool 3 综合洞察 → Tool 1 inputs（Tool 1 紧接 Tool 3，**不开局**） |
| 4 | 产品创新 | Tool 3b | Tool 1 + Tool 3 同时进 inputs（不许跳 Tool 1） |
| 5 | 生态构建 | Tool 8 | — |
| 6 | 持续学习 | Tool 5 | 与任何阶段并行 |

## 触发条件 → 必读 reference（对照表，不允许凭记忆推）

| 触发条件 | 必读 reference |
|---|---|
| 任一 Tool 启动前 | `references/execution.md` §一 Stage→Tool 序列 |
| 跨工具引用 / inputs wikilink | `references/execution.md` §四 跨工具日期格式 |
| 上游 tool 版本升级（v0.x→v1.0 / v1.0→v1.1） | `references/execution.md` §三 Upstream Tool Lock |
| 写 Tool 1 灵魂段 / slogan / brand voice / hero motivator | `references/v1_engineering_extensions.md` § 位置约束 表 Tool 1 行 |
| 写 Tool 3 cross-lens synthesis insight | `references/v1_engineering_extensions.md` § 位置约束 表 Tool 3 行 |
| 写 Tool 3b hero concept / marketing line / pivot statement | `references/v1_engineering_extensions.md` § 位置约束 表 Tool 3b 行 |
| 任一 tool 写跨工具 wikilink「为什么相关」一句 | `references/v1_engineering_extensions.md` § 位置约束 表「任一 tool」行 |
| 收尾 / subagent 报告归并前 | `references/verify.md` §一-§二 triple 协议 + §四 verify_triples.sh |
| GPT 自验 / 验收 / 质量审计 / 版本对比 | `references/gpt_self_acceptance_rubric.md` 全文 |
| verify.md 本身被 edit/split/重构 | `references/verify.md` §九 verify-the-verifier mechanical check |
| 🟡 Simulated expert 模式（无 dedicated skill） | `references/methodology_foundations.md` § 对应理论锚点 |
| 执行某 tool 时（找 prompt 原文） | `references/original_prompt_blocks.md` § Tool N |
| 不会写产出 shape | `templates/tool0X_*.md` + `examples/research_v4_日历机/` 或 `examples/research_v5_productFamilyAI/` |
| v1 工程化深化叠加判断 | `references/v1_engineering_extensions.md` 全文 |
| 从访谈/评论/社媒反馈提取 Tool 3/6/7 需求或洞察 | `.cursor/skills/jtbd-result-audit/references/job_statement_quality_gate.md` + `references/execution.md` § Job Statement Evidence Layer |

## 产出位置

`<project>/01_research/research/research_v<N>_<scenario>/`，11 个 tool 产出文件 + 可选 `_evidence_ledger.md` + `_dogfood_log.md`。

文件命名：`toolXX_<name>_<product>.md`；跨工具引用必须含日期：`[[toolXX_<name>_<product>_YYYYMMDD]]`。详见 `references/execution.md`。

## 与其他 skill 协作

每个工具的方法论锚点对应一位领域专家。当主 agent 要扮演该专家执行时，按 AI-PM CLAUDE.md §4 Expert Skill Gate 三态规则（🟢 Grounded / 🟡 Simulated / 🔴 Forbidden）。常用搭档：
- Tool 1 → `dichter-perspective`
- Tool 3 lens 协奏 → `bob-moesta` / `alan-klement` / `tony-ulwick` / `dichter` / `emily-oster`
- Tool 4 → `bob-moesta-perspective` + `christensen-perspective` 压力测试
- Tool 6 → `eve-rodsky-perspective`（CPE / invisible labor 主线）+ `laura-vanderkam` / `brigid-schulte` / `john-gottman` / `elinor-ochs-celf` 配合
- Tool 7 → `laura-vanderkam-perspective`（time abundance / ringmaster）+ `eve-rodsky`（helper vs ownership lens）
- Tool 9 → `steve-portigal` + `indi-young` + `elinor-ochs-celf` 三 lens
- Tool 10 → 🟡 Dillman simulated（无 dedicated skill）

**重要**：本 skill 不强制 expert persona overlay——可选使用。最小路径是直接按 1218 原稿提示词（references/original_prompt_blocks.md）执行。Persona overlay 是质量提升手段，不是硬约定。

**Job Statement 中间层**：当 Tool 3 / Tool 6 / Tool 7 使用用户访谈、Amazon 评论、社媒反馈等原始素材时，先从 raw data 抽取 Job Statement 表，再进入 emotional/social jobs、functional jobs、四镜洞察或创新概念。缺原话、缺场景、缺 outcome 标尺的条目只能进入待追问，不能升格为需求结论。

## 版本

- **v3.1 — 2026-07-06**：补 Job Statement 证据层。Tool 3/6/7 从原始访谈/评论抽取需求时，先过 `jtbd-result-audit/references/job_statement_quality_gate.md`，再进入聚类、洞察、创新或需求输出。
- **v3 — 2026-05-27**：split 重构（执行规则下沉 `references/execution.md`、triple verify 下沉 `references/verify.md`、templates 升 v4-grade、examples v4+v5 双 ground truth）。Eight Sleep dogfood full_test 验证（Δ +10.25 中等胜出）+ skill-creator eval 6 patch 闭合。dogfood 数字 / verifier 报告 / Patch ID 全部 trace 见 `references/v1_engineering_extensions.md` § 位置约束「触发证据」段 + `代号515/01_research/research_skill_ab_test/eight_sleep/_verify/`。
- **v2.1 — 2026-05-26**：已 archive 至 `evidence-research-suite-v2.1/`（含 v1 深化升推荐 + Tool 1 反 silent failure banner + ~10 layer 元话语）。仅作档案。
- **v2.0 — 2026-05-26**：dogfood 跑 515 product Family AI（产出 596K 11 个 tool 文件）。已含在 v2.1 内。
- **v1 — 2025-12-18 至 2026-05-26**：archive 至 `evidence-research-suite-v1/`（4 轮迭代沉淀，工程化深化产物）。仅作档案。
