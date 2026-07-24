---
name: product-evidence-loop
description: product / 515 demand-and-evidence loop for product-organization work. Use this whenever the user mentions product, 515, Family Hub, Prepare, Pre-flight, Aha, responsibility card, product idea, roadmap, PRD, requirement, bug, meeting conclusion, competitor signal, or asks whether something should enter the product. This skill turns inputs into an evidence packet, applies source/risk/acceptance/owner gates, and returns go / defer / kill / needs evidence before any PRD or roadmap edit.
---

# product Evidence Loop

This skill operationalizes the `515 需求与证据 loop`: every product product idea, requirement, meeting conclusion, bug, competitor signal, or AI/social signal must pass through evidence, risk, acceptance, and ownership gates before it becomes product truth.

Use Drucker's question first: **what contribution does this decision make to the current product outcome?** Use Deming's loop second: **what evidence will change the next cycle?**

## Load Order

| Need | Read |
|---|---|
| Any product / 515 evidence-loop task | `references/sop.md` |
| Producing a demand evidence packet | `templates/demand-evidence-packet.md` |
| Closing a validation cycle | `templates/reviewtrace.md` |
| Need current strategy context | `05_每日记录/2026/07/20260706/20260706_product三条落地策略_组织产品个人.md` |
| Need product truth navigation | `03_索引/索引_AI_Family_Hub.md` and `03_索引/目标项目相关/索引_代号515_需求与验收.md` |

Read only the relevant files. Do not load every linked research note unless a claim depends on it.

## Trigger Boundary

Use this skill for:

- "product / 515 这个需求要不要做?"
- "把这个会议结论落成产品动作"
- "这个 bug / 小修改 / 新想法怎么进产品系统?"
- "Pre-flight / Aha / 责任卡 / Family Hub 下一步怎么拆?"
- "竞品、社交信号、last30days、用户反馈对 product 有什么产品含义?"
- "给 product 组织建需求与证据 loop / SOP / gate / owner"

Do not use it as the primary skill for:

- Personal GTD syncing or commitments. Use `gtd-harness` or `gtd-product-sync`.
- General startup stage decisions not tied to product/515 requirements. Use `ai-native-founder`.
- Source-of-truth disputes across documents. Use `truth-source-governance`, then return here if a product evidence packet is needed.
- Full user research from raw reviews/interviews. Use the relevant JTBD / research skill first, then feed the result here.

## Core Rule

Default output is a **demand evidence packet**, not a PRD section and not an implementation plan.

An item may enter execution only after it has:

1. A clear user problem.
2. A known product / 515 phase or a deliberate `out-of-scope` mark.
3. Evidence strength and source path.
4. The riskiest assumption.
5. A failure standard.
6. An owner.
7. A decision: `go`, `defer`, `kill`, or `needs evidence`.

If any of these are missing, say what is missing and default to `needs evidence`.

## Workflow

### 1. Classify The Input

Classify into one of:

| Type | Meaning |
|---|---|
| `new requirement` | A feature, user story, product change, or roadmap candidate |
| `evidence signal` | User quote, competitor signal, social signal, analytics, support issue |
| `bug / trust issue` | Behavior that may break reliability, trust, source, or sync |
| `meeting conclusion` | A decision-like statement from discussion |
| `organization loop` | Process, role, owner, gate, or learning-system change |

If the input is only a vague idea, keep it as `evidence signal` until the user problem is clear.

### 2. Read The Minimum Truth Set

Always start from index-level truth:

```bash
rtk sed -n '1,220p' 03_索引/索引_AI_Family_Hub.md
rtk sed -n '1,180p' 03_索引/目标项目相关/索引_代号515_需求与验收.md
```

Then use `rtk rg` for the exact phrase, feature name, or risk word. Prefer precise local sources over memory.

Useful search anchors:

- `Prepare`, `Pre-flight`, `Morning Brief`
- `first_trusted_chain_completed`, `first_preflight_decision_completed`
- `责任卡`, `责任交接`, `owner`
- `日历解析层`, `source`, `confidence`, `undo`, `audit`
- `Aha`, `首启`, `5分钟`

### 3. Build The Evidence Packet

Use `templates/demand-evidence-packet.md`.

Evidence strength:

| Strength | Meaning |
|---|---|
| `strong` | Repeated real-user behavior, direct quote, paid/retained behavior, or validated test |
| `medium` | Multiple converging local notes, competitor evidence, observed workaround |
| `weak` | Single meeting conclusion, internal intuition, synthetic user, social heat |
| `unknown` | No source yet |

Social heat, last30days output, or influencer claims are never stronger than `weak` until verified by primary source, real user behavior, or local evidence.

### 4. Apply Four Gates

| Gate | Pass Question |
|---|---|
| Evidence gate | What source proves this is a real problem or risk? |
| Risk gate | What trust, safety, privacy, source, sync, or relationship risk can it trigger? |
| Acceptance gate | How would we know this worked or failed? |
| Owner gate | Who owns judgment, verification, and follow-up? |

If a gate fails, the decision is `needs evidence` or `defer`, not `go`.

### 5. Decide

Use one of:

- `go`: Evidence and acceptance are strong enough for a bounded next action.
- `defer`: Direction is plausible, but timing, phase, cost, or dependency is wrong.
- `kill`: Contradicts strategy, creates trust risk, duplicates an existing rejected path, or solves no clear user problem.
- `needs evidence`: User problem, source, failure standard, or owner is missing.

Every decision needs a stop condition.

### 6. Only Then Edit Product Truth

If the user explicitly asks to update PRD, index, roadmap, issue table, or another product artifact:

1. Produce the evidence packet first.
2. Identify the canonical file before editing.
3. Patch only the smallest necessary section.
4. Verify with `rtk rg` that the new pointer is findable and no old broader claim remains.

Agent may generate evidence packets, risk lists, and experiment templates. Agent does not silently commit a requirement to P0, promise external behavior, or write product truth without user intent.

## Default Response Shape

```markdown
**判断**
go / defer / kill / needs evidence

**为什么**
[one direct paragraph]

**证据包**
| Field | Value |
|---|---|
| 输入类型 |  |
| 用户问题 |  |
| 对应 Phase |  |
| 证据强度 |  |
| 证据来源 |  |
| 最大风险 |  |
| 本轮只验证 |  |
| 失败标准 |  |
| owner |  |

**四道门**
| Gate | Pass/Fail | Evidence |
|---|---|---|

**下一步**
[one smallest action]

**停止条件**
[specific stop/defer/kill condition]
```

## Failure Guards

- Do not turn internal excitement into P0.
- Do not turn meeting notes into validated user demand.
- Do not call an Aha "real" before user behavior, rephrasing, and repeat use prove it.
- Do not let Pre-flight become generic event editing or reminder stacking.
- Do not recommend write-back before source, confidence, undo, and audit are solved.
- Do not make spouse/partner entry require app install in the first validation pass unless the user explicitly changes the experiment.
- Do not confuse personal GTD tasks with family coordination product behavior.

