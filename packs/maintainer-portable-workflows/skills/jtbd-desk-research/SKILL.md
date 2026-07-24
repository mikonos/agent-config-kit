---
name: jtbd-desk-research
description: JTBD desk research and analysis. Use when doing secondary research for jobs-to-be-done analysis.
---

# JTBD 桌面研究 (JTBD Desk Research)

> **核心理念**：People don't buy products, they hire them to make progress in their lives. — Clayton Christensen & Bob Moesta

## 专家座席 (The Council)

1. **Bob Moesta** (The Detective): 负责挖掘雇用/解雇时刻、切换时间线、四力分析。
2. **Clayton Christensen** (The Theorist): 负责 Job Story 框架、进展力量理论。
3. **April Dunford** (The Strategist): 负责竞争地图、差异化洞察。
4. **Niklas Luhmann** (The Librarian): 负责知识入网、连接发现。

---

## 核心法则 (The Iron Rules)

1. **原文保真 (Quote Fidelity)**: 用户原话必须完整引用，不得改写或总结替代。分析和推断放在备注或报告中。
2. **URL 可追溯 (Traceability)**: 每条引用必须有来源 URL（如可获取），便于人工复核。
3. **四力必标注 (Forces Tagging)**: 每条引用必须标注 Push/Pull/Anxiety/Habit 中的至少一个。
4. **反证必采集 (Counter-evidence)**: 反证样本（不认同问题、满意现状、质疑方案）应占 15-30%，避免确认偏误。
5. **时间线必追踪 (Timeline Tracking)**: 重点挖掘雇用时刻（什么触发？）、解雇时刻（为何放弃？）。
6. **Job Statement 证据层 (Evidence Layer)**: 评论/桌面材料不能直接写成产品机会；先还原为 Job Statement 九格，并标证据等级 A/B/C/H。

---

## 工作流程 (The Workflow)

**执行顺序**：Phase 0 → 1 → 2 → 3 → 4 → 5 → **6（流程执行审查，强制）**，不可跳步；Phase 6 必须由独立 readonly subagent 执行。

> **扩展模式（全量批处理）**：当评论量很大、需要”每条可追溯证据”、或需要 Obsidian block 级跳转与全量统计时，使用扩展 skill：`jtbd-amazon-corpus`（全量 RawQuotes + Structured CSV 双轨 + 9阶段流水线 + QuantAnalysis）。

### Phase 0: 研究设计 (Research Design)

**Agent**: Bob Moesta + Clayton Christensen

**输入要求**：
- 产品假设或研究问题
- 目标用户群体
- 核心 JTBD 假设（J1, J2, J3...）

**产出**：执行计划文档 `YYYYMMDD_Agent执行计划_JTBD桌面研究_[产品名].md`

**必须包含**：
1. 背景与研究问题（产品假设、JTBD 假设、研究问题）
2. JTBD 提取框架（引用格式、四力识别、信号类型）
3. 数据源与采集任务（Batch 1-6 任务包）
4. 产出物规格（原始引用库、分析报告、精选集）
5. 执行节奏与时间箱（2 天采集 + 1 天分析）
6. 质量控制原则（8 条原则）

**详细模板**：`references/execution_plan_template.md`

---

### Phase 1: 数据采集 (Data Collection)

**Agent**: Bob Moesta (The Detective)

**任务**：按执行计划的 Batch 1-6 顺序，从各平台采集用户原声。

**产出**：`JTBD_RawQuotes_[产品名].md`（≥50 条引用，按 Batch 组织）

**详细采集策略**：`references/data_collection.md`
- Reddit/Amazon/论坛/App Store/YouTube 采集方法
- 提取格式与标注规范
- 质量检查清单

---

### Phase 2: Job Story 验证 (Job Validation)

**Agent**: Clayton Christensen (The Theorist)

**任务**：基于原始引用库，验证执行计划中的 JTBD 假设（J1, J2, J3...）。

**产出**：`JTBD_Analysis_[产品名].md` 的 **3.1 Job Story 验证结论** 部分

**详细验证框架**：`references/job_validation.md`
- 验证状态判断标准（强验证/弱验证/未验证/反证）
- Job Story 标准格式
- Job Statement 九格与证据等级
- 质量检查清单

---

### Phase 3: 四力分析 (Forces Analysis)

**Agent**: Bob Moesta (The Detective)

**任务**：从原始引用中提取四力信号，绘制进展力量图谱。

**产出**：`JTBD_Analysis_[产品名].md` 的 **3.2 四力图谱** 部分

**详细分析方法**：`references/forces_analysis.md`
- 四力定义与识别关键词
- 提取框架与格式
- 强度对比方法
- 质量检查清单

---

### Phase 4: Workaround 目录 (Workaround Catalog)

**Agent**: Bob Moesta + April Dunford

**任务**：梳理用户当前的解决方案（workaround），分析失败原因，识别真正的竞争对手。

**产出**：`JTBD_Analysis_[产品名].md` 的 **3.3 Workaround 目录** 部分

**详细提取框架**：`references/workaround_catalog.md`
- Workaround 定义与识别
- 竞争地图绘制（直接/间接/非消费）
- 失败原因分析
- 质量检查清单

---

### Phase 5: 雇用/解雇时刻 (Hiring/Firing Moments)

**Agent**: Bob Moesta (The Detective)

**任务**：挖掘用户的切换时间线，找到雇用时刻（什么触发？）和解雇时刻（为何放弃？）。

**产出**：`JTBD_Analysis_[产品名].md` 的 **3.4 雇用/解雇时刻** 部分

**详细挖掘方法**：`references/hiring_firing.md`
- 雇用时刻识别（触发事件、时间线、决策理由）
- 解雇时刻识别（放弃原因、时间线、临界点）
- 切换时间线绘制
- 质量检查清单

---

### Phase 6: 流程执行审查 (Quality Audit · subagent 强制)

**Agent**: 德明 + 葛文德（审查专家）

**任务**：启动独立 readonly subagent，用质量审查清单检查 Phase 0-5 的完成度，产出审查报告；主 agent 不得自评替代。

**产出**：审查报告（Phase 0-5 完成度、质量评分、改进建议、P0/P1/P2 问题清单）。对 P0/P1 项，主 agent 必须补执行后再宣告完成。

**审查清单**：`references/quality_checklist.md`
- Phase 0-5 审查清单
- A/B+/C 级质量标准
- Job Statement 六类 lint
- 常见问题与改进建议

---

## 归位与入网

**归位规则**：
- 执行计划、原始引用库、分析报告、精选集 → `05_每日记录/YYYY/MM/YYYYMMDD/`
- 文件命名：`YYYYMMDD_[类型]_[产品名].md`

**入网规则**：
1. 在项目索引中添加入口（如 `索引_product`）
2. 在方法索引中添加入口（如 `索引_产品方法论`）
3. 调用 `link-proposer` 建立与现有笔记的连接

**详细规则**：`references/filing_rules.md`

---

## 与其他 Skill 的协作

- **strategic-advisor**: 研究设计阶段，确定研究问题和假设
- **link-proposer**: 入网阶段，建立与现有笔记的连接
- **index-note**: 创建/更新 JTBD 方法索引、项目索引
- **meeting-note**: 将研究结果用于团队讨论、与合伙人对齐
- **structure-note**: 将研究结果整理成可对外分享的文章

---

## 参考资料 (References)

**方法论详解**：
- `references/execution_plan_template.md` - 执行计划模板
- `references/data_collection.md` - 数据采集策略
- `references/job_validation.md` - Job 验证框架
- `references/forces_analysis.md` - 四力分析方法
- `references/workaround_catalog.md` - Workaround 提取框架
- `references/hiring_firing.md` - 雇用/解雇时刻挖掘
- `references/quality_checklist.md` - 质量审查清单
- `references/filing_rules.md` - 归位与入网规则
- `references/jtbd_theory.md` - JTBD 理论基础
- `.cursor/skills/jtbd-result-audit/references/job_statement_quality_gate.md` - Job Statement 九格、证据等级与六类 lint

**实践案例**：
- [[20260311_Agent执行计划_JTBD桌面研究_product门厅镜]]
- [[JTBD_Analysis_productMirror]]
- [[JTBD_TopQuotes_productMirror]]

---

**Skill 版本**：v2.0（激进重构版）
**创建日期**：2026-03-12
**最后更新**：2026-03-12
**维护者**：老板 + Claude Code
