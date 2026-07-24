---
name: rednote-caption-to-screenshots
description: Convert XHS captions to screenshot-ready format. Use when preparing XHS content for screenshots.
---

# 小红书配文 → 轮播排版 → 截图交付

## 适用场景
- 需要**一套可发布的小红书文案**（标题/正文/话题/评论引导）。
- 同时需要把内容做成**可截图的轮播图**（常用 1080×1440，3:4）。
- 目标是"从配文到截图完成"的**交付闭环**：文案 + 可渲染文件 + 截图清单 + 自检。

## 输出契约（必须给出）
交付时按以下结构输出，缺一项视为未完成：

1) **发布配文（可直接粘贴）**
   - 标题（1-2 句，含关键词）
   - 正文（分段、可读；含 1 个明确 CTA：收藏/评论/私信）
   - 话题标签（8-15 个；含 2-3 个长尾）
   - 评论区引导（1 句，和正文 CTA 一致）

2) **轮播分镜（Page 1…N）**
   - 每页：一句主标题 + 2-5 条要点（或 1 段短文）
   - 标注：封面/痛点/方法/步骤/示例/总结/CTA 的角色

3) **产出文件清单**
   - HTML 文件名（建议 `YYYYMMDD_小红书轮播_<主题>.html`）
   - 截图命名规则（建议 `YYYYMMDD_<主题>_p01.png`…`p0N.png`）

4) **截图步骤清单（可执行）**
   - 用什么打开（浏览器）
   - 如何逐页截图（每张 1080×1440，避免缩放/裁切误差）

5) **质量自检清单**
   - 文字是否可读、密度是否过高、是否有敏感词风险
   - 封面是否"3 秒内说明白"

## 工作流（默认路径：HTML 轮播）

> **渐进披露（避免重复）**：
> - 做到"更像小红书/更可收藏/更清晰出图"时，**必须读取**：
>   - `references/20260126_小红书图文轮播_工程化出图工作流.md`
> - 用户要求「参考答案阅览室风」「深度阅读风」或「像参考答案阅览室」时，**必须读取**：
>   - `references/20260128_参考答案阅览室_图文风格要点.md`
> - 需要"一键出图"时，**推荐 Playwright 方案**（稳定性最高）：
>   - `scripts/render_deck_playwright.js`（**推荐默认**：直接截取 `.page` 元素，不依赖 CSS hash，2x 清晰出图）
> - 需要"输出契约不漏项"时，运行校验脚本：
>   - `python3 "<installed-skill-dir>/scripts/validate_output.py" "<markdown-output>"`（也支持传入 `.md` 文件路径）

### Step 0：先把"需求变量"定死（缺省也要给默认）
- **主题/一句话主张**：这篇要让读者相信什么？
- **人设与受众**：新手/进阶/从业者？（决定术语密度）
- **轮播页数**：默认 8 页（封面 + 6 内容 + 结尾 CTA）
- **风格**：默认"小红书可收藏风"（细则见 reference）
- **交付格式**：默认 1080×1440（3:4）

### Step 1：先写"封面钩子"，再写大纲
- 封面/大纲的写法与"数字化承诺"规则：见 reference（章节 1/2）

### Step 2：生成发布配文（标题/正文/话题/评论引导）
- 正文使用短段落 + 列表，避免连续长句。
- CTA 只要一个主动作（默认：收藏），不要堆多个。

### Step 3：生成轮播分镜（Page 1…N）
默认 8 页结构（封面/痛点/结论/方法/步骤/示例/清单/CTA）：见 reference（章节 1）

### Step 4：把分镜落到可截图 HTML
HTML 约定与版式细则：见 reference（章节 2/3）

> 如果用户已有 HTML，优先"改现有"而非重写。

#### HTML 关键 CSS 约定（Playwright 出图友好）
```css
.page {
  width: 1080px;
  height: 1440px;
  background: #ffffff;
  display: flex;
  flex-direction: column;
  justify-content: center;  /* 内容垂直居中 */
  padding: 72px 96px 80px;
  overflow: hidden;
}
.content {
  /* ⚠️ 关键：不要加 flex: 1，否则会被拉伸占满空间 */
  display: flex;
  flex-direction: column;
  gap: 24px;
}
```
- **不要用** `display: none` + `:target` 来控制页面显示（Chrome headless 不可靠）
- **不要给 `.content` 加 `flex: 1`**（会导致内容被拉伸而不是居中）
- Playwright 直接截取每个 `.page` 元素，所有页面都应保持 `display: flex`

#### HTML 输入要求
- 一页一个 `.page`（1080×1440），由 Playwright 直接截取元素出图。
- 若需要流程图，先生成用户有权使用的本地图片，再嵌入页面。

### Step 5：截图交付（推荐 Playwright 一键出图）

#### 方案 A：Playwright 截图（推荐）
```bash
# 1. 首次使用时确认项目已有 Playwright；缺少依赖先展示安装命令并获得用户批准
npm install playwright

# 2. 运行出图脚本
node "<installed-skill-dir>/scripts/render_deck_playwright.js" \
  "20260128_小红书轮播_xxx.html" \
  --output-dir "20260128_xxx_png" \
  --prefix "20260128_xxx"
```
- 自动识别所有 `.page` 元素并逐个截图
- 默认 2x 渲染（`deviceScaleFactor: 2`），文字清晰锐利
- 输出：`prefix_p01.png` … `prefix_p08.png`
- 未获准安装依赖时，使用下面的手工截图方案。

#### 方案 B：手工截图（备选）
- 浏览器打开 HTML，缩放 100%
- 逐页滚动到对应 `.page`，确保完整出现在视口内
- 逐页截图并按命名规则保存

## 常见坑（直接规避）
- **字太多**：轮播不是长文，把"解释"换成"步骤 + 例子 + 清单"。
- **封面不聚焦**：封面只讲一个矛盾点 + 一个结果承诺 + 一个关键词。
- **截图尺寸飘**：统一 1080×1440，命名带页码，防止漏页/错序。
- **同一页信息层级混乱**：每页最多 1 个主标题；要点不超过 5 条。
- **P2–P8 空白/黑屏**：不要用 CSS `:target` 控制显示，改用 Playwright 直接截取 `.page` 元素。

## 与其他技能的连接（建议联用）
- `writing-x-posts`：当你想把轮播内容同时改成"高互动短文案/多平台版本"。
- `short-video`：当你想把轮播直接扩展成口播脚本/分镜。
- `skill-creator`：当你要把某套"内容→排版→出图"流程继续固化成新 skill 或自动化脚本。
