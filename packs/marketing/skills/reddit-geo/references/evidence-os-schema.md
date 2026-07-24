# Reddit Evidence OS Schema

Use these fields when the task requires a research database, not just a short answer.

## Communities

| field | meaning |
|---|---|
| subreddit | `r/<name>` |
| url | Community URL |
| discovery_source | Reddit Search / Explore / Google site / Reddit Pro / related community / r/findareddit |
| topic_scope | What the community is for |
| audience | Buyers, users, practitioners, hobbyists, critics |
| community_type | public / restricted / private / unknown |
| activity_signal | recent posts, comment depth, active threads |
| rule_risk | low / medium / high |
| account_gate | karma, age, flair, approval, link limits |
| relevance_reason | why this community matters |

## Queries

| field | meaning |
|---|---|
| query | Exact Reddit/Google/AI prompt |
| platform | Reddit / Google / ChatGPT / Perplexity / Reddit AI search |
| intent | Informational / Comparison / Review / Buying Intent / Troubleshooting / Alternative |
| user_question | The actual question behind the keyword |
| matched_threads | Thread URLs |
| evidence | Source, date, sample boundary |

## Threads

| field | meaning |
|---|---|
| thread_title | Title |
| thread_url | URL |
| subreddit | Community |
| thread_type | question / review / comparison / complaint / guide / warning / AMA |
| observed_at | Date observed |
| sort_path | Hot / Top week / Top year / New / Comment Count / Search Relevance |
| engagement_signal | comments, visible score/upvotes, freshness |
| moderation_status | live / removed / locked / archived / folded / unknown |
| why_it_matters | Pain, competitor, content pattern, AI-citation candidate |

## Comments And Mentions

| field | meaning |
|---|---|
| short_quote | Short excerpt only when useful |
| url | Comment/thread URL |
| speaker_type | buyer / user / expert / critic / brand / unknown |
| sentiment | positive / neutral / negative / mixed |
| pain_or_job | What progress the user wants |
| current_alternative | What they do instead |
| brand_or_competitor | Mentioned entity |
| context | recommended / rejected / compared / complained / explained |
| caveat | bias, joke, stale thread, low confidence |

## Opportunities

Each opportunity must include:

- Evidence:
- Target user:
- Current alternative:
- Why now:
- Counter-evidence:
- Action lane: `listen` / `transparent_engage` / `paid_amplify`
- Next test:
