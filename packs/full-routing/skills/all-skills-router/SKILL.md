---
name: all-skills-router
description: Route plain-language requests across the complete Agent Config Kit catalog when the full profile is installed. Use when the exact Skill is not already obvious, the Runtime may have omitted a Skill from its initial context list, or the user asks what workflow can help; search the bundled index, choose one Skill, then load its sibling SKILL.md.
---

# All Skills Router

Use the complete local Catalog without asking the user to learn Skill names.
The Runtime may omit some installed Skills from its initial context list, so
directory installation alone is not discovery evidence.

## Route

1. Extract two to five outcome or domain keywords from the request.
2. Use local read-only search or filtering on `references/skill-index.json`.
   Return at most five matching records into context. Do not load or print the
   entire index; if the first search is weak, try one narrower synonym set.
3. Match the user's concrete outcome against those indexed descriptions.
4. Choose the smallest single Skill that covers the task. Use a second Skill
   only when the work has a separate, necessary phase.
5. Resolve the recorded `sibling_skill_path` from this Skill directory—the
   directory containing this `SKILL.md`, not the `references/` directory. Read
   the selected Skill's `SKILL.md`, then follow those instructions. Do not
   substitute the index summary for the selected Skill body.
6. If the selected file is unavailable, report that the Skill is installed but
   not verified in use; do not improvise its instructions.

Use only local read access while routing. Do not search the web, install
anything, or perform the selected Skill's side effects merely to prove that it
can be found. The selected Skill and the user's authorization determine what
may happen after routing.
