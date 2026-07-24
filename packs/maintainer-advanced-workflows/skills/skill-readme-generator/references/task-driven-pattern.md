# Task-Driven Pattern (Capability Matrix)

## When to Use
Best for:
- File format handlers (docx, pdf)
- Multi-capability tools
- Technical utilities

## Structure

```markdown
# [Technical Skill Name]

## Overview
[1-2 sentence technical context]

## Quick Reference

| Task | Approach |
|------|----------|
| [Specific task 1] | [Tool/Method + code snippet] |
| [Specific task 2] | [Tool/Method + code snippet] |
...

## [Detailed Section 1]
### [Subsection with code examples]

## [Detailed Section 2]
...
```

## Example from docx (anthropics/skills, ~9.2K installs)

```markdown
## Overview
A .docx file is a ZIP archive containing XML files.

## Quick Reference

### Converting .doc to .docx
\`\`\`bash
python scripts/office/soffice.py --headless --convert-to docx document.doc
\`\`\`

### Reading Content
\`\`\`bash
pandoc --track-changes=all document.docx -o output.md
\`\`\`
```

## Characteristics

✅ Scannable matrix (user finds their task fast)  
✅ Code-first examples (copy-paste ready)  
✅ Hierarchical depth (Overview → Quick Ref → Details)  
⚠️ Assumes user knows what they're looking for

## Key Principles

- **Matrix format**: Use tables when possible (high scan value)
- **Task-oriented**: Organize by what user wants to do, not how it works
- **Copy-paste ready**: Every code example should be immediately executable
- **Progressive disclosure**: Overview → Quick Ref → Advanced Details
