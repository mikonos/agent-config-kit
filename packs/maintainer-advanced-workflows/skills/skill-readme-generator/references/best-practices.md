# skills.sh Top 20 Best Practices

Based on analysis of top-performing skills on skills.sh marketplace (172K to 9K installs).

## Common Success Factors (All Top 20)

### 1. Clear H1 Title
- Skill name (if self-explanatory)
- OR Skill name + value prop subtitle
- Example: "Browser Automation with browser-use CLI"

### 2. Code Blocks Everywhere
- Every skill has executable examples
- Use language identifiers (`bash`, `python`, etc.)
- Keep examples to 1-3 lines when possible
- Show actual output in comments if helpful

### 3. Concise Overview
- 2-4 sentences max before diving in
- Technical context, not motivation
- Answer "what is this?" not "why does this exist?"

### 4. Zero Fluff
- No marketing speak
- Pure utility
- Direct and professional

### 5. Hierarchical Structure
- H2 → H3 → code
- Very scannable
- Easy to jump to relevant section

## What's Notably ABSENT

❌ Testimonials or social proof  
❌ Comparison tables ("Why us vs. X")  
❌ Long background/motivation sections  
❌ Author bios or credentials  
❌ "Getting started" tutorials (assumes competent users)

## Writing Formulas

### "When to Use" Pattern
```
Use this skill when [user/you]:
- [Verb] "[quoted user question/statement]" where [context]
- [User action] that suggests [need]
- [User goal] like [specific example]
```

### Quick Reference Table Patterns

**Task-Approach Matrix** (docx style):
| Task | Approach |
|------|----------|
| [User goal] | [Tool/command + code snippet] |

**Capability Matrix** (hybrid pattern):
| [Dimension 1] | [Dimension 2] | [Outcome] |
|--------------|---------------|-----------|
| [Variable input] | [Framework/Expert] | [What user gets] |

## SEO on skills.sh Platform

- **H1 = Page Title**: First H1 becomes the page title
- **First paragraph**: Acts as meta description
- **Keywords**: Naturally include in "When to Use" scenarios

## Markdown Rendering Notes

- Tables render perfectly
- Code blocks with syntax highlighting
- Alerts/admonitions NOT supported (use standard markdown)
- Images render but rarely used in top skills

## Platform Context

### How skills.sh Works
1. **Discovery**: Leaderboard ranked by total installs (All Time / Trending 24h / Hot)
2. **Installation**: Single command `npx skills add <owner/repo>`
3. **Presentation**: Platform renders SKILL.md directly from GitHub repo
4. **Sidebar**: Shows weekly installs, repo link, compatible agents

### Top 20 Distribution
| Category | Count | Example |
|----------|-------|---------|
| Development Tools | 8 | typescript-best-practices, test-driven-development |
| Search/Documentation | 5 | search-mdn, search-react-docs |
| Content/File Processing | 4 | docx, browser-use, pdf |
| Meta/Discovery | 2 | find-skills, skill-creator |
| Analysis/Audit | 1 | seo-audit |

## Differentiation Strategy

Most skills compete on:
- **Coverage** (Can do X, Y, Z)
- **Simplicity** (Easiest to use)

Stand out by highlighting:
- **Intelligence** (Context-aware expert selection)
- **Methodology Transparency** (Show WHY, not just WHAT)
- **Professional Output** (Structured, enterprise-grade)

**Example Positioning**:
> "The only interview analysis skill that routes to domain-specific evaluation frameworks (Marty Cagan for PM, John Carmack for Engineering). Not just AI analysis - AI with the right expert's lens."

## Quick Checklist for Generated READMEs

- [ ] H1 title is clear and concise
- [ ] First paragraph is 2-4 sentences max
- [ ] Includes executable code examples
- [ ] Uses tables for scannable reference
- [ ] No marketing language or fluff
- [ ] Hierarchical structure (H2 → H3 → code)
- [ ] Matches one of the 3 proven patterns (or hybrid)
