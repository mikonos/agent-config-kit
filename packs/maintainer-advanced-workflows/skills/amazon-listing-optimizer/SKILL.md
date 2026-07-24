---
name: amazon-listing-optimizer
description: Evidence-first Amazon Listing audit, rewrite, migration, and experiment workflow. Use when the user asks for Amazon Listing optimization, 亚马逊 Listing 优化/重写/诊断, Title or Item Highlights migration, keyword-to-field mapping, Alexa for Shopping/COSMO readiness, claim compliance lint, A+ or Bullet planning, or MYE/A-B validation. Do not use for general ecommerce copy outside Amazon or for fabricating reviews, Q&A, product facts, ranking guarantees, or automatic Seller Central publishing.
metadata:
  routing:
    requirePromptTriggers: true
    requireFileTriggers: true
    requireDescriptionRouting: true
---

# Amazon Listing Optimizer

Treat a Listing as a compiled artifact, not a creative-writing prompt.

- Product facts are the dataset.
- Customer questions are the task distribution.
- Field rules are the compiler target.
- Deterministic lint is the test suite.
- Seller Central feedback and experiments are the data flywheel.

The model is jagged: it can compress and rewrite well, then invent one fatal certification, compatibility claim, pack count, or causal story. Put imagination in candidate generation; put facts, policy, approval, and inference behind hard gates.

## Operating boundary

Produce analysis, candidate content, structured evidence maps, lint reports, release packets, and experiment plans. Never:

- invent product specifications, tests, certifications, search volume, PPC, conversion, or platform scores;
- turn competitor reviews, category convention, or LLM knowledge into this product's facts;
- create fake reviews/Q&A, filter for positive reviews, hide affiliation, or manipulate shopper behavior;
- guarantee ranking, sales, Alexa recommendation, or a seller-facing Alexa/Rufus/COSMO score;
- approve claims on behalf of product, compliance, or operations owners;
- write to Seller Central, SP-API, ads, reviews, Q&A, or a production catalog without separate explicit authorization and human approval.

The highest state this skill may assign is `READY_FOR_HUMAN_REVIEW`. There is no `READY_TO_PUBLISH` state.

## Scenario router

| User intent | Mode | Minimum output |
|---|---|---|
| “看看哪里有问题” | `AUDIT` | scope, gap report, claim risks, field lint, next evidence |
| “重写/生成 Listing” | `BUILD` | fact/claim map, question map, candidates, lint, human-review packet |
| “迁移 75/125、新标题规则” | `MIGRATE` | live policy snapshot, before/after diff, canary and rollback plan |
| “为什么曝光/点击/转化差” | `DIAGNOSE` | funnel diagnosis, competing explanations, smallest next test |
| “做 A/B、MYE、证明改版有效” | `EXPERIMENT` | eligibility, hypothesis, design, guardrails, inference label |
| “Alexa/Rufus/COSMO 优化” | `AI_SHOPPING` | question coverage and source consistency; no score or rank promise |
| “自动发布/批量改/造评论问答” | `REJECT_OR_GATE` | refuse unsafe part; offer candidate + review workflow |

For a mixed request, run `AUDIT → BUILD/MIGRATE → EXPERIMENT`. Do not start from copy generation.

## Progressive disclosure

The core workflow is self-contained. When an input fixture or brief already supplies scope and facts, start from this file and produce the smallest safe artifact; do not preload every reference.

Open a reference only when its added detail is required:

| Need | Open |
|---|---|
| Normalize an unstructured brief, construct a lint bundle, or resolve schema ambiguity | `references/input-contract.md` |
| Make a current-policy statement, prepare publish review, check Alexa/COSMO claims, or assess tool eligibility | `references/policy-and-evidence.md` |
| Produce the full reusable review packet rather than a concise answer | `references/output-templates.md` |

For an isolated or time-boxed run without live policy access, do not research indefinitely: label the policy gap, stop at `DRAFT_UNVERIFIED`, and give the next verification step. Stop reading once the mode's minimum output and the relevant gates can be satisfied.

If the user asks for “current/latest”, intends to publish, or the saved policy is stale/absent, re-check current Amazon official sources and the target marketplace/product type before drafting a compliance verdict. A static reference can start research; it cannot issue a current `PASS`.

## State machine

Use exactly one terminal state per run:

| State | Meaning | Allowed next action |
|---|---|---|
| `NEEDS_INPUT` | Marketplace/product type/variant or canonical facts are missing | Request only the blocking facts; still produce a gap report |
| `BLOCKED_RISK` | Facts conflict, high-risk claim lacks evidence, policy cannot be checked, or request is deceptive | Refuse the risky part; list remediation evidence |
| `DRAFT_UNVERIFIED` | A useful candidate exists but policy, evidence, lint, sample, or approval is incomplete | Preserve candidate as non-publishable draft |
| `READY_FOR_HUMAN_REVIEW` | Current policy checked, deterministic lint has no blocker, and every claim is traceable | Hand off to named human approvers; do not publish |

State cannot advance by model self-assessment. Each transition requires an artifact or named human.

## Core workflow

### 1. Lock scope and freshness

Capture:

- marketplace, locale, product type/category;
- parent and child ASIN/variation boundary;
- brand and target customer;
- mode and desired output;
- policy source, `checked_at`, `effective_at`, and account/tool eligibility;
- current Listing snapshot and metric window if an ASIN exists.

Do not propagate facts across child ASINs or marketplaces. If material, dimension, pack count, compatibility, or units conflict, stop that claim at `BLOCKED_RISK` and generate a conflict matrix.

### 2. Build the fact manifest before copy

Normalize each product-specific fact into the schema in `references/input-contract.md`:

```text
claim_id → attribute/value/unit → variant/marketplace → evidence grade/source/date → allowed/prohibited wording
```

Evidence grades:

| Grade | Meaning | Use |
|---|---|---|
| `E0` | unknown, inferred, or conflicting | never publish as a claim |
| `E1` | supplier/owner statement, not independently tested | factual, qualified wording only; no absolute performance promise |
| `E2` | measured internal spec/test with product and conditions matched | bounded claim within tested conditions |
| `E3` | stable external/regulated evidence matched to product and market | use within certificate/legal scope; still check category policy |

Competitor content, reviews, Q&A, and category knowledge may create `question_id` or risk hypotheses. They cannot create a product `claim_id`.

### 3. Build the question distribution

Prefer real SQP/SCP, ad search terms, POE, VOC, returns, reviews, support, and real Q&A. Use the model only to cluster or propose gaps.

Cover:

- identity (`isA`);
- capability/task (`capableOf`, `usedFor`);
- audience and context;
- fit/compatibility;
- comparison;
- concern and boundary.

Every priority question must map to a verified claim, an explicit evidence gap, or a product defect. Do not fabricate an answer to make coverage look complete.

### 4. Compile facts into field responsibilities

Use current marketplace/category limits. Do not assume the saved US 75/125 snapshot applies elsewhere.

| Field | Primary responsibility |
|---|---|
| Title | minimum sufficient product identity and decisive variation |
| Item Highlights | materials, recommended uses, and comparison details when currently supported |
| Product Details | structured, comparable specifications and compliance attributes |
| Bullets | decision facts, benefits, boundaries, package contents |
| Images/A+ | visual proof, dimensions, components, operation, comparison, complex explanation |
| Backend terms | relevant residual synonyms/variants not already covered; never a hidden claim channel |
| Reviews/Q&A | independent customer evidence; observe and respond lawfully, never script as SEO inventory |

Generate at most three purposeful candidates: `identity-first`, `decision-first`, `concise-compliant`. Keep `claim_ids` attached to every sentence or field.

### 5. Run deterministic lint

When a normalized bundle exists, run:

```bash
python3 <installed-skill-dir>/scripts/listing_lint.py \
  <bundle.json> --mode draft --out <lint-report.json>
```

Use `--mode review` only after current policy is checked and named approvers are present. The script checks mechanical gates; it cannot judge product truth, category law, or commercial quality.

Lint **one child ASIN per bundle**. For a multi-child migration, compile and lint one variant-specific bundle for each child, then assemble their reports into the parent rollout packet. This prevents a Red/12 claim from being required on, or accidentally propagated to, a White/8 child.

Blockers include:

- missing/stale policy metadata for a current compliance verdict;
- field length outside the supplied live policy;
- missing, duplicate, `E0`, unverified, or variant-mismatched claims;
- absolute wording backed only by `E1`;
- competitor brands, forbidden terms, or prohibited claim wording;
- priority questions with neither answer nor explicit gap;
- an answered P0 question whose claim is unknown/unpublishable or whose visible field does not reference that claim;
- policy not yet effective for the target date, or an Item Highlights candidate when that field is not confirmed supported;
- causal inference without a randomized/eligible design;
- review mode without product, compliance, and operations approval records containing `status: approved`, a human identifier, and a timezone-aware timestamp.

### 6. Hand off a review packet, not a publish action

Use `references/output-templates.md`. Include:

1. state and assumptions;
2. gap/conflict report;
3. question → claim → field map;
4. candidate fields with claim IDs and character counts;
5. lint report with blockers/warnings;
6. before/after diff, canary, rollback, and change log;
7. named product/compliance/operations approval slots.

If the user supplied only a loose brief, give the smallest safe draft and the exact missing facts. Do not stall for non-blocking niceties.

### 7. Design measurement at the correct inference level

Diagnose first:

| Symptom | First hypotheses |
|---|---|
| low impressions | indexing, product type/attributes, relevance, availability |
| impressions but low click | title, main image, price/offer, review signal |
| click but low cart/purchase | evidence, fit, expectation, price/offer, delivery |
| conversion up but returns/VOC worsen | misleading expectation or product issue |

Then label inference:

- `randomized`: eligible, uncontaminated MYE/random split and completed analysis;
- `correlational`: pre/post or non-random comparison with controlled log;
- `observational`: descriptive monitoring only;
- `inconclusive`: insufficient sample, policy drift, or confounding.

Single-variable tests support component learning. Multi-attribute tests can select an overall package but cannot reliably attribute the win to one component. Without MYE/eligible traffic, never write “the Listing change caused growth.”

Alexa for Shopping observations use an authorized fixed question set across dates/contexts. They detect answer gaps and drift; they do not produce a universal rank or field weight.

## Gray-zone gate

Ask one blocking question or downgrade when any of these changes the result:

- marketplace, locale, product type, parent/child ASIN is unclear;
- units, dimensions, pack count, materials, certification, compatibility, or images conflict;
- medical, child, food, pesticide, electrical safety, environmental, or other regulated claims appear;
- comparison claims lack test conditions or a defined comparator;
- user wants several fields plus price/ads changed while asking for component attribution;
- tool access/eligibility is assumed but not verified.

Refuse the unsafe portion when the request depends on deception, fake feedback, hidden competitor terms, fabricated evidence, ranking guarantees, or approval bypass.

## Completion contract

Before returning `READY_FOR_HUMAN_REVIEW`, verify:

- current marketplace/product-type policy has source and check time;
- canonical facts are variant-specific and conflict-free;
- every candidate sentence maps to valid evidence;
- deterministic lint reports zero blockers;
- current field counts are shown, not merely claimed checked;
- no fake reviews/Q&A, hidden competitor terms, or algorithm guarantees;
- change scope, baseline, canary, rollback, and inference label are explicit;
- human approval slots are named and unfilled by the model.

If any item fails, return `NEEDS_INPUT`, `BLOCKED_RISK`, or `DRAFT_UNVERIFIED` with the next smallest remediation step.
