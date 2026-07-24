---
name: database-helper
description: Database design and query help. Use when working with SQL, schemas, or database architecture.
---

# Database Helper

## Quick start
- Clarify the goal: read / write / migrate / model, plus target DB engine (Postgres/MySQL/SQLite) and constraints.
- Prefer the safest change that is reversible (backfill + validate + switch + cleanup).
- Output must include: SQL (or migration steps), risk analysis, and a minimal test/rollback plan.

## Overview
Guidelines for database interactions and schema management.

## Core Principles

### 1. Schema Design
- Use snake_case for column names
- Every table must have a primary key
- Add indexes for foreign keys

### 2. Query Performance
- Avoid SELECT *
- Use EXPLAIN ANALYZE for complex queries
- Batch operations for large datasets

## Resources
- `resources/schema.md` - Current database schema structure (fill this per project)
- `resources/migration-guide.md` - How to create safe migrations (checklist + patterns)

## Quality checks
- [ ] No destructive migration without a rollback path
- [ ] For large tables: batched backfill, online-safe strategy, and expected runtime
- [ ] Query changes include: index plan, EXPLAIN/EXPLAIN ANALYZE guidance, and worst-case notes
