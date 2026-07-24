# Expert Routing

## 默认座席

| 研究层 | 默认专家 | 用法 |
|---|---|---|
| 行业结构 | Michael Porter | 五力、价值链、利润池、进入壁垒、替代品 |
| 工作流 | Andrej Karpathy | 把研究拆成可执行 agent 循环，先建框架再填样本 |
| 机会验证 | Clayton Christensen + Bob Moesta | JTBD、雇用/解雇时刻、替代方案 |
| 产品发现 | Teresa Torres | 机会树、假设、实验优先级 |
| 定位与品类 | April Dunford | 竞争参照、差异化、品类叙事 |

## 领域替换

| 行业/问题 | 优先专家 | 触发时怎么用 |
|---|---|---|
| AI/ML/开发者工具 | Andrej Karpathy | 系统结构、技术路线、开发者工作流 |
| B2B SaaS / 企业软件 | April Dunford + Geoffrey Moore | ICP、品类、采购路径、跨越鸿沟 |
| 消费品 / DTC / 零售 | Bob Moesta + Byron Sharp | 购买触发、复购、心智可得性、渠道 |
| 市场营销 / 内容生态 | David Ogilvy + Seth Godin | 广告诉求、内容传播、社群 |
| 投资 / 资本市场 | Howard Marks + Michael Porter | 周期、风险、竞争结构；必须核验最新数据 |
| 平台 / 网络效应 | Ben Thompson + Porter | 聚合理论、供需两边、分发控制点 |
| 监管强行业 | 领域监管专家 + 官方来源 | 医疗、金融、教育、法律等必须查当前法规 |
| 用户需求不明 | Christensen + Bob Moesta | 先做 JTBD，不急着画 TAM |
| 产品机会排序 | Teresa Torres | 机会树、假设、实验、证据强度 |

## Skill 调用规则

1. 若本仓库已有对应 `*-perspective` skill，读取该 skill 后再研究。
2. 若没有对应 skill，但任务复杂、高风险、跨多个行业，启用 readonly subagent 独立输出“专家审查”。
3. 若只是 60 分钟入门，主 agent 可以直接模拟专家框架，但输出必须出现具体方法，例如 Porter 五力或 Dunford 定位四要素。
4. 若结论涉及医疗、法律、金融、政策、实时价格、公司人物、监管变化，必须联网查官方或一手来源。

## 专家输出最小格式

```markdown
## Expert Lens

- 本轮采用：[专家 A] + [专家 B]
- 为什么是他们：
- 使用的框架：
- 他们会反对的直觉结论：
- 对研究计划的改动：
```
