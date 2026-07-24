# JTBD Workaround 提取框架

> 本文档提供 Phase 4 Workaround 目录的详细方法、竞争地图绘制与质量检查清单。

---

## Workaround 定义

**Workaround**：用户现在用什么方式"雇用"来解决这个 Job？

**关键洞察**：Workaround 不只是产品，还包括：
- 物理工具（白板、便利贴、纸质日历）
- 数字工具（App、共享日历、群消息）
- 人工流程（口头提醒、重复确认）
- 非消费（什么都不用，靠记忆）

---

## 提取框架

### Workaround 目录格式

```markdown
## 3.3 Workaround 目录

| Workaround | 描述 | 信号强度（引用数） | 为什么不够好（用户原话/归纳） |
|-------------|------|---------------------|------------------------------|
| 白板/纸质日历 | 门口挂白板写提醒 | 5 条 | 「half the time no one looks at it」 |
| 共享数字日历 | Google Calendar 共享 | 8 条 | 「we both have to remember to check」 |
| 口头提醒 | 每天早上口头确认 | 6 条 | 「I'm the only one who remembers」 |
| DIY 智能镜 | MagicMirror² DIY | 4 条 | 「Too much maintenance, modules break」 |
| 智能音箱 | Echo Show 15 | 3 条 | 「disappointing display, widget 受限」 |
| 非消费 | 什么都不用，靠记忆 | 2 条 | 「mental load is breaking me」 |
```

---

## 识别方法

### 1. 直接表达

用户明确说"我现在用..."

**示例**：
- 「We use a whiteboard by the front door for reminders」
- 「I've always used Google Calendar」
- 「Just use a shared app」

### 2. 行为暗示

用户描述行为，暗示 workaround

**示例**：
- 「Every morning I have to remind everyone」→ 口头提醒
- 「I write everything on sticky notes」→ 便利贴
- 「I text my wife the schedule」→ 群消息

### 3. 失败案例

用户说"我试过...但不行"

**示例**：
- 「Stopped using my MagicMirror after 3 months」→ DIY 智能镜
- 「The app is buggy and syncing issues made it unreliable」→ 共享 App

---

## 失败原因分析

### 分类框架

**功能不足**：
- 缺少关键功能
- 功能不够强大
- 无法满足需求

**使用摩擦**：
- 需要主动检查（不是被动可见）
- 需要多步操作（太复杂）
- 需要记住去用（容易忘记）

**技术问题**：
- 维护复杂（DIY 方案）
- 同步不稳定（共享 App）
- 设备故障（硬件问题）

**社交阻力**：
- 家人不接受（太复杂、不喜欢）
- 只有一人维护（心理负荷不均）
- 需要协调多人（太麻烦）

**成本问题**：
- 太贵（订阅费、硬件成本）
- 不值得（收益 < 成本）
- 有免费替代（白板、App）

---

## 竞争地图绘制

### 三层竞争

**直接竞争**：同类产品
- Skylight Calendar
- Echo Show 15
- Google Nest Hub Max
- DIY MagicMirror²

**间接竞争**：替代方案
- 白板/纸质日历
- iPad 挂墙
- 共享数字日历（Google Calendar, Cozi）
- 群消息（WhatsApp, WeChat）

**非消费**：什么都不用
- 靠记忆
- 口头提醒
- 重复确认

### 竞争地图格式

```markdown
## 竞争地图

### 直接竞争（同类产品）
- **Skylight Calendar**：礼物型数字相框 + 家庭日历，$159 + 订阅
  - 优势：简单易用、礼物定位
  - 劣势：订阅费、功能受限
  - 用户原话：「good alternative to a normal calendar」

- **Echo Show 15**：智能音箱 + 墙面屏
  - 优势：语音控制、智能家居集成
  - 劣势：触控减少、widget 受限、音质差
  - 用户原话：「disappointing display」

### 间接竞争（替代方案）
- **白板/纸质日历**：门口挂白板
  - 优势：简单、便宜、可靠
  - 劣势：需要主动看、容易忘记
  - 用户原话：「half the time no one looks at it」

- **共享数字日历**：Google Calendar 共享
  - 优势：免费、同步、多设备
  - 劣势：需要主动打开、手机依赖
  - 用户原话：「we both have to remember to check」

### 非消费（什么都不用）
- **靠记忆 + 口头提醒**
  - 优势：零成本
  - 劣势：心理负荷重、容易忘记、家庭冲突
  - 用户原话：「mental load is breaking me」
```

---

## 真正的竞争对手

### 关键洞察

**真正的竞争对手不是同类产品，而是用户现在的 workaround。**

### 识别方法

1. **看信号强度**：哪个 workaround 的引用数最多？
2. **看使用时长**：用户用了多久？
3. **看满意度**：用户说"good enough"还是"frustrated"？

### 示例

**product 门厅镜的真正竞争对手**：
1. **白板/纸质日历**（5 条引用）- 最常见的 workaround
2. **共享数字日历**（8 条引用）- 最多人在用
3. **口头提醒**（6 条引用）- 最原始的方式

**不是**：
- Skylight Calendar（3 条引用）- 小众产品
- Echo Show 15（3 条引用）- 失望评论多

---

## 差异化洞察

### 从 Workaround 失败原因中提取

**所有失败方案的共同点是什么？**

**product 门厅镜示例**：
- 白板：「没人看它」→ 需要主动检查
- 共享 App：「需要记得打开」→ 需要主动检查
- DIY 镜：「维护复杂」→ 技术门槛高
- Echo Show：「widget 受限」→ 功能不够

**共同点**：需要主动检查 + 技术复杂

**差异化方向**：
1. **被动可见性**：信息主动出现，不需要检查
2. **简单可靠**：零维护，开箱即用

---

## 质量检查清单

### Workaround 目录必须有

- [ ] 列出 ≥5 种 workaround
- [ ] 每种 workaround 有描述
- [ ] 每种 workaround 有信号强度（引用数）
- [ ] 每种 workaround 有失败原因（用户原话或明确归纳）

### 竞争地图必须有

- [ ] 识别出直接竞争（同类产品）
- [ ] 识别出间接竞争（替代方案）
- [ ] 识别出非消费（什么都不用）
- [ ] 明确真正的竞争对手（不只是同类产品）

### 差异化洞察必须有

- [ ] 所有失败方案的共同点
- [ ] 基于共同点的差异化方向
- [ ] 差异化方向基于数据（不是推测）

---

## 常见问题

### Q1: 如何判断哪个是真正的竞争对手？

**A**: 看三个维度：
1. 信号强度（引用数最多的）
2. 使用时长（用户用了多久？）
3. 满意度（用户说"good enough"还是"frustrated"？）

通常，**间接竞争（替代方案）比直接竞争（同类产品）更重要**。

### Q2: 如何识别隐性的 workaround？

**A**: 观察用户行为：
- 用户说"我每天早上..."→ 可能是口头提醒
- 用户说"我会写在..."→ 可能是便利贴/白板
- 用户说"我们用..."→ 可能是共享 App

### Q3: 非消费（什么都不用）算竞争对手吗？

**A**: 算！而且往往是最大的竞争对手。

**原因**：
- 零成本
- 零学习成本
- 零切换成本

**挑战**：如何让用户从"什么都不用"切换到"用你的产品"？

### Q4: 如何从 Workaround 失败原因中提取差异化洞察？

**A**: 三步法：
1. 列出所有 workaround 的失败原因
2. 找共同点（所有失败方案都有什么问题？）
3. 反向设计（如何避免这些问题？）

---

**相关文档**：
- `data_collection.md` - 数据采集策略
- `job_validation.md` - Job 验证框架
- `forces_analysis.md` - 四力分析方法
- `hiring_firing.md` - 雇用/解雇时刻挖掘
