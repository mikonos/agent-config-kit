---
date: <YYYY-MM-DD>
type: research / tool-output
tool: tool03-four-lens
product: <产品代号或名称>
language: zh-CN
status: draft
inputs:
  - <产品介绍来源>
  - <用户访谈 / 评论原始文本来源>
---

# Tool 3 — 四镜深度洞察与创新框架 Four-Lens Deep Insight & Innovation Framework
> Product: <产品代号或名称>
> Stage: Stage 3 洞察分析（先于 Tool 1；Tool 3b 在 Stage 4 复用本提示词的创新输出段）
> Prompt source: `references/original_prompt_blocks.md#tool-3`
> Methodology anchor: `references/methodology_foundations.md` § 消费者心理学四镜

## 上下文输入（执行前必填）

- **产品介绍**：<...>
- **用户访谈 / 评论文本来源**：<文件名 + 条目数量 + 采集时间>
- **语言要求**：zh-CN

## 输出主体

### 一、Insight Lens 1：Find Patterns（找模式）

- **Repeated behaviors**：<重复行为>
- **Repeated complaints**：<重复抱怨>
- **Hidden structural tension**：<结构性张力>
- **Design implications**：<设计启示>

### 二、Insight Lens 2：Find Contradictions（找矛盾）

- **Stated vs actual behavior**：<言行不一>
- **Source of contradiction**：<情感或实际冲突>
- **User compensation behaviors**：<补偿行为>
- **Design implications**：<设计启示>

### 三、Insight Lens 3：Find Feelings（找情感）

- **Emotionally charged moments**：<情绪性时刻>
- **Deep emotional needs**：<深层情绪驱动 — shame / pride / longing / relief / control / ease / beauty / belonging / identity>
- **Identity transformation（user becomes…）**：<身份转变>
- **Design implications**：<设计启示>

### 四、Insight Lens 4：Find Shortcuts（找捷径）

- **What users avoid / don't want to think about**：<规避的心智负担>
- **Existing workarounds**：<现存绕道方案>
- **Desired automation / simplification**：<希望被自动化的微决策>
- **Design implications**：<设计启示>

### 五、Synthesis Insight（综合洞察）

<一段高浓度心理洞察，整合四镜，揭示产品真实机会空间>

### 六、创新输出（如本次只跑 Tool 3 主线，可留占位指向 Tool 3b）

- **New forms / shapes**：<...>
- **New features**：<...>
- **New usage scenarios / rituals**：<...>
- **Hero concept**：<一个最强概念 + 清晰的心理 why>

> 注：若本次为 Stage 3 Tool 3 主线运行，本段可仅留指针 `→ 见 [[tool03b_innovation_<product>_<date>]]`；若为合并运行，按完整 6 段输出。

---

## 自检（agent 必填，每条带证据）

- [ ] **命名归位**：文件名 `tool03_four_lens_<product>.md` —— 证据：本文件名为 `___`
- [ ] **YAML 完整**：date / type / tool / product / language 五字段齐全 —— 证据：第 1-N 行
- [ ] **跨工具引用锁版本**：原始文本来源 + 下游 Tool 1 / Tool 3b 引用都用 `[[...]]` + 日期 —— 证据：第 X 行
- [ ] **格式硬约定**：四镜各含「重复行为/抱怨 → 结构性张力 → 设计启示」三层；**不是摘要**（Please do NOT summarize the text; reveal the hidden structures beneath it）—— 证据：抽样 Lens 1 与 Lens 3 的"结构性张力"行
- [ ] **语言符合约定**：默认 zh-CN —— 证据：整篇语言判定
- [ ] **不越边界**：本产出是洞察素材，没有当切换/购买动因诊断（让位 `bob-moesta-perspective`），也没有把综合洞察当品牌定稿 —— 证据：一句话申明位置
- [ ] **v1 扩展声明**：未用 v1 深化 / 用了 v1 深化（如证据台账、正反类拆分）—— 证据：产出顶部声明位置
