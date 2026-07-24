# Styling Guide（检查清单）

## 可访问性（A11y）
- 颜色对比度满足 WCAG（至少 AA）
- 表单控件有 label / aria-label
- 错误态/成功态不仅靠颜色表达（图标/文案辅助）

## 响应式（Mobile First）
- 先写移动端，再逐步加断点
- 避免固定宽高；优先 flex/grid + max-width

## 一致性
- 间距使用统一 scale（例如 4/8/12/16）
- 组件状态齐全：default/hover/active/disabled/loading

