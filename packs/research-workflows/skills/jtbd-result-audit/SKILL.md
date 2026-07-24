---
name: jtbd-result-audit
description: Systematic audit of review-level JTBD result JSONs. Use when the user wants to know whether a batch is complete, trustworthy, drifting, or in need of targeted revision.
---

# JTBD Result Audit

这是 **结果审计器**。  
它不负责生产结果，而是负责判断一批结果到底能不能信。

家族关系：

- `jtbd-review-runner` 负责生产
- `jtbd-result-audit` 负责审查
- `jtbd-amazon-research` 负责编排整条研究流程

## 适用场景

- 用户问“这批结果质量怎么样？”
- 用户问“能不能直接拿去分析？”
- 用户想知道：
  - 有多少系统性问题
  - 问题集中在哪个字段
  - 是该全量重跑，还是定向修

## 审计目标

至少回答四个问题：

1. **完整性**：有没有缺口、失败、悬空
2. **分布漂移**：新批次和旧批次相比，有没有异常偏移
3. **规则违规**：有没有明显违背当前 prompt / codebook 边界
4. **可信度**：结果是否足以支撑后续研究
5. **Job Statement 保真度**：是否把原始评论/访谈还原成单一场景、可追溯、无功能污染的需求故事

## 核心风险桶

这类项目建议固定检查：

- `screen_only_with_strong_family_signal`
- `coordination_layer_short_weak_evidence`
- `supports_core_short_weak_evidence`
- `tool_pain_short_generic_positive`
- `purchase_unclear_short`
- `unmet_unclear_all`
- `high_risk_missing_coder_note`

Job Statement 语义层必须额外检查：

- `context_too_generic`
- `main_job_is_feature`
- `outcome_not_measurable`
- `wish_as_compensation`
- `mixed_scenes`
- `pain_without_consequence`

## 关键脚本

- 已安装 `jtbd-result-audit/scripts/audit_jtbd_results.py`

## 必读门禁

当结果里包含 Job / unmet need / pain / workaround / opportunity / requirement-card 输入时，先读：

- `references/job_statement_quality_gate.md`

这份文件是 Job Statement 九格、证据等级和六类 lint 的真源。本 skill 负责把它用于审计；不要在报告里另造一套口径。

## 数据边界

公开包不附带真实顾客评论或私有项目输出。请对使用者有权处理的数据运行审计，并把报告写到用户指定的项目目录。

### 常用命令

```bash
python "<installed-skill-dir>/scripts/audit_jtbd_results.py" \
  --review-csv clean_reviews.csv \
  --batch rerun_619_revised=rerun_619_20260424_karpathy/final_revised_out \
  --batch rerun_1154_final=rerun_remaining_1154_20260425_karpathy/final_out \
  --audit-dir systematic_audit
```

## 审计流程

### 1. 文件完整性

检查：

- 目标总数
- `final_out` 条数
- 是否有 `missing_ids`

### 2. 分布层检查

至少统计：

- `purchase_type_normalized`
- `support_level_for_family_ai_brain_normalized`
- `unmet_need_normalized`
- `hire_job_normalized`

如果有两批或多批结果，做漂移比较。

### 3. 规则层检查

重点盯：

- `organized / organization` 是否被过度抬高 `support_level`
- `screen_only` 是否压掉了明显家庭协同语义
- 极短好评是否被过度判成 `tool_pain`
- 高风险标签是否补了 `coder_note`

### 3.5 Job Statement 质量门禁

对进入聚类、洞察或需求卡的每条用户需求故事，按 `references/job_statement_quality_gate.md` 审：

1. 九格是否齐：`Context / Main Job / Desired Outcome / Constraints & Tensions / Compensation Behavior / Current Solution / Pains / Delights / Verbatim`
2. 证据等级是否标明：`A / B / C / H`
3. 六类 lint 是否通过：情境泛化、任务功能化、结果不可衡量、愿望冒充补偿行为、场景混线、痛点无情绪后果
4. 缺证据字段是否诚实写 `缺证据` 或 `待追问`，而不是被模型补编

若原始输出没有九格字段，不要直接判它合格；把结果标成 `needs_job_statement_extraction`，要求先补抽取层再做聚类。

### 4. 风险分层

把风险分成三类：

- **技术风险**：没跑完、文件缺口、summary 不封口
- **内容风险**：标签边界漂移、系统性误判
- **审计风险**：结果能用，但理由不可追溯

## 决策规则

### 可以直接进入分析

当以下条件同时满足时：

- 文件完整
- 强内容风险占比低
- 没有明显系统性坏桶

### 应先定向修订

当以下情况出现时：

- 问题集中在少数固定字段
- 风险样本量不大
- 误差不会改写大盘，但会污染边界判断
- Job Statement lint 集中在少数模式，可通过补 prompt/codebook 或定向重写修复

### 才考虑全量重跑

只有在以下情况才建议：

- prompt / codebook 根本口径错了
- 结果大盘分布明显失真
- 风险不是集中在少量样本，而是遍地开花
- 大量结果把用户故事写成功能清单，或九格关键字段普遍缺原话支撑

## 推荐产物

- `summary.json`
- `report.md`
- `risk_bucket.csv` 若干
- `job_statement_lint.csv`（若结果含 Job Statement 或可转需求字段）
- 若有修订，再补 `revision_report.md`

## 与其他 skill 的边界

如果用户要的是：

- “把评论跑出来”
  - 用 `jtbd-review-runner`

- “把整个 Amazon 评论研究做完”
  - 用 `jtbd-amazon-research`

- “判断这批结果值不值得信”
  - 用 `jtbd-result-audit`
