---
name: research-execution
type: reference
status: hard-rules
applies_to: evidence-research-suite v3
---

# 执行规则 · 六阶段流水线 + 工序纠偏 + 硬约束

> 本文件是 evidence-research-suite v3 的执行规则真源。SKILL.md 只做路由，所有执行规则在这里。Agent 触发 skill 后必读本文件。

## 一、六阶段执行序列（**拷贝即可跑**）

**⚠️ 关键：工具编号 ≠ 执行顺序。** 不要按 Tool 1 → 2 → 3 → ... → 10 跑。

```text
Stage 1  用户识别      →  [Tool 4, Tool 7, Tool 2]
Stage 2  需求挖掘      →  [Tool 6, Tool 9, Tool 10]
Stage 3  洞察分析      →  [Tool 3, Tool 1]
Stage 4  产品创新      →  [Tool 3b]              （= Tool 3 提示词的创新输出二次运行）
Stage 5  生态构建      →  [Tool 8]
Stage 6  持续学习      →  [Tool 5]                （独立支撑，可与任何阶段并行）
```

**执行规则**：
- **阶段间严格上下游**：上一阶段产出齐了才能开下一阶段，禁止跳阶段
- **阶段内可并行**：方括号内的工具可同顺序 / 不同顺序 / 并行 subagent，但都必须在本阶段闭合后才进入下一阶段
- **每次 invoke 把上述 `Stage X → [...]` 序列完整拷贝到工作上下文**，作为 single source of truth 跟踪进度

## 一点五、Job Statement Evidence Layer（v3.1 硬约束）

当 Tool 3 / Tool 6 / Tool 7 的输入包含用户访谈、Amazon 评论、社媒反馈、客服记录或其他 raw user voice 时，先抽取 Job Statement，再写需求/洞察。

**必读**：`.cursor/skills/jtbd-result-audit/references/job_statement_quality_gate.md`

**顺序**：

1. Raw voice / interview transcript / review corpus
2. Job Statement 九格表（含 `evidence_grade` 与 `lint_flags`）
3. Tool 6 emotional/social jobs、Tool 7 functional jobs、Tool 3 四镜洞察
4. Tool 1 / Tool 3b / Tool 8 下游综合

**禁止**：

- 把评论抱怨直接写成创新概念。
- 把“希望产品能...”写成补偿行为。
- 把缺原话、缺 context、缺 outcome 标尺的条目升格为需求结论。
- 一条 Job Statement 混入多个场景后再做聚类。

**降级**：九格关键字段缺失时，写入 `Open Questions / Tool 9 probes`；不要进入 Tool 7 主需求表或 Tool 3b 创新输出。

## 二、工序纠偏（为什么要这样排）

1218 原稿明确说阶段顺序如上，tool 编号只是工具库索引：

- **Tool 1（产品灵魂）属于 Stage 3 洞察分析后半段**，紧接 Tool 3 之后；**不是开局**
- **Tool 3b（创新输出）是 Tool 3 提示词在创新阶段的二次运行**，紧接 Tool 1 之后
- **Tool 5（文献阅读）独立支撑**，在 Stage 6 持续学习层，可与任何阶段并行

**「新品开发全流程」的分周节奏**（1218 §722-743）：
- 第 1 周 用户识别：Tool 4 → Tool 6 → Tool 7
- 第 2 周 深度调研：Tool 9 设计 → 执行访谈 → Tool 3 分析
- 第 3 周 量化验证：Tool 10 设计 → Tool 2 行为分群
- 第 4 周 创新输出：Tool 1 → Tool 3b → Tool 8

**工序纠偏的实战 verified 价值**（v5 vs v4 对比证据）：v5 灵魂段六字「被需要+允许下线」trace 到 Tool 3 Klement Big/Little Hire 切分；v4 Tool 1 在 Stage 1 开局，灵魂段无法承载 Tool 3 洞察。这不是结构重排，是承载洞察的能力差异。

## 三、Upstream Tool Lock（v3 新增硬约束）

**Tool N 的 inputs 必须等待上游 tools 到 v1.0 / final 才能引用**：

- 若上游 tool 是 v0.x draft → **PAUSE Tool N**，等上游 finalize
- 若上游 tool 在 Tool N 启动后从 v1.0 → v1.1（patch round）：
  - 检查 v1.1 改动是仅论证骨架（无 finalist 变更）→ 不重启 Tool N，继续
  - 检查 v1.1 改动影响 finalist / 核心产出 → **PAUSE Tool N，重 input 从 v1.1，发布为 Tool N v1.1**

**Phase Violation Rollback**：
- 发现 Phase 3+ 工具（Tool 1 / 3b）在 Phase 1-2（Tool 4 / 7 / 2 / 6 / 9 / 10）未完成 v1.0 前被启动 → **PAUSE 全部 Phase 3+ 工作，回到 Phase 1-2，重新收集 Tool 1 / 3b inputs**
- 禁止发布 hybrid-version 产出（部分 input 用 v0.x、部分用 v1.0）

## 四、跨工具引用日期格式（v3 硬约束 · k 神 P0-4）

**所有跨工具引用必须含 date 格式**：

```
[[toolXX_<name>_<product>_YYYYMMDD]]
```

**示例**（v5 实操已自然这样做，sed v3 沉淀为硬约束）：
```yaml
inputs:
  - "[[tool04_target_users_productFamilyAI_20260527]]"
  - "[[tool03_four_lens_productFamilyAI_20260527]]"
  - "[[tool06_emotional_social_productFamilyAI_20260527]]"
```

**禁止**：
- 无日期 wikilink（`[[tool04_target_users_productFamilyAI]]` ❌）
- 自然语言引用（"Tool 4 的分群" ❌）
- 简写 wikilink（`[[Tool 4]]` ❌）

**Mechanical verify**：每个 tool 产出文件用 `grep -E "\[\[tool[0-9]+.*_[0-9]{8}\]\]"` 验证 inputs 字段全部含日期。

## 五、YAML frontmatter 标准

```yaml
---
date: YYYY-MM-DD
type: research/tool-output
tool: toolXX-<工具英文短名>
product: <产品代号或名称>
language: zh-CN  # 默认；Tool 9 / Tool 1 部分可指定其他
status: draft / in-review / approved
version: v1 / v2 / ...
inputs:
  - "[[tool0X_<name>_<product>_YYYYMMDD]]"
  - ...
---
```

## 六、文件命名

`toolXX_<工具英文短名>_<产品代号>.md`（如 `tool01_product_soul_productFamilyAI.md`）。

产品代号用 CamelCase 紧凑形式（避免中文导致 grep / hook / shell 出错）。

## 七、阶段间握手要求（硬约定）

**Tool 4 → Tool 7 / Tool 6**：Tool 4 输出的分群必须有命名 + needs/pain summary；Tool 7 / 6 的 inputs 字段必须列 Tool 4 锁版本

**Raw user voice → Tool 3 / Tool 6 / Tool 7**：若输入是访谈/评论/反馈，必须先有 Job Statement 表；Tool 6/7 的每条需求至少能回指一个 Job Statement id 或明确标 `hypothesis / 待追问`

**Tool 3 → Tool 1**：Tool 3 必须有「综合洞察」收尾段（不只是四镜清单）；Tool 1 inputs 必须列 Tool 3 锁版本

**Tool 1 → Tool 3b**：Tool 3b inputs 必须**同时**列 Tool 3 综合洞察 + Tool 1 灵魂段落。禁止跳 Tool 1 直接从 Tool 3 跑 Tool 3b（这是 v3 工序纠偏的核心）

**Tool 6 反向 anxiety 类 → Tool 7 / Tool 1 / Tool 8**：Tool 6 反向类必须映射到 Tool 7「功能边界」+ Tool 1「反触发文案」+ Tool 8「GTM Anxiety-blocker tag」。详见 `references/v1_engineering_extensions.md` 第 2 节

## 八、Verification（执行收尾自检）

每个工具产出收尾按 `references/verify.md` 的自检 block 模板，**每条带 triple 证据**（无 triple = fake echo，重做）。
