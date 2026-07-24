# RawQuotes 标注格式规范

> 每条评论的完整标注格式。Markdown 文件供人工阅读和审查；统计从 Structured CSV 做，不从 Markdown 解析。

---

## 单条评论模板

```markdown
**[{id}]** | Rating: {N} | Helpful: {N} | Verified: {Y/N} | {日期}
> "{评论完整原文，不截断，不用省略号}"

forces:
  - Push: {什么让用户对现状不满/想做出改变}（没有则省略整行）
  - Pull: {什么吸引用户购买/继续使用}（没有则省略整行）
  - Anxiety: {什么让用户犹豫/担心}（没有则省略整行）
  - Habit: {用户原来用什么替代方案/旧习惯}（没有则省略整行）
raw_job_satisfied:
  - "[功能] {用户表达满意/已实现的Job，用用户视角语言}"
  - "[情感] {...}"
  - "[社会] {...}"
raw_job_frustrated:
  - "[功能] {用户表达不满/失败/想要但没得到的Job}"
feature_satisfied:
  - "{已实现且用户满意的功能，用用户原话或自然语言}"
feature_implemented_frustrated:
  - "{已实现但用户不满意的功能}"
feature_requested:
  - "{用户明确希望有但目前不存在的功能}"
competitor_mentions: {竞品或替代方案，如 Skylight / whiteboard / iPad；无则省略整行}
anxiety_theme:
  - "{具体焦虑内容自由文本，仅在 forces 中有 Anxiety 时填写}"
signal_type: {hire_moment / fire_moment / workaround / wishlist}（可多选逗号分隔，没有则省略整行）
```

---

## 规则详解

### 原文引用
- `> "..."` 块内必须是**完整原文**，不能用「...」截断
- 如原文超长（>500字），仍须完整保留，不截断
- 语言保持原语言（英文评论保持英文）

### forces（四力）
- 按需标注，没有的力**省略整行**（不写「Push: 无」或「Push: N/A」）
- 描述用自然语言，不需要很长，抓住核心即可
- Push 例：「家庭日程分散在各自手机，出门前总要互相追问」
- Pull 例：「大屏幕、Google 日历同步、无月费」
- Anxiety 例：「担心每年 $79 订阅费是否值得」
- Habit 例：「之前用白板 + 磁铁贴纸」

### raw_job
- 前缀规则：`[功能]` = 完成具体任务；`[情感]` = 获得某种感受；`[社会]` = 在他人眼中呈现某种形象
- 一条评论可以有多条 raw_job（不限数量）
- 用「用户想达成的进展」描述，不是「评论说了什么功能」
  - ❌ `[功能] 使用了 Google 日历同步`
  - ✅ `[功能] 把夫妻双方日历同步到同一块屏幕，一眼看到全家安排`
- satisfied 和 frustrated 分开填，同一评论可以两者都有

### feature
- 三类分开填写，不混用
- 用具体功能名或用户原话，不用泛化描述
  - ❌ `好用的功能`
  - ✅ `Google 日历同步`、`挂墙安装模板`、`家务奖励积分系统`
- 不限数量，按评论实际提及填写

### anxiety_theme
- **仅在 forces 中有 Anxiety 时填写**（两者是上下级关系）
- 描述具体焦虑内容，不是「有焦虑」本身
  - ❌ `担心订阅`
  - ✅ `已付 $300+ 硬件，照片功能还需额外付 $79/年才能使用`

### signal_type
- `hire_moment`：评论描述了触发购买/雇用的具体场景
- `fire_moment`：评论描述了触发退货/解雇/差评的具体事件
- `workaround`：评论描述了用户自创的变通做法
- `wishlist`：评论明确列出了用户希望有的功能/改进
- 可多选（如 `hire_moment,workaround`）
- 没有明确信号时省略整行

---

## 文件头部模板

```markdown
---
date: {YYYYMMDD}
source_skill: jtbd-amazon-corpus
epistemic_status: empirical
description: {品类} Amazon {N}★ 评论全量 JTBD 标注，{条数}条，含四力/raw_job/feature/signal_type 完整字段。
type: Atomic_Note
tags: [JTBD, {品类}, 亚马逊, {N}星]
links:
  - [[task_plan]]
  - [[JTBD_Clusters_草稿_{品类}]]
---

# JTBD · RawQuotes · {品类} · {N}★

> 数据来源：`{原始CSV文件名}`（{N}★ 共 {条数} 条）
> 标注规范：`jtbd-amazon-corpus` skill v1.0

---
```

---

## 高价值评论筛选（RawQuotes 的抽样策略）

全量评论不一定全部写入 RawQuotes.md（1★~4★ 建议全量；5★ 如超 200 条可只写 helpful≥5 的高质量评论）。

**筛选优先级**：
1. `helpful` 值高（有用投票多，代表社区共鸣）
2. 原文详细（超过 3 句话的叙事性评论）
3. 包含 hire/fire 叙事（Before/After 结构，切换时间线）
4. 包含竞品对比
5. 包含 workaround 描述

**最低覆盖**：
- 每个星级至少 10 条（如总数不足 10 则全量）
- 必须覆盖所有出现过的 anxiety_theme 类型

---

## 实例（来自日历机 5★）

```markdown
**[5star-023]** | Rating: 5 | Helpful: 12 | Verified: True | 2024-11-15
> "We have been using this for about 3 months now and it has been a game changer for our family. My kids actually go and look at the calendar themselves to see what they have going on for the day — I no longer have to tell them 10 times. The Google Calendar sync works perfectly, setup took maybe 15 minutes. The chore system with points is a big hit. My only wish is that there was a screen lock so the kids can't accidentally mess up the calendar."

forces:
  - Pull: 大屏 Always On 可见性、Google 日历同步顺畅、家务积分系统
  - Habit: 之前口头提醒孩子日程，需要反复叮嘱
raw_job_satisfied:
  - "[功能] 孩子主动去屏幕查看今天的日程，不再需要父母反复提醒"
  - "[情感] 孩子获得日程自主权，父母从中间人角色解脱"
  - "[功能] 通过家务积分系统让孩子主动认领任务"
raw_job_frustrated:
  - "[功能] 家长控制或屏幕锁定，防止孩子意外修改日历"
feature_satisfied:
  - "Google 日历同步"
  - "家务奖励积分机制"
  - "整体产品体验"
feature_requested:
  - "家长控制/屏幕锁定功能"
signal_type: hire_moment,wishlist
```
