---
name: meeting-note
description: High-output meeting/conversation notes (decisions, alignment, disagreements, decision trail, assumptions, risks/opportunities, action items) + Zettelkasten links. Use when asked to summarize meeting notes or turn a conversation into reusable knowledge.
---

# Meeting Notes (high-output)

## Core idea
The value is not “what was said”, but:
- why it was said
- what was *not* said (assumptions, power dynamics)
- what it means (risks, decisions, next actions)
…and then linking it into your knowledge network.

## Hard constraints
- Unknowns → `TBD` (time, attendees, owners, deadlines, data sources, etc.)
- Structure by topics and decision status (✅ / ⏳ / ❓)
- Must deliver:
  - decisions / alignment / disagreements (with speakers + reasons)
  - decision trail (proposal → debate → converge / postpone)
  - assumptions (“elephants in the room”) with evidence
  - risks & opportunities + mitigation/leverage
  - action items (measurable + owner + deadline + success criteria)
  - ≥2 Zettelkasten links (`[[Note]]`)

## Workflow

### Step 0: Plan first
Draft a short TODO list, then execute, then report completion + QA.

### Step 1: Basics & importance
- Basics: time, place, topic, attendees (name + role)
- Meeting type: decision / discussion / report / brainstorm / alignment
- Importance:
  - L3 strategic/high-risk → add “expert roundtable”
  - L2 project/stage decision → emphasize decision trail + actions
  - L1 daily sync → stay concise but keep actions

### Step 2: Multi-pass processing
1) Map topics (name each topic with one sentence)
2) Speaker deep-dive (if there is a main presenter)
3) Key decision-maker deep-dive (if applicable)
4) Power dynamics & hidden layer (with evidence)

### Step 3: Topic-by-topic structure
For each key topic include:
- conclusion (✅/⏳/❓) and what blocks it
- alignment points
- disagreement points (speaker + reason)
- decision trail
- hidden layer (assumptions; must include evidence)
- risks/opportunities
- open questions + needed inputs

### Step 4: Atomize reusable units
Extract “atoms”:
- decision atoms
- insight atoms
- assumption/risk atoms

### Step 5: Action items
Each action item must have:
- verb-first task
- measurable success criteria
- owner + deadline (TBD if unknown)

## Output template

```markdown
# YYYYMMDD_HH_MeetingTopic_MeetingNotes

## 🆔 ID
ID: [[YYYYMMDD_HH_MeetingTopic_MeetingNotes]]

## Basics
- Time:
- Place:
- Attendees:
- Type:
- Goal:
- Importance: L1/L2/L3 (why)

## Topic overview
| # | Topic | Status |
|---|------|--------|
| 1 | ...  | ✅/⏳/❓ |

---

## Topic 1: [name]
### Conclusion
### Alignment
### Disagreements (speaker + reason)
### Decision trail
### Hidden layer (with evidence)
### Risks & opportunities
### Open questions (inputs needed)

---

## Key insights (atomic)
1. **[Insight]**: one sentence (decision/insight/assumption/risk)

## Action plan (trackable)
| # | Task | Owner | Due | Priority | Success criteria |
|---|------|------|-----|----------|------------------|

## Follow-ups (make uncertainty explicit)
- [ ] Who needs to confirm what? (owner/deadline TBD)

## Links (≥2)
- [[Related meeting / project / method note]] — link type + why
```

## Quality checks
- [ ] Each key topic includes conclusion/alignment/disagreement/trail/hidden layer/risks/open questions
- [ ] Action items are measurable and owned (TBD allowed)
- [ ] ≥2 links with clear relationship
