---
name: opencli
description: OpenCLI browser-command skill for using the local opencli daemon, installed site integrations, and browser automation workflows. Use when the user wants command-driven browser actions, website data extraction through OpenCLI, or guidance on operating the OpenCLI toolchain.
---

# OpenCLI · AI 工作流浏览器命令化工具

> 官网：https://opencli.info/
> GitHub：https://github.com/jackwener/opencli
> npm：`@jackwener/opencli`

## 核心定位

OpenCLI 将**浏览器操作命令化**，让 AI Agent 从「会说」进化到「会做」。

**原理**：复用 Chrome 已登录态（知乎/B站/小红书/微信读书等），不重新造浏览器，不经历登录→鉴权→Cookie→验证码的地狱流程。

**vs Playwright MCP**：Playwright 是 AI 临场发挥（慢、烧 token）；OpenCLI 是给 AI 发一本写好的操作手册（稳定、可预期）。

---

## 使用前检查

- 运行 `opencli --version`，确认 CLI 已安装。
- 运行 `opencli doctor`，确认 daemon 和浏览器扩展的实际状态。
- 不得根据本 Skill 声称 CLI、daemon、扩展或账号已经可用。

### Chrome Extension 安装步骤

1. 按 OpenCLI 官方文档下载并解压扩展，记下实际目录。
2. Chrome 地址栏输入 `chrome://extensions/`
3. 右上角开启「开发者模式」
4. 点「加载已解压的扩展程序」
5. 选择刚才解压的扩展目录
6. 确认扩展启用后，运行 `opencli doctor` 验证

---

## 常用命令

### 平台数据采集

| 平台 | 命令示例 | 说明 |
|------|---------|------|
| **小红书** | `opencli xiaohongshu search "AI创业" --limit 10` | 搜索笔记 |
| **小红书** | `opencli xiaohongshu creator-profile <uid>` | 创作者账号信息 |
| **小红书** | `opencli xiaohongshu creator-stats <uid>` | 创作者数据看板 |
| **微信公众号** | `opencli weixin article <url>` | 公众号文章正文 |
| **知乎** | `opencli zhihu hot --limit 10` | 知乎热榜 |
| **B站** | `opencli bilibili hot --limit 10` | B站热榜 |
| **YouTube** | `opencli youtube search "AI Agent"` | YouTube搜索 |
| **Twitter** | `opencli twitter user <username>` | Twitter用户推文 |
| **HackerNews** | `opencli hackernews top --limit 10` | HN热榜 |

### 飞书（lark-cli）

```bash
opencli lark-cli --help  # 查看所有飞书命令
opencli lark-cli calendar agenda  # 今日日程
opencli lark-cli messages recent   # 最近消息
```

### Obsidian Vault 管理

```bash
opencli obsidian search "AI Agent"  # 搜索笔记
opencli obsidian list                # 笔记列表
```

### 浏览器自动化（需 Chrome Extension）

```bash
opencli operate open "https://xiaohongshu.com"
opencli operate click ".search-input"
opencli operate get "https://..."   # 获取页面数据
opencli operate screenshot           # 截图
```

---

## AI Agent 集成方式

### 方式一：直接 shell 调用

在 exec 中直接调用 `opencli <command>`，解析 JSON 输出。

### 方式二：安装 AI Skills

```bash
npx skills add jackwener/opencli
```

### 方式三：接进 OpenClaw 流水线

将 OpenCLI 作为 Tool 封装，在 skill 中定义工具描述，供 Agent 调用。

---

## 典型工作流

### 场景一：小红书热门选题采集

```bash
opencli xiaohongshu search "AI工具" --limit 20 --format json
```

### 场景二：微信公众号文章存档

```bash
opencli weixin article "https://mp.weixin.qq.com/s/..."
```

### 场景三：信息聚合早报

一条命令同时拉回多平台热榜，AI 整理成早报。

---

## 注意事项

- Chrome 必须保持打开状态
- 目标平台需提前在 Chrome 登录
- Browser commands 需要 Chrome Extension 连接
- Public API commands（hackernews/youtube search 等）无需 Extension
- OpenCLI 可能复用浏览器中的登录态；只在用户明确指定的账号和网站范围内操作
- 发布、发送、删除、购买或修改外部数据前，先展示目标和内容并取得明确确认
- 遵守目标网站的服务条款、访问限制和隐私要求，不绕过验证码、付费墙或权限控制

---

## 扩展安装验证

```bash
opencli doctor
# [OK] Daemon: running on port 19825
# [OK] Extension: connected  ← 扩展连上后显示此行
```
