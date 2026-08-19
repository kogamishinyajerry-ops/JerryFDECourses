# M01 视觉方向 v1.0

## 设计来源

本模块先用 Image-2 探索了“深色课程导航 + 白色工作台 + 状态化任务卡”的整体构图。

最终实现保留：

- 清楚的左侧学习路径；
- 大面积白色工作区；
- 文件、字段和状态为视觉中心；
- 可直接用于屏幕录制的布局；
- 一眼可见的当前步骤。

最终实现删除：

- 装饰性机器人；
- 发光科技元素；
- 与任务无关的图标堆叠；
- 过多标签和卡片；
- 纯装饰的渐变。

Image-2 输出只作为构图探索。课程中的正式图形使用可编辑 HTML/CSS/SVG 重新实现。

## 视觉目标

观众每一刻都能回答：

1. 当前看的是哪个文件或对象；
2. 哪个字段发生了变化；
3. 任务现在处于什么状态；
4. 这个状态由什么证据支持。

## 画面结构

### 左侧导航

宽度：240–280 px。

包含：

- 当前模块；
- 课程步骤；
- 当前步骤高亮；
- 进度；
- README / Lab 快捷入口。

### 主工作区

优先展示：

- 原始请求；
- 任务卡字段；
- 澄清问题；
- 运行记录；
- 状态变化。

屏幕录制时主工作区至少占画面宽度的 70%。

### 右侧检查区

只在需要时出现：

- 当前缺失字段；
- provenance；
- 验收说明；
- 下一步操作。

## 设计 Token

```css
--bg-app: #eef2f6;
--bg-sidebar: #101a28;
--bg-panel: #ffffff;
--text-primary: #17202e;
--text-secondary: #5f6b7a;
--border: #d9e1ea;
--accent: #2f6fed;
--accent-soft: #eaf1ff;
--warning: #b76a00;
--warning-soft: #fff5df;
--success: #287a4b;
--success-soft: #e8f6ed;
--danger: #a43b3b;
--danger-soft: #fdecec;
--unknown: #6f7782;
--unknown-soft: #f0f2f5;
```

## 状态表现

### DRAFT

- 中性灰；
- 说明请求已被记录；
- 不出现完成图标。

### NEEDS_CLARIFICATION

- 琥珀色；
- 显示缺失数量；
- 主行动为“查看澄清问题”。

### READY

- 绿色；
- 同时显示窄定义：

```text
必填信息已确认，可进入执行准备。
```

不使用庆祝动画，不暗示任务完成。

## 字段来源

| 来源 | 视觉 | 含义 |
|---|---|---|
| SOURCE_TEXT | 蓝色细标 | 原始请求明确出现 |
| SYSTEM_DEFAULT_UNCONFIRMED | 红色虚线标 | 系统补入，未经确认 |
| HUMAN_CONFIRMED | 绿色实线标 | 人工明确确认 |
| MISSING | 灰色空值 | 当前未知 |

## 动效

动效只用于解释变化：

- 字段从空值变为候选值；
- 未确认默认值被划掉；
- 缺失字段聚合到问题列表；
- 人工确认后 provenance 改变；
- 状态从 NEEDS_CLARIFICATION 进入 READY。

单次动画建议 180–320 ms。避免持续漂浮和背景粒子。

## 字体与代码

中文：系统黑体或开源无衬线字体。

代码：系统等宽字体。

建议：

```css
font-family: Inter, "PingFang SC", "Microsoft YaHei", system-ui, sans-serif;
font-family: "SFMono-Regular", Consolas, "Liberation Mono", monospace;
```

## 录屏安全

- 使用相对路径；
- 浏览器使用独立干净 Profile；
- 关闭通知；
- 不显示书签、账号头像和扩展；
- 终端提示符固定为 `course $`；
- 所有姓名使用 Alex / Morgan / DEMO_REQUESTER；
- 所有数据标注 `PUBLIC_DEMO`。
