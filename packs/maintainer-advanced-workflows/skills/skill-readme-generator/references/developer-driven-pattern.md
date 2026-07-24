# Developer-Driven Pattern (Code-First)

## When to Use
Best for:
- CLI tools
- Browser automation
- Low-level utilities

## Structure

```markdown
# [Tool Name with Value Prop Subtitle]

## Installation
[Quick install commands - uvx/pip/npm]

## Quick Start
[Minimal working example - 3-5 lines]

## Core Workflow
1. [Step 1 with command]
2. [Step 2 with command]
...

## [Advanced Features Section]
### [Feature 1]
### [Feature 2]
```

## Example from browser-use (~27K installs)

```markdown
## Installation
# Run without installing
uvx "browser-use[cli]" open https://example.com

## Quick Start
\`\`\`bash
browser-use open https://example.com
browser-use state  # Get page elements
browser-use click 5
\`\`\`
```

## Characteristics

✅ Immediate action (can try in 30 seconds)  
✅ Progressive disclosure (basics → advanced)  
✅ Command reference style (documentation-like)  
⚠️ Low context (assumes dev knows why they need it)

## Key Principles

- **Instant gratification**: User should be able to run something in \u003c30 seconds
- **No explanation needed**: Code speaks for itself
- **Numbered steps**: Clear sequence for workflows
- **Command-first**: Show the command before explaining what it does
