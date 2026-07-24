---
title: 测试用例设计研究 01｜Cem Kaner
type: research
date: 2026-04-23
---

# Cem Kaner

## 核心来源

- `kaner.com` Publications 页
- `Testing Computer Software`
- `What is a Good Test Case?`
- `Scenario-Driven Testing`
- `Bug taxonomies: Use them to generate better tests`
- `Black Box Software Testing: Test Design Course`

## 对测试用例设计最关键的贡献

### 1. 好用例不是步骤整齐，而是更容易暴露重要问题

- Kaner 的重心不是格式，而是杀伤力。
- 在他的体系里，测试用例设计首先服务于发现高价值缺陷，而不是服务于文档合规。

### 2. 测试用例必须围绕风险、场景与错误模式展开

- 他长期强调 `scenario-driven testing`。
- 他不是只问“这个功能应该怎么走”，而是问：
  - 用户会怎么用
  - 用户会怎么误用
  - 产品在哪些场景下最脆弱
  - 哪类缺陷最值得优先寻找

### 3. bug taxonomy 可以反过来驱动用例设计

- 他的一个强贡献是把缺陷模式当成设计输入。
- 不是先机械写 case，再等缺陷出现，而是先问历史上这类产品常怎么坏。

### 4. 用例设计要接受不确定性

- 他不像一些纯技术流派那样追求“列举完所有逻辑组合”。
- 他更承认：测试设计是在有限时间里，用启发式方式最大化发现价值。

## 对综合 skill 的启示

- Kaner 这条线负责：`风险优先`、`场景优先`、`缺陷模式优先`
- 他是这个主题 skill 里最像“现实世界用例设计总教练”的那个人
