# L0 `MEMORY.md` 与 L1 六文件分工（规约）

> **目的**：对齐 **稀疏 L0** 与 **主题 L1** 的职责，避免把 L1 做成第二张 MEMORY，也避免 L0 胀成知识库。  
> **真源**：`core-ops` Step 4.2 / 4.3；本文件为 **memory-dream** 执行时的 **结构验收**参考。

---

## 1. 两层职责

| 层 | 路径 | 职责 |
|---|---|---|
| **L0** | 根目录 `MEMORY.md` | **导航索引**：节标题建议 **「中文标签（user|project|…）→ L1」**；按域分区 → 指向各 L1 的**短指针**；**每行 ≤~150 字符**；**禁止**长段、整表、多行战略展开；原子指针行仅 `- [[memory/…\|短名]]：hook`（Obsidian；落在对应域小节）（类型由文件名推断；冒号体例对齐 CC）。 |
| **L1** | `memory/topics/<machine-id>/{user,project,feedback,reference,affect,vault}.md` | **主题正文**：范式陈述、可复用表、常青/慢衰减、会话摘录；**单文件建议 ≤200 行**；长内容逐步 **Demote** 到 `memory/YYYYMMDD_<type>_*.md` 原子文件或 ZK 笔记。 |

**原则**：MEMORY 回答「**去哪个文件找哪类事**」；L1 回答「**这类事的具体陈述与证据**」。

---

## 2. L0 区块 ↔ L1 文件（域映射）

| `MEMORY.md` 区块 | L1 文件 | 本域写什么 |
|---|---|---|
| 用户与协作 | `user.md` | 稳定画像、铁律、思维模式；**不**把短期情绪堆这里 |
| 项目上下文 | `project.md` | 产品/战役/GTM/商业；**不**把图谱劳动堆这里 |
| 知识库状态 | `vault.md` | ZK 内「此刻在做什么」：深读线、MOC、索引劳动；**禁止**贴原子笔记正文 |
| Feedback | `feedback.md` | 对 Agent 的纠正/确认；**Why / How to apply** 范式（见 CC 模板） |
| 运维与工具 | `reference.md` | URL、排障表、外部系统短指针；易变项 |
| 情绪与协作节奏 | `affect.md` | **周级**、可消退的协作态与节奏请求；**禁止**临床诊断 |

**扩展类型** `affect` / `vault` **非 CC 原生**，与 `user` / `project` 的边界见 `core-ops` Step 4.2。

---

## 3. L1 统一骨架（建议六文件一致）

下列顺序与命名 **建议**一致，便于 dream 扫描与人工扫读；**不**要求各域小节标题完全相同（如 `feedback` 保留「范式级」、`reference` 保留「故障表」）。

```
---
description: …
---

# <Title>

> **定位（可选）**：本文件为 **`<type>` 域** … **`## 原子卡索引（memory-dream 维护）`** 由 **`_session-summary-worker.js`**（与 `MEMORY.md` 同条件）追加新 `[[memory/…|hook]]` 行，**memory-dream** 合并/去重/Demote；日常对话 Agent **勿手改**该节。

## 原子卡索引（memory-dream 维护）

<!-- dream 维护：[[memory/…|hook]] -->

## <本域正文小节>（因域而异：常青 / 慢衰减 / 范式级 / 进行中的知识线程 / …）

## 来自会话的摘录

<!-- session 注释；蒸馏时并入上节或删 -->
```

**铁律**：**勿**由日常对话 Agent **手改** `## 原子卡索引（memory-dream 维护）`** 一节**（与 `user.md` / `project.md` / `reference.md` 已声明一致）。**例外**：仓库内 **`_session-summary-worker.js`** 在抽取成功且更新 `MEMORY.md` 时，向本节**自动追加**索引行（与 `cc-vs-zk-memory-mapping.md` 一致）。

---

## 4. 不必做的事

- **不要**把六个 L1 的目录做成与 `MEMORY.md` **逐节同构**（L1 不是 L0 的放大版）。
- **不要**把 L1 合法表格（如 reference 故障表）强行拆成 MEMORY 式短行——**表留在 L1**，MEMORY 只保留 **一行指针**。
- **不要**在 `affect` 写稳定画像、在 `user` 写战役结论——**分工错置**时由 dream **Demote** 或迁移。

---

## 5. 修订记录

| 日期 | 变更 |
|---|---|
| 2026-04-06 | 初版：L0/L1 分工、域映射、统一骨架、禁止项 |
| 2026-04-07 | 原子卡索引节：允许 worker 自动追加；dream 仍负责合并 |
