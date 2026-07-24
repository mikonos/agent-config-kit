# Planning-with-Files 自动化功能说明

**版本**: v3.1.0-cursor  
**更新日期**: 2026-01-27

---

## 概述

v3.1.0 版本通过增强现有 hooks 系统，实现了原版 Claude Code 中 PreToolUse、PostToolUse 和 Stop hook 的自动化功能。

---

## 自动化功能对比

| 功能 | Claude Code 原版 | Cursor v3.0.0 | Cursor v3.1.0+ |
|------|-----------------|---------------|---------------|
| **注意力刷新** | PreToolUse hook 自动读取 | ⚠️ 需手动提醒 | ✅ **自动注入指令** |
| **更新提醒** | PostToolUse hook 自动提醒 | ⚠️ 需手动更新 | ✅ **自动检测修改** |
| **完成验证** | Stop hook 自动验证 | ⚠️ 需手动运行脚本 | ✅ **自动验证完成** |

---

## 实现机制

### 1. 注意力刷新（PreToolUse 替代）

**触发时机**: `beforeSubmitPrompt`（每次发送消息前）

**实现方式**:
1. `planning-reminder.js` 检测到 `task_plan.md` 存在
2. 生成 `.cursor/context/planning-auto-actions.md` 包含自动指令
3. `skill-activation.js` 检测到 `planning-with-files` skill 激活时，生成 `.cursor/context/planning-auto-instruction.md`
4. Agent 在回答前自动读取这些文件并执行指令

**生成文件**:
- `.cursor/context/planning-auto-actions.md` - 自动动作说明
- `.cursor/context/planning-auto-instruction.md` - 自动指令（当 skill 激活时）

**输出示例**:
```
[planning-with-files] 🤖 AUTO: Read task_plan.md before answering (PreToolUse simulation)
```

---

### 2. 更新提醒（PostToolUse 替代）

**触发时机**: `afterMCPExecution` / `beforeReadFile`（文件操作后）

**实现方式**:
1. `planning-update-tracker.js` 监听文件操作事件
2. 检测到 `task_plan.md` 被修改（通过文件修改时间戳）
3. 生成 `.cursor/context/planning-update-reminder.md` 提醒文件
4. Agent 在下次回答前自动检查提醒

**生成文件**:
- `.cursor/context/planning-update-reminder.md` - 更新提醒

**输出示例**:
```
[planning-with-files] 📝 AUTO: task_plan.md modified - check phase status (PostToolUse simulation)
```

---

### 3. 完成验证（Stop hook 替代）

**触发时机**: `beforeSubmitPrompt`（检测到所有阶段完成时）

**实现方式**:
1. `planning-reminder.js` 解析 `task_plan.md` 提取阶段状态
2. 检测到所有阶段状态为 `complete`
3. 自动运行 `check-complete.sh` 脚本验证
4. 在 `planning-auto-actions.md` 中生成验证结果

**生成内容**:
- 验证结果输出到 `planning-auto-actions.md`
- 控制台输出验证摘要

**输出示例**:
```
[planning-with-files] ✅ AUTO: All phases complete (Stop hook simulation)
[planning-with-files] Verification: Total phases: 5; Complete: 5; ALL PHASES COMPLETE
```

---

## 文件结构

```
.cursor/
├── hooks/
│   ├── planning-reminder.js          # 增强：自动注入指令 + 完成验证
│   ├── planning-update-tracker.js     # 新建：检测文件更新
│   └── skill-activation.js            # 增强：注入自动指令
├── hooks.json                         # 更新：注册新 hook
└── context/
    ├── planning-status.md             # 计划状态摘要
    ├── planning-auto-actions.md       # 自动动作说明
    ├── planning-auto-instruction.md   # 自动指令（skill 激活时）
    └── planning-update-reminder.md    # 更新提醒
```

---

## 使用方式

### 自动执行（无需手动干预）

1. **初始化计划文件**:
   ```bash
   sh .cursor/skills/planning-with-files/scripts/init-session.sh
   ```

2. **正常使用**:
   - ✅ 每次发送消息前，自动注入"读取 task_plan.md"指令
   - ✅ 检测到计划文件修改时，自动生成更新提醒
   - ✅ 所有阶段完成时，自动运行验证

3. **查看自动化状态**:
   - 查看 `.cursor/context/planning-auto-actions.md` 了解自动执行的动作
   - 查看 Cursor Output 面板的 Hooks 日志

### 仍需手动操作

- 更新阶段状态（`in_progress` → `complete`）
- 记录决策和错误到计划文件

---

## 技术细节

### Hook 执行顺序

```
beforeSubmitPrompt:
  1. skill-activation.js (skill 匹配)
  2. planning-reminder.js (计划检测 + 自动指令注入)

afterMCPExecution / beforeReadFile:
  1. context-tracker.js (文件追踪)
  2. planning-update-tracker.js (更新检测)
```

### 文件修改检测

使用文件修改时间戳（`mtimeMs`）检测：
- 记录上次检查时间到 `.cursor/context/planning-update-tracker.json`
- 如果文件修改时间 > 上次检查时间 + 1秒，触发提醒

### 完成验证触发条件

```javascript
phases.length > 0 && phases.every(p => p.status === "complete")
```

---

## 调试

### 查看 Hook 输出

1. 打开 Cursor Output 面板
2. 选择 "Hooks" 下拉菜单
3. 查看 `[planning-with-files]` 前缀的日志

### 检查生成的文件

```bash
# 查看自动生成的文件
ls -la .cursor/context/planning-*.md

# 查看更新追踪状态
cat .cursor/context/planning-update-tracker.json
```

### 手动测试 Hook

```bash
# 测试 planning-reminder
echo '{"workspace_roots": ["/path/to/project"]}' | node .cursor/hooks/planning-reminder.js

# 测试 planning-update-tracker
echo '{"workspace_roots": ["/path/to/project"], "hook_event_name": "afterMCPExecution"}' | node .cursor/hooks/planning-update-tracker.js
```

---

## 限制与注意事项

1. **文件修改检测精度**: 基于时间戳，可能有 1-2 秒延迟
2. **Hook 执行顺序**: 依赖 Cursor hooks 系统，顺序可能因版本变化
3. **跨会话状态**: 更新追踪状态文件在会话间保持，但不会自动恢复上下文
4. **性能影响**: Hook 执行时间 < 100ms，对用户体验影响可忽略

---

## 未来改进方向

1. **更精确的修改检测**: 使用文件内容哈希而非时间戳
2. **智能阶段识别**: 自动识别阶段完成并更新状态
3. **跨会话恢复**: 基于 git 的会话恢复方案
4. **可视化仪表板**: 计划进度可视化展示

---

**版本**: v3.1.0-cursor  
**最后更新**: 2026-01-27
