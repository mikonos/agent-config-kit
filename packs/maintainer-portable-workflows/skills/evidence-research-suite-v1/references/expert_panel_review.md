# Phase 7.5 · 外部专家 panel 二审协议

> Phase 7 的 Cagan + Moesta 自审计是产品风险 + 证据接地审查，覆盖**产品级**失败模式。
> 但方法论流派内的术语合规（Dichter 4 维骨架是否齐 / ODI 句法是否被压成人话 / Christensen 三类结构是否落到表 / core interaction 是否逐项回接 / Indi 三层心智是否压缩成情绪标签）只能由**该 tool 的专家本人 panel**抓出来。
> 这是 v5.10 新增的卡点，把"专家 panel 二审"从手动惯例固化为协议。
> 实践证据：2026-05-21 research 家庭Agent美国市场 dogfood 在 Phase 7 通过 PASS_WITH_FIXES 后，外部 codex 起的 expert panel 二审（review2_*）仍判出 4 BLOCKED + 2 PASS_WITH_FIXES——证明 Phase 7 自审计接不住流派合规层。

---

## 1. 触发条件

**hard required**（必跑，不许跳）：

- tool 进入 `synthesized` 或 `final`，且被任一**下游 tool 引用** / 被**营销台账 append** / 被 **Phase 3 close** 综合使用之前
- tool 出现「非共识裁决」（D3）——主综合方与某个 persona subagent 结论分歧
- tool 涉及术语 cascade（v1.x 锚点替换、戏剧角色改名、文化代码改字）

**strongly recommended**（建议跑，省略需说明理由）：

- tool 第一次 synthesized，主综合方对自己的产出不完全确定
- 跨流派合流的工具（Tool 3 / 6 / 8——多个流派 lexicon 同时入主稿）

**可跳过**：

- 纯 typo / 格式修复
- 仅追加新内容（无新承重假设、无新非共识裁决、无术语 cascade）

---

## 2. Panel 构成规则

每个 tool 的 panel 必须由 **该 tool 在 SKILL.md 中声明的所有 persona + 1 个跨流派挑战者**组成：

| Tool | 必入 panel | 跨流派挑战者建议 |
|---|---|---|
| Tool 1 Product Soul | Dichter + Rapaille + Jobs | （可选）Kahy Sierra（badass test）或 Klement（Big Hire 检验） |
| Tool 3 Four-Lens | Teresa Torres + Christensen + Indi Young | （可选）Bob Moesta（switching evidence 检验） |
| Tool 4 Target Users | Moesta + Christensen | （可选）Indi Young（thinking styles vs persona 检验） |
| Tool 6 Emotional & Social | Klement + Ulwick + Rodsky + Schulte + Vanderkam | （可选）Sierra（cognitive resource 检验） |
| Tool 7 Functional Needs | Ulwick + Moesta | （可选）Patton（薄切片 vs feature wishlist 检验）|
| Tool 8 Ecosystem | Choudary + Spohrer + Dunford | （可选）Cagan（feasibility/viability 风险） |
| Tool 3b Innovation | Buxton + Sierra + Jobs | （可选）Cagan（value risk） |

**约束**：

- panel 全部走 readonly subagent，不许 in-character
- 🟢 grounded persona 必须激活对应 `*-perspective` skill；🟡 simulated 必须能自陈 ≥2 代表作 / 核心概念才允许出 verdict
- panel **不能由主综合方自审**——main agent 此时是被审对象，不参 panel

---

## 3. Panel 输出格式（每个 panelist 必须遵循）

```markdown
# {Tool 编号} {Tool 名称} 二审 - {persona 名}

对象：`{tool 主稿路径}`
依据：`research-research-suite` {tool 编号}、D2、D5、D6、Rule {相关 Rule 列}。

## VERDICT

**{PASS / PASS_WITH_FIXES / BLOCKED}。**

{2-3 句裁决理由——具体指向 tool 的什么内容支持了这个结论}

## 关键问题

1. **{问题标题——一行概括}**
   - Evidence：{主稿哪一行哪一节 + skill 哪条 Rule 哪段 D，引用具体行号}
   - skill 影响：{这个问题违反了 skill 哪条硬约束 / 让 tool 输出偏离了什么目标}
   - 最小修复：{≤2 句话能 actionable 的修复指令——主综合方读完知道动哪里}

2. ...

## 修复顺序

{1-5 步排序修复，依赖在前的先做}
```

**强制要求**：

- VERDICT 三档不接受第四种（"基本通过"/"小问题"/"待定" 不允许）
- 每条问题三段缺一不可（Evidence / skill 影响 / 最小修复）
- 引用行号必须真实存在（panelist 自己 grep 验证）
- "最小修复"必须 actionable——不许写「需进一步研究」「值得再思考」

---

## 4. 合议规则（main agent 收 panel 后怎么处置）

main agent 收到全部 panelist 的 verdict 后，按以下合议规则裁决整体 VERDICT：

- **primary panelist BLOCKED → 整体 BLOCKED**（例：Tool 3 Torres 是 primary，她 BLOCKED 决定整体 BLOCKED；Christensen 和 Indi PASS_WITH_FIXES 不能拉回）
- **任一 panelist BLOCKED + tool 进入跨 tool cascade 角色 → 整体 BLOCKED**（即使 primary 没 BLOCKED）
- **所有 panelist PASS_WITH_FIXES → 整体 PASS_WITH_FIXES**，所有 P0 问题进 tool 修复 queue
- **所有 panelist PASS → 整体 PASS**

**整体 BLOCKED 处置**：

1. tool YAML status 强制降回 `synthesized`，不许标 final
2. 修复完成前**不允许下游 tool 引用**、**不允许 append 营销台账**、**不允许 Phase 3 close 综合使用**
3. 修复后必须**重跑相关 panelist**——不许只 main agent 自评

**整体 PASS_WITH_FIXES 处置**：

1. tool 可升 final，但 changelog 必须记录二审 P0 列表
2. P0 问题进 tool 修复 queue，必须在下游使用前 close
3. P1/P2 进 open loop 或 follow-up

---

## 5. 输出文件命名与归位

panel 产物按下面规范命名：

```
{tool 主稿同目录}/review{N}_tool{NN}_{tool_name}_expert_panel.md
{tool 主稿同目录}/_subagent_views/review{N}_tool{NN}_{persona}_view.md
```

`N` 是审计轮次（第一次 panel = review1，主综合方修复后再审 = review2，依此类推）。

main agent 合议产物（整体 VERDICT + 修复 queue）合并写入 `review{N}_tool{NN}_{tool_name}_expert_panel.md` 顶部段。

---

## 6. 与 Phase 7 quality_audit 的协作

- Phase 7 跑 Cagan + Moesta 2-panel，覆盖产品级失败模式（4 大风险 + 证据接地）
- Phase 7.5 跑 tool-specific panel，覆盖方法论流派合规
- **两者不替代**：dogfood 实证显示 Phase 7 PASS_WITH_FIXES 后 Phase 7.5 仍能判 BLOCKED
- 时序：Phase 7 在所有 tool 全部 synthesized 后跑一次；Phase 7.5 在每个 tool synthesized → final 升档前跑

---

## 7. 与 prd-audit skill 的接口

- research Phase 7.5 panel 报告输出后，作为 PRD pipeline 的 audit 输入之一
- 如果 research 产出物之后会变成 515 PRD 流水线的 insight / risk / decision，则 `prd-audit` skill 的 audit subagent 在跑 7 项 A-G 检查时，会把 research Phase 7.5 panel 的 BLOCKED 视为「研究源头未 close」——直接 BLOCKED PRD 的 audit
- 这是 research → PRD 中间的「研究→PRD 翻译」预审接口

---

## 8. 历史先例

2026-05-21 research 家庭Agent美国市场 dogfood：

- Phase 7（Cagan + Moesta）VERDICT = PASS_WITH_FIXES（11 P0 + 14 P1）
- 外部 codex 起 expert panel 二审（review2_tool01/03/04/06/07/08）：
  - Tool 3 / 4 / 6 / 7 = BLOCKED
  - Tool 1 / 8 = PASS_WITH_FIXES
- 暴露 skill 缺口：4 维动机骨架、四力、ODI 语法、core interaction 回接、Rule11 cascade 在 Phase 7 自审计抓不到——这些都是流派合规层
- 教训：v5.10 把 Phase 7.5 协议固化，避免后续 dogfood 同坑再踩

---

*真源在 `references/expert_panel_review.md`；SKILL.md Phase 7.5 段引用此文件。*
