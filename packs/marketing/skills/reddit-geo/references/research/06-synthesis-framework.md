# Phase 2 Synthesis: Reddit Geo Framework

Date: 2026-06-27

This file converts research files `01-article-framework.md` through `05-risks-timeline.md` into the operating model used by the final `SKILL.md`.

## 1. Core Definition

Reddit Geo is a research and execution framework for improving AI-search and search-answer visibility through authentic Reddit evidence. It does not mean mass posting, fake mentions, or "ranking manipulation." It means building a measurable evidence layer from public Reddit communities: communities, queries, threads, comments, brand/competitor mentions, objections, and AI-answer citations.

## 2. Mental Models

### Model 1: Community Before Channel

Reddit is a federation of subreddits with local rules, moderators, norms, and trust thresholds. A tactic that works in one subreddit can be spam in another. Therefore the unit of analysis is not "Reddit traffic"; it is a specific community with specific rules and repeated questions.

Evidence:

- Agent 2: Reddit Help defines subreddits as communities created and managed by redditors, with public/restricted/private variants.
- Agent 2: community discovery and recommendation are personalized and dynamic.
- Agent 4: failed AMA and astroturfing cases show what happens when teams treat Reddit as a broadcast channel.

Limit:

- Some communities are too small, private, restricted, hostile to brands, or off-topic. The correct action can be "do not participate."

### Model 2: Evidence Density Beats Mention Volume

AI answers and search results reward useful, retrievable evidence more than raw brand-name repetition. Useful Reddit evidence contains a concrete user question, context, tradeoffs, alternatives, objections, and follow-up discussion.

Evidence:

- Agent 1: industry OS article requires small sample evidence and database fields before conclusions.
- Agent 3: Google query fan-out means one user question expands into related subquestions and support sources.
- Agent 4: high-intent question threads outperform brand broadcasts.

Limit:

- Evidence density can improve the probability of being cited or correctly described, but it cannot guarantee citation, ranking, or conversion.

### Model 3: Listen, Transparent Engage, Paid Amplify

Reddit Geo has three lanes. `listen` maps demand and evidence without speaking. `transparent engage` lets an identified human or brand account answer relevant questions. `paid amplify` uses Reddit Ads or Pro surfaces for promotion. Mixing these lanes creates ethical and platform risk.

Evidence:

- Agent 4: effective cases use expert AMA, support, retargeting, and Reddit-native paid products; failures hide intent.
- Agent 5: red lines reject fake organic mentions, hidden affiliations, vote manipulation, and stealth seeding.
- Agent 2: Reddit for Business supports discovering conversations and participating, but Reddit spam rules limit repeated unsolicited promotion.

Limit:

- Transparent engagement still depends on subreddit rules. Paid amplification does not cleanse a deceptive organic strategy.

### Model 4: GEO Is Measurement, Not Magic

Reddit's GEO value must be measured across platforms and time. A screenshot from one prompt is weak. A defensible result tracks baseline, repeated prompt batches, citation hits, entity hits, sentiment, co-cited domains, and Reddit-in-SERP visibility.

Evidence:

- Agent 3: Profound, Ahrefs, Semrush, and Search Engine Land samples show Reddit is often highly cited, but citations vary by platform, date, vertical, and prompt.
- Agent 5: AI answer capture requires platform/date/locale/prompt logging.
- Agent 3: Google AI Overviews, AI Mode, Gemini, ChatGPT, Perplexity, and Reddit AI search must be measured separately.

Limit:

- AI answers are stochastic and product behavior changes quickly. Use "correlated with" unless before/after evidence is strong.

### Model 5: Public Does Not Mean Free-To-Use

Public Reddit content may be visible without login, but API, commercial use, storage, deletion handling, AI training, and automated activity are bounded by Reddit terms and laws.

Evidence:

- Agent 2: Data API requires OAuth, user-agent, rate limits, deletion sync, and compliance with Data API Terms.
- Agent 5: Responsible Builder Policy and Public Content Policy impose commercial approval, app transparency, and retention boundaries.
- Agent 4: FTC endorsement and fake-review rules create additional disclosure constraints.

Limit:

- This skill is not legal advice. If a task involves commercial scraping, regulated categories, sensitive data, or automation, current official terms must be rechecked and counsel may be needed.

## 3. Decision Heuristics

1. If you have not mapped subreddits and rules, do not recommend posting.
2. If the answer relies on current platform policy, re-check official sources first.
3. If a thread has high engagement but weak user intent, treat it as visibility, not demand.
4. If a plan only works when affiliation is hidden, reject it.
5. If a brand can add specific help, comment before creating a new post.
6. If a response needs scale, use paid amplification instead of repeated organic posts.
7. If the target is AI-search visibility, build a prompt corpus before taking action.
8. If evidence comes from Reddit, label it as sample signal, not population truth.
9. If a category is medical, legal, financial, education, policy, or safety-sensitive, use Reddit only as user voice and verify facts elsewhere.
10. If a community says no self-promotion, the organic action is listening or asking moderators, not clever wording.
11. If content cannot survive moderation without disguise, it is not a viable Reddit Geo asset.

## 4. Operating Protocol

1. Boundary: define brand/product/category, market, use cases, competitors, and risk level.
2. Evidence scan: build communities, queries, threads, comments, mentions, and content-pattern tables.
3. Community fit: score relevance, rules, activity, trust threshold, and pain density.
4. GEO baseline: run prompt corpus across AI/search surfaces and capture citations, entities, sentiment, and co-citations.
5. Moderation survivability: check whether candidate actions can remain live without removal, folding, Crowd Control filtering, mod warning, or ban.
6. Opportunity map: identify missing evidence, competitor dominance, unresolved objections, content gaps, and no-go communities.
7. Action lane: choose `listen`, `transparent_engage`, or `paid_amplify`.
8. Validation: rerun measurement after 2-6 weeks and compare baseline.

## 5. Core Tensions

1. Reddit rewards authenticity, while GEO teams want repeatable systems.
   - Resolution: systematize research and measurement, not fake participation.

2. Reddit is public, while Reddit data is not unconstrained.
   - Resolution: use public URLs and short excerpts for insight; use API and commercial data only under current terms.

3. AI-search citations can be valuable, while citation behavior is unstable.
   - Resolution: track repeated snapshots, not single screenshots.

4. Brands can help users, while brand participation can degrade trust.
   - Resolution: disclose, answer concrete questions, admit limits, and avoid link-first behavior.

## 6. Final Skill Construction Notes

The final skill should:

- Trigger on Reddit GEO, AEO, AI-search visibility, subreddit research, Reddit marketing, and Reddit demand mining.
- Start with a factual refresh when the task depends on current policies, platform partnerships, API access, or citation share.
- Use industry-research OS fields, not generic report prose.
- Refuse stealth, spam, multi-account, vote manipulation, hidden-interest, and unauthorized scraping/training requests.
- Output practical tables and decision gates.
- Preserve the Nuwa standard: mental models, heuristics, protocol, boundaries, source appendix, validation.
