# JerryFDECourses

《AI 时代的工业 FDE》课程的唯一工作仓库。

本仓库用于持续开发、评审和发布：

- 课程蓝图与教学规范；
- 各模块讲稿、分镜、字幕与视觉资产；
- 可公开复现的 Build Lab；
- 学员作业、Rubric、评测与参考答案；
- FDE 团队培养、资产化与治理材料；
- 课程版本记录与决策记录。

## 当前状态

| 模块 | 状态 | 说明 |
|---|---|---|
| M01｜从一条模糊需求开始 | `RC1_CANDIDATE` | 课程工程已收口，等待正式录制、人工复核和试讲 |
| M02｜让模型生成候选 | Backlog | 复用 M01 骨架，尚未进入内容开发 |

`RC1_CANDIDATE` 不表示课程已经正式发布。M01 的状态、剩余工作和发布门禁见 [`modules/M01/RC1_STATUS.md`](modules/M01/RC1_STATUS.md)。

## 课程目标

课程面向希望把专业工作转化为可信 AI 能力的工程师。

它不以建设一个大而全的平台为毕业目标。学员需要经历一条完整交付链：

```text
发现真实问题
→ 把工作说清楚
→ 构建最小闭环
→ 运行并观察
→ 暴露失败
→ 增加检查与人工边界
→ 形成可复用资产
→ 让另一名工程师接手
```

项目原则：

> 轻平台、厚人才、厚资产。

## 教学方法

每个模块采用“构建—运行—观察—修改”的节奏：

1. 从一个具体对象开始；
2. 尽快得到第一份可见结果；
3. 每次只增加一层复杂度；
4. 把错误和边界留在课程里；
5. 先经历，再给概念命名；
6. 以可运行、可检查、可评审的产出完成学习。

课程材料分为三轨：

- **Main Lesson**：20–30 分钟工程理解课；
- **Build Lab**：45–90 分钟完整构建与调试；
- **Engineering Notes**：代码、契约、已知问题与扩展练习。

## 公开保密边界

这是公开仓库。所有案例必须满足：代码、数据、截图和日志可以直接公开，无需再次脱敏。

禁止提交：

- 真实工程参数、型号信息或内部数据；
- 专有工具界面、输入格式、脚本和运行链路；
- 内网地址、账号、密钥、组织名单或权限结构；
- 能够反推出实际业务能力和方法细节的材料；
- 未经许可的内部文档、会议记录和截图。

专业场景只保留方法映射。真实适配在具备权限的封闭环境中完成。

## 仓库结构

```text
JerryFDECourses/
├── docs/                 # 项目规范、路线图、ADR 与发布边界
├── modules/              # M01–M18 课程模块
│   └── M01/
│       ├── lesson/       # 模块卡、逐字稿、分镜、字幕、制作交接
│       ├── lab/          # 可运行实验与测试
│       ├── site/         # 互动课件与录屏界面
│       ├── assets/       # 可编辑 SVG、图示与生成提示词
│       └── RC1_STATUS.md # 当前状态与发布门禁
├── templates/            # 学员与教师共用模板
├── scripts/              # 发布检查和仓库维护脚本
└── .github/workflows/    # 自动测试与公开安全检查
```

## M01｜从一条模糊需求开始

把一句“请帮我整理一下”，变成一张可以执行、可以确认的任务卡。

公开案例使用完全虚构的任务请求：

> 请把上个月收到的用户问题整理一下，下周评审时用。

模块逐步构建：

```text
原始请求
→ 原文明确字段
→ 缺失信息
→ 澄清问题
→ 人工确认
→ READY 任务卡
→ 运行记录
```

第一版不调用真实模型。确定性检查先跑通，M02 再加入模型生成候选任务卡。

M01 入口：[`modules/M01/README.md`](modules/M01/README.md)

## 本地运行 M01

```bash
python modules/M01/lab/task_pipeline.py \
  --request modules/M01/lab/data/request.txt \
  --confirmation modules/M01/lab/data/confirmation.json \
  --output modules/M01/lab/output

python -m unittest discover modules/M01/lab/tests -v
```

互动课件无需构建工具，直接打开：

```text
modules/M01/site/index.html
```

## M01 制作入口

- 完整讲师稿：[`modules/M01/lesson/INSTRUCTOR_SCRIPT.md`](modules/M01/lesson/INSTRUCTOR_SCRIPT.md)
- 屏幕录制 Runbook：[`modules/M01/lesson/SCREEN_RECORDING.md`](modules/M01/lesson/SCREEN_RECORDING.md)
- 真人素材交接：[`modules/M01/lesson/HUMAN_RECORDING_HANDOFF.md`](modules/M01/lesson/HUMAN_RECORDING_HANDOFF.md)
- 最终组装与验收：[`modules/M01/lesson/FINAL_ASSEMBLY_CHECKLIST.md`](modules/M01/lesson/FINAL_ASSEMBLY_CHECKLIST.md)
- 作业与 Rubric：[`modules/M01/lesson/ASSIGNMENT_AND_RUBRIC.md`](modules/M01/lesson/ASSIGNMENT_AND_RUBRIC.md)

## 开发约定

- 一次 Pull Request 只解决一个清楚的问题；
- 每个模块必须同时包含正常路径和至少一个失败路径；
- 未验证的判断必须标注；
- 课程概念必须落到文件、数据、动作、状态或证据；
- 讲稿不使用宏大开场，不用网络梗承担教学；
- 真人镜头单独录制，仓库内使用明确占位符；
- 正式结论回写仓库，聊天记录不作为唯一事实源；
- 合并 PR、制作 PILOT、正式发布是三个不同动作。

## 许可证

代码与仓库内明确标注为可发布的材料遵循 [MIT License](LICENSE)。课程成片、真人形象、品牌标识和未标注素材的授权范围另行管理。
