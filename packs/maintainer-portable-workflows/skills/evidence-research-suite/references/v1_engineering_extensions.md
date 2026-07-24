---
name: v1_engineering_extensions
type: reference
status: recommended-default
parent_skill: evidence-research-suite
sourced_from: evidence-research-suite-v1 (archived) + research_v4_日历机 example
description: research 套件 v1 阶段沉淀的「工程化深化」机制——v2.1 升级为推荐默认开启层。SKILL.md 主体守 1218 原稿硬约定（最小闸门）；本文件是推荐质量基线（默认开启 + 关闭场景需声明）。
---

<!-- v2.1 UPGRADE: 整篇 framing 从「可选 menu」改为「推荐默认 + 关闭场景」。SKILL.md 升级后，本文件不再是「想做时怎么做」的可选指南，而是「默认要做、想关需说 why not」的推荐基线。 -->

# evidence-research-suite · v1 工程化扩展（v2.1：推荐默认开启）

> **这是什么**：evidence-research-suite v1 经过 4 轮迭代（v1→v2→v3→v4）沉淀的 7 类工程化机制。v2.1 升级为**推荐默认开启层**——每条扩展都是 4 轮迭代沉淀的工程化经验，默认开启除非有明确关闭场景。
> **两层硬度声明**：
> - **SKILL.md 硬约定（1218 原稿）= 产出最小闸门**（必做，不可协商）
> - **本文件（v1 深化）= 产出推荐质量基线**（默认开启 + 关闭需声明 why not）
> **谁用**：执行 research 套件的主综合方（小P 或 PM 本人），按每个 Tool 推荐深化项默认 append；关闭某项需在产出顶部「v1 深化声明」段写明 why not。
> **何时关闭**：每个扩展条目下「关闭场景」段列明可接受理由。不可接受理由：忘了 / 嫌麻烦 / 1218 没说要做。
> **关闭代价**：SKILL.md 主体 1218 原稿是最小闸门，能跑完一轮完整研究，但产出落地颗粒度会下降（参见 515 product Family AI dogfood：v5 内容质量 > v4，但 v4 工程化深化在落地颗粒度上仍有优势——这是本次升级的触发原因）。

---

## 使用约定（v2.1 强制）

**默认行为**：每个 Tool 按 SKILL.md「推荐扩展」表 append 对应深化段落。

**v1 深化声明段（每个工具产出顶部必填，frontmatter 下方第一段）**：

> **v1 深化声明**：已启用 [扩展条目名 1] / [扩展条目名 2] / ...；未启用 [扩展条目名 X]（why not：[关闭场景理由]）。

- 全部按推荐项 append → 声明列「已启用：A/B/C/...」。
- 关闭某项 → 必须写 why not，对照本文件每条扩展的「关闭场景」段是否匹配。
- 关闭项不写 why not = 自检 block 第 7 条 ❌ = 本工具产出不合格。

本扩展是 **推荐质量基线**（不是 menu）：默认全开按推荐项执行；关闭需理由可辩护。

---

## 位置约束（v3 patch · 2026-05-27 Eight Sleep dogfood 触发）

**问题**：v2.1 升 v1 深化为推荐默认开启后，2026-05-27 Eight Sleep A/B dogfood 实测发现：v1 深化（B/F/H 角色变体 / Bull's Eye / Christensen / coverage matrix / evidence ledger）在 **marketing-facing 段落** append 时**冲淡 PM 决策可读性**——两 verifier 双盲一致在 D8 实测维度反输给 pre-v1 极简版 0.5-1 加权分。

**判定**：v1 深化整体方向对（B 在 D1-D6 系统胜 +115.5 加权），但要按段落位置精准 append，不能 carpet-bomb 所有段落。这是 k 神 bitter lesson 在 research 上的局部成立——**clever rule 在错位置 append 会反向**。

**禁 append 段落清单（hard 约束 · 所有 Tool 都适用）**：

| Tool | 段落 | 只允许的附加内容 |
|---|---|---|
| Tool 1 | §三 soul statement / §四 slogan / §五 brand voice / hero motivator | 原句 + 1 行情感锚 + 1 行 trace 回上游 Q-ID |
| Tool 3 | cross-lens synthesis insight 收尾段（I1-I5 类） | 原句 + 1 行 trace 回 lens X / 上游 Q-ID |
| Tool 3b | hero concept / 单句 marketing line / pivot statement | 原句 + 1 行情感锚 + 1 行 trace 回 Tool 1 灵魂 / Tool 3 综合洞察 |
| 任一 tool | 跨工具 wikilink 引用「为什么相关」一句话 | 原句即可，不附 LB 表 / coverage matrix |

**v1 深化的正确 append 位置（仍按推荐默认）**：

- 承重假设清单（§1） → 独立 §章节，**不包围** marketing 段
- Bull's Eye 渗透路径（§4） → 独立 §章节
- B/F/H 角色变体（§4） → 独立子文档（命名约定 `tool0XF_*_BullsEye_*.md`）
- Christensen 三类拆分 → 独立 §章节
- coverage matrix → 独立 §章节
- evidence ledger（§5） → 独立 §章节
- 下游信号台账（§7） → 独立子文档（`上市与营销信号台账_{product}.md`）

**判定测试**：拿掉这个段落周围的 v1 深化 append，读者能否 1 breath 读完该段落核心句、立刻知道 PM 该怎么用？答否 = v1 深化在错位置 append，移到独立 §章节。

**触发证据**（2026-05-27 Eight Sleep dogfood full_test）：

- **A/B 实测**：v3 vs pre-v1 极简骨架（`~/.agents/skills/evidence-research-suite/`），双 verifier 双盲，平均总分 v3 = **85.95** / pre-v1 = **75.7**，**Δ +10.25 中等胜出**（未达 ≥15 显著档）
- **D8 反输 0.5-1 加权分** → v1 深化（Bull's Eye / B-F-H / Christensen / coverage matrix）在 marketing-facing 段落周围 append 冲淡 PM 决策可读性。这是 patch 出处。
- **D1-D6 系统性领先 +115.5 加权**（triple verify 100% pass、跨工具日期锁 40 处、Verifiable Acceptance Criteria 全落地、边界 0 v5/v4 痕迹泄漏）—— 证明 v1 深化在结构维度是真护城河，问题只在位置错配
- **dogfood 报告**：`代号515/01_research/research_skill_ab_test/eight_sleep/_verify/verdict.md` §三-§五
- **两 verifier 双盲评分**：`_verify/verifier1_scores.md` (X=A Y=B, Δ +7.5) + `_verify/verifier2_scores.md` (X=B Y=A 位置翻转, Δ +13.0)，分歧 5.5 < 10 不需 tiebreaker
- **skill-creator 二次评估**：`_verify/skill_creator_eval.md`（独立 rubric 跑出 verdict good→excellent after 6 patch，6 项自检 + 6 改进 patch · verify-the-verifier 实证）
- **Patch ID**: V3-P0-01（本段）+ SC-P0-1 / P0-2 / P1-1 / P1-2 / P2-1 / P2-2（skill-creator eval 后续 patch · 已落地详见 SKILL.md 版本史）

---

## 1. 承重假设清单（Load-Bearing Assumptions Ledger）

**是什么**：在工具产出文档里单列一张表，把那些「一旦失效、下游某条具体产品动作就作废」的假设挑出来，挂上失效后果和验证交接目标。普通假设挂普通 `[假设]` 标签即可，不进本表。

**加在哪个 Tool 后**：Tool 1 / Tool 6 / Tool 7 / Tool 3b 默认 append；Tool 3 / Tool 8 在 Synthesis 收尾按需 append。

**默认行为**：开启（任一工具综合方在 Synthesis 收尾时判断本轮是否产生了承重假设，有则 append）。
**关闭场景**：超小型项目（< 5 个 functional job），即整轮研究承重假设少于 2 条；此时合并写入主结论即可，不另起表。其他场景一律默认开启。

**不加会失什么**：假设散落在 11 个 tool 文档的各角落，下次研究时没人记得哪条是承重、哪条是普通；当某条假设被推翻，无法快速回溯到「整段定位 / 这条抓手 / 那条 PRD 条款」该跟着作废。

**判定测试**：拿掉这条假设，下游某个具体动作还成不成立？不成立 = 承重，进表。

**格式 / 模板示例**：

```markdown
## 承重假设清单（Load-Bearing Assumptions）

| ID     | 假设            | 证据等级 | 失效后果（人话）                                  | 建议验证方式（Tool 9/10 交接）          |
|--------|-----------------|----------|---------------------------------------------------|----------------------------------------|
| T7-LB-1 | 用户愿为多孩冲突路由付溢价 | H        | 若错 → premium 定价策略作废 + Tool 1 §3 整段重写  | Tool 10 PSM + Tool 9 价格切换题第 3 组 |
| T6-LB-2 | 移民家庭对"被监督"的焦虑 < 对"被遗忘"的焦虑 | B    | 若错 → Tool 6 反向需求 R-3 抓手反向 + 营销主语反转 | Tool 9 移民家庭专访第 8 题反向探查      |
```

- ID 用 `T{N}-LB-{n}` 前缀，证据等级四档 A/B/C/H（A=一手访谈实证 / B=二手数据 / C=方法论推断 / H=HYPOTHESIS）。
- 失效后果**必须写人话三段**：「若 X 被推翻 → Y 抓手作废 + Z 营销/路线图后果」，不写「Tool 6 §2 整段重写」这种黑话。
- 验证方式必须能直接喂给 Tool 9 访谈题 / Tool 10 问卷题，不写「之后再验证」。

**与 SKILL.md 的关系**：若使用本扩展，产出顶部必须声明「本产出含 v1 深化，非 1218 硬约定」。

---

## 2. 正向 demand vs 反向 anxiety 类需求拆分

**是什么**：Tool 6 把情感/社交需求拆成两类——**正向 demand**（用户想要 X，产品越使劲帮、用户越满意）和**反向 / anxiety 类**（用户怕 X，产品越使劲帮、用户反而更紧张）。两类不共用模板，反向类另起结构。

**加在哪个 Tool 后**：Tool 6（情感与社交需求）默认 append；Tool 7 顺带承接反向类的「化解动作」翻译成功能边界。

**默认行为**：开启（家庭 / 育儿 / 健康 / 老人照护 / 金融 / 隐私敏感 / 含 AI 自动化的产品几乎必有 anxiety 维度）。
**关闭场景**：纯 efficiency 工具产品（如开发者工具、纯生产力工具、B2B SaaS dashboard），用户对产品的诉求是「帮我做更多更快」而非「别让我显得不好」，无结构性焦虑维度；此时 Tool 6 按 1218 原稿出一张情感需求表即可。

**不加会失什么**：把反向需求当成正向需求来满足，产品越打磨用户越疏远；营销越使劲喊优势，触发用户的怕。最典型失败：「全自动家庭管理 AI」喊得越响，妈妈越怕「我是不是显得不像个好妈妈」。

**判定测试**：一条需求如果「使劲优化」会让用户更不安、不是更满意，它属于反向类，必须另起结构。

**格式 / 模板示例**：

```markdown
### 反向 / Anxiety 类需求（独立结构，不与正向需求混表）

**R-3 怕"被显得不像个好妈妈"**
- 怕什么：AI 把家庭管理打理得太完美，让她在亲友面前显得"是 AI 在带孩子不是她在带"
- 什么会让这个怕更重：产品把成就归功于 AI（"今天 product 帮您完成了 8 件事"）/ 跨家庭对比仪表盘 / 任何让外部观察者看到 AI 介入痕迹的功能
- 怎么化解：成就归功永远写"妈妈完成了"；外显的 UI 隐藏 AI 痕迹；分享卡片只显示她的视角；可关闭"显得用 AI"的所有显性标签
```

正向需求继续用「方向 + 抓手 + 边界」三段（见扩展 3）。

**与 SKILL.md 的关系**：若使用本扩展，产出顶部必须声明「本产出含 v1 深化，非 1218 硬约定」。

---

## 3. 三段需求结构（方向 + 抓手 + 边界）

**是什么**：Tool 7（功能需求）每条需求写成三段——**方向**（用户从什么处境走向什么处境）+ **抓手**（关键一招）+ **边界**（别偏成什么）。正向起头，三段都要有；只有「边界」=半张地图，不算合格条目。

**加在哪个 Tool 后**：Tool 7（功能需求）默认 append；Tool 6 正向需求段也可用同一三段。

**默认行为**：开启（需求要喂给 PRD / 工程 / roadmap 的场景几乎必需，避免单点功能清单解读）。
**关闭场景**：早期 problem space 探索阶段（pivot 阶段），产品方向尚未收敛、需求还在 churn，强行三段会过早锁死；此时 Tool 7 按 1218 原稿出「When I... I hope... so that...」即可，待方向收敛后再补三段。

**不加会失什么**：需求被读成「加个 X 功能」，PM/工程拿到只看抓手不看方向，做完发现偏了；边界缺失导致后续 scope creep；多分群下抓手通用化、丢掉差异。

**格式 / 模板示例**：

```markdown
**FA1（多子女活动冲突检测与路由）**
- 方向：从「脑子里同时算三条接送路线、随时漏一个」走向「冲突一发生就有 2-3 个可行方案摆在面前」
- 抓手：自动检测时间重叠 + 基于家长数/地理位置/活动优先级生成路由方案
- 边界：不要偏成「自动决定哪个孩子去哪」——决定权留给妈妈，AI 只摆方案
```

**与 SKILL.md 的关系**：若使用本扩展，产出顶部必须声明「本产出含 v1 深化，非 1218 硬约定」。

---

## 4. Bull's Eye 渗透路径 + 角色变体（Angel / Bull's Eye / Delegate）

**是什么**：Tool 4 输出除了 4 象限分群，再加一条 Bull's Eye 渗透路径——**angel → bull's eye → core → strategic → radiation → symbiotic**——给 GTM 排进入序列。每个核心角色（Angel / Bull's Eye / Delegate 等）还可单独生成 Tool 6/7 的「角色变体卷」，不重复主稿 40 条需求、只标注优先级偏移和该角色独有需求。

**加在哪个 Tool 后**：Tool 4（人群分群）默认 append Bull's Eye 渗透路径；Tool 6 / Tool 7 / Tool 3b 在 Tool 4 出现 ≥2 个高优先群时默认 append B/F/H 角色变体卷（命名约定：`tool07F_functional_needs_BullsEye_{product}.md` 等）。

**默认行为**：
- Bull's Eye 渗透路径：Tool 4 默认开启（dogfood v5 已开），分群完成后顺手排进入序列。
- B/F/H 角色变体卷：默认开启**条件触发**——Tool 4 输出 ≥2 个高优先群时，Tool 6 / Tool 7 / Tool 3b 必须生成角色变体子文档；Tool 4 只有单群（或所有群优先级一致无差异）时不触发。

**关闭场景**：
- Bull's Eye 渗透路径：单一目标用户场景（产品定位极窄、用户分群已收敛到 1 群），4 象限分群本身没有渗透路径可排。
- B/F/H 角色变体：单群产品；或所有角色优先级一致无差异（罕见，需举证）。

**不加会失什么**：4 象限分群只告诉你「有哪些群」，不告诉你「先打谁」；GTM 阶段还得自己想次序。多角色产品里所有角色共用一套需求清单，导致「妈妈和奶奶 P0 一样」的失真结论。

**格式 / 模板示例**：

```markdown
## Bull's Eye 渗透路径

Angel（A 超载调度员）→ Bull's Eye（F 课外活动调度员）→ Core（B 双职工夫妻）
→ Strategic（H 远程子女照看老人）→ Radiation（C 单亲）→ Symbiotic（生态伙伴：教练/学校）

- Angel：付费意愿最高、给最早期反馈、容忍 bug
- Bull's Eye：痛点具体可传播 + 社群天然 → GTM 的子弹
- Core：规模最大、决定商业化曲线
- Strategic：长期叙事/护城河
- Radiation：靠 Core/Bull's Eye 口碑自然带
- Symbiotic：渠道/嵌入合作
```

角色变体卷的结构见 `examples/research_v4_日历机/tool07F_functional_needs_BullsEye_productFamilyAIHub_v4.md`：① A 需求在该角色视角下的优先级偏移表 ② 该角色独有需求（不在 A 表里） ③ 该角色的优先级矩阵。

**与 SKILL.md 的关系**：若使用本扩展，产出顶部必须声明「本产出含 v1 深化，非 1218 硬约定」。

---

## 5. 跨工具证据台账（Evidence Map）

**是什么**：在 11 个 tool 产出之外另起一份 `{product}_evidence_map.md`，把主结论 → 证据类型 → 源文件钉死。三段结构：① 显式裁决表（Bull's Eye 选谁、核心用户选谁、依据） ② 主结论 → 证据 → 源文件矩阵 ③ 版本合并说明（不同版本研究怎么吸收/合并）。

**加在哪个 Tool 后**：Tool 3 起锚 evidence map（默认 append 一个锚点段，列本工具产出的关键结论 → 证据指针）；Tool 8 收尾闭合（默认合并所有工具的 evidence map 节点为完整 `{product}_evidence_map.md`）。Phase 7 audit 前也可单独生成给 audit panel 用。

**默认行为**：开启（Tool 3 起锚 + Tool 8 收尾闭合是标配；跨工具结论可追溯是套件交付质量的基线）。
**关闭场景**：单轮研究无版本迭代需求（一次性产出、不需要跨版本合并、不对外汇报、不留半年后回查）；此时各 tool 自带的引用即够，不必另起 evidence map。

**不加会失什么**：结论散落在 11 个 tool 里、引用关系靠记忆；版本合并时反复回查；audit panel 跑得慢、容易漏证据缺口；半年后回看自己也不记得当时凭什么。

**格式 / 模板示例**：

```markdown
## 显式裁决表
| 决策 | 结论 | 判断标准（可辩护） | 主要证据 |
|------|------|-------------------|----------|
| Bull's Eye 靶心 | F 课外活动调度员 | 痛苦具体 × 社群天然 × 口碑场景天然 | Amazon 多孩评论 / v3 Tool4 收敛 |

## 主结论 → 证据 → 源文件
| 主结论 | 证据类型 | 源文件 / 数据 |
|--------|----------|----------------|
| 品类雇用「掌控感」多于「日历功能」 | 量化 + 情感 Job 频次 | JTBD_JobList / JTBD_EmotionalSocial |
```

完整范例见 `examples/research_v4_日历机/V4_evidence_map.md`。

**与 SKILL.md 的关系**：若使用本扩展，产出顶部必须声明「本产出含 v1 深化，非 1218 硬约定」。

---

## 6. 工具间握手协议（Tool Handoffs）

**是什么**：阶段交界处，前一个工具必须显式打包一份「交接清单」给下一个工具，不让下游凭主稿自己拆。三条关键握手：

- **Tool 4 → Tool 7**：必须传两类——① 情境群（按场景切分的用户群）② 横切维度（跨情境群的人群类别，例：DIY 自建派 / 礼物购买者 / 移民家庭 / 特殊家庭结构）。只传情境群 = 漏掉整组横切人群。
- **Tool 6 / 7 → Tool 1 / Tool 3b**：传「承重假设清单 + Bull's Eye 渗透路径」，避免 Tool 1（产品灵魂）凭空起、Tool 3b（创新概念）抓不到承重假设的方向。
- **Tool 3 → Tool 1 / Tool 3b**：传「矛盾对编号 + 综合洞察」，把 Tool 3 四镜分析的矛盾结构显式喂给灵魂层和创新层。

**加在哪个 Tool 后**：阶段交界（Tool 4→Tool 7、Tool 7→Tool 1、Tool 3→Tool 3b 等）。

**默认行为**：开启于完整六阶段流水线 + 多 subagent 协作场景；单工具触发或单 agent 串行执行可省略。
**关闭场景**：单工具触发（场景 2 品牌重塑、场景 3 产品迭代等只跑 1-2 个 tool 的局部任务）；或全程单 agent 串行执行无 subagent 协作（主综合方本人记忆即够）。

**不加会失什么**：下游 subagent 凭自己读上游主稿来推依赖、易漏（尤其横切维度类容易整组掉）；阶段衔接靠主综合方记忆而非显式协议；多人协作时同一阶段交界给出不同握手内容。

**格式 / 模板示例**：

```markdown
## Tool 4 → Tool 7 交接清单（Handoff）

### 情境群（Situational Groups）
- A 超载调度员、B 双职工夫妻、C 单亲、F 课外活动调度员、H 远程照看老人 ...

### 横切维度（Orthogonal Dimensions · 本次产生）
- DIY 自建派（跨 A/B/C 群体）
- 礼物购买者（跨 H/F 群体）
- 移民家庭（跨所有群体，文化承重维度）
- 特殊家庭结构（单亲 / 重组 / 多代同堂）

### 接收方义务
Tool 7 收到本清单时若发现只有情境群、没有横切维度声明，应回查 Tool 4 输出确认。
```

**与 SKILL.md 的关系**：若使用本扩展，产出顶部必须声明「本产出含 v1 深化，非 1218 硬约定」。

---

## 7. 下游信号台账（Downstream Signal Ledger）

**是什么**：每个工具产出尾部 append 一张 "Downstream Signal" 表，记录那些「研究自己用不上、但下游 GTM / 文案 / sales / 渠道需要」的信号。最关键的两类标签：**[Big Hire / 大雇佣]**（正向卖点要喊得响）vs **[Anxiety-blocker / 焦虑阻断器]**（要悄悄化解）——这两类需要**相反的营销处理**。

**加在哪个 Tool 后**：Tool 4（起锚）/ Tool 6 / Tool 7 收尾默认 append；Tool 8 阶段做最终「卖点 / 定位综合」合并。运行中的台账文件命名：`上市与营销信号台账_{product}.md`。

**默认行为**：开启（B2C / 家庭 / 健康 / 隐私敏感产品几乎必需；研究产出会喂下游 GTM / 文案 / 渠道是默认假设）。
**关闭场景**：研究产出不喂 GTM / 文案 / 渠道（纯内部 PM 用研、纯学术研究、纯探索性洞察、上线遥远期产品的早期 problem space 调研）；此时卖点信号尚不需要单独台账。

**不加会失什么**：卖点/定位信号散落在 11 个 tool 里，做营销时回查成本高；最致命的是 Big Hire 和 Anxiety-blocker 不分，营销把要"悄悄化解"的拿来"大声喊"，触发用户反向焦虑。

**格式 / 模板示例**：

```markdown
## Downstream Signal Ledger 段（Tool 6 append）

| 信号 | 类型 | 用途 | 下游处理建议 |
|------|------|------|--------------|
| "周二下午两个孩子同时有活动？product 3 秒给方案" | [Big Hire / 大雇佣] | 首屏文案 / demo 开场 | 大声喊、做成 hero 场景 |
| "不会让外人看出是 AI 在带孩子" | [Anxiety-blocker / 焦虑阻断器] | 隐性功能 / 默认设置 | 不写进首屏；在 onboarding / 隐私页悄悄露出 |
| 接送高峰（周二/周四 17:00-19:00） | [Channel-timing] | 媒体投放时段 | media-buying 时段表 |
```

完整 Phase 3 close 的「卖点 / 定位综合」（ledger + Tool 6 ad-creative + Tool 1 soul/slogans 三方综合）也写在台账末段，是 research 套件交付给下游 GTM 的最后一站。

**与 SKILL.md 的关系**：若使用本扩展，产出顶部必须声明「本产出含 v1 深化，非 1218 硬约定」。

---

## 扩展条目场景速查表（v2.1：判断何时关闭）

| 你的场景 | 默认开启项 | 可关闭项 |
|---------|---------|---------|
| 标配场景（复杂产品 / 多分群 / B2C / 含 AI） | 全部 7 类 | — |
| 简单产品 / 超小型项目（< 5 个 functional job） | 6 类 | 1 (承重假设) |
| 纯 efficiency 工具产品（无 anxiety 维度） | 6 类 | 2 (正反两类) |
| 早期 problem space 探索（pivot 阶段） | 6 类 | 3 (三段需求) |
| 单一目标用户场景 / 单群产品 | 5 类 | 4 (Bull's Eye + 角色变体) |
| 单轮研究无版本迭代需求 | 6 类 | 5 (证据台账) |
| 单工具触发 / 全程单 agent | 6 类 | 6 (握手协议) |
| 研究不喂 GTM / 文案 / 渠道 | 6 类 | 7 (下游信号) |
| 一次性洞察任务（多个关闭条件同时满足） | 按上述列出的可关闭项叠加 | 多项 |
| 全套深化（v4 范式 / 515 product v5 范式） | 全部 7 类 | — |
| **任一场景（v3 patch · 硬约束）** | 其他扩展按场景表 | **Marketing-facing 段落周围禁 append**（v1 深化全部移到独立 §章节，详见上节「位置约束」） |

**核心原则**：默认全部开启（v2.1 升级）；关闭任一项需要匹配上面具体「关闭场景」之一，并在产出顶部「v1 深化声明」段写明 why not。不可接受理由：忘了 / 嫌麻烦 / 1218 没说要做。

**v3 patch 新增硬约束**：marketing-facing 段落（hero / soul / synthesis insight / slogan / pivot statement）周围一律禁 append v1 深化——这条不是「关闭场景」可选项，是硬约束（位置约束），所有场景都适用。详见本文件「位置约束（v3 patch）」段。

---

<!-- v2.1 UPGRADE: 末尾边界声明从「menu / 两者互不替代」改为「最小闸门 + 推荐基线 + 关闭场景需 why not」三层关系。 -->

## 与 evidence-research-suite SKILL.md 的关系（v2.1）

**层级关系**（三层）：
1. **SKILL.md 主体（1218 硬约定）= 产出最小闸门**——守 2025-12-18 研究者原稿的硬性流程，10 个工具 / 六阶段 / 不变形不加塞。不可协商。
2. **本文件（v1 深化）= 产出推荐质量基线**（v2.1 默认开启）——基于 v1→v4 真实迭代经验，每条扩展默认 append，关闭需声明 why not。
3. **关闭场景声明 = 可辩护理由**——每个 Tool 产出顶部「v1 深化声明」段必填，列已启用 + 已关闭项（含 why not 对照本文件关闭场景）。

**v2 vs v2.1 framing 变化**：
- v2：本文件是 menu，「主体没说要做 → 默认不做；本扩展提供想做时怎么做」。
- v2.1：本文件是推荐质量基线，「默认要做 → 想关需说 why not」。SKILL.md 主体仍守 1218 硬约定，但 v1 深化不再是「可选加分项」而是「推荐基线」。

**冲突时**：主体硬约定优先；任何扩展条目与 1218 原稿硬约定冲突，扩展让位（不会发生，本扩展全是 append 不是覆写）。

**声明义务**：每个工具产出顶部必填「v1 深化声明」段，已启用项可指证（行号/章节），已关闭项必须写 why not。声明缺失 = 自检 block 第 7 条 ❌ = 本工具产出不合格。

---

*v1 工程化扩展 · v2.1 推荐默认开启层 · 与 SKILL.md 主体 1218 硬约定形成两层硬度*
