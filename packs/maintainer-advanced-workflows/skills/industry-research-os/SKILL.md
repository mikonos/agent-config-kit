---
name: industry-research-os
description: AI辅助行业研究与行业情报系统搭建。适用于行业研究、陌生行业、市场研究、竞品拆解、行业数据库、行业地图、内容生态和机会地图任务。
metadata:
  routing:
    requirePromptTriggers: true
    requireFileTriggers: true
    requireDescriptionRouting: true
---

> **通用协议**：执行前读取目标项目当前生效的 Rule 和局部说明；不要假设存在
> 某个 Vault、固定目录或 Cursor 专属前置 Skill。

# Industry Research OS

## 核心定位

把“了解一个行业”从一次性搜索，变成可复用的行业操作系统：信源库、样本数据库、竞品结构、内容生态、机会地图、监控节奏。

本 skill 适合两种强度：

1. **60 分钟行业入门**：搭骨架、建小样本、列信源和下一步，不假装完成全量研究。
2. **持续行业研究**：在入门骨架上扩充样本、验证假设、形成周报和决策材料。

## 触发场景

- 用户说“研究/调研/了解某个行业、赛道、品类、市场”。
- 用户要“陌生行业快速入门”“行业地图”“竞品格局”“内容生态”“机会地图”。
- 用户想把一个行业整理成可长期跟踪的数据库或情报系统。
- 用户给出一篇行业文章、竞品网站、关键词清单，要求反推出行业框架。

## 必读资料

- 始终读取 `references/article-framework.md`：文章提炼出的核心框架和字段。
- 要产出正式报告或落盘文件时，读取 `references/output-templates.md`。
- 行业重要、陌生、高风险，或用户要求“最强大脑”时，读取 `references/expert-routing.md`。

## 专家座席

每次开题先选两类专家，并在输出中声明：

1. **行业结构专家**：默认 Michael Porter，用五力、价值链、进入壁垒、利润池拆行业。
2. **工作流专家**：默认 Andrej Karpathy，用 agentic workflow 把研究拆成可验证的小循环。
3. **领域最强大脑**：按行业替换或叠加，例如 AI 用 Karpathy，B2B 定位用 April Dunford，JTBD/需求用 Clayton Christensen + Bob Moesta，产品机会用 Teresa Torres。

执行规则：

- 已有对应 `*-perspective` skill 时，先读取该 skill。
- 没有现成 skill、且任务复杂或高风险时，启用 subagent 扮演该领域最强大脑做独立审查。
- 轻量任务可由主 agent 直接模拟专家方法，但必须显式使用其框架，而不是只挂名。

## 工作流

### Phase 0: 研究边界

若用户没有说明，默认采用“小样本行业 OS”模式；只在缺少关键边界会造成明显误判时追问。

最小边界：

- 行业/品类：
- 地区/语言：
- 研究目的：入门、创业机会、投资判断、竞品、内容选题、采购、产品定义？
- 时间箱：60 分钟入门、半天、一周、持续监控？
- 输出形态：对话结论、Markdown 报告、数据库表、周报模板？

### Phase 1: 行业骨架

按文章框架先建空表，不急着写结论：

- Brands
- Products
- Keywords
- Communities
- Influencers
- Competitors
- Business Models
- Supply Chain
- Regulations
- Trends
- Opportunities

### Phase 2: 小样本填充

只采一组可核验样本，标明样本边界。60 分钟模式下不要承诺 Top100、全量市场规模或投资级结论。

最少填充：

- 10-20 个信源或入口
- 5-10 个品牌/玩家
- 5-10 个产品/服务形态
- 10-30 个关键词
- 5-10 条用户痛点或评论证据

### Phase 3: 竞品与赚钱结构

拆竞品网站和商业结构：

- 导航、品类、Collection、Product Tags、Footer、Blog、SEO、Landing Page
- 定价、包装、分销渠道、利润池、复购机制、采购路径
- 直接竞品、间接替代、“不消费”替代

需要深度战卡时，调用 `competitive-profile-builder`。

### Phase 4: 需求与内容生态

建立关键词和内容生态：

- 关键词按平台分层：Google、Amazon、Reddit、YouTube、TikTok、垂直社区。
- 搜索意图分层：Commercial、Informational、Comparison、Review、Buying Intent。
- 内容账号按作用归类：Exposure、Growth、Save、Conversion、Personal Brand。
- 尽量抓近 90 天高互动样本，避免旧内容误导当前判断。

需要用户原声/JTBD 时，调用 `jtbd-desk-research`。

### Phase 5: 行业地图与机会地图

形成两张图：

- **行业地图**：玩家、价值链、用户、渠道、监管、供应链、内容入口。
- **机会地图**：未满足需求、强痛点、低服务区域、可切入人群、内容空白、分销空白。

每个机会必须写：

- 证据：
- 为什么现在：
- 目标人群：
- 已有替代：
- 最大反证：
- 下一步验证：

### Phase 6: 监控回路

把研究变成持续更新系统：

- Sources/RSS
- 竞品变动
- 新内容/新关键词
- 评论与用户痛点
- 监管与供应链变化
- 每周行业情报报告

### Phase 7: 落盘与入网

如需落盘，先让用户选择目标项目内的目录；用户没有指定时，提出一个项目相对
路径并预览，不自行写入个人知识库或全局目录。

建议文件包：

- `YYYYMMDD_行业研究_[行业名]_brief.md`
- `YYYYMMDD_行业研究_[行业名]_sources.md`
- `YYYYMMDD_行业研究_[行业名]_databases.md`
- `YYYYMMDD_行业研究_[行业名]_opportunity-map.md`
- `YYYYMMDD_行业研究_[行业名]_weekly-intel-template.md`

落盘后遵循目标项目已有的 YAML、链接和索引约定。只有相关 Skill 已安装且项目
确实使用知识网络时，才可选调用 `link-proposer` 或 `index-note`。

### Phase 8: 质量审查

完成前必须检查：

- 是否写明信息截止日期？
- 每个关键判断是否有来源或明确标注为假设？
- 是否区分“样本信号”和“全量结论”？
- 是否覆盖反证、替代方案和不确定性？
- 高时效/高风险信息是否联网核验？
- 是否形成下一轮可执行研究任务，而不是停在漂亮总结？

## 红线

- 不把搜索摘要当作已读原文。
- 不编造市场规模、融资、流量、排名、Top100 清单。
- 不把旧数据说成“当前”。
- 不用单一平台样本代表整个行业。
- 不在 60 分钟模式下输出投资级或创业终局判断。

## 协作 skill

- `deep-research`：联网取证和多源验证。
- `competitive-profile-builder`：深度竞品画像和战卡。
- `jtbd-desk-research`：用户原声、痛点、雇用/解雇时刻。
- `strategic-advisor`：机会优先级和决策建议。
- `link-proposer` / `index-note`：落盘后的知识网络入网。
- `structure-note`：把研究结果改写成可发布文章。
