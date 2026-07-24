---
name: research-gpt-self-acceptance-rubric
type: reference
status: recommended-default
applies_to: evidence-research-suite v3
created: 2026-06-13
---

# evidence-research-suite · GPT 自验验收标准

> **用途**：给 GPT / subagent 在产出 research 任一 tool 后自我验收使用。
>
> **边界**：本文件不替代 `references/verify.md`。`verify.md` 验「证据能不能追」，本文件验「研究质量、方法论边界、下游可用性」。
>
> **一句话标准**：先过硬闸，再按每个 tool 所属领域的最强大脑打分；硬闸不过，分数无效。

---

## 0. GPT 自验总规则

### 0.1 什么时候用

满足任一条件就读本文件：

- 完成任一 research tool 产出后，需要自检 / 验收。
- 主 agent 收回 subagent 的 research 报告后，需要判定可否合并。
- 用户问「这个 research 产出质量如何」「能不能信」「有没有跑偏」。
- 要比较两个 research 版本，而比较标准不能只看文件数、长度、排版。

### 0.2 必读顺序

1. `SKILL.md`：确认本轮是否真的应该触发 research。
2. `references/execution.md`：确认阶段顺序、上游锁定、跨工具日期格式。
3. `references/verify.md`：确认 triple + mechanical verify 协议。
4. 本文件：按对应 tool 的专家验收标准打分。
5. 对应 `templates/toolXX_*.md`：核对输出 shape。
6. 如涉及 v1 深化，读 `references/v1_engineering_extensions.md`。

### 0.3 GPT 自验输出格式

每次验收必须输出独立 block，禁止只写「已检查，通过」：

```markdown
## GPT 自验报告

- target_file: <被验收文件>
- tool: <toolXX-name>
- expert_lens: <本 tool 的首席验收脑>
- upstream_locked: pass / fail / not_applicable
- mechanical_verify: pass / fail / partial
- verdict: pass / conditional_pass / revise / reject
- confidence: high / medium / low

### P0 硬闸
| Gate | Result | Evidence |
|---|---|---|
| <硬闸名称> | pass/fail | <source_file + line_range 或 grep 结果> |

### 评分
| Dimension | Score | Max | Evidence | Fix if not full |
|---|---:|---:|---|---|

### 必改项
1. <若无，写 none>

### 降级声明
<哪些结论只能算 H/C/B/A 证据等级；没有 Tool 9/10 真实用户验证时，必须说明不能升级为市场真相。>
```

### 0.4 Verdict 规则

分数不能覆盖硬闸。硬闸失败，最高只能 `revise`。

| Verdict | 条件 | 允许下游怎么用 |
|---|---|---|
| `pass` | P0 全过；总分 >= 85；本 tool 方法论主分 >= 80%；无未解决 P1 | 可进入下游 tool / 结论稿 / PRD 输入 |
| `conditional_pass` | P0 全过；总分 70-84；只有可标注边界的 P1/P2 | 可作假设输入，必须带降级声明 |
| `revise` | 任一 P0 失败，或总分 50-69，或关键专家问题答不出 | 打回补证据 / 补结构 / 重跑局部 |
| `reject` | 编造证据、错阶段启动、核心 prompt 产物不存在、把假设写成事实 | 不得合并；删除或重跑 |

### 0.5 缺陷等级

| 等级 | 定义 | 处理 |
|---|---|---|
| P0 | 影响真伪、阶段、方法论身份的错误 | 立即打回；不得下游使用 |
| P1 | 影响主要结论可信度或下游决策 | 修完再 pass；可 conditional_pass |
| P2 | 影响可读性、完整性、局部可复用性 | 可列入补丁 |
| P3 | 表述、格式、轻微冗余 | 不阻断 |

---

## 1. 全局硬闸：所有 Tool 共同适用

### 1.1 机械可验证硬闸

以下任一失败 = P0：

- 文件名符合 `toolXX_<name>_<product>.md` 或对应模板要求。
- YAML 至少含 `date / type / tool / product / language / status / inputs`；模板要求 `version` 的 tool 必须有 `version`。
- 所有跨工具 inputs 使用 `[[toolXX_<name>_<product>_YYYYMMDD]]`，不得写「见 Tool 4」这种自然语言引用。
- 关键 claim、用户原话、上游结论、数据、统计、文献引用必须能给出 triple：`claim + source_file + line_range/review_id`。
- 机械抽样至少 5 条 triple，文件存在、行号存在、keyword 在范围内出现。
- 占位符不得残留 `{这里写...}`、`<...>`、`TODO`、`待补`。
- 默认语言为中文；允许英文的段落必须是模板明确允许的段落。

### 1.2 阶段顺序硬闸

以下任一失败 = P0：

- Tool 1 在 Tool 3 之前启动。
- Tool 3b 在 Tool 1 和 Tool 3 之前启动。
- Tool 6 / 7 未引用 Tool 4 锁定目标群。
- Tool 8 未承接 Tool 4 / Tool 6 / Tool 7，或在产品创新前直接空想生态。
- 上游仍是 v0.x draft，却被下游当 final 使用。
- 发现上游 v1.1 改动影响 finalist / 核心产出，却没有重跑下游。

### 1.3 证据边界硬闸

以下任一失败 = P0：

- 把 `H` 假设或方法论推断写成用户已验证事实。
- 没有真实 Tool 9 / Tool 10 用户验证，却宣称「市场已验证」「用户一定会买」。
- 用内部一致性替代外部验证。
- 用本地二手材料直接冒充一手证据。
- 用户原话没有 review_id / interview_id / line_range。

### 1.4 结论可读性硬闸

以下任一失败 = P1，严重时 P0：

- 结论文档必须独立可读，不能只有 sidecar 才看得懂。
- 关键「怎么做」不能只藏在 sidecar；可标假设，但必须出现在结论中。
- sidecar 放证据、推断过程、反证、验证设计；不负责替正文承担主结论。
- 不能漂成通用 AI assistant、通用品牌文案或泛泛用户研究语言。

### 1.5 自验时的最低命令

在本工作区执行时，用 `rtk` 包住命令：

```bash
rtk rg -n "^tool:|^inputs:|^version:" <target_file>
rtk rg -n "\\[\\[tool[0-9]+.*_[0-9]{8}\\]\\]" <target_file>
rtk rg -n "source_file:|line_range:|review_id:" <target_file>
rtk rg -n "\\{|\\}|TODO|待补|<\\.\\.\\.>" <target_file>
```

---

## 2. Tool 1 产品灵魂 · Ernest Dichter 验收标准

### 2.1 首席验收脑

**Ernest Dichter**。理由：Tool 1 的任务不是写广告语，而是从功能、身份、文化、时代语境中挖潜意识动机，凝练 product soul。

### 2.2 Dichter 必问

- 这段灵魂是否回答了「用户在害怕什么、渴望什么」，而不只是「产品能做什么」？
- 四维是否都到位：Core Problem / Sociological Frame / National Culture / Contemporary World？
- 社会参照是否是角色脚本与身份压力，而不是年龄、收入、职业标签？
- 广告语是否让用户觉得「被理解」，而不是被推销？
- 有没有伦理刹车：没有制造焦虑、心理过时或操纵式渴望？

### 2.3 P0 硬闸

- Tool 1 不能开局跑；必须引用 Tool 3 综合洞察，且通常应引用 Tool 4 / Tool 6。
- 缺四维心理分析任一维 = P0。
- 产品灵魂段像功能卖点 / tagline 堆砌 = P1；完全没有潜意识张力 = P0。
- 广告语少于 3 条 = P0；没有情感共鸣、全是功能陈述 = P1。
- marketing-facing 段落被 LB 表、coverage matrix、Bull's Eye 等 v1 深化打断 = P1。
- 没有反触发 / 情感雷区声明，且产品涉及 AI、家庭、隐私、自主权 = P1。

### 2.4 100 分评分

| 维度 | 分值 | 满分标准 |
|---|---:|---|
| 上游锁定与 trace | 15 | Tool 3 / 4 / 6 inputs 带日期；关键灵魂句能回指上游证据 |
| 四维心理分析 | 20 | 四维完整，且每维都写出具体张力，不是通用文化套话 |
| 潜意识动机综合 | 15 | 安全、尊重、归属、自我价值、逃离等动机有取舍，有证据 |
| 产品灵魂段 | 25 | 150-250 字，一口气读完，有「害怕 X -> 走向 Y」的核心张力 |
| 广告语与内心独白 | 15 | >=3 条广告语；主视角内心独白有具体场景和第一人称 |
| 边界与伦理 | 10 | 明确不做什么，避免操纵、夺权、制造焦虑 |

### 2.5 打回信号

- 「让生活更高效 / 更智能 / 更安心」这类泛句占主导。
- National Culture 写成「中国人重视家庭」这类空话。
- 用户内心独白没有具体早晨 / 夜晚 / 周末 / 冲突场景。
- Slogan 可以替换到任何产品上仍成立。

---

## 3. Tool 2 JAS 行为调查 · C. David Jenkins 验收标准

### 3.1 首席验收脑

**C. David Jenkins**。理由：Tool 2 借用 Jenkins Activity Survey 的核心遗产：把行为倾向拆成可测 sub-scale，而不是给人贴人格标签。

辅助验收脑：**Lee Cronbach**，负责内部一致性和量表可靠性。

### 3.2 Jenkins 必问

- SI / JI / HDC 是否是三个可区分的行为倾向，而不是同义重复？
- 题目是否测「购买决策或使用场景里的行为倾向」，不是医学 Type A 诊断？
- 每个维度是否至少 5 题，且每题只测一个东西？
- Likert 5 点是否逐题可用，且含中立选项？
- 是否避免把高分用户标签化为「急躁型人格 / 危险人格」？

### 3.3 P0 硬闸

- 缺 SI / JI / HDC 任一维 = P0。
- 任一维少于 5 题 = P0。
- 没有 Likert 5 点标准，或改成开放题 = P0。
- 输出医学 / 临床诊断含义 = P0。
- 把 JAS 当主分群依据，而不是辅助分群变量 = P1。

### 3.4 100 分评分

| 维度 | 分值 | 满分标准 |
|---|---:|---|
| 三维结构 | 20 | SI/JI/HDC 定义清楚，题项不串维 |
| 题项质量 | 25 | 每题单一含义、无双重问题、无诱导、贴合产品决策行为 |
| 量尺与计分 | 20 | Likert 5 点完整；说明每维求和、阈值与后续信效度路径 |
| 反偏差设计 | 15 | 每维建议至少 1 条反向题或说明未设置原因 |
| 边界声明 | 10 | 明确非临床筛查、非人格标签、非 ODI outcome metric |
| 可分析性 | 10 | 题号清楚，能直接导入问卷系统和统计表 |

### 3.5 打回信号

- 所有题都在问「你是否希望产品更快」。
- JI 写成「你是否喜欢工作」，没有产品相关决策情境。
- HDC 变成虚荣心判断，无法映射到购买/使用行为。
- 计分说明只有「分数越高越明显」，没有后续用途。

---

## 4. Tool 3 四镜深度洞察 · Bob Moesta 主验收，Dichter/Klement/Glaser 辅验收

### 4.1 首席验收脑

**Bob Moesta**。理由：Tool 3 的价值在于从行为、补偿行为、绕道方案中找到真实需求，不是摘要文本。

辅助验收脑：

- Patterns：**Glaser & Strauss**，看 constant comparison 是否成立。
- Contradictions：**Ernest Dichter**，看理性化与潜意识冲突。
- Feelings：**Alan Klement**，看 progress tension 与情绪能量。
- Shortcuts：**Bob Moesta / Daniel Kahneman**，看 workaround 与省力倾向。

### 4.2 四镜必问

- Patterns：重复行为是否跨多个独立样本出现，还是只是一条评论？
- Contradictions：是否指出「说 A / 做 B」的证据对照？
- Feelings：情绪判断是否来自原文语言信号，而不是分析师投射？
- Shortcuts：是否识别了用户已经在用的 workaround？
- Raw voice 是否先被还原成 Job Statement，而不是从评论抱怨直接跳洞察？
- Synthesis：是否整合四镜形成一个机会空间，而不是四段摘要拼接？

### 4.3 P0 硬闸

- 把 Tool 3 写成用户评论摘要 = P0。
- 四镜缺任一镜，且没有解释该镜在材料中弱 = P0。
- 没有 Synthesis Insight = P0。
- 没有原始访谈 / 评论来源，或来源只写「用户反馈」 = P0。
- 输入含访谈/评论/反馈但没有 Job Statement 证据层 = P0。
- 创新输出与四镜没有 trace = P1。

### 4.4 100 分评分

| 维度 | 分值 | 满分标准 |
|---|---:|---|
| 原始语料 trace | 20 | 关键发现能回到访谈/评论原文、review_id 或 line_range |
| 四镜完整性 | 20 | 四镜各有行为/抱怨/张力/启示，弱镜明确说明原因 |
| 隐藏结构深度 | 25 | 发现的是结构性张力、矛盾、补偿、捷径，不是表层总结 |
| 综合洞察 | 20 | 一段高浓度 insight 能指导 Tool 1 / Tool 3b |
| 设计启示边界 | 10 | 设计启示是方向，不伪装成 PRD 或确定功能 |
| 语言与可读性 | 5 | 中文、清楚、有编号，能被下游引用 |

### 4.5 打回信号

- 每段都以「用户希望」「用户觉得」开头。
- 没有任何「但」「然而」「嘴上/实际上」「绕开」。
- Feelings 全靠形容词，没有原文触发句。
- Synthesis 是「用户需要更方便的产品」这类空洞句。

---

## 5. Tool 3b 创新输出 · Steve Jobs 主验收，Dichter 守灵魂

### 5.1 首席验收脑

**Steve Jobs**。理由：Tool 3b 的任务是从洞察和灵魂中提出能成形的 hero concept，而不是功能列表。Jobs 视角检查「是否有一个清晰、完整、能被用户感知的产品概念」。

辅助验收脑：**Ernest Dichter**，确保 hero concept 承载产品灵魂，不只是聪明功能。

### 5.2 Jobs 必问

- Hero concept 是否一句话就能被人想象，而不是一堆功能？
- 新形态 / 新功能 / 新场景是否都服务同一个心理 why？
- 这个概念是否能说清「为什么既有方案做不到」？
- 它是否简化了用户生活，还是把复杂性换了个界面重新丢给用户？
- 如果上线 N 天没兑现，失败指标是什么？

### 5.3 P0 硬闸

- Tool 3b 未引用 Tool 3 综合洞察和 Tool 1 产品灵魂 = P0。
- 重复四镜分析，而不是只输出创新段 = P1。
- 没有 hero concept = P0。
- 没有心理 why = P0。
- 没有 3-5 条反触发声明，且产品涉及 AI / 家庭 / 隐私 / 自动化 = P1。
- 没有 Verifiable Acceptance Criteria = P1；hero 完全不可验 = P0。

### 5.4 100 分评分

| 维度 | 分值 | 满分标准 |
|---|---:|---|
| 上游锚定 | 20 | 每个核心创新都回指 Tool 3 lens 或 Tool 1 灵魂 |
| 概念聚焦 | 20 | hero concept 清晰、单一、有产品形态，不是愿景口号 |
| 创新完整度 | 20 | forms/features/scenarios/rituals 四类覆盖且互相一致 |
| 差异与边界 | 15 | 说明与既有方案差距；不越成 PRD、roadmap 或商业承诺 |
| 反触发 | 15 | 明确不做什么，并能回到 Tool 6 anxiety |
| 可验证指标 | 10 | >=3 个 metric，有 target、fail threshold、measurement method |

### 5.5 打回信号

- Hero concept 名字很好听，但看不出用户怎么用。
- 功能列表可以直接塞进任何智能助手产品。
- 指标是「用户满意度提升」但没有测量方法。
- 反触发只写价值观，不写具体设计规则。

---

## 6. Tool 4 目标用户识别 · Christensen 主验收，Moesta 横切验证

### 6.1 首席验收脑

**Clayton Christensen**。理由：Tool 4 是 Job Performer 分群，核心是用户在什么情境下 hire 产品来取得进展，而不是 persona 或人口标签。

辅助验收脑：**Bob Moesta**，验证这些群是否有不同切换触发、焦虑、惯性和替代方案。

### 6.2 Christensen 必问

- 分群是否按 job / pain / desired progress，而不是年龄、职业、城市？
- X/Y 轴是否是同一属性的两端对立？
- 每群是否有独特需求和痛点，不与其他群重叠？
- 每群是否能说清为什么 hire 本产品，而不是只是「可能会用」？
- 是否把多个情境群塌缩成一个大 persona？

### 6.3 P0 硬闸

- 用人口、地理、职业作主分群 = P0。
- 没有 X/Y 轴，或轴不是对立属性 = P0。
- 群体之间需求/痛点高度重叠 = P1；重叠到无法互斥 = P0。
- 没有每群「为什么 hire 本产品」 = P1。
- 对家庭 / 多角色产品，把所有人写成一个目标用户 = P1。

### 6.4 100 分评分

| 维度 | 分值 | 满分标准 |
|---|---:|---|
| JTBD 分群基础 | 25 | 群体由 job/pain/progress 定义，不由 demographic 定义 |
| MECE 轴设计 | 20 | X/Y 轴各自为同一属性两端，覆盖且互斥 |
| 群体卡质量 | 25 | 每群有名称、需求、痛点、hire reason、边界 |
| 切换验证线索 | 10 | 每群有可能触发购买/切换的事件或 Moesta 四力线索 |
| 下游可用性 | 10 | Tool 6/7 可直接引用某一群，不需重写人群 |
| 证据边界 | 10 | 明确哪些群是证据强、哪些是 theory-strong/evidence-weak |

### 6.5 打回信号

- 群名是「年轻妈妈 / 高收入家庭 / 一线城市用户」。
- X 轴写「价格敏感」，Y 轴写「功能复杂度」，但群体描述仍按角色写。
- 每群痛点都写「时间不够、信息太多」。
- 没有说明群与群之间怎么判别。

---

## 7. Tool 5 文献阅读 · John Ioannidis 主验收，Feynman 查可解释性

### 7.1 首席验收脑

**John Ioannidis**。理由：Tool 5 要验论文证据质量，最危险的错误是把论文结论当成可靠事实，忽略样本、方法、偏差和可重复性。

辅助验收脑：**Richard Feynman**，检查是否真的能用简单语言解释论文，而不是复述术语。

### 7.2 Ioannidis 必问

- 论文回答的研究问题是什么，还是只是在讲主题？
- 样本、方法、统计分析是否足以支持结论？
- 论文自己承认了哪些 limitation？
- 结论能否推广到本产品场景？不能推广的边界是什么？
- 这篇论文提供的是 A/B/C/H 哪一级证据？

### 7.3 P0 硬闸

- 没有读论文全文或 PDF，仅凭标题/摘要生成 = P0。
- 11 段标准分析缺关键段 = P0。
- 没有研究方法、样本量、分析方法 = P0。
- 把论文结论直接写成产品事实 = P0。
- 没有 limitations / future work = P1。

### 7.4 100 分评分

| 维度 | 分值 | 满分标准 |
|---|---:|---|
| 11 段完整性 | 20 | 背景、目标、假设、框架、方法、图表、分析、结论、局限、参考、评价齐 |
| 方法与统计理解 | 25 | 样本、设计、变量、分析方法、显著性/效应量被正确解释 |
| 证据质量判断 | 20 | 科学性、创新性、学术严谨度有证据，不是好坏空评 |
| 局限与外推边界 | 15 | 清楚说明不能证明什么，不能迁移到哪里 |
| 产品启示 | 10 | 只给可证伪假设或变量启发，不直接拍板决策 |
| Feynman 可解释性 | 10 | 普通产品经理能读懂，不靠术语遮蔽 |

### 7.5 打回信号

- 「该研究证明了用户一定会...」。
- 只列结论，不解释研究如何得出结论。
- 图表段写「图表显示...」但没有拆图。
- 参考文献段只复制标题。

---

## 8. Tool 6 情感与社交需求 · Alan Klement 主验收，Dichter/Eve Rodsky 辅验收

### 8.1 首席验收脑

**Alan Klement**。理由：Tool 6 的核心是 Jobs-as-Progress：人在某个情境中想从当前状态前进到更好的自我状态，同时避开情感焦虑和身份风险。

辅助验收脑：

- **Ernest Dichter**：检查潜意识希望与恐惧。
- **Eve Rodsky**：家庭 / invisible labor 场景下检查责任、默认管理者和公平感。

### 8.2 Klement 必问

- 每条 emotional job 是否写出 `feel / avoid feeling` 的情绪进展？
- 每条 social job 是否写出 `appear as / avoid appearing as` 的观察者与身份压力？
- 是否从用户处境出发，而不是从产品抓手出发？
- 是否回指 Job Statement 的 `Context / Pains / Verbatim`，而不是只从产品概念推演？
- 反向 anxiety 类是否被单独拆出来，而不是与正向需求混表？
- 是否能交接给 Tool 1 的灵魂、Tool 7 的边界、Tool 9/10 的验证问题？

### 8.3 P0 硬闸

- Emotional Jobs 不以 `feel` / `avoid feeling` 起手 = P0。
- Social Jobs 不以 `appear as` / `avoid appearing as` 起手 = P0。
- 输入含访谈/评论/反馈但没有 Job Statement id 或原话支撑 = P0。
- 数量明显不足，无法覆盖 10-15 个情感 + 10-15 个社交需求，且无关闭理由 = P1。
- 把功能需求写进 Tool 6 主体 = P1。
- 家庭 / AI / 隐私场景没有 anxiety 类或反触发线索 = P1。

### 8.4 100 分评分

| 维度 | 分值 | 满分标准 |
|---|---:|---|
| 格式硬约定 | 20 | feel/avoid feeling 与 appear as/avoid appearing as 全部合规 |
| 用户处境 | 20 | 每条需求有具体情境，不是抽象情绪词 |
| 情感张力 | 20 | 正向愿望与反向恐惧成对出现，有 progress tension |
| 社交观察者 | 15 | 社交需求写出「被谁看见 / 被谁评价」 |
| 反向需求处理 | 15 | anxiety 类有「怕什么 / 什么会加重 / 怎么化解」 |
| 下游交接 | 10 | 可直接喂 Tool 1 / 7 / 9 / 10 |

### 8.5 打回信号

- 全部是「feel relaxed / feel confident」这类泛情绪。
- 社交需求写「appear as successful」，但不知道在谁面前。
- 只写抓手，不写她怕什么。
- 关键怎么做只藏在 sidecar。

---

## 9. Tool 7 功能需求 · Alan Klement 主验收，Tony Ulwick 查 outcome

### 9.1 首席验收脑

**Alan Klement**。理由：Tool 7 用 `When I... I hope... so that...`，本质是 Job Story：情境触发优先，不是 persona 优先。

辅助验收脑：**Tony Ulwick**，检查 functional job 是否能转成可衡量 outcome，而不是功能想法。

### 9.2 Klement 必问

- 每条是否从具体情境 `When I` 开始？
- `I hope` 是用户想取得的进展，还是产品功能名？
- `so that` 是否写出结果，而不是重复前半句？
- 是否回指 Job Statement 的 `Main Job / Desired Outcome / Compensation Behavior`？
- 每条是否只包含一个任务，没有「和 / 以及 / 同时」合并？
- 是否脱离已有竞品功能清单，回到生活/工作流？

### 9.3 P0 硬闸

- 大量条目不符合 `When I... I hope... so that...` = P0。
- 没有引用 Tool 4 目标用户 = P0。
- 输入含访谈/评论/反馈但没有 Job Statement 证据层 = P0。
- 把 PRD 功能列表当 functional jobs = P1；全篇如此 = P0。
- 每条合并多个任务 = P1。
- 没有说明不被既有产品边界限定 = P2。

### 9.4 100 分评分

| 维度 | 分值 | 满分标准 |
|---|---:|---|
| Job Story 格式 | 20 | 每条三段完整，情境-期望-结果因果链清楚 |
| 单任务原则 | 15 | 每条只做一件事，不用连词合并 |
| Functional 纯度 | 20 | 写任务/结果，不写按钮、页面、AI 功能名 |
| 用户处境 | 15 | 来自 Tool 4 群体的真实生活/工作场景 |
| Outcome 可测性 | 15 | 可转成成功/失败指标或 Tool 10 量化项；不能衡量的标 `待追问` |
| 边界与创新输入 | 15 | 有「方向 + 抓手 + 边界」，并标出非既有功能的 job |

### 9.5 打回信号

- 「When I use the app, I hope AI can...」占多数。
- `so that` 只写「更方便」。
- 一条需求同时包含提醒、沟通、下单、付款。
- 所有需求都能从竞品 feature list 直接抄出。

---

## 10. Tool 8 产品生态 · Ron Adner 主验收，Tony Ulwick 查旅程覆盖

### 10.1 首席验收脑

**Ron Adner**。理由：Tool 8 是生态设计，关键不是列周边产品，而是识别参与方、互补关系、依赖顺序和用户体验闭环。

辅助验收脑：**Tony Ulwick**，检查 JTBD 四维与 8 阶段旅程覆盖。

### 10.2 Adner 必问

- Co-creation 与 Collaborative 是否真的不同，而不是同一张清单换标题？
- 每个生态项是否有明确第三方 / 接口 / 协议 / 互补角色？
- 生态是否降低用户复杂度，还是增加整合负担？
- 是否覆盖 Define -> Conclude 的关键旅程段？
- 是否说明哪些生态项是现在做、以后做、合作做，而不是全都堆进 V1？

### 10.3 P0 硬闸

- 未区分 Co-creation 与 Collaborative = P0。
- 没有引用 Tool 4 / 6 / 7 = P1；完全空想生态 = P0。
- 每个生态项没有解决的需求/痛点 = P1。
- 没有 JTBD x 8 阶段覆盖矩阵 = P1。
- 写成技术架构或 BD 合同计划 = P1。

### 10.4 100 分评分

| 维度 | 分值 | 满分标准 |
|---|---:|---|
| 两层生态区分 | 20 | 共创=开放平台/第三方贡献；协作=互联互通/降低复杂度 |
| 用户需求映射 | 20 | 每项都回到 Tool 6/7 的需求或痛点 |
| 旅程覆盖 | 20 | Define/Locate/Prepare/Confirm/Execute/Monitor/Modify/Conclude 有覆盖解释 |
| 互补方与依赖 | 15 | 参与方、接口、协议、依赖关系说清楚 |
| 产品边界 | 15 | 生态候选不是 V1 全量承诺，有阶段和可行性边界 |
| 可读性 | 10 | 表格清楚，PM 可直接判断优先级与风险 |

### 10.5 打回信号

- 清单里全是「智能日历、智能冰箱、智能音箱」但不知道为什么。
- Co-creation 写第三方，Collaborative 也写第三方，没有体验差异。
- 生态让用户多装 5 个 app，却声称降低复杂度。
- 8 阶段矩阵大面积空白。

---

## 11. Tool 9 访谈问题设计 · Steve Portigal 主验收，Indi Young/Ochs/Moesta 条件介入

### 11.1 首席验收脑

**Steve Portigal**。理由：Tool 9 是访谈题库设计，最关键的是问题能否让受访者讲出真实经历，而不是让研究者听到想听的答案。

条件验收脑：

- **Indi Young**：mental model / listening session。
- **Elinor Ochs**：家庭场景、多人互动、现场观察。
- **Bob Moesta**：购买、切换、流失、替代方案。

### 11.2 Portigal 必问

- 问题是否让人回忆具体事件，而不是发表态度？
- 是否中立，不暗示「我们这个功能很好」？
- 是否每题只问一件事？
- 是否有递进，从低敏感到高敏感，从事实到隐喻？
- 20 类问题是否全覆盖，且每类 3-5 题？

### 11.3 P0 硬闸

- 20 类问题缺漏，且无明确裁剪理由 = P0。
- 每类少于 3 题，且无关闭理由 = P1。
- 大量 leading questions = P0。
- 把访谈题写成问卷封闭题 = P1。
- 没有 Aided Recall，全部问「你一般 / 你觉得」= P1。

### 11.4 100 分评分

| 维度 | 分值 | 满分标准 |
|---|---:|---|
| 20 类覆盖 | 20 | Background -> Comparative 一类不漏，每类意图清楚 |
| 问题质量五原则 | 25 | 清晰、儿童友好、辅助回忆、简洁、中立 |
| 访谈递进 | 15 | 有执行排序，敏感/隐性题放在信任建立之后 |
| 事件追问能力 | 20 | 多数问题能拉回「上一次具体发生」 |
| 研究目标贴合 | 10 | 每类问题都服务本次产品设想和受访群 |
| 边界 | 10 | 不伪装成切换访谈、问卷或验证结论 |

### 11.5 打回信号

- 「你觉得我们的产品是否有帮助？」。
- 「你一般怎么安排家庭事务？」没有追最近一次。
- 每类问题看起来可以用于任何产品。
- Hypothetical questions 被当成结论来源。

---

## 12. Tool 10 问卷设计 · Don Dillman 主验收，Cronbach/Campbell-Fiske 查信效度

### 12.1 首席验收脑

**Don Dillman**。理由：Tool 10 是定量问卷，关键是降低被试成本、提升回答质量，并让数据可分析。

辅助验收脑：

- **Rensis Likert**：量尺设计。
- **Lee Cronbach**：内部一致性。
- **Campbell & Fiske**：区分效度 / 构念效度。

### 12.2 Dillman 必问

- 全部题目是否封闭式，能量化？
- 每个创新概念下是否覆盖 Knowledge / Evaluation / Behavioral / Frequency / Psychological？
- 每个 construct 是否至少 3 题，避免单题谬误？
- 是否避免双重问题、诱导问题、开放题？
- 是否有反向题 / 匿名性 / 顺序设计来防社会赞许偏差？

### 12.3 P0 硬闸

- 出现开放题 = P0，除非明确标为非 Tool 10 附录且不进入量化问卷。
- 未覆盖五大题型 = P0。
- 没有五项 Standards 对照 = P1。
- 问卷无法量化或无法导出分析 = P0。
- 把 Tool 10 当访谈题库 = P0。

### 12.4 100 分评分

| 维度 | 分值 | 满分标准 |
|---|---:|---|
| 封闭式与可量化 | 20 | 全部单选 / Likert / 频率量尺，无开放题 |
| 五题型覆盖 | 20 | 每个创新概念都有 Knowledge/Evaluation/Behavioral/Frequency/Psychology |
| 心理测量质量 | 25 | construct 清楚；每个 sub-scale 3-5 题；有反向题和避免双重问题 |
| 五项效度 | 15 | Factorial/Content/Discriminant/Predictive/Construct 有题号证据 |
| 问卷体验 | 10 | <=10 分钟；顺序从低敏到高敏；语言友好 |
| 验证计划 | 10 | 有 pilot 5-10 人、题项耗时、天花板/地板效应检查 |

### 12.5 打回信号

- 「请描述你为什么喜欢这个概念」出现在主问卷。
- 一题问「这个功能是否方便且安全」。
- 五项效度表只写「已满足」。
- 心理题全部正向，没有反向题或第三方措辞。

---

## 13. 跨 Tool 套件级验收

### 13.1 完整研究包必须回答的问题

一套 research 研究包至少要能回答：

1. 目标用户不是一个人，而是哪几类情境群？
2. 每类用户在什么处境里痛？
3. 她想取得什么 functional / emotional / social progress？
4. 哪些需求是正向 demand，哪些是反向 anxiety？
5. 哪个洞察最能凝成产品灵魂？
6. 哪个 hero concept 最能承载灵魂？
7. 哪些生态项只是候选，哪些是用户旅程闭环的必要条件？
8. 哪些判断已有证据，哪些只是 H 假设？
9. 下一步该用 Tool 9 问什么、Tool 10 量化什么？
10. 若最关键假设被推翻，哪些结论必须作废？

### 13.2 套件级 P0

- 工具都跑完了，但上游/下游没有引用关系。
- 每个 tool 都自洽，但合起来无法形成产品判断。
- 没有 `_evidence_ledger.md` 或等价证据台账，导致关键 claim 找不到源头。
- 没有结论稿 + sidecar 分层，读者只能从长推理里找结论。
- 没有下一步验证路径，却把结论交给 PRD。

### 13.3 Evidence Grade 规则

| 等级 | 定义 | 可做什么 | 不可做什么 |
|---|---|---|---|
| A | 一手访谈 / 真实用户行为 / 可验证原始数据 | 可支撑强产品判断 | 仍需说明样本边界 |
| B | 高质量二手数据 / 竞品评论 / 官方统计 | 可支撑机会方向 | 不可直接证明购买意愿 |
| C | 方法论推断 / 跨材料综合 | 可生成假设 | 不可当事实引用 |
| H | 尚未验证的假设 | 可进 Tool 9/10 验证 | 不可进入确定 PRD |

没有 Tool 9/10 真实用户验证时，整包最多是「高质量假设包」，不能叫「市场真相」。

### 13.4 GPT 自验的最后一句

每次自验最后必须写：

```markdown
本产出当前可用于：<概念探索 / 访谈准备 / 问卷准备 / PRD 输入 / GTM 假设 / 不可下游使用>
本产出当前不可用于：<不能用于什么>
下一步最小验证动作：<一条 Tool 9 或 Tool 10 可执行动作>
```
