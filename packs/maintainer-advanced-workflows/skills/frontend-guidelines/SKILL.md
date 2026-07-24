---
name: frontend-guidelines
description: Frontend development guidelines and best practices. Use when following coding standards for web UI.
---

# Frontend Development Guidelines

## Quick start
- Confirm stack assumptions: React version, router, state management, styling (CSS Modules / Tailwind), and UI library.
- **Visual contract**: If the repo (or app subfolder) has a root **`DESIGN.md`** in the [Google Stitch / VoltAgent awesome-design-md](https://github.com/VoltAgent/awesome-design-md) style (theme, tokens, typography, components, layout, elevation, responsive, do/don'ts, agent prompt guide), **read it before** implementing UI and treat it as the single source of truth for look-and-feel. Do not contradict it without an explicit user decision. A project Agent Rule is not necessarily a UI design document.
- Prefer accessibility + responsiveness by default; ship the smallest correct component first, then iterate.
- Output must include: component API (props), state/data flow, and a minimal test plan (or manual QA checklist).

## Overview
Core standards for frontend development using React and TypeScript.

## Core Principles

### 1. Component Structure
- Use functional components with hooks
- Props interface must be exported
- detailed logic should be extracted to custom hooks

### 2. Styling
- Use CSS Modules or Tailwind (project dependent)
- Avoid inline styles
- Ensure responsive design (Mobile First)

## Resources
- `resources/react-patterns.md` - Practical React patterns (when to use / avoid)
- `resources/styling-guide.md` - Styling checklist (a11y, responsive, consistency)
- `resources/awesome-design-md.md` - **Reference**: VoltAgent curated Stitch-style `DESIGN.md` collection (GitHub / getdesign.md), usage boundaries versus the project's own `DESIGN.md` and product tokens, plus an optional `git clone` path

## Quality checks
- [ ] Keyboard accessible (focus order, Enter/Space actions where applicable)
- [ ] Mobile-first layout works and no horizontal scroll
- [ ] Component props are typed and exported; side effects are isolated (hooks)
