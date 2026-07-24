# CSV Schema · 19 列标准结构

> 经日历机（20寸以上）1051 条全量分析迭代锁定的最终版本。
> **禁止修改列名**（downstream 统计脚本依赖列名）。

---

## 完整列定义

```
id, rating, helpful, verified, date, title, content,
force_push, force_pull, force_anxiety, force_habit,
raw_job_satisfied, raw_job_frustrated,
feature_satisfied, feature_implemented_frustrated, feature_requested,
competitor_mentions, anxiety_theme, signal_type
```

---

## 字段详细规范

### 元数据字段（来自原始 CSV）

| 列名 | 类型 | 来源 | 说明 |
|------|------|------|------|
| `id` | string | 生成 | 格式：`[N]star-[序号]`，如 `5star-001`。每星级独立编号 |
| `rating` | int | 原始 CSV | 评分（1–5） |
| `helpful` | int | 原始 CSV | 有用投票数，0 表示无投票 |
| `verified` | bool | 原始 CSV | `True`/`False`，是否验证购买 |
| `date` | string | 原始 CSV | 格式：`YYYY-MM-DD` 或原始格式 |
| `title` | string | 原始 CSV | 评论标题，可为空 |
| `content` | string | 原始 CSV | **评论完整原文，不得截断** |

### 四力字段

| 列名 | 类型 | 说明 |
|------|------|------|
| `force_push` | string | 推力：什么让用户对现状不满/想改变。没有则留空 |
| `force_pull` | string | 拉力：什么吸引用户购买/继续使用。没有则留空 |
| `force_anxiety` | string | 焦虑：什么让用户犹豫/担心。没有则留空 |
| `force_habit` | string | 习惯：用户原来用什么替代方案。没有则留空 |

**规则**：四力按需标注，没有的留空。**不强制四力全填**（强制填写会引入噪音）。

### raw_job 字段

| 列名 | 类型 | 说明 |
|------|------|------|
| `raw_job_satisfied` | string（多值） | 用户表达满意/已实现的 Job，分号分隔 |
| `raw_job_frustrated` | string（多值） | 用户表达不满/失败/想要但没得到的 Job，分号分隔 |

**格式规则**：
- 每条 raw_job 以 `[功能]` / `[情感]` / `[社会]` 开头，标注需求层
- 用用户视角语言描述（不是功能名，是用户想达成的进展）
- 示例：`[功能] 让全家日程在一个屏幕上同步可见;[情感] 从混乱感转向掌控感`

### feature 字段

| 列名 | 类型 | 说明 |
|------|------|------|
| `feature_satisfied` | string（多值） | 已实现且用户满意的功能，分号分隔 |
| `feature_implemented_frustrated` | string（多值） | 已实现但用户不满意的功能（有 bug/难用），分号分隔 |
| `feature_requested` | string（多值） | 用户明确希望有但目前不存在的功能，分号分隔 |

**规则**：功能用自然语言描述（可用用户原话）。不限数量，按评论实际内容填写。

### 分析字段

| 列名 | 类型 | 说明 |
|------|------|------|
| `competitor_mentions` | string（多值） | 评论中提及的竞品或替代方案，分号分隔。无则留空 |
| `anxiety_theme` | string（多值） | 用户表达的具体焦虑内容自由文本，分号分隔。**仅在 force_anxiety 有内容时填写** |
| `signal_type` | string（多值） | `hire_moment` / `fire_moment` / `workaround` / `wishlist`，可多选分号分隔 |

---

## 多值字段规范

所有多值字段（raw_job_*、feature_*、competitor_mentions、anxiety_theme、signal_type）统一用**英文分号 `;`** 分隔，前后可有空格。

```csv
"[功能] 让全家日程在一个屏幕上同步可见;[情感] 从混乱感转向掌控感"
```

---

## Phase 7 扩展列（聚类完成后回写）

Phase 7c 完成后，在各 Structured CSV 新增以下列：

| 列名 | 说明 |
|------|------|
| `job_id_satisfied` | raw_job_satisfied 映射的 Job ID（如 `J01;J12`） |
| `job_id_frustrated` | raw_job_frustrated 映射的 Job ID |
| `feature_id_satisfied` | feature_satisfied 映射的 feature_id（如 `F01-01;F02-03`） |
| `feature_id_impl_frustrated` | feature_implemented_frustrated 映射的 feature_id |
| `feature_id_requested` | feature_requested 映射的 feature_id |

---

## 字段关系速查

| 字段对 | 关系 |
|--------|------|
| `force_anxiety` vs `anxiety_theme` | 上下级：Anxiety 标记「有焦虑」；anxiety_theme 描述具体内容。有 Anxiety 则 anxiety_theme 必填 |
| `force_push` vs `signal_type: fire_moment` | 不同层面：forces 是驱动力方向；signal_type 是触发事件类型 |
| `raw_job` vs `forces` | 平行不替代：raw_job 是用户想完成的进展；forces 是推动/阻碍这个进展的力 |
| `raw_job` vs `feature` | 不同维度：raw_job 是 Why；feature 是 What |
| `feature_implemented_frustrated` vs `feature_requested` | 不同信号：前者「功能存在但体验差」→ 修复；后者「功能不存在」→ 新增 |

---

## 数据质量已知陷阱

1. **四力 100% 填满**：若某星级某力字段非空率达 100%，可能是模板副作用而非真实标注。统计时用方向性结论，不用绝对数。
2. **anxiety_theme 字段污染**：signal_type 值（hire_moment/fire_moment）可能被误填入 anxiety_theme。统计时需过滤非自由文本内容。
3. **raw_job 归纳压缩**：高星评论 raw_job 可能被归纳成少量高频标准短语（如 5★ 仅 13 个唯一 satisfied），导致唯一数偏低但频次正确。
