---
name: methodology-to-vault
description: Turn a method, theory, expert perspective, research topic, or long learning request into durable Zettelkasten assets. Use when the user asks for detailed research and learning, wants a method distilled into practice, asks whether a conclusion should become a note/skill/compiled wiki, or when a reusable methodology answer should not remain chat-only.
---

# Methodology To Vault

## Core Rule

If the result is reusable, propose the smallest durable vault artifact. Default
to a conversational draft; write files, links, or indexes only when the user
explicitly authorizes the target Vault and output objects.

## Choose The Output

- Structure note: use for a method, theory, or learning path that needs a reading sequence.
- Atomic notes: use for durable concepts, contrasts, and method rules extracted from a source.
- Method note/SOP: use when the value is a repeatable practice.
- Compiled wiki: use for a topic that needs a queryable synthesis layer over many notes.
- Perspective skill: use when a named thinker or expert method will be reused at least several times.

## Workflow

1. Pick the strongest brain for the method.
   - Use the domain expert first, then Luhmann/Feynman for learning and distillation.
   - If a perspective skill exists, activate or read it instead of freehand persona work.

2. Search the existing network first.
   - Read the current Vault's declared keyword table or index when choosing placement.
   - Use `rg` for exact strings, names, and very recent notes.

3. Gather sources.
   - Prefer official or primary sources for the method.
   - Add serious criticism or opposing implementations before declaring a method underspecified.
   - Keep local notes, secondary summaries, and user hypotheses clearly separated.

4. Write the vault artifact.
   - Use the current project's documented note location; ask when no convention exists.
   - Include required English YAML keys.
   - Preserve source boundaries and quote sparingly.
   - Build at least two useful links when possible; if the note is too new to have neighbors, state the temporary gap.

5. Wire it into the network.
   - Add or update the relevant index/MOC entry.
   - Suggest sparse keyword entries by answering: `when would I look for this?`
   - Add reciprocal pointers where the local convention requires it.

6. Ingest and verify.
   - Search for placeholder links, missing frontmatter, and stale paths before finishing.

## Failure Guards

- Do not turn every answer into a note. Use this skill when the method will be reused.
- Do not treat `llm-wiki` and Zettelkasten as the same layer: wiki compiles; ZK decides what deserves permanent entry.
- Do not declare a perspective skill better merely because it is longer; check trigger clarity, self-checks, and usage frequency constraints.
