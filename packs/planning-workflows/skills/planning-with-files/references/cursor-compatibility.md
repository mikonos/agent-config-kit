# Planning-with-Files: Cursor 迁移指南

本文档说明 planning-with-files skill 从 Claude Code 迁移到 Cursor IDE 的适配方案。

## 背景

planning-with-files 原本为 Claude Code 设计，使用了 Claude Code 特有的 hooks 系统：
- `PreToolUse` - 每次工具调用前自动执行
- `PostToolUse` - 每次工具调用后自动执行
- `Stop` - Agent 停止前验证

Cursor IDE 有自己的 hooks 系统，使用不同的事件类型（`beforeSubmitPrompt`、`beforeReadFile` 等），因此原版 hooks 无法直接使用。

## 版本变更

| 版本 | 平台 | 状态 |
|------|------|------|
| v2.10.0 | Claude Code | 原版（完整功能） |
| v3.0.0-cursor | Cursor IDE | 适配版（部分自动化） |
| **v3.1.0-cursor** | **Cursor IDE** | **增强版（全自动化）** ⭐ |

## 功能对比

### 完全可用 ✅

| 功能 | 说明 |
|------|------|
| 计划文件 (`task_plan.md`) | 阶段追踪、决策记录 |
| 发现文件 (`findings.md`) | 研究发现、技术决策 |
| 进度文件 (`progress.md`) | 会话日志、测试结果 |
| `init-session.sh` | 初始化计划文件 |
| `check-complete.sh` | 验证任务完成 |
| 模板系统 | 标准化文件格式 |
| 核心工作流 | Manus 原则 |

### 自动化功能（v3.1.0+）🤖

| 功能 | Claude Code | Cursor v3.0.0 | Cursor v3.1.0+ |
|------|-------------|---------------|---------------|
| 自动读取计划 | PreToolUse hook | ⚠️ 手动提醒 | ✅ **自动注入指令** |
| 自动更新提醒 | PostToolUse hook | ⚠️ 手动更新 | ✅ **自动检测修改** |
| 停止前验证 | Stop hook | ⚠️ 手动运行脚本 | ✅ **自动验证完成** |

**实现方式**:
1. **自动读取**: `planning-reminder.js` + `skill-activation.js` 在检测到计划文件时自动注入读取指令
2. **自动提醒**: `planning-update-tracker.js` 检测到 task_plan.md 修改时生成提醒
3. **自动验证**: `planning-reminder.js` 检测到所有阶段完成时自动运行验证脚本

### 不可用 ❌

| 功能 | 原因 |
|------|------|
| `session-catchup.py` | 依赖 `~/.claude/projects/` 存储路径 |
| 跨会话自动恢复 | Cursor 无等效存储机制 |

## 新增：planning-reminder Hook

为部分补偿缺失的 PreToolUse hook，我们创建了 `planning-reminder.js`：

**位置**: `.cursor/hooks/planning-reminder.js`

**功能**:
1. 检测项目根目录是否存在计划文件
2. 解析 `task_plan.md` 提取当前阶段和目标
3. 生成 `.cursor/context/planning-status.md` 状态摘要
4. 在 Cursor Output 面板输出提醒

**触发时机**: `beforeSubmitPrompt`（每次发送消息前）

**输出示例**:
```
[planning-with-files] Active: task_plan.md, findings.md
[planning-with-files] Reminder: Re-read task_plan.md before decisions.
```

## Cursor 推荐工作流

### 1. 会话开始

```bash
# 进入项目目录
cd /path/to/your/project

# 初始化计划文件（如果不存在）
sh .cursor/skills/planning-with-files/scripts/init-session.sh
```

### 2. 执行过程中

**手动执行（替代 PreToolUse hook）**：
```markdown
# 在做重大决策前，告诉 Agent：
"先读取 task_plan.md 刷新目标，然后再继续"
```

**使用 planning-reminder hook 生成的状态**：
```markdown
# 查看计划状态摘要
Read .cursor/context/planning-status.md
```

### 3. 完成阶段后

**手动更新计划**：
```markdown
# 告诉 Agent：
"更新 task_plan.md，将 Phase X 状态改为 complete"
```

### 4. 任务结束前

```bash
# 验证所有阶段完成（替代 Stop hook）
sh .cursor/skills/planning-with-files/scripts/check-complete.sh
```

## 与 Cursor Plan Mode 的关系

Cursor 在 2025年10月引入了原生 Plan Mode（Shift+Tab），与本 skill 有部分功能重叠：

| 使用场景 | 推荐方案 |
|----------|----------|
| 快速规划 | Cursor Plan Mode |
| 简单任务 | Cursor Plan Mode |
| 复杂多会话任务 | planning-with-files |
| 需要 findings.md | planning-with-files |
| 需要 progress.md | planning-with-files |
| 需要跨会话追踪 | planning-with-files |

**最佳实践**：两者结合使用
1. 用 Cursor Plan Mode 快速生成初始计划
2. 将计划转换为 `task_plan.md` 格式
3. 后续使用 planning-with-files 进行持久化追踪

## 文件结构

```
.cursor/
├── hooks/
│   ├── planning-reminder.js      # 新增：计划提醒 hook
│   ├── skill-activation.js       # 原有：skill 激活
│   └── context-tracker.js        # 原有：上下文追踪
├── hooks.json                    # 更新：注册 planning-reminder
├── context/
│   └── planning-status.md        # 自动生成：计划状态摘要
└── skills/
    └── planning-with-files/
        ├── SKILL.md              # 更新：v3.0.0-cursor
        ├── CURSOR-MIGRATION.md   # 新增：本文档
        ├── scripts/
        │   ├── init-session.sh   # 保留
        │   ├── check-complete.sh # 保留
        │   └── session-catchup.py # 保留（但标记不可用）
        └── templates/            # 保留
```

## 未来改进方向

1. **增强 planning-reminder hook**：
   - 检测长时间未更新计划
   - 自动提取 findings 数量变化
   - 集成到 skill-suggestions

2. **探索 Cursor 新 hooks**：
   - 关注 Cursor 是否会增加 beforeToolUse 类型 hook
   - 如有，可恢复自动化功能

3. **会话恢复替代方案**：
   - 基于 git log/diff 的恢复脚本
   - 基于计划文件时间戳的检测

## 问题排查

### Hook 未生效

1. 检查 `hooks.json` 是否正确注册：
   ```json
   "beforeSubmitPrompt": [
     { "command": "node .cursor/hooks/planning-reminder.js" }
   ]
   ```

2. 查看 Cursor Output 面板 → 选择 "Hooks"

3. 确认 Node.js 可用：
   ```bash
   node --version
   ```

### 计划状态未更新

1. 检查 `.cursor/context/planning-status.md` 是否存在
2. 手动运行 hook 测试：
   ```bash
   echo '{}' | node .cursor/hooks/planning-reminder.js
   ```

---

**版本**: 2026-01-27
**适用于**: Cursor IDE v2.0+
