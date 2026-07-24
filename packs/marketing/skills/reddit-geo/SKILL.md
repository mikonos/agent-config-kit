---
name: reddit-geo
description: Reddit community evidence and AI-search visibility workflow. Use when researching subreddits, mining Reddit VOC or complaints, auditing Reddit participation risk, mapping competitor/alternative mentions, planning Reddit Ads/Reddit Pro, or measuring Reddit citations in Google AI Overview, ChatGPT, Perplexity, Gemini, or Reddit Answers.
metadata:
  routing:
    requirePromptTriggers: true
    requireFileTriggers: true
    requireDescriptionRouting: true
---

# Reddit Geo · Community Evidence Operating System

> Reddit Geo is evidence engineering, not stealth seeding.

## What This Skill Does

Use this skill to turn Reddit into a measurable evidence layer for search and AI-answer visibility:

- Find relevant subreddits, threads, comments, queries, and recurring user questions.
- Map brand, competitor, alternative, objection, and use-case mentions.
- Measure Reddit visibility across Google AI Overviews, AI Mode, Gemini, ChatGPT search, Perplexity, and Reddit AI search.
- Decide whether the right action is `listen`, `transparent_engage`, or `paid_amplify`.
- Refuse spam, astroturfing, hidden-interest posting, vote manipulation, API abuse, and fake "organic" campaigns.

Do not use this skill to mass-post, create fake users, manufacture consensus, scrape around Reddit terms, or guarantee AI-search citations.

When triggered, execute before explaining theory. First classify the request, state assumptions, then produce the smallest applicable artifact: Quick Scan, Engagement Audit, AI Answer Baseline, or Monitoring Plan. Ask clarifying questions only when the missing boundary blocks action; otherwise run a small-sample pass and label it preliminary.

## Expert Lens

Default lens:

- Michael Porter: industry structure, substitutes, profit pools, platform dependency.
- Andrej Karpathy: agentic workflow, small verified loops, measurable execution.
- Clayton Christensen + Bob Moesta: JTBD, current alternatives, switching moments.
- Teresa Torres: opportunity tree, evidence strength, experiment sequencing.
- Elinor Ostrom: community governance, local rules, shared-resource abuse.
- Rand Fishkin / Danny Sullivan: search visibility as evidence, not superstition.

When a domain is high-risk or specialized, add a domain expert and verify current official sources before using Reddit evidence.

## Core Mental Models

### Model 1: Community Before Channel

Reddit is not one traffic channel. It is a federation of subreddits with local rules, moderators, norms, trust thresholds, and anti-spam systems.

Use this when:

- Choosing target subreddits.
- Deciding whether to comment, post, ask moderators, or only observe.
- Explaining why a tactic from one subreddit may fail elsewhere.

Evidence:

- Reddit Help defines subreddits as separate communities with public/restricted/private variants.
- Community discovery and recommendation are dynamic and personalized.
- Failed AMA and astroturfing cases show the cost of treating Reddit as broadcast media.

Limit:

- Some relevant communities are not appropriate for brand participation. The correct recommendation may be "listen only."

### Model 2: Evidence Density Beats Mention Volume

Useful Reddit Geo assets contain a concrete user question, context, tradeoffs, alternatives, objections, and follow-up discussion. Raw brand repetition is weak evidence and often a spam signal.

Use this when:

- Evaluating whether a thread can support AI-answer visibility.
- Designing content or replies.
- Auditing "brand mention" campaigns.

Evidence:

- The industry-research OS framework starts with structured evidence databases, not reports.
- Google AI features can use query fan-out across related subquestions and support sources.
- High-intent question threads are more durable than brand broadcasts.

Limit:

- Evidence density can improve citation or entity accuracy probability. It does not guarantee citation, ranking, or conversion.

### Model 3: Listen, Transparent Engage, Paid Amplify

Every Reddit action must be assigned to one lane:

| Lane | Purpose | Allowed actions | Stop sign |
|---|---|---|---|
| `listen` | Understand communities and evidence | Public research, query mapping, thread sampling, pain clustering | Storing deleted/private/sensitive data |
| `transparent_engage` | Help in context | Clearly identified human/brand answer, support, AMA, correction, disclosure | Hidden affiliation, repeated links, off-topic promotion |
| `paid_amplify` | Scale commercial reach | Reddit Ads, Reddit Pro, retargeting, free-form ads | Using ads to launder fake organic claims |

Limit:

- Paid amplification does not make a deceptive organic strategy acceptable.

### Model 4: GEO Is Measurement, Not Magic

AI-search visibility is stochastic and platform-specific. One prompt screenshot is weak evidence. Measure baseline, repeated snapshots, citations, entity mentions, sentiment, co-cited domains, and moderation survivability.

Use this when:

- A user asks whether Reddit helps ChatGPT, Google AI Overviews, Perplexity, or Reddit AI search.
- Designing experiments.
- Interpreting AI answer screenshots.

Evidence:

- Industry datasets show Reddit can be a high-frequency AI citation domain.
- The same datasets show large variation by platform, time, vertical, and prompt.
- Reddit AI search is itself an answer surface with inline Reddit citations.

Limit:

- Use "observed correlation" unless before/after evidence is strong.

### Model 5: Public Does Not Mean Free-To-Use

Public Reddit content can be visible without login, but API access, commercial use, storage, deletion handling, automation, and AI training are bounded by Reddit terms and law.

Use this when:

- The user asks for scraping, automation, API workflows, data products, or training data.
- The task involves commercial monitoring.
- The task touches sensitive categories or user data.

Evidence:

- Reddit Data API requires OAuth, unique user-agent, rate-limit handling, deletion sync, and policy compliance.
- Reddit Public Content Policy distinguishes public content from private/deleted content and restricts misuse.
- Reddit Responsible Builder Policy restricts automated activity and commercial data use.

Limit:

- This skill is not legal advice. Re-check current official terms for automation, API, commercial, or regulated work.

## Decision Heuristics

1. If you have not mapped subreddits and rules, do not recommend posting.
2. If a conclusion depends on current Reddit/Google/OpenAI/API policy, re-check official sources first.
3. If a thread is popular but weak in user intent, treat it as visibility, not demand.
4. If the plan only works when affiliation is hidden, reject it.
5. If a brand can add specific help, comment before creating a new post.
6. If a response needs scale, use paid amplification instead of repeated organic posting.
7. If the target is AI-search visibility, build a prompt corpus before taking action.
8. If evidence comes from Reddit, label it as sample signal, not population truth.
9. If the category is medical, legal, financial, education, policy, or safety-sensitive, use Reddit only as user voice and verify facts elsewhere.
10. If a community says no self-promotion, the organic action is listening or asking moderators, not clever wording.
11. If content cannot survive moderation without disguise, it is not a viable Reddit Geo asset.

## Operating Workflow

### Step 0: Classify The Request

| Request type | Action |
|---|---|
| Subreddit discovery / demand mining | Run Reddit Evidence OS |
| GEO/AEO/AI-search visibility | Run AI Answer Baseline + Reddit Evidence OS |
| Organic Reddit participation | Run Community Fit + Redline Audit before drafting |
| Reddit Ads / paid amplification | Separate paid plan from organic evidence |
| Scraping / automation / API | Re-check current Reddit official terms first |
| Fake organic seeding / vote manipulation / hidden affiliation | Refuse and redirect |

If the task asks for "latest", "current", API terms, platform rules, partnerships, citation shares, or active policies, browse current official sources before answering.

### Step 1: Define Boundary

Collect or infer:

- Brand/product/category:
- Market/locale/language:
- Use cases:
- Competitors and substitutes:
- Target user:
- Risk level: normal / regulated / sensitive / legal-risk
- Output: quick scan / research database / opportunity map / engagement plan / measurement report
- Time box:

If missing details do not block a first pass, start with a small-sample OS and label assumptions.

If the user gives an incomplete brief, do not stall. Run a default quick scan with explicit assumptions:

- 3-5 candidate subreddits.
- 5-10 exact queries or prompts.
- 5-8 high-signal threads.
- At least 3 competitor/substitute mentions if available.
- One recommended lane per opportunity.

Ask follow-up questions only when the missing information changes safety, legality, market, or language scope.

### Step 1.5: Scenario Router

Classify the business context before choosing an action lane:

| Scenario | Best Reddit use | High-risk move | Default lane |
|---|---|---|---|
| B2B | Expert answers, AMA, technical use-case explanation | Sales DM, demo-link drop | `listen` -> `transparent_engage` |
| SaaS | Troubleshooting, alternatives, changelog/support answers | Fake "anyone used X?" posts | `listen` -> `transparent_engage` |
| DTC | Purchase doubts, sizing/quality/use-case clarification | Fake reviews, affiliate spam | `listen` or `paid_amplify` |
| Local service | Public pricing, licensing, checklist, neighborhood education | Fake neighbor recommendation | `listen` or `paid_amplify` |
| Regulated / YMYL | User language and objections only | Advice or claims from Reddit evidence | `listen` + external verification |

### Step 2: Build Reddit Evidence OS

Create tables before conclusions.

Minimum tables:

- Communities.
- Queries.
- Threads.
- Comments and mentions.
- Opportunities.

For field schemas, read `references/evidence-os-schema.md`. For a quick scan, keep fields compact but always include source URL, observed date, sample boundary, relevance reason, counter-evidence, and action lane.

### Step 3: Community Fit And Moderation Survivability

Before recommending engagement, generate this card:

```markdown
## r/<subreddit> Fit Card

- Topic fit:
- Audience:
- Rules URL/sidebar/wiki:
- Allows brand participation? yes/no/unclear
- Self-promotion/link stance:
- Account gates:
- Recent high-signal threads:
- Common removal/lock patterns:
- Moderation survivability: high / medium / low
- Safe lane: listen / comment only / ask mods first / paid only / no-go
- Reason:
```

Moderation survivability checks:

- Will the content remain live without disguise?
- Is it likely to be removed, locked, folded, filtered by Crowd Control, or held for review?
- Could the account receive mod warnings, subreddit bans, or platform enforcement?
- Can the content survive long enough to be indexed or cited?

### Step 4: AI Answer Baseline

For full GEO/AEO measurement, build 30-50 prompts before taking action. For quick scans or time-boxed first passes, build 6-10 seed prompts across the main prompt groups, label findings as preliminary, and recommend a full baseline before campaign decisions.

Measure each AI/search surface separately. Capture exact prompt, date, locale, answer presence, brand mention, sentiment, Reddit citation URL, subreddit, competitors, co-cited domains, and screenshot/export path.

Interpretation:

- `citation hit`: answer cites Reddit URL.
- `entity hit`: answer mentions brand/product without Reddit citation.
- `evidence hit`: answer claim aligns with Reddit evidence even if final citation is elsewhere.

For prompt groups and capture schema, read `references/ai-answer-baseline.md`.

### Research File Routing

When deeper context is needed, read only the relevant research file:

| Need | Read |
|---|---|
| Evidence OS field schema and research database fields | `references/evidence-os-schema.md` |
| AI answer prompt groups and baseline capture schema | `references/ai-answer-baseline.md` |
| Industry OS fields and article lineage | `references/research/01-article-framework.md` |
| Reddit mechanics, search, karma, moderation, API basics | `references/research/02-reddit-mechanics.md` |
| GEO/AEO, AI citations, Google/OpenAI/Reddit AI evidence | `references/research/03-geo-ai-search.md` |
| Cases, anti-patterns, B2B/DTC/SaaS/local-service differences | `references/research/04-cases-antipatterns.md` |
| Redlines, metrics, timeline, automation/API/data-use risk | `references/research/05-risks-timeline.md` |
| Synthesized models and tensions | `references/research/06-synthesis-framework.md` |

### Step 5: Choose Action Lane

#### Listen

Use when:

- Community rules are restrictive.
- Evidence is still weak.
- The category is sensitive.
- The brand has no credible account or human expert ready.

Output:

- subreddit map
- question clusters
- pain/JTBD map
- competitor mention map
- AI-answer baseline
- monitoring plan

#### Transparent Engage

Use when:

- A real user question exists.
- The answer is specific, useful, and rule-compliant.
- The account can disclose affiliation clearly.
- The content can admit limits and alternatives.

Rules:

- Comment before posting.
- Help before linking.
- Disclose relationship.
- Answer the question first.
- Mention limitations and alternatives.
- Do not duplicate the same content across communities.
- Do not ask for upvotes or coordinate support.

Draft format:

```markdown
Disclosure: I work on / represent <brand>, so take this with that context.

Direct answer:

Useful context:

When not to choose us / this approach:

Alternative options:

Link only if allowed and necessary:
```

#### Paid Amplify

Use when:

- The objective is scale, retargeting, conversion, or paid testing.
- Organic rules or trust thresholds make brand participation inappropriate.
- The team wants commercial reach.

Keep separate:

- Paid creative can be Reddit-native.
- Paid comments need support/moderation readiness.
- Paid results must not be presented as natural community consensus.

### Step 6: Monitor And Re-test

Minimum cadence:

- 2-3 day baseline before intervention.
- 2-6 week retest after content/support/paid action.
- Weekly monitoring for high-risk or active campaigns.

Track:

- Reddit-in-SERP count.
- AI citation hits.
- Brand entity hits.
- Sentiment and co-cited competitors.
- High-signal thread count.
- Official reply survivability.
- Removed/locked/folded/warned content.
- Brand search/direct/referral/support deflection if available.

## Mandatory Checkpoints

Before final output, mark each checkpoint as `pass / fail / unknown`:

- Boundary defined or assumptions stated.
- Subreddit rules checked before engagement advice.
- Evidence table created before conclusions.
- Redlines checked.
- Current official sources rechecked when policy/API/legal/current claims matter.
- Action lane selected: `listen` / `transparent_engage` / `paid_amplify`.
- Validation plan included.

If any safety, legality, affiliation, or scraping checkpoint is `fail`, refuse or redirect before giving execution tactics.

## Gray-Zone Gate

Before approving any Reddit action, classify gray zones:

| Zone | Default |
|---|---|
| Brand or employee answer | Allow only with clear disclosure and subreddit fit |
| Agency-managed organic | Treat as high risk; prefer declared account or paid |
| AI-assisted draft | Require human review; no mass posting or duplicated replies |
| Public monitoring | Store minimal URL + short excerpt; no sensitive profiling |
| Ads amplifying conversations | Keep paid separate from organic; never present as natural consensus |

Stop immediately and switch to review if:

- A moderator removes or warns on the content.
- The strategy needs multiple accounts to look credible.
- A relationship cannot be disclosed cleanly.
- The community forbids brand participation or self-promotion.
- The plan fails the Rampart test, Trap Plan test, FTC test, or subreddit-rule test.

## Redlines: Refuse These Requests

Refuse and redirect if the user asks to:

- Create fake organic mentions.
- Use multiple accounts to ask/answer/upvote.
- Make employees or contractors look like normal users.
- Hide sponsorship, employment, affiliate, or agency relationships.
- Mass-comment, mass-DM, or cross-post substantially similar content.
- Buy upvotes, comments, accounts, karma, or subscribers.
- Evade bans, removals, mod rules, Crowd Control, or API limits.
- Scrape Reddit commercially or at scale without authorization.
- Store deleted/private/quarantined/sensitive content.
- Use Reddit user content to train models without required rights and approvals.
- Promise guaranteed AI Overview / ChatGPT / Perplexity citation.

Safer redirect:

- Run listening research.
- Use transparent brand account.
- Ask moderators.
- Use Reddit Ads.
- Build owned FAQ/help pages.
- Measure AI visibility with a prompt corpus.

## 表达DNA / Output DNA

When using this skill, output should be:

- Evidence-first: tables, URLs, dates, sample boundaries.
- Human-readable: explain Reddit mechanics in plain language.
- Community-aware: no generic "post on Reddit" advice.
- Skeptical of growth hacks: name the redline if a tactic relies on disguise.
- Measurable: every GEO claim gets a metric or a test.
- Honest: state what Reddit evidence cannot prove.
- 句式: short conclusion first, then tables and decision gates.
- 词汇: use `evidence`, `sample boundary`, `subreddit fit`, `moderation survivability`, `citation hit`, `entity hit`, `transparent_engage`.
- 语气: calm, skeptical, plain-spoken; never hype Reddit as a guaranteed shortcut.
- 节奏: boundary -> evidence scan -> risk gate -> action lane -> validation.
- 确定性: use strong language for policy redlines, cautious language for GEO outcomes.
- 引用: cite URLs, dates, and source type for important claims.

Avoid "Reddit hack" framing, guaranteed citation promises, treating upvotes as market share, treating one subreddit as all of Reddit, and treating one AI answer screenshot as proof.

## 核心张力

1. **张力：真实性 vs 可规模化**：Reddit 奖励真实参与，但增长团队天然想复制流程。处理方式是规模化研究、证据采集和测量，不规模化伪装发言。
2. **张力：公开可见 vs 数据权利**：Reddit 公共页面可以被看见，但不等于可以无限采集、商用、训练或保存删除内容。处理方式是 UI-first/低频摘要优先，API/商业/自动化任务先核验当前条款。
3. **张力：AI 可见性 vs 不稳定性**：Reddit 可能进入 AI answer，但平台、prompt、时间、地区都会改变结果。处理方式是 baseline、重复采样、平台分表，而不是截图崇拜。
4. **张力：品牌帮助 vs 社区信任**：品牌方确实能补充事实和售后，但也最容易破坏社区信任。处理方式是披露身份、回答具体问题、承认边界、避免链接优先。

## Output Templates

Use the smallest artifact that answers the request:

| Need | Output | Details |
|---|---|---|
| First pass / incomplete brief | Quick Scan | See `references/output-templates.md` |
| Proposed post, comment, AMA, or brand response | Engagement Audit | Check subreddit rules, disclosure, survivability, and redlines first |
| Ongoing visibility tracking | Monitoring Plan | Track prompts, Reddit-in-SERP, AI citation/entity hits, and moderation outcomes |

Read `references/output-templates.md` only when the user asks for a structured deliverable or when the shape of the artifact is unclear.

## 诚实边界 / Honest Boundaries

- Reddit samples are self-selected and do not represent market share.
- Upvotes, comments, and karma are not demand statistics.
- AI-answer behavior changes by platform, date, locale, prompt wording, and user context.
- Google, OpenAI, Reddit, and other platform policies change; current policy tasks require live verification.
- Reddit can reveal user language, objections, alternatives, and evidence gaps; it cannot replace interviews, analytics, paid tests, or official market data.
- This skill is not legal advice. Regulated categories, commercial data use, scraping, automation, endorsements, and privacy-sensitive work need current source checks and possibly counsel.
- Public Reddit content should be quoted sparingly, with source URLs and context. Do not reproduce long threads or store deleted/private/sensitive data.

## Current-Fact Freshness Rules

When citing platform rules, API terms, ads policy, AI-search behavior, partnerships, or citation-share data:

- Re-check official sources live if the claim affects legality, policy, automation, API use, or current platform behavior.
- Do not quote AI citation percentages unless the source, date, platform, sample, and method are stated.
- Label source confidence: `official / tool-data / media-report / vendor-claim / anecdote`.
- Treat vendor AI-visibility studies as directional evidence, not universal truth.
- If no current source is checked, write `current status: unknown` and recommend verification before action.

## Research Sources

Research details are in `references/research/`.

Key source groups:

- Article framework: the cited WeChat article on building an industry research OS and the installed `industry-research-os` Skill.
- Reddit mechanics: Reddit Help, Reddit Rules, Data API Terms, Public Content Policy, Responsible Builder Policy, Reddit Pro.
- GEO / AI search: Reddit-Google partnership, OpenAI-Reddit partnership, Google AI features docs, Reddit AI Search, Semrush, Ahrefs, Profound, Search Engine Land.
- Cases and anti-patterns: Reddit for Business cases, Reddit policy, FTC endorsement/fake-review guidance, Trap Plan / War Robots astroturfing coverage, Rampart AMA failure.
- Risk timeline: 2024 Google/OpenAI partnerships, 2025-2026 API/policy updates, AI citation volatility, and data-access litigation signals.

Primary source URLs and industry research URLs live in `references/sources/README.md`. Re-check current official sources before policy, API, legal, automation, or active AI-search claims.

---

> This skill was generated with Nuwa-style distillation and adapted as a reusable topic/framework Skill.
> Original method lineage: [女娲 · Skill造人术](https://github.com/alchaincyf/nuwa-skill)
> Creator attribution: [花叔](https://x.com/AlchainHust)
