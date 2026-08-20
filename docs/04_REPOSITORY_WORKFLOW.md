# 仓库工作流与唯一事实源规则

## 1. 唯一工作仓库

《AI 时代的工业 FDE》课程的正式开发只发生在：

```text
kogamishinyajerry-ops/JerryFDECourses
```

聊天、临时 Word、图片和本地草稿用于讨论与生产，不承担长期事实源职责。

一项决定只有回写仓库后，才视为课程正式状态。

## 2. 内容层级

```text
docs/              项目级规范与课程地图
modules/Mxx/       单个模块的完整课程产品
templates/         跨模块复用模板
scripts/           自动检查与生产工具
.github/           CI、Issue 与 PR 流程
```

每个模块独立形成完整资产包。

## 3. 分支策略

### 长期稳定分支

默认分支保存通过评审的课程版本。

### 开发分支

命名建议：

```text
course-foundation
module/M01-task-readiness
module/M02-model-candidates
fix/M01-subtitle-timing
content/M03-work-map
```

### Pull Request

一次 PR 只解决一个清楚问题：

- 一个模块；
- 一次勘误；
- 一组视觉资产；
- 一项教学规范变化；
- 一次公开安全修复。

## 4. 模块目录标准

```text
modules/Mxx/
├── README.md
├── lesson/
│   ├── MODULE_CARD.md
│   ├── INSTRUCTOR_SCRIPT.md
│   ├── STORYBOARD.md
│   ├── SCREEN_RECORDING.md
│   ├── ASSIGNMENT_AND_RUBRIC.md
│   └── SUBTITLES.zh-CN.srt
├── lab/
│   ├── README.md
│   ├── data/
│   ├── schemas/
│   ├── tests/
│   └── reference_output/
├── site/
│   ├── README.md
│   ├── index.html
│   ├── styles.css
│   └── app.js
└── assets/
    ├── VISUAL_DIRECTION.md
    ├── IMAGEGEN_PROMPTS.md
    └── *.svg
```

根据模块需要可以减少文件，不能缺少模块卡、讲师稿、实验/练习、作业、Rubric 和公开边界。

## 5. 内容状态

| 状态 | 含义 |
|---|---|
| DRAFT | 结构仍在快速变化 |
| BUILDABLE | 实验可以运行，内容尚未试讲 |
| PILOT | 已进入首期学员试讲 |
| REVIEWED | 内容、技术和公开安全完成评审 |
| RELEASED | 对外发布版本 |
| DEPRECATED | 保留历史，不再作为当前教学材料 |

状态写在模块 README 与版本记录中。

## 6. PR 完成定义

课程模块 PR 至少通过：

- Python/JS/Schema 语法检查；
- 正常和失败路径回放；
- 公开发布自动扫描；
- 讲师稿与实验一致性检查；
- READY/完成/验收等状态边界检查；
- 人工保密与版权检查；
- 至少一名非作者复现。

## 7. Issue 使用

建议标签：

```text
module:M01
module:M02
content
lab
visual
subtitle
security
accessibility
pilot-feedback
errata
decision
```

试讲反馈不要只写“节奏不好”。Issue 至少记录：

- 学员在哪一步停住；
- 当时看到什么；
- 原本预计什么；
- 哪个文件需要修改；
- 怎样验证修改有效。

## 8. 决策记录

影响多模块的决定写入 `docs/decisions/`。

ADR 格式：

```text
标题
状态
背景
决定
备选方案
后果
触发复审的条件
```

不要把短期工具选择写成永久课程真理。

## 9. 真人素材

真人原片不直接进入公开 Git 仓库。

仓库保存：

- 镜头编号；
- 台词；
- 景别；
- 时长；
- 文件命名；
- 授权状态；
- 最终成片中的时间位置。

大文件进入单独受控素材库。仓库只保存可追踪的 manifest。

## 10. 版本发布

每次模块发布需记录：

- commit SHA；
- 课程视频版本；
- 讲师稿版本；
- 实验版本；
- 测试结果；
- 公开安全复核人；
- 已知问题；
- 下一次复审条件。

## 11. 对话到仓库的转换

在对话中形成新的正式结论时：

1. 找到对应唯一文件；
2. 以 PR 修改；
3. 在 PR 中说明变化原因；
4. 更新测试、讲稿或 Rubric；
5. 通过 CI；
6. 合并后关闭相关 Issue。

不再建立第二套平行“最终版文档”。
