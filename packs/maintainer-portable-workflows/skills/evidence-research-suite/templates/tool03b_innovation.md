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

### 五、Hero 反触发声明 + Verifiable Acceptance Criteria（v3 硬约束 · k 神 P0）

**反触发声明（产品不应该做什么）**：列 3-5 条「Hero 承诺不做的事」，每条含：
- 陷阱名称 + 触发用户哪条情感恐惧（关联 Tool 6 反向 anxiety 类）
- 产品级承诺（不做这件事）
- 具体设计规则（how to avoid）

示例（v5 Tool 3b 示范）：
- ❌ 不做 family surveillance（隐私焦虑反触发；Tool 6 §E4）
- ❌ 不做 AI control tower（替代决策 vs 支撑协作；Tool 6 §E5）
- ❌ 不做 engagement machine for kids（graduation 否决 vs subscription anchoring）
- ❌ 不做 corporate vibe（家庭管理白板讽刺；Tool 6 §RS-#11）

**Verifiable Acceptance Criteria（hero 不是抽象愿景）**：必须能回答「如果目标用户用了 N 天、hero 没有兑现，怎么判定产品失败？」

| Metric | Target | Fail Threshold | Measurement Method |
|---|---|---|---|
| M1: <metric name> | <target value> | <fail value> | <how to measure> |
| M2: ... | | | |
| M3: ... | | | |

**Fail Criteria**：≥2 metrics 未达标 → hero broken → redesign required

---

## 自检（agent 必填，每条带证据 triple）

- [ ] **命名归位**：文件名 `tool03b_innovation_<product>.md` —— triple: (filename, this_file, L1)
- [ ] **YAML 完整 + version**：date / type / tool / product / language / status / version / inputs 八字段齐全 —— triple: (yaml_complete, this_file, L1-LN)
- [ ] **跨工具引用锁日期格式**：Tool 3 + Tool 1 inputs 都用 `[[..._YYYYMMDD]]` —— triple per upstream: ([[upstream_ref]], inputs_field, L_X)
- [ ] **格式硬约定**：仅输出 Output §6 四段 + §五 反触发 + Verifiable Acceptance；**不重复四镜分析**；每条创新带一句心理 why 回指 Lens 或灵魂段 —— triple sample 1: (feature_name + why_anchor, this_file, L_X); triple sample 2: (hero_concept + soul_anchor, this_file, L_Y)
- [ ] **语言符合约定**：默认 zh-CN —— triple: (language, this_file, L_global)
- [ ] **不越边界**：本产出是创新概念候选，不是 PRD / spec / roadmap；功能优先级让位 `marty-cagan-perspective` —— triple: (statement_in_text, this_file, L_X)
- [ ] **v1 扩展声明**：未用 v1 深化 / 用了 v1 深化（如承重假设、Bull's Eye、B/F/H 变体）—— triple per extension: (extension_name, this_file_section, L_X)
- [ ] **v3 新增 · 反触发 + Verifiable Acceptance 必填**：§五 含 3-5 条反触发 + ≥3 metric 的 Verifiable Acceptance 表 + Fail Criteria 声明 —— triple: (anti_pattern_section, this_file, L_X); triple: (metrics_table, this_file, L_Y)
- [ ] **v3 新增 · 机械 verify pass**：主上下文已用 `references/verify.md` 的 grep 脚本验证本产出 triple 至少 5 条，全部 pass —— triple: (verify_log_path, parent_log, L_X)
