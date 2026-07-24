# JTBD 归位与入网规则

> 本文档提供 JTBD 桌面研究产出物的归位路径与入网方法。

---

## 归位规则

### 文件存放位置

**所有产出物默认位置**：`05_每日记录/YYYY/MM/YYYYMMDD/`

**文件命名规范**：
- 执行计划：`YYYYMMDD_Agent执行计划_JTBD桌面研究_[产品名].md`
- 原始引用库：`JTBD_RawQuotes_[产品名].md`
- 分析报告：`JTBD_Analysis_[产品名].md`
- 精选集：`JTBD_TopQuotes_[产品名].md`

### 示例

```
05_每日记录/2026/03/20260311/
├── 20260311_Agent执行计划_JTBD桌面研究_product门厅镜.md
├── JTBD_RawQuotes_productMirror.md
├── JTBD_Analysis_productMirror.md
└── JTBD_TopQuotes_productMirror.md
```

---

## 入网规则

### 1. 项目索引入网

**适用场景**：研究针对特定产品/项目

**操作步骤**：
1. 找到项目索引（如 `索引_product`、`索引_V7Max`）
2. 在索引中添加入口：
   ```markdown
   ## JTBD 研究
   - [[20260311_Agent执行计划_JTBD桌面研究_product门厅镜]] — 门厅镜用户声音采集，验证 J1-J4 假设，20260311
   - [[JTBD_Analysis_productMirror]] — 分析报告：Job 验证、四力、Workaround、雇用解雇
   - [[JTBD_TopQuotes_productMirror]] — 精选引用 43 条，供访谈与文案使用
   ```
3. 在产出文件底部反链项目索引

---

### 2. 方法索引入网

**适用场景**：所有 JTBD 研究

**操作步骤**：
1. 找到方法索引（如 `索引_产品方法论`）
2. 在"JTBD / 用户研究"区域添加入口：
   ```markdown
   ## JTBD / 用户研究
   - [[20260311_Agent执行计划_JTBD桌面研究_product门厅镜]] — product 门厅镜案例，完整执行计划与产出
   ```
3. 在产出文件底部反链方法索引

---

### 3. 调用 link-proposer 建立连接

**操作步骤**：
1. 对每个产出文件调用 `link-proposer`
2. 建立与现有笔记的连接（三路搜索：语义/时间邻近/反相关）
3. 在产出文件底部添加"相关笔记"区域

**示例**：
```markdown
---

**相关笔记**：
- [[20260311_方法_JTBD用户画像模板]] — 用于填充画像
- [[20260311_CEO战略日志_product首品方向推进]] — 用于战略决策
- [[20260228_08_Job_Story构建方法]] — Job Story 方法论
```

---

## 入网检查清单

### 必做

- [ ] 在项目索引中添加入口（如适用）
- [ ] 在方法索引中添加入口
- [ ] 产出文件底部反链索引
- [ ] 调用 `link-proposer` 建立连接

### 可选

- [ ] 在竞品索引中添加入口（如研究涉及竞品）
- [ ] 在用户研究索引中添加入口（如有专门的用户研究索引）

---

## 日记录更新

### 格式

```markdown
### [YYYYMMDD] JTBD 桌面研究 — [产品名]

- **Intent**：[研究目的]
- **Changes**：
  - 产出执行计划：[[执行计划文件名]]
  - 产出原始引用库：[[RawQuotes 文件名]]（X 条引用）
  - 产出分析报告：[[Analysis 文件名]]（Job 验证/四力/Workaround/雇用解雇）
  - 产出精选集：[[TopQuotes 文件名]]（X 条精选）
  - 入网：项目索引 + 方法索引
- **Open loops**：[未闭环事项，如需补充数据、访谈验证等]
```

---

**相关文档**：
- `execution_plan_template.md` - 执行计划模板
- `quality_checklist.md` - 质量审查清单
