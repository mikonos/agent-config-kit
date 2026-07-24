# awesome-design-md（参考资料）

> **定位**：本 skill 的 **外部设计系统素材库** 指针，不替代项目根目录自有 `DESIGN.md` 或业务 Token 真源。

## 是什么

- **仓库**：[VoltAgent/awesome-design-md](https://github.com/VoltAgent/awesome-design-md)（MIT）
- **内容**：60+ 套从真实产品站点整理的 **`DESIGN.md`**（[Google Stitch](https://stitch.withgoogle.com/docs/design-md/overview/) 思路），常含 `preview.html` / `preview-dark.html`。
- **单站在线浏览**：[getdesign.md](https://getdesign.md/)（README 内按品牌链到各站点的 design-md 页）。

## Agent 何时读

1. 需要 **整站气质、组件描述、色板角色、字体阶梯、Do/Don't** 时，先到本仓库或 getdesign **选一套接近的**，再 **映射** 到当前项目的 Token / CSS 变量。
2. **已有**子项目根目录 `DESIGN.md` 时：**以根文件为准**；awesome 仅作补充灵感，禁止静默覆盖已约定 hex/命名。
3. **项目 Agent Rule**：行为协议不一定是 UI 视觉文档；只有明确规定视觉系统时才作为设计输入。

## 与当前项目的边界

- 产品 **业务色、无障碍规则、深色模式与语义 Token** 以当前项目真源为准；从 awesome 借的是 **密度、圆角、阴影、栅格气质**，不是替换 Token。

## 本机离线副本（可选）

上游文件 **默认不在** ZK 仓库内；需要离线或固定版本时在任意路径：

```bash
git clone https://github.com/VoltAgent/awesome-design-md.git
```

若放在当前工作区内，建议置于独立工具目录，并按项目规则决定使用普通目录、`.gitignore` 条目或子模块。

## 延伸阅读

- Stitch DESIGN.md 格式：<https://stitch.withgoogle.com/docs/design-md/format/>
- 当前项目的 `DESIGN.md`、组件文档与 Token 真源。
