---
name: cursor-jtbd-review
description: Deprecated alias. Use `jtbd-review-runner` for prompt calibration, batch execution, retry, audit handoff, and result packaging for review-level JTBD analysis.
---

# Deprecated Alias · Cursor JTBD Review

这个 skill 保留兼容，但正式名字已经改成：

- `jtbd-review-runner`

关系：

- `jtbd-review-runner`：评论级执行器。负责单条试跑、批量运行、失败补跑、串行重试、审计前打包。
- `jtbd-result-audit`：结果审计器。负责分布漂移、规则违规、风险桶与可信度判断。
- `jtbd-amazon-research`：完整研究总流程。编排从 CSV 到 JobList / QuantAnalysis / Bridge Analysis 的全链路。

## 现在该读什么

请直接改读：

- [jtbd-review-runner](../jtbd-review-runner/SKILL.md)

如果用户说的是“整套 Amazon 评论研究”，改读：

- [jtbd-amazon-research](../jtbd-amazon-research/SKILL.md)

如果用户说的是“检查这批结果到底靠不靠谱”，改读：

- [jtbd-result-audit](../jtbd-result-audit/SKILL.md)
