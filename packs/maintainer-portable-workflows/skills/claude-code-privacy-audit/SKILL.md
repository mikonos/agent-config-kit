---
name: claude-code-privacy-audit
description: >-
  Read-only Claude Code privacy audit and documented privacy-control guidance.
  Use when the user asks about telemetry, error reporting, feedback commands,
  nonessential network traffic, local settings, privacy review, or account
  suspension. Never use it to evade enforcement, unlink identities, reset
  device identifiers, inspect credential contents, or delete credentials.
---

# Claude Code privacy audit

Use this Skill to distinguish three questions:

1. Which documented privacy controls are configured?
2. What would change if the user enabled or disabled one of them?
3. Does an account problem require official support rather than a local change?

## Safety boundary

- Start read-only. Do not modify settings until the user sees the exact diff and
  explicitly confirms it.
- Do not read, print, copy, export, or summarize credential values, account
  tokens, session identifiers, device identifiers, or private conversation
  content.
- Do not delete credentials, caches, telemetry files, or local account state.
- Do not reset identifiers, disguise account continuity, or help a suspended
  user bypass platform enforcement. Direct account-status disputes to
  Anthropic's official support or appeal route.
- Do not claim that a control blocks all product traffic. Report only the
  behavior documented for that control.

## Read-only audit

1. Confirm the Claude Code version if the command is available.
2. Locate the active user and project settings using current Claude Code
   documentation. Do not assume a path when the runtime reports a different
   location.
3. Inspect only whether these documented environment controls are present and
   whether their value is `1`:

   - `DISABLE_TELEMETRY`
   - `DISABLE_ERROR_REPORTING`
   - `DISABLE_BUG_COMMAND`
   - `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC`

4. Report each control as `enabled`, `disabled`, or `not found`. Do not print
   unrelated environment variables or any value that could be a secret.
5. State the evidence boundary: this verifies local configuration, not what a
   remote service has retained or whether an account is in good standing.

## Change workflow

When the user asks to change a control:

1. Recheck Anthropic's current official data-usage documentation.
2. Show the exact settings file and minimal JSON diff.
3. Explain the documented effect and the main tradeoff.
4. Wait for explicit confirmation.
5. Apply only that diff, preserve unrelated settings, and parse the resulting
   JSON.
6. Ask the user to restart Claude Code if the documented control requires a new
   process, then rerun the read-only audit.

Example diff shape:

```json
{
  "env": {
    "DISABLE_TELEMETRY": "1"
  }
}
```

This is an example, not authorization to write. If the settings file already
contains an `env` object, merge the selected key without replacing other keys.

## Account suspension

If the user says an account was blocked or suspended:

- help collect non-sensitive facts such as the visible error message, product
  version, time, and official case number;
- recommend the official support or appeal process;
- do not suggest new-account creation, identifier changes, credential deletion,
  cache deletion, or any method intended to avoid account linkage.

## Source

Current behavior must be checked against Anthropic's official Claude Code data
usage documentation:
`https://docs.anthropic.com/en/docs/claude-code/data-usage`.
