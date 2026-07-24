---
name: open-loops
description: Legacy Open Loops 只读工具。用于查询旧 `memory/open loops.md`、从旧条目生成会议议程参考、为旧条目闭环给出确认建议；非 GTD 主任务带出的新承诺走 `dry run gtd-capture`，确认后更新 `memory/gtd/`。
---

> **通用协议**：执行前读取 `.cursor/skills/vault-writing-preamble/SKILL.md`。

# Legacy Open Loops Skill

**定位**：`memory/open loops.md` 是旧系统遗留文件，只作历史查询、会议参考和旧条目处理。新产生的承诺、待办、等待项、项目行动，不进入本文件。

**新承诺入口**：非 GTD 主任务带出的、需老板本人执行、等待、确认或追踪的事项，调用 `dry run gtd-capture` 产出归位建议；老板确认后，再按 `gtd-harness` 更新 `memory/gtd/`。

**禁止事项**：
- 不新增个人执行事项到 `memory/open loops.md`。
- 不把其他 skill 的收尾事项放入旧 open loops。
- 不迁移、清空、批量改写 `memory/open loops.md`。
- 不在未确认的情况下删除旧条目。

---

## 模式一：legacy query（只读查询）

**触发词**：`旧 open loops`、`历史 open loops`、`memory/open loops.md`、`以前 open loops 里有什么`、`旧条目查询`。

**执行**：
1. Read `memory/open loops.md`。
2. 按人物、项目、日期或关键词过滤。
3. 输出时标注“legacy 来源”，不要把旧条目当作当前 GTD 真源。

---

## 模式二：legacy agenda（旧条目议程参考）

以 **Andy Grove（High Output Management）** 的视角生成议程参考。旧 open loops 只提供历史阻塞/决策线索；会议后的新行动项仍走 `dry run gtd-capture`。

**触发场景**：
- 用户明确要求基于旧 open loops 准备会议。
- meeting-note 需要历史议程参考，且当前 GTD 清单不足以还原旧上下文。

**执行**：
1. Read `memory/open loops.md`。
2. 提取与人物或项目相关的旧条目。
3. 按 Grove 优先级输出参考议程：blocking > decision > update。
4. 会后若产生新承诺，输出 `dry run gtd-capture` 建议，等待老板确认后更新 `memory/gtd/`。

---

## 模式三：legacy close proposal（旧条目闭环建议）

用户明确指向旧 open loops 条目并宣告完成/搞定/已解决/打勾时：

1. Read `memory/open loops.md`。
2. 匹配候选旧条目。
3. 输出拟处理条目和理由，询问老板确认。
4. 老板确认后，才删除或调整对应旧条目；未确认时不改文件。

---

## 质量检查

- [ ] 本次是否没有新增任何个人执行事项到 `memory/open loops.md`
- [ ] 查询/议程是否明确标注 legacy 来源
- [ ] 非 GTD 主任务带出的新承诺是否已改走 `dry run gtd-capture`
- [ ] 旧条目删除/调整是否先获得老板确认
