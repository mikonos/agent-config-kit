---
date: {YYYY-MM-DD}
type: research_output
status: draft
product: {Product_Name}
tool: "07"
phase: 1
mode: single_doc
tags: [research-research, tool-output, tool07, functional-needs]
---

# 工具7：功能需求清单 — {Product_Name}

> **方法论**：JTBD Functional Jobs + Outcome-Driven Innovation (ODI)
> **目标用户**：{Primary_User_Group（来自Tool4）}
> **产品概念**：{Product_Concept}
> **来源说明**：本稿基于 Tool 4 final v{X.X} 的 G1-G{N} + X1-X{M} handoff（Rule 16）。
> **推断与证据**：本文件内嵌推断与证据节，覆盖四力量化、切换访谈协议、ODI desired-outcome metric 推导、Moesta kill-list（被剔除的伪需求及切换事件证据）、P0/P1/P2 假设排序论证。

---

## 0. 速查（先扫一眼再读正文）

| 概念 | 说人话翻译 |
|---|---|
| **Official functional jobs** | 本工具正式产出的 {N} 条 functional jobs（控制在 20-30 条），见 §2 |
| **附录池** | 主综合方拆解过但未升正式的候选 jobs，见附录 A |
| **provisional hypotheses** | P0/P1/P2 是**假设排序**（依赖 Tool 9/10 真访谈验证），不是已验证优先级；见 §3 |
| **[Big Hire]** | 客户切换时主动 hire 的事——营销大声卖 |
| **[Anxiety-blocker]** | 客户怕的事——营销安静化解，反向反向反向（不是 Big Hire） |
| **承重能力体检（Rule 18）** | 依赖未验证技术能力的需求列单独体检表，见 §5 |
| **Tool 4 → Tool 7 handoff** | G1-G{N} 情境群 + X1-X{M} 横切维度并列，见 §1 |

---

## 1. Tool 4 → Tool 7 handoff（Rule 16 合规）

> **强制**：本节必须并列列全 Tool 4 输出的两类——情境群 + 横切维度。漏掉任一 = Rule 16 失败 = blocked。

### 1.1 情境群（situational groups）

| ID | 情境定义（不是 persona，是处境） | Tool 4 优先级（圈层）|
|---|---|---|
| G1 | {一句话情境，如「家里刚有大变化（新生儿 / 搬家 / 老人介入）」} | {天使 / 靶心 / 核心 / 战略 / 辐射 / 共生} |
| G2 | ... | ... |
| ... | ... | ... |

### 1.2 横切维度（orthogonal dimensions）

| ID | 维度定义（跨情境群的人群类别）| Tool 4 优先级 |
|---|---|---|
| X1 | {一句话维度，如「DIY 自建派 / 礼物购买者 / 移民家庭 / ADHD/ND / 隐私敏感者」} | ... |
| X2 | ... | ... |
| ... | ... | ... |

### 1.3 G8/X switching audit（来自 Tool 4 新 handoff 时强制补）

每个新加入的 G/X 必须补一段 switching audit：

| 群 ID | 旧方案 | 触发日 | 第一次行动 | 焦虑（什么让她不敢换）| 留存风险 | 对应 official jobs（§2 编号）|
|---|---|---|---|---|---|---|
| G8 | ... | ... | ... | ... | ... | A1, B3, ... |
| X1 | ... | ... | ... | ... | ... | ... |

---

## 2. 功能需求清单（Official Functional Jobs · 20-30 条 ODI）

> **强制格式**：每条保留 ODI 原句（`direction + metric + object + context`）+ 人话翻译。
> **强制裁剪**：official 数量控制在 20-30 条。多出的去附录 A，不计正式产出。
> **强制约束**：每条三段——方向（用户从什么处境走向什么处境）+ 抓手（关键一招）+ 边界（别偏成什么）。只有「别偏成什么」=半张地图，不合格。
> **架构约束/技术能力不在此处**——进 §5 Rule 18 能力体检。

### 2.1 official jobs 主清单

| ID | ODI 原句 | 人话翻译 | 对应群 G/X | hire 类型 | switching evidence | 三段（方向/抓手/边界）|
|---|---|---|---|---|---|---|
| A1 | Minimize the time it takes to {direction} {metric} {object} {context} | 当我{触发场景}时，我希望{抓手}，以便{底层动机} | G3, X2 | [Big Hire] | {某用户原话 / 切换事件 / [HYPOTHESIS]} | 方向：{从 A 到 B}; 抓手：{一招}; 边界：{别偏成 C} |
| A2 | ... | ... | ... | [Anxiety-blocker] | ... | ... |
| ... | ... | ... | ... | ... | ... | ... |

### 2.2 hire 类型判定 gate（强制 Big Hire vs Anxiety-blocker 区分）

> **判定规则**：标 [Big Hire] 必须能写出**真实 switching event**（旧方案是什么 / 哪天换的 / 第一次行动）。
> 不能写 switching event 的，标 [Anxiety-blocker]——客户怕的事，营销**反向**处理（安静化解，不大声卖）。
> 混标 = D5 营销台账上信号错位 = 阻塞 Phase 3 close。

| ID | 标签 | switching event（Big Hire 必填）/ anxiety 触发场景（Anxiety-blocker 必填）|
|---|---|---|
| A1 | [Big Hire] | 2024 春假，孩子第三次错过夏令营报名截止日，她那晚试过 7 个 app 后哭了——第二天搜「family AI calendar」 |
| A5 | [Anxiety-blocker] | 怕：设备替她发消息后丈夫以为她在偷懒；触发：自动化档位 ≥3 |
| ... | ... | ... |

### 2.3 Moesta kill-list（剔除清单 · 进主稿不进附录）

> 从 candidate 池中被 Moesta 切换访谈 / kill-list 判定剔除的伪需求；进主稿是为了让读者看到哪些不做、为什么不做。

| 原 candidate | 裁决 | switching 理由 | 影响优先级 |
|---|---|---|---|
| {原 candidate} | KILL | 没有真实 switching event，是 survey-derived wish | — |
| {原 candidate} | REVISE → A3 | 原 framing 是 feature wish；switching event 揭示真实需求是 X，已重写为 A3 | 升 P1 |
| {原 candidate} | DEFER | trigger 真实但仅出现于 G8（小群体）；先做 G3 主流 | 待 G8 验证 |

---

## 3. 优先级假设矩阵（provisional hypotheses）

> **强制改名**：不写「P0 必须先做」这种已验证语气——本节是**假设排序**，依赖 Tool 9/10 真访谈和工程预研验证。
> 机会分**全部标 `[ODI 假设分]`**——importance × satisfaction 没做真用户调研前，全是估算。

| 优先级假设 | 需求 ID | ODI 假设分 | 核心理由（一句话）| 依赖哪条承重假设（§6 ID）|
|---|---|---|---|---|
| **P0（假设：必须先做）** | A1, A3, B2 | 16-19 [ODI 假设分] | 没有这些 G3 不能产生 big-hire switching | LB-1, LB-3 |
| **P1（假设：差异化）** | C1, C4 | 12-15 [ODI 假设分] | 竞品没做到/没做好 | LB-2 |
| **P2（假设：体验提升）** | D2, E3 | 8-11 [ODI 假设分] | 不影响 V1 成败 | — |

---

## 4. {场景类别} 完整明细（按用户处境编排，不按产品方案）

> D2 编排维度强制：节标题必须是「用户在某处境里要从 A 走向 B」，不是「产品要做 X 抓手」。

### 4.1 {场景类别1 — 核心场景}

**A1.** 当我{具体情境触发}时，我希望**{功能期望}**，以便{底层动机}。

- ODI 原句：`{direction + metric + object + context}`
- hire 类型：[Big Hire] / [Anxiety-blocker]
- 三段：方向：{...} / 抓手：{...} / 边界：{...}

**A2.** ...

### 4.2 {场景类别2 — 差异化场景}

...

---

## 5. 承重能力体检（Rule 18 · 技术能力 in principle / in practice）

> 触发条件：本工具有需求依赖未验证的技术能力（AI 模型准确率 / 传感器精度 / 第三方 API SLA / 外部数据可用性）。
> 强制：架构约束、技术能力**不混进** §2 functional jobs；放本节。

| 能力 ID | 能力描述 | 支撑哪些 official jobs | 理论上限（in principle）| 眼下实际（in practice）| 距可用还差什么 | 不成立后果 |
|---|---|---|---|---|---|---|
| CB-1 | AI 模型在「家庭消息批量分拣」任务上 ≥85% 准确率 | A5, B3 | 理论上 GPT-4 级模型可达 92%+ | 现成模型在真实家庭群 1000 条样本测试 ~76%，错分类含安全/医疗 | 1000 条真实样本微调 + 安全/医疗类目专用过滤层 | A5/B3 P0 假设失效，档 2 需降档 1 |
| CB-2 | 本地处理保证隐私 | A1, A3 | 端侧推理理论可行 | M2/M3 芯片 7B 模型推理速度 ~3-5 token/s，体验 borderline | 推理优化或云本地混合架构 | 隐私承诺降级，hero「the home keeps track」失承诺力 |
| ... | ... | ... | ... | ... | ... | ... |

---

## 6. 承重假设清单（D6）

> 标准表头来自 `templates/_d6_load_bearing.md`，强制使用，不许散写。

| ID | 假设 | 证据等级 | 失效后果（人话）| 建议验证方式（Tool 9/10 交接）|
|---|---|---|---|---|
| LB-1 | G3 妈妈在「孩子开学第一周」会主动 hire 一个家庭 AI 中心 | H | 若错 → P0 A1/A3 整体降级；Q3 back-to-school 投放计划作废 | Tool 9 套餐 A 切换访谈 8 户 G3，问「上一次主动想找一个能帮你记/想/协调的东西，是哪一天，触发是什么」|
| LB-2 | 横切 X2（ADHD/ND）愿意为 AI 记忆功能付溢价 | H | 若错 → X2 不构成天使支付池；首年定价模型 ARPU 模型崩 | Tool 10 Van Westendorp PSM N=200 X2 子样本 + Tool 9 X2 深访 5 户 |
| ... | ... | ... | ... | ... |

---

## 7. 给 Tool 6 / Tool 9 / Tool 10 / 营销台账的交接

### 7.1 给 Tool 6 反向需求 / anxiety branch

- §2.2 标 [Anxiety-blocker] 的 jobs 全部要在 Tool 6 anxiety 段落对应一条反向需求条目

### 7.2 给 Tool 9 访谈题

- 每条承重假设 ID → 对应 probe tree

### 7.3 给 Tool 10 问卷题

- importance × satisfaction 题按 §3 优先级假设矩阵设计

### 7.4 给营销台账 D5（Rule 14 append）

- §2.2 [Big Hire] 标签 → 营销台账 §正向卖点段
- §2.2 [Anxiety-blocker] 标签 → 营销台账 §焦虑阻断器段（**反向**处理）
- demo flow / GTM 渠道 / trust 架构线索 → 营销台账 §对应段

---

## 8. 附录 A · 候选池（不计正式产出）

> 候选条目数：{N - 30} 条；不进 §2 official jobs。

| ID | 候选 ODI 句 | 不升正式的理由 |
|---|---|---|
| Z1 | ... | switching evidence 太弱 / 与 A3 重复 / 待 Tool 9 验证后再升 |
| ... | ... | ... |

---

## 推断与证据

> 写清关键论证链、证据来源、假设标签、分歧裁决和反驳条件。不要另建推断文件。

### A. ODI metric 推导

> 每条 ODI 句 direction / metric / object / context 四元素的推导依据。

### B. Moesta switching evidence

> 每条 [Big Hire] 的 switching event 来源（用户访谈 / 评论数据 / [HYPOTHESIS]）+ 反方 kill-list 全列。

### C. P0/P1/P2 假设排序论证

> importance × satisfaction 假设分推导（标 [ODI 假设分]）；承重假设 LB-N 与优先级的对应关系。

### D. Tool 4 → Tool 7 handoff 完整对照

> Tool 4 G1-G{N} + X1-X{M} 每个群在 §2 official jobs 里都覆盖到（不许漏 X）。

### E. Rule 11 cascade 状态（若上游 Tool 1 / Tool 4 改版）

> kill log 表，引用 `references/cascade_sop.md`。

### F. Rule 18 能力体检详细推导

> §5 各 CB-N 的 in principle / in practice 论证依据。

---

*基于 JTBD Functional Jobs + ODI 框架 · 产品：{Product_Name} · 含推断与证据*
