---
name: worktree-handoff
description: Manage git worktree handoffs for multi-file, audit-heavy, parallel, or half-finished-risky changes. Use when the user mentions worktree, BRIEF.md, scratch.md, parallel review, large refactors, governance migrations, or when main should stay clean while a task may span many files.
---

# Worktree Handoff

## Decision Rule

Use a worktree when the task is multi-file, audit-heavy, likely to leave half-finished work, or may run in parallel with another agent/session. Stay in-place for a small, single-file, easy-to-verify edit.

## Workflow

1. Confirm the real repository.
   - The current project root may not be a git repo.
   - Check the target project directory, symlinks, and `git rev-parse --show-toplevel` before claiming scope.
   - Never assume a parent repo setting protects a nested or symlinked repo.

2. Check the starting state.
   - Inspect `git status -sb` and `git worktree list`.
   - If unrelated work is present, do not revert it. Either isolate your changes or create a worktree from the right branch.
   - For user-owned WIP in touched files, read carefully and work around it.

3. Create or enter the worktree.
   - Use a descriptive branch name.
   - Keep main clean when the task may take multiple passes.
   - Before creating a branch or worktree, show the exact repository, base,
     branch name, and destination path and obtain explicit user approval.
   - Record the assignment in the project's existing handoff location when that
     convention exists; otherwise keep it in the conversation unless the user
     asks for a project-local `BRIEF.md`.

4. Use the handoff split.
   - `BRIEF.md`: main -> worktree assignment, scope, constraints, inputs, success checks.
   - `scratch.md`: worktree -> main return notes, merge follow-ups, unresolved findings.
   - Do not use `scratch.md` as the source of truth for the task itself.

5. Execute and verify in the worktree.
   - Run the project-local tests/checks.
   - For governance work, run the relevant grep/drift/audit checks.
   - If subagents are involved, give each a disjoint responsibility and review their changes before integration.

6. Close the loop.
   - Re-check `git worktree list`, `git status -sb`, current `HEAD`, `origin/main` or the target base, and stash/WIP state.
   - Do not say all worktrees are clean or merged unless every surface was checked.
   - Report what stayed in the worktree, what moved back to main, and what remains open.

## Failure Guards

- Do not open a worktree as ceremony for tiny edits.
- Do not edit main and worktree copies of the same file casually.
- Do not confuse a clean worktree with a clean project; verify the main repo too.
- If a sync service or filesystem change makes a path disappear, pause file
  writes and re-check the path before continuing.
