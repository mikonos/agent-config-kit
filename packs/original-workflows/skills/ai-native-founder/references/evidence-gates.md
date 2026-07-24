# Evidence Gates

Use this file when applying `ai-native-founder` to a real startup question.

## Sources

- Official blog: https://claude.com/blog/the-founders-playbook
- Official PDF copy: `05_每日记录/2026/07/20260704/founder-skill-creation/source/The-Founders-Playbook-05062026_v3.pdf`
- Extracted PDF text: `05_每日记录/2026/07/20260704/founder-skill-creation/source/The-Founders-Playbook-05062026_v3.txt`
- PDF deep-reading: `[[20260515_00_Anthropic_AI_Native创业手册_结构笔记]]`
- AI-native organization article deep-reading: `[[20260704_00_AI原生组织红宝书_结构笔记]]`
- Useful method notes: `[[20260515_方法_AI原生创业四阶段证据闸门]]`, `[[20260515_方法_AI原生创业假设测试矩阵]]`, `[[20260515_方法_创始人注意力退出系统]]`, `[[20260704_方法_AI原生组织流程砍除与验证重排SOP]]`

## Evidence Hierarchy

| Strength | Counts as evidence | Does not count by itself |
|---|---|---|
| High | repeated past user stories, active use, paid use, retention, referral, procurement/security acceptance, support tickets, churn reasons | founder conviction |
| Medium | prototype sessions with target users, concierge delivery, landing-page conversion with qualified intent, competitor review patterns | raw traffic or likes |
| Low | AI market synthesis, investor/friend excitement, user opinions about future use, synthetic personas, polished demo | permission to scale |

## Claude Surface Router

Use this when a user asks "which AI tool/workflow should do this?" If Claude is not the actual tool stack, map the same responsibilities to the closest local tool.

| Task | Anthropic surface | Local abstraction | Boundary |
|---|---|---|---|
| Quick question, rewrite, brainstorm, adversarial prompt | Claude Chat | fast thinking partner | Does not become organizational memory by itself. |
| Research, analysis, finished docs, recurring ops, file/system synthesis | Claude Cowork | knowledge/ops layer with files, connectors, scheduled runs | Needs source data and human review. |
| Writing, testing, shipping software | Claude Code | code execution layer with repo access, diffs, tests, dev environment | Requires architecture context, tests, and security review. |

## Stage Gates

| Stage | Core question | Exit condition | Main failure mode | Required founder output |
|---|---|---|---|---|
| Idea | Is this worth building? | Qualitative evidence that a real, specific group has a real, frequent problem and that the proposed solution addresses the revealed problem. | Building replaces validating; AI confirms the founder's belief. | Testable problem hypothesis, target profile, interview evidence, disconfirming evidence, one core interaction to test. |
| MVP | What exactly should we build first? | Evidence that identifiable users return, pay, or refer because the product solves a real problem. | False PMF, scope creep, security gaps, agentic technical debt. | Narrow MVP scope, architecture/context file, assumption matrix, retention/revenue/referral benchmarks, security review threshold. |
| Launch | Can growth and operations repeat without the founder holding every thread? | Repeatable acquisition plus product, support, infrastructure, security, and operating cadence that can handle real users. | Founder bottleneck, technical debt coming due, fragile support, hidden compliance risk. | Founder attention exit map, weekly metrics brief, triage cadence, launch OS, debt/security hardening list. |
| Scale | Can the company remain trustworthy and defensible as founder involvement drops? | Systems are reliable, governance and procurement trust are credible, and advantage survives copycats. | Founder judgment stays undocumented; workflow trust and moat are shallow. | Moat audit, enterprise/trust packet, governance controls, escalation policy, system ownership map. |

## Cross-Stage Lenses

### Teresa Torres Lens

Always map `outcome -> opportunity -> solution -> assumption -> test`. If the user starts with a solution, move backward to outcome and customer opportunity before deciding.

### Drucker Lens

Ask whether activity is producing results. In Launch and Scale, the key result is not founder busyness; it is a system that turns judgment into repeatable contribution.

### Munger Lens

Invert the question. Ask how the founder could fool themselves:

- AI makes a bad idea look researched.
- A demo makes an unvalidated problem feel real.
- Early traffic hides retention failure.
- Adding features hides lack of one painful use case.
- Founder heroics hide missing operations.

### Karpathy Lens

Treat the company as a harness: context, tools, policy, evals, logs, review. Any AI-native workflow without evals and human review boundaries is just faster generation.

## Risk Patterns And Antidotes

| Pattern | Symptom | Antidote |
|---|---|---|
| Mistaking building for validating | "We can ship it tonight" becomes proof the idea is good. | Run five target-user sessions around the core interaction; log support and contradiction. |
| Premature scaling | AI builds many workflows before problem-solution fit. | Freeze build except evidence-producing actions until the Idea gate passes. |
| Loss of objectivity | AI returns a beautiful case for the founder's prior belief. | Ask for disconfirming evidence, failed analogs, and strongest competitor argument. |
| Agentic technical debt | Each coding session re-derives scope, architecture, and tradeoffs. | Write a project charter / context file before production work. |
| False PMF | Launch spike, friends, investors, or one channel look like demand. | Measure retention, paid behavior, referral, and week-6/week-12 durability. |
| Zero-friction scope creep | Every extra feature feels cheap. | Keep only features tied to the riskiest current assumption. |
| Insecure by inexperience | Working code handles real user data without security review. | Define minimum security/privacy review before real user exposure. |
| Founder bottleneck | Every support, sales, roadmap, and exception decision routes through founder. | Audit founder attention and move repeatable work to AI/person/process with escalation rules. |
| Undefined "good" | The product works but quality cannot be judged consistently. | Define evaluation rubrics, examples, non-examples, and human review owners. |

## Project Charter Minimum

For an AI-built product, the charter should contain:

- Problem and target user.
- Current stage and stage gate.
- Current riskiest assumption.
- What not to build yet.
- Architecture principles and dependencies to avoid.
- Data, privacy, and security boundaries.
- Human review points.
- Test and launch requirements.
- Key historical decisions and why they were made.

## Sensitive-Domain Minimum

Trigger this for legal, medical, financial, child/family, security, privacy, enterprise data, or other high-consequence contexts:

- Use redacted or synthetic-safe samples until data handling is approved.
- Define who may see raw data and where it is stored.
- Add professional review before advice, diagnosis, legal interpretation, compliance commitment, or customer-facing claims.
- Add security/privacy review before real user data touches the product.
- Make the test objective learning, not production use, until the gate passes.

## Founder Attention Exit Map

Classify founder work:

| Class | Action |
|---|---|
| Fully automatable | reports, CRM hygiene, reminders, doc sync, routine summaries |
| Delegable but needs a person | standard support, demo prep, routine ops |
| Needs founder judgment | positioning, key account tradeoffs, fundraising story, major architecture/market bets |
| Needs escalation | security event, legal/compliance exception, key customer risk, data exposure |

Start by exiting high-frequency low-risk work. Never exit work without an exception path.
