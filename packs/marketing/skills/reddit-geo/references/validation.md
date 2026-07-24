# Reddit Geo Skill Validation

Status: PASS as of 2026-06-27.

This file records validation after `SKILL.md` exists.

Required checks:

- Structure check: PASS. Frontmatter, trigger conditions, workflow, research dimensions, mental models, heuristics, risk boundaries, source appendix, templates, and mandatory checkpoints are present.
- Nuwa check: PASS. `quality_check.py` returned 6/6 PASS: 5 mental models, limitations, expression DNA, honest boundaries, core tensions, primary-source section.
- Industry OS check: PASS. The skill uses database-first workflow, sample boundaries, sources, communities, queries, threads, comments, mentions, opportunities, and monitoring loop.
- Reddit safety check: PASS. The skill refuses spam, hidden affiliation, vote manipulation, ban evasion, mass-account behavior, unauthorized scraping, deleted/private/sensitive data storage, and unsupported AI-training/data use.
- GEO check: PASS. The skill distinguishes citation hit, entity hit, evidence hit, quick scan, full baseline, platform-specific measurement, and speculative claims.
- Routing check: PASS for this skill. `quick_validate.py` confirms required prompt triggers, file triggers, description routing, and `resources.primary`.
- Cursor config global check: PARTIAL. `.cursor/skill-rules.json` is valid JSON and contains the `reddit-geo` route. `tools/validate_cursor_config.py` still reports unrelated pre-existing registry drift: several old unregistered skill folders and one registered route without folder (`md2wechat-skill`). No `reddit-geo` issue was reported.

Verification commands:

```bash
rtk python3 .cursor/skills/reddit-geo/scripts/quality_check.py .cursor/skills/reddit-geo/SKILL.md
rtk python3 .cursor/skills/skill-creator/scripts/quick_validate.py .cursor/skills/reddit-geo
rtk python3 -m json.tool .cursor/skill-rules.json >/tmp/reddit_geo_skill_rules_check.json
rtk rg -n '"reddit-geo"|Reddit Geo|resources|primary' .cursor/skill-rules.json .cursor/skills/reddit-geo/SKILL.md
rtk rg -n "fake organic|multiple accounts|hidden affiliation|vote manipulation|Scrape Reddit commercially|Store deleted|Promise guaranteed" .cursor/skills/reddit-geo/SKILL.md
rtk rg --files .cursor/skills/reddit-geo | rtk sort
```

## Forward-test matrix

| Prompt | Expected artifact | Must verify |
|---|---|---|
| "帮我看看某 SaaS 要不要去 r/SaaS 发帖" | Engagement Audit | subreddit rules, disclosure, moderation survivability, action lane |
| "研究 Reddit 上大家怎么抱怨 <category>" | Quick Scan | communities, queries, thread samples, sample boundary, counter-evidence |
| "我们在 ChatGPT/Perplexity 里有没有 Reddit 引用机会" | AI Answer Baseline | prompt corpus, platform-specific table, citation/entity/evidence hit distinction |

Raw outputs should be linked here after each forward-test run.

## Dual-review optimization check

After Nuwa-style and skill-creator-style subagent review on 2026-06-27:

- `SKILL.md` reduced from 620 lines to 497 lines via progressive disclosure.
- Added `Scenario Router`, `Gray-Zone Gate`, and `Current-Fact Freshness Rules`.
- Moved detailed schemas/templates into:
  - `references/evidence-os-schema.md`
  - `references/ai-answer-baseline.md`
  - `references/output-templates.md`
  - `references/sources/README.md`
- Re-ran `quality_check.py`, `quick_validate.py`, and JSON parse check successfully.
