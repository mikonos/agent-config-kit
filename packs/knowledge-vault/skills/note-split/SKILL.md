---
name: note-split
description: Split long notes into atomic, reusable notes. Use when asked to “atomize / split / break down” a note, and produce titles, source ranges, and link suggestions.
---

# Note Split (Atomization)

## Goal
Turn one long, fuzzy document into multiple notes that can stand alone and connect cleanly.

## Quick start
- Identify 3–7 candidate atomic concepts.
- For each new note: one-sentence core + original source location + ≥2 link suggestions.

## Workflow

### Step 1: Concept identification (three layers)
1. Surface concepts (explicit terms)
2. Implicit concepts (assumptions / premises)
3. Core insight (what the author really claims)

### Step 2: Boundary test
- If removing any part breaks the concept, it’s not atomic yet.
- If the concept can explain other phenomena, it’s a good atomic note.

### Step 3: Split plan
Provide a mapping table:
- original section → new note title → core concept → note type (concept/method/case)

### Step 4: Title patterns
- Definition: “What is X? core elements”
- Method: “Method X: key steps”
- Insight: “On [topic]: [insight]”

### Step 5: Links
Include:
- sibling links (notes split from the same source)
- topical links (same theme)
- contrast links (alternative view / counterexample)

## Output template

```markdown
## 📋 Split Plan

### Source note
- **File**: [name]
- **Length**: [words/lines]
- **Concepts identified**: [N]

### Proposed new notes

#### 1) [New note title]
- **Core concept**: [one sentence]
- **Source location**: [section/paragraph]
- **Suggested links**: [[Link 1]] [[Link 2]]

### Keep-as-index suggestion
- Keep the original as an index note? yes/no (why)
```

## Quality checks
- [ ] Each new note is atomic and independently understandable
- [ ] Each includes source location
- [ ] Clear linking between split notes and the wider network

