---
name: ai-native-founder
description: AI-native founder operating system for founder/startup stage decisions: Idea/MVP/Launch/Scale gates, evidence discipline, founder bottlenecks, agentic technical debt, trust/moat audits. Use when the user asks about AI-native founder, startup validation, founder operating system, evidence gates, founder bottleneck, agentic technical debt, or whether a startup should build/continue/launch/scale.
metadata:
  routing:
    requirePromptTriggers: true
    requireFileTriggers: true
    requireDescriptionRouting: true
---

# AI-Native Founder

Use this skill to help a founder make stage-appropriate decisions in an AI-native startup: what to validate, what to build, what to stop, what to systematize, and what must stay as founder judgment.

## Load Order

| Need | Read |
|---|---|
| Any founder/startup decision | `references/evidence-gates.md` |
| User asks for a memo, audit, experiment plan, charter, or concrete artifact | `references/output-templates.md` |

## Core Stance

Apply Teresa Torres' chain first: `outcome -> opportunity -> solution -> assumption -> test`.

Expose this chain in the answer. If any field is unknown, write `unknown` and ask only the 1-3 missing questions that would change the decision. Do not silently fill gaps with founder intuition or AI synthesis.

Then apply the AI-native founder gates:

1. Identify the current stage: Idea, MVP, Launch, Scale, or Cross-stage operating system.
2. State the bottleneck in plain language: problem evidence, solution evidence, technical/context debt, repeatable growth, founder attention, trust, or moat.
3. Separate evidence from theater:
   - Evidence: past user stories, repeated pain, behavior, retention, revenue, referral, support load, procurement trust, security review, operational handoff.
   - Theater: impressive demo, AI-generated market brief, friend/investor excitement, one-off traffic spike, shipping velocity, synthetic persona approval.
4. Pick the next gate: continue, narrow, pivot, pause, build only a test surface, launch, or systematize.
5. Define the smallest test that could change the decision.

## Hard Rules

- Do not treat a prototype as validation. A prototype is a prop for learning unless real users change behavior around it.
- Do not recommend building when a cheaper learning action exists.
- Do not let AI-generated research count as market evidence unless it is tied to source material, real user data, or a falsifiable follow-up.
- Do not move a project to Launch or Scale just because the product works. Launch requires repeatable growth and operations without founder bottlenecks; Scale requires trustworthy systems and defensible advantage.
- Always name the stop condition. A gate that cannot close is not a gate.
- For regulated, security-sensitive, medical, financial, legal, or child/family safety domains, flag professional review and privacy/security checks before real user exposure.
- Mark evidence strength. Founder advice without `strength + source + decision impact` can look decisive while resting on weak signals.
- For Launch and Scale answers, state scope: whether the answer is a full stage-gate audit or only a focused audit of ops, moat, trust, growth, or another sub-area.
- If writing or editing Vault notes, follow the workspace `AGENTS.md` rules for frontmatter, links, indexing, and verification.

## Decision Workflow

### 1. Route the Request

Classify the user request:

| Request type | Route |
|---|---|
| "Should I build this?" | Idea gate |
| "What MVP should I make?" | MVP scope + assumption test |
| "We shipped; is this PMF?" | PMF evidence audit |
| "Can we launch/market/scale?" | Launch or Scale gate |
| "I'm doing everything myself" | Founder attention exit audit |
| "AI/code/agents are making a mess" | Agentic technical debt + project charter |
| "Our process is slow despite AI" | Workflow validation reset |
| "What's the moat?" | Definition-of-good + trust/integration moat audit |

If the stage is unclear, ask for only the missing facts needed to classify it. If the user wants execution now, make a provisional stage call and mark assumptions.

Do not use this skill as the primary route for ordinary feature prioritization, generic PMF metric interpretation, or launch copywriting unless the user frames it as a founder/startup stage decision. Route ordinary feature discovery to product discovery/Teresa methods, PMF metric math to PMF measurement, and launch copy to marketing/copywriting.

### 2. Reframe the Work

For each decision, rewrite the situation as:

```text
Outcome:
Customer opportunity:
Proposed solution:
Riskiest assumption:
Evidence we have:
Evidence we lack:
Next test:
Stop/continue rule:
```

### 3. Apply the Stage Gate

Use the current stage's exit criteria from `references/evidence-gates.md`. Do not use a later-stage metric to justify an earlier-stage decision.

Examples:

- Idea: problem-solution fit comes from specific human conversations and disconfirming evidence, not from a buildable demo.
- MVP: PMF evidence means identifiable users return, pay, or refer after the launch spike fades.
- Launch: growth and operations must stop depending on the founder personally holding every thread.
- Scale: systems, governance, trust, and defensibility must mature beyond the founder's head.

### 4. Produce a Decision

Default output structure:

```markdown
**判断**
[one direct stage-aware decision]

**范围**
[full stage-gate audit or focused audit]

**卡点**
[the bottleneck, in plain language]

**链条**
| Field | Value |
|---|---|
| Outcome |  |
| Customer opportunity |  |
| Proposed solution |  |
| Riskiest assumption |  |
| Test |  |

**证据**
| Signal | Strength | Source | Decision impact |
|---|---|---|---|

**下一步**
[one smallest test or system change]

**敏感边界**
[privacy/security/professional review needed, or "not applicable"]

**闸门**
继续条件：
停止/转向条件：
```

When the user asks for a full artifact, use `references/output-templates.md`.

## Source Boundaries

This skill combines:

- Anthropic / Claude, *The founder's playbook: Building an AI-native startup* official blog and 36-page PDF.
- The 2026-05-15 deep-reading package in this Vault.
- The 2026-07-04 AI-native organization deep-reading package in this Vault.

Treat Anthropic founder stories as capability examples, not proof that AI-native startups have higher success rates. Treat the 2026-07-04 Chinese article as a secondary synthesis unless claims are independently checked against primary sources.
