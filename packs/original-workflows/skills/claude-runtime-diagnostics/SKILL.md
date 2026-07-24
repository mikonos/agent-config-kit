---
name: claude-runtime-diagnostics
description: Diagnose Claude Code installation, upgrade, plugin visibility, skill versus slash-command surfaces, config activation, session recovery, transcript lookup, and runtime capability mismatches. Use when Claude is upgraded, plugins are installed but not visible, a new session still cannot use a feature, settings changes seem ineffective, or an abruptly closed Claude session needs recovery.
---

# Claude Runtime Diagnostics

## Core Rule

Do not treat `installed` as `usable`. Diagnose the actual runtime surface: binary, version, plugin install state, plugin capability type, config scope, session startup boundary, and transcript path.

## Workflow

1. Identify the target surface.
   - Claude Code binary/version
   - plugin marketplace/install state
   - skill visibility
   - slash command visibility
   - config behavior
   - session recovery
   - Codex vs Claude Code mismatch

2. Verify the binary and channel.
   - Locate `claude`.
   - Check `claude --version`.
   - Use the official updater path for upgrades.
   - Report `already current` as a valid outcome when updater and version agree.

3. Diagnose plugin visibility.
   - Use plugin list to prove install/enabled state.
   - Use plugin details to determine whether a capability is a skill, slash command, or another surface.
   - Test in a normal fresh Claude Code session when startup mode may hide capabilities.
   - Remember: installing in `~/.claude` affects Claude Code, not Codex.

4. Diagnose config changes.
   - Check the correct config file and scope before editing.
   - Verify with a structured reader such as `jq` when possible.
   - State whether the change applies immediately or only after restart/new session.

5. Recover sessions.
   - Locate transcript directories under `~/.claude/projects/`.
   - Narrow candidates by mtime, size, and real user prompts parsed from JSONL.
   - Resume with `claude --resume` or `claude --resume <session-id>`.
   - Do not reconstruct manually until transcript recovery has failed.

## Failure Guards

- Do not say a plugin should work just because it is installed.
- Do not assume a Codex-visible tool exists because a Claude plugin exists.
- Do not identify sessions by grep alone when multiple large JSONL files match.
- Do not claim a config setting changed current-session behavior unless the activation boundary was verified.
