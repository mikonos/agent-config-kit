---
date: <YYYY-MM-DD>
type: research / tool-output
tool: tool06-emotional-social
product: <产品代号或名称>
language: zh-CN
status: draft
inputs:
  - "[[tool04_target_users_<product>_<date>]]"
  - <产品概念来源>
---

# Tool 6 — 情感与社交需求 Finding Emotional & Social Jobs
> Product: <产品代号或名称>
> Stage: Stage 2 需求挖掘（与 Tool 9 / Tool 10 同阶段；目标用户取自 Tool 4）
> Prompt source: `references/original_prompt_blocks.md#tool-6`
> Methodology anchor: `references/methodology_foundations.md` § JTBD 情感与社交维度
> Job Statement gate: `.cursor/skills/jtbd-result-audit/references/job_statement_quality_gate.md`（输入含访谈/评论/反馈时必读）

## 上下文输入（执行前必填）

- **目标用户**（来自 Tool 4 的某一群）：`[[tool04_target_users_<product>_<date>]]` § 群 Q<n> <群名>
- **产品概念**：<...>
- **使用情境聚焦**（可选）：<...>
- **Job Statement 表**（若输入含 raw user voice）：<文件名 + JS id 范围；缺则先抽取>
- **语言要求**：zh-CN

## 输出主体

### 零、Job Statement 映射（raw voice 输入时必填）

| Emotional/Social Job 候选 | Job Statement id | Context / Verbatim 支撑 | 证据等级 | 缺口 |
|---|---|---|---|---|
| <job name> | JS-001 | <context + quote> | A/B/C/H | <缺证据 / 待追问 / 无> |

### 一、Emotional Jobs（情感需求 10-15 个）

> 行首必须是 `feel` 或 `avoid feeling`；每条粗体 job name + 一句描述；第一人称动词开头。

1. **<job name>**：feel <情绪>，当 <情境> 时 <一句描述>
2. **<job name>**：avoid feeling <情绪>，当 <情境> 时 <一句描述>
3. **<job name>**：feel <...> <...>
4. **<job name>**：avoid feeling <...> <...>
5. **<job name>**：<...>
6. **<job name>**：<...>
7. **<job name>**：<...>
8. **<job name>**：<...>
9. **<job name>**：<...>
10. **<job name>**：<...>
11. **<job name>**：<...>
12-15. <...>

### 二、Social Jobs（社交需求 10-15 个）

> 行首必须是 `appear as` 或 `avoid appearing as`；每条粗体 job name + 一句描述；第一人称动词开头。

1. **<job name>**：appear as <身份/形象>，在 <社交场景> 中 <一句描述>
2. **<job name>**：avoid appearing as <身份/形象>，在 <社交场景> 中 <一句描述>
3. **<job name>**：appear as <...> <...>
4. **<job name>**：avoid appearing as <...> <...>
5. **<job name>**：<...>
6. **<job name>**：<...>
7. **<job name>**：<...>
8. **<job name>**：<...>
9. **<job name>**：<...>
10. **<job name>**：<...>
11-15. <...>

### 三、跨维度提示（不必每次填）

<识别情感与社交需求的张力点；若同一行为既要 feel A 又 avoid appearing as B，记下来供 Tool 1 / Tool 3 复用>

---

## 自检（agent 必填，每条带证据）

- [ ] **命名归位**：文件名 `tool06_emotional_social_<product>.md` —— 证据：本文件名为 `___`
- [ ] **YAML 完整**：date / type / tool / product / language 五字段齐全 —— 证据：第 1-N 行
- [ ] **跨工具引用锁版本**：Tool 4 目标用户引用用 `[[...]]` + 日期 —— 证据：第 X 行
- [ ] **格式硬约定**：情感行首必须 `feel` / `avoid feeling`；社交行首必须 `appear as` / `avoid appearing as`；每条粗体 job name + 一句描述；**第一人称动词开头**；Format: Chinese —— 证据：抽样 1 条情感 + 1 条社交对应原文行首
- [ ] **Job Statement 证据层**：输入含访谈/评论/反馈时，每条 emotional/social job 至少回指一个 JS id 或标 `hypothesis / 待追问`；没有原话支撑的不进入主表 —— 证据：抽样 2 条映射
- [ ] **语言符合约定**：默认 zh-CN —— 证据：整篇语言判定
- [ ] **不越边界**：本产出是 emotional / social jobs 候选，**不是功能 spec**（功能让位 Tool 7），也不是广告语 / 品牌定稿（让位 Tool 1 / `april-dunford-perspective`）—— 证据：一句话申明位置
- [ ] **v1 扩展声明**：未用 v1 深化 / 用了 v1 深化（如 Bull's Eye 渗透路径 B/F/H 分版、三段需求拆分）—— 证据：产出顶部声明位置
