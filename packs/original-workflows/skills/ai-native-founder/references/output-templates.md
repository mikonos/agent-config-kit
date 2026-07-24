# Output Templates

Use these formats when the user asks for a concrete founder artifact.

## Quick Diagnosis

```markdown
**判断**
[Continue / narrow / pivot / pause / build test surface / launch / systematize]

**阶段**
[Idea / MVP / Launch / Scale / Cross-stage]

**范围**
[完整阶段闸门审计 / 只审 ops / 只审 moat / 只审 PMF / etc.]

**卡点**
[plain-language bottleneck]

**链条**
| Field | Value |
|---|---|
| Outcome | [or unknown] |
| Customer opportunity | [or unknown] |
| Proposed solution | [or unknown] |
| Riskiest assumption | [or unknown] |
| Test | [or unknown] |

**证据**
| Signal | Strength | Source | Decision impact |
|---|---|---|---|
|  | Strong / Medium / Low | user story / behavior / revenue / retention / AI synthesis / demo / etc. | supports / contradicts / missing |

**下一步**
[one action that can change the decision]

**敏感边界**
[privacy/security/professional review required, or "not applicable"]

**闸门**
继续条件：
停止/转向条件：
```

## Stage-Gate Memo

```markdown
# [Project] Stage-Gate Memo

## Stage
[current stage + why]

## Outcome
[measurable outcome or learning outcome]

## Opportunity
[customer problem / need / desire, from evidence]

## Solution
[current solution or test surface]

## Riskiest Assumption
[one assumption that can kill the project]

## Evidence Ledger
| Evidence | Supports / contradicts | Strength | Source | Decision impact |
|---|---|---|---|---|

## Sensitive-Domain Check
- Data/privacy/security:
- Professional review:
- User exposure limit:

## Decision
[continue / narrow / pivot / pause / launch / scale]

## Gate
Continue if:
Stop or pivot if:
Review date:
```

## Feedback-to-Opportunity Ledger

Use this when the user brings feature requests, customer feedback, support messages, sales objections, or "users asked for X". Do not turn raw requests directly into roadmap items.

```markdown
| Raw request / feedback | Evidence type | Customer opportunity | Outcome served | Assumption | Test | Decision |
|---|---|---|---|---|---|---|
|  | user story / support ticket / sales objection / opinion / AI synthesis |  |  |  |  | build / test / park / reject |
```

Decision rules:

- `build` only when the request maps to a repeated opportunity and a current stage gate.
- `test` when the opportunity is plausible but the assumption is still risky.
- `park` when the request is real but outside the current stage.
- `reject` when it is solution noise, isolated preference, or conflicts with the current gate.

## Assumption Test

```markdown
| Field | Content |
|---|---|
| Assumption | If [user] in [situation] has [problem], they will [behavior]. |
| Type | Value / Usability / Feasibility / Viability / Security-Trust / Operability |
| Why risky |  |
| Test |  |
| Sample |  |
| Pass standard |  |
| Fail standard |  |
| Next decision | Continue / narrow / pivot / stop |
```

## Founder Attention Audit

```markdown
| Workflow | Current owner | Frequency | Judgment complexity | Risk | Exit path | Escalation rule | Done standard |
|---|---|---:|---|---|---|---|---|
```

After the table, classify the next move:

- Automate now:
- Delegate now:
- Keep with founder:
- Requires escalation policy:

## Project Charter

```markdown
# [Project] AI-Native Charter

## Problem

## Target User

## Current Stage And Gate

## Riskiest Assumption

## What Not To Build Yet

## Architecture Principles

## Data / Privacy / Security Boundaries

## Human Review Points

## Test And Launch Requirements

## Key Decisions
| Date | Decision | Why | Revisit when |
|---|---|---|---|
```
