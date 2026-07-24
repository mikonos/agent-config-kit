# Policy and Evidence Baseline

This file is a dated starting snapshot, not a permanent policy table. For publish-ready work, re-check the target Seller Central rules and Product Type Definition, then save the new source and check time in the run bundle.

## Table of contents

1. Verified snapshot
2. Current-fact freshness gate
3. Tool access and fallback
4. Claims the evidence does not support
5. Primary sources

## 1. Verified snapshot — 2026-07-15

- On 2026-05-13, Amazon renamed/combined Rufus and Alexa+ shopping capabilities as Alexa for Shopping. Its public explanation describes product catalog/knowledge, reviews, Community Q&A, web information, preferences, history, and conversation context as sources/signals.
- Starting 2026-07-27, Amazon announced a gradual rollout for non-media titles of up to 75 characters including spaces, plus up to 125 characters of Item Highlights. Listings remain active during the transition; brand owners receive a 14-day review window for relevant AI suggestions.
- Amazon Listing AI can draft titles, bullets, descriptions, and attributes from descriptions, images, URLs, or spreadsheets. The seller remains responsible for accuracy, completeness, law, and policy compliance.
- COSMO is an e-commerce commonsense knowledge-generation/serving system using relations such as `usedFor`, `capableOf`, `isA`, and `cause`. Its publication does not expose a seller-facing score or fixed Listing field weights.
- Manage Your Experiments supports randomized customer splits and can test multiple content attributes. The official page advises completing the experiment; custom durations commonly recommend 8–10 weeks, while to-significance may sometimes finish around four weeks.

Never copy this snapshot to another marketplace/product type without live verification.

## 2. Current-fact freshness gate

Live-verify whenever the task is current/latest, publish-ready, bulk, regulated, or marketplace-specific:

1. title limits, repetition/character rules, media exceptions;
2. Item Highlights availability, limit, display, indexing, template/API mapping;
3. Bullet, description, backend terms, image, A+, comparison, and alt-text rules;
4. required Product Type Definition attributes, enums, units, variation themes, safety/compliance;
5. Review Listings Changes access, coverage, review window, and notification behavior;
6. MYE eligibility, testable fields, multi-attribute behavior, duration, metrics;
7. SQP/SCP/POE/VOC/Brand Analytics access, marketplace coverage, latency, metric definitions;
8. reviews, Vine, Request a Review, and Community Q&A manipulation rules;
9. restricted-product and category-specific law/policy;
10. SP-API schema, patch semantics, contribution priority, errors, and rate limits;
11. Alexa for Shopping name, coverage, information sources, and capabilities.

If live verification fails, set:

```text
policy_status: unverified
publishability: draft_only
state: DRAFT_UNVERIFIED or BLOCKED_RISK
```

Do not issue a compliance pass.

## 3. Tool access and fallback

| Tool | Typical prerequisite | Fallback |
|---|---|---|
| SQP/SCP | Professional account; Brand Registry/Brand Representative for brand/ASIN analytics | ads search terms, business reports, orders/returns; label differing scope |
| MYE | Professional account, Brand Registry/Representative, eligible ASIN and traffic | pre-registered staged observation; inference no stronger than correlational |
| Review Listings Changes | Brand Registry and relevant representative permissions | own snapshots, submission logs, Manage All Inventory history, PDP sampling, Seller Support |
| POE/VOC/Customer Reviews/A+ | account, role, site, and tool-specific access | available demand, support, returns, review, and post-purchase signals |

The 14-day Amazon window is a maximum response window, not an internal SLA. Assign a human owner and check high-value catalogs more frequently; do not rely only on email/dashboard coverage.

## 4. Claims the evidence does not support

Do not state as facts:

- a seller-visible Alexa/Rufus/COSMO score;
- fixed title/Bullet/A+/image/Q&A weights;
- fixed Q&A count, question density, Bullet count, star threshold, or semantic-score threshold;
- direct rank lift from inserting COSMO relation words;
- guaranteed Alexa recommendation or first-page placement;
- image alt text/OCR as a proven direct Alexa ranking lever;
- “A9 is dead” or Alexa replaced traditional search;
- causal impact from one pre/post change, simulated score, anonymous case, or single-account answer.

## 5. Primary sources

- Alexa for Shopping, 2026-05-13: https://www.aboutamazon.com/news/retail/alexa-for-shopping-ai-assistant
- Alexa/Rufus information sources and personalization: https://www.aboutamazon.com/news/retail/amazon-rufus-ai-assistant-personalized-shopping-features
- COSMO publication: https://www.amazon.science/publications/cosmo-a-large-scale-e-commerce-common-sense-knowledge-generation-and-serving-system-at-amazon
- 2026 Title + Item Highlights update: https://sellercentral.amazon.com/seller-forums/discussions/t/145b6d0f-999c-4555-896c-c694bda2e470
- Amazon Listing AI: https://sell.amazon.com/blog/amazon-listing-ai
- Brand Analytics: https://sell.amazon.com/tools/amazon-brand-analytics
- Product Opportunity Explorer: https://sell.amazon.com/tools/product-opportunity-explorer/
- Manage Your Experiments: https://sell.amazon.com/tools/manage-your-experiments
- Customer Reviews: https://sell.amazon.com/tools/customer-reviews
- SP-API Manage Product Listings: https://developer-docs.amazon.com/sp-api/lang-en_EN/docs/manage-product-listings-guide
