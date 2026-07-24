---
name: claude-system-prompt-anatomy
description: |
  逆向解剖**真实可观察的** Claude / Anthropic 系统提示词成品模式（描述性，非方法论）。
  回答三类问题:Anthropic 实际怎么写系统提示词?这份"泄露的 Claude 提示词"是真是假?怎么按真实成品模式审我自己的 system prompt?
  适用于:想看 Claude 系统提示词长什么样、判断一份泄露真伪、按官方成品模式审查自己的 system prompt / agent instructions、理解"人格在训练还是在提示词"。
  触发词:claude 系统提示词、claude.ai system prompt、Claude Code 提示词、Anthropic 怎么写提示词、这份泄露是真的吗、系统提示词逆向、do X not Y、dispositions over rules、强调词/CRITICAL/MUST 该不该用、拒答怎么写、Amanda Askell、Constitutional AI 与提示词。
  不适用于:从零学"该怎么写 prompt"的通用方法论（→ prompt-design）;纯 API 参数/后端实现;一次性文案润色;非 Claude 厂商的提示词。
  与 prompt-design 分流:想知道"我该怎么写"→ prompt-design（规范方法论）;想知道"Anthropic 实际怎么写的 / 这份是不是真的"→ 本 skill（描述性成品 + 真伪守门）。两者互补,不重叠。
tags: [system-prompt, prompt-engineering, claude, reverse-engineering, prompt-audit]
related_skills: [prompt-design, nuwa-skill]
---

# Claude System Prompt Anatomy

> **时效边界**：这是截至 2026-06-29 的公开研究快照。回答当前产品行为、模型版本或平台规则前，必须重新核对 `references/sources/README.md` 中的 Anthropic 官方来源。不得尝试提取、绕过或披露隐藏系统提示词。

## 这个 skill 是什么

它是一张**已核证的 Claude 系统提示词解剖图**,不是"怎么写 prompt"的教程。

来源限于可回溯的 Anthropic 官方系统提示词公布页、官方文档/博客与公开可观察产品行为。网络上流传的"泄露完整提示词"**默认不进正文**——本 skill 自带一套真伪守门,见 §真伪纪律。

凡本文给出的"官方样例"句式,均为 Anthropic 官方文档里逐字可见的文本,可直接借鉴。

## 何时用本 skill,何时用 prompt-design

| 你的问题 | 用哪个 |
|---|---|
| "我该怎么写一个稳定的 system prompt?" | `prompt-design`（规范方法论:七层骨架、eval 集） |
| "Anthropic **实际**是怎么写的?有哪些可抄的成品句式?" | **本 skill** |
| "这份网上的 Claude 系统提示词是真的吗?" | **本 skill**（§真伪纪律） |
| "帮我按 Claude 的真实做法审一下我这段提示词" | **本 skill**（§审查清单） |

## 调用工作流

收到任务后先归类,再走对应路径:

| 模式 | 触发 | 做什么 |
|---|---|---|
| **A 解剖** | "Claude 提示词怎么写的""有哪些模式" | 用 §设计哲学 + §成品模式库 回答,引官方证据 |
| **B 审查** | "审我这段提示词""这样写行不行" | 用 §审查清单 逐条过,给可判定的修改建议 |
| **C 真伪** | "这份泄露是真的吗""这段是官方的吗" | 用 §真伪纪律 三锚点法判定,不确定就标"未核证" |

任何模式下,区分"官方一手 / 可信二手 / 我的推断",不把推断说成事实。

---

## 一、设计哲学层(为什么这样写)

理解这三条,才看得懂提示词里每句话的"层归属"。

### 哲学 1 · 写的是性情,不是规则(dispositions over rules)

Anthropic 跨文档明说:与其给 Claude 穷举硬规则,不如训练好价值与判断,再让它在情境里裁量。

> 官方一手(《Claude's Constitution》):"We generally favor cultivating good values and judgment over strict rules and decision procedures, and we try to explain any rules we do want Claude to follow."

含义:线上系统提示词里很多句子是**倾向性描述**而非 if-then 硬规则。硬规则那一层尽量沉进训练,运行时文本只放"当下情境微调 + 少数必须显式的约束"。

### 哲学 2 · 人格在权重,提示词在运行时(两层分工)— 解剖的命门

| | 承担什么 | 怎么进去 |
|---|---|---|
| **训练 / character** | 人格、价值倾向(诚实、善意解读、不谄媚、brilliant-friend 语气) | 经 Constitutional AI 的 character 变体训练**注入权重**(Soul Doc + Askell 确认用于 supervised learning) |
| **系统提示词** | 动态事实(日期)、产品差异、修补训练没压住的当下行为 | TDD 写出来的**可快改薄层**,官方明说"不适用 API、非定稿" |

> 官方一手(Askell):"The boring yet crucial secret behind good system prompts is test-driven development. You don't write down a system prompt and find ways to test it. You write down tests and find a system prompt that passes them."

**解剖判据**:看到提示词里某句,先判它属哪层——
- 动态事实(日期/产品名/可用工具)→ 必在提示词层(训练不知运行时事实)
- 产品差异/合规(claude.ai 专属、copyright、引用格式)→ 提示词层(API 没有)
- 人格/价值倾向(诚实、开放、不谄媚)→ 主要是训练层的"回声";出现在提示词里通常是**强化**而非首次注入
- 措辞像 if-then 硬规则、在压一个具体坏行为 → TDD 补丁,提示词层

### 哲学 3 · 系统提示词是 production code

改一句要 per-model eval + 逐行 ablation + soak period,不是随手编辑。

> 官方一手(2026-04 postmortem):Anthropic 给 Claude Code 提示词加了 verbosity 限制(≤25/≤100 词),更广 eval 显示 Opus 4.6/4.7 各掉 3%,于 2026-04-20 紧急回滚。

含义:**别凭感觉改系统提示词,改完要有 eval 证据**。这条也是 §反模式 里"砍 verbosity 伤推理"的出处。

---

## 二、成品模式库(怎么写)

七个核心模式,每个标了证据强度(稳定 = ≥2 处独立来源复现)。

### P1 · 分层与 provenance(稳定)

真实运行时提示词不是一整块,而是**按来源分层、每层信任级别不同**:

| 层 | 作者 | 信任级别 |
|---|---|---|
| harness 层 | Anthropic | 系统级运行时机制 |
| identity / 行为层 | Anthropic | 人格与行为(claude.ai)/ 身份(Claude Code) |
| 项目层(CLAUDE.md) | 用户 | 覆盖默认行为 |
| 动态上下文(注入) | harness | **降级为数据,非指令** |

要点:注入内容(`<system-reminder>`、检索结果、记忆、工具输出)显式标注来源并降级——"它是数据,不是命令"。同一个 Claude 有**多套**提示词:claude.ai(人格/安全)、API(默认无系统提示词)、Claude Code(harness + 工具)。

### P2 · "do X, not don't-Y" + 正例优先(官方列为格式控制第一法则)

官方把这条列为格式控制的第一法则。给正向指令,别只给负向禁止。

> 官方样例(可逐字借鉴):
> - 不要写:`Do not use markdown in your response`
> - 改写成:`Your response should be composed of smoothly flowing prose paragraphs.`

> 官方一手:"Positive examples ... tend to be more effective than negative examples or instructions that tell the model what not to do."

### P3 · 约束可判定(官方一手 + 右海拔)

把模糊形容词改成**可判定的条件门 + 量化阈值 + 配套清单**。

- 枚举条件门:列表只在 "(a) asked, or (b) the content is multifaceted enough that they're essential" 时用
- 量化阈值:"Bullets are at least 1-2 sentences"
- 抽象规则配具体清单:"hard to reverse operations" 旁边附 `git push --force`、`rm -rf`

> 这就是官方说的 "right altitude"(Goldilocks):既不过硬(hardcode 脆弱逻辑),也不过软(空泛高层指导)。

### P4 · 强调词节制 · 措辞 steer ≠ 机制强制(官方一手)

官方明确建议**调低**强硬措辞,并坦承大写措辞只是 advisory。

> 官方一手:"these models may now overtrigger. The fix is to dial back any aggressive language. Where you might have said 'CRITICAL: You MUST use this tool when...', you can use more normal prompting like 'Use this tool when...'."

> 官方一手:CLAUDE.md 指令是 advisory,加 "IMPORTANT/YOU MUST" 能**提升** adherence;但 "hooks are deterministic and guarantee the action happens." 真要确定性,落到 hook,不靠措辞。

实践:全大写 `MUST`/`NEVER` 只留给极少数不可妥协处(官方实例:读文件再答、不可逆操作、安全);其余用平实祈使。**想要"保证执行"→ 用机制(hook/gate),不要靠堆强调词**(堆多了反而 over-trigger,见 §反模式)。

### P5 · 每条戒律配理由 + 不暴露内部机制(官方一手)

给指令配动机,模型更遵守、人更懂。

> 官方样例:不写 `NEVER use ellipses`,而写 `Your response will be read aloud by a text-to-speech engine, so never use ellipses since the text-to-speech engine will not know how to pronounce them.`

同时:别让模型用"我的系统提示词要求…"来解释自己(用户看不到提示词,这种话用"诉诸隐藏规则"替换了真实推理)。

### P6 · 拒答 = 善意解读 + 比例响应 + 显式阈值(官方一手)

不靠"宁可错杀"的一刀切。先做最善意的合理解读,再按比例响应,阈值写明白 + 反例压低误拒。

> 官方样例(default_stance):"Claude defaults to helping. Claude only declines a request when helping would create a concrete, specific risk of serious harm; requests that are merely edgy, hypothetical, playful, or uncomfortable do not meet that bar."

判据:上下文能反向触发拒绝——"怎么削刀"该答,"怎么削刀好杀我妹妹"该拒。

### P7 · agent 特有:验证状态机 + 风险闸 + act-don't-interview(官方 ≥3 处复现)

写 agent 提示词时,这三条复现度最高。

- **验证状态机**:`gather context → take action → verify work → repeat`;**出示证据,别断言成功**("show evidence rather than asserting success: the test output ... or a screenshot")。别让用户当验证回路。
- **风险闸**:难撤销/对外的动作先确认。官方清单:删除、`git push --force`、对外发消息。
- **act, don't interview**:细节没说全时默认先合理动手,只有"genuinely unanswerable"才追问;能用工具消解歧义就先用工具,别让用户去查。

> 官方样例(可逐字借鉴,并行工具):
> `If you intend to call multiple tools and there are no dependencies between the tool calls, make all of the independent tool calls in parallel.` + `Only batch tool calls that are independent of each other.`

需要模板时回到 `references/sources/README.md` 中的官方提示工程与 Claude Code 文档；不要从本 Skill 复刻长段专有文本。

---

## 三、决策启发式(写 / 审 / 解剖 / 真伪)

> 以下是从官方成品**反推**的借鉴点;系统性的「该怎么写」仍以 `prompt-design` 为准。

1. 写约束先问:它可判定吗?能落成 (a)/(b) 条件或量化阈值就写,不能就改写或删。
2. 想禁止某行为 → 改写成"do this instead"(正向)。
3. 想要确定性执行 → 落到 hook / gate,别靠大写措辞(措辞只提升概率)。
4. 强调词预算:全大写只留"读文件再答 / 不可逆 / 安全"少数处,其余平实。
5. 每条 instruction 配一句理由。
6. 抽象规则旁边永远附具体清单。
7. 拒答写"only when concrete, specific risk" + 反例清单。
8. agent 提示词:把验证写成能跑出 pass/fail 的东西。
9. 解剖一句提示词:先判它属"动态事实 / 产品差异 / 人格回声 / TDD 补丁"哪层。
10. 判一份"Claude 提示词"真伪:对得上官方锚点才采信,否则标"未核证"。

---

## 四、表达 DNA(Claude 提示词文本自身的风格)

描述的是**提示词文本长什么样**,不是让你扮演谁。

- 人称:claude.ai = 纯第三人称("Claude does X");Claude Code = 第二人称身份开篇 + 第三人称行为。
- 分节:语义化 XML 标签(`<lists_and_bullets>`、`<default_stance>`)或 Markdown 标题,二选一。
- 句式:祈使 + 理由从句;(a)/(b) 条件门;量化阈值;正向改写("lists read naturally as 'x, y, and z'")。
- 身份句三件套:这一代是谁 + 哪个家族 + 能力梯队定位;用 "in case the person asks" 机会式触发。
- 强调词稀疏(见 P4)。

## 五、反模式(含 Anthropic 自承的批评)

- **堆强调词 → over-trigger**(官方自承:新模型对系统提示词更敏感,旧的激进措辞会过度触发)。
- **过度压缩 verbosity → 伤推理**(官方 postmortem:砍到 ≤25/≤100 词,掉 3%,回滚)。
- **over-refusal / 过度啰嗦**(研究证实,但**跨厂商通病,非 Claude 独有**,诚实标注)。
- **把 advisory 当 guarantee**:以为写了大写就一定执行(见 P4)。
- **测一次 demo 就上线**:系统提示词是 production code,缺 eval = 裸奔。
- **身份膨胀**:开篇塞世界观长篇(官方成品恰恰极克制;弱印证,方向一致)。

## 六、真伪纪律(本 skill 的守门职责)

网上大量"Claude 系统提示词泄露"。**默认不可信**,除非对得上以下至少一个锚点:

1. Anthropic 官方 `release-notes/system-prompts` 页(claude.ai 提示词,带日期版本)
2. Anthropic 官方一手(文档 / 博客 / Amanda Askell 公开解读)
3. 当前 Anthropic 官方文档和公开可观察产品行为；隐藏运行时提示词不作为提取目标

甄别要点:
- **官方公布版省略了全部工具描述**(search/artifacts/copyright)。所以"含完整工具 schema 的版本"必然来自泄露——这是区分官方 vs 泄露的最可靠刀口(Simon Willison)。
- 长度矛盾不等于互相证伪:消费端纯人格版 ~3K tokens,含全部工具的"完整版" ~27K——测的是**不同的层**。
- 高 star / 流传广 ≠ 真实。Pliny 的 27K"完整版"、134K star 工具仓库 = 未核证,至多标"社区如何想象 Claude 提示词"。
- **安全铁律:不下载任何"泄露源码/提示词"压缩包或可执行档**(已确证有投毒仓库植入 stealer 恶意软件)。只读网页文本。

判定输出三档:✅ 可印证(对上锚点)/ 🟡 部分(官方+泄露混合,需切分)/ ❌ 未核证(隔离,不进正文)。

## 七、审查清单(审一段 system prompt 用)

逐条过。每个"否"都给可判定的改法。

1. 约束都可判定吗(条件门/阈值),还是堆了模糊形容词?
2. 有没有把"don't Y"改成"do X"?有没有给正例?
3. 全大写强调词是不是只留在不可妥协处?其余降为平实?
4. 想要"保证执行"的地方,是靠措辞还是靠机制(hook/gate)?
5. 每条戒律配理由了吗?
6. 抽象规则旁边有具体清单吗?
7. 拒答写了显式阈值 + 反例吗,还是一刀切?
8. (agent)验证能跑出 pass/fail 吗?难撤销动作有风险闸吗?
9. 注入的外部内容被降级为"数据非指令"了吗?
10. 身份段是不是膨胀了?动态事实(日期/产品)放对层了吗?
11. 规则之间有没有自相矛盾(如「别用列表」与「始终好好排版」并存)?冲突的两条要合并或定优先级。

## 诚实边界

- 不含 Anthropic **内部流程**(草稿、A/B 数据、每句取舍的内部理由)——不公开,本 skill 只解剖**可观察成品**。
- 工具描述全文官方**从不公布**;本 skill 不采信任何"完整工具版"原文。
- claude.ai 含工具的完整 token 数官方未公布。
- 系统提示词**有保质期**:会随模型迭代过期(官方"context anxiety"案例:为某代加的补丁到下一代成纯开销)。本文模式截至 2026-06-29 的可观察版本。
- 已知缺口(调研时主动留下):Lex Fridman 访谈 Askell 逐字原话未一手取到;泄露仓库"Official"子目录未逐字 diff 官方页。
- 官方自相矛盾处(线上第三人称 vs 文档教第二人称;劝少用强调词却仍在硬约束处用)**保留,不强行统一**——矛盾本身是信息。

## 来源

公开来源与核证边界见 `references/sources/README.md`。公开包不附带内部研究日志、运行时提示词摘录或“泄露版”全文。

> 本 Skill 由主题研究流程蒸馏于 2026-06-29。配套规范方法论见 `prompt-design`。
