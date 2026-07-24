---
name: truth-source-governance
description: Resolve source-of-truth and canonical artifact boundaries across overlapping docs, notes, PRDs, meeting notes, briefs, action plans, AGENTS/CLAUDE mirrors, GTM docs, ZK cards, and indexes. Use when the user asks which file should own a decision, when duplicate docs drift, when historical notes should point to execution docs, or before editing governance-heavy documentation.
---

# Truth Source Governance

## Core Rule

Give the plain answer first: `live truth belongs in X; Y is historical/source material; Z is an index or pointer`.

Do not decide from memory alone. Inspect the live files, indexes, manifests, changelogs, and routing targets before changing or declaring the canonical source.

## Workflow

1. Identify the artifact roles.
   - Historical source: meeting notes, old audits, raw discussion, backups.
   - Execution truth: action plan, live PRD/card, manifest item, current SOP.
   - Framing card: brief, manifesto, positioning note, future-PR draft.
   - Index/pointer: MOC, design hub, old entrypoint, README.
   - Runtime mirror: Runtime-specific Rule files and generated mirrors.

2. Read the minimum live set.
   - For overlapping docs: read all contenders and their inbound pointers.
   - For PRD/card disputes: read index/manifest, live card, changelog, source note.
   - For protocol drift: read the truth source and the generated/projected mirrors.

3. Choose one canonical owner.
   - If the user named the owner, respect it unless live evidence makes it impossible.
   - If one doc is denser but marked historical, move operative detail into the execution truth before demoting it.
   - If an old doc is still a useful entrypoint, preserve it as a pointer instead of deleting it.
   - If a backup exists, keep it as rollback/reference only; never let it re-enter the live truth chain.

4. Patch surgically.
   - Put each fact in the file that owns that type of truth.
   - Replace duplicate live claims with explicit pointers.
   - Preserve intentional role splits once the user has set them.
   - Avoid broad rewrites unless stale wording would keep the old truth alive.

5. Verify.
   - Search for old dates, old labels, duplicate milestones, outdated freeze gates, and obsolete source-owner claims.
   - Check that canonical docs and pointer docs agree.
   - Confirm no doc now claims a broader ownership scope than intended.
   - Report the files changed and the checks run.

## Failure Guards

- If the proposed execution truth is thinner than the source note, absorb the missing operating detail first.
- If the task is correction/governance-heavy, use an independent audit or subagent when available.
- If the workspace has generated mirrors, update the truth source first, regenerate/check mirrors, and do not hand-edit all layers into drift.
- If unsure whether the user means a structure note, source pool, candidate card, manifest PRD, or released truth, state the inferred artifact class before editing.
