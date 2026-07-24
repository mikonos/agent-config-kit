---
date: <YYYY-MM-DD>
type: research / tool-output
tool: tool01-product-soul
product: <产品代号或名称>
language: zh-CN
status: draft
inputs:
  - <Tool 3 综合洞察文件名（如 tool03_four_lens_<product>_<date>）>
  - <目标市场 / 目标人群 描述源>
---

# Tool 1 — 产品灵魂 Soul of Product
> Product: <产品代号或名称>
> Stage: Stage 3 洞察分析（紧接 Tool 3 之后；不是开局）
> Prompt source: `references/original_prompt_blocks.md#tool-1`
> Methodology anchor: `references/methodology_foundations.md` § Dichter 品牌心理学四维

## 上下文输入（执行前必填）

- **产品定义**：<...>
- **目标市场**：<...>
- **目标人群**：<...>
- **上游 Tool 3 综合洞察**：`[[tool03_four_lens_<product>_<date>]]`
- **语言要求**：zh-CN（广告语允许中英双语）

## 输出主体

### 一、四维心理分析

#### 1. 核心问题（Core Problem）
<功能层 / 情感层 / 身份层张力——产品消失后用户最怀念什么；寻求"日常便利"还是"内在焦虑"的解脱；减轻哪种情绪负担；强化哪种正向状态>

#### 2. 社会参照框架（Sociological Frame of Reference）
<使用产品时用户希望他人感知的身份；产品在何种社交场景被展示；象征意义>

#### 3. 国家文化（National Culture）
<嵌入的国家/地区文化价值；放大的文化敏感性（仪式 / 可靠 / 精度等）；可用作锚点的文化符号或习语>

#### 4. 当代世界（Contemporary World）
<本时代的情绪与技术气候；产品回应的时代张力；10 年后哪些功能仍永恒、哪些会过时>

### 二、心理动机综合

<从四维推出的潜意识动机——吸引/魅力、安全、尊重/自尊、归属、自我价值与掌握感、逃离/情绪释放；每条与四维证据对齐>

### 三、产品灵魂段落

<一段完整、有重量的灵魂段，约 150-250 字；说出未说之言，不是功能复述>

### 四、广告语 × 3（情感共鸣，非功能陈述）

1. **中文**：<...>　**English**：<...>
2. **中文**：<...>　**English**：<...>
3. **中文**：<...>　**English**：<...>

### 五、用户内心独白式品牌信息

> <第一人称 1-2 句，回应用户潜意识身份与抵抗/追求>

---

## 自检（agent 必填，每条带证据）

- [ ] **命名归位**：文件名 `tool01_product_soul_<product>.md` —— 证据：本文件名为 `___`
- [ ] **YAML 完整**：date / type / tool / product / language 五字段齐全 —— 证据：第 1-N 行
- [ ] **跨工具引用锁版本**：Tool 3 / Tool 4 / Tool 6 等上游引用都用 `[[...]]` + 日期 —— 证据：第 X 行
- [ ] **格式硬约定**：四维心理分析 + 灵魂段落 + 3 条情感共鸣广告语（非功能陈述）+ 用户内心独白；广告语中英双语；Format: Chinese 主体 —— 证据：随机抽样 2 条广告语对应原文位置
- [ ] **语言符合约定**：默认 zh-CN，广告语允许中英双语 —— 证据：整篇语言判定
- [ ] **不越边界**：本产出仅为用户洞察的可读化呈现，没有把广告语当品牌定稿；品牌定位 / 视觉识别 / 传播策略让位 `april-dunford-perspective` / `positioning-statement` —— 证据：一句话申明位置
- [ ] **v1 扩展声明**：未用 v1 深化 / 用了 v1 深化（具体哪几项）—— 证据：产出顶部声明位置
