---
name: jtbd-amazon-research
description: End-to-end Amazon review JTBD research workflow. Use when the user wants the full pipeline from CSV intake to structured coding, clustering, quant analysis, and bridge outputs for downstream research.
---

# JTBD Amazon Research

这是 **完整研究总流程 skill**。  
它负责定义研究项目怎么做完，不负责把每一条评论怎么跑得最稳。

家族关系：

- `jtbd-amazon-research` = 总流程 / 总导演
- `jtbd-review-runner` = 评论级执行器
- `jtbd-result-audit` = 结果审计器

## 适用场景

- 用户给了一份 Amazon 评论 CSV，要做完整 JTBD 研究
- 需要从评论一路产出：
  - 结构化结果
  - Job / Feature 聚类
  - QuantAnalysis
  - Bridge outputs
- 需要把研究结果交给更高层方法论或决策模块

## 核心原则

1. **全量流程，不是单次跑数**
2. **RawQuotes / Structured data / QuantAnalysis 分层产出**
3. **跑完之后必须过审计 gate**
4. **默认定向修订，不默认全量重跑**
5. **评论先还原成 Job Statement，再进入机会判断**：用户抱怨、星级和 feature mention 不能直接变成产品机会；必须先过已安装 `jtbd-result-audit/references/job_statement_quality_gate.md`

## 数据边界

公开包不附带真实顾客评论、私有项目路径或测试 prompt。使用者应提供自己有权处理的评论 CSV、prompt、codebook 和输出目录。

## 推荐阶段

### Phase 1. Intake

- 检查 CSV 字段
- 统计总量与星级分布
- 确认字段映射

如需先把原始 Amazon CSV 清洗成标准评论表，优先用：

- 已安装 `jtbd-amazon-research/scripts/clean_amz_reviews.py`

示例：

```bash
python "<installed-skill-dir>/scripts/clean_amz_reviews.py" \
  --input-file "raw_reviews.csv" \
  --output-file "clean_reviews.csv" \
  --report-file "cleaning_report.md" \
  --review-prefix "skylight15"
```

### Phase 2. Calibration

在真正全量处理前，先调用：

- `jtbd-review-runner`

完成：

1. prompt / codebook 校准
2. 小样本验证
3. 决定是否全量、定向重跑或先修口径

### Phase 3. Production

用 `jtbd-review-runner` 产出评论级结果。

要求：

- 分片主跑
- 明确 summary
- 失败尾巴串行补跑
- 形成 `final_out`

### Phase 4. Audit Gate

这是这次任务验证出来必须加入的步骤。

在进入聚类和量化之前，必须让独立只读 reviewer 调用：

- `jtbd-result-audit`

至少确认：

1. 文件是否完整
2. 是否存在系统性边界漂移
3. 是否需要定向修订
4. Job Statement 九格与六类 lint 是否过门禁

如果 audit 没过：

- 先修结果
- 不要直接进入 QuantAnalysis

执行者不得自审自批。优先使用当前 Runtime 的独立 Agent / reviewer；若不可用，明确标记为非独立自审，并交给人类复核。reviewer 只输出审计报告、风险桶和修订建议，执行者负责定向修订并记录处理结果。

### Phase 5. Clustering / Job-Feature Synthesis

- Job Statement 聚类：先按 `Context / Main Job / Desired Outcome / Compensation Behavior / Current Solution` 聚类，再映射到 Job / Feature
- Job 聚类
- Feature 聚类
- 高价值矛盾点与 workaround 抽取

禁止把单条评论里的抱怨直接写成 opportunity。若 Job Statement 关键字段缺证据，只能进入 `OpenQuestions / Interview probes`。

### Phase 6. Quant / Bridge

- QuantAnalysis
- Brand / Emotional / Contradictions / OpenQuestions
- 与下游研究框架对接
- 将 `Desired Outcome` 转成可量化题项或追问，不把模糊形容词直接当 metric

### Phase 7. Final Packaging

最终应至少有：

- `master CSV / JSONL`
- 审计报告
- 修订报告
- 分析底稿

## 默认决策顺序

当用户问“要不要重跑”时，优先顺序是：

1. 先判断是 **字段口径问题** 还是 **执行结果问题**
2. 口径问题先修 prompt / codebook
3. 小样本验证
4. 定向重跑高风险样本
5. 只有在用户明确要求或旧结果整体不可信时才全量重跑

## 什么时候不要用它

如果用户只是要：

- 跑几条评论
- 校 prompt
- 补跑失败
- 看某批结果是否可信

那不要直接上总流程，改用：

- `jtbd-review-runner`
- `jtbd-result-audit`
