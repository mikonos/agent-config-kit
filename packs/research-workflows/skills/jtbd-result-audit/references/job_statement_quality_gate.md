---
name: job-statement-quality-gate
type: reference
status: hard-rules
applies_to: jtbd / interview analysis / requirement cards / desk research
---

# Job Statement Quality Gate

Job Statement 是 raw evidence 到产品洞察之间的保真层。它不是访谈总结，也不是功能需求；它只还原一个人在一个具体情境下要完成的任务、遇到的限制、已经做过的补偿行为、当前方案，以及当前方案带来的痛点/愉悦点。

## 1. 九格 schema

每条 Job Statement 至少输出下列字段。缺证据时写 `缺证据`，不要补编。

| 字段 | 写法标准 | 证据要求 |
|---|---|---|
| `Context` | 有画面感：具体对象、状态、时间、数量、动作；不写抽象品类和评价词 | 原文直接支持；若来自评论/访谈，可附 quote/review_id/line_range |
| `Main Job` | 用户动作 + 对象 + 目标/时间；不写产品功能 | 必须是用户想做的事，不是产品应该有的能力 |
| `Desired Outcome` | 可感知、可衡量，可写 1-4 条成功标尺 | 若原文只有“方便/好用”，标 `待追问`，不能伪造数值 |
| `Constraints & Tensions` | 客观外部阻碍：时间、空间、工具、流程、角色、不可控条件 | 不写主观不喜欢；不写厂商专利、工程限制 |
| `Compensation Behavior` | 用户已经发生的额外应对动作，通常麻烦、费时、不理想 | 必须是已发生行为；愿望/期待不能放这里 |
| `Current Solution` | 用户今天依赖的产品、方法、他人、空间、流程或非消费 | 可跨品类；新买产品也可有痛点 |
| `Pains` | 情绪 + 场景 + 后果，不只写现象 | “所以怎样”必须明确：浪费、延误、冲突、焦虑、放弃等 |
| `Delights` | 当前方案让用户满意的具体体验 | 没有就写 `缺证据`，不要为了平衡硬写 |
| `Verbatim` | 用户原话，保留口吻和关键词 | 禁止 AI 自动补原话；没有原文就写 `缺证据` |

## 2. 证据等级

| 等级 | 含义 | 下游使用 |
|---|---|---|
| `A` | 一手访谈/原始评论明确支持，含原话或可复核位置 | 可作为需求/产品判断的强证据 |
| `B` | 多条二手评论/桌面材料支持，但缺少访谈追问 | 可作为机会方向，不可直接宣称因果 |
| `C` | 方法论推断，有间接证据 | 只能写成假设，需 Tool 9/访谈验证 |
| `H` | 研究者假设或素材缺口 | 不进入需求卡；只能进入待验证问题 |

每条 Job Statement 必须标 `evidence_grade`。同一条中如果九格证据强弱不一，按最弱关键字段定级；尤其是 `Context / Main Job / Desired Outcome / Verbatim` 任一缺失，不能高于 `C`。

## 3. 六类 lint

审计时逐条打 `pass / warn / fail`：

| Lint | Fail 信号 | 修正动作 |
|---|---|---|
| `context_too_generic` | “存蔬菜”“做饭”“管理日程”这类泛场景 | 回原文补具体对象、状态、时间、数量、动作 |
| `main_job_is_feature` | “冰箱要大”“希望 AI 自动识别”“App 要提醒” | 改成用户动作和进展；功能放下游 solution |
| `outcome_not_measurable` | “更方便”“保鲜好一点”“更清楚”无标尺 | 标 `待追问` 或补原文中的时间、数量、误差、可见性标准 |
| `wish_as_compensation` | 把“希望产品能...”写成补偿行为 | 只保留已发生 workaround；愿望移到 Desired Outcome 或 Open Question |
| `mixed_scenes` | 前半是采购，后半变成晚餐；一条混多个 moment | 拆成多条 Job Statement |
| `pain_without_consequence` | 只写现象，没有情绪和后果 | 补“所以导致什么、用户什么感受”；缺证据则标缺口 |

## 4. 通过标准

一条 Job Statement 进入后续聚类/产品洞察前，必须满足：

- `Context / Main Job / Desired Outcome / Verbatim` 四项不为空；否则只能进入 `Open Questions`。
- 不触发任何 `fail` 级 lint；`warn` 必须写修订建议或待追问问题。
- 若来源是 Amazon/Reddit/App Store 等评论，必须保留 `source_id` 或可回查位置。
- 若要进入需求卡，至少 `evidence_grade >= B`，且 `Compensation Behavior` 或 `Current Solution` 至少有一项有证据。

## 5. 最小输出表

```markdown
| id | Context | Main Job | Desired Outcome | Constraints & Tensions | Compensation Behavior | Current Solution | Pains | Delights | Verbatim | evidence_grade | lint_flags | open_questions |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
```

不要用这张表替代分析。它的作用是让后续分析有可追溯、可审计的用户需求故事底座。
