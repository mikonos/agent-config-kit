---
date: <YYYY-MM-DD>
type: research / tool-output
tool: tool05-literature
product: <产品代号或名称>
language: zh-CN
status: draft
inputs:
  - <论文 PDF 文件名 / DOI / arXiv ID>
---

# Tool 5 — 文献阅读 Reading Academic Papers
> Product: <产品代号或名称>
> Stage: Stage 6 持续学习（独立支撑，可与任何阶段并行）
> Prompt source: `references/original_prompt_blocks.md#tool-5`
> Methodology anchor: `references/methodology_foundations.md` § 学术研究方法论 11 段

## 上下文输入（执行前必填）

- **论文标识**：<标题 / DOI / arXiv ID>
- **PDF 来源**：<文件路径或链接>
- **关联产品 / 项目**：<...>
- **语言要求**：zh-CN

## 输出主体（11 段标准化分析）

### 1. Research Background（研究背景）
- **Title**：<...>
- **Summary**：<...>
- **Key Points**：<...>
- **Authors & Affiliations**：<...>

### 2. Research Objectives（研究目标）
<研究目标 + 具体回答的研究问题>

### 3. Research Hypotheses（研究假设）
- 原假设（H0）：<...>
- 备择假设（H1）：<...>
- 其他假设：<...>

### 4. Theoretical Framework（理论框架）
<使用的理论模型 / 概念图>

### 5. Research Methods（研究方法）
<访谈 / 焦点小组 / 问卷 / 实验等的设计、样本、流程>

### 6. Figures and Tables（图表拆解）
<对复杂图表的逐项解释>

### 7. Analytical Methods（分析方法）
<数据分析技术、样本量、分析结果、显著性>

### 8. Research Conclusions（研究结论）
<...>

### 9. Limitations and Future Work（局限与未来工作）
<原文承认的局限 + 作者建议的下一步>

### 10. References（关键参考文献摘要）
<重要引文逐条 1 句话>

### 11. Paper Evaluation（论文质量评估）
- **Scientific Rigor（科学性）**：<评估 + 证据>
- **Innovation（创新性）**：<评估 + 证据>
- **Academic Rigor（学术严谨度）**：<评估 + 证据>

### 12. 对当前产品的启示（可选附加段）

<论文与本产品的接口；可借用的方法/变量；可证伪的产品假设>

---

## 自检（agent 必填，每条带证据）

- [ ] **命名归位**：文件名 `tool05_literature_<product or paper-slug>.md` —— 证据：本文件名为 `___`
- [ ] **YAML 完整**：date / type / tool / product / language 五字段齐全 —— 证据：第 1-N 行
- [ ] **跨工具引用锁版本**：本工具松耦合，引用其他工具产出时锁版本 / 无引用 —— 证据：第 X 行 / 本工具无上游
- [ ] **格式硬约定**：11 段标准化分析齐全（研究背景 / 目标 / 假设 / 框架 / 方法 / 图表 / 分析 / 结论 / 局限 / 参考文献 / 评估）+ 三维评估（科学性 / 创新性 / 学术严谨度）；Format: Chinese —— 证据：抽样第 3 段假设 + 第 11 段评估的行号
- [ ] **语言符合约定**：默认 zh-CN —— 证据：整篇语言判定
- [ ] **不越边界**：本产出是论文结构化阅读笔记，**不是同行评审 / 不是元分析 / 不是行业研报**；不直接拍板产品决策 —— 证据：一句话申明位置
- [ ] **v1 扩展声明**：未用 v1 深化 / 用了 v1 深化（如证据台账接驳）—— 证据：产出顶部声明位置
