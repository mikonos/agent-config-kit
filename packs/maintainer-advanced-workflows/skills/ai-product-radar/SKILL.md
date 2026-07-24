---
name: ai-product-radar
description: 小众 AI 产品机会雷达。扫描小众/利基市场的高情绪痛点，按透明可复现公式评分，产出三件套——信号采集文档 + 机会报告（决策优先 + 内置证伪）+ 交互式四象限气泡雷达图（ECharts HTML，由脚本确定性生成）。Use when 用户要找小众 AI 产品机会、micro-SaaS / 出海 App 选题、B2C 订阅 App 机会扫描、习惯/生产力/ADHD/心理健康等赛道的需求挖掘与竞品缺口分析，或说"产品雷达/机会雷达/雷达扫描/选品/找需求/有什么 App 值得做/这个赛道还有什么机会"。关键词：ai-product-radar、产品雷达、机会雷达、小众AI产品、micro-SaaS、出海App选题、B2C订阅、需求挖掘、选品、机会评分。
---

# 小众 AI 产品机会雷达

把"小众市场里的高情绪抱怨"炼成"可 vibe-code 的 B2C 订阅 AI micro-app 机会"。一次扫描产出三件套：
**①信号采集文档 ②机会报告（决策优先）③交互式四象限雷达图**。三者数字由同一份评分驱动，永不脱钩。

> 核心心法（贯穿全程）：**内容验证先于产品构建** · 新手引导占成败 70% · 强制付费墙验真实意愿 · 30 天验证截止 · 把 App 当数字房产。

## 模式速选（先确认再执行）

| 模式 | 触发 | 信号数 | 深档 | 跳过 |
|---|---|---|---|---|
| 🏃 快速扫描 | "快速/先看看" | 5–8 | 仅 Top1 | GTM 细节、系统化 |
| 📋 标准（默认） | 默认 | 8–12 | Top1–2 | 无 |
| 🔬 深度 | "详细/完整/多赛道" | 12+ | Top2 + 全 GTM | 无；增竞品深挖、系统化数据库 |

> **前置依赖**：实时联网采集（WebSearch / WebFetch；装了 `deep-research` skill 则优先用它做多角检索）+ Python3（跑 build_radar.py，无第三方依赖）。

## 工作流（八阶段，严格按序）

### Phase 0 — 定标（确认后再扫）
确认 4 个入参，缺则问用户（默认值括注）：**垂类**（默认 自律A+专注B+心理健康C，见 signal-sources.md §3）、**地区**（默认 海外+中国）、**商业模式**（默认 B2C 订阅）、**模式**（默认 标准）。

### Phase 1 — 信号采集 → 信号文档
读 `references/signal-sources.md`（渠道与扫描法 + 高 MRR 狩猎地图）。多渠道扫，每条信号落 `assets/signal-doc-template.md` 的结构化字段。**专找"错误前提裂缝"**（现有 App 假设用户具备某能力/状态，而真实用户没有）——这是最高产的信号模式。每个市场数字标认知状态/贴出处。

### Phase 2 — 三重门筛选
读 `references/scoring-rubric.md §1`。用 **G1 情绪强度 + G2 workaround 存在 + G3 付费竞品验证** 过闸门。未过的移入观察池附录，不进评分。

### Phase 3 — 四轴评分（透明公式）
读 `references/scoring-rubric.md §2–3`。对通过的信号打四轴分：需求强度(0–100) / 供给稀缺度(0–100) / B2C 适配(0–10) / AI 系数。**机会分 = (需求/100)×(稀缺/100)×(B2C/10)×AI系数×1000**。完成后做 §5 一致性自检。

### Phase 4 — 雷达图（脚本确定性生成）
把评分写成 JSON（字段 `demand/scarcity/b2c_fit/ai_fit/stage`），跑：
```bash
python3 <installed-skill-dir>/scripts/build_radar.py \
  --in opps.json --out-html radar.html --out-md-table radar_table.md \
  --title "..." --date YYYY-MM-DD
```
脚本算机会分+颜色+坐标、注入 `assets/radar-chart-template.html`，并输出排序表（喂报告"二、雷达图"）。**雷达数字一律由脚本产出，禁止手填**。

### Phase 5 — Top 机会深档
读 `references/report-guide.md §3–5`。为 Top1–2 各写一份七要素深档（痛点+画像 / 竞品共同缺口 / AI差异化 / MVP路径 / 新手引导5屏 / 三层验证Go-NoGo / 预估指标），**每份必含「内置证伪」段**（杀死条件 + 最强反方 + 不利证据）。

### Phase 6 — GTM + 行动
读 `references/report-guide.md §6`。填 `assets/report-template.md`：推广渠道矩阵、本周行动清单、ASO 检查清单、指标追踪表。**报告开头强制决策优先**：一句话裁决 + 单一首推赌注 + 雷达图，再往下才是明细。

### Phase 7 — 系统化 + 归档（可选）
报告"八、系统化"写每月重跑约定 + 固定监控源。若用户要落盘，先确认目标
项目和目录，遵循该项目已有的 frontmatter 与索引约定；不假设存在维护者的
每日记录或发布索引。

## 资源索引

| 资源 | 何时读取 | 内容 |
|---|---|---|
| `references/scoring-rubric.md` | Phase 2–3 | 三重门 + 四轴锚点 + 机会分公式 + 一致性自检 + 算例 |
| `references/signal-sources.md` | Phase 1 | 6 渠道扫描法 + 认知状态纪律 + 高 MRR 类目狩猎地图 |
| `references/report-guide.md` | Phase 5–6 | 深档七要素 + 三层验证 + 内置证伪 + GTM/ASO + 反模式清单 |
| `assets/signal-doc-template.md` | Phase 1 | 信号采集文档骨架 |
| `assets/report-template.md` | Phase 6 | 最终报告骨架（决策优先） |
| `assets/radar-chart-template.html` | Phase 4 | ECharts 雷达模板（含 `__RADAR_DATA__` 注入点） |
| `scripts/build_radar.py` | Phase 4 | 评分 JSON → 雷达 HTML + 排序表（确定性，无依赖） |

## 质量门禁（强制，完成前逐条核对）

| 检查项 | 标准 | 阶段 |
|---|---|---|
| 执行顺序 | 0→1→…→7，严禁跳过采集直接出报告 | 全程 |
| 信号溯源 | 每个市场数字有出处或认知状态标，无凭空数字 | P1 |
| 三重门 | 进评分的信号 G1/G2/G3 全过（蓝海特例显式标注） | P2 |
| 评分一致性 | §5 四问全过：分数↔推荐、稀缺↔竞品、气泡位置↔结论、数字有源 | P3 |
| 雷达同源 | radar.html 由 build_radar.py 生成，与报告表格逐格一致 | P4 |
| 内置证伪 | 每个 Top 机会含杀死条件 + 最强反方 + 不利证据 | P5 |
| 决策优先 | 报告开头是裁决+首推+雷达，不是信号墙 | P6 |

## 比原版强在哪（给使用者的设计意图）

透明可复现评分（治原版黑箱+自相矛盾分）· 信号强制溯源+认知状态（治凭空数字）· 内置证伪（治一边倒乐观）· 垂类参数化+类目地图（治锁死单赛道）· 脚本确定性成图（治图表与报告脱钩）· 决策优先排版（治信号墙）。
