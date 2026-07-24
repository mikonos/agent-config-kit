---
date: <YYYY-MM-DD>
type: research / tool-output
tool: tool02-jas
product: <产品代号或名称>
language: zh-CN
status: draft
inputs:
  - <产品定义来源>
---

# Tool 2 — 詹金斯行为调查 Jenkins Activity Survey
> Product: <产品代号或名称>
> Stage: Stage 1 用户识别（与 Tool 4 / Tool 7 同阶段，量化行为分群用）
> Prompt source: `references/original_prompt_blocks.md#tool-2`
> Methodology anchor: `references/methodology_foundations.md` § Jenkins Activity Survey（Type A Behavior Pattern 量表）

## 上下文输入（执行前必填）

- **产品名称**：<...>
- **产品核心特征**：<...>
- **想测的购买决策行为情境**：<...>
- **语言要求**：zh-CN

## 输出主体

### Likert 5 点量尺（必须原文使用，每题统一）

```
1 = Strongly Disagree（非常不同意）
2 = Disagree（不同意）
3 = Neutral / Unsure（中立 / 不确定）
4 = Agree（同意）
5 = Strongly Agree（非常同意）
```

### 一、SI 维度 — Speed and Impatience（速度与急躁）

> 测量：时间紧迫感 / 行动节奏 / 对等待、延迟、中断的容忍度

1. <题干> ——（1–5 Likert）
2. <题干> ——（1–5 Likert）
3. <题干> ——（1–5 Likert）
4. <题干> ——（1–5 Likert）
5. <题干> ——（1–5 Likert）
6. <可选 6-7 题>

### 二、JI 维度 — Job Involvement（工作投入）

> 测量：目标投入程度 / 成就导向 / 把任务置于生活中心的倾向

1. <题干> ——（1–5 Likert）
2. <题干> ——（1–5 Likert）
3. <题干> ——（1–5 Likert）
4. <题干> ——（1–5 Likert）
5. <题干> ——（1–5 Likert）
6. <可选 6-7 题>

### 三、HDC 维度 — Hard-Driving and Competitiveness（进取与竞争）

> 测量：高标准追求 / 赢家心态 / 与同类对比时希望产品放大成果的倾向

1. <题干> ——（1–5 Likert）
2. <题干> ——（1–5 Likert）
3. <题干> ——（1–5 Likert）
4. <题干> ——（1–5 Likert）
5. <题干> ——（1–5 Likert）
6. <可选 6-7 题>

### 计分与分群说明

<每维度求和；维度间相关性与分群阈值；建议样本量与信效度检验路径>

---

## 自检（agent 必填，每条带证据）

- [ ] **命名归位**：文件名 `tool02_jas_survey_<product>.md` —— 证据：本文件名为 `___`
- [ ] **YAML 完整**：date / type / tool / product / language 五字段齐全 —— 证据：第 1-N 行
- [ ] **跨工具引用锁版本**：上游引用都用 `[[...]]` + 日期 / 本工具无上游 —— 证据：第 X 行
- [ ] **格式硬约定**：Likert 1=Strongly Disagree … 5=Strongly Agree **原文照用**；SI / JI / HDC 三维各 ≥5 题；Format: Chinese —— 证据：抽样 2 题对应 Likert 块 + 维度归属
- [ ] **语言符合约定**：默认 zh-CN —— 证据：整篇语言判定
- [ ] **不越边界**：本产出仅为用户行为分群量表，没有当 outcome metric / opportunity score（让位 `tony-ulwick-perspective`）；也没有当临床 Type A 健康筛查 —— 证据：一句话申明位置
- [ ] **v1 扩展声明**：未用 v1 深化 / 用了 v1 深化（具体哪几项）—— 证据：产出顶部声明位置
