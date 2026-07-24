---
name: chanlun-trading
description: Analyze A-share, HK-stock, ETF, index, or futures technical走势 using 缠论/缠中说禅 structure concepts. Use when the user asks about 中枢, 级别, 分型, 笔, 线段, 背驰, 区间套, 三类买卖点, 持股/持币, 技术面复盘, K-line chart reading, or converting Chan theory into reproducible backtest proxy rules. Research and study only; never provide investment advice, direct buy/sell instructions, or return promises. Routing: for Chan theory explanation, original-text verification (原文考据), 缠中说禅 persona/thinking simulation, market philosophy, or Chanlun critiques without a concrete chart to audit, yield to chanzhongshuochan-perspective; this skill is for structural audit of actual charts/data.
---

# Chanlun Trading

Use this skill to turn 缠论 analysis into a disciplined, reviewable workflow: define level, identify structure, map possible signals, state invalidation, and downgrade when data is insufficient.

This skill is for technical research and learning only. Do not recommend trades, promise returns, or tell the user what to buy or sell.

## Operating Modes

Declare one mode before giving any operational conclusion:

- `strict_chanlun`: Use only when the provided chart/data is enough to inspect inclusion handling, fractals, strokes, segments, same-level centers, divergence, and lower-level trigger.
- `structure_proxy`: Use when K-line inclusion, fractals, strokes, and center-like overlap can be approximated, but segments or trend types are simplified.
- `proxy_research`: Use when only partial chart, daily bars, swing data, or indicators are available. State the approximation loss explicitly.

Default to a strict audit first. If any required gate cannot pass, name the missing structure and downgrade to `structure_proxy`, `proxy_research`, or `observe`.

## Non-Negotiable Rules

- Define `review_level`, `trade_level`, `confirm_level`, and `trigger_level` before discussing signals.
- Separate definition modes: `original_definition`, `segment_proxy`, `swing_proxy`, `kline_proxy`, `indicator_proxy`.
- Analyze in this order: trend type -> level -> center -> divergence/strength -> buy/sell-point candidate -> filters.
- Do not treat small-level divergence as a large-level reversal unless the small-to-large condition is checked.
- Do not define Chanlun buy/sell points with MACD, RSI, volume, moving averages, trend lines, chips, or capital flow. These are filters only.
- If chart detail is insufficient, say what is missing and downgrade. Never pretend to see structure that is not provided.
- State invalidation before discussing potential upside.
- Use conditional research labels, not direct trade instructions.

## Strict Audit Gates

Run these gates before mapping a signal:

1. `level_gate`: Name `review_level / trade_level / confirm_level / trigger_level`.
2. `structure_gate`: Build or cite the chain `inclusion -> fractal -> stroke -> segment -> center`.
3. `type_gate`: Classify the same-level state as trend, consolidation, center extension, center breakout, transition, or unclear.
4. `comparison_gate`: For divergence, name the two same-direction, same-level movements being compared.
5. `buy_sell_gate`: Map to first/second/third buy or sell candidate only after the prior gates pass.
6. `trigger_gate`: Require lower-level trigger, or mark `trigger_missing`.
7. `risk_gate`: State invalidation and next observation point.
8. `downgrade_gate`: If any gate fails, output `observe` or proxy mode rather than a confirmed signal.

Forbidden shortcuts:

- indicator divergence -> first buy
- breakout without pullback test -> third buy
- higher low without first-buy context -> second buy
- 30m moving average/MACD state -> 30m Chanlun structure
- daily signal plus 30m indicator confirmation -> strict multi-level Chanlun signal

## Workflow

1. Confirm the target, market, available data, user objective, and holding horizon.
2. Set the level stack. Common defaults: medium-term `weekly/daily/30m`, swing `daily/30m/5m`, short-term `30m/5m/1m`.
3. If an image is provided, read the chart first; do not rely on surrounding text before visual structure.
4. Identify the latest valid center and its `zg/zd` boundaries.
5. Classify current state: `center_oscillation`, `center_extension`, `center_breakout`, `uptrend`, `downtrend`, `transition`, `first_buy_candidate`, `second_buy_candidate`, `third_buy_candidate`, sell-side mirror, or `untradable_unclear`.
6. Map candidate signals only after the strict gates pass.
7. Add filters after structural classification only.
8. Output a concise self-check: what would prove this reading wrong?

## Reference Routing

Read only the reference needed for the task:

- `references/concepts.md`: definitions, source levels, terms, and state taxonomy.
- `references/strict-original-system.md`: strict/proxy downgrade matrix and audit contract.
- `references/structure-engine.md`: inclusion, fractal, stroke, segment, center, extension, expansion.
- `references/visual-reading.md`: screenshot, book chart, or hand-drawn chart reading.
- `references/buy-sell-playbooks.md`: first/second/third buy-sell candidates and false-positive checks.
- `references/multi-level-recursion.md`: interval nesting, small-to-large transition, and level conflict.
- `references/filters.md`: MACD, RSI, trend lines, moving averages, chips, and sector strength as filters.
- `references/volume-turnover-money.md`: volume, turnover, and capital-flow matching rules.
- `references/invalidation-risk.md`: invalidation, stop logic, position discussion boundaries, hold/reduce logic.
- `references/backtest-proxies.md`: reproducible proxy rules and required output columns for backtests.
- `references/self-test-cases.md`: common false positives and reusable test prompts.
- `references/full-general-ai.md`: standalone full prompt for non-Codex AI tools or when the user wants exportable usage text.
- `references/original-skill.md`: legacy source wording from the original package.
- `references/original-quickstart.md`: original user-facing quickstart.
- `references/original-readme.md`: original package README and design notes.

For current-market analysis, use user-provided charts/data when possible. If using external market data, state the data source and timestamp.

## Output Template

```markdown
**级别**
- review_level:
- trade_level:
- confirm_level:
- trigger_level:
- definition_mode:
- structure_completeness:
- approximation_loss:

**结构**
- current_state:
- latest_center:
- zg / zd:
- trend_or_oscillation:
- compared_movements:

**信号**
- candidate:
- divergence:
- confirmation:
- lower_level_trigger:

**失效与观察**
- research_label:
- basis:
- invalidation:
- next_watch:
- what_would_change_my_mind:
```
