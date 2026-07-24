# developer-toolkit — 新手上路（三条线）

每条线 **5～7 步**；每步 **一句**：用啥 + 为啥。细节以各工具官方 SKILL 为准。

---

## 线 A：纯应用开发（业务代码 / 功能，少碰 OpenClaw 本体）

1. **装齐三样**（见 `install.md`）— 没有工具则后面全是空转。  
2. **用 Superpowers `brainstorming`** 把需求边界说清 — 避免直接写偏了代码。  
3. **需要组织级承诺时**：`cd ~/.openclaw` 后 **`openspec new change`**，把「做啥、不验收不算完」写进 change — 变更可追溯、可交接。  
4. **拆任务**：`openspec instructions apply --change <id>` 跟 `tasks.md`，或用 **`writing-plans`** 把实现步写细 — 执行不靠口头。  
5. **写码**：**`test-driven-development`**（或 `subagent-driven-development`）— 先测后码，减少返工。  
6. **合并前**：在已装 gstack 的会话里 **`/review`**；有 URL 再 **`/qa`** — 别人能复现、你能看见界面。  
7. **收尾**：`openspec archive`（若该功能走了 OpenSpec）+ **`/ship`** 或团队流程 — 规格与代码一起收束。

---

## 线 B：OpenClaw 运维 / 配置 / 多 agent（动「运行时」）

1. **先读**用户 guardrails：**动 `openclaw.json`、协议、多 agent 必须先 OpenSpec change** — 防线上翻车。  
2. **`cd ~/.openclaw && openspec new change "<id>"`**，在 proposal/design 写动机、范围、回滚、验收 — 没有台账不要改 JSON。  
3. **`openspec status --change <id>`** 直到可 Apply — 避免半成品改配置。  
4. **按 `tasks.md` 执行**：需要时用 **`openspec-apply-change`** 节奏；改完 **`openclaw gateway restart`**（若适用）+ **`openclaw doctor`** — 与运维习惯一致。  
5. **编排侧**：OpenClaw spawn 编码任务时按 gstack **Simple → Full** 选档（见 `docs/OPENCLAW.md`）— 小改不堆全流程。  
6. **交付**：**`openspec archive`**，delta 合主 spec — 下一任看得懂「当时承诺了什么」。

---

## 线 C：只评审 / 规划，不（或少）写代码

1. **装 gstack**（`install.md`）— 评审类能力主要在 gstack slash。  
2. **战略/想法**：**`/office-hours`** 或 **`/plan-ceo-review`** — 先把「值不值」说清楚。  
3. **架构/方案**：**`/plan-eng-review`**；偏 UI/体验：**`/plan-design-review`** — 分工明确，不靠一篇大作文。  
4. **一次要多角色**：**`/autoplan`** — 省得自己串 prompt。  
5. **看代码不写代码**：**`/review`**；要看线上行为：**`/qa <URL>`** — 证据在 diff 和浏览器里。  
6. **安全视角**：**`/cso`** — 专门一条线，别混在普通 review 里省略。  
7. **若组织要求变更也要留痕**：相关决策仍应回写到 **OpenSpec**（由执行方开 change），你只评审时可在结论里注明「须落 change」— 避免口头拍板。

---

## 三条线怎么选

- 只改产品代码、不动 OpenClaw → **线 A**。  
- 动网关、agent、飞书通道、`openclaw.json` → **线 B** 优先。  
- PM/负责人/架构师为主、自己不 commit → **线 C**。
