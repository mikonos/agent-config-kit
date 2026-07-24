---
name: index-note
description: Create an index / entry-point note (MOC-like). Use when asked to build a directory, navigation, or “best starting points”.
---

# Index Note

## Principle
An index is an **entry point**, not a taxonomy. Be selective and keep it short.

## Quick start
- Pick an index type (keyword / structure / thinking trail).
- Select only 3–5 best entry notes.
- Immediately add bidirectional links (index ↔ entry notes).

## Index types
- **Hub note**: stable top-level entry for a domain
- **Structure note**: project outline / argument structure
- **Thinking trail**: chronological evolution of a line of thought

## Workflow

### Step 1: Collect
1. Choose index type
2. Search related notes
3. Extract 3–5 core concepts
4. Pick 1–2 best entry notes per concept

### Step 2: Shape the structure
- Separate primary vs secondary concepts
- Use indentation to show relationships
- Keep it within one screen

### Step 3: Link & maintain
- Index → entries: `[[Note]]`
- Entries → index: add backlink
- Mark created/updated time

## Output template

```markdown
# Index: [Topic]

## Overview
- **Type**: Hub / Structure / Trail
- **Status**: SEED / EVERGREEN
- **Created**: YYYY-MM-DD

## Core entry points
- [[Best starting note]] — why it’s the best start
- [[Second entry]] — why

## Quick navigation
- **Start here**: [[Best starting note]]
- **Go deeper**: [[Advanced note]]

## Related indexes
- [[Related index]]
```

## Common mistakes
- Treating the index as a full catalog → keep only the best entry points
- Too much hierarchy → keep it readable
- Never updating → review periodically

## Quality checks
- [ ] Entry points are truly “best starts”
- [ ] Navigation is clear
- [ ] Fits within one screen

