---
date: <YYYY-MM-DD>
type: research / tool-output
tool: tool04-target-users
product: <产品代号或名称>
language: zh-CN
status: draft
inputs:
  - <产品定义来源>
---

# Tool 4 — 目标用户识别 Finding Job Performers
> Product: <产品代号或名称>
> Stage: Stage 1 用户识别（先于 Tool 6 / Tool 7 的目标用户填空）
> Prompt source: `references/original_prompt_blocks.md#tool-4`
> Methodology anchor: `references/methodology_foundations.md` § Jobs to be Done — Job Performer 分群

## 上下文输入（执行前必填）

- **产品定义**：<...>
- **核心差异化**：<...>
- **语言要求**：zh-CN

## 输出主体

### 一、X / Y 轴属性定义（MECE）

- **X 轴**：<属性名> — 左端 `<极端 A>` ↔ 右端 `<极端 B>`（必须是同一属性的两端）
- **Y 轴**：<属性名> — 下端 `<极端 C>` ↔ 上端 `<极端 D>`（必须是同一属性的两端）

### 二、4 象限分群图（按需 6-8 象限亦可，前提是仍 MECE）

```
                  Y↑ <D>
                    │
     [群 Q2]        │        [群 Q1]
                    │
    ────────────────┼────────────────  X
     <A>            │            <B>
                    │
     [群 Q3]        │        [群 Q4]
                    │
                  Y↓ <C>
```

### 三、每群用户分群卡

#### 群 Q1：<名字>
- **位置**：X=<...> / Y=<...>
- **独特需求（needs）**：<...>
- **独特痛点（pain points）**：<...>
- **为什么 hire 本产品**：<一句 JTBD 解释>
- **与其他群的边界**：<这群与 Q2/Q3/Q4 互斥的判据>

#### 群 Q2：<名字>
- **位置**：X=<...> / Y=<...>
- **独特需求**：<...>
- **独特痛点**：<...>
- **为什么 hire 本产品**：<...>
- **与其他群的边界**：<...>

#### 群 Q3：<名字>
- **位置**：X=<...> / Y=<...>
- **独特需求**：<...>
- **独特痛点**：<...>
- **为什么 hire 本产品**：<...>
- **与其他群的边界**：<...>

#### 群 Q4：<名字>
- **位置**：X=<...> / Y=<...>
- **独特需求**：<...>
- **独特痛点**：<...>
- **为什么 hire 本产品**：<...>
- **与其他群的边界**：<...>

### 四、MECE 自检表

| 检查项 | 是否满足 | 证据 |
|---|---|---|
| 4 群互斥（需求/痛点不重叠）| ✅ / ⚠️ | <...> |
| 4 群穷尽（覆盖产品可能的 Job Performer）| ✅ / ⚠️ | <...> |
| X/Y 轴是同一属性的两端 | ✅ / ⚠️ | <...> |
| 分群不基于人口 / 地理 / 职业 | ✅ / ⚠️ | <...> |

---

## 自检（agent 必填，每条带证据）

- [ ] **命名归位**：文件名 `tool04_target_users_<product>.md` —— 证据：本文件名为 `___`
- [ ] **YAML 完整**：date / type / tool / product / language 五字段齐全 —— 证据：第 1-N 行
- [ ] **跨工具引用锁版本**：本工具无上游 / 下游 Tool 6 / Tool 7 引用本工具产出时锁版本 —— 证据：第 X 行 / 本工具无上游
- [ ] **格式硬约定**：MECE 原则；X/Y 轴为对立属性极端；分群**基于 needs / pain points 而非人口/地理/职业**（原文：focus on user needs or pain points rather than demographic, geographic, or occupational dimensions）—— 证据：抽样 2 群的"独特需求/痛点"对应轴位
- [ ] **语言符合约定**：默认 zh-CN —— 证据：整篇语言判定
- [ ] **不越边界**：本产出按 needs/pain points 分群，**没有用人口 / 地理 / 职业切分**；不是 persona 画像，不是市场份额报告 —— 证据：一句话申明 + MECE 自检表第 4 行
- [ ] **v1 扩展声明**：未用 v1 深化 / 用了 v1 深化（如 Bull's Eye 渗透路径、8 群体细化）—— 证据：产出顶部声明位置
