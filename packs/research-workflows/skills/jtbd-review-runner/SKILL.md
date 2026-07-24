---
name: jtbd-review-runner
description: Review-level JTBD execution runner. Use for prompt calibration, single-review dry runs, batch execution, shard reruns, serial retry, final output packaging, and audit handoff.
---

# JTBD Review Runner

这是 **评论级执行器**。  
它不负责整套研究结论，而是负责把「评论 CSV + prompt + codebook」稳定地跑成一批结构化结果。附带的自动批处理脚本使用 Cursor Agent 的 `agent` CLI；其他 Runtime 可按同一校准、分片、重试和审计流程使用自己的 Agent 执行面。

家族关系：

- `jtbd-amazon-research` = 总流程 / 总导演
- `jtbd-review-runner` = 跑评论 / 补跑 / 收结果
- `jtbd-result-audit` = 审结果 / 判断可信度

## 适用场景

- 单条评论试跑，检查 prompt 是否走偏
- 小样本验证，决定要不要扩大
- 批量跑评论
- 分片重跑 / 定向重跑
- 失败尾巴串行补跑
- 把结果收成 `final_out`

## 先读什么

只读必要真源：

- 项目 `prompt` 文件
- 项目 `codebook` 文件
- 项目 `clean_reviews.csv`
- 若本轮输出要进入 Job / unmet need / opportunity / requirement card，读已安装 `jtbd-result-audit/references/job_statement_quality_gate.md`

## 关键脚本

优先用现有脚本：

- 已安装 `jtbd-review-runner/scripts/run_single_review.py`
- 已安装 `jtbd-review-runner/scripts/run_review_batch.py`
- 已安装 `jtbd-review-runner/scripts/run_review_batch_from_file.py`
- 已安装 `jtbd-review-runner/scripts/select_review_batch.py`
- 已安装 `jtbd-review-runner/scripts/review_runner_lib.py`

## 数据边界

公开包不附带真实顾客评论、私有 payload 或测试 prompt。使用者应提供自己有权处理的数据和项目级 prompt / codebook。

### 常用命令

单条试跑：

```bash
python "<installed-skill-dir>/scripts/run_single_review.py" \
  skylight15-0001 \
  --reviews-file clean_reviews.csv \
  --prompt-file llm_jtbd_prompt_v6.md \
  --codebook-file jtbd_v2_codebook.md \
  --workspace .
```

小批量运行：

```bash
python "<installed-skill-dir>/scripts/run_review_batch.py" \
  --review-ids skylight15-0001 skylight15-0002 skylight15-0003 \
  --reviews-file clean_reviews.csv \
  --prompt-file llm_jtbd_prompt_v6.md \
  --codebook-file jtbd_v2_codebook.md \
  --output-dir run_sample/out \
  --payload-dir run_sample/payloads
```

从 id 文件批量运行：

```bash
python "<installed-skill-dir>/scripts/run_review_batch_from_file.py" \
  --review-ids-file sample_ids.txt \
  --reviews-file clean_reviews.csv \
  --prompt-file llm_jtbd_prompt_v6.md \
  --codebook-file jtbd_v2_codebook.md \
  --output-dir run_sample/out \
  --summary-out run_sample/summary.json
```

## 标准工作流

### 1. 先校 prompt，再扩大

顺序固定：

1. `--dry-run`
2. 单条实跑
3. 8–20 条小样本验证
4. 只有稳定后才扩大到批量

小样本验证不只看 JSON 是否能解析，还要看 Job Statement 语义是否过门禁：

- 输出是否能还原 `Context / Main Job / Desired Outcome / Compensation Behavior / Current Solution / Verbatim`
- `Main Job` 是否仍是用户任务，而不是产品功能
- `Desired Outcome` 是否有标尺；没有就标 `待追问`
- 补偿行为是否是已发生 workaround，不是“希望产品能...”
- 一条结果是否只讲一个场景切片
- 痛点是否有情绪和后果，而不是只写现象

若 8–20 条样本中有系统性失败，先修 prompt / codebook；不要扩大批量。

### 2. 批量执行优先分片

批量大于 200 条时：

1. 先切 shard
2. 每片独立输出 `out_* / payloads_* / summary_*.json`
3. 主跑结束后，不要立刻宣告完成，必须检查：
   - 缺口条数
   - error / timeout
   - summary 是否封口

### 3. 并发策略

经验规则：

- 主跑可以分片并行
- 失败尾巴默认改成 **serial retry**

原因：

- Cursor Agent / CLI 容易在并发下争用自己的运行状态目录
- 失败尾巴串行补跑，通常比继续硬并发更稳

### 4. 不默认全量重跑

优先级：

1. 改 prompt / codebook
2. 小样本验证
3. 定向重跑高风险样本
4. 只有在用户明确要求或旧结果整体不可信时才全量重跑

### 5. 跑完不等于可用

批量执行完成后，必须交给：

- `jtbd-result-audit`

至少回答三个问题：

1. 结果是否完整
2. 结果是否有系统性边界漂移
3. 结果是否已经可信到可以进入研究分析

如果结果要进入需求卡或产品洞察，还必须回答第四个问题：Job Statement 质量门禁是否通过。未通过时，只能进入定向修订，不能直接做聚类和机会判断。

## 结果打包

推荐标准产物：

- `summary_shard*.json`
- `retry_round*.json`
- `final_out/`
- `final_summary.json`

若项目进入分析阶段，再补：

- `master.csv / master.jsonl`
- `analysis summary`
- `research brief`

## 经验性高风险模式

这类项目尤其要盯：

- `unmet_need = unclear` 被滥用
- `organized / organization` 把 `support_level` 抬高
- 极短好评被机械判成 `tool_pain`
- 高风险标签没有 `coder_note`
- 评论抱怨被直接写成产品机会，中间缺 Job Statement 证据层
- “希望 AI/产品能...”被写成用户已经采取的补偿行为
- 多个使用场景被压成一条 job，导致后续聚类失真

## 与其他 skill 的边界

如果用户要的是：

- “帮我跑评论 / 校 prompt / 补跑失败”
  - 用 `jtbd-review-runner`

- “帮我完成整个 Amazon 评论研究项目”
  - 用 `jtbd-amazon-research`

- “帮我判断这批结果是否可信”
  - 用 `jtbd-result-audit`
