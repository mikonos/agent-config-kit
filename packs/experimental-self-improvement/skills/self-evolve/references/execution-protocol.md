# Self-Evolve 执行协议与状态机

## 全局并发状态机 (Concurrent State Machine)

Agent 每次运行 self-evolve 都是一次**滴答巡航（Tick Handler）**。
进化流程受制于用户所选项目内的状态文件：`.agent-evolve/state.json`

`state.json` 包含 `active_experiments` 数组，允许同时记录多个等待后续观察的实验。
“观察中”是状态标签，不表示有后台进程；每次采集都必须由用户显式继续或由另行
批准的自动化触发。
**并发限制**：最多允许 10 个实验同时处于 `OBSERVING` 或 `BLOCKED`，且它们**必须是正交的**（不修改相同的配置、代码或能力维度）。

每次启动 `self-evolve`，必须按照以下 **四个步骤的巡航顺序** 执行，走完一步才能走下一步。

### 侧车状态：`.agent-evolve/self-evolve-meta.json`

- 字段 **`non_cold_streak`**：用于 **冷门 skill 配额**（见 Step 4）。**每次在 Phase 1 成功注册新实验后必须更新**，规则见该节。
- 若文件不存在：创建为 `{"non_cold_streak": 0, "schema": "self-evolve-meta v1"}`。

### Harness 自进化扩展（与训练管线类比）

- 设计意图：把「自训练」里 **合成数据 + 多评委 + 防分布窄化** 翻译成
  **配置层** 的可逆实验。
- 本协议新增三块：**合成压测 → candidates**、**held-out 回归门禁**、**冷门 skill 配额**。

---

## 执行协议：四步滴答巡航（The 4-Step Tick）

### Step 1: 扫描正在运行的实验 (Status Sync)
打开并读取 `.agent-evolve/state.json` 的 `active_experiments` 数组。
- 如果文件不存在，在用户已确认的项目内创建最小初始状态后跳到 Step 4。
- 如果数组为空：直接跳到 Step 4。
- 若有实验属于 `BLOCKED` 状态：检查是否有解救条件（例如 API 恢复了）。如未解除，跳过该实验；如已解除，将状态重置为 `OBSERVING`。

### Step 2: 记录观察数据 (Record Observations)
针对所有 `status: OBSERVING` 并且还没到期的实验：
- 读取该实验在 `state.json` 中的 `telemetry_hook` 字段。先确认命令是只读的；
  非只读命令必须重新预览并获得用户批准后才能收集原始日志。
- **降噪防护**：如果本次 Tick 没有任何实质性指标变化或未收集到新的反馈，**直接跳过，切勿写入全空的假日志**。只有捕获到了新指标才追加到对应的 `.agent-evolve/[cycle_id].jsonl`。
- **连续跳过强制审计**：记录连续降噪跳过的次数（每个 tick 全员跳过 = +1）。**若连续 ≥3 次全员降噪跳过，必须强制触发轻量审计**（执行 workflow-audit skill 生成审查报告），并在 state.json 中记录 `consecutive_skips_audit_triggered=true`。
- **强制输出**：生成的 JSONL 记录的 `metrics` 字典中，必须强制包含并输出 `extract` 要求的所有监控项键，防范糊弄。
- **极端拦截**：若收集数据时发现极端负向反应（如系统连续崩溃），触发提前终止，强制进入下一步的评估流。

### Step 3: 到期评估与阶段固化 (Evaluate & Solidify)
针对所有 `status: OBSERVING` 并且当前时间 `>= evaluate_by` 的实验：
1. **对比数据**：读取它累积的 JSONL 数据与基线做对比。
2. **决策胜诉方**：选出 A 方案还是 B 方案成功（若都没有基线好，返回退回基线）。
3. **Held-out 回归门禁（配置 / Harness 类实验强制）**  
   - **触发条件**：本轮拟「物理固化」的路径命中以下**任一**时，必须先跑门禁再固化：  
     当前 Runtime 的 Rule、Agent 配置、工具说明、Skill、Hook 配置，以及
     **CI 中仅服务于 Agent 质量的门禁 job**（与业务单元测无关的纯编排不算，除非实验目标就是 CI）。  
   - **动作**：打开 `.agent-evolve/held-out-tasks.md`，对其中所有 **`[x]` 启用** 的任务逐项执行其「验收」块（命令或清单）。任何非只读验收命令仍需用户批准。  
   - **判定**：**任一项失败 → 禁止执行本步第 4 点的物理固化**；在 `.agent-evolve/evolution-log.md` 记一条 `HELD_OUT_BLOCK`（含失败任务名与日志摘要）；该实验可记为「观察结束但配置未落地」或延长观察，**不得**把未过 held-out 的改动写入仓库。  
   - **空集豁免**：若 held-out 文件中**没有任何** `[x]` 启用项，视为门禁未就绪——**仍允许固化**，但必须在同一条 evolution-log 中记 `HELD_OUT_SKIPPED_EMPTY`，并给老板留一条 open loop：**尽快补全 held-out**。
4. **物理固化**：仅在第 3 点未拦截，且用户看过精确 diff 并明确批准后执行——修改对应的 Rule、Agent 配置、Skill、工具说明或实际代码库。
5. **归档沉淀**：向 `.agent-evolve/evolution-log.md` 写入本轮赢家和教训（若 held-out 拦截，写清原因）。
6. **驱逐清理**：将其从 `state.json` 的 `active_experiments` 中移除。

### Step 4: 启动新轮次 (Launch New Experiment)
在走完前 3 步后，统计 `state.json` 中剩下的未完结任务数量。
- 若剩余任务数 `>= max_concurrent`（如 10）：**强制结束巡航并交还用户！**禁止再接新活。
- 若容量充足：开始挑选**一个**全新的进化实验。
- **凑数防护**：如果此时雷达探测不到亟待解决的瓶颈，或者现存痛点均已被包含在活跃实验中，**果断保持安静并退出，绝不可为填满限额而捏造无意义垃圾实验。**
- **冷门 skill 配额（防分布窄化）**  
  1. 读取 `.agent-evolve/self-evolve-meta.json` 的 `non_cold_streak`（缺省按 0）。  
  2. **若 `non_cold_streak >= 4`**：本轮 Phase 0/1 **必须**选择「**最近约 30 天内在实际会话中极少触发的 Skill 或工具路径**」相关瓶颈（证据来源示例：当前项目的 Git 历史、用户提供的会话日志，或用户明确的冷门领域）。新注册实验的 `state.json` 对象建议带 `"cold_skill_quota": true`。  
  3. **注册完成后更新 meta**：若本实验 `cold_skill_quota: true` → 将 `non_cold_streak` **置 0**；否则 → `non_cold_streak` **加 1**（上限逻辑：连续 4 次非冷门后第 5 次强制冷门，故 streak 达到 4 时下一发必须冷门，注册冷门后归零）。  
  4. **语义核对**：`non_cold_streak` 表示「**已连续注册的非冷门实验数**」；冷门实验会将其清零。

---

## 寻找实验：Phase 0 与 Phase 1

若 Step 4 决定启动新轮次，执行以下流程：

### Phase 0: 寻找瓶颈 (The "What")
- **首先**读取 `.agent-evolve/candidates.md`（由用户或已批准的工作流写入的候选池）。
- 其他来源：当前项目近期错误日志的重复模式、用户明确提供的反馈、效率观察
  （严重耗时的任务）。
- **合成压测（主动感知，对标「合成数据」）**  
  - 从用户提供或明确允许读取的近期 **成功** 会话中抽取 1–3 条任务描述。  
  - **变异**：在人为构造的副本或隔离测试环境中增加约束（删 Rule 关键段、
    注入冲突规则、加大上下文噪声、换栈假信息）——变异需**记录在案**，不得
    为压测破坏真实项目文件。  
  - **回放**：用当前 harness 再跑变异任务；若出现可复现失败，将根因写入 `candidates.md`，条目注明 `source: synthetic-stress`。  
  - **风险**：变异若只覆盖「模型想象得到的极端」，会 **过拟合**；须与 Step 3 **held-out**（含人工设计项）配合。
- **选择原则**：一次只进化一个方向。按以下优先级筛选：**即发频率 > 全局杠杆 > 量化可测性**；`source: synthetic-stress` 与生产故障 **同等进入候选池**，不降级。

### Phase 1: 搜索方案 (The "How")
- 必须同时搜索至少 3 个来源寻找解法（如 `skills.sh`, GitHub, Reddit/社区）。
- 每个来源最多保留 2 个候选方案进行短描述对比。
- **部署实验**：在 `.agent-evolve/` 中创建一份实验部署说明（参照进化报告模板）。说明不是执行授权。
- **注册评估任务**：把当前评估截止时间更新至 `.agent-evolve/state.json` 的新实验对象中，并将状态从 `IDLE` 改为 `OBSERVING`。
- **注册后**：按 Step 4「冷门 Skill 配额」更新 `.agent-evolve/self-evolve-meta.json` 中的 `non_cold_streak` 与（可选）`cold_skill_quota` 标记。

**完成注册后，本轮巡航彻底结束并交还用户，等待下一次显式继续。**
