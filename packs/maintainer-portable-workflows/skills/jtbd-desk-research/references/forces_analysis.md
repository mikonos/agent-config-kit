# JTBD 四力分析方法

> 本文档提供 Phase 3 四力分析的详细方法、识别关键词与质量检查清单。

---

## 四力定义

### Push（推力）：当前痛点

**定义**：用户当前遇到的痛点、不满、焦虑，推动他们寻找新解法。

**识别关键词**：
- frustrated, chaos, breaking me, forget, drives me crazy
- 受够了, 每次都忘, 太麻烦, 烦死了

**识别句式**：
- "I'm so frustrated with..."
- "Every morning we..."
- "I always forget..."
- "It drives me crazy that..."

**重点**：
- 高频痛点（多次出现）
- 情感强烈的表达（breaking me, chaos）
- 具体场景描述（不是泛泛抱怨）

---

### Pull（拉力）：期望收益

**定义**：用户期望的收益、吸引力，拉动他们采用新解法。

**识别关键词**：
- want, wish, love, transformed, become reliant, saved my life
- 想要, 希望有, 太好了, 离不开

**识别句式**：
- "I want..."
- "Wish there was..."
- "Love this feature..."
- "Transformed my..."
- "Become reliant on..."

**重点**：
- 具体期望（不是泛泛的"更好"）
- 成功案例的收益描述
- 强依赖信号（become reliant, can't live without）

---

### Anxiety（焦虑）：对新方案的顾虑

**定义**：用户对新方案的担心、顾虑，阻止他们采用新解法。

**识别关键词**：
- too complex, expensive, unreliable, maintenance, won't let me
- 太贵, 太复杂, 不靠谱, 担心, 不会用

**识别句式**：
- "Too expensive..."
- "Too complex for..."
- "Worried about..."
- "What if it breaks..."
- "My wife won't let me..."

**重点**：
- 技术门槛（太复杂、不会用）
- 价格顾虑（太贵、不值得）
- 可靠性担心（会不会坏、稳不稳定）
- 家庭接受度（家人不让、不喜欢）

---

### Habit（习惯）：现有惯性

**定义**：用户现有的习惯、替代方案，阻止他们改变。

**识别关键词**：
- use, currently, whiteboard, shared app, good enough
- 一直在用, 习惯了, 够用了, 就这样吧

**识别句式**：
- "We currently use..."
- "I've always done..."
- "Good enough for now..."
- "Just use a whiteboard..."

**重点**：
- 现有 workaround（白板、App、口头提醒）
- 为什么还在用（够用、习惯了、懒得换）
- 切换成本（要学新东西、要花钱）

---

## 提取框架

### 四力图谱格式

```markdown
## 3.2 四力图谱

| 标签 | 代表原话（≥5 条） |
|------|-------------------|
| **Push** | 「原话1」「原话2」「原话3」「原话4」「原话5」 |
| **Pull** | 「原话1」「原话2」「原话3」「原话4」「原话5」 |
| **Anxiety** | 「原话1」「原话2」「原话3」「原话4」「原话5」 |
| **Habit** | 「原话1」「原话2」「原话3」「原话4」「原话5」 |
```

### 原话选择标准

1. **用户原文**（不是总结）
2. **情感强度**（frustrated/love/hate）
3. **具体场景**（不是泛泛而谈）
4. **高强度信号**（高赞/高回复）

---

## 四力强度对比

### 为什么重要

四力的相对强度决定了市场机会是否成立。

### 对比公式

```
如果 Push + Pull > Anxiety + Habit
→ 市场机会成立

如果 Push + Pull < Anxiety + Habit
→ 市场机会不成立或需要降低 Anxiety/Habit
```

### 强度评分方法

**Push 强度**（1-10 分）：
- 引用数量（≥10 条 = 8-10 分，5-9 条 = 5-7 分，<5 条 = 1-4 分）
- 情感强度（breaking me/chaos = 9-10 分，frustrated = 6-8 分，不满 = 3-5 分）
- 频率（每天 = 9-10 分，每周 = 6-8 分，偶尔 = 3-5 分）

**Pull 强度**（1-10 分）：
- 引用数量（同上）
- 情感强度（saved my life/transformed = 9-10 分，love = 6-8 分，want = 3-5 分）
- 依赖程度（can't live without = 9-10 分，become reliant = 6-8 分，nice to have = 3-5 分）

**Anxiety 强度**（1-10 分）：
- 引用数量（同上）
- 顾虑严重性（won't let me/too expensive = 7-10 分，worried = 4-6 分，有点担心 = 1-3 分）
- 阻止程度（完全阻止 = 9-10 分，犹豫 = 4-6 分，小顾虑 = 1-3 分）

**Habit 强度**（1-10 分）：
- 引用数量（同上）
- 使用时长（≥5 年 = 9-10 分，1-5 年 = 6-8 分，<1 年 = 3-5 分）
- 满意度（very satisfied = 9-10 分，good enough = 6-8 分，不太满意 = 3-5 分）

### 示例

**product 门厅镜研究**：
- Push = 8/10（「mental load breaking me」情感强烈，10+ 条引用）
- Pull = 7/10（「transformed schedule」「become reliant」，8+ 条引用）
- Anxiety = 6/10（「维护复杂」「月费」但不致命，6+ 条引用）
- Habit = 5/10（白板/App 但都不满意，5+ 条引用）

**结论**：Push + Pull (15) > Anxiety + Habit (11) → **市场机会成立**

---

## 四力关系图

### 进展力量模型

```
旧方案 ────────────────────────> 新方案
   │                              │
   │  Push (推离旧方案)            │
   │  ↓                           │
   │  Habit (拉回旧方案)           │
   │  ↑                           │
   │                              │
   │  Pull (拉向新方案)            │
   │  ↓                           │
   │  Anxiety (推离新方案)         │
   │  ↑                           │
   └──────────────────────────────┘
```

### 关键洞察

1. **Push 和 Habit 是对立的**：Push 推离旧方案，Habit 拉回旧方案
2. **Pull 和 Anxiety 是对立的**：Pull 拉向新方案，Anxiety 推离新方案
3. **切换发生在**：Push + Pull > Anxiety + Habit 的时刻

---

## 质量检查清单

### 每个力量必须有

- [ ] ≥5 条代表原话
- [ ] 原话是用户原文（不是总结）
- [ ] 原话有情感强度（frustrated/love/hate）
- [ ] 原话有具体场景（不是泛泛而谈）

### 四力强度对比必须有

- [ ] Push 和 Pull 的强度可对比（哪个更强？）
- [ ] Anxiety 和 Habit 的阻力可量化（多大阻力？）
- [ ] 四力强度对比有明确结论（Push + Pull vs Anxiety + Habit）
- [ ] 结论基于数据（不是推测）

---

## 常见问题

### Q1: 如何判断四力的强度？

**A**: 看三个维度：
1. 引用数量（≥10 条 = 强，5-9 条 = 中，<5 条 = 弱）
2. 情感强度（breaking me/saved my life = 强，frustrated/love = 中，不满/want = 弱）
3. 频率/依赖度（每天/can't live without = 强，每周/become reliant = 中，偶尔/nice to have = 弱）

### Q2: 如何处理一条引用包含多个力量的情况？

**A**: 一条引用可以标注多个四力标签。例如：
- 「I'm frustrated with the whiteboard (Push), but I'm worried a smart mirror is too complex (Anxiety)」
- 这条引用同时包含 Push 和 Anxiety

### Q3: 如何识别隐性的 Anxiety 和 Habit？

**A**:
- **隐性 Anxiety**：用户没说担心，但行为显示犹豫（如"我再想想"）
- **隐性 Habit**：用户没说满意，但一直在用（如"就这样吧"）

### Q4: 四力强度对比的结论应该怎么写？

**A**: 格式：
```markdown
**四力强度对比**：
- Push = X/10（说明）
- Pull = X/10（说明）
- Anxiety = X/10（说明）
- Habit = X/10（说明）

**结论**：Push + Pull (总分) > Anxiety + Habit (总分) → 市场机会成立/不成立
```

---

**相关文档**：
- `data_collection.md` - 数据采集策略
- `job_validation.md` - Job 验证框架
- `workaround_catalog.md` - Workaround 提取框架
- `jtbd_theory.md` - JTBD 理论基础
