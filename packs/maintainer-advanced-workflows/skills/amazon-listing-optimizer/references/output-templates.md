# Output Templates

Use the smallest template that satisfies the mode. A quick audit does not need a full release packet; a publish-ready migration does.

## Table of contents

1. Run header
2. Gap/conflict report
3. Question-claim-field map
4. Candidate fields
5. Lint report
6. Change/review packet
7. Experiment card

## 1. Run header

```markdown
# Amazon Listing Optimization Packet

- State: NEEDS_INPUT | BLOCKED_RISK | DRAFT_UNVERIFIED | READY_FOR_HUMAN_REVIEW
- Mode: AUDIT | BUILD | MIGRATE | DIAGNOSE | EXPERIMENT | AI_SHOPPING
- Marketplace / locale:
- Product type / ASIN / variation:
- Policy status / checked_at / source:
- Baseline window:
- Assumptions:
- Non-goals:
```

## 2. Gap/conflict report

| id | missing/conflicting fact | affected claim/field | risk | evidence needed | owner | state |
|---|---|---|---|---|---|---|

Follow with `Safe work possible now` and `Blocked work` lists.

## 3. Question-claim-field map

| question_id | real shopper question | source | claim_id | grade | field | answer or explicit gap |
|---|---|---|---|---|---|---|

Competitor/review signals may occupy `source`; they cannot create the product answer.

## 4. Candidate fields

```markdown
## Candidate: identity-first

### Title — __ / __ chars
[text] 〔CL-001, CL-002〕

### Item Highlights — __ / __ chars
[text] 〔CL-003〕

### Bullets
1. [text] 〔CL-...〕

### Product Details gaps
- [attribute]: [value needed / conflict]

### Image/A+ evidence plan
- Asset 1: question → claim → visual proof → prohibited implication

### Backend terms
[only residual relevant synonyms; no hidden claims]
```

Provide no more than three variants. Explain the single meaningful difference between them.

## 5. Lint report

| check_id | check | measured | verdict | evidence/next action |
|---|---|---|---|---|
| L-01 | policy freshness and field lengths | | PASS/BLOCK/WARN | |
| L-02 | claim IDs and variant scope | | PASS/BLOCK | |
| L-03 | evidence grade/status | | PASS/BLOCK | |
| L-04 | forbidden/prohibited/competitor wording | | PASS/BLOCK | |
| L-05 | duplicate claim/field responsibility | | PASS/WARN | |
| L-06 | priority question coverage | | PASS/BLOCK | |
| L-07 | human approval slots | | PENDING/PASS | |
| L-08 | inference/experiment integrity | | PASS/BLOCK/WARN | |

Always show actual character counts and exact hits. “Checked” is not evidence.

## 6. Change/review packet

```markdown
## Change packet

- Before snapshot:
- After candidate:
- Primary changed field:
- Other fields intentionally frozen:
- Canary ASIN/variation:
- Submission owner:
- Review Listings Changes owner/check cadence:
- Desktop/mobile/search/PDP checks:
- Rollback value and trigger:
- Product approval: [status / approver / approved_at / evidence_ref]
- Compliance approval: [status / approver / approved_at / evidence_ref]
- Operations approval: [status / approver / approved_at / evidence_ref]
```

Only a structured record with `status: approved`, a human identifier, and a timezone-aware timestamp can pass review lint. `pending`, a name alone, or model-generated approval remains incomplete.

If several fields are changing, label the run `package_optimization`, not component learning.

## 7. Experiment card

```markdown
## Experiment card

- Observed problem:
- Competing explanations:
- Hypothesis:
- Objective: component_learning | package_optimization | monitoring
- Design: MYE_randomized | randomized | observational | none
- MYE/tool eligibility:
- Primary change:
- Frozen variables:
- Primary metric:
- Guardrails: conversion, return, CX Health, policy/customer harm
- Minimum sample / stopping rule:
- Observation window:
- Confounder log:
- Rollback rule:
- Inference allowed: randomized | correlational | observational | inconclusive
- Result:
- What enters the next question/claim backlog:
```

Never fill a result before the experiment. Never translate an Alexa answer screenshot into a rank or causal metric.
