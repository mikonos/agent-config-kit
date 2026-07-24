# AI Feature Test Add-On

Use when the feature includes LLM generation, extraction, classification, ranking, agents, prompt workflows, retrieval, or tool calls.

## Coverage

- Input variation.
- Empty or malformed input.
- Long input.
- Multilingual input.
- Ambiguous input.
- Toxic or unsafe input.
- Prompt injection.
- Retrieval missing data.
- Retrieval stale data.
- Tool call success.
- Tool call failure.
- Partial output.
- Structured output schema.
- Determinism tolerance.
- Human review / approval.
- Auditability.

## Useful TC Modules

```text
输入覆盖
输出格式
事实准确性
拒答/安全
工具调用
检索/RAG
长上下文
多轮状态
人工审核
日志与追溯
回归评测集
```

## Evaluation Guidance

- Use golden examples for deterministic behavior.
- Use rubric-based review for subjective quality.
- Add schema assertions for JSON/structured output.
- Track hallucination, omission, unsafe compliance, and formatting failure separately.

