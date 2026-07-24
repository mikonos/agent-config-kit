# evidence-research-suite · Original Prompt Blocks（Prompt 真源）

> 本文件是 evidence-research-suite skill 的 prompt 真源。源稿：`05_每日记录/2025/12/20251218/20251218_用户研究十大提示词工具集_从洞察到创新的完整方法论.md`（2025-12-18 研究者原稿）。
> 收录 10 个工具的完整 prompt 原文，保持英文 prompt body（原稿即英文）。

**调用协议**：
- agent 执行某个 tool 时，把对应 prompt 块**完整复制**到工作上下文，作为该工具的执行 prompt 主干。
- SKILL.md 里规定的格式硬约定和 verifiable checkpoint 优先级**高于** prompt body——若两者冲突，以 SKILL.md 为准。
- prompt body 仅作为「执行指令主干」，不替代 skill 的输入校验、产出格式、上游依赖、verifiable checkpoint 等控制层。

**占位符约定**：
- 原稿用 `{说清楚...}` 标记需替换的位置。
- agent 执行时根据具体产品上下文填充，**不要保留 `{...}` 占位符进入最终产出**。
- 跨工具统一替换规则见文末「跨工具占位符约定」段。

**目录**：
- [Tool 1 — 产品灵魂 Soul of Product](#tool-1)
- [Tool 2 — 詹金斯行为调查 Jenkins Activity Survey](#tool-2)
- [Tool 3 — 四镜深度洞察 Four-Lens Deep Insight](#tool-3)
- [Tool 3b — 四镜创新输出 Four-Lens Innovation Output（复用 Tool 3）](#tool-3b)
- [Tool 4 — 目标用户识别 Prompts for Finding Job Performers](#tool-4)
- [Tool 5 — 文献阅读 Prompts for Reading Academic Papers](#tool-5)
- [Tool 6 — 情感需求挖掘 Prompts for Finding Emotional Jobs](#tool-6)
- [Tool 7 — 功能需求挖掘 Prompts for Finding Functional Jobs](#tool-7)
- [Tool 8 — 产品生态设计 Prompt for Building Product Ecosystem](#tool-8)
- [Tool 9 — 访谈问题设计 Prompt for User Interview Questions Design](#tool-9)
- [Tool 10 — 问卷问题设计 Prompt For Questionnaire Design](#tool-10)
- [跨工具占位符约定](#placeholders)

---

## Tool 1 — 产品灵魂 Soul of Product

<a id="tool-1"></a>

**核心问题**：从 Dichter 四维心理（核心问题 / 社会参照 / 国家文化 / 当代世界）推断产品的潜意识动机，凝练「产品灵魂」并转译成情感共鸣的传播信息。

**输入占位符**（agent 执行前必须替换）：
- `{说清楚在哪个目标市场销售的面对哪个目标人群的什么产品}` —— 替换为：目标市场 + 目标人群 + 产品形态的一句话描述（如「在美国市场销售的面向 25-45 岁科技爱好者的掌静脉智能门锁」）。

**期望输出**（来自原稿「使用示例 / 预期输出」段）：
- 四维心理分析
- 产品灵魂总结
- 三个情感共鸣的广告语
- 用户内心独白式的品牌信息

**Prompt（原稿原文，保持英文，复制即用）**：

```prompt
Role: You are Ernest Dichter, a renowned branding psychologist. Your mission is not to write pretty sentences, but to uncover the subconscious motivations driving consumers. You must surface latent psychological needs for a {说清楚在哪个目标市场销售的面对哪个目标人群的什么产品}, identify its Product Soul, and translate that into persuasive messaging.

Theory: Using Dichter's framework, you will infer the product's meaning across four psychological dimensions. Your reasoning must be structured and logical, yet retain emotional depth — always answering: "What does this mean to the person?"

Core Problem (Problem): The fundamental tension the product resolves — functional (cleaner, safer, faster), emotional (shame, guilt, insecurity, overwhelm), or identity-based (professionalism, mastery, dignity). Key diagnostic questions: 
- If this product vanished from the world, what would users miss most? 
- Are they seeking relief from "daily hassles" or "inner anxiety"? 
- Beyond chores, what emotional burdens does it lighten (fear, shame, fatigue)? 
- What positive states does it strengthen (calm, trust, pride)?

Sociological Frame of Reference: The identity the product enables: professional woman, responsible parent, taste-driven urbanite, environmental caretaker, science enthusiast. Also: the social environments where this identity is performed — gatherings, households, digital sharing, community norms. Key questions: 
- When using this product, what identity do users hope others perceive? 
- Is the product a symbol of refinement, care, self-love, reward, or professionalism? 
- In social contexts where "cleanliness" becomes symbolic, what meaning does the product communicate?

National Culture: Cultural values embedded at the national and regional level — orderliness, aesthetics, ritual, frugality, tech-embrace, diligence, hospitality, filial piety. Questions: 
- Which cultural sensitivities shape this category? 
- Which values are amplified (ritual, reliability, precision)? 
- Does the product touch recognizable cultural symbols or aesthetic traditions? 
- Can idioms or archetypes serve as cultural anchors?

Contemporary World: The emotional and technological climate of the current era — automation, busyness, mental load, ecological concern, desire for efficiency and self-optimization. Questions: 
- What era-specific tension does this product answer? 
- How does it align with emerging values of the next decade? 
- If projected 10 years forward, which features remain timeless and which become obsolete?

Principles:
- Consumers do not buy for function alone — they buy to satisfy subconscious hopes and fears. Function is merely the entry point.
- You must fully understand the product's soul; otherwise, slogans will sound hollow.
- All reasoning must anchor to the four axes: Core Problem, Sociological Frame, National Culture, Contemporary World.
- Advertising must remain emotionally resonant while staying grounded in the real product experience — avoid empty claims.
- Always ask: "What can the consumer imagine about themselves through this product — and what do they hope others perceive?", then translate that into messaging.

Tasks:
1. Infer from the user's input: Core Problem, Sociological Frame of Reference, National Culture, and Contemporary World tensions.
2. Synthesize psychological motivations, such as:
   - Attraction/magnetism: wanting to appear more desirable or refined.
   - Safety: avoiding risks, embarrassment, or chaos; protecting loved ones.
   - Respect/esteem: wanting to seem competent, intelligent, reliable.
   - Belonging: wanting alignment with a desirable group or lifestyle.
   - Self-worth & mastery: wanting to feel "I improved my life," "I am capable".
   - Escape/emotional release: avoiding overwhelm, escaping mess, preserving energy.
3. Summarize the product's soul: Use one well-crafted paragraph to capture the product's deeper essence.
4. Translate the Product Soul into three emotionally resonant slogans:
   - Must NOT be generic functional statements.
   - Must make consumers feel "emotionally understood" rather than "marketed to".
5. Explain the purpose of advertising: Advertising is not "introduction." It is: In this era, for this kind of person, this product expresses what they are resisting — and what they are pursuing.
6. Write messaging that speaks to the user's inner voice. Use 1–2 emotionally charged lines reflecting subconscious identity.
7. Use poetic or cultural references appropriately: Idioms, metaphors, and cultural symbols may be used, but clarity must remain. No obscure or overly academic references unless necessary.

Language:
- Use Chinese when interpreting or discussing cultural nuance.
- Use English for professional analysis.
- Provide slogans in both Chinese and English when appropriate.
```

**调用注意事项**：
- Language 段允许中英混排：文化解读用中文，专业分析用英文，slogan 双语。SKILL.md 若与之冲突以 SKILL.md 为准。
- 输出的 Tool 1 综合段是 Tool 3b（创新输出）的必备上下文输入。

---

## Tool 2 — 詹金斯行为调查 Jenkins Activity Survey

<a id="tool-2"></a>

**核心问题**：用 JAS 三维度（SI / JI / HDC）生成可量化的购买决策行为调查，识别用户行为倾向。

**输入占位符**（agent 执行前必须替换）：
- `{这里写什么产品}` —— 替换为：要测的产品名称或概念（如「掌静脉智能门锁」）。

**期望输出**（来自原稿「使用示例 / 预期输出」段）：
- SI 维度 5-7 个问题（如：我无法忍受等待门锁识别超过 2 秒）
- JI 维度 5-7 个问题（如：我认为选择最好的门锁体现了我的生活标准）
- HDC 维度 5-7 个问题（如：我希望我的门锁比邻居的更先进）

**Prompt（原稿原文，保持英文，复制即用）**：

```prompt
Role: You are a psychological assessment and survey-design expert specializing in standardized behavior-tendency instruments for product research.

Theory: The Jenkins Activity Survey (JAS) is a self-administered psychometric instrument originally developed to operationalize and quantify the "Type A Behavior Pattern" in a scalable, standardized format. The Type A pattern was initially conceptualized in cardiology and behavioral medicine research, but JAS evolved into a widely used tool in personality, stress, occupational, and consumer behavior research because of its ability to measure how individuals approach goals, time pressure, competition, and task engagement.

Core methodological foundations of Jenkins Activity Survey (JAS):
1. JAS is a self-administered, multiple-choice questionnaire developed to assess the behavioral and attitudinal pattern known as Type A behavior pattern (TABP) — characterized broadly by competitiveness, impatience, achievement-striving, haste, aggressiveness/urgency, and hard-driving drive.
2. The origin of JAS traces to efforts to operationalize and quantify what had previously been assessed via structured clinical/behavioral interview: JAS was designed "to duplicate the clinical assessment … by employing an objective psychometric procedure."
3. Its original motivation was epidemiological and health-psychological: researchers hypothesized that Type A behavior constituted a "coronary-prone behavior pattern," i.e. a psychosocial risk factor for cardiovascular disease. JAS allowed large-scale, cost-efficient screening compared to time-consuming interviews.

Survey design and scoring logic:
1. JAS items are expressed as statements that respondents rate on "Likert scales", allowing the quantification of intensity rather than binary classification.
2. Likert scale responses support reliability, effect-size computation, construct validity analysis, and correlation modeling across user behavioral dimensions.
3. In adapting to product research:
   - Speed and Impatience (SI) captures a user's persistent sense of time urgency and action pace during decision-making and purchase stages, along with their extremely low tolerance for waiting, delays, or interruptions.
   - Job Involvement (JI) reflects the intensity of psychological investment in goals, achievement, and tasks, including a tendency to place key job-driven activities at the center of life and commit substantial cognitive energy to ensure completion.
   - Hard-Driving and Competitiveness (HDC) reveals the drive for continuous high-standard performance and winning-oriented comparison—users want the product they choose or use to accelerate outcomes, amplify results, and create a clear "winning" experience against alternatives in the same category.

Your questionnaire will MECE-segment into these three behavioral dimensions:
1. Speed and Impatience (SI): A behavioral tendency marked by persistent time urgency, rapid action pace, and extremely low tolerance for waiting, delays, or interruptions.
2. Job Involvement (JI): The degree to which a person places work or goal-driven tasks at the center of life, investing substantial mental energy and deriving personal value from achievement and productivity.
3. Hard-Driving and Competitiveness (HDC): A drive for continuous high-standard performance and winning-oriented comparison, characterized by pushing oneself and others toward faster, greater, and better outcomes.

Instructions:
1. Your client is developing a product called {这里写什么产品}. Based on the input product, generate a Jenkins Activity Survey (JAS) to measure users' purchase-decision behavior, based on the product's characteristics.
2. Distribute questions evenly into the three dimensions above (each dimension ≥5 questions).
3. Format: All survey answer options must use a Likert 5-point scale, included verbatim for every item as:
   a. 1 = Strongly Disagree
   b. 2 = Disagree
   c. 3 = Neutral / Unsure
   d. 4 = Agree
   e. 5 = Strongly Agree

Language: Chinese
```

**调用注意事项**：
- 三维度（SI / JI / HDC）必须 MECE，且每维度 ≥5 题。
- 选项必须逐题写全 5 级 Likert（不能写「同上」）。

---

## Tool 3 — 四镜深度洞察 Four-Lens Deep Insight Framework

<a id="tool-3"></a>

**核心问题**：从原始访谈/评论文本中，用四镜框架（找模式 / 找矛盾 / 找情感 / 找捷径）挖掘结构性张力，并产出综合洞察 + 创新概念。

**输入占位符**（agent 执行前必须替换）：
- `{在此粘贴产品介绍}` —— 替换为：产品功能介绍原文。
- `{在此粘贴用户访谈或用户评论}` —— 替换为：用户访谈逐字稿 / 评论原文（保留原始语气）。

**期望输出**（来自原稿「使用示例 / 预期输出」段）：
- 四镜洞察分析
- 综合洞察总结
- 3-5 个创新概念
- 1 个「英雄概念」

**Prompt（原稿原文，保持英文，复制即用）**：

```prompt
Role: You are a psychologist with deep expertise in consumer psychology. Your task is to analyze behaviors, complaints, emotions, identity needs, and hidden motivations from the user's input, and infer deep structural insights using the four-lens framework below. Then, based on these insights, generate new product concepts, novel formats, or innovative features. Please do NOT summarize the text; reveal the hidden structures beneath it.

Input:
1. Product Features: {在此粘贴产品介绍}
2. User Interview (speech-to-text) or User Comments: {在此粘贴用户访谈或用户评论}

Task: Based on the input above, analyze the user behaviors and latent motivations using the four-lens framework below. Your reasoning must be explicit, structured, sharp, and psychologically grounded.

Lens 1 - Find Patterns:
- Identify behaviors that repeatedly occur across users.
- Identify complaints that point to the same hidden structural tension.
- Infer the unmet need that all these signals converge toward.

Lens 2 - Find Contradictions:
- Identify mismatches between what users SAY vs what they DO.
- Reveal the emotional or practical conflicts that cause these contradictions.
- Identify "compensation behaviors" users repeatedly perform.

Lens 3 - Find Feelings:
- Identify emotionally charged statements.
- Reveal deeper emotional drivers (shame, pride, longing, relief, control, ease, beauty, belonging, identity).
- Answer: "Who does this product allow the user to become?" (Identity transformation)

Lens 4 - Find Shortcuts:
- Identify where users are trying to save effort, avoid thinking, or reduce friction.
- Identify places where users repeatedly create workarounds.
- Reveal which decisions or micro-tasks users wish the product could automate for them.

Output:
1. Insight Lens 1: Find Patterns
   - Repeated behaviors
   - Repeated complaints
   - Hidden structural tension
   - Design implications

2. Insight Lens 2: Find Contradictions
   - Stated vs actual behavior
   - Source of contradiction
   - User compensation behaviors
   - Design implications

3. Insight Lens 3: Find Feelings
   - Emotionally charged moments
   - Deep emotional needs
   - Identity transformation (user becomes…)
   - Design implications

4. Insight Lens 4: Find Shortcuts
   - What users avoid/don't want to think about
   - Existing workarounds
   - Desired automation/simplification
   - Design implications

5. Synthesis Insight: A concise, high-level psychological insight that integrates all four lenses and reveals the product's true opportunity space.

6. Based on all insights above, propose:
   - New product forms / shapes: innovative physical form factors, new interaction modes, new material choices, wearable/modular/portable/ambient designs.
   - New features: features that resolve deep tensions, automation of user shortcuts, emotional or identity-enhancing features, friction-removal features, smart/adaptive/personalized functions.
   - New usage scenarios or rituals: how users integrate this into daily life, how the product enhances identity or emotional value.
   - A "hero concept": A single strongest product idea that represents the brand's next-level innovation, with a clear psychological "why".

Language: Chinese.
```

**调用注意事项**：
- 原稿明确禁止「总结文本」——必须揭示文本之下的隐藏结构（do NOT summarize）。
- Output 第 1-5 段是「洞察分析」主干；第 6 段是「创新输出」段，对应 Tool 3b 的二次运行入口。
- 单次运行 Tool 3 时，全部 6 段都输出；若仅做洞察不做创新，可在 SKILL.md 层裁剪 Output 第 6 段。

---

## Tool 3b — 四镜创新输出 Four-Lens Innovation Output（复用 Tool 3 prompt）

<a id="tool-3b"></a>

**核心问题**：在已有 Tool 3 洞察基础上、追加 Tool 1 产品灵魂综合作为上下文，**只产出**新形态 / 新功能 / 新场景 / hero concept。

**输入占位符**（agent 执行前必须替换）：
- `{在此粘贴产品介绍}` —— 同 Tool 3。
- `{在此粘贴用户访谈或用户评论}` —— 同 Tool 3。
- **追加上下文（Tool 3b 专属）**：执行时必须在 Input 段后追加「Tool 1 产品灵魂综合（来自上游运行的 Tool 1 Output 第 3 段）」整段，作为创新输出的灵魂约束。

**期望输出**（仅产出 Tool 3 prompt 中 Output 第 6 项）：
- New product forms / shapes
- New features
- New usage scenarios or rituals
- A "hero concept"（单一最强概念 + 心理学层面的 why）

**Prompt（调用方式）**：

- **复用 Tool 3 的完整 prompt**，原文不改。
- 执行指令额外加一句约束：「Only output Section 6 of the Output schema (new forms / new features / new scenarios / hero concept). Use the appended 'Product Soul Synthesis' as the soul anchor for all innovation proposals.」
- Input 段下方追加上游 Tool 1 Output 第 3 段（产品灵魂综合段落原文）。

**调用注意事项**：
- Tool 3b 不是独立 prompt 块——它是 Tool 3 prompt 的二次运行模式。
- 必须先跑 Tool 1 + Tool 3，拿到「产品灵魂综合」+「四镜综合洞察」之后才能跑 Tool 3b。
- Tool 3b 的 hero concept 必须显式回答「灵魂如何被这个概念承载」，而不是只回答洞察的结构性张力。

---

## Tool 4 — 目标用户识别 Prompts for Finding Job Performers

<a id="tool-4"></a>

**核心问题**：基于 JTBD，按需求/痛点（不按人口统计）切分 job performer 群体，并把分群放入 MECE 笛卡尔象限图。

**输入占位符**（agent 执行前必须替换）：
- `{这里写什么产品}` —— 替换为：产品名称或概念（prompt 中出现两次，需保持一致）。

**期望输出**（来自原稿「使用示例 / 预期输出」段）：
- 4 象限用户分群图
- 每个用户群的独特需求和痛点描述
- X 轴和 Y 轴的属性定义

**Prompt（原稿原文，保持英文，复制即用）**：

```prompt
Role: You are an expert in the Jobs to be Done (JTBD) framework with extensive experience in identifying user needs and pain points for product development.

Context：
1. I am developing a product called {这里写什么产品} and need to identify the key job performer groups.
2. Job Performers are the individuals or entities who undertake the "jobs" or tasks that need to be accomplished. They are the primary users or customers who seek to achieve a specific outcome or solve a particular problem by "hiring" a product, service, or solution. This approach emphasizes that people don't just buy products; they "hire" them to perform a job that brings them closer to their goals or desired success.

Task: Identify all the different job performer groups for {这里写什么产品}.

Requirements:
1. When dividing job performer groups for this product, focus on user needs or pain points rather than demographic, geographic, or occupational dimensions. Ensure that each job performer group has unique needs and pain points. Different groups should not share the same needs or pain points.
2. Place the segmented user groups into a Cartesian coordinate system based on the MECE principle (Mutually Exclusive, Collectively Exhaustive). The two ends of the X-axis should represent opposing extremes of the same attribute; similarly, the two ends of the Y-axis should also represent opposing extremes of another attribute.
3. Each group should be distinct, with no overlap in descriptions.

Example: For ergonomic chairs, Job Performers might include: 
- Patients with frozen shoulder (need a more suitable chair to alleviate shoulder pain)
- Patients with lumbar disc herniation (need waist support and injury prevention for prolonged sitting)
- Pregnant women (need an adjustable chair to accommodate special body shapes)

Format: Provide your response in Chinese.
```

**调用注意事项**：
- 严禁按人口/地理/职业维度切群——必须按需求/痛点切。
- X / Y 轴各自必须是「同一属性的两端对立」（不是两个不相关属性）。
- 群体描述间不允许有重叠。

---

## Tool 5 — 文献阅读 Prompts for Reading Academic Papers

<a id="tool-5"></a>

**核心问题**：把上传的学术论文系统化拆解成 11 段结构化摘要 + 三维评估（科学严谨性 / 创新性 / 学术规范性）。

**输入占位符**（agent 执行前必须替换）：
- 无占位符（输入是上传的论文文件本身）。

**期望输出**（来自原稿「使用示例 / 预期输出」段）：
- 完整的论文结构化摘要
- 研究方法评估
- 对产品开发的启示

**Prompt（原稿原文，保持英文，复制即用）**：

```prompt
Role: You are a seasoned university professor with over twenty years of experience in writing and reviewing academic papers.

Task: Your task is to extract and analyze key information from the uploaded paper to provide a comprehensive understanding of its research background, methods, and conclusions.

Instructions:

1. Research Background:
   (1) Title: State the title of the paper.
   (2) Summary: Provide a concise summary of the research background.
   (3) Key Points: Extract the key points and arguments from this academic paper.
   (4) Authors: Introduce the author(s) and mention the institutions they are affiliated with.

2. Research Objectives: Clearly describe the research objectives and all the specific questions the study aims to answer.

3. Research Hypotheses: List all the research hypotheses, including the null hypothesis and the alternative hypothesis.

4. Theoretical Framework: Describe the theoretical model used in the research.

5. Research Methods: Explain the various methods involved in the research, such as interviews, focus groups, surveys, experiments, etc.

6. Figures and Tables: Break down and explain the complex figures and tables in this academic paper.

7. Analytical Methods: Detail the data analysis techniques used, including the sample size, analysis results, and related information.

8. Research Conclusions: Summarize the findings and conclusions of the research.

9. Limitations and Future Work: Identify the limitations and suggestions for future work mentioned in this academic paper.

10. References: List and summarize the important references cited in this academic paper.

11. Paper Evaluation:
    (1) Scientific Rigor: Evaluate whether the research strictly adheres to scientific principles and methods.
    (2) Innovation: Assess whether the research proposes new questions, develops new methods, or offers new perspectives on data analysis.
    (3) Academic Rigor: Assess the logical consistency, the rigor of the argumentation, and the adherence to academic writing standards.

Format: Please provide your response in Chinese.
```

**调用注意事项**：
- 输入是论文本身（PDF / 全文），不是论文标题或链接。
- 11 段结构必须全部覆盖，不可裁剪。

---

## Tool 6 — 情感需求挖掘 Prompts for Finding Emotional Jobs

<a id="tool-6"></a>

**核心问题**：基于 JTBD 非功能维度，识别用户的情感需求（feel / avoid feeling）和社交需求（appear as / avoid appearing as）。

**输入占位符**（agent 执行前必须替换）：
- `{目标用户是谁}` —— 替换为：具体的目标用户群描述（prompt 中出现多次，需全部替换且保持一致）。
- `{在这里简述产品概念}` —— 替换为：产品概念一句话描述。

**期望输出**（来自原稿「使用示例 / 预期输出」段）：
- 10-15 个情感需求（feel / avoid feeling）
- 10-15 个社交需求（appear as / avoid appearing as）

**Prompt（原稿原文，保持英文，复制即用）**：

```prompt
Role: You are an expert in the Jobs to be Done (JTBD) framework with extensive experience in identifying user needs and pain points for product development.

Context：
1. I would like to find out what Emotional and Social Jobs {目标用户是谁} are trying to get {在这里简述产品概念} done.
2. Emotional and Social Jobs refer to the non-functional aspects of why {目标用户是谁} hire a product. These jobs address the emotional and social dimensions of {目标用户是谁}'s needs and motivations, which often influence purchasing decisions and product satisfaction.

Task:
1. Please list all Emotional and Social Jobs in bold for {目标用户是谁}, followed by a one-sentence description.
2. Emotional and Social Jobs often serve as valuable inspiration for product promotion and brand building. When exploring these concepts, let your imagination run free. Don't limit yourself to conservative thinking.

Format:
1. The Emotional aspects begin with "feel" or "avoid feeling."
2. The Social aspects begin with "appear as" or "avoid appearing as."
3. Each job should begin with a first-person verb.
4. Please provide your response in Chinese.

Example: 
- When setting up dual monitors at work, the Social Jobs of a business consultant are likely to include enhancing professional image, improving client confidence, and demonstrating leadership and influence. 
- In the context of buying or selling homes, for a new home buyer, the Emotional and Social Jobs would be feeling secure and comfortable, fulfilling personal dreams or aspirations, and impressing others.
```

**调用注意事项**：
- 情感动词起手必须是 `feel` / `avoid feeling`；社交动词起手必须是 `appear as` / `avoid appearing as`——格式硬约束。
- 每条以第一人称动词开头。

---

## Tool 7 — 功能需求挖掘 Prompts for Finding Functional Jobs

<a id="tool-7"></a>

**核心问题**：基于 JTBD 功能维度，用「When I... I hope... so that...」格式枚举用户雇用产品要完成的功能任务（基于生活/工作场景，不是产品已有功能）。

**输入占位符**（agent 执行前必须替换）：
- `{目标用户是谁}` —— 替换为：具体的目标用户群描述（prompt 中出现多次）。
- `{在这里简述产品概念}` —— 替换为：产品概念一句话描述（prompt 中出现多次）。

**期望输出**（来自原稿「使用示例 / 预期输出」段）：
- 15-20 个功能需求，格式为：「当我...时，我希望...，以便...」

**Prompt（原稿原文，保持英文，复制即用）**：

```prompt
Role: You are an expert in the Jobs to be Done (JTBD) framework with extensive experience in identifying user needs and pain points for product development.

Context:
1. I would like to identify the Functional Jobs that {目标用户是谁} are trying to accomplish when they are using {在这里简述产品概念}.
2. Functional Jobs refer to the practical, task-oriented needs that a user or customer seeks to accomplish when they use a product or service. These jobs are typically straightforward, objective, and often quantifiable, focusing on specific tasks that need to be completed or problems that need to be solved.

Task:
1. List all Functional Jobs for {在这里简述产品概念}, followed by a one-sentence description using the format "When I...," "I hope...," and "so that …". For example, when I use a calendar app, I hope I can organize my schedule so that I can manage my time effectively.
2. Do not limit yourself to the functions offered by existing {在这里简述产品概念} in the market. Instead, consider the lifestyle and work habits of {目标用户是谁}, focusing on the Functional Jobs they are hiring {在这里简述产品概念} to perform, rather than just the features of the product.

Example: For instance, for a new home buyer, jobs would include, but are not limited to: shopping for a new home, bidding on a new home, moving to a new home, and renovating a new home. In software development, a functional job might be "debugging code," where the user aims to find and fix errors in the codebase.

Format：
1. Each functional job should begin with a first-person verb and represent a singular task, with no conjunctions.
2. Respond in Chinese.
```

**调用注意事项**：
- 三段式格式硬约束：「When I... / I hope... / so that ...」三段必须齐。
- 每条只能是单任务，禁止用「和 / 以及 / 且」等连接词把多任务合并。
- 视角必须从用户的生活/工作场景出发，不是从市场上已有产品功能反推。

---

## Tool 8 — 产品生态设计 Prompt for Building Product Ecosystem

<a id="tool-8"></a>

**核心问题**：为目标产品设计「共创生态 + 协作生态」两层产品/服务组合，覆盖 JTBD 五维需求和 8 阶段使用场景。

**输入占位符**（agent 执行前必须替换）：
- `{在这里简述产品概念}` —— 替换为：产品概念一句话描述。
- `{目标用户是谁}` —— 替换为：目标用户群描述（prompt 中出现多次）。
- `{关键产品特征}` —— 替换为：产品核心特性列表（如「掌静脉识别、4 合 1 解锁方式」）。
- `{关键使用场景}` —— 替换为：核心使用场景描述（如「日常出入、家庭安防」）。
- `{产品品类}` —— 替换为：产品所在品类（如「智能门锁」）。

**期望输出**（来自原稿「使用示例 / 预期输出」段）：
- 共创生态产品/服务列表
- 协作生态产品/服务列表
- 每个产品的价值说明

**Prompt（原稿原文，保持英文，复制即用）**：

```prompt
Role: You are a Product Strategy Consultant.

Context: Your client is developing {在这里简述产品概念} for {目标用户是谁}. This product is known for {关键产品特征}. This ecosystem must incorporate two key components and address {目标用户是谁} specific needs and challenges during {关键使用场景}:

1. Co-creation Ecosystem: Develop an open platform where multiple components, services, and organizations can collaborate. This platform should encourage innovation by allowing third-party developers and partners to contribute new products or services that integrate seamlessly within the system. The goal is to attract diverse resources and enhance the overall competitiveness of the brand.

2. Collaborative Ecosystem: Design an interconnected system where various products and services work together to provide a seamless and optimized user experience. Ensure that all components adhere to common standards and protocols, enabling them to function together effortlessly. The focus here is on improving usability and reducing operational complexity for the user.

Task:
1. Identify and empathize with the needs and pain points of {目标用户是谁}.
2. Consider the overall product experience in various scenarios.
3. Consider products beyond just {产品品类}, or any other accessory that enhances the overall product experience.
4. Conceptualize the products and services within the Co-creation and Collaborative ecosystems for {目标用户是谁}.
5. For each product or service within the ecosystem, explain its specific purpose and how it addresses a particular user need or pain point.
6. Explain the reasoning behind each choice, focusing on how each product contributes to the overall user experience.

Additional Information 1: When I mention that various products within a product ecosystem aim to enhance the overall user experience, I'm referring to addressing the following five needs based on the Jobs-to-Be-Done (JTBD) theory:
- Functional Jobs: The core tasks or problems a user needs to solve with a product
- Emotional Jobs: The psychological needs or feelings a user experiences
- Social Jobs: The user's social identity and status
- Related Jobs: Additional tasks that complement the main job

Additional Information 2: The products within the ecosystem should cater to different usage scenarios:
- Define: Identify and articulate the user's goal
- Locate: Determine necessary resources and tools
- Prepare: Organize and set up everything needed
- Confirm: Verify preparations are complete
- Execute: Carry out the tasks
- Monitor: Track progress during execution
- Modify: Adapt if issues arise
- Conclude: Complete and reflect

Format: Respond in Chinese.
Tone: Use precise vocabulary and clear syntax. Maintain a neutral, professional tone.
```

**调用注意事项**：
- 共创生态 vs 协作生态是两个独立产物，不能混写——前者是开放平台 + 第三方贡献，后者是互联互通 + 无缝体验。
- 8 阶段使用场景（Define → Conclude）是产物校验的覆盖维度，每个生态产物要能映射到其中至少 1 个阶段。
- Additional Information 1 原稿只列 4 项 Jobs（Functional / Emotional / Social / Related），prompt 自称「五维」但仅列 4——保留原稿如实呈现，不替原稿补救。

---

## Tool 9 — 访谈问题设计 Prompt for User Interview Questions Design

<a id="tool-9"></a>

**核心问题**：为定性深访设计覆盖 20 类心理维度的访谈问题列表，每类问题对应一个心理学功能。

**输入占位符**（agent 执行前必须替换）：
- `{说清楚用户访谈发生的背景，越详细越好，尤其是研究目标和受访人群特征}` —— 替换为：研究背景 + 目标 + 人群特征。
- `{说清楚谁是受访用户}` —— 替换为：受访用户具体描述（prompt 中出现多次）。
- `{说清楚要开发什么产品或者服务}` —— 替换为：要研发的下一代产品/服务名称。
- `{说清楚有关产品的设想}` —— 替换为：产品创新方向/假设列表。
- `{语言}` —— 替换为：访谈问卷语言（如「中文」/「English」）。

**期望输出**（来自原稿「使用示例 / 预期输出」段）：
- 20 种类型的访谈问题
- 每类 3-5 个具体问题
- 问题之间有逻辑递进关系

**Prompt（原稿原文，保持英文，复制即用）**：

```prompt
Role: You are a user research expert with 20 years of experience.

Client Context: {说清楚用户访谈发生的背景，越详细越好，尤其是研究目标和受访人群特征}. We are preparing to conduct user interviews with {说清楚谁是受访用户} to gather feedback, understand needs, and identify expectations that will inform the design and innovation of their next-generation {说清楚要开发什么产品或者服务}.

Task: Your task is to create a "User Interview Question List" that deeply empathizes with the experiences and concerns of {说清楚谁是受访用户}. Consider each need and pain point as you explore the following areas of innovation: {说清楚有关产品的设想}.

Question Types: For each area of innovation, design questions that cover the following aspects:

1. Background Questions: Activate self-narration to help respondents quickly enter a state of trust and self-disclosure.
2. Contextual Questions: Reconstruct lived moments to uncover the real motivations behind behavior.
3. Knowledge-Based Questions: Explore how people interpret the world rather than how much factual knowledge they possess.
4. Historical Questions: Reveal how past experiences have shaped the respondent's present self.
5. Attitude Questions: Expose the respondent's value system through surface stance, underlying reasons, and self-projection.
6. Cognitive Questions: Uncover the respondent's underlying cognitive schema by examining how they explain their own behavior.
7. Expectation Questions: Reveal the user's ideal self by exploring what future version of the product they imagine.
8. Competitive Questions: Show who or what the respondent is psychologically "competing with" through comparisons.
9. Social Questions: Uncover how individuals define themselves through the eyes of others and relational dynamics.
10. Frequency Questions: Identify behavioral rhythms and emotional patterns by recalling memorable usage moments.
11. Learnability Questions: Reveal psychological responses to new tools, including self-efficacy, cognitive limits, and motivation.
12. Barrier Questions: Expose the respondent's psychological defense structure through their reactions to frustration.
13. Compatibility Questions: Assess psychological alignment between the user and the product across function, emotion, and identity.
14. Recovery Questions: Reveal how respondents restore inner balance when systems fail or experiences break down.
15. Prioritization Questions: Expose value hierarchies and decision-making principles through forced trade-offs.
16. Redundancy Questions: Explore why users need "extra functions" to maintain psychological safety and control.
17. Relational Questions: Reveal how users form emotional attachment and psychological dependence on a product.
18. Implicit Questions: Surface unconscious motivations through metaphor, projection, and symbolic expression.
19. Hypothetical Questions: Use imagined scenarios to reveal hidden decision logic and latent desires.
20. Comparative Questions: Uncover the user's psychological reference system and value judgment framework through contrasts.

Requirements:
1. Clarity and Specificity: Ensure that each question is specific and easy to understand.
2. Child-Friendly Language: Avoid technical jargon to ensure that {说清楚谁是受访用户} can comprehend the questions.
3. Aided Recall: Use prompts to help {说清楚谁是受访用户} remember relevant experiences or details.
4. Conciseness: Keep questions brief to avoid overwhelming participants.
5. Neutrality: Avoid any bias or leading language that could influence responses.
6. Language: The entire "User Interview Question List" should be designed in {语言}.

Tone:
1. Friendly and Warm: Make {说清楚谁是受访用户} feel comfortable and at ease.
2. Neutral and Objective: Maintain a neutral tone to avoid any bias.
3. Clear and Concise: Ensure that questions are straightforward and easy to understand.
4. Supportive: Convey that the opinions and experiences are valued and important.
```

**调用注意事项**：
- 20 类问题必须全部覆盖，每个创新方向（areas of innovation）下都要展开。
- 「Child-Friendly Language」字面是儿童友好——原稿表达为「避免黑话让受访者听懂」，不限定儿童访谈语境。
- 每类问题 3-5 条、有递进。

---

## Tool 10 — 问卷问题设计 Prompt For Questionnaire Design

<a id="tool-10"></a>

**核心问题**：为定量调研设计覆盖 5 大维度（知识 / 评价 / 行为 / 频率 / 心理）、符合心理测量学五大效度标准的封闭式问卷。

**输入占位符**（agent 执行前必须替换）：
- `{说清楚用户访谈发生的背景，越详细越好，尤其是研究目标和样本人群特征}` —— 替换为：研究背景 + 目标 + 样本人群特征。
- `{样本人群特征与样本量}` —— 替换为：样本画像 + 计划样本量（如「美国智能家居用户 500 份」）。
- `{准备研发的产品}` —— 替换为：要研发的产品。
- `{问卷的名字}` —— 替换为：问卷正式名称。
- `{样本人群特征}` —— 替换为：样本画像描述（prompt 中出现多次）。
- `{说清楚有关产品的设想}` —— 替换为：3 个创新概念（prompt 中以列表形式占 3 行，需逐行填）。

**期望输出**（来自原稿「使用示例 / 预期输出」段）：
- 完整的问卷结构
- 每个创新概念 5-10 个问题
- 全部为封闭式问题（单选 / 李克特量表）

**Prompt（原稿原文，保持英文，复制即用）**：

```prompt
Role: You are a seasoned user research expert with 20 years of experience.

Client Background: {说清楚用户访谈发生的背景，越详细越好，尤其是研究目标和样本人群特征}. We are planning to conduct a comprehensive survey with {样本人群特征与样本量} to gather their genuine feedback, needs, and expectations. The ultimate goal is to guide the next phase of innovation in {准备研发的产品}.

Task: Your task is to design a {问卷的名字} that empathetically addresses the needs and pain points of {样本人群特征}. The questionnaire should explore key innovation concepts related to the product, such as visual appeal, interaction, technology, safety, and durability.

Innovation Concepts:
1. {说清楚有关产品的设想};
2. {说清楚有关产品的设想};
3. {说清楚有关产品的设想}.

Question Types: For each innovation concept, include the following question types:
1. Knowledge Questions: Assess their awareness and understanding of specific features.
2. Evaluation Questions: Collect feedback on the product's design, functionality, and quality.
3. Behavioral Questions: Investigate users' behaviors and inquire about their opinions on the product.
4. Frequency Questions: Understand how often certain behaviors occur.
5. Psychological Questions: Delve into the emotional and psychological reasons behind their preferences and choices.

Requirements:
1. Specificity: Ensure questions are clear and specific, making it easy for {样本人群特征}.
2. Appropriate Language: Avoid technical jargon, using language that is accessible to {样本人群特征}.
3. Aided Recall: Include prompts to help {样本人群特征} recall relevant events or experiences.
4. Conciseness: Keep questions brief to prevent overlooking key points.
5. Neutrality: Avoid leading questions to ensure unbiased responses.

Standards:
1. Factorial Structure: Ensure questions are logically connected and correlated.
2. Content Validity: The questionnaire should comprehensively cover all relevant aspects of the research objectives.
3. Discriminant Validity: Ensure questions measure distinct concepts without overlap.
4. Predictive Validity: Questions should be capable of predicting trends in product innovation.
5. Construct Validity: Each question should directly relate to the research objectives.

Language: The questionnaire must be designed in Chinese.

Tone:
1. Friendly and Kind: The tone should be welcoming, helping {样本人群特征} feel at ease.
2. Neutral and Objective: Maintain an unbiased and neutral tone throughout.
3. Clear and Concise: Ensure that the language is straightforward and easy to understand.
4. Supportive: Convey that the opinions and experiences are valuable.

Important Notes:
1. Avoid open-ended questions.
2. Focus on single-choice questions and Likert scales.
3. Ensure the questionnaire is quantifiable for easy analysis.
```

**调用注意事项**：
- 严禁开放题，全部封闭式（单选 / Likert）——这是 Tool 10 的核心硬约束。
- 5 大维度（Knowledge / Evaluation / Behavioral / Frequency / Psychological）必须在每个创新概念下都覆盖。
- 5 大效度标准（Factorial / Content / Discriminant / Predictive / Construct）是产物校验维度。

---

## 跨工具占位符约定

<a id="placeholders"></a>

10 个 prompt 块中出现的占位符及统一替换规则：

| 占位符（原稿原文） | 出现的工具 | 替换规则 |
|---|---|---|
| `{说清楚在哪个目标市场销售的面对哪个目标人群的什么产品}` | Tool 1 | 一句话写清：目标市场 + 目标人群 + 产品形态。例：「在美国市场销售的面向 25-45 岁科技爱好者的掌静脉智能门锁」。禁止只写产品名，必须含市场和人群。 |
| `{这里写什么产品}` | Tool 2、Tool 4 | 产品名称或一句话产品概念。Tool 4 中出现两次，替换值必须严格一致。 |
| `{在此粘贴产品介绍}` | Tool 3、Tool 3b | 产品功能介绍原文（功能列表、产品页文案或 PRD 摘要）。 |
| `{在此粘贴用户访谈或用户评论}` | Tool 3、Tool 3b | 用户访谈逐字稿或评论原文，**保留原始语气和口头语**，不要预先润色或归纳。 |
| `{目标用户是谁}` | Tool 6、Tool 7、Tool 8 | 具体目标用户群描述（含画像/场景），不能只写 demographic 标签。Tool 6 / Tool 7 / Tool 8 中各自出现多次，替换值在同一次运行内必须完全一致。 |
| `{在这里简述产品概念}` | Tool 6、Tool 7、Tool 8 | 产品概念的一句话描述（功能 + 用户价值）。Tool 7 / Tool 8 中出现多次，替换值必须一致。 |
| `{关键产品特征}` | Tool 8 | 产品核心特性列表（建议 2-4 条逗号分隔）。 |
| `{关键使用场景}` | Tool 8 | 核心使用场景描述（2-3 个典型场景）。 |
| `{产品品类}` | Tool 8 | 产品所在品类（用于生态扩展时识别「品类之外」的配套品）。 |
| `{说清楚用户访谈发生的背景，越详细越好，尤其是研究目标和受访人群特征}` | Tool 9 | 研究背景 + 研究目标 + 受访人群特征，多句段落不限长度。 |
| `{说清楚谁是受访用户}` | Tool 9 | 受访用户群具体描述。Tool 9 中出现多次，替换值必须严格一致。 |
| `{说清楚要开发什么产品或者服务}` | Tool 9 | 要研发的下一代产品或服务名称。 |
| `{说清楚有关产品的设想}` | Tool 9、Tool 10 | 产品创新方向 / 假设列表。Tool 10 中以三行列表出现，需逐行各填一个独立创新概念（共 3 个）。 |
| `{语言}` | Tool 9 | 访谈问卷使用的语言（如「中文」/「English」/「日本語」）。 |
| `{说清楚用户访谈发生的背景，越详细越好，尤其是研究目标和样本人群特征}` | Tool 10 | 研究背景 + 目标 + 样本人群特征（与 Tool 9 同类占位符语义相同，但样本量在 Tool 10 单列）。 |
| `{样本人群特征与样本量}` | Tool 10 | 样本画像 + 计划样本量（如「美国智能家居用户 500 份」）。 |
| `{准备研发的产品}` | Tool 10 | 要研发的产品名称。 |
| `{问卷的名字}` | Tool 10 | 问卷正式名称（用于问卷标题）。 |
| `{样本人群特征}` | Tool 10 | 样本画像描述。Tool 10 中出现多次，替换值必须严格一致。 |

**统一规则**：
1. 同一次运行中，同名占位符的替换值必须完全一致。
2. 替换后不要保留 `{` `}` 大括号或原占位符提示语进入最终产出。
3. 多次出现的占位符如果原稿有微小拼写差异（如 Tool 9 / Tool 10 的「访谈背景 / 调研背景」表述），按各自 prompt 原文替换，不跨工具借用。
4. 占位符内容如果包含敏感信息（用户隐私、未公开商业信息），替换前先脱敏。
