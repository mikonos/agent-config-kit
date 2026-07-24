---
name: project-launch-report
description: 生成并发送 project GitHub issue 产品上线状态简报。适用于 issue 上线风险盘点、open/closed 趋势、飞书产品开发群同步、自动化发送（关键词：project issue 上线 飞书 产品开发 自动化）
metadata:
  routing:
    requirePromptTriggers: true
    requireFileTriggers: true
    requireDescriptionRouting: true
---

# project Issue Launch Report

## Purpose

Turn `sunsetyyun/project` GitHub issues into a product-launch risk report, then optionally send it to the Feishu/Lark group `产品开发`.

Default report lens:

- Product outcome, not issue bookkeeping.
- Launch blockers first: open `P0`, then open `P1`.
- Separate `待验收` from `待确认`.
- Plot recent issue flow as daily opened/closed/open-backlog data.

## Dependencies

Required local commands:

- `gh`, authenticated to GitHub and able to read `sunsetyyun/project`.
- `lark-cli`, configured with a bot that can see and send to the target group.
- `python3`.

In this AI-Zettelkasten workspace, run shell commands with `rtk`.

## Quick Workflow

1. Generate the Feishu-ready report:

   ```bash
   rtk python3 .cursor/skills/project-launch-report/scripts/project_issue_launch_report.py \
     --repo sunsetyyun/project \
     --days 9 \
     --format feishu
   ```

2. Find the target Feishu group by name, not by hard-coded `chat_id`:

   ```bash
   rtk lark-cli im +chat-search --query "产品开发" --chat-modes group --page-size 10 --format json --as bot
   ```

3. Send the generated Markdown:

   ```bash
   rtk lark-cli im +messages-send \
     --chat-id <oc_xxx> \
     --markdown "$REPORT" \
     --as bot \
     --idempotency-key "project-issue-launch-$(date +%Y%m%d)"
   ```

4. Verify the send result contains `ok: true`, `message_id`, `chat_id`, and `create_time`.

## Automation Mode

Read `references/automation.md` before creating or running a scheduled automation.

Automation mode may send without a per-run confirmation only when all of these are true:

- The user has explicitly approved the fixed recipient: Feishu group `产品开发`.
- The user has explicitly approved the fixed sender identity: `bot`.
- The message content is generated only by this skill's deterministic report script from GitHub issue data.
- The automation prompt states the no-confirmation boundary.
- The command searches the group by name at runtime and refuses to send if search result is not exactly one normal group named `产品开发`.

If any parameter is changed by a human prompt at runtime, fall back to interactive confirmation before sending.

## Report Interpretation

Use Marty Cagan's launch-risk lens:

- Closed count is not launch confidence by itself.
- `待验收` means possible risk reduction, not done.
- `待确认` means product judgment is still pending.
- P0 open issues are release blockers unless the user explicitly declares them out of scope.
- P1 bugs in 首页、任务GTD、日历、对话Agent usually affect launch confidence more than P2 copy or research items.

## Failure Handling

- If `gh` fails: report GitHub auth/repo access as blocked; do not send stale data.
- If group search returns zero or multiple matches: do not send; ask for target clarification.
- If `lark-cli` returns missing bot scope: surface the missing scope and console URL/hint.
- If `lark-cli` returns an update notice, finish the user request first, then mention the update.

## Verification Checklist

- [ ] Script generated current issue totals from GitHub, not copied from chat history.
- [ ] Open/closed daily trend uses the intended timezone.
- [ ] P0/P1 open issues are visible in the report.
- [ ] Feishu group resolved by name at runtime.
- [ ] Send result returned `ok: true`.
