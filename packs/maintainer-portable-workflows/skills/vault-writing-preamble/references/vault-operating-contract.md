# Vault Operating Contract

> **角色**：本文件是低频 Vault 细节的 execution truth；`AGENTS.md` 只保留触发与权限，`vault-writing-preamble/SKILL.md` 保留高频快速合同。普通回答、审查、诊断不加载本文件，也不因此产生写入。

## 工作区与归位

| 路径 | 角色 |
|---|---|
| `000_收件箱/` | 闪念、未消化输入 |
| `00_收件箱_工作区/projects/[项目名]/` | 用户明确命名项目的项目文档 |
| `03_索引/` | MOC 与问题入口 |
| `04_compiled-wiki/` | 编译 / 当前共识层，不是原始证据 |
| `05_每日记录/YYYY/MM/YYYYMMDD/` | 其他知识笔记的默认落点 |
| `memory/daily/<machine-id>/YYYY-MM-DD.md` | 明确要求或 workflow 要求的人工 / 技能日志 |
| `memory/` 其他目录 | 运营记录，不进入知识图谱 |

- 文件名：`YYYYMMDD_具体描述.md`。
- 位置服从用户指定与局部规则；不确定的知识笔记默认进 `05_每日记录/`，靠链接和索引找回。
- 修改 `04_compiled-wiki/` 前，先读主题目录的 `AGENTS.md`、`schema.md`、`index.md`，并回到 raw notes / 索引 / 项目真源核对；compiled page 不能充当原始证据。
- daily 路径只用 `node .cursor/scripts/print-daily-memory-path.js` 解析；该命令只打印路径，不创建目录或文件。

## 知识网络写入闭环

仅在用户已授权创建或修改 Vault 知识笔记时执行：

1. 用 `file-organize` 决定路径，位置问题不压过连接质量。
2. 用 `luhmann-perspective` 判断可接续性、差异、稀疏指针、偶遇与生命尺度。
3. 用 `link-proposer` 先读关键词总表，再建立至少 2 条可验证连接；双向链接必须在两端都能检索到。
   正文提到已核实存在的具体笔记时，直接写成 `[[笔记名]]` 可点击链接，不只写纯文本标题。
4. 关键词入口目标 1–2 个，3 个可接受；4–5 个应收敛，>5 个警告。关键词必须回答一个查找问题，不是分类标签。
5. 入网校验通过后写 `indexed: true`；不要在正文末尾另写“归网：✅”。新笔记 30 天内可暂时孤岛，但必须记录已执行的检索与待补链。
6. `index-note` 负责索引创建 / 归网，`network-health` 负责观测，`random-walk` 只在用户明确要求或已授权 workflow 调用时运行；普通任务不按隐藏频率自动漫游。

五层关系：产出进入每日记录 → 已授权时即时入网 → `index-note` 每日归网兜底 → `network-health` 只观测 → 明确修复任务再改网络。观测不能静默升级为修复。

## Vault L1 记忆合同

只有任务明确包含记忆更新时才写；普通回答、审查、诊断不写。

- `memory/topics/<machine-id>/{user,project,feedback,reference}.md`：稳定协作态、项目决策、反馈规则和外部短指针；根 `MEMORY.md` 只保留稀疏索引。
- `feedback` / `project` 条目必须有规则或事实、独立 `Why`、独立 `How to apply`；相对日期先改为绝对日期。
- `user` 只写协作相关画像，不作负面判断；`reference` 只写可检索短指针，不搬正文。
- `affect.md` 只写短时协作情绪 / 节奏，不作临床诊断；`vault.md` 只写 `[[笔记链接]]` + 一句 hook，不复制知识正文。
- 禁存：可从仓库 / git / 规则推出的信息、活动流水、瞬时任务状态。
- L1 中可验证断言在使用前轻量复核；冲突时以当前观测为准。
- 知识真源在笔记与索引。能被 MOC 找到的内容不写进 L1 长段落；单主题超过 200 行或检索噪声过大时才拆分，并在 `MEMORY.md` 留一行指针。

Codex 原生 memories 与 Vault L1 并行，但都不获得普通回答的隐式写入授权；显式用户指令和当前工作区真源优先。

## 历史数据修复

仅在明确修复历史 frontmatter 时使用 `tools/migrate_frontmatter_keys_en.py` 与 `tools/restore_epistemic_enum_en.py`；不要再用会把键改成中文的 `tools/migrate_frontmatter_zh.py`。
