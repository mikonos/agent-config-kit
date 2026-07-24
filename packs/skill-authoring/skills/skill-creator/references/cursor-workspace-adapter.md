## Cursor 工作区适配层（本仓库专用）

> 本文件用于补齐官方 `skill-creator` 母版里**不存在**的“Cursor hooks + 路由规则”特殊性。  
> 目标：让“写一个 skill”在这个仓库里不仅能写出 `SKILL.md`，还能被 hooks 稳定命中。

---

## 1) Cursor hooks 到底做了什么（为什么你的 skill 必须“可路由”）

本仓库在 `.cursor/hooks.json` 配置了 hooks：

- `beforeSubmitPrompt`：运行 `.cursor/hooks/skill-activation.js`
  - 会读取 `.cursor/skill-rules.json`（fallback: `.claude/skills/skill-rules.json`）
  - 基于 **promptTriggers + fileTriggers** 给出“建议加载的 skills”
  - 写入 `.cursor/context/skill-suggestions.md`
- `beforeReadFile` / `beforeMCPExecution` / `afterMCPExecution`：运行 `.cursor/hooks/context-tracker.js`
  - 维护 `.cursor/context/active-files.json` / `active-files.md`

结论：**你的 skill 不注册到 skill-rules（promptTriggers/fileTriggers）就等于不存在**（系统无法稳定命中）。

---

## 2) 本仓库的“第三路由”：description 预加载信号（强烈建议）

虽然 hooks 主要靠 `skill-rules.json`，但本仓库的实践里：
- `SKILL.md` frontmatter 的 `description` 写得“可识别”，会显著提升预加载/选择时的命中率与稳定性。

推荐写法（可中英混用）：

```yaml
description: <做什么>。适用于<何时用/什么输入>（关键词：A/B/C）
```

最低要求：
- 有 WHAT（做什么）
- 有 WHEN（适用于… / Use when …）
- 含触发词（至少一个与路由规则关键词一致的词）

---

## 3) skill-rules.json 的最小可用条目（你需要确保这些字段存在）

在 `.cursor/skill-rules.json` 里新增条目时，至少要有：

- `promptTriggers.keywords`（非空数组）
- `promptTriggers.intentPatterns`（非空数组，regex）
- `fileTriggers.pathPatterns`（非空数组，glob）
- `resources.primary`：**必须是** `.cursor/skills/<skill-name>/SKILL.md`

> 注意：`skill-activation.js` 读取的是 `.cursor/skill-rules.json`。

---

## 4) 本仓库“创建 skill”的推荐策略（别再手工漏掉路由）

### 推荐
- 用本仓库版 `scripts/init_skill.py` 创建 skill 时，**默认会尝试注册到 `.cursor/skill-rules.json`**（可用 `--no-register` 跳过）。
- 新建 skill 时在 `SKILL.md` frontmatter 里加入：
  - `metadata.routing.requirePromptTriggers: true`
  - `metadata.routing.requireFileTriggers: true`
  - `metadata.routing.requireDescriptionRouting: true`
  
这样 `scripts/quick_validate.py` 会在校验阶段强制检查：
- 路由条目是否存在
- keywords/intentPatterns/pathPatterns 是否为空
- `resources.primary` 是否符合 `.cursor/skills/<name>/SKILL.md`
- description 是否包含 WHEN cue，且命中至少一个 keyword（预加载信号）

---

## 5) ZK core skill 额外要求

本仓库的 ZK core skills（产出笔记、操作知识网络的 skill）必须在 frontmatter 后第一行加入：

```markdown
> **通用协议**：执行前读取 `.cursor/skills/vault-writing-preamble/SKILL.md`（Iron Law、YAML 规范、indexed 标记、归位快查）。
```

**ZK core skills 列表**（需要 preamble）：
`deep-learning` · `deep-reading` · `file-organize` · `fleeting-note` · `index-note` · `link-proposer` · `meeting-note` · `network-health` · `note-split` · `obsidian-cli` · `open-loops` · `random-walk` · `strategic-advisor` · `structure-note` · `weekly-report`

**新建 ZK skill 时**：写完 frontmatter 后立即加这行，再写 body。

**批量修复存量**：
```bash
python3 .cursor/skills/skill-creator/scripts/add_zk_preamble.py
```
脚本会自动扫描 ZK_SKILLS 列表，仅补入缺失的声明行，已有的跳过。新增 ZK skill 时记得同步更新脚本里的 `ZK_SKILLS` 列表。

---

## 6) 常见坑与修复

- **坑：只写了 `SKILL.md`，没注册 skill-rules**  
  - 现象：hooks 永远不会建议加载该 skill  
  - 修复：补 `.cursor/skill-rules.json` 条目；再跑 `scripts/quick_validate.py <skill_dir>`

- **坑：resources.primary 写成 `_系统/.../SKILL.md`**  
  - 现象：路由/加载链路断裂（系统期望 `.cursor/skills/...`）  
  - 修复：强制改为 `.cursor/skills/<skill-name>/SKILL.md`

