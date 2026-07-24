---
date: <YYYY-MM-DD>
type: research / tool-output
tool: tool10-survey-design
product: <产品代号或名称>
language: zh-CN
status: draft
inputs:
  - <研究背景 + 样本人群特征与样本量>
  - <准备研发的产品>
  - <创新概念若干 — 可引 Tool 3 / Tool 3b>
---

# Tool 10 — 问卷设计 Questionnaire Design
> Product: <产品代号或名称>
> Stage: Stage 2 需求挖掘（与 Tool 6 / Tool 9 同阶段；可用于量化验证 Tool 3b 创新概念）
> Prompt source: `references/original_prompt_blocks.md#tool-10`
> Methodology anchor: `references/methodology_foundations.md` § 心理测量学五维（Knowledge / Evaluation / Behavior / Frequency / Psychology）

## 上下文输入（执行前必填）

- **研究背景**（含研究目标 + 样本人群特征）：<...>
- **样本人群特征 & 样本量**：<...>
- **问卷名称**：<...>
- **准备研发的产品**：<...>
- **创新概念 1-3 个**（可引 `[[tool03b_innovation_<product>_<date>]]`）：
  1. <...>
  2. <...>
  3. <...>
- **语言要求**：zh-CN

## 输出主体

### 通用量尺（按需在题目中选用其一）

```
Likert-5：1=非常不同意 / 2=不同意 / 3=中立 / 4=同意 / 5=非常同意
频率-5：1=从不 / 2=很少 / 3=有时 / 4=经常 / 5=总是
评价-5：1=很差 / 2=较差 / 3=一般 / 4=较好 / 5=很好
```

### 创新概念 1：<...>

#### Knowledge Questions（知识 / 单选）
1. <题干> — A/B/C/D <选项>
2. <题干> — A/B/C/D
3. <可选 3-5 题>

#### Evaluation Questions（评价 / Likert-5）
1. <题干> —（1-5）
2. <题干> —（1-5）
3. <可选 3-5 题>

#### Behavioral Questions（行为 / 单选）
1. <题干> — A/B/C/D
2. <题干> — A/B/C/D
3. <可选 3-5 题>

#### Frequency Questions（频率-5）
1. <题干> —（1-5）
2. <题干> —（1-5）
3. <可选 3-5 题>

#### Psychological Questions（心理 / Likert-5）
1. <题干> —（1-5）
2. <题干> —（1-5）
3. <可选 3-5 题>

### 创新概念 2：<...>

#### Knowledge / Evaluation / Behavioral / Frequency / Psychological（同上结构，每类 3-5 题）

### 创新概念 3：<...>

#### Knowledge / Evaluation / Behavioral / Frequency / Psychological（同上结构，每类 3-5 题）

### Standards 五项验收对照

| Standard | 本问卷如何满足 | 证据题号 |
|---|---|---|
| Factorial Structure（逻辑相关） | <...> | <...> |
| Content Validity（内容效度，全覆盖研究目标）| <...> | <...> |
| Discriminant Validity（区分效度，无重叠）| <...> | <...> |
| Predictive Validity（预测效度，可预测创新趋势）| <...> | <...> |
| Construct Validity（建构效度，每题直接对应目标）| <...> | <...> |

---

## 自检（agent 必填，每条带证据）

- [ ] **命名归位**：文件名 `tool10_survey_design_<product>.md` —— 证据：本文件名为 `___`
- [ ] **YAML 完整**：date / type / tool / product / language 五字段齐全 —— 证据：第 1-N 行
- [ ] **跨工具引用锁版本**：创新概念引用 Tool 3 / Tool 3b 用 `[[...]]` + 日期 —— 证据：第 X 行
- [ ] **格式硬约定**：**禁用开放式问题**（原文：Avoid open-ended questions）；**只用单选 + Likert**；五题型齐全（Knowledge / Evaluation / Behavioral / Frequency / Psychological）；五项 Standards（Factorial / Content / Discriminant / Predictive / Construct Validity）—— 证据：抽样 2 题验证封闭式 + Standards 对照表完整
- [ ] **语言符合约定**：默认 zh-CN —— 证据：整篇语言判定
- [ ] **不越边界**：**全部封闭式问题，没有夹带开放题 / 半开放题**；本产出是量化问卷，不是访谈题库（让位 Tool 9）、不是市场份额估算 —— 证据：一句话申明 + 全文搜索无 "请描述" / "请简述" / "为什么" 之类开放式提示
- [ ] **v1 扩展声明**：未用 v1 深化 / 用了 v1 深化（如承重假设量化映射、证据台账接驳）—— 证据：产出顶部声明位置
