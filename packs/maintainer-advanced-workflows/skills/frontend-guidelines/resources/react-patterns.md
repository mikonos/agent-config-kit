# React Patterns（实战版）

## 何时用 Context
- **适合**：跨多层组件共享且更新不频繁（主题、locale、权限）
- **不适合**：高频更新的大对象（容易导致无谓重渲染）→ 用更细粒度 state/store

## 何时用自定义 Hook
- 抽离副作用（fetch、订阅、事件绑定）
- 抽离复用逻辑（表单、分页、筛选）

## 组件拆分
- **展示/容器分离**：UI（pure） vs 数据/状态（smart）
- **优先 props 下发**，必要时再上升为 Context

