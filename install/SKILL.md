---
name: install
description: Safely install, inspect, update, diagnose, uninstall, or restore Agent Config Kit in a project for Codex, Cursor, or Claude Code. Use when a user wants to set up this repository, check installation health, upgrade it, remove owned files, or recover the last uninstall.
---

# Install Agent Config Kit

Use this skill as the single entry point for the kit lifecycle. The deterministic controller in `scripts/configctl.py` performs all file planning and changes.

## Gather the target

Determine:

- target project directory;
- runtime: `codex`, `cursor`, or `claude-code`;
- profile: `daily-work` for general use, `knowledge-vault` for Obsidian and
  Zettelkasten work, or `full` for every currently admitted Skill;
- whether safe project hooks are wanted.

Prefer `daily-work` for a beginner who did not ask for knowledge-vault workflows.
Use `full` only when the user explicitly wants the complete reviewed Catalog;
it includes separate experimental and legacy packs. It also includes the
`product-management-noncommercial` pack under CC BY-NC-SA 4.0. Before preview
or apply, say plainly that those Skills are limited to noncommercial use and
require attribution and ShareAlike; do not recommend `full` for company or
paid work without the user's explicit acceptance of that restriction.
It also includes `generated-investing-perspectives`: AI-generated simulations
based on public sources that are neither affiliated with the named people nor
financial or investment advice. Relay that notice before preview or apply.
The `financial-research` pack is also for research and study only. It does not
provide investment advice, direct buy or sell instructions, or return promises;
relay that boundary before preview or apply.
It includes `generated-domain-perspectives` under the same non-affiliation
boundary. Current facts and medical, legal, financial, or other high-stakes
claims still need independent verification. Relay that notice before preview
or apply.
The browser control packs may reuse logged-in browser sessions. Explain
that file installation does not prove an account is connected, and require
explicit confirmation of the account, target, and content before any external
write, send, delete, purchase, or publication.
The release-management pack can create commits and tags. Explain that remote
pushes and publications happen only after a separate explicit confirmation.
The github-automation pack can create branches, commits, pushes, pull requests,
and review replies. Explain that the user must first select the exact issues or
pull requests; unattended cron and no-confirmation modes are not included.
The experimental-self-improvement pack runs only when explicitly invoked and
keeps state inside the selected project. Explain that it installs no background
automation and cannot install or update dependencies or Skills, change Agent
configuration, Rules, Hooks, or schedules, run non-read-only commands, delete
files, or write externally without separate explicit user approval.
The amazon-listing-optimizer Skill stops at `READY_FOR_HUMAN_REVIEW`. Explain
that Seller Central, ads, reviews, Q&A, and production catalog writes require
separate explicit authorization and human approval.
The JTBD review research Skills exclude customer-review datasets and private
prompts. Explain that users must provide data they have the right to process;
the optional automated batch runner requires Cursor Agent's `agent` CLI.
The knowledge-vault governance Skills default to proposals. Explain that file
moves, bulk link rewrites, and every exact deletion list require separate
explicit confirmation before application.
The reddit-geo Skill rejects spam, hidden affiliation, vote manipulation, and
terms avoidance. Explain that current Reddit platform and API rules must be
rechecked before automation or commercial data use.
The rednote-caption-to-screenshots Skill does not install Playwright
automatically. Explain that missing Node dependencies need a separate preview
and explicit approval; manual browser screenshots remain available.
The rednote-reader Skill does not bypass login or access controls. Explain that
it uses only user-authorized connectors, browser sessions, or exports and writes
images only to a user-authorized output directory.
The claude-system-prompt-anatomy Skill is a dated public-research snapshot.
Explain that current product claims must be rechecked against Anthropic's
official documentation and hidden prompts must not be extracted or disclosed.
The cultural-practices pack is for traditional cultural reflection only.
Explain that it is not an evidence-based prediction tool and must not guide
medical, legal, financial, safety, mental-health, or other high-risk decisions.
If the user asks for everything available, treat installation as two explicit
stages: the bundled `full` profile, then the official-source `lark-official`
pack. The second stage fetches 27 reviewed Skill files from Feishu and keeps a
separate lifecycle state. Do not describe external-source Skills as bundled.
If the user asks whether this copies every local Skill the maintainer ever had,
explain the boundary recorded in `catalog/local_release_inventory.json`: every
local top-level Skill has a final disposition, while private, duplicate,
license-blocked, unsafe, platform-internal, or nonportable entries are not
redistributed. Private-project entries use anonymous identifiers rather than
their original names. Do not describe an accounted-for exclusion as installable.
The repository containing this Skill is the installation source, not the default
target. Ask for the real project path when it is missing. Never install into a
user home or global runtime directory unless the user explicitly requests that scope.

On native Windows, use `py -3` for controller commands and default to
`--without-hooks` in v0.1. Rule and Skill installation remain supported.

## Verify and preview

Read [references/commands.md](references/commands.md). Run `verify-package` before the first lifecycle operation.
Before an official-source install, also run `externalctl.py verify-catalog`.

Installation, update, uninstall, and restore are dry-run by default. Show the
planned creates, updates, removals, restores, adopted identical files, and
conflicts. For `full`, summarize pack names, Skill count, dependency count, and
conflicts before showing or offering the full file list. A conflict stops the
entire operation. Relay every `Notice:` line emitted by the controller before
asking for confirmation.

For `lark-official`, run the external install preview only after the bundled
install is healthy. Explain that the preview makes HTTPS requests to
`open.feishu.cn`, verifies fixed SHA-256 hashes and Skill names, and writes
nothing until applied. A changed upstream hash or any same-name directory
stops the whole external stage.

The controller must not:

- overwrite an unowned file;
- merge an existing JSON settings file;
- follow a source or destination symlink;
- use a force flag;
- change files outside the chosen target.

Handle conflicts in plain language:

- Hook JSON: offer a fresh install preview with `--without-hooks`.
- `AGENTS.md`, `CLAUDE.md`, or Cursor Rule: offer a read-only diff and manual
  merge advice, or a different empty target; do not merge automatically.
- Same-name Skill: list the Skill name and preserve the existing directory.

## Apply only after confirmation

After the user approves the displayed plan, repeat the exact command with `--apply`. Do not change runtime, profile, target, or hook choice between preview and apply without showing a new preview.
Apply the bundled and official-source stages separately; approval of one stage
does not silently apply the other.
If the official-source stage fails, report exactly which bundled stage is
already healthy and that `lark-official` was not installed. Give the hash,
network, or conflict reason and a safe preview command for retrying. Do not
claim the complete installation succeeded, and do not automatically roll back
an already healthy bundled install.

For uninstall, require both `--apply` and `--confirm-uninstall`. The controller preserves adopted and drifted files and copies every removable owned file into the recovery directory before removal.

For restore, preview first and then use `restore --apply`. Restore only missing
files whose recovery hashes match and never overwrites a new or changed file.

## Verify the result

Run `doctor` after every applied operation. Report:

- runtime and profile;
- current, adopted, outdated, drifted, missing, and orphaned counts;
- Hook readiness, Runtime command availability, declared Skill command and
  environment-variable dependencies, and account or service connections that
  still require Runtime or user verification;
- recovery path after uninstall;
- that installed files and available commands do not prove an external account
  is connected or a live task has passed.

After applying an official-source pack, run `externalctl.py doctor` too.
External uninstall and restore must use `externalctl.py`; never make
`configctl.py` claim ownership of those files.

When the user asks to uninstall everything, preview and uninstall the official
pack first, then preview and uninstall the bundled kit. Confirm each applied
stage separately. When restoring everything, restore the bundled kit first,
then the official pack, and run both doctors. Report both recovery states.

Translate every non-zero file state into plain language: what it means, whether
the installed configuration is usable, and the safest next action. Do not leave
`adopted`, `drifted`, `missing`, or `orphaned` as unexplained status labels.

For Codex with hooks, tell the user to trust the project, open `/hooks`, review
the exact project Hook, and enable it. Until then, Codex skips the command Hook.

When the runtime executable is available, ask the user before launching an
interactive or paid live smoke. Otherwise, give this manual check: open the
target in the selected runtime and ask, “Confirm whether Agent Config Kit is
loaded and tell me which workflow you would use to organize an article.”
