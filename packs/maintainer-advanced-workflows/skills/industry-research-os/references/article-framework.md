# Article Framework Reference

来源：

- 原文：`https://mp.weixin.qq.com/s/UzikNhV0jbZDiMwnF-EIdg?scene=1`
- 方法来源：维护者对“陌生行业一小时研究”工作流的本地实践总结；公开版仅保留
  本 Skill 可独立执行的框架，不依赖维护者的私有笔记路径。

## 一句话框架

陌生行业研究不是先写报告，而是先搭一个行业数据库骨架，再用小样本填充、验证、监控，让后续每次研究都能接着长。

## 60 分钟边界

60 分钟只能完成：

- 行业骨架
- 小样本数据库
- 主要信源
- 初步机会假设
- 监控与下一步研究计划

60 分钟不能宣称：

- 全量 Top100 玩家
- 准确市场规模
- 投资级判断
- 可直接创业的最终结论

## 文章框架的 7 步

1. 建行业数据库目录：品牌、产品、关键词、社区、KOL、竞品、商业模式、供应链、法规、趋势、机会。
2. 填样本库：先抓品牌、产品、痛点，不追求全量。
3. 建关键词库：跨 Google、Amazon、Reddit、YouTube、TikTok、垂直社区。
4. 拆竞品结构：导航、品类、Collection、Product Tags、Footer、Blog、SEO、Landing Page。
5. 扫内容生态：账号、爆款、评论、互动、转化意图。
6. 做行业地图和机会地图：把玩家、需求、渠道、空白位放到一张图上。
7. 建更新回路：Sources、RSS、竞品监控、内容监控、周报。

## 最小数据表

### sources

| field | meaning |
|---|---|
| name | 信源名称 |
| type | 官网、社区、报告、媒体、数据库、KOL、监管 |
| url | 来源链接 |
| authority | 高/中/低 |
| cadence | 更新频率 |
| why_it_matters | 为什么值得跟踪 |

### brands

| field | meaning |
|---|---|
| name | 品牌/玩家 |
| category | 细分位置 |
| country_or_region | 地区 |
| positioning | 对外定位 |
| channel | 主要渠道 |
| evidence_url | 证据 |

### products

| field | meaning |
|---|---|
| name | 产品/服务 |
| brand | 所属玩家 |
| job_to_be_done | 用户雇用它完成什么进展 |
| price_signal | 价格或定价信号 |
| distribution | 分销路径 |
| review_signal | 评论/痛点信号 |

### pain_points

| field | meaning |
|---|---|
| quote_or_signal | 原话或证据信号 |
| source | 来源 |
| user_type | 用户类型 |
| current_alternative | 当前替代方案 |
| severity | 高/中/低 |
| note | 解释 |

### keywords

| field | meaning |
|---|---|
| keyword | 关键词 |
| platform | Google/Amazon/Reddit/YouTube/TikTok/其他 |
| intent | Commercial/Informational/Comparison/Review/Buying Intent |
| user_question | 用户真正想问什么 |
| evidence | 来源或样本 |

### competitors

| field | meaning |
|---|---|
| name | 竞品 |
| type | 直接/间接/替代/不消费 |
| website | 网站 |
| money_path | 怎么赚钱 |
| acquisition_path | 怎么获客 |
| moat_signal | 护城河信号 |
| weakness_signal | 弱点信号 |

### content_accounts

| field | meaning |
|---|---|
| account | 账号 |
| platform | 平台 |
| audience | 受众 |
| content_role | Exposure/Growth/Save/Conversion/Personal Brand |
| top_post_signal | 近 90 天高互动内容 |
| comment_signal | 评论里的需求信号 |

### opportunities

| field | meaning |
|---|---|
| opportunity | 机会假设 |
| evidence | 支撑证据 |
| target_user | 目标用户 |
| current_alternative | 当前替代 |
| why_now | 为什么现在可能成立 |
| counter_evidence | 最大反证 |
| next_test | 下一步验证 |

## 可复用提示词骨架

用于开题：

```text
我想研究 [行业/品类] 在 [地区/语言] 的机会。请先不要写完整报告，先建立行业研究 OS：信源库、品牌/产品样本、关键词、竞品结构、内容生态、机会地图和监控计划。标明哪些是证据、哪些是假设、哪些需要继续验证。
```

用于竞品拆解：

```text
请按导航、品类、Collection、Product Tags、Footer、Blog、SEO、Landing Page、定价、渠道、复购机制拆解这些竞品，并输出它们的赚钱路径和获客路径。
```

用于机会地图：

```text
基于已有样本，输出机会地图。每个机会必须包含证据、目标人群、当前替代、为什么现在、最大反证、下一步验证。
```

用于周报：

```text
请把本周新增信源、竞品动作、内容爆点、关键词变化、用户痛点和机会变化整理成行业情报周报，并标注哪些需要下周继续追踪。
```
