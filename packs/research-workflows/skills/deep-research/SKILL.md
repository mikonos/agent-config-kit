---
name: deep-research
description: 系统化联网深度调研（多角检索、全页抓取、交叉验证）。在需要当前网页信息、行业/竞品/技术事实、或内容生成前补证据时优先于单次随意搜索。触发：research、调研、什么是 X、对比 X 与 Y、有哪些最新进展。来源：bytedance/deer-flow（已适配本仓库工具名）。
---

# Deep Research（联网深度调研）

> **出处**：[`bytedance/deer-flow`](https://github.com/bytedance/deer-flow) `skills/public/deep-research`（main），经本项目适配 `WebSearch` / `WebFetch` 及 MCP 检索能力。

## 与 `deep-reading` 的分工

| 场景 | 用哪个 |
|------|--------|
| 用户已给书/长文/链接/附件，要**消化并进 ZK** | `deep-reading` |
| 主要靠**网上现查**拼出证据链、趋势、对比 | **本 skill** |

ZK 相关落盘、YAML、链接规则：执行前可读 `.cursor/skills/vault-writing-preamble/SKILL.md`。

## Overview

系统化网页调研方法论。**在依赖实时信息的内容任务前**先按本流程检索，避免仅凭模型内训或一两次搜索就写结论。

## When to Use

**优先加载本 skill 当：**

### 调研类

- 「什么是 X」「解释 X」「调研 X」「X 和 Y 对比」
- 需要**多源、较新**信息，单次搜索明显不够

### 内容生成前（预调研）

- 幻灯片、文章、报告、文档、前端方案里要**真实案例/数据/出处**
- 任何需要「现查」支撑产出的任务

## Core Principle

**不要只靠常识或单次搜索就交付。** 产出质量取决于调研的广度与深度；**一轮搜索几乎永远不够**。

## Research Methodology

### Phase 1: Broad Exploration

1. **Initial Survey**：用 `WebSearch`（及可用的 MCP 搜索类工具，如 exa）扫主题全貌  
2. **Identify Dimensions**：从结果里拆出子题、利益方、技术线、监管/伦理等角度  
3. **Map the Territory**：记下对立观点、主要玩家、术语变体  

### Phase 2: Deep Dive

对每个重要维度：

1. **Specific Queries**：更窄的关键词与英文/中文变体  
2. **Multiple Phrasings**：同义替换、产品名、标准名、缩写  
3. **Fetch Full Content**：对高相关、权威 URL 用 **`WebFetch`** 读全文，不停留在摘要  
4. **Follow References**：文中提到的报告、论文、官方文档 → 再搜再抓  

### Phase 3: Diversity & Validation

| 信息类型 | 目的 | 查询示意 |
|----------|------|----------|
| Facts & Data | 可验证证据 | statistics、market size、数据集 |
| Examples & Cases | 落地感 | case study、implementation |
| Expert / Authority | 背书 | interview、analysis、官方 blog |
| Trends | 时间轴 | trends、forecast、outlook |
| Comparisons | 选项框架 | vs、alternatives、compared to |
| Challenges | 反方与边界 | limitations、criticism、failure |

### Phase 4: Synthesis Check

进入写作/方案前自检：

- [ ] 是否从至少 **3～5 个不同角度** 搜过？  
- [ ] 是否对**最关键**的来源做过 **WebFetch 全文**？  
- [ ] 是否有**数据、实例、权威观点**？  
- [ ] 是否覆盖**利好与限制/批评**？  
- [ ] 时间是否对齐用户问的粒度（见下「时间意识」）？  

**任一为否 → 继续调研再产出。**

## 工具约定（Cursor / 本仓库）

- **搜索**：`WebSearch`；若 MCP 提供更强检索（如 exa），可与 `WebSearch` 交叉使用。  
- **全文**：`WebFetch`（对具体 `https://...` URL）。  
- **勿**把搜索snippet当已读原文；关键结论尽量落到**打开过的页面**。

## Search Strategy Tips

### 有效问法

```
❌ "AI trends"
✅ "enterprise AI adoption trends 2026"

# 权威信源提示
"[topic] site:gov" / "[topic] annual report" / "[topic] technical documentation"

# 内容类型
"[topic] case study" / "[topic] benchmark" / "[topic] postmortem"
```

### 时间意识（Temporal）

在构造查询前，先看你**上下文里的当前日期**（系统提供的 today / user_info）。

| 用户意图 | 精度 | 示例 |
|----------|------|------|
| 今天 / 刚发布 | 月+日+年 | `"product launch March 26 2026"` |
| 本周 | 周区间 | `"AI releases week of March 24 2026"` |
| 最近 / 最新 | 至少到月 | `"LLM updates March 2026"` |
| 今年趋势 | 年 | `"cloud trends 2026"` |

- 问「今天有什么新闻」时，**不要**只搜 `"news 2026"`，应带**月日**或 *this week* 类表述。  
- 可用多种写法：数字日期、英文月份、`latest`、`this week`。

### 何时 WebFetch

- 摘要已显示高度相关且权威（官网、论文页、监管文件、年报 PDF 的 html  landing）  
- 需要表格、数字、方法细节、引用列表  
- 需要核对「原文到底怎么写的」  

### 迭代

检索 → 列缺口 → 换关键词/换语言/换信源类型 → 重复直到通过 Synthesis Check。

## Quality Bar

可自信回答再写正文：

- 关键事实与数字？  
- 2～3 个可核对的真实案例？  
- 专家或官方怎么说？  
- 趋势与「现在为什么重要」？  
- 主要风险、限制、争议？  

## Common Mistakes

- 1～2 次搜索就停  
- 只看摘要不拉全文  
- 只搜一个子话题  
- 忽略反面证据  
- 该精确到日时只用年份  
- 调研未完就开始长文生成  

## Output

调研阶段结束后你应持有：

1. 多角度理解  
2. 可引用的数据与出处  
3. 实例与案例  
4. 权威来源（含你已 fetch 的页面）  
5. 趋势与上下文  

**再**进入报告/幻灯片/方案/营销文案等生成步骤。
