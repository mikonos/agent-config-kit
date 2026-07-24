---
name: rednote-reader
description: Read and analyze Xiaohongshu (小红书) content. Use when extracting insights from XHS posts.
---

# Rednote Reader Skill（小红书笔记全文获取）

从**小红书链接**获取笔记并**全部保存**：接口返回的正文、所有图片文件、以及每张图片内的文字（读图提字），一并落盘为 Markdown + images 目录。**无论正文是否为空**，只要有图片就下载并提字，与正文合并为一份完整内容。

## 何时使用

用户出现以下任一情况时使用本 Skill：

- **意图**：阅读小红书、查看小红书、学习小红书、获取/提取小红书笔记内容/全文
- **材料**：提供了小红书笔记链接（`xhslink.com/...` 或 `www.xiaohongshu.com/explore/...`）

## 核心流程（不可跳步）

### Step 1：从已授权来源获取元数据与正文

1. 优先使用当前 Runtime 已配置且用户已授权的 Rednote 连接器或登录浏览器会话；也可读取用户提供的页面导出 JSON。
2. 得到 `title`、`content`、`author`、`imgs`（图片 URL 列表）、`url` 等。
3. 不绕过登录、验证码、付费墙、访问控制或平台限制；来源不可访问时，请用户提供导出内容。

### Step 2：正文与图片内容均保留

- **正文**：来源返回的 `content`（若有）保留，作为 Markdown 的「正文」部分。
- **图片**：只要 `imgs` 非空，**一律**执行 **Step 3**（下载图片 + 读图提字），不因正文非空而跳过。最终落盘时合并「正文 + 图片提字」为一份完整内容，并保留所有图片文件。

### Step 3：有图则必做——下载图片 + 读图提字

（**仅当 `imgs` 为空时跳过**；否则必须执行。）

1. **下载图片**  
   - 运行已安装 `rednote-reader/scripts/download_note_images.py`（见下方 Usage），传入来源返回的 `imgs` 与用户授权的输出目录。
   - 脚本将图片保存为 `01.webp`, `02.webp`, ...，并写入 `manifest.json`（title、source_url、author、image_paths）。

2. **读图提字（Agent 执行）**  
   - 按 `manifest.json` 中 `image_paths` 的**顺序**，用当前 Runtime 的图片读取能力逐张查看，**完整提取图中所有可见文字**，按顺序拼接为一段「图片内文字」文本。
   - 若下载或读图任一步失败：提示用户并尽量保留已下载的图片与已提取的文字。

### Step 4：落盘（正文 + 图片内容 + 图片文件）

- **单篇 Markdown**：
  - **YAML frontmatter**：`title`、`source_url`、`author`、`date`、`platform: 小红书`；若有图片可加 `images_count: N`。
  - **正文**：先写来源的 `content`（若有），再写「图片内文字」：若执行了 Step 3，用明确标题（如 `## 图片内容（读图提字）`）接按顺序拼接的图片提字全文，保证正文与图片内容**全部**进入同一 Markdown。
- **图片文件**：Step 3 的图片保存在任务目录下 `images/` 中（`01.webp`, `02.webp`, ...），不删除，便于后续查看或复用。
- **默认行为**：先在对话中返回内容。只有用户明确要求保存并给出或确认目标目录后，才写 Markdown 和 `images/`。

### Step 5：后续学习（可选）

- 若用户意图是**学习/阅读/深度消化**该笔记，可继续使用已安装 `deep-read` Skill；写入知识库仍需单独授权。

## 依赖

- **内容来源**：当前 Runtime 已配置的连接器、登录浏览器会话，或用户提供的导出 JSON。
- **Python**：仅图片下载需要 Python ≥3.8；脚本只用标准库。

## Usage（Step 3 下载脚本）

在用户授权的项目目录执行：

```bash
python "<installed-skill-dir>/scripts/download_note_images.py" \
  --urls "https://sns-webpic-qc.xhscdn.com/..." "https://..." \
  --output-dir "<authorized-output-dir>/images"

# 或使用 --manifest 传入已保存的来源 JSON（脚本会读 imgs、title、author、url）
python "<installed-skill-dir>/scripts/download_note_images.py" \
  --manifest "path/to/note_meta.json" \
  --output-dir "<authorized-output-dir>/images"
```

脚本行为：

- 下载 `--urls` 中的每张图到 `--output-dir`，命名为 `01.webp`, `02.webp`, ...（按列表顺序）。
- 在 `--output-dir` 下生成 `manifest.json`：`title`, `source_url`, `author`, `image_paths`（相对路径列表），供 Agent 按顺序读图提字。

## 输出结构示例

```
<authorized-output-dir>/rednote_{标题slug}/
├── images/
│   ├── 01.webp
│   ├── 02.webp
│   └── manifest.json
├── note_meta.json
└── {YYYYMMDD}_小红书_{标题slug}.md
```

## 与其它 skill 的关系

- **rednote-caption-to-screenshots**：做「配文 + 轮播出图」，不负责从链接拉正文；本 skill 负责「从链接拿到可读全文」。
- **deep-read**：本 Skill 产出 Markdown 后，若用户要深度消化，再调用 deep-read；入网写入需单独授权。

## 验收

- [ ] 已从用户授权的连接器、浏览器会话或导出文件获取笔记。
- [ ] **正文**：来源的 `content`（若有）已写入返回内容或已授权的 Markdown。
- [ ] **图片**：若 `imgs` 非空，已下载全部图片到 `images/`，并已读图提字、将图片内文字合并进同一 Markdown（正文 + 图片内容均保留）。
- [ ] 若用户授权落盘，Markdown 含 frontmatter 与完整内容（正文 + 图片提字），路径符合约定；图片文件已保留在 `images/`。
- [ ] 用户意图为学习时，已提示可接 deep-read。
