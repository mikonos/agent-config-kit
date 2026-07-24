---
date: <YYYY-MM-DD>
type: research / tool-output
tool: tool08-ecosystem
product: <产品代号或名称>
language: zh-CN
status: draft
inputs:
  - <产品概念来源>
  - "[[tool04_target_users_<product>_<date>]]"
  - "[[tool06_emotional_social_<product>_<date>]]"
  - "[[tool07_functional_needs_<product>_<date>]]"
---

# Tool 8 — 产品生态设计 Building Product Ecosystem
> Product: <产品代号或名称>
> Stage: Stage 5 生态构建（在 Tool 1 / Tool 3b 创新输出之后）
> Prompt source: `references/original_prompt_blocks.md#tool-8`
> Methodology anchor: `references/methodology_foundations.md` § JTBD 全维度 + 用户使用旅程 8 段

## 上下文输入（执行前必填）

- **产品概念**：<...>
- **目标用户**：`[[tool04_target_users_<product>_<date>]]`
- **关键产品特征**：<...>
- **关键使用场景**：<...>
- **可对接的现有 functional / emotional / social jobs**：上游 Tool 6 / Tool 7 引用
- **语言要求**：zh-CN

## 输出主体

### 一、Co-creation Ecosystem（共创生态 — 开放平台 + 第三方）

> 开放平台允许第三方开发者/合作伙伴贡献新产品或服务，整合进系统；目标是吸引多样资源、增强品牌整体竞争力。

| # | 产品 / 服务 | 第三方角色 | 解决的需求 / 痛点 | JTBD 维度（F/E/S/Related）| 旅程段位（Define→Conclude）|
|---|---|---|---|---|---|
| 1 | <...> | <...> | <...> | <...> | <...> |
| 2 | <...> | <...> | <...> | <...> | <...> |
| 3 | <...> | <...> | <...> | <...> | <...> |
| 4 | <...> | <...> | <...> | <...> | <...> |
| 5 | <...> | <...> | <...> | <...> | <...> |

**共创生态价值说明**：<2-4 句话讲清开放平台对用户旅程的整体增益、对品牌的长期价值>

### 二、Collaborative Ecosystem（协作生态 — 互联互通产品）

> 各产品与服务遵循共同标准/协议，无缝协作，降低用户操作复杂度；focus 是 usability 与减少操作复杂度。

| # | 产品 / 服务 | 互联接口 / 协议 | 解决的需求 / 痛点 | JTBD 维度（F/E/S/Related）| 旅程段位（Define→Conclude）|
|---|---|---|---|---|---|
| 1 | <...> | <...> | <...> | <...> | <...> |
| 2 | <...> | <...> | <...> | <...> | <...> |
| 3 | <...> | <...> | <...> | <...> | <...> |
| 4 | <...> | <...> | <...> | <...> | <...> |
| 5 | <...> | <...> | <...> | <...> | <...> |

**协作生态价值说明**：<2-4 句话讲清互联互通如何降低用户认知负担、如何提升旅程闭合度>

### 三、生态全景图（可选）

<可放一张 ASCII 图或 mermaid 图，展示中心产品与共创/协作生态的拓扑>

### 四、JTBD × 旅程矩阵覆盖自检

| 旅程段位 | Functional | Emotional | Social | Related |
|---|---|---|---|---|
| Define | <...> | <...> | <...> | <...> |
| Locate | <...> | <...> | <...> | <...> |
| Prepare | <...> | <...> | <...> | <...> |
| Confirm | <...> | <...> | <...> | <...> |
| Execute | <...> | <...> | <...> | <...> |
| Monitor | <...> | <...> | <...> | <...> |
| Modify | <...> | <...> | <...> | <...> |
| Conclude | <...> | <...> | <...> | <...> |

---

## 自检（agent 必填，每条带证据）

- [ ] **命名归位**：文件名 `tool08_ecosystem_<product>.md` —— 证据：本文件名为 `___`
- [ ] **YAML 完整**：date / type / tool / product / language 五字段齐全 —— 证据：第 1-N 行
- [ ] **跨工具引用锁版本**：Tool 4 / Tool 6 / Tool 7 引用都用 `[[...]]` + 日期 —— 证据：第 X 行
- [ ] **格式硬约定**：必须分 Co-creation 与 Collaborative **两段**；每项含产品/服务名 + 价值说明（解决什么需求/痛点）；覆盖 JTBD 四维（Functional / Emotional / Social / Related）+ 旅程 8 段（Define / Locate / Prepare / Confirm / Execute / Monitor / Modify / Conclude）；Tone: 精准、中性、专业 —— 证据：抽样 1 条 Co-creation + 1 条 Collaborative，对应 JTBD 维度 + 旅程段位
- [ ] **语言符合约定**：默认 zh-CN —— 证据：整篇语言判定
- [ ] **不越边界**：本产出是生态候选清单 + 价值说明，**不是商业 BD / 不是技术架构 / 不是合同**；商业可行性让位 PM 风险评估流程 —— 证据：一句话申明位置
- [ ] **v1 扩展声明**：未用 v1 深化 / 用了 v1 深化（如证据台账接驳、product 八段映射模板）—— 证据：产出顶部声明位置
