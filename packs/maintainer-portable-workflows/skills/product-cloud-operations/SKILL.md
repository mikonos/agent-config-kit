---
name: product-cloud-operations
description: Use when debugging, validating, or operating product Cloud through product-cli, including login status, family and Hub routing, calendar sync, external artifacts, deployment smoke checks, and Cloud API schema/API fallback calls.
---

# product Cloud

Use `product-cli` for product Cloud checks and operations.

## Required Flow

1. Start with:
   ```bash
   product-cli doctor --format json
   ```
2. Then check login state:
   ```bash
   product-cli status --format json
   ```
3. Prefer typed commands:
   ```bash
   product-cli family list --format json
   product-cli hub route --format json
   product-cli calendar accounts --format json
   product-cli calendar events list --from <yyyy-mm-dd> --to <yyyy-mm-dd> --format json
   product-cli chat sessions list --format json
   product-cli chat proactive recent --format json
   product-cli tasks list --status open --format json
   product-cli projects list --status active --format json
   product-cli waiting-for list --status open --format json
   product-cli external artifacts --status all --format json
   ```
4. Before using an unfamiliar Cloud API, inspect schema:
   ```bash
   product-cli schema show <domain.method> --format json
   ```
5. Use `product-cli api` only when there is no typed command.

## Full Smoke

For a full authenticated CLI check after code changes:

```bash
npm test
npm run build
npm run smoke:cloud
```

`smoke:cloud` creates temporary `product-cli-smoke` calendar/task/project/waiting-for records in the current family and cleans them up. It checks Chat session/proactive read paths without calling the LLM by default; set `product_CLI_SMOKE_CHAT=1` for a real Agent Chat turn. If member-name inference fails, set `product_CLI_SMOKE_MEMBER=<member-name>`.

## Safety

- Never print access tokens, refresh tokens, captcha values, or Authorization headers.
- For delete, reset, migration, or high-impact write operations, explain the impact and get explicit user confirmation first.
- Use `--format json` for outputs that an agent will parse.
- If auth refresh fails, ask the user to run `product-cli login`; do not request their password.
