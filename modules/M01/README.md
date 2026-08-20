# M01｜从一条模糊需求开始

## 副标题

把一句“请帮我整理一下”，变成一张可以执行、可以确认的任务卡。

## 模块位置

第一部分「工程师如何进入 AI 时代」第 1 模块。

## 当前发布状态

```text
RC1_CANDIDATE
```

课程工程已经收口，可以进入正式录制、人工复核和试讲；尚未正式发布。

- 状态与门禁：[`RC1_STATUS.md`](RC1_STATUS.md)
- 真人素材交接：[`lesson/HUMAN_RECORDING_HANDOFF.md`](lesson/HUMAN_RECORDING_HANDOFF.md)
- 最终组装与验收：[`lesson/FINAL_ASSEMBLY_CHECKLIST.md`](lesson/FINAL_ASSEMBLY_CHECKLIST.md)
- 试讲与成片任务：Issue #2

## 适合对象

- L0 AI 使用者；
- L1 AI 增强工程师候选人；
- 尚未系统学习 Agent 的专业工程师。

无需模型训练和前端开发经验。Build Lab 使用 Python 标准库。

## 本集完成什么

学员会亲手构建一条很小的任务准备流程：

```text
读取原始请求
→ 提取原文已经明确的信息
→ 检查缺失字段
→ 生成澄清问题
→ 接收人工确认
→ 形成 READY 任务卡
→ 保存运行记录
```

## 公开案例

```text
请把上个月收到的用户问题整理一下，下周评审时用。
```

案例完全虚构。文件名、人员、日期和验收要求均为教学样例。

## 为什么从这里开始

很多 Agent 项目在任务尚未说清时就开始生成内容。

M01 先处理更基础的问题：

- 系统知道哪些信息来自原文；
- 哪些内容仍然缺失；
- 哪些值不能被静默猜测；
- 谁确认任务可以开始；
- 怎样保留形成任务卡的证据。

## 三个状态

```text
DRAFT
NEEDS_CLARIFICATION
READY
```

- `DRAFT`：请求刚被记录；
- `NEEDS_CLARIFICATION`：执行所需信息仍有缺失；
- `READY`：必填信息已由人确认，可以进入执行阶段。

`READY` 不表示任务已经完成，也不表示最终交付已验收。

## 学习产出

学员提交《我的第一个任务准备闭环》：

- 一条虚构或彻底脱敏的原始请求；
- 一张初始任务卡；
- 一份缺失字段清单；
- 一组澄清问题；
- 一张确认后的任务卡；
- 一份运行记录；
- 一个系统必须停止的条件。

## 目录

```text
M01/
├── README.md
├── RC1_STATUS.md
├── lesson/
│   ├── MODULE_CARD.md
│   ├── INSTRUCTOR_SCRIPT.md
│   ├── STORYBOARD.md
│   ├── SCREEN_RECORDING.md
│   ├── HUMAN_RECORDING_HANDOFF.md
│   ├── FINAL_ASSEMBLY_CHECKLIST.md
│   └── SUBTITLES.zh-CN.srt
├── lab/
│   ├── README.md
│   ├── task_pipeline.py
│   ├── data/
│   ├── schemas/
│   ├── tests/
│   └── reference_output/
├── site/
│   ├── index.html
│   ├── styles.css
│   └── app.js
└── assets/
    ├── VISUAL_DIRECTION.md
    ├── m01-flow.svg
    └── IMAGEGEN_PROMPTS.md
```

## 快速运行

```bash
python modules/M01/lab/task_pipeline.py \
  --request modules/M01/lab/data/request.txt \
  --output modules/M01/lab/output
```

第一次运行应得到：

```text
NEEDS_CLARIFICATION
```

加入确认文件：

```bash
python modules/M01/lab/task_pipeline.py \
  --request modules/M01/lab/data/request.txt \
  --confirmation modules/M01/lab/data/confirmation.json \
  --output modules/M01/lab/output
```

第二次运行应得到：

```text
READY
```

运行测试：

```bash
python -m unittest discover modules/M01/lab/tests -v
```

## 模块完成定义

学员能够：

1. 区分原文事实、系统候选和人工确认；
2. 发现执行任务所缺少的信息；
3. 让系统在关键信息缺失时停止；
4. 解释 `READY` 的边界；
5. 使用自己的安全样例复现同一结构。

## 不在本集展开

- 模型 API；
- Agent 循环；
- Harness；
- RAG；
- 多 Agent；
- 专业工具调用；
- 企业平台架构。

M02 会在同一条流程中加入模型，让模型只负责生成候选字段和澄清问题。

## 公开边界声明

本模块使用合成案例，用于演示任务建模、状态、校验和人工确认。它不包含真实工程数据、专业工具链或内部流程，也不构成任何工程批准或业务决策依据。
