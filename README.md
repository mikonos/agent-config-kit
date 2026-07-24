# Agent Config Kit

一套让 AI 新手直接开工的项目级配置。它包含：

- Rule：Agent 做事时始终遵守的工作约定；
- Skill：阅读、研究、计划、写作、验收和知识管理流程；
- Safe Hook：会话开始时提醒 Agent 使用这些流程，不读取或保存 prompt。

所有安装和维护都从 `install/SKILL.md` 进入，不需要先学会命令行。

## 五分钟开始

1. 准备一个真正要使用 AI 的目标项目文件夹；没有项目时可以先建一个空文件夹。
   本仓库只是安装源，不要把配置安装回本仓库根目录。
   不知道完整路径时，让 Agent 指导你从系统文件管理器复制路径，不要猜。
2. 用你正在使用的 Codex、Cursor 或 Claude Code 打开本仓库，把下面这句话里的
   应用名和目标路径替换成自己的：

   ```text
   请读取 install/SKILL.md。我正在使用 Codex，请把 daily-work 配置安装到【目标项目的完整路径】。先验证配置包并展示 dry-run，用中文解释会改什么；不要应用，等我确认。
   ```

3. 让 Agent 先按配置分组、Skill 数量、依赖和冲突汇总预览；需要时再展开
   文件明细。确认没有 `conflict` 后说：

   ```text
   按刚才完全相同的目标、Runtime、profile 和 Hook 选择执行安装，完成后运行 doctor。
   ```

4. 用所选应用打开目标项目，说：

   ```text
   请确认 Agent Config Kit 是否已加载，并告诉我处理“整理一篇资料”会选择哪个工作流。
   ```

想一次装上目前全部可直接交付的内容，可复制：

```text
请读取 install/SKILL.md。我正在使用 Codex，请把 full 安装到【目标项目的完整路径】，并额外安装 lark-official 27 个飞书官方 Skill。分别验证、预览并解释两个阶段；不要应用，等我逐段确认。安装完成后运行两个 doctor。
```

Codex 第一次加载项目 Hook 时，还要信任项目并在 `/hooks` 中审查、启用该
Hook；未完成这一步时 Rule 和 Skill 仍可用，但 Hook 会被跳过。

## 选择配置包

- `daily-work`：读资料、做研究、制定计划、写作和验收；新手默认选它。
- `knowledge-vault`：包含 `daily-work`，再增加卡片盒工作流和 5 个官方
  Obsidian Skill。
- `full`：安装当前全部已通过来源、许可和敏感信息审查的 Skill。它包含实验性
  和上游已标记 deprecated 的独立分组，也包含一个明确标记的非商业产品管理
  分组，不是新手默认档。

要完整安装时，把五分钟开始中的 `daily-work` 换成 `full`。`full` 表示
“当前 Catalog 中全部获准分发的 Skill”，不包含平台内置 Skill、许可证禁止
再分发的内容，也不会复制虚拟环境、依赖缓存、账号或个人路径。

“全部”有一份可检查的逐项账本：
[`catalog/local_release_inventory.json`](catalog/local_release_inventory.json)。
最初 443 个入口对应的 398 个唯一候选全部有最终去向：270 个已进入公开包，
27 个改由安装器从官方来源获取，101 个因平台内置、仅为嵌套子组件、私有项目、
旧副本、许可、安全或可移植性边界而明确不分发，没有待审条目。其中 42 个
私有项目候选只以匿名编号、数量和排除理由记账，不公开原名。363 个是顶层候选，
另外 30 个只在其他 Skill 内嵌套出现，5 个只来自平台 `.system`。
公开 Catalog 另有 18 个经许可引入、但不在原始 398 名称中的 Skill；其中一个
是本项目为大目录渐进加载新增的 `all-skills-router`。因此 `full` 实际随包安装
288 个：287 个工作 Skill 加一个总目录路由 Skill；再安装 `lark-official`
后，共有 315 个可安装 Skill。
账本公布非私有名称、匿名私有条目、去向、理由和替代项，不公布私有项目原名、
本机路径、内容哈希或私有审计信息。
随包分发的 288 个 Skill 另有统一机器目录
[`catalog/skill_catalog.json`](catalog/skill_catalog.json)，逐项记录打包路径、
来源归属、许可证、分类、适用 profile、操作系统限制、命令/环境变量/连接依赖、
潜在副作用信号和是否默认安装。

`full` 中的 `product-management-noncommercial` 分组采用 CC BY-NC-SA 4.0：
只允许非商业使用和分享，并要求署名、相同方式共享。安装器会在预览和应用时
显示这条提醒；如果朋友准备把配置用于公司或收费业务，不应安装 `full`，先用
`daily-work` 或 `knowledge-vault`。

`full` 中的 `generated-investing-perspectives` 分组包含 26 个基于公开资料生成
的人物投资视角。它们是 AI 模拟，不代表相关人物本人，也不构成金融或投资建议；
该分组不进入新手默认配置。

`full` 中的金融研究分组只用于学习和结构化复盘，不提供投资建议、具体买卖
指令或收益承诺。行情数据和实际决策必须独立核验。

`full` 中的 `generated-domain-perspectives` 分组包含 25 个基于公开资料生成的
设计、产品、社会科学与思想人物视角。它们是 AI 模拟，不代表相关人物本人；
涉及当前事实、医疗、法律、金融或其他高风险判断时仍需独立查证。公开包保留
运行所需核心 Skill 与少量路由/校准材料，不带生成过程日志和完整内部调研草稿。

`full` 中的浏览器控制分组可能复用浏览器登录态。安装文件不等于
账号已连接；发布、发送、删除、购买或修改外部数据前，必须再次确认具体账号、
目标和内容。

`full` 中的发布管理分组可以生成版本变更、commit 和 tag；只有用户明确确认后
才能 push 或发布。缺少 Git 时，doctor 会把文件安装与功能可用分开报告。

`full` 中的 GitHub 自动化分组可以从 issue 创建分支、commit、PR 和回复 review；
必须先由用户选定具体 issue 或 PR。公开版移除了 OpenClaw 账号读取、无人值守
cron 和跳过确认的选项。

`full` 中的实验性自我改进分组只在用户明确调用时运行，并把状态保存在所选
项目内。它不会安装后台任务；安装或更新依赖、Skill，修改 Agent 配置、Rule、
Hook 或计划任务，运行非只读命令，删除文件或写外部系统，都必须先展示精确
变更并再次获得用户批准。

`full` 中的 Amazon Listing 工作流只生成证据表、候选文案、lint 报告和人工
审核包；写入 Seller Central、广告、评论、问答或生产目录，必须另行明确授权并
由人类审核。

`full` 中的 JTBD 评论研究工作流不附带真实顾客评论、私有 prompt 或内部项目
路径。使用者只应处理自己有权使用的数据；清洗与审计脚本可直接运行，自动批量
调用模型的 runner 目前还需要 Cursor Agent 的 `agent` CLI。

`knowledge-vault` 与 `full` 中的知识库治理工作流默认先给预览。移动文件、批量
改写链接，以及每一份精确删除清单，都必须在执行前获得用户明确确认。

`full` 中的 Reddit 研究工作流只允许观察、透明参与和平台付费放大；不做垃圾
发布、隐藏利益关系、刷票或绕开平台条款。自动化或商业数据使用前必须重新核对
Reddit 当前官方政策。

`full` 中的传统文化分组只用于文化理解和结构化反思，不是经过科学验证的预测
工具；不得用它指导医疗、法律、金融、安全、心理健康或其他高风险决定。

如果你说“把能用的都装上”，Agent 会分两段执行：先安装 `full`，再单独预览
`lark-official`。后者包含 27 个飞书官方 Skill，不保存在本仓库里，而是从
`open.feishu.cn` 读取；安装器会核对固定 SHA-256 和 Skill 名称，官方内容一旦
变化就停止，等待维护者重新审核。两段各自确认、各自记录安装状态，也能分别
检查、卸载和恢复。

你正在使用哪个应用，就选择同名 Runtime：`codex`、`cursor` 或
`claude-code`。

## 遇到冲突

安装器遇到任一冲突会整批停止，不会先写一半：

- Hook 配置冲突：说“保留原 Hook，不安装本套 Hook，请重新预览”；Agent 会
  使用 `--without-hooks`。
- `AGENTS.md` 或 `CLAUDE.md` 冲突：让 Agent 只生成差异和人工合并建议，
  或改用空白目标；安装器不自动合并。
- 同名 Skill 冲突：保留原 Skill，先决定保留哪一份；没有 `--force`。

新手默认保留 Safe Hook。原生 Windows v0.1 请使用 `--without-hooks`；
Rule、Skill 和安装生命周期仍受 CI 验证。Hook 当前支持 macOS、Linux 和 WSL，
且要求 `python3` 在 PATH 中。

## 维护与恢复

仍然让 Agent 读取 `install/SKILL.md`，然后用自然语言说：

```text
检查这套配置
预览更新这套配置
预览卸载这套配置
恢复上一次卸载
```

安装、更新、卸载和恢复默认都只是 dry-run。卸载会先把将删除的 owned 文件
复制到 `.agent-config-kit/recovery/...`；`restore` 只恢复缺失且哈希匹配的
备份，遇到新文件或改动会停止。

`doctor` 会分别报告文件状态、Hook 状态、Runtime 命令是否在 PATH、以及各
Skill 声明的命令和环境变量依赖；环境变量只报告存在与否，不输出值。它不会
把“文件已安装”写成“账号已连接”或“真实任务已通过”；后两项仍需在朋友
自己的 Runtime 和账号中验证。

## 支持范围

| Runtime | Rule | Skill | Safe Hook |
|---|---:|---:|---|
| Codex | yes | yes | macOS/Linux/WSL；首次需在 `/hooks` 信任 |
| Cursor | yes | yes | macOS/Linux/WSL |
| Claude Code | yes | yes | macOS/Linux/WSL |
| 原生 Windows | yes | yes | v0.1 使用 `--without-hooks` |

本仓库不包含账号配置、MCP 凭证、个人记忆、GTD 状态或后台自动化。Hook
只输出固定提示，不联网、不写日志，也不扩大 Agent 权限。

## 发布前验证

```bash
python3 scripts/build_adapters.py --check
python3 scripts/build_full_router_index.py --check
python3 scripts/build_skill_catalog.py --check
python3 scripts/check_semantic_privacy.py
python3 scripts/check_sensitive_reviews.py
python3 scripts/live_runtime_smoke.py check-contract
python3 scripts/check_admissions.py --require-full
python3 scripts/check_local_release_inventory.py
python3 scripts/verify.py
python3 install/scripts/externalctl.py verify-catalog
python3 -m unittest discover -s tests -v
```

Windows 可把 `python3` 换成 `py -3`。这些检查证明包结构和文件生命周期
正确，不等于商业 Runtime 的真实账号会话已经加载。真实测试必须在全新项目、
只读模式且只允许读取 Skill 文件的会话中运行
[`scripts/live_runtime_smoke.py`](scripts/live_runtime_smoke.py) 生成的同一份
四场景测试；具体步骤见
[`install/references/commands.md`](install/references/commands.md#live-runtime-smoke)。
