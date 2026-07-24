---
name: connection-discovery
description: Propose write-backable, bidirectional links between notes. Use to connect new notes, rescue orphan notes, or find cross-domain associations.
---

# Connection Discovery

## Purpose
Embed notes into a living knowledge network by proposing **high-value bidirectional links** you can actually add to both files.

## Quick start
- Extract 3–7 key concepts from the target note.
- Run 2–3 search passes (direct keyword, conceptual, cross-domain).
- Deliver only the top 3–5 links, each with **write-back text for both sides**.

## Workflow

### Step 1: Analyze the target note
- Identify core topic and key concepts
- Identify note type (theory / case / method / insight)
- Produce search keywords

### Step 2: Multi-pass search
- **Direct**: obvious topical neighbors
- **Conceptual**: shared models / methods / mechanisms
- **Serendipity**: forced cross-domain analogy

### Step 3: Typed links (optional but recommended)
Use explicit link types:
- `extends` / `is_extended_by`
- `questions` / `is_questioned_by`
- `supports` / `is_supported_by`
- `contradicts` (symmetric)
- `analogous` (symmetric)

### Step 4: Rank connections
Score each candidate:
- Meaning depth (1–5)
- Personal specificity (1–5)
- Network leverage (1–5)

### Step 5: Output bidirectional write-back
For each selected link, provide:
- why it matters
- exact snippet to add into **both** notes

## Output template

```markdown
## 🧩 Connection Plan

### Target note
**Note**: [[Target]]
**Core concepts**: [c1, c2, ...]

### Suggested bidirectional links

#### 1) With [[Related A]]
- **Type**: extends/questions/supports/contradicts/analogous
- **Why**: ...
- **Add to Target**:
  > `[[Related A]]` (…)
- **Add to Related A**:
  > `[[Target]]` (…)

### Serendipity
- **[Unexpected link]**: ...
```

## Quality checks
- [ ] ≥2 meaningful links for new notes
- [ ] Each link includes write-back text for both sides
- [ ] Each link has a clear value statement

