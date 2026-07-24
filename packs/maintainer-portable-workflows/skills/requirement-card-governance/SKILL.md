---
name: requirement-card-governance
description: Route 515/product requirement, PRD, ZK card, inbox, candidate, unreleased, released, manifest, and changelog work through the correct canonical artifact and release gate. Use when deciding whether to create a PRD, update an unreleased card, keep a source in inbox, promote a release-ready candidate, or split product truth across facts, preparation, capture, and runtime capability layers.
---

# Requirement Card Governance

## Plain Rule

Before writing, answer: `where does this truth attach?`

Do not answer only `can it be built?` or `should we write a PRD?`. The useful decision is whether the truth belongs in a ZK card, source inbox, release-ready candidate, live unreleased manifest card, released truth, structure note, or action board.

## Required Reads

For 515-style requirement work, read these together before creating or moving cards:

- `05_requirements/prd-v<X>-unreleased/index.md`
- the live requirement card, if it exists
- `05_requirements/prd-v<X>-unreleased/changelog.md`
- relevant `inbox/` source or candidate notes
- project action source such as `NEXT-ACTIONS.md` when planning status is involved

For requirements derived from interviews, comments, JTBD analysis, or user research, also read:

- `.cursor/skills/jtbd-result-audit/references/job_statement_quality_gate.md`

Adjust paths to the live repo after checking the actual CWD and git root.

## Routing

1. Use a structure note or dry run when the product boundary is still exploratory.
2. Use `inbox/` for raw source, release-ready candidates, or material that has not passed gates.
3. Use `prd-v<X>-unreleased/` for live in-progress manifest cards that downstream docs actually consume.
4. Use `prd-v<X>-released/` only for shipped truth.
5. Keep a single ZK card as canonical when the user says the ZK card is what they want to maintain.
6. Use pointers, not parallel truth, for old docs that remain useful as navigation.

## Job Statement Gate

Do not promote interview notes, comments, or user complaints directly into a requirement card. First bind the card to at least one upstream Job Statement:

| Required field | Requirement-card use |
|---|---|
| `Context` | Defines the concrete user situation; prevents abstract persona prose |
| `Main Job` | Defines the user task; prevents feature-first wording |
| `Desired Outcome` | Defines success criteria; prevents vague "better/easier" claims |
| `Compensation Behavior` | Shows the user has already paid a workaround cost; helps prioritize |
| `Verbatim` | Anchors the card in real user language |

If any of those fields are missing, the card is not a requirement yet. Keep it in `inbox/` or candidate state as a hypothesis, with explicit `missing_evidence`.

Promotion rule:

- `evidence_grade A/B` + no fail-level Job Statement lint → may enter requirement-card review.
- `evidence_grade C/H` or missing `Verbatim` → keep as discovery hypothesis.
- Product-function wording without a user task → rewrite from `Main Job` before promotion.

## Edit Policy

When the user asks whether an unreleased requirement can change, answer with one of:

- `in-place clarification`: same behavior, clearer wording, same card.
- `new version or new card`: materially new behavior or a changed contract.
- `keep in inbox/candidate`: useful but not yet consumed or not through gates.
- `do not promote`: clear engineering text is not enough without gates.

Promotion into live unreleased manifest requires all three:

- `G-design audit`
- `Publish Gate`
- real downstream consumption

## Product Language

Write requirement prose around a real person, decision point, hidden information, and concrete cost. Avoid abstract lines such as `the system makes conflict visible` unless rewritten as a concrete user situation.

Useful pattern:

`When [person] is deciding [specific action], they cannot see [hidden information], so the cost is [concrete consequence]. The system should [bounded behavior].`

## Boundary Checks

- Facts, ownership, sync, and writeback belong together.
- Preparation output belongs in the home/action layer.
- Capture, routing, and responsibility proposals belong in the capture layer.
- Runtime memory/safety capability is not automatically a user-facing feature.
- Reward/points or gamification should not leak into responsibility-transfer core unless explicitly scoped.

## Verification

- Search for duplicate cards, old names, and stale manifest entries.
- Confirm `index.md`, the card, and `changelog.md` agree.
- Confirm old entrypoints point to the canonical owner.
- State exactly which artifact now owns the truth.
