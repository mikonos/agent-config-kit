---
name: qa-cases
description: Use this skill whenever the user needs test strategy, test plans, QA analysis, test cases, acceptance tests, edge cases, regression suites, checklist-style coverage, or mind-map style test cases for any product, feature, API, app, workflow, backend system, frontend UI, data pipeline, AI feature, or business process. Trigger this skill even if the user only says "写测试用例", "补测试", "测试策略", "验收用例", "边界条件", "回归测试", "QA", "帮我测一下这个需求", or provides a PRD/prototype/API doc and asks what to test.
---

# QA Cases

This skill turns requirements, prototypes, code changes, APIs, workflows, or product ideas into systematic test strategy and test cases.

Use a combined expert model:

- **Boris Beizer** for structural testing: equivalence classes, boundary values, decision tables, state transitions, pairwise/combinatorial coverage, and fault models.
- **Cem Kaner** for scenario testing: user harm, lawsuits/complaints, support tickets, business risk, and real-world workflows.
- **James Bach** for context-driven testing: risk-first sequencing, exploratory charters, product-specific tradeoffs, and testability.
- **Gerald Weinberg** for systems thinking: hidden coupling, feedback loops, human process failure, and observability.

The output should make the system easier to test, easier to discuss, and easier to trust.

## When You Start

First identify the work item type:

| Type | Examples |
| --- | --- |
| Product feature | New app page, user flow, settings, account feature |
| API/backend | Interface, job, service, permission, data sync |
| Frontend/UI | Form, modal, dashboard, editor, responsive UI |
| Business workflow | Approval, onboarding, payment, fulfillment |
| Data/analytics | ETL, metrics, reports, dashboards |
| AI feature | Prompt workflow, extraction, classification, generation |
| Incident fix | Bug fix, regression risk, hotfix |
| Campaign/event | Activity page, ranking, lottery, reward, notification |

Then identify inputs:

- Requirement/PRD.
- Prototype/screenshot/design.
- API documentation.
- Existing test cases.
- Code diff or implementation notes.
- Known production incidents.
- Success metrics and business constraints.

If inputs are incomplete, proceed with explicit assumptions and mark open questions. Do not block unless the missing information changes the expected result.

## Output Modes

Choose the mode that matches the user’s ask. If unclear, produce a concise strategy plus a first batch of executable cases.

### Mode A: Test Strategy

Use when the user asks how to organize testing.

Template:

```markdown
# [Feature] - 测试策略

## 1. 测试目标
## 2. 范围内 / 范围外
## 3. 风险分级
## 4. 测试分层
## 5. 测试数据
## 6. 测试钩子 / 可观测性
## 7. 执行节奏
## 8. 阻塞问题
```

### Mode B: Complete Executable Test Cases

Use when the user asks for “完整测试用例”, “可执行 TC”, or cases QA can run.

Each case should contain:

- 用例编号
- 模块
- 场景
- 前置条件
- 操作步骤
- 预期结果
- 优先级
- 备注 / 数据要求

Markdown table format:

```markdown
| ID | 模块 | 场景 | 前置条件 | 操作步骤 | 预期结果 | 优先级 |
| --- | --- | --- | --- | --- | --- | --- |
```

Mind-map format:

```xml
<node TEXT="TC-LOGIN-001 密码错误登录失败">
  <node TEXT="前置条件">
    <node TEXT="用户账号已注册"/>
  </node>
  <node TEXT="操作步骤">
    <node TEXT="1. 输入正确手机号"/>
    <node TEXT="2. 输入错误密码"/>
    <node TEXT="3. 点击登录"/>
  </node>
  <node TEXT="预期结果">
    <node TEXT="登录失败"/>
    <node TEXT="提示密码错误"/>
    <node TEXT="不创建登录态"/>
  </node>
</node>
```

### Mode C: Checkpoint Tree

Use when the user asks for mind-map style, high coverage, checklist, or “尽量多”.

Checkpoint trees are not full TC cases. They are granular assertion trees.

Example:

```text
登录
  手机号输入
    空值
    非数字
    少于11位
    多于11位
  密码输入
    空值
    错误密码
    锁定账号
  登录结果
    成功跳转
    失败提示
    登录态
    埋点
```

Use checkpoint trees to expose missing dimensions. Convert only the critical leaves into full TC cases when needed.

### Mode D: Review Existing Test Cases

Use when the user provides a test-case file and asks if it is complete.

Review in this order:

1. Requirement coverage.
2. Risk coverage.
3. Boundary values.
4. State transitions.
5. Negative/error cases.
6. Permissions/security.
7. Data integrity.
8. Observability/logs.
9. Regression scope.
10. Duplicates and dead cases.

Lead with missing risks and concrete gaps.

## Test Design Method

### Step 1: Model The System

Extract these dimensions:

| Dimension | Questions |
| --- | --- |
| Actor | Who uses it? Admin/user/guest/system/job/third party? |
| State | What states can the object/user/workflow be in? |
| Action | What can the actor do? |
| Input | What values, files, requests, events, or configs enter the system? |
| Output | What should the user/API/database/notification/log show? |
| Rule | What business rules decide the result? |
| Time | What changes before/during/after deadlines, retries, expiry, schedules? |
| Permission | Who can see, modify, approve, delete, export? |
| Failure | What happens on invalid input, timeout, duplicate request, partial failure? |
| Observability | How do we prove the result in logs/data/analytics? |

### Step 2: Rank Risk

Use this default severity model:

| Priority | Meaning |
| --- | --- |
| P0 | Money loss, data loss, privacy/security, irreversible action, legal/compliance, production outage |
| P1 | Broken core workflow, wrong permission, wrong calculation, bad state transition, hard-to-recover user harm |
| P2 | Important UI/UX, compatibility, content accuracy, non-core workflow |
| P3 | Cosmetic, rare edge, low-impact polish |

Write P0/P1 cases first.

### Step 3: Choose Test Techniques

Use several techniques, not one.

| Technique | Use For |
| --- | --- |
| Equivalence classes | Valid/invalid categories |
| Boundary value analysis | Numeric, date, count, length, money, quota |
| Decision table | Many rules decide one outcome |
| State transition | Workflows, approvals, binding, payment, lifecycle |
| Pairwise/combinatorial | Browser × role × state × config |
| CRUD matrix | Create/read/update/delete/import/export |
| Permission matrix | Role × object × action |
| Data integrity | Database, idempotency, reconciliation |
| Failure injection | Timeout, retry, duplicate request, rollback |
| Exploratory charters | Unknown risks, UX, integration behavior |

### Step 4: Build Test Data

For every major module, specify data needs:

- Normal user.
- Boundary user.
- Permission-limited user.
- Existing data / no data.
- Max-count data.
- Invalid/corrupt data.
- Time-sensitive data.
- Cross-tenant or cross-organization data.
- Backend logs or database rows needed for verification.

### Step 5: Add Observability

Good tests do not stop at “page looks right.” Add backend proof where risk justifies it:

- Database record.
- API response.
- Job log.
- Audit log.
- Notification log.
- Analytics event.
- Reconciliation report.
- Cost or inventory ledger.

If observability is missing, create a “test hook needed” section.

## Generic Coverage Checklist

### Functional Flow

- Happy path.
- Required fields.
- Optional fields.
- Empty state.
- Edit existing state.
- Delete/cancel/revoke.
- Duplicate operation.
- Refresh/reload.
- Back/forward navigation.
- Multi-tab or multi-device behavior.

### Input Validation

- Empty.
- Null.
- Whitespace.
- Min length.
- Max length.
- Special characters.
- Unicode/emoji.
- SQL/script-like strings.
- Invalid format.
- Very large input.
- File type/size if applicable.

### State And Lifecycle

- Initial state.
- In progress.
- Completed.
- Failed.
- Cancelled.
- Expired.
- Archived.
- Reopened.
- Retry.
- Rollback.

### Time

- Before start.
- Exact start.
- During.
- Exact end.
- After end.
- Expiry.
- Daily/monthly reset.
- Time zone.
- Daylight saving if relevant.
- Scheduled job delay.

### Permissions

- Guest.
- Normal user.
- Owner.
- Collaborator.
- Admin.
- Super admin.
- Cross-tenant access.
- Removed user.
- Suspended user.
- Token/session expired.

### Data Integrity

- Create record.
- Update record.
- Delete record.
- Duplicate submit.
- Concurrent update.
- Partial failure.
- Reconciliation.
- Idempotency.
- Event ordering.
- Pagination and sorting.

### UI/UX

- Loading.
- Empty.
- Error.
- Success.
- Disabled.
- Hover/focus if relevant.
- Responsive sizes.
- Long text.
- International text.
- Accessibility basics.

### Integration

- Third-party timeout.
- Third-party error.
- Retry.
- Callback duplicate.
- Callback out of order.
- Webhook signature.
- Notification delivery.
- External data mismatch.

### Regression

- Existing flows using same component.
- Existing APIs using same model.
- Old data migration.
- Feature flag off.
- Feature flag on.
- Rollback behavior.

## Domain Add-Ons

Read or use these add-ons only when relevant.

- For revenue/operations events, campaign pages, lottery pools, rankings, reward inventories, or cost controls, use `references/revenue-events.md`.
- For API/backend-heavy work, use `references/api-backend.md`.
- For UI/frontend-heavy work, use `references/frontend-ui.md`.
- For AI features, use `references/ai-features.md`.

## File And Validation Guidance

When creating files:

- Use `.md` for strategy or table cases.
- Use `.mm` for FreeMind-style mind maps.
- Validate `.mm` with XML parsing when possible.
- Report final counts:
  - TC count by prefix/module.
  - Node count.
  - Leaf count for checkpoint trees.
  - Known unresolved questions.

## Quality Bar

A strong test-case deliverable:

- Covers core flow, edge cases, negative cases, permissions, data integrity, and observability.
- Separates complete executable TC cases from high-density checkpoint trees.
- Prioritizes P0/P1 before exhaustive low-risk checks.
- Names exact values, exact states, and exact expected outputs.
- Calls out missing test hooks and unresolved product/backend questions.
- Is structured enough that another QA can execute it without asking what the case means.

Avoid:

- Only testing happy path.
- Vague expected results like “works normally.”
- Big cases that hide many assertions.
- Many duplicate low-value UI cases while missing state/data risks.
- Test cases with no way to verify backend result.
