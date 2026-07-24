# developer-toolkit — 金样例（few-shot）

模型应模仿：**先标阶段 → 缺口 → 唯一下一步**；涉 OpenClaw 运行时则点明 **先 OpenSpec change**。以下为示意，真实对话需替换具体 change 名与路径。

---

## 样例 A（典型编排）

**用户**：「三栈我现在算哪一步？下一步只给一个。我们刚写完 proposal，还没齐 specs。」

**合格回复骨架**：

1. **阶段**：3（规格立项）— 依据：proposal 已有，specs 未齐。  
2. **缺口**：specs 未落地；`openspec status` 未过 apply 门槛；验收/回滚未在 artifacts 中闭合。  
3. **下一步（唯一）**：在 `~/.openclaw` 下执行 `openspec instructions <artifact-id> --change "<id>" --json` 补全 `specs/`，直至 `openspec status --change "<id>"` 显示可 Apply。  
4. **运行时/协议**：若本 change 含 `openclaw.json`/多 agent/协议 — **先保证 change 内 specs/design 写明再改文件**。

---

## 样例 B（硬规则 + 唯一动作）

**用户**：「想改 `openclaw.json` 里 memory 的 embedding，三栈我该先干啥？」

**合格回复骨架**：

1. **阶段**：3→4 之间（规格/计划交界），但**改动类属运行时配置**。  
2. **缺口**：缺已批准的 OpenSpec change；缺 tasks 中「改配置 / doctor / 验收」条目。  
3. **下一步（唯一）**：**先** `openspec new change` 或接续既有 `change-id`，在 proposal/design 写动机与回滚，再 `openspec config set` 或经批准的 JSON 编辑（以你们 guardrails 为准）。  
4. **先 OpenSpec change**（本例必显式写出）。

---

## 反面 brief（勿模仿）

只回「阶段 3，建议用 OpenSpec」而无 **具体命令或 artifact**；或把整段 seven 阶段表复读一遍。
