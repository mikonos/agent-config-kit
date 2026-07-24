---
date: <YYYY-MM-DD>
type: research / tool-output
tool: tool09-interview-questions
product: <产品代号或名称>
language: zh-CN
status: draft
inputs:
  - <研究背景描述>
  - <受访人群特征来源（可引 Tool 4）>
  - <产品设想来源>
---

# Tool 9 — 访谈问题设计 User Interview Questions Design
> Product: <产品代号或名称>
> Stage: Stage 2 需求挖掘（先于实际访谈执行；执行后产出回流到 Tool 3）
> Prompt source: `references/original_prompt_blocks.md#tool-9`
> Methodology anchor: `references/methodology_foundations.md` § 访谈心理学 20 种问题类型

## 上下文输入（执行前必填）

- **研究背景**（越详细越好，含研究目标 + 受访人群特征）：<...>
- **受访用户**（建议引 Tool 4 群体）：`[[tool04_target_users_<product>_<date>]]` § 群 Q<n>
- **产品设想**（创新方向 1-N）：<...>
- **访谈语言**：<默认 Chinese；可指定其他>

## 输出主体（20 类问题，每类 3-5 题，递进有序）

> 每类问题：先 1 句类别意图（≤20 字），再列 3-5 题；中文表述；遵循 Clarity / Child-Friendly / Aided Recall / Conciseness / Neutrality 五原则；Tone: Friendly + Neutral + Clear + Supportive。

### 1. Background Questions（背景问题）
- 类别意图：<激活自我叙述，建立信任与自我披露>
- 题 1：<...> / 题 2：<...> / 题 3-5：<...>

### 2. Contextual Questions（情境问题）
- 类别意图：<重建真实使用时刻，挖掘行为背后的真实动机>
- 题 1-5：<...>

### 3. Knowledge-Based Questions（知识型问题）
- 类别意图：<了解用户如何解读世界，而非考事实知识>
- 题 1-5：<...>

### 4. Historical Questions（历史问题）
- 类别意图：<过去经验如何塑造当下的他>
- 题 1-5：<...>

### 5. Attitude Questions（态度问题）
- 类别意图：<经由表层立场暴露价值系统>
- 题 1-5：<...>

### 6. Cognitive Questions（认知问题）
- 类别意图：<揭示用户如何解释自己的行为>
- 题 1-5：<...>

### 7. Expectation Questions（期望问题）
- 类别意图：<想象的未来产品揭示理想自我>
- 题 1-5：<...>

### 8. Competitive Questions（竞争问题）
- 类别意图：<显示他心理上在与谁/什么对比>
- 题 1-5：<...>

### 9. Social Questions（社交问题）
- 类别意图：<通过他人之眼定义自己>
- 题 1-5：<...>

### 10. Frequency Questions（频率问题）
- 类别意图：<行为节律与情绪模式>
- 题 1-5：<...>

### 11. Learnability Questions（可学习性问题）
- 类别意图：<对新工具的心理反应：自我效能感、认知极限、动机>
- 题 1-5：<...>

### 12. Barrier Questions（障碍问题）
- 类别意图：<挫败反应揭示心理防御结构>
- 题 1-5：<...>

### 13. Compatibility Questions（兼容性问题）
- 类别意图：<在功能 / 情感 / 身份维度评估用户与产品的对齐度>
- 题 1-5：<...>

### 14. Recovery Questions（恢复问题）
- 类别意图：<系统失效或体验崩坏时如何恢复内在平衡>
- 题 1-5：<...>

### 15. Prioritization Questions（优先级问题）
- 类别意图：<强制取舍暴露价值层级>
- 题 1-5：<...>

### 16. Redundancy Questions（冗余问题）
- 类别意图：<为什么需要"多余功能"维持心理安全感>
- 题 1-5：<...>

### 17. Relational Questions（关系问题）
- 类别意图：<情感依附与心理依赖如何形成>
- 题 1-5：<...>

### 18. Implicit Questions（隐性问题）
- 类别意图：<通过隐喻、投射、象征表达浮现潜意识动机>
- 题 1-5：<...>

### 19. Hypothetical Questions（假设问题）
- 类别意图：<假想情境暴露隐藏决策逻辑与潜在欲望>
- 题 1-5：<...>

### 20. Comparative Questions（比较问题）
- 类别意图：<通过对比揭示心理参考系与价值判断框架>
- 题 1-5：<...>

### 问题间的递进逻辑（执行排序建议）

<给一个建议的访谈执行排序，例如 1→4→3→5→6→...→18→19→20；标注高敏感类（如 Implicit / Hypothetical）建议放在信任建立之后>

---

## 自检（agent 必填，每条带证据）

- [ ] **命名归位**：文件名 `tool09_interview_questions_<product>.md` —— 证据：本文件名为 `___`
- [ ] **YAML 完整**：date / type / tool / product / language 五字段齐全 —— 证据：第 1-N 行
- [ ] **跨工具引用锁版本**：Tool 4 受访群体引用用 `[[...]]` + 日期 —— 证据：第 X 行 / 本工具无上游
- [ ] **格式硬约定**：**20 类问题全覆盖**（Background → Comparative 一类不漏）；每类 3-5 题；遵循 Clarity / Child-Friendly / Aided Recall / Conciseness / Neutrality 五原则；Tone: Friendly + Neutral + Clear + Supportive —— 证据：列出 20 类标题对应章节号 + 抽样 1 题验证中性表述
- [ ] **语言符合约定**：默认 zh-CN（Tool 9 允许指定其他语言）—— 证据：整篇语言判定
- [ ] **不越边界**：本产出是访谈题库，**20 类已全覆盖、敏感类（Implicit / Hypothetical）也没漏**；不是切换购买访谈大纲（让位 `bob-moesta-perspective`），也不是问卷（让位 Tool 10）—— 证据：一句话申明 + 全覆盖证据
- [ ] **v1 扩展声明**：未用 v1 深化 / 用了 v1 深化（如承重假设嵌入 probe tree、Steve Portigal 追问策略合并）—— 证据：产出顶部声明位置
