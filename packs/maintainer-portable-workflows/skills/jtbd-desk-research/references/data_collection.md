# JTBD 数据采集策略

> 本文档提供 Phase 1 数据采集的详细方法、平台策略、提取格式与质量检查清单。

---

## 采集策略总览

### Batch 优先级

- **必做（Must）**：Batch 1（Reddit）、Batch 2（Amazon）、Batch 3（论坛/社区）
- **在必做完成且有余力时执行（Should）**：Batch 4（App Store / Google Play）、Batch 5（YouTube）
- **可选（Nice to have）**：Batch 6（Product Hunt / Twitter / Kickstarter）

### 最低完成线

时间不足时，优先保证：
- 每个必做 Batch 至少完成 **50–70% 数量目标**
- 每个必做 Batch 覆盖到 **至少 3 种不同来源/子版块/ASIN**

---

## 平台采集方法

### 1. Reddit 采集

**目标 subreddit 示例**：
- r/MagicMirror, r/Parenting, r/HomeAutomation, r/Mommit, r/daddit

**关键词搜索示例**：
- morning routine, mental load, family calendar, hallway mirror, out the door

**排序策略**：
1. Top (All time) - 找高赞经典讨论
2. Relevance - 找最相关内容
3. New - 找最新讨论

**重点关注**：
- 高赞评论（≥10 upvotes）
- 长帖详述（≥200 字）
- 具体场景描述（有时间、地点、人物）
- 情感强烈表达（frustrated, love, hate, saved my life）

**提取示例**：
```markdown
**[R-MM-001]**
来源：Reddit r/MagicMirror · Show Your Mirror 帖
URL：https://reddit.com/r/MagicMirror/comments/xxxxx
原文：「I've got a mirror in the entry way so that I can glance at it on the way out and find out at a glance what's going on.」
Job 标签：J1, J3
四力标签：Pull
信号类型：需求表达
强度信号：45 upvotes
备注：门厅位置 + "at a glance" 反复出现
```

---

### 2. Amazon 评论采集

**目标产品示例**：
- Skylight Calendar (ASIN: B0XXXXX)
- Echo Show 15 (ASIN: B0XXXXX)
- Google Nest Hub Max (ASIN: B0XXXXX)

**筛选策略**：
- Verified Purchase（已验证购买）
- 3-5 星评论（含失望评论，不只看好评）
- 1-2 星评论（失败案例）

**重点关注**：
- "为什么买"（雇用时刻）
- "用了多久"（使用时长）
- "什么不满意"（解雇时刻）
- "和什么对比"（竞争对手）

**提取示例**：
```markdown
**[AM-SKY-001]**
来源：Amazon · Skylight Calendar 评论
URL：https://amazon.com/review/xxxxx
原文：「This is a good alternative to a normal calendar. We've really become reliant on this!」
Job 标签：J1
四力标签：Pull, Habit
信号类型：雇用时刻 / 情感表达
强度信号：Verified Purchase, 5 stars, 120 helpful votes
备注：「become reliant」= 强依赖信号
```

---

### 3. 论坛/社区采集

**目标论坛示例**：
- MagicMirror² Forum (forum.magicmirror.builders)
- Product Hunt 评论区
- Hacker News 讨论

**版块策略**：
- Show Your Mirror（展示作品）
- General Discussion（通用讨论）
- Troubleshooting（问题排查）

**重点关注**：
- DIY 动机（为什么要做？）
- 使用场景（放在哪里？怎么用？）
- 放弃原因（为什么不用了？）
- 技术问题（什么地方卡住了？）

**提取示例**：
```markdown
**[F-SYM-001]**
来源：MagicMirror Forum · Show Your Mirror · Hallway Notice Board
URL：https://forum.magicmirror.builders/topic/2585/...
原文：「For a while I've wanted to make my own mirror and decided to integrate it into a hallway notice board next to the front door. I like the MMM-Todoist Module, I use that to send my mirror messages from wherever I am as reminders.」
Job 标签：J1, J3
四力标签：Pull
信号类型：动机自述 / Workaround描述
强度信号：7+ 回复，高赞
备注：门厅 + 前门旁；Todoist 远程发提醒 = 非手机时刻触达
```

---

### 4. App Store/Google Play 采集

**目标 App 示例**：
- Cozi Family Organizer
- OurHome - Chores and Rewards
- TimeTree - Shared Calendar

**筛选策略**：
- 1-3 星评论（失望点）
- 5 星评论（雇用时刻）
- 最近 6 个月的评论（时效性）

**重点关注**：
- 功能缺失（想要但没有的）
- 使用摩擦（什么地方不方便？）
- 替代方案（之前用什么？）

---

### 5. YouTube/媒体评测采集

**搜索关键词示例**：
- [产品名] review
- [产品名] unboxing
- [产品名] setup tutorial

**重点关注**：
- 评论区用户讨论（比视频本身更有价值）
- 评测者提到的痛点
- 对比其他产品的评论

---

### 6. 其他渠道（可选）

- **Twitter/X**: 产品提及、用户抱怨
- **Kickstarter**: 众筹评论、更新讨论
- **Blog/Medium**: 用户故事、使用心得

---

## 提取格式规范

### 标准格式

```markdown
**[引用ID]**
来源：平台 · 版块/ASIN/频道名
URL：[直链]
原文：「……完整原文……」
Job 标签：J1/J2/J3/J4（可多选）
四力标签：Push / Pull / Anxiety / Habit
信号类型：痛苦陈述 / Workaround描述 / 雇用时刻 / 解雇时刻 / 需求表达 / 情感表达
强度信号：点赞数/评论数（如可获取）
备注：（可选，特殊上下文）
```

### 引用 ID 命名规范

- **Reddit**: `R-[SUB缩写]-[序号]`（如 R-MM-001, R-PAR-002）
- **Amazon**: `AM-[产品缩写]-[序号]`（如 AM-SKY-001, AM-ES15-002）
- **论坛**: `F-[论坛缩写]-[序号]`（如 F-SYM-001, F-MM-002）
- **App Store**: `AS-[App缩写]-[序号]`（如 AS-COZI-001）
- **YouTube**: `YT-[频道缩写]-[序号]`（如 YT-TECH-001）

---

## 信号强度标注

### 高强度信号（优先采集）

- Reddit: ≥50 upvotes
- Amazon: ≥100 helpful votes
- 论坛: ≥10 回复
- App Store: ≥50 helpful votes

### 中强度信号

- Reddit: 20-50 upvotes
- Amazon: 50-100 helpful votes
- 论坛: 5-10 回复
- App Store: 20-50 helpful votes

### 低强度信号（但内容有价值也采集）

- 具体场景描述
- 情感强烈表达
- 雇用/解雇时刻
- 反证样本

---

## 质量检查清单

### 每条引用必须有

- [ ] 完整原文（不截断语意）
- [ ] URL（如可获取）
- [ ] Job 标签（J1/J2/J3/J4）
- [ ] 四力标签（Push/Pull/Anxiety/Habit）
- [ ] 信号类型（6 种之一）

### 整体采集必须达到

- [ ] 总引用数 ≥50 条（必做 Batch 完成后）
- [ ] Reddit 引用 ≥20 条
- [ ] Amazon 引用 ≥15 条
- [ ] 论坛/社区引用 ≥10 条
- [ ] 每个 Batch 覆盖 ≥3 种不同来源/子版块
- [ ] 反证样本占比 15-30%
- [ ] 高强度信号已标注（点赞数/评论数）

---

## 常见问题

### Q1: 找不到相关讨论怎么办？

**A**: 在对应 Task 下注明"未找到相关讨论"，不猜测或填充。调整关键词或扩大搜索范围。

### Q2: 同一表达在多平台出现怎么办？

**A**: 只保留信息最完整的一条，其他平台在 `备注` 中通过 `multi-platform: Reddit + Amazon` 标注。

### Q3: 如何判断是否为反证样本？

**A**: 反证样本包括：
- 不认同问题严重性（"我觉得白板就够了"）
- 对现有方案满意（"我们用共享日历很好"）
- 质疑产品形态（"门厅镜太贵了，不值得"）

### Q4: 原文太长怎么办？

**A**: 保留完整原文，不截断。如果超过 500 字，可以在备注中标注"长引用"，但原文必须完整。

### Q5: 如何平衡采集速度和质量？

**A**:
- 优先采集高强度信号（高赞/高回复）
- 每个 Batch 先快速扫描，标记高价值帖子
- 再逐条提取，确保格式规范
- 时间不足时，保证必做 Batch 的最低完成线

---

**相关文档**：
- `execution_plan_template.md` - 执行计划模板
- `quality_checklist.md` - 质量审查清单
- `jtbd_theory.md` - JTBD 理论基础
