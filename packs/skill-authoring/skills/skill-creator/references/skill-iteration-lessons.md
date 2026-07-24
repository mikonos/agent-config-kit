# 从真实 skill 改进中沉淀的经验

> 本文档来自对 **file-organize** skill 一轮迭代的复盘。用「写 skills 最好的人」的视角提炼可复用原则，并映射到 skill-creator 的既有规范，供后续新建/迭代 skill 时参考。
> 适用：迭代现有 skill、评审 skill 质量、做「专家模拟」时。

---

## 1. 改进来源与背景

**对象**：file-organize（文件/笔记归类 + 用 03_索引 实现 MOC 入网）

**主要改动**：合并 workflow 入 SKILL；description 只做路由、不写执行细节；两大流程（归位/入网）显式化并注明「何时读什么」；入网在本 skill 内闭环；设计原则与杜威表减重；必做拆成归位/入网并写明入网前先读 reference。

---

## 2. 好的地方 → 根因 → 可复用经验

| 好的地方（现象） | 根因（为什么好） | 可复用经验（原则） |
|------------------|------------------|---------------------|
| **两大流程一表说清，且标明「何时读什么」** | Agent 一眼知 scope，且知道做入网时要加载哪份 reference，不会漏读 | **多阶段/多流程 skill**：在 body 开头用表概括「流程名 / 做什么 / 何时读什么」；在必做里按流程分条，对依赖 reference 的阶段写死「先读 references/X 再执行」 |
| **Description 只含「做什么 + Use when」** | 路由阶段只看 description；执行细节在 body 里，避免 description 膨胀且与 body 重复 | **Description 只做触发**：不写路径、不写步骤、不写例外列表；只写能力一句话 + 「Use when [典型触发句]」。执行规则全部放在 body 或 references |
| **入网闭环在本 skill，不依赖 index-note** | 执行时心智负担小，不会「先 A 再调 B」导致漏步或上下文切换 | **能闭环就闭环**：若某流程可在本 skill 的 reference 里写全步骤，就不要设计成「本 skill 只做一半，另一半请调另一个 skill」；跨 skill 依赖会增加漏读与不一致 |
| **设计原则压缩、杜威表压成一行** | 低频或历史兼容内容占 token 多却很少被用；压成一行或迁到 reference 可减重 | **减重优先**：重复的表述合并；低频用的表/列表压成一行枚举或移到 reference；body 只保留「每次执行都会用到」的决策表与必做 |
| **「必做」按流程拆成归位 / 入网** | 执行顺序与加载顺序清晰：先归位（本页），再视需要入网（先读某 reference） | **必做与加载绑定**：若某步依赖 reference，在该步直接写「先读 references/X，再按其中步骤执行」 |
| **用「写 skills 最好的人」模拟评审** | 以专家标准自检：context、progressive disclosure、无重复、触发清晰 | **迭代时做专家模拟**：问「若由设计 Anthropic skill 规范的人来审，会挑哪些问题？」并逐项改进 |

---

## 3. 在 skill-creator 中的体现

| 经验 | 在 skill-creator 中的对应 |
|------|---------------------------|
| 多流程时表概括 + 何时读什么 | **Progressive Disclosure** 已有「reference 要从 SKILL 明确引用并说明 when to read」；可加强为：**多阶段 skill 在 body 开头用表列出「阶段 / 做什么 / 何时读什么」** |
| Description 只做触发 | **Frontmatter** 已要求 description 含 what + when；可加强为：**不在 description 里写实现细节（路径、步骤、例外表），只写能力句 + Use when 触发句** |
| 能闭环就闭环 | 当前未显式写；可新增一条 **「Skill 边界」**：**尽量在本 skill 内闭环；若必须依赖其他 skill，在 body 中明确写调用时机与契约** |
| 减重 / 低频压成一行或迁出 | **Avoid duplication** 与 **Concise is Key** 已覆盖；可补充：**低频或历史兼容内容**用一行枚举或迁到 reference，避免大表占 body |
| 必做与加载绑定 | **Progressive Disclosure** 的「describe clearly when to read」可细化：**在必做/步骤里对依赖 reference 的步骤写「先读 references/X」** |
| 迭代时专家模拟 | **Step 6: Iterate** 可增加：**迭代后做一次「专家模拟评审」并沉淀可复用教训，考虑更新本 skill 的 guidance（见本 reference）** |

---

## 4. 迭代/评审时的自检清单（来自本次复盘）

- [ ] **触发**：Description 是否只含「做什么 + Use when」，没有实现细节？
- [ ] **闭环**：是否避免了「做完 A 再调 B skill」的设计？若必须跨 skill，是否写清调用时机？
- [ ] **何时读什么**：多阶段时是否在表或必做里写死「做 X 时先读 references/Y」？
- [ ] **减重**：是否有重复表述或低频大表可压成一行/迁到 reference？
- [ ] **必做与阶段**：必做是否按阶段拆分，且对依赖 reference 的步骤写明「先读再执行」？
- [ ] **专家模拟**：若由「写 skills 最好的人」审一遍，还会改哪几处？

---

## 5. developer-toolkit Eval+Improve 教训（2026-04-06）

**来源**：developer-toolkit skill 重构 + 5 个测试用例运行

| 教训（现象） | 根因 | 可复用原则 |
|-------------|------|-----------|
| 路由表写"gstack（找对应工具）"——模型不知具体用哪个 | 工具类名 vs 具体 skill 名是不同的抽象层级；路由表应给出可执行的最小单元 | **路由表给具体 skill 名**，不给抽象工具类；模型执行时不需要再做一次查找 |
| Step 0（读产出）是建议不是强制，模型会跳过直接给答案 | 隐含假设不如显式声明；技能文件里的"应该"≈模型会忽略 | **强制约束必须显式写**："必须先执行 Step 0，不允许跳过"比"先读产出"有力得多 |
| 输出格式说"最多3条"，但没强调只给一个工具，结果给了两个 | 表格允许多行，输出格式约束不精确 | **"唯一"原则要写在输出格式里**，不是依赖表格单元格隐含；精确约束 > 模糊建议 |

**映射到 skill-creator 既有原则**：

- 路由表给具体名 → 补充"Routing table should list specific skill names, not abstract tool categories"
- 强制约束显式 → 补充"Critical constraints (must/must not) need explicit wording, not implied assumptions"
- 输出唯一原则 → 补充"Output format constraints should be explicit and exclusive, not tabular-optional"

---

## 6. 与本 skill（skill-creator）的衔接

- **创建/更新 skill 时**：按 SKILL.md 的 Core Principles、Progressive Disclosure、Step 4 执行。
- **迭代现有 skill 时**：在 Step 6 执行后，用本节「自检清单」过一遍，并将反复出现的教训纳入本 reference 或回写 SKILL.md。
- **评审质量时**：可模拟「写 skills 最好的人」视角，用本 reference 的表格与自检清单做一次 pass。
