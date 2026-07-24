---
name: skill-readme-generator
description: Generate README files for skills. Use when documenting a new skill or updating skill documentation.
---

# Skill README Generator

Generate professional README.md files for skills based on skills.sh Top 20 presentation patterns.

## When to Use This Skill

Use this skill when:
- You need to create a README.md for a skill to publish on GitHub
- You want to document a skill following skills.sh marketplace best practices
- You're preparing a skill for public distribution and need professional documentation
- The user says "create a README for [skill-name]" or "document this skill"

## How It Works: Pattern Matching

The skill analyzes your SKILL.md and automatically selects the best README pattern:

| Skill Type | Pattern | Best For |
|------------|---------|----------|
| Meta-tools (find/search/discover) | Intent-Driven | Workflow orchestrators, discovery tools |
| File processors (docx/pdf/csv) | Task-Driven | Multi-capability tools, format handlers |
| CLI/Automation tools | Developer-Driven | Browser automation, dev utilities |
| Interview/Analysis skills | Hybrid | Domain expert routing, professional output |

## What You Get

### Output
- **README.md** file in the skill's root directory
- Follows skills.sh Top 20 success patterns
- Scannable structure (H1 → H2 → H3 → code)
- Zero marketing fluff

### Quality Standards
All generated READMEs include:
- ✅ Clear H1 title (skill name + optional value prop)
- ✅ Executable code examples
- ✅ Concise overview (2-4 sentences max)
- ✅ Hierarchical, scannable structure
- ❌ No testimonials, comparisons, or fluff

## Quick Start

### Basic Usage
Tell the agent: "Create a README for skill-name"

The agent will:
1. Read the skill's SKILL.md
2. Analyze skill type and capabilities
3. Select matching pattern
4. Generate README

### Specify Pattern
To force a specific pattern:
- "Create an Intent-Driven README for [skill]"
- "Use Task-Driven pattern for [skill]"
- "Generate a Developer-Driven README"

## Pattern Reference

For detailed pattern structure and examples, see:
- `references/intent-driven-pattern.md` - Scenario-first approach
- `references/task-driven-pattern.md` - Capability matrix approach
- `references/developer-driven-pattern.md` - Code-first approach
- `references/best-practices.md` - skills.sh Top 20 analysis and common success factors
