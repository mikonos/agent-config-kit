---
date: <YYYY-MM-DD>
type: research / tool-output
tool: tool07-functional-needs
product: <产品代号或名称>
language: zh-CN
status: draft
inputs:
  - "[[tool04_target_users_<product>_<date>]]"
  - <产品概念来源>
---

# Tool 7 — 功能需求 Finding Functional Jobs
> Product: <产品代号或名称>
> Stage: Stage 1 用户识别（与 Tool 4 / Tool 2 同阶段；目标用户取自 Tool 4）
> Prompt source: `references/original_prompt_blocks.md#tool-7`
> Methodology anchor: `references/methodology_foundations.md` § JTBD 功能维度
> Job Statement gate: `.cursor/skills/jtbd-result-audit/references/job_statement_quality_gate.md`（输入含访谈/评论/反馈时必读）

## 上下文输入（执行前必填）

- **目标用户**（来自 Tool 4 的某一群）：`[[tool04_target_users_<product>_<date>]]` § 群 Q<n> <群名>
- **产品概念**：<...>
- **明确突破的既有产品边界**（提示：不要被市面同品类功能限定）：<...>
- **Job Statement 表**（若输入含 raw user voice）：<文件名 + JS id 范围；缺则先抽取>
- **语言要求**：zh-CN

## 输出主体

### 零、Job Statement 映射（raw voice 输入时必填）

| Functional Job 候选 | Job Statement id | Main Job / Desired Outcome 支撑 | 补偿行为 / 当前方案 | 证据等级 | 缺口 |
|---|---|---|---|---|---|
| <job name> | JS-001 | <main job + desired outcome> | <compensation/current solution> | A/B/C/H | <缺证据 / 待追问 / 无> |

### Functional Jobs（15-20 个）

> 严格格式：`When I <情境>，I hope <期望>，so that <目标>`
> 每条第一人称动词开头；**单一任务，禁用 and / or 等连词**；情境-期望-目标因果链必须完整。

1. **<job name>**：When I <情境>，I hope <期望>，so that <目标>
2. **<job name>**：When I <情境>，I hope <期望>，so that <目标>
3. **<job name>**：When I <情境>，I hope <期望>，so that <目标>
4. **<job name>**：When I <...>，I hope <...>，so that <...>
5. **<job name>**：<...>
6. **<job name>**：<...>
7. **<job name>**：<...>
8. **<job name>**：<...>
9. **<job name>**：<...>
10. **<job name>**：<...>
11. **<job name>**：<...>
12. **<job name>**：<...>
13. **<job name>**：<...>
14. **<job name>**：<...>
15. **<job name>**：<...>
16-20. <...>

### 与产品边界的脱钩提示

<列 2-3 条不在既有竞品功能清单里、但仍属于用户希望产品完成的 functional jobs；作为创新输入留给 Tool 3b>

---

## 自检（agent 必填，每条带证据）

- [ ] **命名归位**：文件名 `tool07_functional_needs_<product>.md` —— 证据：本文件名为 `___`
- [ ] **YAML 完整**：date / type / tool / product / language 五字段齐全 —— 证据：第 1-N 行
- [ ] **跨工具引用锁版本**：Tool 4 目标用户引用用 `[[...]]` + 日期 —— 证据：第 X 行
- [ ] **格式硬约定**：每条 `When I... I hope... so that...` **完整因果链**；第一人称动词开头；**单一任务，no conjunctions**（不用 and / or 把两件事拼一条）—— 证据：抽样 2 条对应原文 + 验证无 and/or 拼接
- [ ] **Job Statement 证据层**：输入含访谈/评论/反馈时，每条 functional job 至少回指一个 JS id；`Main Job` 没有产品功能污染；`Desired Outcome` 不可衡量的已标 `待追问` —— 证据：抽样 2 条映射
- [ ] **语言符合约定**：默认 zh-CN —— 证据：整篇语言判定
- [ ] **不越边界**：本产出是 functional jobs 候选，**不是 PRD / spec / 功能优先级排序**（让位 `marty-cagan-perspective` / `tony-ulwick-perspective`）；不被既有竞品功能清单限定 —— 证据：一句话申明位置
- [ ] **v1 扩展声明**：未用 v1 深化 / 用了 v1 深化（如 Bull's Eye 渗透路径 B/F/H 分版、正反类需求拆分）—— 证据：产出顶部声明位置
