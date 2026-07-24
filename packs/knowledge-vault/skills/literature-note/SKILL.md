---
name: literature-note
description: "Convert external material into reusable, linkable, executable literature-note assets. Use for articles, books, papers, videos, or podcasts through multi-pass reading, tool and template extraction, atomization, link discovery, deduplication, indexing, and QA."
---

# Literature Note (high-output)

## Role
Combine:
- **Luhmann** (links first)
- **Feynman** (can-you-teach test)
- **First principles** (mechanisms, constraints, leverage)

## Output contract (hard constraints)
- **Naming / ID**: use `YYYYMMDD_HH_Topic` consistently (file name == ID).
- **Keep concrete details**: names, numbers, platforms, specific actions, timelines.
- **How > What**: every framework/tool must include steps + template + checklist + pitfalls + evaluation.
- **Links**: end with **≥2** meaningful `[[bidirectional links]]` (state the link type).
- **Unknowns**: mark as `TBD` and list what to clarify.
- **Diagrams**: use PlantUML when a diagram is needed.

## Workflow

### Step 0: TODO first
Draft a task checklist (≥6 items), then execute, then report completion + QA.

### Step 1: Define inputs (boundary conditions)
- Material type + source (author/link/date; otherwise `TBD`)
- Your use case (decision / execution / skill building / writing / review)
- Output granularity (toolbox vs full framework)

### Step 2: Four-pass reading
1) **Frame**: structure + main claim + argument path
2) **Tooling**: extract all tools/templates/checklists (keep details)
3) **Network**: propose ≥5 link candidates, keep the best ≥2
4) **Completeness**: missing tools / boundaries / counterexamples / prerequisites

### Step 3: Atomize when needed
If there are ≥3 independent concepts/tools, split into multiple notes + create an index note.

### Step 4: Tool extraction (6 required fields)
For each tool:
1) purpose
2) inputs / prerequisites
3) steps (doable)
4) template (copy-paste)
5) acceptance checklist
6) pitfalls / failure modes + prevention

## Output template (single file)

```markdown
# YYYYMMDD_HH_Topic

## 🆔 ID
ID: [[YYYYMMDD_HH_Topic]]

## Source
- Type:
- Author/org:
- Link/path:
- Date/version:
- Use case:
- Importance: L1/L2/L3 (why)

## One-sentence summary (Feynman)
> What problem does it solve, by what mechanism, and how to apply it?

## Frame
- Main claim:
- Argument path: A → B → C
- Key conclusions (3–7):

## Tool library (high signal)
| Tool | Purpose | Inputs | Steps | Template | Checklist | Pitfalls | Evaluation |
|---|---|---|---|---|---|---|---|

## Next experiments
- [ ] Smallest actionable experiment this week (owner/date can be TBD)

## Links (≥2, explain why)
- : supplement/contrast/apply/analogy/counterexample — why
- : ...

## QA (results only)
- Extracted: concepts X / tools Y / cases Z
- Structure: Frame clear / How executable / Why includes mechanism + boundaries
- Links: N links with reasons
```

## Quality checklist
- [ ] File name == ID
- [ ] Tools are fully specified (purpose/inputs/steps/template/checklist/pitfalls/eval)
- [ ] Concrete details preserved
- [ ] ≥2 meaningful links with stated relationship
