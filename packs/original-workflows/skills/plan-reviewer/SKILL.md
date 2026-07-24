---
name: plan-reviewer
description: |
  Review important plans, strategies, roadmaps, launches, migrations, or irreversible decisions before execution.
  Use when the user asks to review a plan, check risks, find gaps, pre-mortem a proposal, sanity-check a strategy,
  evaluate whether a plan is executable, or identify assumptions, missing steps, dependencies, alternatives,
  and failure modes. Do not use for generic brainstorming with no concrete plan; use strategic-advisor instead.
---

# Plan Reviewer

Use this skill to review an existing plan before execution. The goal is not to create a new strategy from scratch;
it is to prevent foreseeable mistakes, expose hidden assumptions, and make the plan more executable.

## Workflow

### 1. Restate The Plan

Start by compressing the plan into:

- Goal: what outcome it is trying to produce
- Scope: what is included and excluded
- Success criteria: how we know it worked
- Constraints: time, people, money, tools, dependencies

If any of these are missing, mark them as open questions instead of inventing certainty.

### 2. Assumption Check

List the assumptions the plan depends on:

- User/customer assumptions
- Market or timing assumptions
- Resource and capacity assumptions
- Technical or operational assumptions
- Stakeholder and approval assumptions

For each important assumption, say whether it is validated, weakly supported, or untested.

### 3. Failure Mode Review

Run a short pre-mortem:

- What would make this plan fail even if the team works hard?
- What step is most likely to slip?
- What dependency could block execution?
- What risk is low probability but high impact?
- What would be expensive or hard to reverse?

Prioritize risks by severity, not by how interesting they are.

### 4. Completeness And Sequencing

Check whether the plan has:

- Clear owner for each major workstream
- Correct order of operations
- Decision gates before irreversible steps
- Test or validation points before scaling
- Rollback or recovery path
- Communication plan for affected people

### 5. Alternatives

Only propose alternatives when they are meaningfully better, simpler, cheaper, or safer. Do not add options just to look thorough.

Use this structure:

- Keep: what is already strong
- Change: what must be modified before execution
- Cut: what adds complexity without enough value
- Add: what is missing and materially reduces risk

## Output Format

```markdown
# [Plan Name] Review

## Verdict
[Can execute / modify before execution / rethink]

## Main Findings
### Must Fix
- [Problem] -> [Concrete fix]

### Should Improve
- [Issue] -> [Suggested adjustment]

### Optional
- [Small optimization]

## Hidden Assumptions
- [Assumption] - [validated / weak / untested]

## Failure Modes
| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|

## Missing Pieces
- [Missing owner, dependency, validation, rollback, communication, metric, etc.]

## Better Path
[Only if there is a simpler or safer alternative]
```

## Review Rules

- Be direct and specific; vague warnings are not useful.
- Separate blockers from nice-to-have improvements.
- Do not rewrite the plan unless the user asks.
- Do not overcomplicate a plan that is intentionally lightweight.
- If the plan is already good enough, say so and identify residual risk.
- If the plan is missing basic information, ask only the smallest number of questions needed to review it.
