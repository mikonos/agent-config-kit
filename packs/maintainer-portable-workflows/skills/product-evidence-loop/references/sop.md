# product / 515 Demand And Evidence Loop SOP

## Purpose

The loop makes product product judgment repeatable without outsourcing judgment to AI.

It answers one question:

> Should this input become a bounded product product action, or should it stay as evidence, backlog, shelf, or no-go?

## Operating Model

```text
input
  -> classify
  -> read minimum truth set
  -> build evidence packet
  -> apply four gates
  -> decide go / defer / kill / needs evidence
  -> if validated, update canonical truth
  -> write ReviewTrace after test
```

## Minimum Truth Set

Read index-level truth before drilling down:

- `03_索引/索引_AI_Family_Hub.md`
- `03_索引/目标项目相关/索引_代号515_需求与验收.md`
- `03_索引/索引_AI原生组织_Agent运转层.md`
- `03_索引/索引_AI产品判断力与流程反转.md`
- `05_每日记录/2026/07/20260706/20260706_product三条落地策略_组织产品个人.md`

When working on onboarding / Pre-flight, also inspect:

- `05_每日记录/2026/06/20260626/20260626_product_Onboarding_deep-reading/20260626_方法_product首启5分钟Aha设计SOP.md`

## Weekly Cadence

| Time | Meeting | Purpose | Output |
|---|---|---|---|
| Monday 30 min | Demand intake | Decide which inputs deserve evidence packets | Packet queue |
| Wednesday 60 min | Evidence gate | Review 3-5 packets | go / defer / kill / needs evidence |
| Friday 45 min | Learning review | Review failures, missing sources, wrong gates | One changed rule, template, index pointer, or SOP |

No status-only meeting. If the session cannot change a decision, gate, or reusable constraint, it is not part of this loop.

## First 5 Candidate Packets

Start with:

1. Tomorrow / Departure Pre-flight.
2. Family calendar parsing layer.
3. Trusted object chain: source / confidence / unknown / undo / audit.
4. Minimal spouse/partner entry.
5. Today / departure check connection.

## Gate Definitions

### Evidence Gate

Pass only if the packet names a source path or a planned primary test.

Fail examples:

- "会议里大家觉得"
- "竞品有这个功能"
- "last30days 很多人讨论"
- "这个看起来很有用"

### Risk Gate

Pass only if the packet names the highest product risk.

Common product risks:

- Calendar sync or merge error.
- Fact/proposal/unknown confusion.
- AI invents owner.
- High-consequence missed preparation.
- Relationship harm from responsibility cards.
- Monitoring or scoring vibe.
- User sees one more system instead of less mental load.

### Acceptance Gate

Pass only if success and failure are observable.

Useful metrics:

- `first_trusted_chain_completed`
- `first_preflight_decision_completed`
- Aha rephrase: user can say "it thought of X for me"
- Day-2 return.
- 7-day Pre-flight completion.
- Non-default coordinator confirms one card.
- Main coordinator reports less retelling / chasing.

### Owner Gate

Pass only if one human owns judgment and one human or agent owns evidence gathering.

Agent can prepare packets and templates. Agent does not own product judgment.

## Decision Semantics

| Decision | Meaning | Next Action |
|---|---|---|
| `go` | Smallest next action is justified | Run bounded test or patch canonical truth |
| `defer` | Plausible but wrong timing / phase / dependency | Add shelf trigger or dependency |
| `kill` | Contradicts strategy or creates unacceptable risk | Record reason and no-go |
| `needs evidence` | Missing source, user problem, acceptance, or owner | Gather one specific source |

## Canonical Boundaries

- Aha is a candidate until behavior proves it.
- Pre-flight v1 is read-only unless user explicitly changes the experiment.
- Product truth belongs in the canonical product / requirement file, not in chat.
- Historical notes remain source material. Indexes should point; they should not become duplicate PRDs.
- Social heat is a signal, not proof.

## ReviewTrace Rule

After a test or decision cycle, write:

- What was tested.
- What evidence appeared.
- What failed.
- Which rule/template/index changed.
- Whether the item is now go, defer, kill, or needs evidence.

If nothing reusable changed, the loop has not learned yet.

