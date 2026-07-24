---
name: network-maintenance
description: Knowledge network health check and structural maintenance. Use to handle orphans/weak links in bulk, identify hubs/bridges, and propose a prioritized maintenance plan.
---

# Network Maintenance

## Goal
Keep the knowledge graph healthy: reduce orphans, increase meaningful connectivity, and create bridges between clusters.

## Quick start
- Define scope: directories + time window (e.g. last 30/90 days).
- Diagnose first, prescribe second: deliver only the top 3–5 structural issues and a task list.

## Workflow

### Step 1: Scan
- Count notes / links
- Identify hubs and clusters
- Identify outliers (orphans, weak links)

### Step 2: Diagnose
Example thresholds:
- Orphan rate: <5% excellent / 5–10% good / 10–20% ok / >20% bad
- Avg degree: >3 excellent / 2–3 good / 1–2 ok / <1 bad

### Step 3: Identify issues
- Orphans (0 links)
- Weak links (<2 links)
- One-way links
- Cluster isolation (no bridges)
- Tag/label inconsistency (if you use tags)

### Step 4: Prescribe
Prioritize:
1. Bridge work (cluster-to-cluster)
2. Orphan rescue (high value notes first)
3. Index creation / consolidation

## Output template

```markdown
## 🔧 Network Maintenance Report

### Snapshot
- **Total notes**: [N]
- **Total links**: [N]
- **Orphans**: [N] ([%])

### Health score: [0-100]

### 🚨 Top issues (prioritized)
1. **[Issue type]**: [what] → [why it matters] → [fix]

### 📋 Task list
- [ ] [Task 1]
- [ ] [Task 2]
```

## Quality checks
- [ ] Metrics → diagnosis → tasks align 1:1
- [ ] Tasks are concrete (which notes, what links)
- [ ] Priorities are explicit

