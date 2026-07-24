---
date: <YYYY-MM-DD>
type: research / tool-output
tool: tool01-product-soul
product: <产品代号或名称>
language: zh-CN
status: draft
version: v1.0
inputs:
  - "[[tool03_four_lens_<product>_<YYYYMMDD>]]"
  - "[[tool04_target_users_<product>_<YYYYMMDD>]]"
  - "[[tool06_emotional_social_<product>_<YYYYMMDD>]]"
  - <目标市场 / 目标人群 描述源>
---

# Tool 1 — 产品灵魂 Soul of Product

> **Product**：<产品代号或名称>
> **Stage**：Stage 3 洞察分析（紧接 Tool 3 之后；**不是开局**）
> **Methodology anchor**：Ernest Dichter 品牌心理学四维（核心问题 / 社会参照 / 国家文化 / 当代世界）
> **Prompt source**：`references/original_prompt_blocks.md#tool-1`
> **范本参考**：`examples/research_v4_日历机/tool01_product_soul_productFamilyAIHub.md`（v4 形态完整范本）
> **位置约束**：marketing-facing 段（§ 三灵魂段 / § 四广告语 / § 六-八内心独白）周围**禁 append v1 深化**（LB 表 / Bull's Eye / coverage matrix / B-F-H）。深化项放 § 九/十/十一 独立章节。详见 `references/v1_engineering_extensions.md` § 位置约束。

## v1 深化声明（产出顶部必填）

> **v1 深化声明**：已启用 [§ 九多角色变体（对应 v1 §4 B/F/H）/ § 十下游信号（对应 v1 §7）/ § 十一反触发（对应 v1 §2 正反需求）/ ...]；未启用 [...]（why not：[对照关闭场景理由]）。

## 上下文输入（执行前必填）

- **产品定义**：<...>
- **目标市场**：<...>
- **目标人群**：<...>（来自 Tool 4 锁版本）
- **上游 Tool 3 综合洞察**：`[[tool03_four_lens_<product>_<YYYYMMDD>]]`
- **上游 Tool 6 情感社交需求**：`[[tool06_emotional_social_<product>_<YYYYMMDD>]]`
- **语言要求**：zh-CN（广告语允许中英双语；§ 八允许独立英文段）

---

## 输出主体

### 一、四维心理分析 【必做 · 1218 硬约定】

#### 1. 核心问题（Core Problem）
<功能层 / 情感层 / 身份层张力——产品消失后用户最怀念什么；寻求"日常便利"还是"内在焦虑"的解脱；减轻哪种情绪负担；强化哪种正向状态>

#### 2. 社会参照框架（Sociological Frame of Reference）
<使用产品时用户希望他人感知的身份；产品在何种社交场景被展示；象征意义>

#### 3. 国家文化（National Culture）
<嵌入的国家/地区文化价值；放大的文化敏感性（仪式 / 可靠 / 精度等）；可用作锚点的文化符号或习语 2-3 个>

#### 4. 当代世界（Contemporary World）
<本时代的情绪与技术气候；产品回应的时代张力；10 年后哪些功能仍永恒、哪些会过时>

### 二、心理动机综合 【必做 · 1218 硬约定】

<从四维推出的潜意识动机——吸引/魅力、安全、尊重/自尊、归属、自我价值与掌握感、逃离/情绪释放；每条与四维证据对齐 + 引用 Tool 3 / Tool 6 上游 Q-ID 或洞察编号>

### 三、产品灵魂段 【必做 · 1218 硬约定 · marketing-facing 禁 append v1 深化】

<一段完整、有重量的灵魂段，150-250 字；说出未说之言，不是功能复述；产品消失后用户最怀念什么的 1 breath 描述>

**Trace**：上游 Q-ID / Tool 3 综合洞察句 / Tool 6 反向需求编号 1-2 个，单行不展开成表

### 四、广告语 × 5（情感共鸣，非功能陈述）【必做 · v1 深化扩展（3 → 5 条）· marketing-facing 禁 append v1 深化】

1. **中文**：<...>　**English**：<...>
2. **中文**：<...>　**English**：<...>
3. **中文**：<...>　**English**：<...>
4. **中文**：<...>　**English**：<...>
5. **中文**：<...>　**English**：<...>

> 1218 原稿硬约定下限是 3 条；v4 范本扩到 5 条作为推荐。少于 3 条 = 不合格；3 条 = 合格；5 条 = 推荐质量基线（覆盖功能信任 → 情感信任 → 关系信任 → 身份信任 → 时代信任）

### 五、广告的本质 【推荐 · 解释 slogan 设计哲学】

> 广告不是"介绍产品"。广告是：**在这个时代，对这样的人，这个产品表达了他们正在抵抗什么——以及他们在追求什么。**

| 抵抗什么 | 追求什么 |
|---|---|
| <用户当下身份/处境/情绪被什么挤压> | <用户想走向的身份/处境/情绪> |
| <8-12 条对位> | <8-12 条对位> |

**关闭场景**：纯 efficiency / B2B 工具产品，抵抗-追求二元结构不明显时可跳过。

### 六、用户内心独白——主视角（主决策者）【必做 · 1218 "用户内心独白" · marketing-facing 禁 append v1 深化】

> *<第一人称段落，约 200-400 字。讲一个具体的晚上 / 早晨 / 周末场景，把用户当下处境、内心独白、挫败感、渴望按时间顺序展开。结尾落到一句"我需要的是 ___"。>*

### 七、用户内心独白——配偶 / 协作者视角 【推荐 · 条件触发：Tool 4 含「配偶 / 协作者」类角色】

> *<第一人称段落，约 150-200 字。从配偶 / 协作者 / 第二决策者视角讲为什么"不是不想做、是不知道做什么"或类似张力。结尾落到"如果有 ___，我会愿意 ___"。>*

**关闭场景**：单角色产品 / 个人工具 / Tool 4 没识别出第二角色时可跳过。对应 v1 §4 B/F/H 角色变体的 H（Helper）轨。

### 八、内心独白英文版（精炼）【推荐 · 条件触发：B2C 出海 / 双语市场】

**主视角——精炼版**：
> *"<60-100 words English. 把 § 六核心张力压缩成 landing page 可直接引用的句子>"*

**配偶视角——精炼版**：
> *"<60-100 words English，同 § 七压缩>"*

**关闭场景**：单语市场 / 纯本地产品 / 不出海。

### 九、对多角色用户群的灵魂延伸 【推荐 · 条件触发：Tool 4 输出 ≥2 群】

> 产品灵魂的核心是为 [主目标群] 设计的——她/他是最痛、最愿意买单的人。但产品要成功留在 [使用场景] 里，灵魂必须延伸到 [其他相关角色]。

| 角色（来自 Tool 4） | 她/他的核心渴望 | 产品灵魂的延伸表达（一句话 marketing） | 对应创新概念（Tool 3b） |
|---|---|---|---|
| <主目标群 A> | <核心渴望> | "<一句 marketing 表达>" | <Tool 3b feature/concept ID> |
| <次要群 B> | <核心渴望> | "<一句>" | <...> |
| <协作群 H> | <核心渴望> | "<一句>" | <...> |
| <扩散群 D/F> | <核心渴望> | "<一句>" | <...> |

**对应 v1 深化**：§4 B/F/H 角色变体（Bull's Eye + 角色变体卷）。**关闭场景**：单群产品。

### 十、灵魂兑现路线图（Soul → Roadmap）【推荐 · 条件触发：研究产出喂下游 GTM / PRD / roadmap】

> 产品灵魂不是一次性交付的，而是随版本逐步兑现的。每个版本兑现灵魂的一个层面，让用户的信任阶梯式上升。

| 版本 | 品类阶段 | 兑现的灵魂层面 | 核心能力 | 用户感受（Aha 句） |
|---|---|---|---|---|
| **V1** | <品类阶段名 e.g. See + Think> | <第 1 层灵魂兑现> | <Tool 3b feature 1-2> | "<用户 Aha 一句>" |
| **V2** | <+ 下一阶段> | <第 2 层> | <feature 3-4> | "<用户 Aha 一句>" |
| **V3** | <+ 下一阶段> | <第 3 层> | <feature 5-N> | "<用户 Aha 一句>" |

**路线图背后的信任逻辑**：先用 V1 证明"___"（哪类信任）→ V2 证明"___" → V3 证明"___"。每一步都在为下一步积累用户信任资本。

**对应 v1 深化**：§7 下游信号台账（信任路线图 = 给 GTM / PRD 的关键信号）。**关闭场景**：研究不喂下游 GTM。

### 十一、必须回避的情感雷区 【推荐 · 条件触发：含 AI / 家庭 / 隐私敏感 / 自主性敏感场景】

> 反触发声明：本灵魂**承诺不做**什么。每条对应一类用户情感恐惧（来自 Tool 6 反向 / anxiety 类需求）。

| 雷区 | 为什么危险（trace 回 Tool 6 反向需求 R-X） | 如何回避（具体设计规则 / 文案规则） |
|---|---|---|
| <雷区 1 名> | <对应 Tool 6 R-X anxiety + 文化红线> | <具体怎么避：UI 规则 / 文案规则 / 默认设置 / 物理 affordance> |
| <雷区 2-5 同> | <...> | <...> |

**对应 v1 深化**：§2 正反两类需求拆分（反向 / anxiety 类的化解动作翻译成灵魂层反触发承诺）。**关闭场景**：纯 efficiency 工具 / 无 anxiety 维度产品。

---

## 自检（agent 必填，每条带证据 triple）

- [ ] **命名归位**：文件名 `tool01_product_soul_<product>.md` —— triple: (filename, this_file, L1)
- [ ] **YAML 完整 + version**：date / type / tool / product / language / status / version / inputs 八字段齐全 —— triple: (yaml_complete, this_file, L1-L13)
- [ ] **跨工具引用锁日期格式**：Tool 3 / Tool 4 / Tool 6 inputs 都用 `[[..._YYYYMMDD]]` —— triple per upstream
- [ ] **§ 一-§ 三硬约定全到位**：四维心理分析（4 子维齐）+ 心理动机综合 + 灵魂段（150-250 字 single breath）—— triple sample per §
- [ ] **§ 四广告语 ≥ 3 条**（推荐 5 条），每条中英双语 + 情感共鸣（非功能陈述）—— triple per slogan
- [ ] **§ 六内心独白主视角**：第一人称 / 具体场景 / 落到「我需要的是 ___」—— triple
- [ ] **位置约束合规（V3-P0-01 硬约束）**：§ 三灵魂段 / § 四广告语 / § 六-八内心独白周围**没**被 LB 表 / Bull's Eye / coverage matrix / B-F-H 矩阵 inline 包围；v1 深化全部在 § 九 / § 十 / § 十一 独立章节 —— triple: grep "LB-\|Bull.s Eye\|coverage matrix" 在 § 三-§ 八 范围 = 0
- [ ] **v1 深化声明完整**：产出顶部 § "v1 深化声明" 列出已启用项 + 关闭项 why not（对照 `references/v1_engineering_extensions.md` 关闭场景）—— triple
- [ ] **§ 九多角色变体**（若 Tool 4 ≥2 群）/ **§ 十路线图**（若喂下游 GTM）/ **§ 十一反触发**（若含 anxiety 维度）按条件触发 —— triple per § + 关闭场景声明
- [ ] **语言符合约定**：默认 zh-CN，广告语允许中英双语，§ 八允许独立英文 —— triple
- [ ] **不越边界**：本产出仅为用户洞察的可读化呈现，没有把广告语当品牌定稿；品牌定位 / 视觉识别 / 传播策略让位 `april-dunford-perspective` / `positioning-statement` —— triple: 一句话申明
- [ ] **机械 verify pass**：主上下文用 `references/verify.md` 的 grep 脚本验证本产出 triple 至少 5 条，全部 pass —— triple: (verify_log_path, parent_log, L_X)
