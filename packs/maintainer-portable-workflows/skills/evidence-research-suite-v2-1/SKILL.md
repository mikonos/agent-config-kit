---
name: evidence-research-suite-v2-1
legacy: true
description: "[ARCHIVED v2.1] 研究者用户研究方法论套件 v2.1（使用期 2026-05-26 至 2026-05-27）。已被 research-research-suite v3（split 重构后）取代。仅作档案保留。不要按关键词触发本 skill；新工作请使用 research-research-suite。v3 split 的原因详见 _skill_optimization_from_v4v5.md + k 神 review verdict（march of nines 错位 + SKILL.md 长成 mini-OS 而非 prompt）。"
---

> **⚠️ ARCHIVED — v2.1，已退役**
> 本 skill 是 research-research-suite v2.1，于 2026-05-27 经 k 神 review 后判定 SKILL.md 长到 23K 已超出 healthy prompt 边界，被 v3 split 重构取代。v2.1 完整内容（含 v1 工程化深化推荐表 + 7 类扩展整合）保留作为档案。
> 路由层不再指向本 skill。如需调用方法论流水线，请使用新版 `research-research-suite`（split 后 SKILL.md ≤3K + references/execution.md + references/verify.md + v4-grade templates + examples spec by example）。

# 研究者用户研究方法论套件

> **真源**：[[20251218_用户研究十大提示词工具集_从洞察到创新的完整方法论]]
> **形态**：10 个用户研究提示词工具，按六阶段流水线串联，从用户识别 → 需求挖掘 → 洞察分析 → 产品创新 → 生态构建 → 持续学习。
> **边界声明（重要）**：本套件是**用户研究工具**，不是品牌方法论。用户研究是品牌工作的关键前置输入，但品牌战略本身需要其他方法论（品牌定位声明、品牌屋、品牌原型选择）——见「与其他 skill 的分流」。

---

## 何时使用本 skill

### 显式触发

「用研究者的方法」「跑一遍研究者十大工具」「research」「四镜洞察」「JAS 调查」「找 Job Performers」「Jenkins Activity Survey」「情感需求 + 社交需求」「功能需求 When I... I hope... so that...」「20 类访谈问题」「Dichter 产品灵魂」「产品生态共创/协作」「学术论文结构化阅读」「从洞察到创新」「用户研究十大工具」。

### 隐式触发

- 为一个**新产品**做系统性用户研究（不是 ad-hoc 单点问题）。
- 要从原始素材（用户访谈、亚马逊评论、社交媒体反馈）**提取创新概念**。
- 既有产品做**品牌定位**前的用户洞察前置（让位 dunford/dichter 之前先用本套件取证）。
- **量化验证**一个产品概念（结合 tool09 访谈 + tool10 问卷 + tool02 JAS）。
- 系统性识别产品的**目标用户群与未满足需求**。

### 不触发（让位）

- 单点判断「这个功能该不该做」→ `marty-cagan-perspective`（四风险）。
- 纯**切换/购买访谈**「客户为什么今天买」→ `bob-moesta-perspective`（Demand-Side JTBD）。
- 纯**需求量化** outcome metric + opportunity score → `tony-ulwick-perspective`（ODI）。
- 纯**品牌定位/sales pitch** → `april-dunford-perspective` / `positioning-statement`。
- **deep consumer motivation** 单点动机诊断 → `dichter-perspective`（但 tool01 仍用 Dichter 四维框架）。
- 早期假设拆解 → `lean-ux-canvas` / `problem-statement`。

---

## 六阶段执行序列（执行顺序的真源 · 拷贝即可跑）

**⚠️ 关键：工具编号 ≠ 执行顺序。执行严格按下列阶段序列，不要按 Tool 1 → 2 → 3 → ... 跑。**

```text
Stage 1  用户识别      →  [Tool 4, Tool 7, Tool 2]
Stage 2  需求挖掘      →  [Tool 6, Tool 9, Tool 10]
Stage 3  洞察分析      →  [Tool 3, Tool 1]
Stage 4  产品创新      →  [Tool 3b]            （= Tool 3 提示词的创新输出二次运行）
Stage 5  生态构建      →  [Tool 8]
Stage 6  持续学习      →  [Tool 5]              （独立支撑，可与任何阶段并行）
```

执行规则：
- **阶段间严格上下游**：上一阶段产出齐了才能开下一阶段，禁止跳阶段。
- **阶段内可并行**：方括号内的工具可同顺序、不同顺序、或并行 subagent，但都必须在本阶段闭合后才进入下一阶段。
- **执行入口**：每次 invoke 这个 skill 时，agent 把上述 `Stage X → [...]` 序列**完整拷贝到工作上下文**，作为 single source of truth 跟踪进度。

### 工序纠偏（为什么要这样排）

1218 原稿明确说阶段顺序如上，tool 编号只是工具库索引：

- Tool 1（产品灵魂）属于**阶段 3 洞察分析的后半段**，紧接 Tool 3 之后；不是开局。
- Tool 3b（创新输出）是 Tool 3 同一提示词在创新阶段的二次运行，紧接 Tool 1 之后。
- Tool 5（文献阅读）独立支撑，在阶段 6 持续学习层，可与任何阶段并行。

「新品开发全流程」的分周节奏（1218 §722-743）：
- **第 1 周** 用户识别：Tool 4 → Tool 6 → Tool 7（初步 JTBD 三维）
- **第 2 周** 深度调研：Tool 9 设计 → 执行访谈 → Tool 3 分析
- **第 3 周** 量化验证：Tool 10 设计 → Tool 2 行为分群
- **第 4 周** 创新输出：Tool 1 → Tool 3 创新部分（Tool 3b）→ Tool 8

跨工具引用必须**锁源工具版本**，用 `[[Tool X v日期]]` 写明，便于追溯。

---

## 工具库索引（按编号，非执行顺序）

**⚠️ 本节按 Tool 编号排序便于查阅，不代表执行顺序。执行顺序见上面「六阶段执行序列」。**

每个工具的完整提示词原文见 [`references/original_prompt_blocks.md`](references/original_prompt_blocks.md)。每个工具的产出模板见 `templates/tool0X_<name>.md`。理论锚点见 [`references/methodology_foundations.md`](references/methodology_foundations.md)。

### Tool 1 — 产品灵魂 Soul of Product

- **核心问题**：产品对用户的深层心理意义是什么？
- **执行阶段**：Stage 3 洞察分析后半段（紧接 Tool 3 之后），**不是开局**。
- **方法论锚点**：Dichter 品牌心理学四维（核心问题 / 社会参照框架 / 国家文化 / 当代世界）
- **输入**：产品定义 + 目标市场 + 目标人群 + Tool 3 综合洞察
- **输出**：四维心理分析 + 产品灵魂段落 + 3 条情感共鸣广告语 + 用户内心独白式品牌信息
- **⚠️ 反 silent failure 注脚（重要）**：Tool 1 的「广告语」和「品牌信息」是**用户洞察的可读化呈现**，**不是品牌定稿**。评价标准是「四维心理分析是否扎根证据 + 灵魂段落是否说出未说之言」，**不是**「广告语朗朗上口吗 / 能不能直接投放」。品牌定稿、视觉识别、传播策略需让位 `april-dunford-perspective` / `positioning-statement` / 外部品牌战略方法。把 Tool 1 输出当广告创意验收 = silent failure。
- **提示词**：`references/original_prompt_blocks.md#tool-1`
- **模板**：`templates/tool01_product_soul.md`

### Tool 2 — 詹金斯行为调查 Jenkins Activity Survey

- **核心问题**：用户的行为决策倾向（时间紧迫 / 工作投入 / 进取竞争）是什么？
- **方法论锚点**：Jenkins Activity Survey（Type A Behavior Pattern 量表）
- **输入**：产品名称
- **输出**：Likert 5 点问卷（**硬约定**）；SI/JI/HDC 三维各 5-7 题
- **格式硬约定**：Likert 1=Strongly Disagree … 5=Strongly Agree 必须原文用；Format: Chinese
- **提示词**：`references/original_prompt_blocks.md#tool-2`
- **模板**：`templates/tool02_jas_survey.md`

### Tool 3 — 四镜深度洞察与创新框架 Four-Lens Deep Insight & Innovation Framework

- **核心问题**：用户反馈中隐藏的模式、矛盾、情感、自动化需求是什么？
- **方法论锚点**：消费者心理学四镜（Find Patterns / Find Contradictions / Find Feelings / Find Shortcuts）
- **输入**：产品介绍 + 用户访谈/评论文本
- **输出**：四个洞察镜头 + 综合洞察 + 创新概念 3-5 个 + 1 个英雄概念（hero concept）
- **格式硬约定**：四镜各含「重复行为/抱怨 → 结构性张力 → 设计启示」；禁止只做摘要（原文：Please do NOT summarize the text; reveal the hidden structures beneath it）
- **提示词**：`references/original_prompt_blocks.md#tool-3`
- **模板**：`templates/tool03_four_lens.md`

### Tool 3b — 创新输出（Tool 3 创新部分）

- **核心问题**：把四镜洞察转化为产品创新概念。
- **位置**：阶段 4 产品创新，紧接 Tool 1 之后；不是独立工具，是 Tool 3 提示词后半段的二次运行。
- **输入**：Tool 3 综合洞察 + Tool 1 产品灵魂
- **输出**：新形式（form factors）+ 新功能 + 新场景/仪式 + 1 个英雄概念
- **提示词**：复用 Tool 3 提示词（执行时只取 Output 第 6 段「Based on all insights above, propose...」）
- **模板**：`templates/tool03b_innovation.md`

### Tool 4 — 目标用户识别 Finding Job Performers

- **核心问题**：谁是产品的核心工作执行者（Job Performers）？
- **方法论锚点**：JTBD 用户分群
- **输入**：产品定义
- **输出**：4 象限用户分群图 + 每群独特需求/痛点 + X/Y 轴属性定义
- **格式硬约定**：用 MECE 原则；X/Y 轴必须是对立属性极端；需求**基于 needs/pain points**而非人口/地理/职业（原文：focus on user needs or pain points rather than demographic, geographic, or occupational dimensions）
- **提示词**：`references/original_prompt_blocks.md#tool-4`
- **模板**：`templates/tool04_target_users.md`

### Tool 5 — 文献阅读 Reading Academic Papers

- **核心问题**：学术论文的核心贡献、局限、对产品的启示是什么？
- **方法论锚点**：学术研究方法论（背景/目标/假设/框架/方法/分析/结论/局限/参考文献/三维评估）
- **输入**：论文 PDF
- **输出**：结构化摘要 + 11 段标准化分析 + 论文质量评估（科学性 / 创新性 / 学术严谨度）
- **提示词**：`references/original_prompt_blocks.md#tool-5`
- **模板**：`templates/tool05_literature.md`
- **独立性**：本工具支撑阶段 6 持续学习，与其他工具松耦合，可单独使用。

### Tool 6 — 情感与社交需求 Finding Emotional & Social Jobs

- **核心问题**：用户希望感受/避免感受什么；希望在他人眼中呈现什么形象？
- **方法论锚点**：JTBD 情感与社交维度
- **输入**：目标用户（来自 Tool 4）+ 产品概念
- **输出**：10-15 个情感需求（feel / avoid feeling）+ 10-15 个社交需求（appear as / avoid appearing as）
- **格式硬约定**：粗体 job name + 一句描述；情感行首必须是 `feel` 或 `avoid feeling`；社交行首必须是 `appear as` 或 `avoid appearing as`；每项**第一人称动词开头**；Format: Chinese
- **Job Statement 兼容闸**：若输入含访谈/评论/反馈，先按 `.cursor/skills/jtbd-result-audit/references/job_statement_quality_gate.md` 抽取 JS 九格；缺原话/场景的条目只进待追问，不进主需求表
- **提示词**：`references/original_prompt_blocks.md#tool-6`
- **模板**：`templates/tool06_emotional_social.md`

### Tool 7 — 功能需求 Finding Functional Jobs

- **核心问题**：用户在什么情境下希望产品完成什么具体任务？
- **方法论锚点**：JTBD 功能维度
- **输入**：目标用户（来自 Tool 4）+ 产品概念
- **输出**：15-20 个功能需求，格式「When I... I hope... so that...」
- **格式硬约定**：每条**第一人称动词开头**；单一任务（no conjunctions，不用 and 连接）；完整因果链（情境-期望-目标）；不被既有产品功能限定
- **Job Statement 兼容闸**：每条 functional job 至少回指一个 JS id 或标 `hypothesis / 待追问`；不能把产品功能写成 Main Job
- **提示词**：`references/original_prompt_blocks.md#tool-7`
- **模板**：`templates/tool07_functional_needs.md`

### Tool 8 — 产品生态设计 Building Product Ecosystem

- **核心问题**：如何构建共创/协作生态以支撑用户全生命周期体验？
- **方法论锚点**：JTBD 全维度（功能 / 情感 / 社交 / 相关任务）+ 用户使用旅程 8 段（Define / Locate / Prepare / Confirm / Execute / Monitor / Modify / Conclude）
- **输入**：产品概念 + 目标用户 + 关键产品特征 + 关键使用场景
- **输出**：共创生态清单（开放平台 + 第三方）+ 协作生态清单（互联互通产品）+ 每项的价值说明
- **提示词**：`references/original_prompt_blocks.md#tool-8`
- **模板**：`templates/tool08_ecosystem.md`

### Tool 9 — 访谈问题设计 User Interview Questions Design

- **核心问题**：如何通过 20 类问题激发用户真实表达和深层动机？
- **方法论锚点**：访谈心理学 20 种问题类型（Background / Contextual / Knowledge / Historical / Attitude / Cognitive / Expectation / Competitive / Social / Frequency / Learnability / Barrier / Compatibility / Recovery / Prioritization / Redundancy / Relational / Implicit / Hypothetical / Comparative）
- **输入**：研究背景 + 受访人群特征 + 产品设想
- **输出**：20 类问题各 3-5 个具体问题，问题间有逻辑递进；Format: Chinese 或指定语言
- **格式硬约定**：Clarity / Child-Friendly / Aided Recall / Conciseness / Neutrality 五原则；Tone: Friendly + Neutral + Clear + Supportive
- **提示词**：`references/original_prompt_blocks.md#tool-9`
- **模板**：`templates/tool09_interview_questions.md`

### Tool 10 — 问卷设计 Questionnaire Design

- **核心问题**：如何量化验证产品概念与用户需求的适配度？
- **方法论锚点**：心理测量学五维（Knowledge / Evaluation / Behavior / Frequency / Psychology）
- **输入**：样本人群特征与样本量 + 准备研发的产品 + 创新概念若干
- **输出**：封闭式问卷（单选 + Likert），全部可量化分析
- **格式硬约定**：**禁用开放式问题**（原文：Avoid open-ended questions）；只用单选 + Likert；五项 Standards（Factorial Structure / Content Validity / Discriminant Validity / Predictive Validity / Construct Validity）
- **提示词**：`references/original_prompt_blocks.md#tool-10`
- **模板**：`templates/tool10_survey_design.md`

---

## 输出规范（硬约定，按 1218 原稿）

### 通用 YAML frontmatter

每个工具产出文档必须含：

```yaml
---
date: YYYY-MM-DD
type: research / tool-output
tool: tool01-product-soul / tool02-jas / ...（精确到工具名）
product: <产品代号或名称>
language: zh-CN / en / 其他
status: draft / in-review / approved
inputs:
  - <上游工具产出文件名或外部数据源>
---
```

### 文件命名

`toolXX_<工具名拼音或英文>_<产品代号>.md`（如 `tool01_product_soul_productFamilyAIHub.md`）。

### 跨工具引用

用 `[[wiki-link]]`，附版本日期或迭代号（例：`[[tool04_target_users_productFamilyAIHub_20260326]]`）。引用上游产出时**必须锁版本**，便于产出文档追溯到具体快照。

### 语言约定

默认 Format: Chinese（1218 原稿全部工具的硬约定，仅 Tool 1 允许中英双语广告语，Tool 9 允许指定其他语言）。Prompt body 保留英文便于复制。

<!-- v2.1 UPGRADE: 在硬约定输出规范末尾追加「推荐扩展」段，让 agent 在写每个工具产出时知道默认要 append 哪些 v1 深化段落。 -->

### 推荐扩展（v1 深化 · v2.1 默认开启）

下表是每个 Tool 默认推荐叠加的 v1 深化项。**默认开启即应当 append；若关闭，必须在产出顶部「v1 深化声明」段写明 why not**（关闭场景详见下节「与 v1 工程化扩展的关系」表格 + `v1_engineering_extensions.md`）。

| Tool | 推荐深化项（默认 append） |
|---|---|
| Tool 1（产品灵魂） | 承重假设清单（把产品定位/灵魂的承重假设挂上失效后果） |
| Tool 3（四镜深度洞察） | 跨工具证据台账锚点段（起锚 evidence map，给后续工具喂证据指针） |
| Tool 3b（创新输出） | B/F/H 角色变体（若 Tool 4 已开角色变体）+ 承重假设清单（创新概念的承重假设） |
| Tool 4（目标用户） | Bull's Eye 渗透路径（angel → bull's eye → core → strategic → radiation → symbiotic）+ 下游信号台账起锚 |
| Tool 6（情感与社交） | 正反两类需求拆分（正向 demand vs 反向 anxiety）+ 承重假设清单 + B/F/H 角色变体（若 Tool 4 ≥2 群） + 下游信号台账 append |
| Tool 7（功能需求） | 三段需求结构（方向 + 抓手 + 边界）+ 承重假设清单 + B/F/H 角色变体（若 Tool 4 ≥2 群） + 下游信号台账 append |
| Tool 8（产品生态） | 跨工具证据台账闭合（收尾合并所有 evidence map 节点）+ 下游信号台账闭合（卖点/定位综合） |

补充硬约束（2026-07-06）：Tool 3 / 6 / 7 如果从 raw user voice 抽需求，必须先产出 Job Statement 证据层；v1 深化不能替代 JS 九格，也不能把评论抱怨直接升格为创新概念。

未列出的 Tool 2 / Tool 5 / Tool 9 / Tool 10 默认不强制叠加 v1 深化（这些工具产出形态固定，深化收益低）。

---

<!-- v2.1 UPGRADE: v1 深化从「可选扩展层」升级为「推荐默认开启层」。原 framing 让 v5 dogfood 时产出量级 < v4 example，因为 SKILL 硬约定不跟 v4 走、deepen 项被解读为"看心情加"。 -->

## 与 v1 工程化扩展的关系（v2.1：默认开启 + 关闭场景）

`examples/research_v4_日历机/` 是 2026-03 用 v1 流水线产出的一份完整范本，体现了 v1 在 4 轮迭代中沉淀的工程化深化（承重假设清单、Bull's Eye 渗透路径、三段需求 = 方向+抓手+边界、正反两类需求拆分、B/F/H 角色变体、跨工具证据台账、下游信号台账等）。

**v2.1 关键变更**：v1 深化是 4 轮迭代沉淀的工程化经验，**推荐默认开启**，详见 [`references/v1_engineering_extensions.md`](references/v1_engineering_extensions.md)。

**两层硬度声明**：
- **SKILL.md 硬约定（1218 原稿）= 产出最小闸门**（必做，不可协商）
- **v1 深化 = 产出推荐质量基线**（默认开启除非有明确关闭场景）

**7 类深化的默认行为与关闭场景**：

| 深化项 | 挂在 Tool | 默认行为 | 关闭场景（关闭须在产出顶部 why not） |
|---|---|---|---|
| 1. 承重假设清单 | Tool 1 / Tool 6 / Tool 7 / Tool 3b | 默认开启 | 超小型项目（< 5 个 functional job） |
| 2. 正反两类需求拆分 | Tool 6 | 默认开启 | 纯 efficiency 工具产品（无 anxiety 维度） |
| 3. 三段需求（方向+抓手+边界） | Tool 7 | 默认开启 | 早期 problem space 探索（pivot 阶段） |
| 4. Bull's Eye 渗透路径 | Tool 4 | 默认开启（dogfood v5 已开） | 单一目标用户场景 |
| 5. B/F/H 角色变体卷 | Tool 6 / Tool 7 / Tool 3b | 当 Tool 4 出现 ≥2 个高优先群时默认开启 | 单群产品 |
| 6. 跨工具证据台账 | Tool 3 起锚，Tool 8 收尾闭合 | 默认开启 | 单轮研究无版本迭代需求 |
| 7. 下游信号台账 | Tool 4 / Tool 6 / Tool 7 收尾 | 默认开启 | 研究产出不喂 GTM / 文案 / 渠道 |

**模板层 vs 推荐层**：
- `templates/` 模板按 1218 原稿硬约定（最小闸门）。
- v1 深化作为推荐叠加，主综合方需要在每个工具产出时主动 append 对应深化段落。
- 关闭某项深化时必须在产出顶部「v1 深化声明」段写明 why not，不能默写省略。

---

## Prerequisites（启动前清单）

在激活本 skill 之前，确认你能回答以下问题：

- [ ] **产品定义**：产品是什么？核心差异化在哪？
- [ ] **市场上下文**：目标市场、地理、价格区间、竞争格局。
- [ ] **已有数据**（如果有）：用户评论、问卷数据、JTBD 分析、会议纪要、竞品分析。
- [ ] **目标用户假设**：你认为主要用户是谁？
- [ ] **语言要求**：产出/访谈/问卷用什么语言？

任一项缺失先补齐再开工——本套件的输出质量严重依赖 prerequisite 的完整度。

---

## 执行流程

### 完整六阶段（新产品立项）

按主线顺序执行；每个阶段内的工具可并行（subagent 视情况隔离避免上下文污染）；阶段间是严格上下游。

1. **阶段 1 用户识别**：Tool 4 → Tool 7 → Tool 2
2. **阶段 2 需求挖掘**：Tool 6 → Tool 9 →（执行访谈，不在本 skill 内）→ Tool 10
3. **阶段 3 洞察分析**：Tool 3（基于已收集的访谈/评论）→ Tool 1（基于 Tool 3 综合洞察）
4. **阶段 4 产品创新**：Tool 3b（Tool 3 提示词的创新输出段）→ 紧接 Tool 1
5. **阶段 5 生态构建**：Tool 8
6. **阶段 6 持续学习**：Tool 5（独立支撑，可与任何阶段并行）

### 单工具触发

可独立调用任一工具完成局部任务（如品牌重塑只跑 Tool 1+6；产品迭代只跑 Tool 3）。1218 §720-756 给了三套常见组合：
- **场景 1 新品开发**：第 1-4 周分阶段（见上文「工序纠偏」）
- **场景 2 品牌重塑**：Tool 1 + Tool 6 + Tool 3
- **场景 3 产品迭代**：用户反馈 → Tool 3 → 新概念；需求变化 → Tool 6 + Tool 7 → 功能优先级

### 与本仓 perspective skill 的协作

每个工具的方法论锚点对应一位领域专家。当主 agent 要扮演该专家执行时，按 AI-PM CLAUDE.md §4 Expert Skill Gate 三态规则：

- 🟢 **Grounded**：本仓有对应 perspective skill 时，先 Read 该 SKILL.md 再以其视角执行。
  - Tool 1 → `dichter-perspective`
  - Tool 3 / Tool 6 / Tool 7 → 主要用 1218 原稿提示词；可选搭配 `bob-moesta-perspective`（切换访谈）/ `tony-ulwick-perspective`（outcome metric）/ `alan-klement-perspective`（job story trigger moment）
  - Tool 4 → 可选 `bob-moesta-perspective` + `christensen-perspective` 做压力测试
  - Tool 9 → 可选 `steve-portigal-perspective`（probe tree）/ `indi-young-perspective`（listening session）/ `elinor-ochs-celf-perspective`（参与框架）

- 🟡 **Simulated**：无对应 skill 时（如 Jenkins、Dillman），用训练数据 + `references/methodology_foundations.md` 锚点执行，开场声明「（基于训练数据，本仓暂无 skill）」。

- 🔴 **Forbidden**：列不出该专家 ≥2 个代表作/核心概念/术语，禁止挂名；改用 1218 原稿通用方法或直说「不熟悉此专家」。

**重要**：本 skill 不强制 expert persona 路由——可选使用。最小路径是直接按 1218 原稿提示词执行。Persona overlay 是质量提升手段，不是硬约定。

---

## 反触发与边界

### 边界声明（1218 §775-784 原话）

> 本工具集是**用户研究工具**，而非品牌方法论。但用户研究是品牌工作的**关键前置输入**。

**品牌战略的下游配套**（不在本 skill 范围）：
- 品牌定位声明 → `positioning-statement` / `april-dunford-perspective`
- 品牌屋 / 品牌金字塔 / 品牌原型选择 → 外部品牌战略方法
- 品牌故事 / 视觉识别 / 传播策略 → 外部创意方法

### 不要本 skill 处理的情形

- 单次用户访谈复盘 → `meeting-note` / `steve-portigal-perspective`
- 单次需求卡片识别 → `requirement-card` / `pm-zettel`
- 临时灵感落盘 → `fleeting-note`
- 数据分析与可视化 → 外部数据 skill
- 急救型产品决策（48 小时内要拍板）→ 跑不动六阶段，用 `marty-cagan-perspective` 四风险快评

---

## 与其他 skill 的分流

| 当用户问... | 本 skill 适用？ | 应让位的 skill |
|---|---|---|
| 「这个功能该不该做」 | 否 | `marty-cagan-perspective`（四风险） |
| 「客户为什么从竞品切到我们」 | 否（除非要系统化做 Tool 4+7+9） | `bob-moesta-perspective` |
| 「把需求做成可量化 outcome」 | 否 | `tony-ulwick-perspective`（ODI） |
| 「为什么 X 产品卖不动」 | 否 | `dichter-perspective`（动机研究） |
| 「我们的定位是什么 / 销售 pitch 怎么写」 | 否 | `april-dunford-perspective` |
| 「Job Story 怎么写」 | 否 | `alan-klement-perspective` |
| 「访谈提纲怎么追问」 | 否（除非要全套 20 类） | `steve-portigal-perspective` |
| 「这个家庭产品的责任分布怎么看」 | 否 | `eve-rodsky-perspective` / `elinor-ochs-celf-perspective` |
| **「给一个新产品做完整用户研究」** | **是** | — |
| **「从访谈/评论中提取创新概念」** | **是**（Tool 3） | — |
| **「设计访谈 + 问卷做量化验证」** | **是**（Tool 9 + 10） | — |
| **「产品定位前先做用户洞察」** | **是** | 完成后让位 dunford/dichter |

---

## 验收硬约束（每个工具产出收尾必做）

**⚠️ 这不是给人看的 checklist——这是 agent 必须在产出文件里 echo 的硬约束。**

每个工具产出的 `.md` 文件**末尾必须 append**一个 `## 自检` block，逐条 echo 下列 7 条，**每条必须带证据**（行号、文件内某段引用、或具体片段）。没有 `## 自检` block 或证据不带 = 本工具产出不合格，不得进入下一阶段。

### 自检 block 模板（每个产出文件末尾必填）

```markdown
## 自检（agent 必填，每条带证据）

- [ ] **命名归位**：文件名 `toolXX_<name>_<product>.md` —— 证据：本文件名为 `___`
- [ ] **YAML 完整**：date / type / tool / product / language 五字段齐全 —— 证据：第 1-N 行
- [ ] **跨工具引用锁版本**：上游引用都用 `[[...]]` + 日期 —— 证据：第 X 行引用了 `[[...]]`，未引用上游则写「本工具无上游」
- [ ] **格式硬约定**：本工具的硬格式条目（如 Likert 原文 / 第一人称 / feel-avoid 行首 / When-I-hope-so-that 完整因果链）—— 证据：随机抽样 2 条产出条目对应原文位置
- [ ] **语言符合约定**：默认 Chinese（Tool 9 / Tool 1 例外详见各 tool 条目）—— 证据：整篇语言判定
- [ ] **不越边界**：未把品牌战略 / 切换访谈 / outcome metric / sales pitch 当本套件输出 —— 证据：写一句「本产出仅为用户研究 / 洞察素材，没有 X」
- [ ] **v1 深化声明（v2.1 升级）**：v1 深化默认推荐开启。本工具应启用以下 v1 深化项：[按上节「推荐扩展」表填本 Tool 对应推荐项]。已启用的项在产出中可指证（行号 / 章节）；如未启用某项，必须在产出顶部「v1 深化声明」段解释 why not（可接受理由：项目类型不匹配 / 早期探索阶段 / 单群单场景 等关闭场景；不可接受理由：忘了 / 嫌麻烦 / 1218 没说要做）
```

agent 验收逻辑：
- 产出文件末尾**没有** `## 自检` block → 工具未完成，重做。
- `## 自检` block 有但**证据栏空**（只打 ✅ 不带行号 / 引用 / 片段）→ 工具未完成，重做。
- 自检 7 条任一为 ❌ → 修产出文件直到该条满足。
- 全 ✅ 且证据完整 → 进入下一工具。

---

## 版本

<!-- v2.1 UPGRADE: 经 515 product Family AI dogfood 暴露「v4 是 example 但 SKILL 硬约定不跟 v4 走」张力，v1 深化升级为推荐默认开启。 -->

- **v2.1 — 2026-05-27**：经 515 product Family AI dogfood 暴露「v4 是 example 但 SKILL 硬约定不跟 v4 走」张力（v5 产出质量 > v4，但 v4 工程化深化在落地颗粒度上仍有优势），升级 v1 工程化深化从「可选」到「**推荐默认开启**」。改动 5 处：① frontmatter description 加推荐叠加 v1 深化一句；② 「与 v1 工程化扩展的关系」整段重写为「默认开启 + 关闭场景」7 类深化表；③ 输出规范末尾新增「推荐扩展」段，列每个 Tool 的推荐深化项；④ 自检 block 第 7 条改写为「v1 深化声明」，已启用项需指证、未启用项需解释 why not；⑤ 本版本记录。`references/v1_engineering_extensions.md` 同步从「可选 menu」改为「推荐默认 + 关闭场景」。SKILL.md 主体硬约定（1218 原稿）保留不变作为产出最小闸门。
- **v2.1.1 — 2026-07-06**：archive 兼容补丁。Tool 3/6/7 从访谈/评论/反馈抽需求前，先走 Job Statement 九格与六类 lint；避免从 raw voice 直接跳功能、创新概念或需求卡。
- **v2 — 2026-05-26**：推倒 v1 重构，回归 1218 原稿为方法论真源，工程化深化下沉到 `references/v1_engineering_extensions.md` 作为可选层。六阶段主线 + tool01 工序纠偏。
  - 同日经 karpathy-perspective subagent review 后修订 3 处：
    - 六阶段主线升格为「显式可执行序列」（防 LLM 编号偏置默认按 Tool 1→2→...→10 跑）
    - 「十个工具一览」改名为「工具库索引（按编号，非执行顺序）」
    - 验收 checklist 升格为硬约束：每个工具产出末尾必须 append `## 自检` block，逐条带证据 echo
    - Tool 1 加反 silent failure 注脚：把「广告语 / 品牌信息」与「品牌定稿」切开
- **v1 — 2025-12-18 至 2026-05-26**：已 archive 至 `.cursor/skills/research-research-suite-v1/`，仅作档案。
