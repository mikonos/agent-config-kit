# Research Agent 3: Reddit in GEO / AEO / AI Search

日期：2026-06-27

范围：只核验 Reddit 在 Google AI Overviews / AI Mode、ChatGPT、Perplexity 等 AI 搜索/答案引擎中的可见性证据；不写最终 `SKILL.md`。

方法：优先使用 Google、Reddit、OpenAI、Reddit Investor Relations 等一手来源；行业样本只作为观测证据，不当作因果证明。未使用知乎、微信公众号、百度百科。

## 结论速览

Reddit 对 GEO/AEO 的影响是“有证据的强信号”，但不是“发帖即可被 AI 引用”的确定公式。最硬的事实是：Google 和 OpenAI 都在 2024 年宣布通过 Reddit Data API 获得 Reddit 内容；Google 的 AI 搜索功能会用 query fan-out 找支持链接；多家行业数据集显示 Reddit 在 AI answers / AI Overviews / Perplexity 中经常进入高频引用域名。但反证也同样明确：不同平台、同一平台的不同 AI 表面、不同品类和意图之间，Reddit 引用占比差异很大；品牌自有站、商家列表、评测站、YouTube、Wikipedia、LinkedIn 等仍会在大量场景中超过 Reddit。

## 证据账本：关键判断

### 1. Google 与 Reddit 存在官方数据/API 合作

- 判断：Google 已获得 Reddit Data API 访问，用于更结构化、更高效地访问 Reddit 的实时、独特、动态内容；官方文本同时提到展示、训练和改善产品服务。
- URL：
  - https://redditinc.com/news/reddit-and-google-expand-partnership
  - https://blog.google/company-news/inside-google/company-announcements/expanded-reddit-partnership/
- 发布日期：2024-02-22。
- 来源类型：Reddit 官方公告 + Google 官方博客。
- 一手/二手：一手。
- 可信度：高。双方官方同时公告，且核心事实一致。
- 关键边界：Google 官方明确说该合作不改变 Google 对公开可抓取内容在索引、训练、展示中的使用方式。不能把所有 Reddit 出现在 Google AI 搜索里的现象都归因于 Data API 合作。

### 2. OpenAI 与 Reddit 存在官方数据/API 合作

- 判断：OpenAI 宣布会把 Reddit 内容带入 ChatGPT 和新产品，并通过 Reddit Data API 获取实时、结构化、独特内容，尤其用于更好理解和展示近期话题；OpenAI 也成为 Reddit 广告合作伙伴。
- URL：https://openai.com/index/openai-and-reddit-partnership/
- 发布日期：2024-05-16。
- 来源类型：OpenAI 官方公告，原文标注由 Reddit 发布。
- 一手/二手：一手。
- 可信度：高。
- 关键边界：公告没有披露 ChatGPT 何时、以何种权重、在哪些答案场景引用 Reddit；不能直接推出“Reddit 讨论会稳定进入 ChatGPT 答案”。

### 3. Google AI Overviews / AI Mode 的检索机制让第三方 UGC 有机会进入答案

- 判断：Google Search Central 说明 AI Overviews 与 AI Mode 可能使用 query fan-out，即围绕用户问题发起多个相关搜索，从更多子主题和数据源找支持页面；AI Mode 和 AI Overviews 可能使用不同模型和技术，因此链接集合会不同。
- URL：https://developers.google.com/search/docs/appearance/ai-features
- 发布/更新日期：页面未在抓取文本中显示具体发布日期；当前核验日期 2026-06-27。
- 来源类型：Google Search Central 官方文档。
- 一手/二手：一手。
- 可信度：高。
- 操作含义：Reddit GEO 不应只围绕一个关键词，而要覆盖用户问题的子问题、比较维度、真实使用场景、反例和替代方案。

### 4. Google 官方不承认 GEO/AEO 是脱离 SEO 的新规则

- 判断：Google 的 AI optimization guide 说，从 Google Search 角度看，面向 generative AI search 的优化仍是优化 search experience，本质仍是 SEO；AEO/GEO 是第三方常用术语。
- URL：https://developers.google.com/search/docs/fundamentals/ai-optimization-guide
- 发布/更新日期：页面未在抓取文本中显示具体发布日期；当前核验日期 2026-06-27。
- 来源类型：Google Search Central 官方文档。
- 一手/二手：一手。
- 可信度：高。
- 操作含义：skill 不能承诺“绕过 SEO 直接操控 AI 答案”。更稳妥的说法是：用 Reddit UGC 补足 AI 搜索在“真实经验、比较、推荐、反对意见”上的证据层。

### 5. AI Overviews 是带链接的搜索体验，不是普通 chatbot

- 判断：Google 2024 年发布 AI Overviews 时强调，其使用定制 Gemini 模型结合 Search 系统，给出概览和链接；Google 的 PDF 说明 AI Overviews 会用核心排名系统、Knowledge Graph，并以顶部 web results 支持答案。
- URL：
  - https://blog.google/products-and-platforms/products/search/generative-ai-google-search-may-2024/
  - https://www.google.com/search/howsearchworks/google-about-AI-overviews.pdf
- 发布日期：2024-05-14；PDF 为 2024-07。
- 来源类型：Google 官方博客 + Google 官方 PDF。
- 一手/二手：一手。
- 可信度：高。
- 操作含义：测量 Reddit GEO 时要同时记录“答案是否提到品牌”和“支持链接是否引用 Reddit URL”，二者不是一回事。

### 6. Reddit 自己也在把站内搜索改造成 AI answer surface

- 判断：Reddit 2024 年推出 Reddit Answers，用 AI conversational interface 汇总 Reddit 对话并链接相关社区和帖子；2026 年帮助文档显示 Reddit AI search 可从真实帖子和评论生成答案，并带 inline citations。
- URL：
  - https://redditinc.com/news/introducing-reddit-answers
  - https://support.reddithelp.com/hc/en-us/articles/32026729424916-Reddit-s-AI-search
- 发布/更新日期：2024-12-09；帮助文档更新于 2026-05-26。
- 来源类型：Reddit 官方博客 + Reddit Help 官方文档。
- 一手/二手：一手。
- 可信度：高。
- 操作含义：Reddit 不只是外部 LLM 的数据源，也在变成站内 AI 搜索入口。skill 可把“站内 Reddit AI search 能否引用目标讨论”作为辅助验证面。

### 7. Reddit 投资者材料把“搜索目的地”列为战略方向

- 判断：Reddit Q2 2025 shareholder letter 称核心搜索产品有 7000 万 weekly users，Reddit Answers 达到 600 万 weekly users，并计划全球扩展、深度整合到核心搜索。
- URL：https://s203.q4cdn.com/380862485/files/doc_financials/2025/q2/Q2-25-Shareholder-Letter.pdf
- 发布日期：2025-07-31。
- 来源类型：Reddit Investor Relations 股东信。
- 一手/二手：一手。
- 可信度：高，但属于公司叙事和经营指标，需警惕营销口径。

### 8. 行业样本显示 Reddit 是 AI answers 的高频引用域名，但数值依平台和口径变化

- 判断：Profound 对 2024-08 至 2025-06 的 6.8 亿 citations 分析中，Reddit 是 Google AI Overviews 总引用占比第一（2.2%）和 Perplexity 总引用占比第一（6.6%）；在各平台 top 10 source share 中，Google AI Overviews 的 Reddit share 为 21.0%，Perplexity 为 46.7%。
- URL：https://www.tryprofound.com/blog/ai-platform-citation-patterns
- 发布/更新日期：2025-06-05，页面标注 updated August 2025。
- 来源类型：Profound 行业研究。
- 一手/二手：行业自有数据，一手采集；对平台机制的解释属于二手推断。
- 可信度：中高。样本量大，但供应商有 AI visibility 产品利益相关，且口径包括“overall citation volume”和“top source share”两套不同指标。

### 9. Ahrefs 样本显示 Reddit 在 2025 年春季 AI Overviews 中显著上升

- 判断：Ahrefs 分析 2500 万个 US AI Overview keywords 后称，Reddit.com 出现在 5.5% 的 AI Overviews citation market share 中，且从 2025-03-12 的 1.3% 上升到 2025-05-06 的 5.5%。
- URL：https://ahrefs.com/blog/ai-overview-growth/
- 发布日期：2025-05-13。
- 来源类型：Ahrefs 行业研究。
- 一手/二手：行业自有数据，一手采集；结论解释为二手。
- 可信度：中高。样本量大、方法相对清楚，但只覆盖其数据库中的 US AI Overview keywords。

### 10. AI Mode 与 AI Overviews 不是同一个 citation surface

- 判断：Ahrefs 对 73 万 response pairs 的研究显示，AI Mode 与 AI Overviews 的 URL citation overlap 只有 13.7%，但语义相似度平均 86%；AI Overviews 更偏视频和 Reddit 等社区平台，AI Mode 答案更长、实体更多。
- URL：https://ahrefs.com/blog/ai-overviews-vs-ai-mode/
- 发布日期：2025-12-15。
- 来源类型：Ahrefs 行业研究。
- 一手/二手：行业自有数据，一手采集；解释为二手。
- 可信度：中高。
- 操作含义：不能把“Google AI 搜索”合并成一个指标。至少分开测 AI Overviews、AI Mode、Gemini。

### 11. 2025 下半年到 2026 初，Reddit citation 出现明显波动

- 判断：Semrush 对 2025-07-14 至 2025-10-12 的 23 万 prompts、1 亿 citations 分析称，ChatGPT 中 Reddit citation 8 月接近 60% prompt responses 后在 9 月中降至约 10%；AI Mode 和 Perplexity 相对稳定但也有不同方向变化。
- URL：https://www.semrush.com/blog/most-cited-domains-ai/
- 发布日期：2025-11-10。
- 来源类型：Semrush 行业研究。
- 一手/二手：行业自有数据，一手采集；原因解释为二手推断。
- 可信度：中高。
- 操作含义：skill 必须要求重复测量与时间窗口，不应根据一次 prompt 截图判断 Reddit 策略有效。

### 12. “Reddit 最重要”存在强反证：品牌自有/可控来源仍可能主导

- 判断：Search Engine Land 报道 Yext 对 680 万 AI citations 的分析称，在 ChatGPT、Gemini、Perplexity 中，86% citations 来自品牌拥有或管理的来源；forums 只有 2%。
- URL：https://searchengineland.com/ai-search-citations-brand-controlled-sources-463166
- 发布日期：2025-10-09。
- 来源类型：Search Engine Land 对 Yext 报告的行业报道。
- 一手/二手：二手报道；原始数据来自 Yext。
- 可信度：中。它是重要反证，但行业、intent、平台选择可能与 Reddit-heavy 数据集不同。
- 操作含义：Reddit 是 off-site evidence layer，不是品牌官网、产品页、结构化信息、第三方评测的替代品。

### 13. 没有 universal top source，Reddit 权重强烈依赖平台、行业、意图

- 判断：Search Engine Land/Tinuiti Q1 2026 AI Citation Trends 称 2025-10 至 2026-01 期间，不存在统一 top source；Reddit 在全部类别和平台中 citation share 至少增长 73%，但 Google AI Overviews 的社交引用中 Reddit 44%，Google Gemini 只有 5%；Perplexity 2026-01 有 24% citations 来自 Reddit。
- URL：https://searchengineland.com/ai-citation-data-no-universal-top-source-brands-471285
- 发布日期：2026-03-17。
- 来源类型：Search Engine Land 行业分析，披露作者来自 Tinuiti。
- 一手/二手：二手/作者关联行业报告。
- 可信度：中。适合做“不要一刀切”的反证，具体数值需回查 Tinuiti 原报告。

### 14. Peec AI / Search Engine Land 样本支持 Reddit 是跨平台高频域名

- 判断：Search Engine Land 报道 Peec AI 对 3000 万 sources 的分析称，Reddit 是 ChatGPT、Google AI Mode、Gemini、Perplexity、AI Overviews 的最常被引用域名，YouTube、LinkedIn、Wikipedia、Forbes 也在 top five。
- URL：https://searchengineland.com/ai-search-engines-cite-reddit-youtube-and-linkedin-most-study-473138
- 发布日期：2026-03-31。
- 来源类型：Search Engine Land 对 Peec AI 报告的行业报道。
- 一手/二手：二手报道；原始数据来自 Peec AI。
- 可信度：中。结论方向与 Profound/Ahrefs 相互印证，但仍是供应商数据。

### 15. Perplexity 与 Reddit 的官方合作证据不足

- 判断：未找到 Perplexity 与 Reddit 的官方内容/API 合作公告。相反，Reddit 在 2025 年诉讼材料中主张 Perplexity 没有 Reddit license，并指控其通过搜索结果/第三方 scraper 获得 Reddit 内容；这些是 Reddit 单方诉讼主张，未等于法院认定事实。
- URL：https://redditinc.com/hubfs/Reddit%20Inc/Content/Reddit%20v.%20SerpApi.pdf
- 发布/提交日期：诉讼文件标注 filed 2025-10-22。
- 来源类型：Reddit 官方披露的法院文件。
- 一手/二手：一手诉讼材料，但内容是当事方主张。
- 可信度：中。可用于否定“已有公开官方合作”的说法；不能用于最终判定 Perplexity 的实际行为。

## 可证实事实

1. Reddit 与 Google 在 2024-02-22 宣布扩大合作，Google 获得 Reddit Data API 访问；Google 官方称该 API 提供 real-time、structured、unique content，并帮助更准确相关地理解、展示、训练和使用 Reddit 内容。
2. Reddit 与 OpenAI 在 2024-05-16 宣布合作，OpenAI 通过 Reddit Data API 获得 Reddit 内容，用于 ChatGPT 和新产品，特别是近期话题。
3. Google AI Overviews 与 AI Mode 会在生成答案时寻找支持网页；Google 官方确认它们可能使用 query fan-out，且 AI Mode 与 AI Overviews 的结果和链接会不同。
4. Reddit 在 2024-12 推出 Reddit Answers，2026-05 帮助文档显示其 AI search 已支持多语言、跨平台，并给出 inline citations 到原始 Reddit post/comment。
5. Reddit 2025-Q2 股东信称 Reddit core search 有 7000 万 weekly users，Reddit Answers 有 600 万 weekly users，搜索是公司战略方向。

## 行业研究样本

| 来源 | 样本/口径 | Reddit 可见性观察 | 可信度 |
|---|---:|---|---|
| Profound, 2025-06-05 / updated 2025-08 | 2024-08 至 2025-06，6.8 亿 citations | Reddit 是 Google AI Overviews overall citation #1（2.2%）和 Perplexity #1（6.6%）；top 10 share 中 AIO 21.0%、Perplexity 46.7% | 中高 |
| Ahrefs, 2025-05-13 | 2500 万 US AI Overview keywords | Reddit.com 在 AIO citations market share 达 5.5%，较 2025-03-12 的 1.3% 上升 | 中高 |
| Ahrefs, 2025-12-15 | 73 万 AI Mode / AI Overview response pairs | 同语义问题可用不同来源回答；AI Mode 与 AIO citation overlap 只有 13.7% | 中高 |
| Semrush, 2025-11-10 | 23 万 prompts，1 亿 citations，13 周 | ChatGPT 中 Reddit citation 大幅波动；Reddit/Wikipedia 仍是高频源但不稳定 | 中高 |
| Search Engine Land / Tinuiti, 2026-03-17 | 9 verticals、7 AI platforms、4 个月至 2026-01 | Reddit citation share 增长，但各平台和品类差异巨大；Perplexity 2026-01 有 24% citations 来自 Reddit | 中 |
| Search Engine Land / Peec AI, 2026-03-31 | 3000 万 sources | Reddit 被报道为跨 ChatGPT、Google AI Mode、Gemini、Perplexity、AI Overviews 的最常引用域名 | 中 |
| Search Engine Land / Yext, 2025-10-09 | 680 万 citations、160 万 queries | 反证：品牌自有/管理来源占 86%，forums 仅 2% | 中 |

## 为什么 Reddit 影响 GEO

### 1. 供给层：AI 平台直接需要“实时人类对话”

Google 与 OpenAI 的官方合作都指向同一类资产：实时、结构化、动态、独特的人类对话。Reddit 的价值不只是网页能被抓取，而是 Data API 提供了更稳定的结构化访问路径。对 GEO 来说，这意味着 Reddit 不是普通外链源，而是已被大型 AI/search 公司明确采购或接入的数据供给层。

### 2. 检索层：query fan-out 会扩大“问题证据面”

传统 SEO 经常围绕主关键词排名。AI search 的 query fan-out 会把一个问题拆成多个相关问题，例如“best X for Y”“X vs Y”“is X worth it”“real user complaints about X”。Reddit 天然覆盖这些长尾比较、吐槽、实测、替代方案和购买犹豫场景。

### 3. 答案层：LLM 不只找事实，也找“经验判断”

Wikipedia、官方文档、产品页擅长回答“是什么”；Reddit 更擅长回答“真实用户怎么看”“有没有坑”“哪种场景适合”。在推荐、购买、替代、故障排查、生活经验、软件选型等 prompt 中，Reddit 线程可能成为“真实世界证据”。

### 4. 实体层：品牌可能以“被别人谈论”的方式进入答案

GEO 不只看 URL citation。AI answer 可能没有引用品牌官网，但会在答案中提到品牌、竞品、品类属性、优缺点。Reddit 讨论能影响的是 off-site entity context：一个品牌是否常与某个 use case、痛点、优点、缺点共同出现。

### 5. 分发层：Reddit 本身正在变成 AI answer surface

Reddit Answers / Reddit AI search 会把站内帖子评论重新组织为答案，并带原始引用。即使不考虑 Google/OpenAI，Reddit 内部也正在把“帖子讨论”变成“答案资产”。

## 品牌提及 / 实体答案 / UGC 证据如何测量

### 1. Prompt corpus

建立不少于 30-50 个 prompt，按意图分组：

- 品类推荐：`best [category] for [use case]`
- 购买犹豫：`is [brand/product] worth it`
- 竞品比较：`[brand A] vs [brand B] for [job]`
- 风险/缺点：`problems with [brand/product]`
- Reddit 显性：`what do Reddit users think about [brand/product]`
- 非 Reddit 显性：同一问题删除 `Reddit`，观察自然是否仍引用 Reddit
- 长尾场景：预算、地区、经验水平、设备、年龄、行业、约束条件

### 2. 平台分开测

至少分开记录：

- Google AI Overviews
- Google AI Mode
- Gemini
- ChatGPT with search
- Perplexity
- Reddit AI search / Reddit Answers

不要合并成“Google”或“AI 搜索”。Ahrefs 与 Tinuiti 样本都显示同一母公司或同一语义问题下，citation source 也会明显不同。

### 3. 每次采集的字段

建议用表格记录：

- `date`
- `locale`
- `platform`
- `prompt`
- `answer_present`
- `brand_mentioned`
- `brand_rank_in_answer`
- `brand_sentiment`：positive / neutral / negative / mixed
- `reddit_cited`
- `reddit_url`
- `subreddit`
- `thread_title`
- `comment_or_post`
- `citation_position`
- `co_cited_domains`
- `competitors_mentioned`
- `answer_claim_supported_by_reddit`
- `screenshot_or_export_path`

### 4. 区分三类命中

- **Citation hit**：答案支持链接明确指向 Reddit URL。
- **Entity hit**：答案正文提到品牌/产品/竞品，但没有 Reddit citation。
- **Evidence hit**：答案中的某个判断可追溯到 Reddit 线程的用户经验，即使最终引用了别的域名。

skill 里应优先追踪 citation hit，但不能忽略 entity hit。很多 AI answer 的影响发生在“提到谁、怎么描述谁”，不是只发生在点击。

### 5. 追踪 Reddit 线程质量，而不是只看 upvotes

对每条候选线程记录：

- 问题是否清晰具体。
- 回答是否直接解决一个 use case。
- 是否有正反两面和真实约束。
- 是否包含品牌、竞品、替代方案、价格、失败场景。
- 讨论是否非营销口吻。
- 是否是目标品类中 AI answer 已经反复引用的 subreddit。
- 帖子年龄：新内容重要，但旧的 evergreen 经验帖也可能被引用。

### 6. 做 baseline / after 对比

Reddit GEO 的验证不能靠一次截图：

1. 先跑 2-3 天 baseline，记录平台波动。
2. 再做合规社区参与、FAQ 补充、产品解释、用户案例整理。
3. 观察 2-6 周内 Reddit citation、品牌 entity mention、sentiment 和竞品共现变化。
4. 同时看 Google Search 中 Reddit thread 是否进入 top results，因为 Google 官方说 AI feature supporting links 要先满足可索引和 snippet eligibility。

### 7. 不要伪造社区信号

Reddit 的 GEO 价值来自真实人类经验。刷帖、硬广、品牌小号、伪装用户反馈很可能被社区删除、被模型识别为低质量，甚至带来负面训练信号。更稳妥的动作是：找到已经讨论该问题的线程，用品牌官方身份或真实用户视角补充可核验信息、限制条件、解决步骤。

## 反证 / 不确定性

1. **“Google/OpenAI 有 Reddit 合作，所以 Reddit 一定进答案”证据不足。** 合作证明数据可访问，不证明某个品牌、帖子或 subreddit 会被引用。
2. **“Perplexity 与 Reddit 有官方合作”未证实。** 当前未找到双方官方公告；Reddit 诉讼材料反而主张 Perplexity 没有 license，但这是单方诉讼说法。
3. **“Reddit 是所有 AI answer 的第一来源”过度概括。** Profound、Ahrefs、Peec 等样本支持 Reddit 高频；Yext、Tinuiti 样本显示品牌自有站、商家列表、品类差异、平台差异会显著改变结论。
4. **“AEO/GEO 已替代 SEO”与 Google 官方表述冲突。** Google 明确说从 Search 角度仍是 SEO；AI features supporting links 没有额外技术要求，但必须可索引、可显示 snippet。
5. **“Upvote / karma 决定 AI citation”证据不足。** 行业观察更支持“具体问题 + 直接回答 + 自然语言 + 正反约束 + 可检索文本”比单纯热度更重要。
6. **“品牌账号经营 Reddit 就能影响 AI 答案”证据不足。** 多数 AI citation 指向具体讨论线程或答案，不是品牌 profile 或 subreddit 首页。
7. **“一次 prompt 截图可当证据”不可靠。** Semrush、Ahrefs 都显示 citation 会随时间、平台、生成轮次明显变化。
8. **“Reddit 对所有行业同样有效”证据不足。** Reddit 更适合真实经验、推荐、替代、故障排查、软件/硬件/消费决策等场景；强监管、高专业门槛、事实型 YMYL 场景可能更依赖权威站点。

## 对 skill 的操作启发

1. **把 Reddit GEO 定义为证据工程，不定义为发帖技巧。** 目标不是制造帖子，而是让真实用户问题、约束、比较和答案在 AI 可检索的 Reddit 线程中清晰存在。
2. **先找 AI 已经信任的 subreddit。** 对目标品类跑 30-50 个 prompt，统计反复被引用的 3-5 个 subreddit，再决定是否参与。
3. **优先做 Q&A 型内容。** Reddit 线程最适合承载“问题-回答”结构：用户痛点、上下文、限制、可选方案、为什么推荐/不推荐。
4. **每条建议都要带反面证据。** AI answer 需要真实评估，不是营销稿。skill 应要求写出缺点、适用边界、替代方案。
5. **测量时分开 citation、entity mention、sentiment。** 不要只问“有没有链接”；答案正文中的品牌排序、语气和共现竞品同样重要。
6. **按平台拆 dashboard。** Google AI Overviews、AI Mode、Gemini、ChatGPT、Perplexity、Reddit AI search 分别记录，不合并。
7. **用重复采样替代单次截图。** 最少连续 3 天 baseline；重要品类做每周复测。
8. **把官网 SEO 与 Reddit UGC 联动。** Google 官方仍要求可索引、snippet eligible、people-first content；Reddit 不是替代官网，而是补充“真实使用证据”。
9. **不要承诺因果。** 更准确的 promise 是“提高被 AI answer 可引用的 off-site evidence density”，不是“保证进入 AI Overview”。
10. **设置合规红线。** 禁止伪装用户、刷赞、批量灌水、跨 subreddit 复制粘贴、无 disclosure 的品牌推广。

## 可用于最终 skill 的最小检测流程

1. 输入品牌、产品、品类、3 个核心 use cases、5 个竞品。
2. 自动生成 30-50 个 prompt，覆盖推荐、比较、风险、替代、Reddit 显性/非显性。
3. 分平台采集答案：AIO / AI Mode / Gemini / ChatGPT / Perplexity / Reddit AI search。
4. 提取 citation URLs、Reddit 线程、subreddit、品牌实体、竞品实体、sentiment。
5. 生成 Reddit opportunity map：
   - 已被 AI 引用的 subreddit
   - 已被 AI 引用的线程
   - 品牌缺席但竞品出现的 prompt
   - 负面 sentiment 高的 prompt
   - 官网内容可补强的事实缺口
6. 输出动作建议：
   - 社区阅读，不发言
   - 官方身份答疑
   - 帮助文档补强
   - 找用户案例
   - 不适合介入
7. 2-6 周后复测，比较 citation/entity/sentiment 变化。

## 来源清单

- Reddit + Google partnership, 2024-02-22: https://redditinc.com/news/reddit-and-google-expand-partnership
- Google + Reddit partnership, 2024-02-22: https://blog.google/company-news/inside-google/company-announcements/expanded-reddit-partnership/
- OpenAI + Reddit partnership, 2024-05-16: https://openai.com/index/openai-and-reddit-partnership/
- Google AI features and websites, current docs: https://developers.google.com/search/docs/appearance/ai-features
- Google AI optimization guide, current docs: https://developers.google.com/search/docs/fundamentals/ai-optimization-guide
- Google AI Overviews launch, 2024-05-14: https://blog.google/products-and-platforms/products/search/generative-ai-google-search-may-2024/
- Google PDF, How AI Overviews in Search work, 2024-07: https://www.google.com/search/howsearchworks/google-about-AI-overviews.pdf
- Reddit Answers launch, 2024-12-09: https://redditinc.com/news/introducing-reddit-answers
- Reddit AI search help, updated 2026-05-26: https://support.reddithelp.com/hc/en-us/articles/32026729424916-Reddit-s-AI-search
- Reddit Q2 2025 shareholder letter, 2025-07-31: https://s203.q4cdn.com/380862485/files/doc_financials/2025/q2/Q2-25-Shareholder-Letter.pdf
- Profound AI citation patterns, 2025-06-05 / updated 2025-08: https://www.tryprofound.com/blog/ai-platform-citation-patterns
- Ahrefs AI Overview growth, 2025-05-13: https://ahrefs.com/blog/ai-overview-growth/
- Ahrefs AI Mode vs AI Overviews, 2025-12-15: https://ahrefs.com/blog/ai-overviews-vs-ai-mode/
- Semrush most-cited domains in AI, 2025-11-10: https://www.semrush.com/blog/most-cited-domains-ai/
- Search Engine Land / Yext counter-evidence, 2025-10-09: https://searchengineland.com/ai-search-citations-brand-controlled-sources-463166
- Search Engine Land / Tinuiti platform variance, 2026-03-17: https://searchengineland.com/ai-citation-data-no-universal-top-source-brands-471285
- Search Engine Land / Peec AI cross-platform citation sample, 2026-03-31: https://searchengineland.com/ai-search-engines-cite-reddit-youtube-and-linkedin-most-study-473138
- Reddit v. SerpApi / Perplexity complaint, filed 2025-10-22: https://redditinc.com/hubfs/Reddit%20Inc/Content/Reddit%20v.%20SerpApi.pdf
