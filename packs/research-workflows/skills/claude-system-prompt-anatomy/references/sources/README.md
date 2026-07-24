# Sources · raw source 边界说明

## raw source 完整性

**Skill 摘要自包含；raw source snapshot 不分发 —— 这是有意设计。**

本 skill 的对象是"逆向解剖**可观察的**系统提示词成品"。因此:

- **不下载/快照**原始 PDF、整本书、长视频。
- 公开包只保留下方官方 URL；使用时重新核对当前页面。
- 对真实系统提示词，**抽取设计模式与结构**，而非逐字复制专有全文或内部安全措辞（IP / 安全双重考虑；且"模式"才是可复用的部分）。

## 官方一手来源

- Anthropic system prompt release notes: <https://platform.claude.com/docs/en/release-notes/system-prompts>
- Claude prompt engineering best practices: <https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-4-best-practices>
- Claude Code best practices: <https://code.claude.com/docs/en/best-practices>
- Effective context engineering for AI agents: <https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents>
- Building effective agents: <https://www.anthropic.com/engineering/building-effective-agents>
- Writing tools for agents: <https://www.anthropic.com/engineering/writing-tools-for-agents>
- Claude character research: <https://www.anthropic.com/research/claude-character>
- Claude's Constitution: <https://www.anthropic.com/news/claudes-constitution>

## 真伪纪律（关键）

网络上流传大量"Claude 系统提示词泄露"。**默认不可信**，除非满足以下任一:

1. 能对应到 **Anthropic 官方公布页**（claude.ai 系统提示词官方文档 / release notes）；
2. 来自 **Anthropic 官方文档**（prompt engineering、tool use 等）；
3. 与当前官方产品文档和公开可观察行为一致。

不满足者，在 research 文件中标注「未核证 / 疑似伪造」，**不得作为模式来源**，至多作为"社区如何想象"的旁注。

不得以高 star、转述文章或“泄露版”仓库替代官方锚点；不得下载相关可执行文件或压缩包。
