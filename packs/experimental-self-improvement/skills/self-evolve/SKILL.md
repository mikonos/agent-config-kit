---
name: self-evolve
description: >-
  用可逆实验改进 Agent 的能力或工作流：定位具体瓶颈，建立量化基线，
  比较候选方案，运行回归门禁，再由用户批准是否固化。适用于能力升级、
  工作流优化、Skill 或工具迭代，以及 self-improve、A/B test、进化实验。
license: MIT
metadata:
  author: Agent Config Kit maintainers
  portability: codex-cursor-claude-code
---

# Self-Evolve — Agent 自主进化引擎

> 生物进化的核心机制：变异 → 选择 → 保留。
> 这个 skill 把同样的机制应用到 agent 自身——不断发现可改进的角度，用实验找到更好的方案，然后永久固化。

## 这是什么

Self-Evolve 是一个 **meta-skill**——它不解决具体业务问题，而是让 agent 自身变强。

* **和反思工作的边界**：反思负责发现短板（诊断），`self-evolve` 对短板寻找解法并跑实验验证（治疗）。
* **不是什么**：禁止无目标的空转、禁止为写长篇自省报告而改排版的“伪进化”。（详细约束见: [约束与红线](references/constraints-and-rules.md)）

## 快速使用说明 (Quick Start)

### 触发方式
仅在用户明确要求改进某个能力或继续一个已批准实验时启动。

本公开包不会安装定时任务、Hook、心跳或后台进程。用户如另行要求自动运行，
必须先单独预览触发频率、写入位置、命令和停止方式，并再次获得明确授权。

默认把状态和报告写到用户所选项目的 `.agent-evolve/` 目录。开始前先确认项目
路径；不得写入用户主目录、全局 Runtime 配置或其他项目。

### 执行协议 (The 4-Step Tick)
每次触发此技能，你必须执行一次且仅执行一次“滴答巡航”（Tick Handler），绝不能无视状态机一次性跑完实验全流程。
完整并发状态机制及操作边界，请细读： [执行状态机与四步巡航协议](references/execution-protocol.md)

协议包含 **合成压测 → candidates**、`.agent-evolve/held-out-tasks.md`
**回归门禁**和 `self-evolve-meta.json` **冷门 Skill 配额**。

1. **Step 1: Status Sync** - 扫描 `state.json` 的活跃实验。
2. **Step 2: Record Observations** - 将观察指标降噪后写入相应的 `jsonl` 记录。
3. **Step 3: Evaluate & Solidify** - 将到期限对比基线固化，并清理任务队列。
4. **Step 4: Launch New Experiment** - 如并发额度允许（<10），则寻找新瓶颈，搜索方案，设计实验并在状态机注册 `OBSERVING`。部署要求参考 [模板与输出规范](assets/evolution-report-template.md)。

> 🚨 **注意**：注册新实验后，本轮巡航结束并把结果交还用户。状态文件只表示
> “等待下次显式继续”，不代表有后台任务正在运行。

任何安装或更新 Skill、依赖或插件，修改 Rule、Agent 配置、Hook、计划任务，
运行非只读命令，删除文件，或写入外部系统的动作，都必须先展示精确变更并由
用户明确批准。实验状态和报告不能充当这些动作的授权。

## 参考结构指南

你需要严格遵照以下文件来展开进化，**严禁凭感觉行事**：

* [执行状态机与四步巡航协议](references/execution-protocol.md) - How to run a tick (Step 1 to Step 4).
* [约束红线与分级自主权](references/constraints-and-rules.md) - What is NOT allowed (Anti-Pseudo Constraint).
* [质量自检 Checklist](references/quality-checklist.md) - Validation for the experimental design and solidification.
* [模板与文件规范](assets/evolution-report-template.md) - Data storage paths, YAML format, markdown templates.
