# AI Answer Baseline

Use this when measuring Reddit visibility in AI/search answers.

## Prompt Groups

- `best <category> for <use case>`
- `<brand> vs <competitor> for <job>`
- `is <brand/product> worth it`
- `<brand/product> problems`
- `<category> alternatives to <competitor>`
- `what do Reddit users think about <brand/category>`
- same prompts without the word `Reddit`

## Surfaces

Measure each surface separately:

- Google AI Overviews
- Google AI Mode
- Gemini
- ChatGPT with search
- Perplexity
- Reddit AI search / Reddit Answers

## Capture Schema

| field | meaning |
|---|---|
| date | snapshot date |
| locale | country/language/device if available |
| platform | AI/search surface |
| prompt | exact prompt |
| answer_present | yes/no |
| brand_mentioned | yes/no |
| sentiment | positive / neutral / negative / mixed |
| reddit_cited | yes/no |
| reddit_url | cited URL |
| subreddit | cited community |
| competitors | entities mentioned |
| co_cited_domains | other sources |
| screenshot_or_export | evidence path |
