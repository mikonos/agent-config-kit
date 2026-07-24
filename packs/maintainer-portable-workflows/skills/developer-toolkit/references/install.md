# developer-toolkit — 安装与环境

## OpenSpec

- **CLI**：`openspec --version` 应成功。
- **初始化**：`openspec init [项目路径]` 在项目目录生成 `.openspec/` 目录。
- **验证**：`openspec list` 查看当前变更提案。
- **若缺失**：`brew install openspec`（macOS）或 `npm i -g openspec`。

## gstack

- **就绪**：`~/.cursor/skills/gstack/SKILL.md` 存在（Cursor）；若只用 Claude Code，则为 `~/.claude/skills/gstack/SKILL.md`。
- **安装**：参考 gstack 官方文档。
- **Slash**：`/office-hours`、`/review` 等在已加载 gstack 的 Claude Code 会话中使用（Cursor 侧以 skill 名加载，无同名 slash 时以文档为准）。

## GSD（get-shit-done）

- **就绪**：本仓库存在 `.cursor/get-shit-done/workflows/`（随 `npx get-shit-done-cc@latest --cursor --local` 写入）。
- **与 developer-toolkit**：项目级节奏与验收走 GSD workflow；单条 OpenSpec change 仍走 OpenSpec；浏览器/QA/发版走 gstack。
- **安装**：`npx get-shit-done-cc@latest --cursor --local`（或 `--cursor --global`）。

## Superpowers

- **就绪**：通过 `skill-creator` 安装或手动 clone 到 `~/.cursor/skills/`（Cursor）或 `~/.claude/skills/`（Claude Code）。
- **激活**：使用 `Superpowers` 相关 skill 时直接按 skill 名加载。
