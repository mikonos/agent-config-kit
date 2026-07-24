# Rule 11 跨 tool 术语 cascade · SOP

> Rule 11 原本只管「单 tool synthesis 内的术语一致性扫描」——parallel subagents 翻译同一概念会分叉，主综合方收口前要扫一遍。
> v5.10 扩展：当 **Tool 1（灵魂/术语真源）或 Tool 4（用户群定义真源）** 改版后，下游 Tool 6/7/8 + 营销台账 + 证据台账 + quality_audit 必须**整套**同步替换；不彻底 = D5 状态冲突。
> 这条 SOP 描述具体怎么 cascade、谁负责、什么时候算完成。

---

## 1. 触发条件

下面任一情况触发**整套 cascade**：

- Tool 1 灵魂句、戏剧角色、文化代码、hero/launch/sustaining slogan **任一替换**（v0.x → v1.x 升档时常见）
- Tool 4 用户群命名、编号、群定义 **任一替换**（G1 重命名、G8/X1-X5 新增、靶心圈层调整）
- Tool 8 core interaction 单句声明替换
- 任一 tool 主稿声明了 retire 某术语 / hold 某术语 / 新增同义词族

**判定测试**：如果一个**英文短语 / 大写英文单词 / 中文名词短语 / 数字编号**在 tool 主稿被改写，且这个词在其他 tool 主稿 / 营销台账 / 证据台账中出现过——必走 cascade。

---

## 2. Cascade 范围（必扫文件列表）

每次 cascade 必须扫描以下文件，无一例外：

```
{dogfood 目录}/
├── tool01_product_soul_{product}.md
├── tool03_four_lens_{product}.md
├── tool03b_innovation_{product}.md   (若存在)
├── tool04_target_users_{product}.md
├── tool05_literature_{product}.md   (若存在)
├── tool06_emotional_social_{product}.md
├── tool07_functional_needs_{product}.md
├── tool08_ecosystem_{product}.md
├── tool09_interview_questions_{product}.md
├── tool10_survey_design_{product}.md
├── 上市与营销信号台账_{product}.md
├── 00_证据可信度台账_{product}.md
├── quality_audit_{product}.md
└── _dogfood进度与下一步.md
```

漏扫任一文件 = cascade 失败。

---

## 3. Kill log 强制要求

每次 cascade 必须在 **Tool 1 主稿「§推断与证据」节** 和 **营销台账「§cascade history」段** 同时写 kill log，格式：

```markdown
### Cascade v{N} → v{N+1} kill log（{YYYY-MM-DD}）

| # | 旧词 | 新词 | retire 理由 | 替换范围 | 状态 |
|---|---|---|---|---|---|
| 1 | second watch | second memory | 旧戏剧角色被读成 surveillance | 全部 14 文件 + 主稿 §1.3 § 3 §6 | ✅ done |
| 2 | WATCH | HOLDING | culture code 升级（reptilian → on-code） | 全部 14 文件 + 主稿 §2 §3.5 §4 §5 | ⚠️ 营销台账 L48 / L335 未替换，本次完成 |
| 3 | Eyes | （删或改 memory）| metaphor 不再使用 | 主稿 §1.3 + Tool 8 §一 §二 + 台账 §10 | ⏳ Tool 8 进行中 |
| ... | | | | | |
```

字段：
- **旧词**：被 retire 的具体字符串（精确到大小写、引号、复数形态）
- **新词**：替换后的字符串；如果是 retire 后**删除**而非替换，写「（删）」
- **retire 理由**：一句话——「为什么这次改字」
- **替换范围**：具体到文件 + 章节段落（不写「全文」这种含糊范围）
- **状态**：✅ done / ⚠️ partial（说明哪里还没替换）/ ⏳ in progress / ❌ blocked

---

## 4. Cascade 执行顺序

按下面顺序执行，串行，不许跳：

1. **Tool 1 主稿**先 lock 新版本（v1.x final + changelog）；本身的旧词在「§cascade history」kill log 段保留为历史档案
2. **Tool 8 主稿**——生态叙事最依赖 Tool 1 戏剧角色
3. **Tool 6 主稿**——anxiety / 反向需求段最依赖灵魂句
4. **Tool 7 主稿**——P0/P1/P2 trust architecture 列依赖 Tool 1 文化代码
5. **Tool 3 主稿**——cross-lens 综合段引用灵魂句
6. **Tool 4 主稿**——通常只受 Tool 4 自身改动影响，跨 Tool 1 cascade 较少；但若 Tool 1 改了「核心靶心群」描述，回头改 Tool 4 速查
7. **Tool 9 / Tool 10 主稿**（若已存在）——访谈题 / 问卷题里若提到旧词，替换
8. **营销台账**——所有 §2-§11 段
9. **证据台账**——速查 + §1 原始材料可信度段
10. **quality_audit 报告**——§覆盖矩阵 + §P0 状态段
11. **_dogfood进度与下一步**——速查 + 进度表

每步完成后在 kill log 表的「状态」列标 ✅。

---

## 5. Cascade 完成判定（自检）

cascade 完成后跑两遍验证：

### 5.1 Grep 验证（强制）

```bash
grep -rn "{旧词}" {dogfood 目录}/ --include="*.md"
```

每个旧词都 grep 一遍。预期结果：旧词**只能**出现在以下位置，其他地方 = cascade 失败：

- Tool 1 主稿 §cascade history（历史档案）
- 营销台账 §cascade history
- 各 tool changelog 段（"v1.0 → v1.x 替换 X 为 Y"）
- review/audit 报告里引用旧版本结论时的原文

任何 sentence subject / 表列 / hero phrase 仍含旧词 = cascade 失败。

### 5.2 Set 验证（Rule 15 横向延伸）

不只看 count，看具体词族：

- Tool 1 §1.3 戏剧角色定的「不是 …」清单里所有 misframe 词，必须在 Tool 8 sales pitch + 营销台账 reverse anchor 段也出现，**或** 显式标注「本产品不在此清单的 misframe 范围」
- Tool 1 §2 文化代码「禁忌词族」里所有词，必须在营销台账 §5 GTM 硬规则有匹配的禁用规则

漏一个 = Rule 15 漂移 = cascade 失败。

---

## 6. Cascade 失败后处置

任一 grep / set 验证不通过 → cascade 失败 → 触发 D5 状态冲突 → 进 Phase 7.5 expert panel review。

panel 必须包含 **Tool 1 的 Dichter（或当时改字的 persona）** 作为 panelist——只有他能判定「这个旧词残留是历史档案还是 cascade 漏网」。

---

## 7. Cascade 真源与责任人

- **Cascade 真源**：Tool 1 主稿（灵魂/术语）和 Tool 4 主稿（用户群定义）；其他 tool 不许做术语主真源。
- **执行责任人**：主综合方（小P）；不许下放给 subagent。
- **审核责任人**：Phase 7.5 panel；不许由主综合方自审。

---

## 8. 历史先例

2026-05-26 research 家庭Agent美国市场 v1.3 cascade：

- Tool 1 round 5 final 替换 `second watch → second memory`、`WATCH → HOLDING`、`Eyes → 删`
- 营销台账 v0.7 声明 cascade override
- 但 review2_tool08 panel 发现台账 L17-588 仍大量旧词残留，正文仍 `Eyes 不是 hands`、`Two pairs of eyes`、`second-watch device`
- 教训：cascade override 不能只在台账顶部声明 v0.x → v0.x 完成，必须 grep 验证整文件；本 SOP 把 grep 列为强制步骤

---

*真源在 `references/cascade_sop.md`；SKILL.md Rule 11 引用此文件作扩展协议。*
