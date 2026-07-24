---
name: review-and-verify
description: Check whether work satisfies its stated requirements and report evidence-backed gaps or a release verdict. Use when the user asks to review, audit, validate, test, inspect, fact check, or decide whether a deliverable is ready.
---

# Review and Verify

Review against the intended outcome, not against effort spent.

## Workflow

1. Derive a requirement-to-evidence map from the request and current rules.
2. Inspect the actual files, output, runtime state, or source material.
3. Exercise important success, failure, empty, and conflict paths.
4. Classify each requirement as proved, contradicted, incomplete, or unverified.
5. Report high-impact findings first, then residual risk and a clear verdict.

A passing command is evidence only for the behavior it actually covers. If live verification is unavailable, name the unverified boundary instead of inferring success.
