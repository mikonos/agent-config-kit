# Reddit Geo Research: Article Framework Extraction

本文件只抽取本地文章《如何用 Codex 在 1 小时内快速了解陌生行业》和本仓 `industry-research-os` 的可迁移框架，供后续蒸馏 `reddit-geo` skill 使用；不定义最终 `SKILL.md`。

## 1. 文章核心框架

### 一句话

陌生领域研究不要先追求一篇完整报告，而要先建立一个可持续增长的研究 OS：信源库、样本库、关键词库、竞品/替代库、内容生态、机会地图和监控回路。

迁移到 Reddit Geo 时，核心不是“搜几条 Reddit 帖子”，而是把 Reddit 变成一个可复用的需求、内容、竞品和可见性信号数据库。

### 文章的工作流

| 阶段 | 原文框架 | Reddit Geo 可迁移含义 |
|---|---|---|
| 1. 建数据库骨架 | Brands、Products、Keywords、Communities、Influencers、Competitors、Business Models、Supply Chain、Regulations、Trends、Opportunities | 先建 Reddit Geo 研究目录：subreddits、threads、comments、queries、pain points、brand mentions、competitor mentions、content patterns、AI/GEO visibility signals、opportunities、monitoring |
| 2. 小样本填充 | 先填品牌、产品、痛点，不追求全量 | 先抓一组可核验 subreddit、帖子、评论原话和查询词；标明样本边界 |
| 3. 关键词库 | Google、Amazon、Reddit、YouTube、TikTok 等平台关键词 | 为 Reddit Geo 建 `query -> subreddit/thread/comment -> user intent` 映射；区分信息型、比较型、评测型、购买意图和问题排查型 |
| 4. 竞品拆解 | 导航、Collection、Tag、Blog、SEO、Landing Page | 改成拆 Reddit 上的竞品出现路径：被谁提到、在哪些问题下被推荐、反对理由、替代方案、常见比较对象 |
| 5. 内容生态 | 账号、爆款、评论、互动、转化意图 | 改成帖子/评论生态：高互动主题、反复出现的问题、可被引用的经验帖、争议帖、购买前后复盘帖 |
| 6. 行业地图和机会地图 | 玩家、需求、渠道、空白位 | Reddit Geo 机会地图要写清：用户问题、当前替代、证据原话、竞品弱点、内容空白、下一步验证 |
| 7. 监控回路 | Sources、RSS、竞品监控、内容监控、周报 | 建 subreddit/关键词/竞品 mention/高互动 thread 的持续监控节奏，输出周报或更新日志 |

### 60 分钟边界

60 分钟适合产出：

- Reddit Geo 研究骨架。
- 5-20 个 subreddit / thread / query 的小样本。
- 10-50 条用户原话或信号摘录。
- 初步痛点、关键词、竞品 mention 和机会假设。
- 下一轮验证计划。

60 分钟不能宣称：

- 全量 Reddit 市场共识。
- 准确代表整个平台或整个行业。
- 已证明某个 GEO 策略一定有效。
- 已覆盖所有 subreddit、历史帖子或实时 AI 搜索结果。
- 投资级、医疗级、法律级或监管级结论。

## 2. 可迁移到 Reddit Geo 的字段表

### sources

| field | meaning | Reddit Geo 用法 |
|---|---|---|
| name | 信源名称 | subreddit、Reddit search、Google SERP、行业论坛、品牌官网、AI answer surface |
| type | 信源类型 | subreddit / thread index / official site / search result / AI answer / report |
| url | 来源链接 | 原始 subreddit、帖子、评论、搜索页或官方页面 |
| authority | 可信度 | 官方、一手用户原话、高互动社区、低质量转载等 |
| cadence | 更新频率 | 高频活跃、低频长尾、事件驱动 |
| why_it_matters | 跟踪理由 | 是否能暴露用户痛点、竞品比较、购买阻碍、GEO 可见性机会 |

### communities

| field | meaning | Reddit Geo 用法 |
|---|---|---|
| subreddit | 社区名 | 例如 `r/...`，作为最小社区单元 |
| topic_scope | 主题边界 | 社区讨论什么、不讨论什么 |
| audience | 主要人群 | 买家、使用者、从业者、爱好者、反对者 |
| rules_or_mod_signal | 规则/管理信号 | 是否允许品牌、自荐、链接、购买建议 |
| activity_signal | 活跃度信号 | 帖子频率、评论密度、近期高互动帖 |
| relevance_reason | 纳入理由 | 它回答 Reddit Geo 研究中的哪个问题 |

### threads

| field | meaning | Reddit Geo 用法 |
|---|---|---|
| thread_title | 帖子标题 | 用户问题、评测、吐槽、推荐、比较的入口 |
| thread_url | 帖子链接 | 原始证据 |
| subreddit | 所属社区 | 连接社区地图 |
| thread_type | 帖子类型 | question / review / comparison / complaint / guide / success story / warning |
| created_or_observed_at | 创建或观察时间 | 避免旧帖被误判为当前趋势 |
| engagement_signal | 互动信号 | upvotes、comments、保存价值、争议度；不要单独当作质量 |
| why_it_matters | 研究价值 | 痛点、关键词、竞品、内容模式或 GEO 可引用性 |

### comments

| field | meaning | Reddit Geo 用法 |
|---|---|---|
| quote | 用户原话 | 尽量保留短原话，作为痛点和 JTBD 证据 |
| comment_url | 评论链接 | 可追溯证据 |
| speaker_type | 发言者类型 | 新手、重度用户、购买者、反对者、专业人士、品牌方 |
| sentiment | 情绪方向 | positive / negative / mixed / neutral |
| pain_or_job | 痛点或待完成任务 | 用户想取得的进展 |
| current_alternative | 当前替代方案 | 竞品、DIY、放弃、不消费、线下方案 |
| caveat | 注意事项 | 样本偏差、玩笑、讽刺、低可信、过时 |

### keywords_and_queries

| field | meaning | Reddit Geo 用法 |
|---|---|---|
| query | 查询词 | Reddit 内搜索、Google `site:reddit.com`、AI 答案触发问题 |
| platform | 平台 | Reddit / Google / Perplexity / ChatGPT / YouTube / TikTok / 其他 |
| intent | 意图 | Informational / Comparison / Review / Buying Intent / Troubleshooting / Alternatives |
| user_question | 用户真正想问什么 | 把关键词翻译成需求问题 |
| matched_threads | 命中的帖子 | 连接 thread 证据 |
| evidence | 证据 | 链接、截图说明、原话或样本编号 |

### brand_and_competitor_mentions

| field | meaning | Reddit Geo 用法 |
|---|---|---|
| name | 品牌/竞品/替代方案 | 被讨论或推荐的对象 |
| mention_context | 出现场景 | 推荐、反对、比较、踩坑、价格、售后、效果 |
| compared_with | 比较对象 | 用户把它和谁放在一起比较 |
| positive_signal | 正向信号 | 被推荐的理由、被信任的理由 |
| weakness_signal | 负向信号 | 抱怨、风险、失败原因、反对理由 |
| money_or_conversion_signal | 赚钱/转化信号 | 购买触发、价格接受度、渠道、复购、替代成本 |

### content_patterns

| field | meaning | Reddit Geo 用法 |
|---|---|---|
| pattern | 内容模式 | AMA、长评测、对比帖、踩坑帖、清单帖、教程帖、警告帖 |
| role | 内容作用 | Exposure / Growth / Save / Conversion / Trust / Objection Handling |
| repeated_topic | 反复出现的话题 | 多个 thread 中重复的问题或标题结构 |
| quote_or_example | 样本 | 代表性帖子或评论 |
| geo_relevance | GEO 相关性 | 是否容易被 AI answer 引用、总结、推荐或作为用户原声 |
| next_action | 下一步 | 继续采样、建内容资产、验证搜索触发、监控变化 |

### opportunities

| field | meaning | Reddit Geo 用法 |
|---|---|---|
| opportunity | 机会假设 | 可做内容、产品、定位、竞品反击或 GEO 可见性优化的机会 |
| evidence | 支撑证据 | 帖子、评论、查询、竞品 mention |
| target_user | 目标用户 | 谁有这个问题 |
| current_alternative | 当前替代 | 用户现在怎么解决 |
| why_now | 为什么现在可能成立 | 新趋势、新平台、新痛点、新竞品变化 |
| counter_evidence | 最大反证 | Reddit 偏样本、需求弱、监管风险、强竞品已覆盖 |
| next_test | 下一步验证 | 更大样本、访谈、搜索核验、内容测试、监控一周 |

### monitoring

| field | meaning | Reddit Geo 用法 |
|---|---|---|
| watch_item | 监控对象 | subreddit、query、brand mention、competitor、high-signal thread |
| cadence | 节奏 | daily / weekly / monthly / event-driven |
| trigger | 触发条件 | 新高互动帖、负面激增、竞品被频繁推荐、AI 答案引用 Reddit |
| output | 输出物 | weekly intel、机会更新、风险提示、内容选题 |
| owner_or_agent | 执行者 | 人工、Codex、脚本、后续 skill |

## 3. 专家路由建议

Reddit Geo 后续 skill 可继承 `industry-research-os` 的专家路由，但要按 Reddit 的社区、内容和 GEO 可见性问题做加权。

| 场景 | 建议专家 | 使用方式 |
|---|---|---|
| 研究一个品类/市场在 Reddit 上的结构 | Michael Porter | 用五力、替代品、进入壁垒、利润池判断 Reddit 信号属于行业哪一层 |
| 把 Reddit 研究做成可执行流程 | Andrej Karpathy | 把任务拆成可验证循环：query -> sample -> evidence ledger -> cluster -> hypothesis -> next test |
| 从 Reddit 评论抽痛点和需求 | Clayton Christensen + Bob Moesta | 用 JTBD 识别“雇用/解雇时刻”和当前替代方案 |
| 从 Reddit 信号生成机会地图 | Teresa Torres | 用机会树把 pain、audience、solution idea、experiment 分开 |
| 判断品牌/竞品在 Reddit 的定位 | April Dunford | 看用户把品牌归入哪个比较集合、为什么选择/拒绝它 |
| 判断内容能否传播和转化 | David Ogilvy + Seth Godin | 区分广告诉求、信任建立、社群传播和转化证据 |
| Reddit/AI answer 作为分发平台时 | Ben Thompson + Michael Porter | 看聚合、供需两侧、分发控制点和平台依赖风险 |
| 医疗、金融、法律、教育、政策等高风险品类 | 领域监管专家 + 官方来源 | Reddit 只能做用户原声，不可替代当前法规和专业建议 |

后续 skill 的最小专家声明可采用：

```markdown
## Expert Lens

- 本轮采用：[主领域专家] + [Reddit/JTBD/工作流专家]
- 为什么是他们：
- 使用的框架：
- 他们会反对的直觉结论：
- 对研究计划的改动：
```

## 4. 哪些地方不能照搬

1. **不能照搬 Top100 叙事。** 原文里的 Top100 品牌/账号适合表达方向，但 Reddit Geo 在 60 分钟内只能做小样本，必须写清样本边界。
2. **不能把 Reddit 样本当总体统计。** Reddit 用户自选择偏差强，帖子和评论只能作为用户原声和问题线索，不能直接代表市场规模或真实占比。
3. **不能把电商网站结构字段原样套用。** Shopify 的导航、Collection、Product Tag 要转译为 subreddit、thread type、flair、query、mention context、comparison set。
4. **不能把互动量等同于价值。** upvotes/comments 受时间、社区规模、争议、梗文化和版规影响；需要结合原话质量、重复出现频率和决策相关性。
5. **不能把一次搜索当持续情报系统。** Reddit Geo 的价值在监控回路：新帖、新评论、新竞品 mention、新 AI answer 引用、新反证。
6. **不能忽略版规和伦理边界。** 某些社区禁止自荐、营销、链接或品牌参与；后续 skill 应提醒只做公开内容研究，并尊重平台规则。
7. **不能把 GEO 结论写成已验证。** 如果没有实时搜索/AI answer surface 证据，只能写“可见性假设”或“待验证触发词”。
8. **不能只输出漂亮总结。** 每个机会都要回到 evidence、target user、current alternative、counter evidence、next test。

## 5. 来源路径

- 原文 URL：`https://mp.weixin.qq.com/s/UzikNhV0jbZDiMwnF-EIdg?scene=1`
- 配套 Skill：已安装 `industry-research-os/SKILL.md`
- 框架引用：已安装 `industry-research-os/references/article-framework.md`
- 专家路由：已安装 `industry-research-os/references/expert-routing.md`
