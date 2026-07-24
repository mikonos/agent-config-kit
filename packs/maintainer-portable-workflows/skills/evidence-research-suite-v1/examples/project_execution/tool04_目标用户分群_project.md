# 工具4：目标用户识别 — product AI-Native 家庭日历机

> **方法论**：基于 JTBD（Jobs to be Done）框架的用户分群  
> **产品**：product — AI-Native 家庭日历机 / 家庭 AI 中心  
> **核心概念**：持久型 AI × 家庭感知网络，以大屏日历为界面、以 AI 引擎连接日程管理、Prepare 清单、家庭任务协同、家庭会议主持等场景

---

## 一、分群坐标系定义

基于 MECE 原则，我们选取两个**互斥对立**的属性维度构建四象限：

- **X 轴**：「被动式管理 ←→ 主动式规划」  
  - 被动式管理：日程变化时才响应、被通知后才行动、不提前规划  
  - 主动式规划：提前安排下周/下月、主动检查冲突、会花时间系统整理

- **Y 轴**：「个人时间焦点 ←→ 家庭协同焦点」  
  - 个人时间焦点：关注自身日程效率、个人时间块管理、习惯养成  
  - 家庭协同焦点：管理全家日程、协调多成员冲突、承担家庭invisible labor

```
                    家庭协同焦点
                        │
          ┌─────────────┼─────────────┐
          │  群体E:      │  群体A:      │
          │  家务委派     │  Mental Load │
          │  执行者       │  妈妈        │
          │             │             │
 被动式   │  群体D:      │  群体B:      │  主动式
 管理 ────┤  结构空缺     │  课外活动    ├── 规划
          │  老人         │  调度员      │
          │             │             │
          │  群体F:      │  群体C:      │
          │  随遇而安     │  时间优化    │
          │  独居者       │  效率者      │
          └─────────────┼─────────────┘
                        │
                    个人时间焦点
```

---

## 二、六大用户群详细画像

### 群体 A：Mental Load 妈妈（核心用户 · 首要人群）

**象限位置**：主动规划 × 家庭协同

**群体描述**：  
25-50岁北美家庭的主要日程管理者，通常为双职工妈妈或全职妈妈。她是家庭的"中央调度器"——所有人的日程、所有孩子的活动、所有需要准备的物品，都在她一个人的脑子里。她不是不主动，恰恰因为她**过度主动**地承担了一切，才导致 mental load 的崩塌。

**核心 Job（JTBD）**：  
> "When I am managing my family's schedules across multiple calendars and apps, I want to have one single view that shows me everything at a glance, so I can stop carrying everything in my head and feel like I have control."

**独特需求**：
- **一眼看全家**（J1强验证）：所有人的日程汇聚在一处、颜色区分、无需打开5个App
- **Prepare 清单自动生成**：明天field trip需要什么、下周比赛要带什么——她不想再"想"这些事
- **减轻 invisible labor**：不是帮她"做得更多"，而是帮她"不用再独自想那么多"
- **让家人可见**：当日程和任务被可视化、共享，其他家人才会分担

**独特痛点**：
- 多日历散落（Google + iCloud + 学校App + 运动队App），手动汇总耗时耗力
- 白板/便签纸/口头提醒三件套失效——写了没人看，说了没人记
- 独自承担所有"准备工作"——打印permission slip、洗球衣、买派对礼物——no one else remembers
- 被抱怨"你怎么又忘了"时的愧疚感

**Amazon评论典型原话**：
> *"It has been a game changer for our family. I'd been begging my husband for one of these for 2 years. No one else looked at the whiteboard..."*  
> *"We went from a dry erase calendar that could only go 1 month out to being able to see our schedule at a glance."*

---

### 群体 B：课外活动调度员

**象限位置**：主动规划 × 家庭协同（偏执行导向）

**群体描述**：  
有2个以上学龄儿童的家庭，孩子们参与多项课外活动（足球、钢琴、游泳、tutoring等）。核心任务是**多孩子多活动的时间协调与接送安排**。

**核心 Job（JTBD）**：  
> "When I am juggling multiple kids' extracurricular schedules that often conflict, I want a system that detects conflicts and suggests alternatives, so I can stop having meltdowns on Tuesday evenings."

**独特需求**：
- 冲突检测与替代方案：两个孩子同时有活动时的调度
- 装备准备追踪：足球赛带water bottle和shin guards
- 接送路线优化与家庭成员调度

**独特痛点**：
- 临时取消/改期导致整个下午安排推倒重来
- 孩子到了足球场发现球鞋忘在家
- 信息散落在TeamSnap/WhatsApp/学校Newsletter各处

---

### 群体 C：时间优化效率者

**象限位置**：主动规划 × 个人焦点

**群体描述**：  
25-45岁专业人士或创业者，高度关注个人生产力和时间块管理，核心是**个人效率**而非家庭协同。

**核心 Job（JTBD）**：  
> "When I am planning my week, I want a dedicated physical display that shows my time blocks, so I can maintain deep focus without constantly checking my phone."

**独特需求**：时间块可视化、习惯养成追踪、减少手机干扰、Morning Glance仪式  
**与product适配度**：中等——早期adopter和口碑传播者，但product可能"过于家庭化"。

---

### 群体 D：结构空缺老人

**象限位置**：被动管理 × 个人焦点

**群体描述**：  
65+退休人群，失去工作带来的时间结构，每天"都差不多"，与子女时间不同步，易被遗忘在family loop之外。

**核心 Job（JTBD）**：  
> "When every day feels the same after retirement, I want gentle rhythm anchors that give my day structure, so I can feel purposeful and connected to my family."

**独特需求**：节奏锚点（吃药/运动/社交提醒）、与家人保持连接、安全网/看护、极简操作  
**战略意义**：与SellerSprite市场分析一致——"老年友好 + 无订阅"是未被充分服务的利基。

---

### 群体 E：家务委派执行者

**象限位置**：被动管理 × 家庭协同

**群体描述**：  
家庭中的"非主管理者"（通常是父亲/配偶），不主动管理日程，但愿意被分配任务并执行。

**核心 Job（JTBD）**：  
> "When my partner is overwhelmed and I want to help but don't know where to start, I want clear assigned tasks I can just check off, so I can contribute without needing to ask 'what do you need me to do?'"

**独特需求**：明确任务推送（非pull式查看）、任务完成反馈、降低询问成本  
**产品启示**：push notification和"成员任务视图"对这群人特别关键。

---

### 群体 F：随遇而安独居者

**象限位置**：被动管理 × 个人焦点

**群体描述**：独居年轻人或空巢期成年人，日程简单、无复杂协同需求。  
**与product适配度**：低——核心价值过度匹配。非目标市场。

---

## 三、优先级排序

| 优先级 | 用户群 | 市场规模 | 支付意愿 | 核心价值匹配 | 建议 |
|---|---|---|---|---|---|
| ★★★ | A. Mental Load妈妈 | 大 | 高（$399-699） | 完美匹配 | 首要目标 |
| ★★☆ | B. 课外活动调度员 | 中大 | 高 | 高匹配 | A的子集/进阶 |
| ★★☆ | D. 结构空缺老人 | 中 | 中 | 高匹配 | 第二人群利基 |
| ★☆☆ | E. 家务委派执行者 | 大 | 低 | 中匹配 | 附带用户 |
| ★☆☆ | C. 时间优化效率者 | 中 | 中高 | 低匹配 | 早期种子/KOL |
| ☆☆☆ | F. 随遇而安独居者 | 大 | 低 | 低匹配 | 非目标 |

## 四、与已有JTBD验证的对照

| 已验证Job | 最匹配用户群 | 验证强度 |
|---|---|---|
| J1: 一眼看全家安排 | A + B + D | 强验证 |
| J2: 家庭任务/清单协同 | A + E | 强验证 |
| J3: 多日历同步 | A + B | 强验证+强反证 |
| J4: 替代白板/纸条 | A + B | 强验证 |

---

*基于 JTBD 框架 · 数据来源：1051条Amazon评论JTBD分析 + 会议纪要 + SellerSprite市场分析*
