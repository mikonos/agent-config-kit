# Agent 4 Research: Reddit cases and anti-patterns for SEO/GEO

Date: 2026-06-27

Role: 调研 Reddit 营销、社区 PR、SEO/GEO 增长案例、失败案例和反模式。本文只提供研究材料，不负责最终 `SKILL.md`。

## 0. 结论摘要

Reddit 的 SEO/GEO 价值来自三类信号：真实用户问题、可被搜索/AI 检索的长尾讨论、品牌代表在高意图语境里的可信介入。它不是“批量发帖换 AI 引用”的渠道。越像操控自然提及，越容易被 Reddit 用户、版主、平台政策和 FTC 广告披露规则同时惩罚。

关键判断：

1. Reddit 已经是搜索与 AI 答案的重要第三方语料面，但引用强度会随平台、行业、prompt 意图变化，不能把“Reddit 是第一来源”当成通用策略。
   - URL: https://searchengineland.com/ai-search-engines-cite-reddit-youtube-and-linkedin-most-study-473138
   - URL: https://searchengineland.com/ai-citation-data-no-universal-top-source-brands-471285
   - 来源类型: SEO 行业媒体 + AI visibility 数据复盘
   - 一手/二手: 二手，转述 Peec AI / Tinuiti 等数据
   - 可信度: 中高。适合判断趋势，不适合作为单品牌预测。

2. 能产生品牌搜索/GEO 价值的 Reddit 参与，通常是“高意图问题 + 真实经验 + 透明身份 + 可被后来搜索者复用”的组合，而不是链接投放。
   - URL: https://www.semrush.com/blog/reddit-seo/
   - URL: https://searchengineland.com/a-smarter-reddit-strategy-for-organic-and-ai-search-visibility-459369
   - 来源类型: SEO 工具厂商指南 + Search Engine Land 专栏
   - 一手/二手: 二手，含工具数据与策略归纳
   - 可信度: 中高。Semrush 有工具立场，策略仍与 Reddit 政策一致。

3. Reddit 官方规则把 spam 定义为重复或未经请求的行为；多账号、投票操控、批量推广、隐藏身份、用 AI/自动化制造垃圾内容，都是高风险区。
   - URL: https://redditinc.com/policies/reddit-rules
   - URL: https://support.reddithelp.com/hc/en-us/articles/360043504051-Spam
   - URL: https://support.reddithelp.com/hc/en-us/articles/360043066412-Disrupting-Communities
   - 来源类型: Reddit 官方政策
   - 一手/二手: 一手
   - 可信度: 高。应作为 skill 的硬边界。

4. Astroturfing 的核心风险不是“用户一定能立刻识破”，而是只要被识破一次，就会把品牌、代理商和自然讨论一起污染。
   - URL: https://www.pcgamer.com/games/game-marketing-company-takes-down-blog-post-bragging-about-how-good-it-is-at-astroturfing-reddit-after-reddit-finds-the-post/
   - URL: https://www.ftc.gov/business-guidance/resources/ftcs-endorsement-guides-what-people-are-asking
   - URL: https://www.ftc.gov/news-events/news/press-releases/2024/08/federal-trade-commission-announces-final-rule-banning-fake-reviews-testimonials
   - 来源类型: 第三方新闻 + FTC 官方广告披露/假评论规则
   - 一手/二手: PC Gamer 为二手但引用归档材料；FTC 为一手
   - 可信度: 高。适合转成禁止事项。

5. B2B/SaaS 更适合专家答疑、技术问题解释、AMA、长期评论；DTC 更适合真实使用场景、比较、售前疑虑；本地服务/高客单服务更依赖地理、需求时机和再营销，不适合伪装成“邻居推荐”。
   - URL: https://www.business.reddit.com/success-stories/advertisers/threatlocker
   - URL: https://www.business.reddit.com/success-stories/advertisers/warpstream
   - URL: https://www.business.reddit.com/success-stories/advertisers/dbrand
   - URL: https://www.business.reddit.com/success-stories/advertisers/montana-fire-pits
   - 来源类型: Reddit for Business 案例库
   - 一手/二手: 一手/平台自报，数据来自 Reddit internal、Ads Manager 或客户
   - 可信度: 中。适合看模式，不应照搬 KPI。

## 1. Sources scanned

| Source | URL | 类型 | 一手/二手 | 可信度 | 用途 |
|---|---|---|---|---|---|
| Reddit Rules | https://redditinc.com/policies/reddit-rules | 平台政策 | 一手 | 高 | 真实性、社区规则、反 spam 总边界 |
| Reddit Help: Spam | https://support.reddithelp.com/hc/en-us/articles/360043504051-Spam | 平台政策 | 一手 | 高 | spam 定义、批量推广、自动化风险 |
| Reddit Help: Disrupting Communities | https://support.reddithelp.com/hc/en-us/articles/360043066412-Disrupting-Communities | 平台政策 | 一手 | 高 | 投票操控、多账号、ban evasion |
| Reddit legacy self-promotion guide | https://www.reddit.com/r/reddit.com/wiki/selfpromotion/ | 平台历史指南 | 一手但已标注不再更新 | 中 | 文化语法：不要成为“带账号的网站” |
| FTC Endorsement Guides FAQ | https://www.ftc.gov/business-guidance/resources/ftcs-endorsement-guides-what-people-are-asking | 监管指南 | 一手 | 高 | 付费/雇佣/利益关系披露 |
| FTC fake reviews final rule | https://www.ftc.gov/news-events/news/press-releases/2024/08/federal-trade-commission-announces-final-rule-banning-fake-reviews-testimonials | 监管公告 | 一手 | 高 | 假评论、insider review、假社交指标 |
| Search Engine Land: AI sources | https://searchengineland.com/ai-search-engines-cite-reddit-youtube-and-linkedin-most-study-473138 | SEO 媒体 | 二手 | 中高 | Reddit 在 AI citation 中的趋势 |
| Search Engine Land: no universal top source | https://searchengineland.com/ai-citation-data-no-universal-top-source-brands-471285 | SEO 媒体 | 二手 | 中高 | 防止把 Reddit 绝对化 |
| Search Engine Land: Reddit strategy | https://searchengineland.com/a-smarter-reddit-strategy-for-organic-and-ai-search-visibility-459369 | SEO 专栏 | 二手 | 中 | crawl/walk/run、透明参与 |
| Search Engine Land: Reddit product review SERPs | https://searchengineland.com/reddit-dominates-google-search-discussions-forums-437501 | SEO 媒体 | 二手 | 中高 | Reddit 在 Google forum SERP 的可见性与 spam 风险 |
| Ahrefs: AI Overview growth | https://ahrefs.com/blog/ai-overview-growth/ | SEO 数据研究 | 一手/工具数据 | 中高 | Reddit 在 AI Overviews 中的增长 |
| Semrush: Reddit SEO | https://www.semrush.com/blog/reddit-seo/ | SEO 工具指南 | 一手/工具数据 + 二手建议 | 中 | Reddit SEO 指标和操作建议 |
| Semrush: most-cited AI domains | https://www.semrush.com/blog/most-cited-domains-ai/ | SEO 数据研究 | 一手/工具数据 | 中高 | AI citation volatility |
| SparkToro: Search Everywhere Optimization | https://sparktoro.com/blog/its-still-seo-search-everywhere-optimization/ | 行业观点 | 二手/方法论 | 中高 | 把 GEO 放回 Search Everywhere，而不是新术语崇拜 |
| SparkToro: zero-click 2026 | https://sparktoro.com/blog/in-2026-less-than-one-third-of-google-searches-still-send-a-click/ | 数据观点 | 二手/Similarweb 数据解释 | 中高 | 品牌影响不只看点击 |
| Reddit Pro | https://www.business.reddit.com/pro | Reddit 产品页 | 一手 | 中高 | 官方鼓励监控关键词、参与客户讨论 |
| Reddit for Business: ThreatLocker | https://www.business.reddit.com/success-stories/advertisers/threatlocker | 平台案例 | 一手/平台自报 | 中 | B2B AMA 与 pipeline 案例 |
| Reddit for Business: WarpStream | https://www.business.reddit.com/success-stories/advertisers/warpstream | 平台案例 | 一手/平台自报 | 中 | B2B developer audience + free-form ads |
| Reddit for Business: dbrand | https://www.business.reddit.com/success-stories/advertisers/dbrand | 平台案例 | 一手/平台自报 | 中 | DTC organic community + paid expansion |
| Reddit for Business: Under 5'10 | https://www.business.reddit.com/success-stories/advertisers/under-510 | 平台案例 | 一手/平台自报 | 中 | DTC commerce + DPA/Shopify |
| Reddit for Business: Montana Fire Pits | https://www.business.reddit.com/success-stories/advertisers/montana-fire-pits | 平台案例 | 一手/平台自报 | 中 | 高客单/contractor targeting |
| Marketing Examined: Caliber | https://www.marketingexamined.com/blog/reddit-ad-built-community | 营销复盘 | 二手 | 中 | 坦诚广告转社区的模式 |
| PC Gamer: Trap Plan / War Robots | https://www.pcgamer.com/games/game-marketing-company-takes-down-blog-post-bragging-about-how-good-it-is-at-astroturfing-reddit-after-reddit-finds-the-post/ | 新闻报道 | 二手，含归档材料 | 高 | astroturfing 反例 |
| Reddit AMA: Woody Harrelson | https://www.reddit.com/r/IAmA/comments/p9a1v/im_woody_harrelson_ama/ | Reddit 原帖 | 一手 | 高 | 失败 AMA 原始证据 |
| Observer: Woody Harrelson AMA | https://observer.com/2012/02/woody-harrelson-and-the-no-good-very-bad-reddit-ama/ | 媒体复盘 | 二手 | 中 | PR 失败解读 |

## 2. 模式库

### 模式 1：高意图问题线程，不是品牌广播

有效参与通常发生在用户已经在问“哪个更好”“是否值得”“怎么解决”“有没有替代品”的语境里。Reddit 线程之所以能进入 Google/AI 答案，不是因为品牌塞入了关键词，而是因为讨论呈现真实经验、异议、比较和后续追问。

关键判断：

- Reddit 对 SEO/GEO 的价值来自用户主动研究行为。Search Engine Land 报道 Reddit 在 AI-generated answers 中被高频引用；Semrush 也把 Reddit SEO 定义为提升 Google 与 AI answer 可见性。  
  URL: https://searchengineland.com/ai-search-engines-cite-reddit-youtube-and-linkedin-most-study-473138  
  URL: https://www.semrush.com/blog/reddit-seo/  
  来源类型: SEO 媒体/工具研究；一手/二手: 二手 + 工具数据；可信度: 中高。

- 但 AI citation 没有 universal top source。不同模型、行业、prompt 意图会改变来源结构，所以 SOP 必须先做 niche-level evidence scan。  
  URL: https://searchengineland.com/ai-citation-data-no-universal-top-source-brands-471285  
  来源类型: SEO 媒体；一手/二手: 二手；可信度: 中高。

可操作模式：

- 找到 Google 已排名、AI answers 已引用或目标用户高频提问的 Reddit threads。
- 优先补“具体经验、故障排查、参数、限制、对比”，少放链接。
- 用官方或清晰披露身份的账号回答，接受反问和负面反馈。
- 衡量品牌搜索、referral、thread visibility、AI citation presence、sentiment，而不是只数发帖量。

### 模式 2：专家型 AMA 与技术答疑，适合 B2B/SaaS

B2B/SaaS 的 Reddit 价值不是“打广告给决策者”，而是出现在真实买方委员会的信息搜集中：IT、开发者、采购、使用者会在不同 subreddits 中评估问题和方案。

案例：ThreatLocker

- ThreatLocker 用 AMA + takeover + 多格式广告触达 cybersecurity buying committee。Reddit for Business 报告 AMA upvote rate 32%，CPC 低于行业均值 64%，Reddit 成为 qualified pipeline 的主要引擎之一。  
  URL: https://www.business.reddit.com/success-stories/advertisers/threatlocker  
  来源类型: Reddit for Business 案例；一手/二手: 一手/平台自报，数据源 Reddit internal + HockeyStack；可信度: 中。平台有商业立场，但案例结构可借鉴。

案例：WarpStream

- WarpStream 面向开发者/工程师，使用 subreddit 和 keyword targeting，并在 free-form ads 中保持评论开启，主动回复评论以建立关系。案例报告 74x ROAS，15% marketing influenced deals came from Reddit。  
  URL: https://www.business.reddit.com/success-stories/advertisers/warpstream  
  来源类型: Reddit for Business 案例；一手/二手: 一手/客户自报；可信度: 中。

可操作模式：

- 先从“问题领域”而不是“产品类目”找社区：例如 Kafka cost、endpoint security、SOC workflow、dev tooling。
- 让 SME/工程师/PM 直接参与，减少营销话术。
- AMA 前准备可公开回答的技术边界、失败条件、竞品比较原则。
- 广告可以放大触达，但讨论必须能承受技术追问。

### 模式 3：拥有社区不是发布阵地，而是长期证据池

品牌 subreddit 或官方账号的价值在于持续收集使用场景、抱怨、比较、FAQ 和客户语言。它能间接支持 SEO/GEO，因为后续搜索者和 AI retrieval 更容易看到有上下文的真实讨论。

案例：dbrand

- dbrand 先有 organic community `r/dbrand`，再扩展到 paid media。Reddit for Business 案例称其 Max campaigns 达成 6x ROAS、CPA 低于目标 43%、CTR 高于 benchmark 40%。  
  URL: https://www.business.reddit.com/success-stories/advertisers/dbrand  
  来源类型: Reddit for Business 案例；一手/二手: 一手/Ads Manager 数据；可信度: 中。

案例：Caliber

- Marketing Examined 复盘称 Caliber 的 Reddit ad 没有直接强推下载，而是以坦诚口吻请求反馈并引导加入 subreddit，社区达到约 16k members。  
  URL: https://www.marketingexamined.com/blog/reddit-ad-built-community  
  来源类型: 营销 newsletter 复盘；一手/二手: 二手；可信度: 中。适合看创意和 funnel，不适合作为财务表现证据。

可操作模式：

- 官方社区优先服务：support、roadmap feedback、FAQ、known issues、真实用户用法。
- 不要把自有 subreddit 做成全是自家链接的 SEO farm。Reddit legacy self-promotion guide 明确把这种行为视为 linkfarming/using reddit for SEO 的风险。  
  URL: https://www.reddit.com/r/reddit.com/wiki/selfpromotion/  
  来源类型: Reddit 历史指南；一手/二手: 一手但已不再更新；可信度: 中。

### 模式 4：DTC/电商适合“使用场景 + 产品目录 + 再营销”，不适合伪装评测

DTC 的高价值线程通常是“值不值得买”“尺码/质量/耐用性”“替代品比较”“售后体验”。这里的品牌参与必须接受真实缺点，否则看起来像 affiliate spam。

案例：Under 5'10

- Under 5'10 使用 Reddit Dynamic Product Ads + Shopify integration，同步产品和价格。案例称 ROAS 7.7x，retargeting ROAS 13.6x。  
  URL: https://www.business.reddit.com/success-stories/advertisers/under-510  
  来源类型: Reddit for Business 案例；一手/二手: 一手/Ads Manager 数据；可信度: 中。

案例：dbrand

- dbrand 的模式不是只投商品广告，而是建立 tech enthusiast 场景中的品牌语气和社区，再放大 paid conversion。  
  URL: https://www.business.reddit.com/success-stories/advertisers/dbrand  
  来源类型: Reddit for Business 案例；一手/二手: 一手/平台自报；可信度: 中。

可操作模式：

- 产品页和 Reddit 评论要一致：规格、限制、退换、价格、兼容性不能冲突。
- 允许负面评价存在；只在事实错误、售后问题、使用方法上补充。
- 付费广告可以用 DPA/retargeting；自然线程不能让员工/代理商伪装成用户推荐。

### 模式 5：本地服务/高客单服务更像“需求捕捉 + 信任验证”，不是泛社区刷存在

本地服务、家装、医疗、法律、维修等领域，Reddit 的自然价值常在城市 subreddit、问题型 subreddit、购买前验证和避坑讨论。风险也更高，因为“邻居推荐”一旦是利益相关方伪装，属于信任欺骗。

案例：Montana Fire Pits

- Montana Fire Pits 面向高客单 outdoor product 与 contractor signup。Reddit for Business 案例称通过 Max campaigns + age-band targeting 增加 contractor signups 30%。  
  URL: https://www.business.reddit.com/success-stories/advertisers/montana-fire-pits  
  来源类型: Reddit for Business 案例；一手/二手: 一手/客户提供数据；可信度: 中。

案例：Culligan

- Culligan 作为 residential/commercial water treatment company，使用 Max prospecting traffic campaign，对比标准 campaign 后得到 lower CPC 与 higher click volume。  
  URL: https://www.business.reddit.com/success-stories/advertisers/culligan  
  来源类型: Reddit for Business 案例；一手/二手: 一手/Reddit internal；可信度: 中。

可操作模式：

- 本地服务自然参与只适合公开身份答疑：价格构成、许可/资质、常见坑、检查清单。
- 不要伪装成客户写“推荐某某公司”；这同时触发 Reddit authenticity 风险和 FTC endorsement/fake review 风险。
- 地域投放、retargeting、lead gen 可以走 Reddit Ads；organic engagement 用于信任和教育，不承担强转化压力。

## 3. 失败案例与反模式

### 反模式 1：把 AMA 当电影/产品巡演

案例：Woody Harrelson / Rampart AMA

- 原始 AMA 显示开场就围绕电影宣传；Observer 复盘认为他把 Reddit AMA 当成普通宣传采访，是失败起点。  
  URL: https://www.reddit.com/r/IAmA/comments/p9a1v/im_woody_harrelson_ama/  
  URL: https://observer.com/2012/02/woody-harrelson-and-the-no-good-very-bad-reddit-ama/  
  来源类型: Reddit 原帖 + 媒体复盘；一手/二手: 一手 + 二手；可信度: 高/中。

反模式定义：

- 只回答有利于宣传的问题。
- 回避用户真正关心的争议或历史问题。
- 用 PR 口吻替代个人/专家口吻。
- 不准备承接负面追问。

SOP 禁止项：

- 不做“只许问新品”的 AMA。
- AMA 必须先列出可答、不可答、必须透明说明的边界。
- 如果目标只是曝光，不要用 organic AMA，走 paid placement 或普通发布。

### 反模式 2：Astroturfing - 把广告伪装成自然讨论

案例：Trap Plan / War Robots: Frontiers

- PC Gamer 报道 Trap Plan 曾公开描述为游戏做约 100 条 organic-style Reddit posts/comments，后来被 Reddit 社区注意到并删除复盘。报道引用归档材料称内容设计成让用户和版主以为是自然讨论。  
  URL: https://www.pcgamer.com/games/game-marketing-company-takes-down-blog-post-bragging-about-how-good-it-is-at-astroturfing-reddit-after-reddit-finds-the-post/  
  来源类型: 新闻报道，含 Internet Archive 归档材料；一手/二手: 二手但证据链较强；可信度: 高。

政策/法律边界：

- Reddit Rules 要求 authentic participation，不得 spam 或 content manipulation。  
  URL: https://redditinc.com/policies/reddit-rules  
  来源类型: Reddit 官方政策；一手/二手: 一手；可信度: 高。

- FTC endorsement guidance 要求利益关系清晰披露；FTC fake reviews final rule 禁止 fake reviews、insider reviews without disclosure、购买假 social indicators。  
  URL: https://www.ftc.gov/business-guidance/resources/ftcs-endorsement-guides-what-people-are-asking  
  URL: https://www.ftc.gov/news-events/news/press-releases/2024/08/federal-trade-commission-announces-final-rule-banning-fake-reviews-testimonials  
  来源类型: FTC 官方；一手/二手: 一手；可信度: 高。

SOP 禁止项：

- 不创建或雇佣“看似无关”的账号来推荐品牌。
- 不批量制造“我刚发现一个产品/游戏/工具”的 discovery-style posts。
- 不要求员工、粉丝、代理商投票、顶帖、互评。
- 不用 AI 生成大量拟人评论。

### 反模式 3：自然提及 KPI 化

错误目标：要求团队“本月制造 50 条自然 Reddit 提及”。

为什么危险：

- 自然提及一旦被 KPI 化，执行层会倾向于伪装、刷量、换号、买评。
- Reddit spam policy 禁止 repeated or unsolicited mass engagement。  
  URL: https://support.reddithelp.com/hc/en-us/articles/360043504051-Spam  
  来源类型: Reddit 官方政策；一手/二手: 一手；可信度: 高。

- Disrupting Communities policy 禁止 vote manipulation、coordinated voting、multiple accounts 等行为。  
  URL: https://support.reddithelp.com/hc/en-us/articles/360043066412-Disrupting-Communities  
  来源类型: Reddit 官方政策；一手/二手: 一手；可信度: 高。

替代 KPI：

- 目标关键词下的高质量线程覆盖数。
- 官方回答被保留率、正负反馈、追问闭环率。
- Reddit-in-SERP visibility。
- AI answers 中品牌是否被正确描述。
- 品牌搜索、direct/referral、assisted conversion。

### 反模式 4：只为 SEO 建 subreddit

错误目标：为每条产品线建 subreddit，把官网内容搬进去，期待 Google/AI 抓取。

为什么危险：

- Reddit legacy self-promotion guide 明确说，即使是自有 subreddit，如果只提交自家链接，也可能被视为 link farming 或 using Reddit for SEO。  
  URL: https://www.reddit.com/r/reddit.com/wiki/selfpromotion/  
  来源类型: Reddit 历史指南；一手/二手: 一手但已不再更新；可信度: 中。

替代做法：

- 只有当已有真实用户问题、支持需求、社区成员和维护能力时才建 subreddit。
- 自有社区应以 support、FAQ、roadmap、用户作品、bug/issue、教育内容为主。
- 如果只是内容分发，使用 Reddit Ads 或外部内容渠道。

## 4. 自然提及 vs 操控提及

| 维度 | 自然提及 | 透明参与 | 操控提及 |
|---|---|---|---|
| 发起者 | 无利益关系用户 | 品牌员工/创始人/代理商公开身份 | 员工/代理商/水军伪装成普通用户 |
| 意图 | 分享经验、提问、比较、吐槽 | 解决问题、补充事实、承接反馈 | 制造“大家都在推荐”的假象 |
| 链接 | 用户自发，或按需补充 | 少量、相关、允许时提供 | 批量插入、跳转、追踪、affiliate 冒充 |
| 语气 | 有优点也有缺点 | 可解释限制，能承认不足 | 过度正面、模板化、回避追问 |
| 平台风险 | 低 | 低到中，取决于社区规则 | 高 |
| 法律/合规风险 | 低 | 低，前提是披露清楚 | 高，尤其涉及付费、员工、评价、推荐 |
| GEO/SEO 价值 | 高，可信但不可控 | 中高，可持续 | 短期可能有效，长期污染实体与品牌信任 |

判断规则：

1. 如果发帖者因品牌受雇、收钱、拿免费产品、拿佣金、参与代理项目，必须披露。
2. 如果内容的成功依赖“别人不知道我是品牌方”，就是操控。
3. 如果同一团队可控多个账号互相提问、附和、投票，就是操控。
4. 如果不能公开给版主说明操作方式，就不要做。
5. 如果这条内容被截图发到 `r/HailCorporate`、`r/Games` 或行业 subreddit 后会让品牌难堪，就不要做。

## 5. B2B / DTC / SaaS / 本地服务差异

| 类型 | Reddit 价值 | 推荐参与 | 高风险做法 | 推荐指标 |
|---|---|---|---|---|
| B2B | 买方委员会研究、技术可信度、竞品比较 | AMA、专家答疑、use case 解释、问题线程补充 | 销售私信、伪装用户推荐、只发 demo link | qualified discussion、influenced pipeline、branded search、Reddit-in-SERP |
| SaaS | troubleshooting、替代品比较、roadmap feedback、support | 官方账号答疑、公开 changelog、技术 deep dive、透明竞品比较 | 建多个小号问“有没有人用过 X”，再自答 | support deflection、feature feedback、trial assisted conversion |
| DTC | 使用体验、购买前疑虑、真实评价、deal/retargeting | 尺码/兼容性/耐用性解释，DPA/retargeting，社区反馈 | 假晒单、affiliate spam、删负评 | product thread visibility、ROAS、review sentiment、brand query lift |
| 本地服务 | 地域信任、避坑、资质/价格教育、需求时机 | 城市/主题社区公开答疑，地理投放，检查清单 | 伪装邻居推荐、自建假评论、攻击竞品 | local branded search、lead quality、CPC/CPL、negative issue resolution |

## 6. 可转成 SOP 的规则

### 6.1 进入前：证据扫描

1. 搜索 `site:reddit.com <category> best|vs|worth it|alternative|problem|near me|city`。
2. 记录目标关键词下已进入 Google SERP、Discussions and forums、AI Overviews、ChatGPT/Perplexity answers 的 Reddit threads。
3. 对每个 subreddit 记录：规则、版主严格度、品牌容忍度、链接规则、常见发帖格式、用户痛点。
4. 标记自然提及：正面、负面、中立、错误事实、未解问题。
5. 如果目标社区对品牌或自推明确禁止，只允许 listening，不做 organic posting。

### 6.2 参与前：身份和权限

1. 选择官方或清晰披露的账号名，例如 `BrandName_Official` 或 `BrandName_Tom`。
2. Profile 写清楚身份、职责、可回答范围和不能提供的内容。
3. 任何员工、代理商、创始人、投资人、affiliate 参与时都要披露关系。
4. 不使用个人旧号隐藏商业身份。
5. 不共用账号，不批量开号，不买号。

### 6.3 回复时：先帮助，后品牌

1. 先回答用户问题，再说明品牌相关性。
2. 先给可验证信息：步骤、参数、价格范围、限制、替代方案、适用/不适用场景。
3. 链接只在被问到、规则允许、或答案必须引用事实时放。
4. 明确承认缺点或边界：不支持什么、不适合谁、什么时候选竞品。
5. 遇到负面评价，优先解决事实和售后，不争辩用户感受。

### 6.4 放大时：广告与自然分开

1. 想规模化曝光，走 Reddit Ads，不把 organic engagement 当广告库存。
2. Paid creative 可以 Reddit-native，但不能伪装成无利益关系用户。
3. 广告评论区开启前必须准备 moderation、FAQ、support escalation。
4. Free-form ads/AMA/takeover 适合 B2B/SaaS 专业解释；DPA/retargeting 更适合 DTC/电商。
5. Paid campaign 的学习可以反馈到 SEO/content，但不要把 paid 评论包装成自然评价。

### 6.5 衡量时：不用“操控自然提及”作 KPI

推荐指标：

- Reddit-in-SERP count：目标关键词下 Reddit 线程是否出现、位置如何。
- Thread quality：高意图问题、评论深度、是否存在真实异议。
- Brand accuracy：AI answers 是否正确描述品牌、产品、限制。
- Branded demand：品牌搜索、direct traffic、assisted conversion。
- Engagement health：官方回复保留率、upvote ratio、追问闭环率、版主警告数。
- Risk signals：删除、锁帖、ban、用户质疑 astroturfing、`HailCorporate` 式评论。

禁用指标：

- “自然提及数量”硬目标。
- 小号发帖数。
- upvote 购买/互投。
- 未披露好评数。
- 只看 referral clicks，不看品牌搜索和零点击影响。

### 6.6 停止条件

出现以下任一情况，停止发帖并转为复盘：

- 版主删除或警告。
- 用户质疑账号关系且质疑成立。
- 内部无法清楚披露代理商/员工/激励关系。
- 需要多个账号互相配合才能让内容成立。
- 需要隐藏缺点、删除负面或误导体验。
- 目标 subreddit 明确禁止品牌参与或自我推广。

## 7. 对 skill 的操作启发

1. Skill 要先做“Reddit evidence scan”，再决定是否参与。不能默认推荐发帖。
2. Skill 必须内置 Reddit policy guardrails：spam、vote manipulation、ban evasion、misleading behavior、undisclosed affiliation 一律禁止。
3. Skill 应把 GEO 拆成可测项：AI citation、AI answer brand accuracy、Reddit-in-SERP、brand search lift。不要承诺“发 Reddit 就能进 AI 答案”。
4. Skill 输出应区分三种动作：listen、transparent engage、paid amplify。任何 stealth seed 都应被拒绝。
5. Skill 应要求行业分流：
   - B2B/SaaS：专家答疑、AMA、技术解释、社区 support。
   - DTC：购买疑虑、使用体验、真实评价、DPA/retargeting。
   - 本地服务：公开资质/价格/避坑教育，地理投放；禁止伪装邻居推荐。
6. Skill 应生成“可公开给版主看的参与说明”。如果说明写不出来，说明策略本身不干净。
7. Skill 应优先推荐补充事实、解决问题、承认限制，而不是插入品牌名。
8. Skill 要把失败案例作为 hard tests：
   - Rampart test：如果 AMA 只服务发布宣传，拒绝。
   - Trap Plan test：如果计划依赖 organic-style stealth posts，拒绝。
   - FTC test：如果有利益关系但用户看不出来，拒绝。
   - Subreddit rule test：如果社区规则不允许，拒绝或转 paid/listening。

## 8. 信息缺口

- Reddit for Business 案例多为平台/客户自报，KPI 可信度中等，需要第三方广告账户或品牌方复盘才能验证。
- AI citation 数据变化快。2025-2026 年已有 Reddit citation 上升、下跌、再分化的多份报告，skill 不应固化某个比例。
- 很多 Reddit 营销失败案例被删帖、删文或只留社区讨论，证据链常不完整。应优先使用官方政策和可归档新闻，不依赖单条 Reddit 评论。
- 本地服务的公开 Reddit 案例较少，现有证据更多来自 Reddit Ads 的 construction/home improvement 类目，不足以覆盖所有本地服务。
