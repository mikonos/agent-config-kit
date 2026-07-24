---
name: competitive-profile-builder
description: Build structured competitor profiles for PM and sales using DHM (Delight, Hard-to-copy, Margin), SWOT, head-to-head tables, win/loss scenarios, and battlecard-ready messaging. Use for competitive deep-dives, battlecards, "how we beat X", and sales enablement intel with sourced, dated claims.
---

# Competitive Profile Builder

## 何时启用

用户要：**竞品画像 / 深度竞品分析 / battlecard（战卡）/ 赢单·输单复盘 / head-to-head / 销售话术对抗**；或显式提到 `competitive-profile-builder`、`/competitive-profile-builder`。

## 执行前

1. 先读取目标项目当前生效的 Rule 和局部说明；不要假设存在某个 Vault 或
   Cursor 专属前置 Skill。
2. 若需联网取证，配合 `deep-research` 或 WebSearch/WebFetch；**每条重要结论尽量带来源与抓取日期**。

## 工作流

### 1. 澄清（缺一则问）

- 我方产品 / 品类 / 目标市场
- 竞品清单（直接 / 间接 / 「不做」的替代）
- 读者：销售、PM、高管、对外材料？
- 交付：对话片段 vs 用户指定的项目路径（若落盘，遵循目标项目现有命名约定）

### 2. 证据规则

- 优先官网、文档、定价页、发布说明、监管披露、可信媒体；避免匿名论坛当唯一依据。
- 对**推测**单独标注 `epistemic_status: speculative` 或文中写「待验证」。
- 在输出顶部或附录写 **信息截止日期**（例如 `As of YYYY-MM-DD`）。

### 3. 交付结构（可按需删减，顺序可读）

| 区块 | 内容 |
|------|------|
| 一页纸 | 竞品定位、ICP、包装/定价信号、近期公开动作 |
| DHM | Gibson Biddle 三角：**Delight / Hard-to-copy / Margin** — 各写「对方怎么做」与「我方可叙事」 |
| SWOT | 以竞品为主角；每点尽量有来源 |
| Head-to-head 表 | 自选维度（功能、价格、集成、安全、支持、生态、采购路径…） |
| Win / Loss | 3–5 个具体场景（预算、迁移、合规、采购周期…）+ 推荐话术与需避开的坑 |
| Battle card | 电梯陈述、常见异议、可问对手的「地雷」问题、需客户侧验证的证明点 |

### 4. 与库内其它 skill 的分工

- `competitor-alternatives`：偏 **SEO/落地页** 的竞品与替代方案页。
- `marketing-strategy-pmm`：偏 **定位、GTM、April Dunford 式叙事**。
- `deep-research`：本 skill 的 **联网取证** 子流程。

## 红线

- 不编造内幕、不实财务数据或无法公开的「客户原话」。
- 不做诽谤性表述；措辞保持可对外转述的专业度。

## 来源说明

能力结构对齐 [mySecond · Competitive Profile Builder](https://www.mysecond.ai/skills/competitive-profile-builder) 的公开描述（DHM、SWOT、战卡等）。**本文件为仓库内自撰 SKILL，不是 mySecond 付费包中的原始分发文件**；若需要其官方打包素材，请在 mySecond 页面下载。
