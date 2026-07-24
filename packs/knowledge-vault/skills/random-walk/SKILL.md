---
name: random-walk
description: Do a controlled random walk through your notes to create serendipity and write-backable bidirectional links. Use when asked to “random walk / explore / surprise me with links”.
---

# Random Walk

Luhmann deliberately created “accidents” by revisiting old cards. This skill operationalizes that habit.

## Inputs
- `mode` (default: `random`): `random` / `theme` / `time` / `cross`
- `count` (default: 4): recommended 3–5
- `filter` (optional): keyword or time prefix (e.g. `202401`)

## Workflow

### Step 1: Sample notes
Sample from your note directories (adjust to your repo):
- `Notes/`
- `Literature/`

Strategies:
- `random`: slightly bias toward older notes
- `theme`: filter by keyword, then random
- `time`: filter by date prefix
- `cross`: force one note from different domains/categories

### Step 2: Deep read — “three link questions”
For each sampled note:
1. How does it relate to my current problem/project?
2. What does it echo from recent learning?
3. What new question does it create?

### Step 3: Action output
- New link → propose bidirectional write-back edits
- New idea → propose a new fleeting/permanent note
- Needs update → specify what to refresh
- No signal → record why and adjust next parameters

## Output template

```markdown
## Random Walk Log [YYYY-MM-DD]

### Sampled notes
1. [[Note 1]] — one-line takeaway
2. [[Note 2]] — one-line takeaway

### Serendipity insights
- **[Note A] × [Current project]**: ...
- **[Note B] × [Note C]**: ...

### Actions
- [ ] [Concrete write-back change / new note]
```

## Quality checks
- [ ] ≥2 bidirectional link suggestions that can be written back
- [ ] ≥1 cross-domain analogy or “unexpected link”
- [ ] If no discoveries: explain why + propose better parameters

