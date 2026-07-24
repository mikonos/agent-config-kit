---
date: <YYYY-MM-DD>
type: research / tool-output
tool: tool03b-innovation
product: <产品代号或名称>
language: zh-CN
status: draft
inputs:
  - "[[tool03_four_lens_<product>_<date>]]"
  - "[[tool01_product_soul_<product>_<date>]]"
---

# Tool 3b — 创新输出 Innovation Output（复用 Tool 3 提示词的第 6 段）
> Product: <产品代号或名称>
> Stage: Stage 4 产品创新（紧接 Tool 1 之后；不是独立提示词，是 Tool 3 prompt 第 6 段「Based on all insights above, propose...」的二次运行）
> Prompt source: `references/original_prompt_blocks.md#tool-3`（仅 Output §6）
> Methodology anchor: `references/methodology_foundations.md` § 消费者心理学四镜 + Dichter 产品灵魂

## 上下文输入（执行前必填）

- **Tool 3 综合洞察**：`[[tool03_four_lens_<product>_<date>]]`
- **Tool 1 产品灵魂**：`[[tool01_product_soul_<product>_<date>]]`
- **创新边界 / 约束**（可选）：<供应链 / 平台 / 时间窗口>
- **语言要求**：zh-CN

## 输出主体（仅 4 段，不重复四镜分析）

### 一、New product forms / shapes（新形式）

<创新物理形态 / 新交互模式 / 新材料选择 / 可穿戴 / 模块化 / 便携 / 环境式设计>

- 形式 1：<名称> — <一句心理 why>
- 形式 2：<名称> — <一句心理 why>
- 形式 3：<名称> — <一句心理 why>

### 二、New features（新功能）

<化解深层张力 / 自动化用户捷径 / 增强情感或身份 / 移除阻力 / 智能自适应个性化>

- 功能 1：<名称> — <对应 Lens X / 灵魂段第 N 句>
- 功能 2：<名称> — <对应 Lens X / 灵魂段第 N 句>
- 功能 3：<名称> — <对应 Lens X / 灵魂段第 N 句>
- 功能 4-5：<...>

### 三、New usage scenarios / rituals（新场景与仪式）

<用户如何把产品嵌入日常 / 产品如何增强身份或情绪价值>

- 场景 1：<...>
- 场景 2：<...>
- 场景 3：<...>

### 四、Hero concept（英雄概念）

> **概念名**：<一句产品断言>
>
> **心理 why**：<为什么这个概念能同时回应 Lens 1-4 张力与灵魂段身份转变>
>
> **与既有方案的差距**：<这个概念不能从既有功能堆砌中推出的根本原因>

---

## 自检（agent 必填，每条带证据）

- [ ] **命名归位**：文件名 `tool03b_innovation_<product>.md` —— 证据：本文件名为 `___`
- [ ] **YAML 完整**：date / type / tool / product / language 五字段齐全 —— 证据：第 1-N 行
- [ ] **跨工具引用锁版本**：Tool 3 与 Tool 1 引用都用 `[[...]]` + 日期 —— 证据：第 X 行
- [ ] **格式硬约定**：仅输出 Output §6 四段（new forms / new features / new scenarios / hero concept），**不重复四镜分析**；每条创新带一句心理 why 回指 Lens 或灵魂段 —— 证据：抽样 1 条 feature + hero concept 的回指
- [ ] **语言符合约定**：默认 zh-CN —— 证据：整篇语言判定
- [ ] **不越边界**：本产出是创新概念候选，不是 PRD / spec / roadmap 决策；功能优先级让位 `marty-cagan-perspective`（四风险）—— 证据：一句话申明位置
- [ ] **v1 扩展声明**：未用 v1 深化 / 用了 v1 深化（如承重假设、Bull's Eye 渗透路径）—— 证据：产出顶部声明位置
