# CC memdir · `type: feedback` 原子（示例指针 + 落盘模板）

**何时读本文**：`memory-dream` **Phase 3**，且拟新建 **`memory/YYYYMMDD_feedback_*.md`**（根目录）、YAML 含 **`type: feedback`**。其它类型见文末指针，勿读本文件全文。

**铁律**：`05_每日记录/…` 下示例 **只读**；dream **禁止**改写该目录。

---

## 导航

| 节 | 内容 |
|----|------|
| [只读示例（路径）](#只读示例路径) | 三份完整体例，需对齐时再 `Read` |
| [复制模板](#复制模板写入-memory-根目录) | 新建原子时直接粘贴 |
| [Phase 3 清单](#phase-3-清单-feedback-原子) | 逐项勾选，防漏双写 |
| [字段速查](#字段速查) | YAML + 正文一行一句要求 |
| [L0/L1 双写](#l0l1-双写-3-步) | 与 `MEMORY.md`、L1 索引同步 |

---

## 只读示例（路径）

自 Vault 根；体例：**YAML 三键**（`name` / `description` / `type: feedback`）+ **`**Why:**`** + **`**How to apply:**`**，短、可单卡进上下文。

| 主题 | 路径 |
|------|------|
| 执行前不索要确认 | `05_每日记录/2026/04/20260407/CC记忆参考_本机搬运/feedback_no_confirmation.md` |
| wikilink 与文件名一致 | `05_每日记录/2026/04/20260407/CC记忆参考_本机搬运/feedback_wikilink_filename_consistency.md` |
| ZK 工作区边界 | `05_每日记录/2026/04/20260407/CC记忆参考_本机搬运/feedback_workspace_zk.md` |

**注意**：`feedback_workspace_zk.md` 可能含本机绝对路径；落盘原子时写 **「ZK 工作区 = 本 Vault 根」** 或相对约定，勿固化单机路径。

---

## 复制模板（写入 memory 根目录）

文件名：`YYYYMMDD_feedback_简述.md`（日期 = 蒸馏执行日或与信号日一致；与 `YYYY-MM-DD` 日报区分）。

```markdown
---
name: 短标题（人读）
description: 一句检索/召回钩子（可与 name 互补）
type: feedback
---

（可选：1～2 句现象或结论，陈述句。）

**Why:** 用户为何在意 / 根因 / 此前错在哪。

**How to apply:** 可执行规则；必要时列表。长案例只给链接：`05_每日记录/` 或 `03_索引/` 内笔记，勿堆正文。
```

---

## Phase 3 清单（feedback 原子）

- [ ]  frontmatter 含 `name`、`description`、`type: feedback`
- [ ]  正文含独立行 **`**Why:**`** 与 **`**How to apply:**`**（非「用户说过」空转）
- [ ]  新文件：`memory/YYYYMMDD_feedback_简述.md`
- [ ]  `MEMORY.md` **对应域**增一行，整形如 `- [[memory/….md|短名]]：一句 hook`（与 `description` 一致；Obsidian wikilink）
- [ ]  `memory/topics/<machine-id>/feedback.md`（及 skill 要求的 **user/project/reference** 侧 **`## 原子卡索引（memory-dream 维护）`**）增 `[[memory/…|hook]]`
- [ ]  未改写 `05_每日记录/`；未把禁止路径操作写进 How（执行协议已约束）

---

## 字段速查

| 键 / 段 | 要求 |
|---------|------|
| `name` | 短、稳定；不必与文件名逐字同 |
| `description` | 检索与 L0/L1 写 hook 时对齐 |
| `type` | 范式纠正 → `feedback`；若属 user/project/reference，改 `type` 并对齐 `memory/topics/liuyunjiao_local/20260406_CC_memdir四类型_源码模板.md` |
| **Why** | 因果与动机 |
| **How to apply** | 下一轮 Agent 可直接照做；禁冗长案例 |

---

## L0/L1 双写（3 步）

1. 原子正文落 `memory/YYYYMMDD_feedback_简述.md`
2. `MEMORY.md` 对应域小节一行指针 + hook（体例见 `MEMORY.md` 文首说明）
3. L1：`feedback.md` 等与 skill 约定的 **`## 原子卡索引（memory-dream 维护）`** 追加 `[[memory/…|hook]]`（路径限定）

细则与矛盾处理仍以 `memory-dream/SKILL.md` Phase 3 与 `core-ops.mdc` Step 4.1 为准；**本文件不重复** Phase 全文。

---

## 其它 `type`

`user` / `project` / `reference` 结构不同 → `memory/topics/liuyunjiao_local/20260406_CC_memdir四类型_源码模板.md`（§3.1 / §3.3 / §3.4）。
