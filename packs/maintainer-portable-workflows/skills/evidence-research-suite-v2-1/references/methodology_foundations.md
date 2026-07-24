# 方法论锚点 · research-research-suite 理论根源参考

> **这是什么**：research-research-suite skill 十个工具背后的理论根源参考。SKILL.md 主体只给每个工具的轮廓与硬约定，深层「这个工具背后的理论凭什么成立、关键术语怎么用、和哪些专家关联」由本文件兜底。
>
> **谁用 / 什么时候读**：agent 执行 research 任一工具前，如对方法论根源有疑问、要解释为什么这样设计、或要在没有对应 perspective skill 的情况下扮演某位专家（🟡 Simulated 模式），先读本文件对应段。本文件 = 🟡 Simulated 模式的 fallback anchor。
>
> **使用顺序**：先 Read SKILL.md 找到对应工具 → 如需理论支撑或专家扮演，再 Read 本文件对应章节 → 按决策启发式落地。
>
> **覆盖 6 个理论锚点**：① Dichter 品牌心理学（Tool 1） / ② Jenkins JAS 行为研究（Tool 2） / ③ 四镜消费者心理学（Tool 3） / ④ Jobs to be Done 谱系（Tool 4/6/7/8） / ⑤ 用户访谈 20 类问题（Tool 9） / ⑥ 心理测量学问卷设计（Tool 10）。

---

## 1. Dichter 品牌心理学（Tool 1 灵魂）

### 人物 / 出处

- **Ernest Dichter（1907-1991）**：奥地利-美国心理学家，「动机研究之父」（Father of Motivational Research / Mr. Mass Motivations）。
- 维也纳精神分析学派出身（受 Freud 影响），1938 年逃离纳粹后移居美国，1946 年在纽约创立 Institute for Motivational Research。
- 麦迪逊大道（Madison Avenue）黄金时代的核心顾问，被同行称为「Madison Avenue 的 Freud」、Don Draper 的现实原型之一。
- 一生主持过 2500+ 项品牌动机研究，客户涵盖 P&G、Chrysler、Esso（Exxon）、Betty Crocker、Mattel 等。

### 核心命题

- **消费者购买行为不只为功能，更为满足潜意识的希望与恐惧（subconscious hopes & fears）**。
- 产品 = 「Soul of Things」（物的灵魂）：每件产品都承载着情感、社会、文化意义；脱离这个 soul 谈卖点等于把产品当工业品。
- 广告不是介绍产品，是「表达这个时代这种人在抗拒什么、追求什么」——广告本质是社会无意识的镜子（mirror of cultural unconscious）。
- 「Permission to Enjoy」（享乐许可）：现代消费者背负清教伦理留下的享乐罪疚（pleasure guilt），品牌的工作是给消费者一个「可以享受」的道德借口。
- 「Psychological Obsolescence」（心理过时）：在功能耗损之前先让消费者感到心理上的过时，是消费经济持续增长的引擎之一（也是后世对他最大的伦理批评点）。

### 关键术语（Tool 1 用到的四维）

- **Core Problem（核心问题）**：用户在此品类下深层的心理张力是什么——不是「需要什么」，是「在害怕什么、在渴望什么」。
- **Sociological Frame（社会学框架）**：这个问题如何被所属社会阶层、家庭角色、性别脚本、职业身份所放大或抑制。
- **National Culture（国族文化）**：同一品类在中国 / 美国 / 法国 / 日本的意义为什么不同——Dichter 在 50-60 年代已大量做跨国动机研究。
- **Contemporary World（当代语境）**：此时此刻的时代精神（technology, generational shift, gender role, climate of anxiety）如何重塑这个 core problem。
- **Subconscious hopes & fears（潜意识希望与恐惧）**：所有四维向下追问的终点——找到那一对张力，品牌灵魂的提案才有锚。

### 经典文本

- *The Strategy of Desire*（1960）—— Dichter 主纲领，「desire 不是被发现的，是被组织和释放的」。
- *Handbook of Consumer Motivations*（1964）—— 几百个品类的动机字典，到今天还是营销研究底层参考书。
- *Motivating Human Behavior*（1971）—— 把动机研究从消费扩展到组织、政治、教育。
- *The Naked Manager*（1974）—— 把动机研究方法应用到管理与员工激励。
- 批评文献：Vance Packard *The Hidden Persuaders*（1957）、Betty Friedan *The Feminine Mystique*（1963）对 Dichter 把女性消费者塑造为家庭主妇角色的批评。

### 与本仓 skill 关联

- 本仓有 `dichter-perspective` skill —— **Tool 1 默认走 🟢 Grounded**：执行前先 Read `.cursor/skills/dichter-perspective/SKILL.md`。
- 双模式：默认营销/品牌顾问模式；如要做 3-4 小时 depth interview 设计可切换方法论教练模式。
- 与 Tool 3 四镜的「Contradictions」镜头协同：理性化（rationalization）诊断是 Dichter 的强项。
- 与 Tool 6 情感/社交需求协同：享乐罪疚、psychological obsolescence、permission to enjoy 是情感需求的常见底层结构。

### 决策启发式

1. **不要让用户告诉你他「为什么买」**——他给的是 post-hoc rationalization。要追问「上次买之前那一刻你在想什么 / 在抗拒什么」，让动机从场景里浮现，而不是从自评里要。
2. **四维问完先停一下找张力**——Core Problem 拆出来后，必须能在一句话里写出一对张力（希望 X 但又害怕 Y / 想成为 A 但被困在 B）。写不出来 = 还没下到潜意识层，继续追问。
3. **Sociological Frame 不是人口统计**——不是「30 岁女性」，是「30 岁有 5 岁孩子的双职工母亲被『好妈妈』脚本和『职业女性』脚本同时拉扯」。维度是角色脚本与社会期待，不是 age / income。
4. **National Culture 在中国家庭场景里要扣到具体的代际与城乡张力**——不要复述「中国人重视家庭」这种 generic 结论；要找到「这一代 80/90 后父母 vs 自己父母在育儿/家庭分工/数字化容忍度上的具体冲突点」。
5. **品牌灵魂 ≠ 卖点 ≠ slogan**——灵魂是一句话回答「我们帮用户从害怕什么里走出来，进入哪种他渴望但不敢承认的状态」。如果这句话听起来像功能宣传，回头继续挖。
6. **保留伦理刹车**：Dichter 的工具威力大，但 research 这里只用动机研究做产品方向判断，不用来做操纵式说服或心理过时的人为制造。引导消费者「理解自己想要什么」而不是「制造他没有的渴望」。

---

## 2. Jenkins Activity Survey / Type A 行为研究（Tool 2 JAS）

### 人物 / 出处

- **C. David Jenkins**（流行病学家）、**Stephen J. Zyzanski**（行为医学）、**Ray H. Rosenman**（心脏病学家）等心血管行为医学团队。
- 1960s-70s 在 Western Collaborative Group Study（WCGS）中开发，目的是用自填问卷替代 Friedman & Rosenman 的结构化访谈（SI, Structured Interview）来识别 Type A 行为。
- Jenkins Activity Survey（JAS）1965 年发布初版，1979 年由 Psychological Corporation 正式出版 manual。

### 核心命题

- **Type A 行为模式（Type A Behavior Pattern, TABP）是一个可量化的行为构造**——不是性格，不是疾病，是一组在特定情境下被诱发的、可观察、可测量的行为倾向。
- 原始目的：预测冠心病（Coronary Heart Disease, CHD）风险。后续研究证明 Type A 整体与 CHD 的因果关系比 Friedman 最初主张要弱，但其子维度（特别是 hostility）仍是稳健预测因子。
- **核心方法论遗产**：把一种「人格类型」拆成 3-4 个可独立测量的 sub-scale，每个 sub-scale 用多个 Likert / 强迫选择题构成 —— 这是行为问卷研究的范式。
- 在产品研究里被借用：把「重度用户 / 高节奏人群 / 高竞争性职业人群」从泛泛人群里量化筛出来，作为 segmentation 或 over-served / under-served 判断的辅助变量。

### 关键术语（Tool 2 改编三维）

- **SI（Speed & Impatience，速度与不耐烦）**：对等待、慢节奏、被打断的反应强度；典型题项「我经常觉得别人讲话太慢」「红灯让我烦躁」。
- **JI（Job Involvement，工作卷入度）**：工作占据精神带宽的比例；典型题项「即使在度假也常想工作」「下班后仍反复回想工作问题」。
- **HDC（Hard-Driving & Competitiveness，硬驱与竞争性）**：在不必要的场合也激起竞争；典型题项「玩游戏也要赢」「不喜欢比自己更优秀的同事」。
- 原始 JAS-Form C 还有一个 **Type A 总分**（A/B 二分），research Tool 2 不沿用总分，只用三个 sub-scale 做画像。
- **Likert 5 点**：1 = 完全不符合 / 2 = 较不符合 / 3 = 一般 / 4 = 较符合 / 5 = 完全符合。**这是 JAS 量表的标准做法**，不是产品研究自定——5 点偶数题项数与平衡反向题是心理测量学惯例。

### 经典文本

- Jenkins, C. D., Zyzanski, S. J., & Rosenman, R. H. (1979). *Jenkins Activity Survey Manual*. The Psychological Corporation.
- Rosenman, R. H., et al. (1975). "Coronary heart disease in the Western Collaborative Group Study: Final follow-up experience of 8½ years." *JAMA*.
- Friedman, M., & Rosenman, R. H. (1974). *Type A Behavior and Your Heart* —— Type A 概念的科普版起点。
- Booth-Kewley, S., & Friedman, H. S. (1987). "Psychological predictors of heart disease: A quantitative review." *Psychological Bulletin* —— 对 Type A 因果性的批判性元分析。

### 与本仓 skill 关联

- **无 dedicated skill，本文件即 🟡 Simulated fallback anchor**。
- 执行时声明：「（基于训练数据，本仓暂无 JAS / Jenkins 行为研究 skill）」，并在 `memory/skill-distillation-candidates.md` 追加一行记录（如已多次使用且产出稳定可考虑蒸馏）。
- 与 Tool 4 JTBD 协同：JAS 三维提供「行为节奏画像」，JTBD 提供「想要进展的方向画像」，两者结合可识别「高节奏 + 高情感 job」类用户群（典型如双职工父母）。
- 与 Tool 10 问卷设计协同：JAS 三维 sub-scale 可作为问卷的 segmentation 模块（不是主体，主体仍是 Tool 10 的五维问题）。

### 决策启发式

1. **三维不必都用满**——某产品场景若只与「时间压力」有关，只跑 SI 也可以；JI / HDC 在家庭场景里不一定 relevant。判断标准：这一维若高/低分对产品决策有不同含义，则保留；没有差异则删。
2. **Likert 5 点是硬约定**——不要改成 7 点或 4 点。5 点是 JAS 原始量表的设计，也是国内被试最熟悉的尺度；改尺度等于放弃可比性。
3. **反向题（reverse-coded items）要混入**——比如 SI 维度里至少放 1-2 道「我能耐心等待」类反向题，识别社会赞许偏差（social desirability bias）和直答（straight-lining）。
4. **不要拿 Type A 总分给用户贴标签**——research 用 JAS 是做行为节奏画像，不是诊断人格类型，更不是医学风险判断。输出维度分而非总分，避免标签化。
5. **JAS 是辅助分群变量，不是主分群依据**——主分群仍应基于 jobs / needs / pain points（Tool 4-7），JAS 仅在「高节奏人群 vs 低节奏人群对同一产品反应是否不同」这类问题上做对照。

---

## 3. 消费者心理学四镜（Tool 3 Four-Lens）

### 人物 / 出处

- **非单一作者，是心理学 + JTBD 实践 + 定性访谈分析传统的整合**。
- 谱系来源：
  - **Patterns（重复模式）**——民族志（ethnography）与扎根理论（grounded theory, Glaser & Strauss 1967）的 constant comparison 方法。
  - **Contradictions（言行矛盾）**——Dichter 的理性化诊断 + 社会心理学的态度-行为差距研究（attitude-behavior gap, LaPiere 1934）。
  - **Feelings（情感驱动）**——Alan Klement 的 Jobs-as-Progress + Forces of Progress 中的「emotional anxiety / habit」力学。
  - **Shortcuts（省力捷径）**——Bob Moesta 的 workaround 观察 + Kahneman 的双系统理论（System 1 省力倾向）。

### 核心命题

- **用户的真实需求隐藏在四个结构性张力下**——不是浮现在「我想要 X」的自陈里，而是隐藏在文本/语料的结构性裂缝里。
- 分析师的工作不是 summarize（归纳要点），是 **reveal hidden structures**（揭示底下的结构）。
- 四镜不是分类法（一句话只属于一镜），是 lens（同一段话可被四镜分别照出不同信息）。

### 关键术语（四镜各自解决什么问题）

- **Patterns（重复模式）**：在多个独立访谈/评论里反复出现的相同行为/抱怨/工作流——指向「这不是个人偏好，是品类级的结构性现象」。问题：跨样本一致性。
- **Contradictions（言行矛盾）**：用户嘴上说 A 但行为/选择 B——指向「真实驱动力是 A 之下的另一层动机」（典型 Dichter 场景）。问题：自陈 ≠ 真实动机。
- **Feelings（情感驱动）**：用户描述事件时的情绪密度异常（突然加重 / 突然回避 / 反复回到同一情景）——指向「这里有未被消化的进展张力（progress tension）」。问题：哪里在发生情感能量积累。
- **Shortcuts（省力捷径）**：用户用奇怪的 workaround、替代品、不合规但管用的方法——指向「现有方案在这个 job 上有结构性缺陷，用户用低成本 hack 在弥补」。问题：现有 solution 在哪里漏。

### 关键命令（写进 prompt 的硬约束）

> **Please do NOT summarize the text; reveal the hidden structures beneath it.**
> （不要做摘要，揭示底下的隐藏结构。）

- 这条命令是 Tool 3 的灵魂——summary 给的是 LLM 的归纳能力，structure mining 给的是研究价值。
- 实操：每条「发现」必须能指出「在原始语料里哪段话 / 哪两段话的对照」让你看到这个结构，不能只给抽象结论。

### 与本仓 skill 关联

- **多 perspective 协奏**：
  - Patterns / Shortcuts → 借力 `bob-moesta-perspective`（切换访谈、workaround 观察、四力中的 push / pull / anxiety / habit）。
  - Feelings / Trigger moments → 借力 `alan-klement-perspective`（Jobs-as-Progress、trigger moment、demand energy）。
  - Contradictions → 借力 `dichter-perspective`（理性化、潜意识冲突、社会脚本张力）。
  - 模式型问题可参 `christensen-perspective` 的 Anomaly-Seeking（注意异常 → 找品类级机会）。
- 执行 Tool 3 前先判断：本次语料偏哪一镜？偏 contradictions 优先走 🟢 Dichter；偏 feelings 优先走 🟢 Klement；偏 patterns/shortcuts 优先走 🟢 Moesta。
- 若四镜都重，串行 4 次比并行 1 次更深——每次只戴一镜，最后再综合。

### 决策启发式

1. **summary 是反模式**——任何输出如果可以用「用户表示...」「用户希望...」开头总结，回头重做。结构性输出应以「在 X 段与 Y 段之间发现矛盾 / 在 Z 类场景下出现反复 workaround / 当谈到 W 主题时情绪密度突增」开头。
2. **四镜各自至少给一条**——即便某镜在本批语料里弱，也要明确说「本镜在本批语料里发现较弱，可能因 [原因]」，不要省略。空镜也是信号。
3. **Contradictions 比 Patterns 更值钱**——重复出现的现象是「市场共识需求」，言行矛盾才指向「未被竞品发现的潜空间」。Tool 3 的 ROI 主要靠 contradictions。
4. **Shortcuts 是 Tier-0 需求线索**——用户已经在用 workaround 解决的问题，已经是「足够痛到自己动手」的需求；优先看 shortcuts 反推产品做什么。
5. **Feelings 要避免投射**——分析师感到「这段话好难过」不算数，要找到原文里的语言信号（重复的句子 / 突然的迂回 / 异常详细的细节 / 突然的简短）作为证据。

---

## 4. Jobs to be Done（Tool 4 / 6 / 7 / 8）

### 人物谱系

JTBD 是一个理论族而非单一框架，research 的 Tool 4 / 6 / 7 / 8 横跨四位主要贡献者：

- **Clayton Christensen**（哈佛商学院，1952-2020）—— JTBD 理论源头。
  - 核心贡献：奶昔访谈、Hire / Fire 隐喻、Anomaly-Seeking、Jobs-to-be-Done 命名权。
  - 本仓 skill：`christensen-perspective` —— **🟢 Grounded**。
  - 关键书：*The Innovator's Dilemma*（1997）、*Competing Against Luck*（2016）。
- **Bob Moesta**（Christensen 早期合作者，Re-Wired Group / The Re-Wired Group 创始人）—— Demand-Side JTBD。
  - 核心贡献：切换访谈（Switch Interview）、Forces of Progress（push / pull / anxiety / habit）、Demand-Side Sales、真竞品识别。
  - 本仓 skill：`bob-moesta-perspective` —— **🟢 Grounded**。
  - 关键书：*Demand-Side Sales 101*（2020）、*Job Moves*（2024）。
- **Tony Ulwick**（Strategyn 创始人）—— Outcome-Driven Innovation（ODI）。
  - 核心贡献：outcome statement 格式、importance × satisfaction 二维、opportunity score、outcome-based segmentation、job map（8 阶段）。
  - 本仓 skill：`tony-ulwick-perspective` —— **🟢 Grounded**。
  - 关键书：*What Customers Want*（2005）、*Jobs to Be Done: Theory to Practice*（2016）。
- **Alan Klement**（独立顾问 / NYC JTBD 社区）—— Jobs-as-Progress。
  - 核心贡献：Job Story 格式、When-I-want-so-I-can、Big Hire / Little Hire、demand energy、Forces of Progress 重述。
  - 本仓 skill：`alan-klement-perspective` —— **🟢 Grounded**。
  - 关键书：*When Coffee and Kale Compete*（2016）。

### 核心命题

- **用户不是买产品，是「雇」产品来完成 job**——产品 = 工具，用户雇佣它是因为生活里出现了一个「想要进展但被卡住」的情境。
- **分群基于 needs / pain points / desired progress，而非人口学（age / gender / income）**——人口学是相关性，jobs 是因果性。
- **Job 不变，solutions 变**——「让孩子按时上学」这个 job 从马车到电动滑板车都不变，工具在变。竞品定义来自同 job 不同 solution，不来自同行业不同品牌。
- **每个 job 有三层**：功能层（做什么）、情感层（怎么感觉）、社交层（在他人眼里成为什么样的人）。三层都要看。

### 关键术语（三维 jobs）

- **Functional Job（功能 job）**：用户要完成的客观任务、达成的可观察结果。
  - 格式：**When I [situation], I want to [motivation], so I can [expected outcome].**
  - 中文：当我在 [情境]，我希望 [动机]，这样我就能 [期望进展]。
  - 例：「当我下班回家发现没买菜，我希望能 30 分钟内做出一餐，这样我就能让全家在 7 点前吃上热饭。」
- **Emotional Job（情感 job）**：用户对自己想要的感觉 / 想要避免的感觉。
  - 格式：**When I [situation], I want to feel [feeling] / avoid feeling [feeling], so I can [emotional progress].**
  - 例：「当我看到孩子吃我做的饭吃得很香，我希望感到『我没有亏待这个家』，避免感到『我又用外卖凑合』。」
- **Social Job（社交 job）**：用户希望在他人眼里呈现的样子 / 避免被看成的样子。
  - 格式：**When I [situation], I want to appear as [identity] / avoid appearing as [identity], so I can [social progress].**
  - 例：「当家里来客人时，我希望被看成『一个懂得照顾家人的母亲』，避免被看成『只会点外卖的人』。」
- **Related Job（相关 job）**：与主 job 同时发生、影响主 job 决策的其他 job（如「主 job：做晚饭」相关 job：监督孩子作业、回工作消息）。

### 经典文本

- Christensen, C. M., et al. (2016). *Competing Against Luck: The Story of Innovation and Customer Choice*.
- Ulwick, A. W. (2016). *Jobs to Be Done: Theory to Practice*.
- Klement, A. (2016). *When Coffee and Kale Compete: Become great at making products people will buy*.
- Moesta, B., & Spiek, C. (2020). *Demand-Side Sales 101: Stop Selling and Help Your Customers Make Progress*.
- 早期源头：Theodore Levitt (1960) "Marketing Myopia" —— "People don't want a quarter-inch drill, they want a quarter-inch hole."（被 Christensen 引为 JTBD 思想起源之一。）

### research 使用决策启发式（Functional / Emotional / Social 三维选择）

1. **三维不必每次都全做**——B2B 工具型产品功能 job 主导，情感与社交弱；家庭 / 育儿 / 健康 / 教育产品情感与社交往往比功能更决定购买；身份认同型品类（穿戴 / 教育选择 / 育儿方式）社交 job 是主战场。先判断品类，再决定三维深度。
2. **情感 job 必须找到「feel X / avoid feeling Y」双向**——只写「想感到温暖」不够，要找到对立面「避免感到失败 / 愧疚 / 被评价」。双向才是动机张力，单向是愿望清单。
3. **社交 job 在中国家庭场景里要扣到具体观察者**——不是「让别人觉得我是好妈妈」，是「让我妈、让小区里的其他妈妈、让先生家的人、让孩子幼儿园老师觉得我是 X」。观察者明确，社交 job 才落地。
4. **Job 格式不要简化成 user story**——「作为 X 用户，我希望 Y，以便 Z」是 user story，不是 Job Story。Job Story 必须以 situation 开头（When I...），强调情境触发，不强调角色。情境 = 因果，角色 = persona（JTBD 反 persona）。
5. **三维之间会冲突，这本身就是发现**——功能上想省时间，情感上想感到「认真照顾家」，社交上想被看成「有时间精力的母亲」——三者冲突的时刻就是产品介入的 trigger moment。把冲突写出来，不要平铺三维。

---

## 5. 用户访谈 20 类问题（Tool 9）

### 人物 / 出处

- **非单一作者，是定性访谈心理学传统的整合**。
- 可关联的核心专家：
  - **Steve Portigal**（独立 UX 研究顾问）——访谈技术、probe tree、silence/echo/tell me more。
    - 本仓 skill：`steve-portigal-perspective` —— **🟢 Grounded**。
    - 关键书：*Interviewing Users*（2013, 2nd ed. 2023）、*Doorbells, Danger, and Dead Batteries*（2019）。
  - **Indi Young**（Adaptive Path 联合创始人，独立顾问）——Listening Session、mental models、cognitive empathy。
    - 本仓 skill：`indi-young-perspective` —— **🟢 Grounded**。
    - 关键书：*Mental Models*（2008）、*Practical Empathy*（2015）、*Time to Listen*（2022）。
  - **Elinor Ochs**（UCLA 语言人类学家 / CELF 主任）——参与框架、家庭互动民族志。
    - 本仓 skill：`elinor-ochs-celf-perspective` —— **🟢 Grounded**。
    - 适用于 research 在家庭场景做现场观察 / 视频研究时的访谈框架。
  - 历史源头：Robert Merton（focused interview 1956）、Lazarsfeld（depth interview 50s）。

### 20 类问题清单（每类一句话定位）

1. **Background / Demographics（背景）**——基本身份、生活状态、产品相关的事实背景。建立 rapport 也建立画像基线。
2. **Daily Routine（日常流程）**——用户在产品相关场景里的典型一天 / 一周如何展开。找 trigger moment 与 friction 的现场。
3. **Goals & Motivations（目标与动机）**——在此品类下想达成什么、为什么。Job Story situation 的源数据。
4. **Pain Points & Challenges（痛点与挑战）**——具体卡住的事件，不是抽象抱怨。每个痛点都要追到「上一次发生是什么时候」。
5. **Current Solutions（当前方案）**——目前怎么解决（包括 workaround、替代品、自制方案、不解决）。Tool 3 的 shortcuts 镜头数据源。
6. **Buying / Adoption Triggers（触发事件）**——什么事让你开始找新方案 / 什么事让你最后决定切换。Moesta 切换访谈核心。
7. **Decision Criteria（决策标准）**——选 / 不选的具体维度，按重要性排序。注意自陈 ≠ 真实，需与行为对照。
8. **Comparison & Alternatives（对比与替代）**——考虑过哪些方案、为什么选 / 不选。真竞品识别。
9. **Usage Patterns（使用模式）**——具体怎么用，频率、时长、场合、与谁一起。功能 job 的现场。
10. **Emotional Responses（情感反应）**——用某方案时的情绪、放弃时的情绪、推荐给别人时的情绪。情感 job 数据源。
11. **Social Context（社交语境）**——这个决策 / 使用过程里有谁在场 / 影响 / 评价。社交 job 数据源。
12. **Anxieties & Concerns（焦虑与顾虑）**——切换新方案时害怕什么、留在旧方案时担心什么。Moesta 四力中的 anxiety / habit。
13. **Aspirations & Identity（向往与身份）**——希望成为什么样的人、希望避免成为什么样的人。Dichter 与 Klement 的 identity progress。
14. **Past Experiences（过去经历）**——过去尝试 / 失败 / 成功的故事。具体事件优先于抽象总结。
15. **Hypothetical Scenarios（假设场景）**——「如果...你会怎么做」类。慎用，自陈预测准确度低；只用作探针不用作结论。
16. **Future Expectations（未来期待）**——3 年 / 5 年后希望这件事变成什么样。战略对话的开口。
17. **Frustrations with Industry（行业级抱怨）**——对整个品类的失望、对供给方共同行为的不满。category-level insight。
18. **Workarounds & Hacks（替代方案与窍门）**——自己发明的小窍门、奇怪的用法、不合规但管用的方式。Tier-0 需求线索。
19. **Recommendations Behavior（推荐行为）**——是否推荐给别人、推荐给谁、怎么描述。NPS 的定性版，比分数有信息量。
20. **Reflections & Wishes（反思与愿望）**——访谈尾段开放性收口，「如果你能挥魔法棒...」类。出乎意料的需求常出现在这里。

### 五原则

- **Clarity（清晰）**——每个问题只问一件事，无歧义。反例：「你觉得这个产品好用且有趣吗？」（拆成两题）。
- **Child-Friendly（语言友好）**——如果一个 10 岁孩子听不懂，重写。术语、缩写、行业黑话一律翻译。
- **Aided Recall（辅助回忆）**——不要问「你一般怎么做」，问「上一次发生是什么时候 / 当时具体怎么做的」。具体事件比抽象习惯准确。
- **Conciseness（简洁）**——一句话能问清不用两句。长问题 = 误导问题。
- **Neutrality（中立）**——不暗示期望答案。反例：「这个功能很方便对吧？」（leading question）。

### 四 tone

- **Friendly（友好）**——建立 rapport 阶段、敏感话题前。语气放松，让被访者感到安全。
- **Neutral（中立）**——核心信息收集阶段。不评价、不附和、不引导，保持空白让被访者填。
- **Clear（清晰）**——遇到被访者理解偏差或答非所问时，重述问题。不放过模糊。
- **Supportive（支持）**——被访者讲到挫败 / 失败 / 羞耻经历时。承认情绪但不打断，「这听起来确实不容易，能再多说一点吗」。

### 与本仓 skill 关联

- **优先走 🟢**：访谈技术与追问 → `steve-portigal-perspective`；Listening Session 非验证式倾听 → `indi-young-perspective`；家庭场景 / 多人在场访谈 → `elinor-ochs-celf-perspective`；购买切换访谈 → `bob-moesta-perspective`。
- Tool 9 本身是脚手架，具体怎么追问、怎么 silence、怎么 echo、怎么处理矛盾自陈，都让位给上述 perspective skills。
- 当问题主线是「为什么今天买 / 为什么切换 / 为什么流失」时，20 类问题中第 6 / 8 / 12 类是骨架，必须走 Moesta；其他类是肉。

### 决策启发式

1. **20 类不是 20 题清单**——是 20 个**类别**，每类下根据本次研究目的选 0-3 题。一场 60-90 分钟访谈最多覆盖 8-12 类，贪多反而每类都浅。
2. **优先选「事件型」类（4 / 6 / 14 / 18）而不是「态度型」类（7 / 13 / 16）**——事件比态度准；事件能被追问到具体场景，态度只能被自陈。
3. **第 15 类（假设场景）只用作探针，不用作结论**——「如果我们做 X 你会用吗」的回答几乎全是社会赞许偏差，价值在于看追问后的犹豫和具体化能力。
4. **Aided Recall 是 20 类问题里最被低估的原则**——把所有「你一般怎么...」改成「最近一次...是什么时候，那次具体怎么发生的」。这一条改完，访谈质量翻倍。
5. **第 20 类（reflections & wishes）的「魔法棒问题」要留时间**——访谈最后 5-10 分钟做开放收口，常出现整场最有价值的一句话，因为被访者已经被前面的具体追问唤醒了真实感受。

---

## 6. 心理测量学 / 问卷设计（Tool 10）

### 人物 / 出处

- **Don A. Dillman**（华盛顿州立大学社会学家，调查方法学）—— Tailored Design Method（TDM）。
  - 关键书：*Mail and Telephone Surveys*（1978）、*Internet, Phone, Mail, and Mixed-Mode Surveys: The Tailored Design Method*（2014, 4th ed.）。
- 经典心理测量学谱系：
  - **Rensis Likert**（1932）—— Likert 量表发明者。
  - **Lee Cronbach**（1951）—— Cronbach's α，内部一致性信度。
  - **Donald Campbell & Donald Fiske**（1959）—— Multitrait-Multimethod Matrix，convergent / discriminant validity。
  - **Jum Nunnally**（1978）—— *Psychometric Theory*，心理测量学集大成。
- **无本仓 dedicated Dillman skill，本文件即 🟡 Simulated fallback anchor**。

### 核心命题

- **量化问卷必须 closed-ended（封闭式：单选 + Likert），可量化、可分析**——开放式问题（open-ended）属于定性访谈领域（Tool 9），不进 Tool 10。
- 问卷不是「把访谈写下来发出去」——访谈靠追问纠错，问卷一次性，所有歧义会被放大成噪音。
- 问卷设计 = 减少所有非「真实变异」来源：歧义、社会赞许偏差、顺序效应、疲劳效应、抽样偏差。
- **TDM（Tailored Design Method）核心**：把问卷视为社会交换（social exchange），通过降低被试成本、提高被试收益、建立信任三个杠杆提升回应率与质量。

### 关键术语（Tool 10 五维问题）

- **Knowledge（知识）**——被试对相关概念 / 品类 / 功能的认知程度。例：「以下哪个最接近 [品类] 的定义？」（单选）。
- **Evaluation（评价）**——对某物 / 某体验的评分。例：「您对 X 的满意度」（Likert 5 / 7 点）。
- **Behavior（行为）**——做了什么 / 怎么做（过去时，可观察的事实）。例：「过去 30 天您使用 X 的次数」（选项区间）。
- **Frequency（频率）**——多久做一次 / 多频繁发生。例：「您每周做饭次数」（选项区间）。注意：Frequency 与 Behavior 有重叠，区分在于 Behavior 问「是什么」，Frequency 问「多频繁」。
- **Psychology（心理）**——态度、信念、价值观、动机倾向。例：「我倾向于在家做饭而不是外食」（Likert 5 点）。最容易受社会赞许偏差污染，必须放反向题。

### 关键术语（五项效度）

- **Factorial Structure（因子结构）**——同一个 sub-scale 下的题项是否在因子分析（EFA / CFA）里聚成同一因子。决定 sub-scale 是否「真的在测同一个东西」。
- **Content Validity（内容效度）**——题项是否覆盖了构造（construct）的全部内容范围。靠专家评审与文献回顾建立，没有统计指标。
- **Discriminant Validity（区分效度）**——本构造与其他相邻构造的相关性是否显著低于本构造内部一致性。决定「这个 sub-scale 测的是它自己的东西，不是别人的」。
- **Predictive Validity（预测效度）**——本量表分数是否能预测未来的相关行为 / 结果。例：JAS 的 SI 分数是否能预测真实使用频率。
- **Construct Validity（构念效度）**——整体来看，量表测的是不是它声称要测的那个抽象构造。是 Factorial / Content / Discriminant / Predictive 的总和判断。

### 反 single-question fallacy / social-desirability defense

- **Single-question fallacy（单题谬误）**——一题问两件事，被试无法分别作答。
  - 反例：「你觉得这个产品快速且易用吗？」（快速与易用是两个维度）。
  - 修正：拆成两题，「快速」一题、「易用」一题。
- **Social-desirability bias（社会赞许偏差）防御**：
  - **反向措辞（reverse-coded items）**：sub-scale 内部至少 30% 题项语义反向（如测「健康饮食倾向」放「我经常吃零食代替正餐」），与正向题分数互校。
  - **第三方措辞（third-party phrasing）**：把敏感问题从「你」改成「像你这样的人」或「你身边的朋友」，降低自我曝光压力。例：「您是否每天准时下班？」→「您身边的同事大多是否能每天准时下班？」
  - **Forced-choice（强迫选择）**：在两个同等社会赞许度的陈述里二选一，绕开「都选好答案」。
  - **匿名性强化**：问卷开头明示匿名、不可追溯，并在敏感题前再次声明。

### 经典文本

- Dillman, D. A., Smyth, J. D., & Christian, L. M. (2014). *Internet, Phone, Mail, and Mixed-Mode Surveys: The Tailored Design Method* (4th ed.). Wiley.
- Nunnally, J. C., & Bernstein, I. H. (1994). *Psychometric Theory* (3rd ed.). McGraw-Hill.
- Cronbach, L. J. (1951). "Coefficient alpha and the internal structure of tests." *Psychometrika*.
- Campbell, D. T., & Fiske, D. W. (1959). "Convergent and discriminant validation by the multitrait-multimethod matrix." *Psychological Bulletin*.
- Krosnick, J. A. (1999). "Survey research." *Annual Review of Psychology* —— 调查方法学的综述权威。

### 与本仓 skill 关联

- **无 dedicated skill，本文件即 🟡 Simulated fallback anchor**。
- 执行时声明：「（基于训练数据，本仓暂无 Dillman / 心理测量学 skill）」，必要时在 `memory/skill-distillation-candidates.md` 追加记录。
- 与 Tool 2（JAS）协同：JAS 是已有量表的应用，Tool 10 是新量表的设计；两者共享 Likert / 反向题 / sub-scale 等原则。
- 与 Tool 6 / 7（情感 / 功能需求）协同：Tool 6/7 的定性发现是 Tool 10 题项的内容来源；Tool 10 是 Tool 6/7 的量化验证。

### 决策启发式

1. **每个 sub-scale 至少 3 道题**——单题不足以检验内部一致性（Cronbach's α 至少需要 3 题以上才有意义）。每个 construct 给 3-5 题，宁少题数但留出反向题。
2. **Likert 5 点 vs 7 点**——5 点对中国被试更友好（与日常表达习惯一致），7 点在专业被试 / 跨文化研究里更有区分度。research 默认 5 点除非有具体理由（与 Tool 2 JAS 保持一致）。
3. **问卷长度上限：单次回答 ≤ 10 分钟**——超过 10 分钟疲劳效应（fatigue effect）开始显著恶化后半部分数据质量。50-80 题为常见上限，敏感题前置。
4. **题项顺序：低敏感 → 高敏感，宽 → 窄**——开头放容易回答的事实题（年龄 / 频率），中段放评价 / 心理题，结尾放敏感题与人口学补充。避免开场即问敏感题导致放弃率上升。
5. **永远跑 pilot（预调研）**——正式发放前找 5-10 人填一遍，看每题平均耗时、看哪些题被跳过、看哪些题答案分布过度集中（接近天花板 / 地板效应说明区分度不足）。pilot 是 Tool 10 最容易被省略也最值得做的一步。
