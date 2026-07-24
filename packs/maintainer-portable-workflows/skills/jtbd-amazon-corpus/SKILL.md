---
name: jtbd-amazon-corpus
description: Deprecated alias. Use `jtbd-amazon-research` for the end-to-end Amazon review research workflow from CSV ingestion to quant analysis and bridge outputs.
---

# Deprecated Alias · JTBD Amazon Corpus

这个 skill 保留兼容，但正式名字已经改成：

- `jtbd-amazon-research`

关系：

- `jtbd-amazon-research`：完整研究总流程
- `jtbd-review-runner`：评论级 LLM 执行器
- `jtbd-result-audit`：结果审计器

## 现在该读什么

请直接改读：

- [jtbd-amazon-research](../jtbd-amazon-research/SKILL.md)

如果当前只需要跑评论、补跑失败、校 prompt：

- [jtbd-review-runner](../jtbd-review-runner/SKILL.md)

如果当前要判断结果是否可信：

- [jtbd-result-audit](../jtbd-result-audit/SKILL.md)

如果当前结果要进入 Job Statement、需求卡或产品机会判断，必须同时使用：

- `.cursor/skills/jtbd-result-audit/references/job_statement_quality_gate.md`
