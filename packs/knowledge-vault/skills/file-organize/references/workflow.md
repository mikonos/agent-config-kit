# File Organize Workflow (detailed)

## Goal
Given a file/note, output:
- the most precise target path (as specific as your taxonomy allows)
- **≥2** meaningful links
- correct type judgement (literature note / permanent note / project doc / raw material, etc.)

---

## Step 1: Decide note type → target folder

| Type | Target folder (example) | Heuristic |
|---|---|---|
| Fleeting idea | `Inbox/` | seed, not yet distilled |
| Permanent note | `Notes/` (+ taxonomy) | distilled own thinking |
| Literature note | `Literature/` (+ taxonomy) | keeps source metadata |
| Index / MOC | `Index/` | navigation entry |
| Raw materials | `Archive/` | PDFs, screenshots, originals |
| Project docs | `Workspace/projects/` | active project material |
| People docs | `Workspace/people/` | person-specific |
| Tasks | `Tasks/` | actionable TODOs |
| Logs | `Logs/` | weekly reports / logs |
| System config | `[_system/ or your system directory]` | **never** working docs |

---

## Step 2: Pick a taxonomy (optional)
If you use a classification system (e.g., DDC), pick the closest domain.

---

## Step 3: Quality checks (must pass)
- Path precision: as specific as possible
- Link health: ≥2 links (different types preferred)
- Type correctness: literature vs permanent vs project vs raw

---

## Special handling
- If the user explicitly requests a path, follow it; use links/indexes to improve discovery later.
- For cross-domain content: pick one “home”, and link from other entry points (do not duplicate content).

