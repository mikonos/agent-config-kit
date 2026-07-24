# Source Synthesis

本文件记录 `prompt-design` skill 的来源映射。只有在需要追溯设计依据、扩展 skill 或做审查时读取。

## 读取来源

- `kangarooking/system-prompt-skills`：完整读取 `README.md`、`README.en.md`、`OVERVIEW.md`、`INDEX.md` 和 15 个 `*/SKILL.md`。
- 本地 `huashu-nuwa`：采用「提炼 HOW they think，而不是复制 WHAT they said」的蒸馏原则。
- 本地 `andrej-karpathy-perspective` 与 `karpathy-guidelines`：采用 Software 3.0、构建即理解、锯齿状智能、March of Nines、最小复杂度、可验证目标等框架。
- Andrej Karpathy 公开材料：`Software 2.0`、`A Recipe for Training Neural Networks`、`karpathy.ai` 教育视频索引。

## system-prompt-skills 到 prompt-design 的映射

| 来源 skill | 抽取为 prompt-design 的能力 |
|---|---|
| `persona-design` | 身份、能力边界、关系框架 |
| `personality-system` | 基础身份与可插拔风格分离，防人格污染 |
| `tool-specification` | 工具定义、权限门控、发现机制、生命周期 |
| `safety-guardrails` | 多层安全防线、规则不可变、拒绝策略 |
| `memory-system` | 记忆 CRUL、类型化记忆、静默应用、敏感边界 |
| `output-formatting` | 结论先行、复杂度分级、反 AI slop、平台输出 |
| `conversation-flow` | 意图分类、澄清策略、自主度、快速通道 |
| `search-integration` | 搜索触发、多查询、源优先级、追问重新检索 |
| `citation-system` | 内联引用、来源可审计、引用保留、日期消歧 |
| `context-management` | token 预算、延迟加载、分层压缩、结构化摘要 |
| `agent-delegation` | 子代理专业化、上下文简报、不委派理解、结果验证 |
| `injection-defense` | 信任分级、外部内容无指令权、反泄露规则 |
| `voice-optimization` | 语音短句、格式降级、音频安全边界 |
| `mobile-adaptation` | 小屏长度量化、窄屏格式限制、答案优先 |
| `code-engineering` | 安全 Git 工作流、编辑前读文件、验证循环 |

## Karpathy 融合原则

### 1. Software 3.0: prompt 是自然语言程序

系统提示词不是说明书，而是运行在 LLM 上的自然语言程序。写 prompt 时要像写软件一样定义输入、输出、权限、异常和测试。

### 2. 构建即理解

不要一开始写宏大的完整 prompt。先写最小可运行骨架，跑通 happy path，再逐步加入工具、安全、记忆、引用和平台适配。

### 3. 锯齿状智能

LLM 不是均匀聪明。Prompt 要把高风险凹陷点显式包起来：模糊需求、长上下文、外部注入、工具误用、无证据断言、格式漂移。

### 4. March of Nines

一次 demo 成功只能证明 90%。可复用 prompt 必须跑多类 eval，尤其要看尾部场景：用户表达不完整、外部内容恶意、工具失败、记忆冲突、引用缺失。

### 5. Don't be a hero

不要为单一场景设计复杂抽象。能用一句规则解决，就不要设计一套框架；能用 5 条测试证明，就不要写 50 条泛化原则。

## 可继续扩展的方向

- 为 `prompt-design` 增加 `scripts/eval_prompt.py`：用固定测试集批量跑 prompt 输出并评分。
- 增加 `references/examples.md`：收录优秀 system prompt 的拆解样例，而不是原文泄露材料。
- 增加平台专项：mobile、voice、coding-agent、RAG、browser-agent 的 prompt 模板。
