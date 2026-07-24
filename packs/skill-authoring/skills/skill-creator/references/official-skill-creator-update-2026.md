# Official skill-creator update (March 2026)

> 官方 2026 年 3 月对 skill-creator 的增强：Evals、Benchmark、多 Agent、description 调优。  
> 本文档为 SKILL.md 的参考资料，便于需要时查阅来源与细节。

---

## 来源

- **Blog**: [Improving skill-creator: Test, measure, and refine Agent Skills](https://claude.com/blog/improving-skill-creator-test-measure-and-refine-agent-skills) (March 3, 2026)
- **Plugin**: [Skill Creator – Claude Plugin](https://claude.com/plugins/skill-creator)
- **Repo (plugin)**: [anthropics/claude-plugins-official – plugins/skill-creator](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/skill-creator)
- **Repo (skill)**: [anthropics/skills – skills/skill-creator](https://github.com/anthropics/skills/tree/main/skills/skill-creator)

---

## 两类 Skill（与测试动机）

| 类型 | 说明 | 测试侧重 |
|------|------|----------|
| **Capability uplift** | 让 Claude 做基座模型做不好或做不稳的事（如文档生成技能） | 模型迭代后可能不再需要；evals 可判断基座是否已覆盖 |
| **Encoded preference** | 把已有能力按团队流程编排（如 NDA 审查、周报草稿） | 价值在于与真实流程一致；evals 验证是否贴合流程 |

---

## 四模式（Plugin）

| 模式 | 作用 |
|------|------|
| **Create** | 引导式创建新 skill（需求、结构、资源） |
| **Eval** | 编写并运行 evals：定义测试 prompt + 期望，得到通过/失败 |
| **Improve** | 根据 eval 结果给改进建议（质量回归、description 精度、A/B 对比） |
| **Benchmark** | 标准化评估；记录通过率、耗时、token 用量（可多轮跑并看方差） |

---

## Evals 要点

- **定义**：测试 prompt（可带文件）+「好结果」的判定方式；类似软件测试。
- **用途**：  
  - 发现质量回归（模型/基础设施变更后技能是否仍达标）。  
  - 对 capability uplift 类：若基座模型在不加载 skill 时也能通过 evals，说明技能可能已被模型吸收。
- **结果归属**：evals 与结果由用户保存（本地、看板或 CI）。

---

## 多 Agent 与 A/B

- **并行执行**：独立 agent 并行跑 eval，各自干净上下文，避免 run 间串扰；单独统计 token 与耗时。
- **Comparator**：盲测 A/B（两版 skill 或 skill vs 无 skill），判断哪个输出更好，用于确认改动是否有效。

---

## Description 调优

- 技能多了以后，description 过宽会误触发，过窄从不触发。
- skill-creator 可针对样本 prompt 分析当前 description，建议修改以降低误报和漏报。
- 官方在文档类技能上试验后，6 个里有 5 个触发表现有提升。

---

## 使用方式（Plugin）

- Claude Code 中安装插件后，用 `/skill-creator` 唤起，选择模式。
- 示例指令：  
  - "Create a new skill that reviews PRs for security issues"  
  - "Run evals on my code-review skill"  
  - "Improve my deploy skill based on these test cases"  
  - "Benchmark my skill across 10 runs and show variance"

---

## 与本仓库的对应关系

- 本仓库的 skill-creator 以 **SKILL.md + references + scripts** 形式存在，侧重「如何设计/写 skill、如何在本仓库归位与路由」。
- 官方插件提供 **Create / Eval / Improve / Benchmark** 的交互与自动化；若已安装插件，创建与测试可优先用四模式，本 skill 仍负责设计原则、目录结构、Cursor 适配（见 **cursor-workspace-adapter.md**）与迭代经验（见 **skill-iteration-lessons.md**）。
