# Research Agent 5: Risks, Boundaries, Metrics, and Timeline

Date: 2026-06-27

Scope: execution risks, ethics boundaries, automation/API limits, measurement design, and 2024-2026 timeline for Reddit Geo.

Source strategy: official Reddit policy/help/investor pages first, Google/OpenAI official sources second, industry research only for measurement context. No Zhihu, WeChat public accounts, Baidu Baike, or Baidu Zhidao were used.

## 0. Executive Summary

Reddit Geo is only defensible when it treats Reddit as a public community evidence layer, not as a controllable posting surface. The safe path is: listen first, map communities and questions, engage transparently when a human can add value, use paid Reddit products for promotion, and measure AI-search visibility separately from Reddit engagement.

The hard boundary is simple: do not automate spam, hide commercial interest, manipulate votes, evade bans, mass-create accounts, scrape around API limits, or preserve deleted/private/sensitive data. These are not style preferences; they are platform, legal, and brand-safety constraints.

## 1. Source Ledger

| ID | Source | URL | Date / updated | Type | Primary / secondary | Confidence | Use |
|---|---|---|---|---|---|---|---|
| R01 | Reddit Rules | https://redditinc.com/policies/reddit-rules | current page checked 2026-06-27 | Reddit policy | Primary | High | Authentic participation, community rules, no spam/content manipulation. |
| R02 | Spam | https://support.reddithelp.com/hc/en-us/articles/360043504051-Spam | checked 2026-06-27 | Reddit Help | Primary | High | Repetitive unsolicited activity, link masking, AI/bot spam. |
| R03 | Disrupting Communities | https://support.reddithelp.com/hc/en-us/articles/360043066412-Disrupting-Communities | updated 2026-05 | Reddit Help | Primary | High | Vote manipulation, ban evasion, detection signals. |
| R04 | Responsible Builder Policy | https://support.reddithelp.com/hc/en-us/articles/42728983564564-Responsible-Builder-Policy | updated 2026-06 | Reddit Help | Primary | High | App registration, automated activity, commercial approval. |
| R05 | Data API Terms | https://redditinc.com/policies/data-api-terms | checked 2026-06-27 | Reddit policy | Primary | High | API restrictions, commercial use, rate limits, AI training limits. |
| R06 | Reddit Data API Wiki | https://support.reddithelp.com/hc/en-us/articles/16160319875092-Reddit-Data-API-Wiki | updated 2026-05-11 | Reddit Help | Primary | High | OAuth, user-agent, throttling, deleted content retention. |
| R07 | Public Content Policy | https://support.reddithelp.com/hc/en-us/articles/26410290525844-Public-Content-Policy | updated 2025-05-29 | Reddit Help | Primary | High | Public vs private/deleted content, licensing, prohibited data uses. |
| R08 | OpenAI and Reddit Partnership | https://openai.com/index/openai-and-reddit-partnership/ | 2024-05-16 | OpenAI official | Primary | High | OpenAI Data API partnership and ChatGPT/new products. |
| R09 | Google and Reddit Partnership | https://redditinc.com/news/reddit-and-google-expand-partnership | 2024-02-22 | Reddit official | Primary | High | Google Data API partnership. |
| R10 | Reddit AI Search | https://support.reddithelp.com/hc/en-us/articles/32026729424916-Reddit-s-AI-search | updated 2026-05-26 | Reddit Help | Primary | High | Reddit AI search citations and limitations. |
| R11 | Reddit Community Intelligence at Cannes 2026 | https://redditinc.com/news/live-from-cannes-2026-real-conversations-are-driving-the-new-consumer-decision-journey | 2026-06 | Reddit official | Primary / commercial | Medium-high | Reddit strategic direction for community intelligence. |
| R12 | Google AI features and query fan-out | https://developers.google.com/search/docs/appearance/ai-features | checked 2026-06-27 | Google official | Primary | High | AI search source discovery and measurement boundaries. |
| R13 | Semrush most-cited domains in AI | https://www.semrush.com/blog/most-cited-domains-ai/ | 2025-11-10 | Industry research | Tool-data primary, interpretation secondary | Medium-high | Citation volatility and platform differences. |
| R14 | Profound AI platform citation patterns | https://www.tryprofound.com/blog/ai-platform-citation-patterns | updated 2025-08 | Industry research | Tool-data primary, interpretation secondary | Medium-high | Reddit citation share by AI platform. |
| R15 | Ahrefs AI Overview growth | https://ahrefs.com/blog/ai-overview-growth/ | 2025-05-13 | Industry research | Tool-data primary, interpretation secondary | Medium-high | Reddit growth in AI Overview citation market share. |

## 2. Red Lines

These are hard stops for the final skill.

1. Do not spam Reddit.
   - Evidence: Reddit Rules require authentic participation and prohibit spam or disruptive behavior. Reddit Spam guidance treats repeated or unsolicited mass engagement, link masking, and bot/AI-generated spam as spam risks.
   - Sources: R01, R02.

2. Do not manipulate votes, karma, comments, subscribers, or visibility signals.
   - Evidence: Reddit's Disrupting Communities policy covers vote manipulation and ban evasion, and Reddit uses moderator/user reports plus internal systems to detect violations.
   - Source: R03.

3. Do not hide brand, employee, contractor, affiliate, or paid relationships.
   - Evidence: Reddit requires authentic participation; FTC endorsement and fake-review rules, reviewed in Agent 4, make undisclosed incentives and fake testimonials a legal risk.
   - Sources: R01 plus Agent 4 FTC sources.

4. Do not use multi-account or proxy workflows to simulate organic consensus.
   - Evidence: vote manipulation, ban evasion, subscriber fraud, and disruptive behavior are prohibited. Low-trust account signals can be filtered by community and platform systems.
   - Sources: R03, Agent 2 CQS/Crowd Control evidence.

5. Do not bypass API, scraping, or rate-limit rules.
   - Evidence: Reddit Data API requires approved/registered access, OAuth, accurate user-agent, and compliance with Data API Terms; commercial or out-of-scope use needs explicit approval or separate agreement.
   - Sources: R04, R05, R06.

6. Do not store or reuse deleted, private, quarantined, modmail, private-message, or sensitive-profile data.
   - Evidence: Public Content Policy distinguishes public content from private and deleted content; Data API Wiki requires deletion of locally stored deleted content and recommends routine deletion of stored user data/content within 48 hours.
   - Sources: R06, R07.

7. Do not train models or create derived datasets from Reddit user content unless the rights and Reddit terms explicitly allow it.
   - Evidence: Data API Terms restrict using user content to train ML/AI models without required permissions and separate approval where needed.
   - Source: R05.

8. Do not promise guaranteed GEO outcomes.
   - Evidence: AI citations are volatile across platform, date, vertical, and prompt. Semrush and Profound show Reddit can be highly visible, but Semrush also shows large swings.
   - Sources: R13, R14.

## 3. Gray Zones

These require cautious handling, not automatic approval.

| Zone | Why risky | Safe default |
|---|---|---|
| Brand account answering user questions | Useful support can look like marketing if context is wrong. | Use a clearly identified account; answer only relevant questions; disclose affiliation; minimize links. |
| Employee participation | Employees may have real expertise but also undisclosed interest. | Require disclosure if discussing employer/product/category where the employer benefits. |
| Agency-managed organic participation | High risk of astroturfing and KPI pressure. | Use official/declared accounts or paid ads; avoid fake-user posts. |
| Monitoring public threads | Legitimate research can become invasive profiling if data is stored or segmented by sensitive attributes. | Store only minimal excerpts and URLs; avoid sensitive profiling; remove deleted data. |
| AI-assisted draft replies | Helpful for clarity but can become automated spam or generic low-value content. | Human review, community-specific context, no mass posting, no duplicated comments. |
| Reddit Ads amplifying positive conversations | Platform-supported but can look exploitative if detached from community context. | Use Reddit ad products transparently; do not manufacture the underlying conversation. |
| AI-search visibility tracking | Useful but prompt results are stochastic and localized. | Use prompt batches, repeated snapshots, locale/device/date logging, and avoid ranking-position overinterpretation. |

## 4. Validation Metrics

### 4.1 Community Fit Metrics

| Metric | Definition | Interpretation |
|---|---|---|
| subreddit_relevance | Topic overlap between community scope and product/category use case. | High relevance beats large subscriber count. |
| rule_fit | Whether rules permit the intended observation, comment, support, AMA, or ad path. | Rule mismatch is a stop sign for organic participation. |
| activity_health | Recent posts/comments, comment depth, moderator activity, repeated questions. | Choose active communities with current discussion, not abandoned high-subscriber shells. |
| trust_threshold | Karma/account-age/community-karma/link restrictions and visible mod warnings. | New or low-trust accounts should observe and answer cautiously. |
| pain_density | Count and quality of high-intent questions, complaints, alternatives, comparisons. | This is a demand signal, not a population statistic. |

### 4.2 Mention Quality Metrics

| Metric | Definition | Good signal | Bad signal |
|---|---|---|---|
| mention_context | Why a brand/product appears. | Specific use case, comparison, constraint. | Generic praise, link drop, repeated phrasing. |
| speaker_credibility | Whether the commenter appears to have relevant experience. | Detailed setup, tradeoffs, follow-up answers. | Empty endorsement, suspicious account pattern. |
| sentiment_shape | Positive/negative/mixed and why. | Balanced pros/cons and failure modes. | One-sided promotional language. |
| competitor_set | Brands/products compared together. | Reveals category framing. | Random unrelated comparisons. |
| objection_clarity | What stops purchase/adoption. | Actionable risks: price, durability, support, setup, trust. | Vague dislike without context. |

### 4.3 Thread Longevity Metrics

| Metric | Definition |
|---|---|
| evergreen_question | The thread answers a recurring question, not only a one-day news event. |
| search_index_presence | Thread appears in Reddit search and/or Google `site:reddit.com` for target queries. |
| late_comment_activity | New comments continue after the initial burst. |
| AI_citation_candidate | Thread has clear question, specific answers, contrasting views, and stable URL. |
| risk_of_deletion | Low if rule-compliant, non-spammy, non-sensitive, and not deceptive. |

### 4.4 AI Answer Capture Metrics

Track each platform separately:

- Google AI Overviews
- Google AI Mode
- Gemini
- ChatGPT with search
- Perplexity
- Reddit AI search / Reddit Answers

Minimum capture fields:

| Field | Meaning |
|---|---|
| date | Snapshot date. |
| locale | Country/language/device if available. |
| platform | AI/search surface. |
| prompt | Exact prompt/query. |
| answer_present | Whether an AI answer appeared. |
| brand_mentioned | Whether target brand/entity appears in answer. |
| sentiment | Positive/neutral/negative/mixed. |
| reddit_cited | Whether a Reddit URL appears as source/citation. |
| subreddit | Which community is cited or summarized. |
| thread_url | Evidence URL. |
| co_cited_domains | Other domains used in the same answer. |
| screenshot_or_export | Local evidence path if captured. |

Interpretation rule: one screenshot is weak evidence. Use baseline, repeated runs, and before/after comparison.

## 5. Timeline: 2024-2026

| Date | Event | Source | Meaning for Reddit Geo |
|---|---|---|---|
| 2024-02-22 | Reddit and Google announced expanded partnership and Google access to Reddit Data API. | R09 | Reddit content became an explicitly licensed, structured input for Google products; do not reduce Reddit visibility to ordinary crawling. |
| 2024-05-09 / 2025-05-29 | Reddit published/updated Public Content Policy explaining public content access, licensing, and prohibited data uses. | R07 | Public content is visible, but commercial data use, sensitive profiling, and misuse are bounded. |
| 2024-05-16 | OpenAI and Reddit announced partnership; OpenAI gets Reddit Data API access for ChatGPT and new products. | R08 | Reddit content can appear in ChatGPT/new OpenAI product experiences, but exact citation behavior is not guaranteed. |
| 2024-12-09 | Reddit introduced Reddit Answers. | Agent 3 / Reddit official | Reddit itself started turning posts/comments into AI answer surfaces. |
| 2025-03 to 2025-05 | Ahrefs observed Reddit's AI Overview citation market share rise strongly after Google's March Core Update. | R15 | Reddit became a major AI Overview visibility domain in observed US keyword sets. |
| 2025-07 to 2025-10 | Semrush observed high Reddit citation volatility in ChatGPT and platform-specific differences. | R13 | Reddit Geo must use repeated measurement, not one-off prompt evidence. |
| 2025 | Reddit litigation and public disputes around Anthropic / Perplexity / SerpApi / Oxylabs signaled stronger enforcement against unauthorized large-scale data access. | Reddit public court filings / industry reporting | Treat as enforcement signal and party claims, not final court findings; it strengthens the default rule to use authorized API/licensing paths. |
| 2026-05-11 | Reddit Data API Wiki updated; legacy docs may be out of date, OAuth and terms are emphasized. | R06 | Always re-check current API terms before any automated collection. |
| 2026-05-26 | Reddit Help says AI search is available across platforms and languages, with inline citations to posts/comments. | R10 | Reddit AI search should be a first-class measurement surface. |
| 2026-06 | Reddit promoted Community Intelligence tools at Cannes Lions 2026, emphasizing 25B+ posts/comments as business insight. | R11 | Reddit is commercially positioning community conversation as decision intelligence; brands should still avoid manipulating organic signals. |

## 6. Operating Implications for the Skill

1. Default mode is research, not posting.
   - Build `communities -> queries -> threads -> comments -> mentions -> opportunities -> monitoring` before suggesting engagement.

2. Split actions into three lanes:
   - `listen`: observe public conversations, extract questions, pain, alternatives, and mention context.
   - `transparent_engage`: named human or brand account answers relevant questions with disclosure and value.
   - `paid_amplify`: use Reddit Ads/Reddit Pro for promotion, retargeting, or commercial campaigns.

3. Refuse these requests:
   - "Seed fake organic mentions."
   - "Create accounts to upvote/comment."
   - "Make it look like users are recommending us."
   - "Scrape all Reddit posts for training/commercial data without approval."
   - "Bypass API limits or deleted-content requirements."

4. Require current-source refresh when:
   - User asks about API access, automation, scraping, ads policy, or platform rules.
   - User asks for latest Reddit/Google/OpenAI partnership status.
   - User asks for current AI citation shares or platform ranking.

5. Treat AI-search visibility as a measurement problem:
   - Build prompt corpus.
   - Run baseline.
   - Log platform/date/locale.
   - Track Reddit citation hit, brand entity hit, sentiment, co-citations.
   - Re-run after any campaign or content intervention.

5.1. Add moderation survivability as a risk metric:
   - Whether a post/comment remains live.
   - Whether it is removed, locked, folded, filtered by Crowd Control, or held for review.
   - Whether the account receives mod warnings, subreddit bans, or platform enforcement.
   - Whether the content survives long enough to be indexed or cited.

6. Treat Reddit user quotes carefully:
   - Quote only short excerpts when needed.
   - Preserve URL and context.
   - Do not reproduce long Reddit threads.
   - Do not store deleted/private/sensitive content.

7. Keep honest boundaries visible:
   - Reddit samples are self-selected.
   - Upvotes are not market share.
   - AI answers are stochastic.
   - GEO effects are correlation until measured with a before/after design.
