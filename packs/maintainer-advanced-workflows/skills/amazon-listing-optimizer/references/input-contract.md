# Input Contract

Use this contract for `AUDIT`, `BUILD`, `MIGRATE`, and `EXPERIMENT`. Plain-text inputs may be normalized into this shape. Never infer a missing product-specific value.

## Table of contents

1. Scope and policy
2. Product facts and claims
3. Questions and source signals
4. Candidate Listing
5. Experiment and approvals
6. Conflict rules

## 1. Scope and policy

```json
{
  "scope": {
    "marketplace": "US",
    "locale": "en-US",
    "product_type": "ARTIFICIAL_PLANT",
    "parent_asin": null,
    "child_asins": ["B0EXAMPLE"],
    "target_date": "2026-07-27",
    "brand": "ExampleBrand",
    "mode": "BUILD"
  },
  "policy": {
    "checked_at": "2026-07-15",
    "effective_at": "2026-07-27",
    "source_url": "https://...",
    "title_max_chars": 75,
    "item_highlights_max_chars": 125,
    "max_age_days": 7,
    "item_highlights_supported": true
  }
}
```

The numbers above illustrate the verified 2026 US non-media snapshot; they are not universal defaults. Load the target marketplace/product-type values from current official sources or Seller Central.

The deterministic linter accepts **one child ASIN per bundle**. For a parent with several children, create a separate scope, fact set, Listing candidate, and lint report for each child; then combine those reports only in the rollout packet. Never make one child's claim cover every sibling.

## 2. Product facts and claims

```json
{
  "claims": [
    {
      "claim_id": "CL-001",
      "attribute": "material_treatment",
      "value": "UV-treated polyethylene",
      "unit": null,
      "marketplace": "US",
      "variants": ["B0EXAMPLE"],
      "evidence_grade": "E1",
      "evidence_status": "verified_source",
      "evidence_source": "supplier-spec-2026-07.pdf",
      "evidence_date": "2026-07-01",
      "allowed_wording": ["made with UV-treated material"],
      "prohibited_wording": ["never fades", "100% fade proof"],
      "owner": "product"
    }
  ]
}
```

Required claim fields:

- `claim_id`, unique;
- `attribute`, `value` and unit where applicable;
- marketplace and exact variants;
- evidence grade/status/source/date;
- allowed and prohibited wording;
- owner.

Evidence status values: `verified_source`, `needs_verification`, `conflicting`, `expired`.

## 3. Questions and source signals

```json
{
  "questions": [
    {
      "question_id": "Q-001",
      "text": "Will it fade in full sun?",
      "type": "concern_boundary",
      "priority": "P0",
      "sources": ["returns-2026Q2.csv", "review-theme-04"],
      "claim_ids": ["CL-001"],
      "status": "answered",
      "field_refs": ["item_highlights", "bullet_1"]
    }
  ]
}
```

Allowed question status: `answered`, `explicit_gap`, `product_issue`, `deferred`. P0 questions must not disappear; if no claim supports them, use `explicit_gap`.

Source signals such as competitor reviews must include `product_specific: false`. They may support the question, never the answer.

## 4. Candidate Listing

```json
{
  "listing": {
    "title": {
      "text": "ExampleBrand Artificial Flowers, 12 Bundles, Outdoor Planters",
      "claim_ids": ["CL-002", "CL-003"]
    },
    "item_highlights": {
      "text": "UV-treated material for porches and patios; check the size image before choosing a planter.",
      "claim_ids": ["CL-001", "CL-004"]
    },
    "bullets": [
      {
        "field_id": "bullet_1",
        "text": "Includes 12 bundles; dimensions are shown in the size image.",
        "claim_ids": ["CL-002", "CL-004"]
      }
    ],
    "backend_terms": {
      "text": "faux greenery patio decor",
      "claim_ids": []
    }
  },
  "competitor_brands": ["CompetitorA"],
  "forbidden_terms": ["best", "perfect", "never", "100%", "#1"]
}
```

All visible field claims must carry `claim_ids`. Backend terms may have no claims only when they are genuine synonyms/categories, not hidden product promises.

## 5. Experiment and approvals

```json
{
  "experiment": {
    "design": "observational",
    "objective": "component_learning",
    "changed_fields": ["title"],
    "primary_metric": "click_through_rate",
    "guardrail_metrics": ["conversion_rate", "return_rate", "cx_health"],
    "minimum_sample": "pre-registered by operator",
    "observation_window": "one complete business cycle",
    "confounders": ["price", "ads", "inventory", "coupon", "buy_box", "rating"],
    "rollback_rule": "rollback on material CTR/CVR or expectation harm",
    "inference": "correlational",
    "mye_eligible": false
  },
  "approvals": {
    "product": {
      "status": "approved",
      "approver": "product-owner@company",
      "approved_at": "2026-07-15T09:00:00+08:00",
      "evidence_ref": "approval-ticket-123"
    },
    "compliance": null,
    "operations": null
  }
}
```

`design`: `MYE_randomized`, `randomized`, `observational`, or `none`.  
`objective`: `component_learning`, `package_optimization`, or `monitoring`.  
`inference`: `randomized`, `correlational`, `observational`, or `inconclusive`.

For review mode, each of `product`, `compliance`, and `operations` must be an object with `status: approved`, a non-empty human `approver`, and a timezone-aware ISO-8601 `approved_at`; `evidence_ref` is recommended. `pending`, a role name, a Boolean, or an unstructured string is not approval. The model must not populate or infer any approval record.

## 6. Conflict rules

Create a conflict row and stop the affected claim when:

- two sources disagree on material, dimensions, unit, compatibility, pack count, certification, or warranty;
- a source does not match marketplace, child ASIN, SKU, test condition, or date;
- image, specification, manual, certificate, and PDP disagree;
- US and another marketplace are being compiled from one policy object;
- a parent fact is being propagated to children without evidence.

Conflict output:

| conflict_id | attribute | marketplace | variants | source A | source B | risk | owner | state |
|---|---|---|---|---|---|---|---|---|
| CF-001 | pack_count | US | B0... | 12 bundles | 12 stems | misleading quantity | product | BLOCKED_RISK |
