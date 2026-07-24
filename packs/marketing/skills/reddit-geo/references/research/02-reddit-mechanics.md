# Reddit Geo Phase 1 Agent 2 Research: Reddit Platform Mechanics

调研日期：2026-06-27  
调研范围：Reddit 平台机制、subreddit 社区发现、搜索入口、排序与互动信号、发帖/评论/karma/审核/反垃圾/API/公开访问边界、人工参与边界。  
来源策略：优先 Reddit Help、Reddit Inc policy、Reddit for Business / Reddit Pro、Google 官方搜索文档；少量使用公开 subreddit 页面作为社区发现入口示例。未使用知乎、微信公众号、百度百科、百度知道。  
核心视角：Reddit 不是“内容发布渠道”，而是由站规、社区版规、版主自治、用户投票、账号声誉和反垃圾系统共同约束的社区网络。

## 摘要表

| 主题 | 关键判断 | 边界 | 来源与可信度 |
|---|---|---|---|
| Reddit 结构 | Reddit 是由大量 subreddit 组成的社区网络；subreddit 由 redditors 创建并由志愿版主管理，有 public / restricted / private / premium-only 等类型。 | 社区类型会影响可见性、发帖/评论权限和可采集性。 | S01 官方帮助，一手，高 |
| 社区发现 | 官方发现入口包括 Explore Communities、搜索、推荐、r/all / r/popular、trending lists；推荐受兴趣、相似社区、位置、社区活跃度和趋势影响。 | 推荐是个性化和动态的，不能当作稳定全量目录。 | S02/S03/S04 官方帮助，一手，高 |
| 搜索 | Reddit Search 支持社区内搜索、评论搜索、flair、字段过滤、布尔运算和 AI-powered search；Google `site:reddit.com` 是重要补充，但结果不保证完整。 | Reddit 搜索和 Google site 搜索都不等于全量数据库。 | S05/S06 官方帮助，一手，高；S07/S08 Google 官方，一手，高 |
| 排序与互动 | 搜索排序包括 Relevance、Hot、Top、New、Comment Count；社区默认通常是 Hot；推荐和排序会看 votes、comments、post age、flair、community、用户历史活动等。 | Reddit 没公开完整排名算法，只能使用官方披露的信号。 | S06/S09/S10/S11 官方帮助，一手，高 |
| Karma / 账号可信度 | Karma 来自帖子/评论收到的 upvote/downvote，但不是 1:1；部分社区有 karma 门槛；CQS 结合账号处罚历史、网络/位置、账号安全等信号，用于识别潜在 spam / 低质贡献者。 | CQS 是版主工具字段，不是公开可直接读取的普通指标。 | S12/S13 官方帮助，一手，高 |
| 审核/反垃圾 | Reddit 是多层治理：站规由 admins 执行，社区规则由 mods 执行；工具包括 reports、mod queue、Automoderator、Crowd Control、spam filters、post guidance。 | 单个社区的规则和 automod 条件可能更严格且不公开。 | S14/S15/S16/S17/S18/S19 官方帮助，一手，高 |
| API / 公开访问 | 公共内容可被未登录用户查看，但 API 访问需要遵守 Data API Terms、OAuth、User-Agent、删除内容同步、rate limits；免费 Data API 100 QPM/OAuth client id；商业、超限研究、AI 训练等需要授权或单独协议。 | 公开可见不等于可无限抓取、存储、商用或训练模型。 | S20/S21/S22/S23 官方政策/帮助，一手，高 |
| 人工参与 | 品牌/研究者可以参与真实对话、回答问题、提供支持，但必须读版规、发到最合适社区、避免重复/无关/商业链接轰炸，不确定时联系 mods。 | Reddit Geo skill 应把“观察和理解”放在“发言”之前。 | S24/S25/S26/S27 官方帮助/业务页，一手，高 |

## 证据表

| ID | 关键判断 | URL | 来源类型 | 一手/二手 | 可信度 | 对 skill 的用途 |
|---|---|---|---|---|---|---|
| S01 | subreddit 是 Reddit 内的小社区，由 redditors 创建和管理；可为 public / restricted / private / premium-only。 | https://support.reddithelp.com/hc/en-us/articles/204533569-What-are-communities-or-subreddits | Reddit Help | 一手 | 高 | 建立社区类型检查，不把所有 subreddit 当成同等可参与/可读取对象。 |
| S02 | Explore Communities 会基于 favorite communities、local trends、popular topics、featured handpicked、topic browsing 推荐相关/本地社区。 | https://support.reddithelp.com/hc/en-us/articles/17881389378196-How-do-I-browse-and-find-communities-on-the-Reddit-app | Reddit Help | 一手 | 高 | 社区发现阶段优先用官方 Explore 和 topic/trend 入口。 |
| S03 | 版主可控制社区 discoverability：是否出现在 r/all / r/popular、communities tab、trending lists、individual recommendations。 | https://support.reddithelp.com/hc/en-us/articles/15484078610708-How-can-I-control-how-people-find-my-community | Reddit Help / Mod Help | 一手 | 高 | 发现结果偏差解释：不出现在推荐中不等于社区不存在或不活跃。 |
| S04 | Reddit 推荐社区/内容时会考虑社区活跃度、全球和本地趋势、相似订阅/互动社区、位置等因素。 | https://support.reddithelp.com/hc/en-us/articles/23511859482388-Reddit-s-Approach-to-Content-Recommendations | Reddit Help | 一手 | 高 | 社区发现要记录“发现入口”，避免把个性化推荐当客观排名。 |
| S05 | Reddit Search 支持评论搜索、flair、社区内搜索、字段过滤（author/flair/self/selftext/site/subreddit/title/url）、布尔运算、AI-powered search。 | https://support.reddithelp.com/hc/en-us/articles/19696541895316-Available-search-features | Reddit Help | 一手 | 高 | 生成 Reddit 内部搜索 query 模板。 |
| S06 | Reddit 搜索排序包括 Relevance、Hot、Top、New、Comment Count；Relevance 会看词稀缺、帖子年龄、votes/comments。 | https://support.reddithelp.com/hc/en-us/articles/19695706914196-What-filters-and-sorts-are-available | Reddit Help | 一手 | 高 | 搜索结果采样时必须多排序、多时间窗，不只看默认 relevance。 |
| S07 | Google 支持 `site:`、引号、排除词、before/after/filetype 等 operator。 | https://support.google.com/websearch/answer/2466433?hl=en | Google Search Help | 一手 | 高 | Google 补充检索模板：`site:reddit.com/r/<subreddit> "query"`。 |
| S08 | Google `site:` 可限定域名/URL/prefix，但不保证返回全部已索引 URL；无 query 的 site 搜索不用于排名判断。 | https://developers.google.com/search/docs/monitor-debug/search-operators/all-search-site | Google Search Central | 一手 | 高 | 给 Google site 检索加“不完整/不排名”警告。 |
| S09 | Reddit 推荐信号包括 votes、comments、post age、post type、flair、community、用户 upvote/comment/停留/访问/订阅/位置/账号年龄。 | https://support.reddithelp.com/hc/en-us/articles/23511859482388-Reddit-s-Approach-to-Content-Recommendations | Reddit Help | 一手 | 高 | 评估帖子时不要只看 upvotes；加入评论、时间、flair、社区关系。 |
| S10 | Home feed Best 使用 ML 个性化排序，会参考用户是否喜欢新社区、账号新旧、过去 upvote/comment 类型。 | https://support.reddithelp.com/hc/en-us/articles/4402284777364-What-are-home-feed-recommendations | Reddit Help | 一手 | 高 | 不使用个人 home feed 作为研究主样本。 |
| S11 | 社区页默认通常按 Hot 排序；Hot 优先近期获得 upvotes/comments 的帖子，Top 可按时间过滤，New 看最新。 | https://support.reddithelp.com/hc/en-us/articles/23511859482388-Reddit-s-Approach-to-Content-Recommendations | Reddit Help | 一手 | 高 | 对每个 subreddit 至少看 Hot / Top week-month / New。 |
| S12 | Karma 反映帖子/评论收到的 upvotes/downvotes，但 upvotes 与 karma 非 1:1；部分社区因防 spam 设置 karma 门槛。 | https://support.reddithelp.com/hc/en-us/articles/204511829-What-is-karma | Reddit Help | 一手 | 高 | 账号准入检查：总 karma、post/comment karma、目标社区 karma。 |
| S13 | CQS 是用于识别潜在 spammer 或较低正向贡献概率用户的分类，参考过去账号动作、网络和位置、账号安全步骤，如 email verification。 | https://support.reddithelp.com/hc/en-us/articles/19023371170196-What-is-the-Contributor-Quality-Score | Reddit Help / Mod Help | 一手 | 高 | skill 应把账号可信度写成风险项，而不是只写“karma 够不够”。 |
| S14 | Reddit 多层审核：社区规则由 mods 执行，站规由 admins 执行；admins 使用自动检测、人工审查、用户报告、LLM 等工具。 | https://support.reddithelp.com/hc/en-us/articles/23511059871252-Content-Moderation-Enforcement-and-Appeals | Reddit Help | 一手 | 高 | 发言前必须同时检查 Reddit Rules 和 subreddit rules。 |
| S15 | mods 可移除社区内不合主题的帖子/评论、ban 破坏版规者、处理报告；不能封禁平台账号、不能删除/编辑别人内容。 | https://support.reddithelp.com/hc/en-us/articles/204533859-What-s-a-moderator | Reddit Help | 一手 | 高 | 被移除不等于内容从 Reddit 消失；争议走 modmail。 |
| S16 | 社区规则用于设定成员/访客预期、支撑 enforcement action、提供 report reasons；规则名称和描述应清晰。 | https://support.reddithelp.com/hc/en-us/articles/15484500104212-Rules | Reddit Help / Mod Help | 一手 | 高 | 每个目标 subreddit 建“版规摘要卡”。 |
| S17 | Automoderator 可基于 domain/keyword、specific content、report count、低质/潜在 spam contributors 等做过滤/移除/提醒；不能处理历史内容或 duplicate content。 | https://support.reddithelp.com/hc/en-us/articles/15484574206484-Automoderator | Reddit Help / Mod Help | 一手 | 高 | 不把“发出后看不到”简单归因于人工版主，可能是 automod/filter。 |
| S18 | Crowd Control 可折叠/过滤还不被社区信任的用户的评论/帖子；阈值会涉及 negative community karma、新账号、非成员。 | https://support.reddithelp.com/hc/en-us/articles/15484545006996-Crowd-Control | Reddit Help / Mod Help | 一手 | 高 | 新账号/跨社区发言应默认低触达风险。 |
| S19 | Spam 包括重复/未请求的大规模互动、重复旧内容攒 karma、使用 bot/生成式 AI 造成 spam、link masking、多个账号刷订阅等；商业链接需谨慎或考虑广告。 | https://support.reddithelp.com/hc/en-us/articles/360043504051-Spam | Reddit Help | 一手 | 高 | 人工参与边界：禁止自动群发、重复跨帖、伪装链接、刷量。 |
| S20 | Reddit 公开内容多数无需账号可见，但不包括 private/quarantined、deleted、私信、mod mail、非公开账户信息等。 | https://support.reddithelp.com/hc/en-us/articles/26410290525844-Public-Content-Policy | Reddit Help / Policy | 一手 | 高 | 数据采集边界：只用公开页面，不推断私域或删除内容。 |
| S21 | Data API wiki 要求遵守 Developer Terms / Data API Terms、OAuth、唯一且描述性 User-Agent；非 OAuth/未登录流量可能被 block；删除内容需同步删除，建议 48 小时内例行删除缓存。 | https://support.reddithelp.com/hc/en-us/articles/16160319875092-Reddit-Data-API-Wiki | Reddit Help / Data API | 一手 | 高 | skill 中所有 API 路径必须显式走 OAuth、限速、删除同步。 |
| S22 | 免费 Data API 限制为 100 QPM/OAuth client id，且要读 X-Ratelimit-* headers。 | https://support.reddithelp.com/hc/en-us/articles/16160319875092-Reddit-Data-API-Wiki | Reddit Help / Data API | 一手 | 高 | 调研脚本限流默认值和错误处理。 |
| S23 | Data API Terms 限制 AI 训练、超限研究、商业使用、出售/出租 API access、spam/incentivize/harass；终止后需停止使用并删除缓存/衍生数据。 | https://redditinc.com/policies/data-api-terms | Reddit Inc Policy | 一手 | 高 | Reddit Geo 不做训练集抓取，不绕过 API 限制，不承诺商用数据权。 |
| S24 | Reddiquette 要求读社区规则、投给最适合社区、搜索重复内容、根据内容质量投票，不要因不喜欢而 report。 | https://support.reddithelp.com/hc/en-us/articles/205926439-Reddiquette | Reddit Help | 一手 | 高 | 参与前检查：读规则、查重、选对社区、内容贡献。 |
| S25 | 发帖看不到可能因默认 Hot、违反版规、karma/社区 karma 不足、spam filter；可通过 modmail 联系 mods。 | https://support.reddithelp.com/hc/en-us/articles/360045989712-Why-can-t-I-see-my-post | Reddit Help | 一手 | 高 | 发布后诊断流程。 |
| S26 | Reddit Pro 官方定位为发现客户讨论、追踪关键词/产品/竞品、直接参与对话、提供支持、看 upvote rate/views 等表现。 | https://www.business.reddit.com/pro | Reddit for Business | 一手/商业官方 | 中高 | 品牌参与应先监听、再回复、再评估表现。 |
| S27 | Reddit for Business 建议品牌进入相关社区参与 subreddit conversations、分享有价值内容、提供真实互动与推荐。 | https://www.business.reddit.com/learn/what-is-reddit | Reddit for Business | 一手/商业官方 | 中高 | 人工参与是可行路径，但必须是上下文相关和真实贡献。 |
| S28 | r/findareddit 是公开社区，提供 subreddit directory、How to Find a Sub、相关社区列表等资源。 | https://www.reddit.com/r/findareddit/about/ | Reddit community page | 一手/社区自述 | 中 | 作为补充发现入口，不作为官方全量目录。 |

## 1. Reddit 平台基本机制

Reddit 的基本单位不是账号主页，而是 subreddit。一个 subreddit 是围绕具体主题形成的社区，用户在其中发帖、评论、投票、讨论和建立规范。官方帮助将其定义为 Reddit 内部的小社区，由 redditors 创建并由 redditors 管理。Reddit 社区可为 public、restricted、private、premium-only；public 可见且开放参与，restricted 可见但发帖/评论受控，private 只对批准成员可见。来源：S01，一手，高。

治理上，Reddit 是“双层规则 + 多层执行”：

- 站规：Reddit Rules，适用于全平台，由 admins 执行。
- 社区规则：每个 subreddit 自己的版规，由 mods 执行。
- 版主：志愿者，负责社区风格、规则、移除不合主题内容、ban 社区内违规者、处理用户报告；不是 Reddit 员工，也不能封禁整个平台账号或删除/编辑他人内容。来源：S14/S15，一手，高。

对 Reddit Geo skill 的含义：任何 Reddit 调研都必须以 subreddit 为基本观察单元，而不是以“Reddit 总体用户”泛化。每个社区都要单独记录主题、规则、规模、活跃度、排序样本、参与门槛和审核风险。

## 2. Subreddit 发现方法

### 2.1 官方发现入口

优先使用这些入口交叉发现 subreddit：

1. Reddit 内部搜索：关键词、subreddit 字段、title/selftext/flair/site 过滤。
2. Explore Communities / Communities tab：按 latest global/local trends、相关 favorite communities、featured handpicked communities、topics 发现。
3. r/all / r/popular / trending lists：适合找高曝光、近期热度社区，但会受 discoverability 设置影响。
4. Reddit 推荐：根据已订阅/互动社区、兴趣、位置、社区活跃度、趋势等推荐。
5. Reddit Pro / Trends：对品牌/产品/竞品关键词做 social listening，找 top communities、trending posts/comments。

证据：S02/S03/S04/S26，一手，高到中高。

### 2.2 补充发现入口

可用 `r/findareddit`、`r/ListOfSubreddits`、`r/LocationReddits`、`r/newreddits` 等社区自组织目录作为补充。`r/findareddit/about` 显示它提供主目录、How to Find a Sub、相关社区列表和外部工具。来源：S28，社区自述，一手/社区层，中。

边界：这些是社区维护的启发式入口，不保证完整、最新或无偏。skill 应将它们标为“辅助发现”，不能当成官方目录。

### 2.3 发现偏差

社区是否出现在推荐、r/all/r/popular、trending lists 受社区设置影响。版主可以选择“Show up in high-traffic feeds”和“Get recommended to individual redditors”，也可能因为支持/身份类社区担心骚扰而关闭 discoverability。来源：S03，一手，高。

操作判断：如果某个主题在 Explore / Popular 里不出现，不能判定“Reddit 上没有这个主题”。要用 Reddit Search、Google site、社区目录、相关社区链接继续查。

## 3. 搜索入口与 query 方法

### 3.1 Reddit Search

Reddit 官方搜索支持：

- Comment search：在特定帖子里搜评论。
- Flair search：通过 post flair 找社区内特定子话题。
- Search within communities/custom feeds：在社区页或帖子页限定社区搜索。
- Manual filtering：`author:`、`flair:`、`self:`、`selftext:`、`site:`、`subreddit:`、`title:`、`url:`。
- 多字段组合：如 `subreddit:cats title:"kitten gif"`。
- 布尔运算：`AND`、`OR`、`NOT`，区分大小写；可用括号。
- AI-powered search：用生成式 AI 从真实 posts/comments 中找答案、观点和推荐。

来源：S05，一手，高。

推荐模板：

```text
subreddit:<subreddit> "exact phrase"
title:"best <product/category>" subreddit:<subreddit>
selftext:"pain phrase" subreddit:<subreddit>
flair:<flair> "<query>"
("<brand>" OR "<competitor>") AND (review OR recommend OR alternative)
```

### 3.2 Reddit Search 排序与时间窗

搜索帖子排序：

- Relevance：默认；看词稀缺、帖子年龄、votes/comments。
- Hot：近期获得 upvotes、comments 等互动的帖子。
- Top：upvotes 和 comments 高的帖子，可加时间过滤。
- New：最新帖子，不看互动。
- Comment Count：评论最多。

评论排序：Relevance、Top、New。时间过滤支持 all time、past year、month、week、24 hours、hour。来源：S06，一手，高。

操作判断：同一 query 至少跑 3 个视角：

- `Relevance`：找语义相关和官方默认结果。
- `Top` + month/year/all：找沉淀高价值讨论。
- `New` 或 `Hot`：找当前活跃问题和新信号。

### 3.3 Google `site:reddit.com` 补充检索

Google 官方支持 `site:`、引号、排除词、before/after、filetype 等 operator。`site:` 可限定域名、URL 或 URL prefix，例如 `site:reddit.com/r/parenting "screen time"`。来源：S07/S08，一手，高。

推荐模板：

```text
site:reddit.com/r/<subreddit> "<exact phrase>"
site:reddit.com/r/<subreddit> (<brand> OR <competitor>) review
site:reddit.com/r/<subreddit>/comments "<pain phrase>"
site:reddit.com/r/<subreddit> "<query>" after:2025-01-01 before:2026-06-27
site:reddit.com "<topic>" "reddit" -pinterest -quora
```

边界：Google `site:` 不保证返回所有已索引 URL；没有 query 的 `site:example.com` 不适合判断排名，结果可能相对随机。来源：S08，一手，高。

## 4. 帖子排序与互动信号

Reddit 的可观察互动信号主要包括：

- upvotes/downvotes：影响内容可见性，也影响 karma。
- comments/comment history：用于搜索 relevance、Top、Comment Count、推荐信号。
- post age：影响 relevance、Hot、New、Top 时间窗。
- flair：影响社区内话题组织和搜索。
- community：同一内容在不同 subreddit 的规则、受众和可见性不同。
- account / user activity：订阅、访问、停留、upvote/comment 历史等影响个人推荐。
- location/account age：影响某些推荐和 Best 排序。

证据：S06/S09/S10/S11/S12，一手，高。

Reddit 未公开完整排名算法，所以 skill 只能把这些称为“官方披露信号”，不能承诺“如何操纵算法”。更稳的做法是把帖子评估成四维：

| 维度 | 看什么 | 为什么 |
|---|---|---|
| 相关性 | query 命中、title/selftext、flair、社区主题 | 防止热门但跑题 |
| 活跃度 | comments、recent comments、Hot/New | 找当前仍有参与价值的话题 |
| 共识度 | upvotes、Top time window、评论赞同/反对 | 找沉淀观点和争议结构 |
| 参与风险 | 版规、karma/CQS、新账号、商业链接敏感度 | 防止被移除或被视为 spam |

## 5. 社区规范、版规与审核

### 5.1 规则层

每个 subreddit 的 rules 是参与前的硬门槛。官方 Mod Help 说明，规则用于设定成员/访客预期、支持 enforcement action、提供 report reasons；规则标题、描述、适用对象（posts/comments/chat）都应明确。来源：S16，一手，高。

Reddiquette 对普通用户的参与要求包括：读社区规则、投到最合适的社区、搜索重复内容、根据内容贡献投票，不要因为不喜欢就 report。来源：S24，一手，高。

### 5.2 审核层

常见审核/安全机制：

- Moderator removal：mods 可以移除不合主题或违反社区规则的内容。
- Reports / mod queue：用户报告进入审核队列。
- Automoderator：按 domain/keyword/content/report count/低质或潜在 spam contributor 等条件自动 filter/remove/reply/flair。
- Crowd Control：对新账号、非成员、负社区 karma 等“不被社区信任”的用户折叠或过滤帖子/评论。
- Spam filters / community settings：社区可以调整 spam filter 强度、hold content for review、require post flair 等。
- Admin enforcement：站规层面由 Reddit admins 通过自动检测、人工审查、用户报告、LLM 等执行。

证据：S14/S17/S18/S19，S15 一手，高。

操作判断：发帖/评论未显示时，不要只猜“版主删了”。需要按顺序排查：

1. 是否默认 Hot 排序导致新帖不可见。
2. 是否违反社区规则或格式。
3. 是否 karma/community karma 不足。
4. 是否触发 spam filter / Automoderator / Crowd Control。
5. 是否 Reddit incident。
6. 如怀疑误移除，走 modmail，不直接私信或公开抱怨。

证据：S25，一手，高。

## 6. 账号可信度与参与门槛

### 6.1 Karma

Karma 是账号收到 upvotes/downvotes 后形成的近似反映；upvotes 与 karma 不是 1:1。官方建议不要为了累积 karma 而发言，应成为好贡献者。一些社区会因为防 spam 设置 karma 门槛，新账号或低 karma 用户可能发帖不显示。来源：S12，一手，高。

skill 中应检查：

- account age
- total karma
- post karma / comment karma
- target subreddit community karma
- email verification / account security status（如果用户能提供）
- 目标社区是否有新用户/karma 门槛说明

### 6.2 CQS / 信任层

Contributor Quality Score 是 Reddit 给每个账号分配的分类，用于识别潜在 spammer 或较低正向贡献概率用户。官方披露信号包括：账号过去被采取的 action、network/location signals、账号安全措施（如 email verification）。CQS 分 Highest / High / Moderate / Low / Lowest，mods 可通过 Automod 的 `contributor_quality` 字段使用。来源：S13，一手，高。

边界：CQS 不一定对普通用户公开；skill 不能要求用户“查 CQS”，只能提醒：低 karma、新账号、未验证、频繁跨社区重复发言、商业链接密集，都可能被系统或社区看作低信任。

## 7. API、公开可访问性与数据边界

### 7.1 公开可见不等于无限可用

Reddit Public Content Policy 说明，大多数 Reddit 平台和公开内容无需账号即可查看，公众可见内容包括 public posts、comments、usernames、profiles、karma scores 和相关 metadata。例外包括 private/quarantined 社区、deleted posts/comments、private messages、group chats、mod mail、非公开账号信息、浏览/购买历史等。来源：S20，一手，高。

操作边界：Reddit Geo skill 只能默认处理公开内容；不得试图推断私信、mod mail、private/quarantined 社区内容，也不得保存或复现已删除内容。

### 7.2 Data API 使用边界

官方 Data API Wiki 说明：

- 部分 legacy API docs 可能过时，应以 Developer Terms / Data API Terms 为准。
- Data API 使用需遵守 Responsible Builder Policy、Developer Terms、Data API Terms。
- Clients 必须用注册 OAuth token 认证；Reddit 可 throttle/block unidentified Data API users。
- 应使用唯一、描述性 User-Agent。
- 删除的 posts/comments/account author-identifying info 必须从本地同步删除；官方建议例行 48 小时内删除存储的用户数据和内容。
- 免费 Data API：100 QPM/OAuth client id；读取 `X-Ratelimit-Used`、`X-Ratelimit-Remaining`、`X-Ratelimit-Reset`。
- 非 OAuth 或未登录流量可能被 blocked。

来源：S21/S22，一手，高。

Data API Terms 进一步说明：

- Reddit 授权是 revocable、non-transferable、non-sublicensable。
- 用户内容只能按条款用于 app 展示；未经权利人许可，不得将用户内容用于训练 ML/AI model。
- 商业目的、超过 rate limits 的研究、未被条款明确允许的用途，需要单独协议。
- 不得绕过调用限制、扰乱 API、出售/出租/sublicense API access、用 API spam/incentivize/harass users。
- API 终止后需停止使用并删除缓存/存储内容和 derived data/models。

来源：S23，一手，高。

### 7.3 对 skill 的默认数据策略

默认推荐三档：

| 档位 | 做法 | 适用 |
|---|---|---|
| Manual / UI-first | 人工打开公开页面，记录 URL、标题、时间、社区、互动数据、摘要 | 低频调研、策略判断、人工参与准备 |
| Search-assisted | Reddit Search + Google `site:` query，手动抽样 | 社区发现、问题挖掘、帖子样本池 |
| API-with-compliance | OAuth + unique User-Agent + rate limit + deletion sync + non-commercial/授权边界 | 需要结构化采样且用户确认合规前提 |

禁止默认做：大规模抓取、绕登录/OAuth、保存删除内容、训练模型、商用数据转售、自动发帖/自动私信/自动评论、跨社区重复铺内容。

## 8. 人工参与边界

Reddit for Business 认可品牌在 Reddit 上发现客户讨论、直接参与对话、提供支持、衡量 upvote rate/views 等表现。它强调通过追踪 business/product/competitor 关键词发现 top communities、trending posts/comments，再进入相关讨论。来源：S26/S27，一手/商业官方，中高。

但 Reddit 的反垃圾规则给出了明确边界：

- 不要 repeated / unsolicited mass engagement。
- 不要 mass-post 重复内容、重复旧内容攒 karma。
- 不要用 bots/generative AI tools 制造 spam。
- 不要 link masking / harmful redirects。
- 如果主要贡献是自己受益的商业链接，要谨慎控制频率，或考虑 Reddit Ads。
- 不确定内容是否 spam，先看社区规则或联系 mods。

来源：S19，一手，高。

Reddit Geo skill 的人工参与原则：

1. 先听：先读目标 subreddit 的 Top/Hot/New、wiki、rules、FAQ、常见提问。
2. 再判断：确认是否有明确需求、问题、经验缺口，而不是强行插入品牌/产品。
3. 后发言：评论优先于发帖；回答具体问题优先于发布泛内容；透明披露利益关系。
4. 低频率：同一链接/模板/话术不要跨社区重复使用。
5. 尊重 mods：不绕过移除，不私信骚扰版主，不组织用户冲击其他社区。
6. 不自动化参与：调研可辅助，发帖/评论必须人工审核与人工发送。

## 9. 对 skill 的操作启发

### 9.1 社区发现 workflow

```text
输入：topic / geo / product / competitor / pain phrase
1. Reddit Search：topic + manual filters
2. Explore Communities：topic/local/trending/related
3. Google site：site:reddit.com/r/<candidate> "<query>"
4. r/findareddit / related communities：补全长尾社区
5. Reddit Pro / Trends（如可用）：关键词追踪 top communities/posts/comments
6. 输出 candidate subreddit table
```

候选 subreddit table 字段：

| 字段 | 说明 |
|---|---|
| subreddit | `r/<name>` |
| URL | 社区 URL |
| discovery_source | Search / Explore / Google site / Reddit Pro / related community / r/findareddit |
| community_type | public / restricted / private / premium-only / unknown |
| topic_fit | strong / medium / weak |
| activity_signals | recent posts, comments, Hot/New freshness |
| rule_risk | low / medium / high |
| account_gate | visible karma/age/flair/manual approval requirements |
| evidence_urls | 3-5 个代表帖/规则/FAQ |

### 9.2 帖子采样 workflow

每个目标 subreddit 不用单一排序抽样。默认：

1. `Hot`：当前被社区推上来的讨论。
2. `Top` + week/month/year/all：长期沉淀和高共识讨论。
3. `New`：新问题和未被算法放大的早期信号。
4. `Comment Count`：争议/高讨论度样本。
5. `Search Relevance`：query 相关样本。

输出时给每个帖子记录：URL、title、subreddit、created/relative date、sort path、upvotes/score（如可见）、comments、flair、author visible status、是否 removed/locked/archived、核心观点、反对观点、参与机会。

### 9.3 版规摘要卡

每个社区参与前生成：

```markdown
## r/<subreddit> 版规摘要卡

- 社区主题：
- 官方 rules URL / sidebar / wiki：
- 允许内容：
- 禁止内容：
- 发帖格式：
- flair 要求：
- self-promo / commercial link stance：
- karma / account age / approval gate：
- modmail policy：
- 近期被移除/locked 的高风险模式：
- 参与建议：observe only / comment only / ask mods first / safe to post
```

### 9.4 账号可信度检查

发帖/评论前输出风险评估：

| 风险项 | 低风险 | 高风险 |
|---|---|---|
| 账号年龄 | 老账号 | 新账号 |
| karma | 有目标社区贡献 | 总 karma/社区 karma 低 |
| CQS proxy | email verified、正常历史、低重复 | 未验证、重复跨帖、商业链接密集 |
| 社区关系 | 已订阅/评论过 | 第一次进入就发链接/推广 |
| 内容 | 针对问题、有证据、有经验 | 模板化、泛泛宣传、AI味重 |

### 9.5 人工参与决策树

```text
是否需要发言？
├─ 没有明确问题/需求/错误信息？        → 不发言，只记录洞察
├─ 没读 rules/wiki/FAQ/近期 Top？       → 不发言，先读
├─ 账号不满足门槛或社区反商业？          → 不发言，或 modmail 询问
├─ 内容主要是推广/导流？                → 不发言，考虑 ads 或重写为帮助型回答
├─ 可以具体回答并披露关系？              → 评论优先
└─ 需要开新帖？                         → 查重、选对 flair、写清上下文、人工发布
```

### 9.6 自动化边界

Reddit Geo skill 可以自动化：

- 生成搜索 query。
- 生成候选 subreddit 表。
- 生成帖子采样表。
- 生成版规摘要卡。
- 生成参与草稿和风险清单。
- 做公开页面级别、低频、合规的资料整理。

Reddit Geo skill 不应自动化：

- 自动发帖、自动评论、自动私信。
- 跨 subreddit 批量铺内容。
- 自动创建多个账号或社区。
- 绕过 OAuth/API/rate limit/robots/登录限制。
- 保存删除内容、private/quarantined 内容、mod mail、私信。
- 未授权使用 Reddit 内容训练模型或构造商用数据产品。

## 10. 待核验 / 后续给最终 SKILL.md 的注意点

1. Reddit 的完整排名算法未公开，最终 SKILL.md 只能说“官方披露信号”，不能写“算法规则”。
2. subreddit 规则和 automod 条件会随时变，skill 应要求运行时读取当前规则，而不是写死。
3. Reddit Pro / Trends 是否可用取决于账号权限和地区；最终 skill 应设计无 Pro 的 fallback。
4. API 条款和 rate limits 易变，最终 skill 若提供 API 模式，应强制运行前重查 S21-S23。
5. Google `site:` 只适合作补充发现，不适合估算 Reddit 内容总量或排名。
6. 对“geo”场景，位置推荐和本地趋势可能受登录状态、位置设置、IP、用户历史影响；必须记录采样环境。

## 来源清单

| ID | 来源 | URL | 类型 | 一手/二手 | 可信度 |
|---|---|---|---|---|---|
| S01 | What are communities or subreddits? | https://support.reddithelp.com/hc/en-us/articles/204533569-What-are-communities-or-subreddits | Reddit Help | 一手 | 高 |
| S02 | How do I browse and find communities on the Reddit app? | https://support.reddithelp.com/hc/en-us/articles/17881389378196-How-do-I-browse-and-find-communities-on-the-Reddit-app | Reddit Help | 一手 | 高 |
| S03 | How can I control how people find my community? | https://support.reddithelp.com/hc/en-us/articles/15484078610708-How-can-I-control-how-people-find-my-community | Reddit Help / Mod Help | 一手 | 高 |
| S04 | Reddit's Approach to Content Recommendations | https://support.reddithelp.com/hc/en-us/articles/23511859482388-Reddit-s-Approach-to-Content-Recommendations | Reddit Help | 一手 | 高 |
| S05 | Available search features | https://support.reddithelp.com/hc/en-us/articles/19696541895316-Available-search-features | Reddit Help | 一手 | 高 |
| S06 | What filters and sorts are available? | https://support.reddithelp.com/hc/en-us/articles/19695706914196-What-filters-and-sorts-are-available | Reddit Help | 一手 | 高 |
| S07 | Refine Google searches | https://support.google.com/websearch/answer/2466433?hl=en | Google Search Help | 一手 | 高 |
| S08 | `site:` search operator | https://developers.google.com/search/docs/monitor-debug/search-operators/all-search-site | Google Search Central | 一手 | 高 |
| S09 | Reddit's Approach to Content Recommendations | https://support.reddithelp.com/hc/en-us/articles/23511859482388-Reddit-s-Approach-to-Content-Recommendations | Reddit Help | 一手 | 高 |
| S10 | What are home feed recommendations? | https://support.reddithelp.com/hc/en-us/articles/4402284777364-What-are-home-feed-recommendations | Reddit Help | 一手 | 高 |
| S11 | Why can't I see my post? | https://support.reddithelp.com/hc/en-us/articles/360045989712-Why-can-t-I-see-my-post | Reddit Help | 一手 | 高 |
| S12 | What is karma? | https://support.reddithelp.com/hc/en-us/articles/204511829-What-is-karma | Reddit Help | 一手 | 高 |
| S13 | What is the Contributor Quality Score? | https://support.reddithelp.com/hc/en-us/articles/19023371170196-What-is-the-Contributor-Quality-Score | Reddit Help / Mod Help | 一手 | 高 |
| S14 | Content Moderation, Enforcement, and Appeals | https://support.reddithelp.com/hc/en-us/articles/23511059871252-Content-Moderation-Enforcement-and-Appeals | Reddit Help | 一手 | 高 |
| S15 | What's a moderator? | https://support.reddithelp.com/hc/en-us/articles/204533859-What-s-a-moderator | Reddit Help | 一手 | 高 |
| S16 | Rules | https://support.reddithelp.com/hc/en-us/articles/15484500104212-Rules | Reddit Help / Mod Help | 一手 | 高 |
| S17 | Automoderator | https://support.reddithelp.com/hc/en-us/articles/15484574206484-Automoderator | Reddit Help / Mod Help | 一手 | 高 |
| S18 | Crowd Control | https://support.reddithelp.com/hc/en-us/articles/15484545006996-Crowd-Control | Reddit Help / Mod Help | 一手 | 高 |
| S19 | Spam | https://support.reddithelp.com/hc/en-us/articles/360043504051-Spam | Reddit Help | 一手 | 高 |
| S20 | Public Content Policy | https://support.reddithelp.com/hc/en-us/articles/26410290525844-Public-Content-Policy | Reddit Help / Policy | 一手 | 高 |
| S21 | Reddit Data API Wiki | https://support.reddithelp.com/hc/en-us/articles/16160319875092-Reddit-Data-API-Wiki | Reddit Help / Data API | 一手 | 高 |
| S22 | Developer Platform & Accessing Reddit Data | https://support.reddithelp.com/hc/en-us/articles/14945211791892-Developer-Platform-Accessing-Reddit-Data | Reddit Help / Developer | 一手 | 高 |
| S23 | Data API Terms | https://redditinc.com/policies/data-api-terms | Reddit Inc Policy | 一手 | 高 |
| S24 | Reddiquette | https://support.reddithelp.com/hc/en-us/articles/205926439-Reddiquette | Reddit Help | 一手 | 高 |
| S25 | How do I keep spam out of my community? | https://support.reddithelp.com/hc/en-us/articles/28012014962580-How-do-I-keep-spam-out-of-my-community | Reddit Help / Mod Help | 一手 | 高 |
| S26 | Reddit Pro | https://www.business.reddit.com/pro | Reddit for Business | 一手/商业官方 | 中高 |
| S27 | What is Reddit? | https://www.business.reddit.com/learn/what-is-reddit | Reddit for Business | 一手/商业官方 | 中高 |
| S28 | r/findareddit About | https://www.reddit.com/r/findareddit/about/ | Reddit community page | 一手/社区自述 | 中 |
