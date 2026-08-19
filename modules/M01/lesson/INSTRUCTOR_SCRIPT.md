# M01 完整讲师稿

> 建议成片：27–30 分钟  
> 形式：真人开场/收束 + 屏幕录制 + 旁白 + 可编辑 SVG 过渡  
> 本稿中的真人镜头均可暂时用旁白和课程标题替代。

---

## 00:00–00:25｜开场

[真人镜头｜中景，桌面保持简单｜约 20 秒]

这一节，我们从一条很普通的工作消息开始。

没有模型排行榜，也不搭 Agent。

先看文件。

[切屏幕录制]

---

## 00:25–01:20｜打开原始请求

[画面：打开 `lab/data/request.txt`]

文件里只有一句话：

> 请把上个月收到的用户问题整理一下，下周评审时用。

今天的目标是把这句话变成一张可以执行、可以确认的任务卡。

最后会生成四份东西：

```text
task_card.json
questions.md
run_record.json
status.txt
```

先不让 AI 来填。

我们自己读一遍。

---

## 01:20–04:20｜只记录原文里有的东西

[画面：左侧 request.txt，右侧空白 task_card 草稿]

原文给了一个目标：整理用户问题。

时间范围写的是“上个月”。

使用场景是“下周评审”。

目前能安全写进任务卡的内容，大概只有这些：

```json
{
  "objective": "整理用户问题",
  "time_range_text": "上个月",
  "usage_context": "下周评审",
  "source": null,
  "expected_output": null,
  "due_date": null,
  "owner": null,
  "reviewer": null,
  "acceptance_criteria": []
}
```

这里先停一下。

“上个月”是自然月，还是最近三十天？

“下周评审”具体是哪一天？

用户问题存在哪里？

交付表格、文档，还是演示材料？

谁负责？

整理到什么程度算完成？

原文没有回答。

这些空值看起来不漂亮。空值本身没有问题。它准确地表示：我们还不知道。

---

## 04:20–05:30｜看看文件结构

[画面：文件树]

实验很小：

```text
lab/
├── task_pipeline.py
├── data/
│   ├── request.txt
│   └── confirmation.json
└── output/
```

`task_pipeline.py` 负责三件事：

1. 读取请求；
2. 检查任务卡是否具备执行条件；
3. 写出问题、状态和运行记录。

第一版代码故意留了一个常见问题。

我们先运行。

---

## 05:30–08:10｜运行 v0：代码成功，任务也“准备好了”

[画面：终端]

```bash
python modules/M01/lab/task_pipeline.py \
  --mode v0 \
  --request modules/M01/lab/data/request.txt \
  --output modules/M01/lab/output-v0
```

[等待命令完成]

终端显示：

```text
status=READY
```

打开任务卡。

```json
{
  "expected_output": ["PPT"],
  "due_date": "NEXT_FRIDAY",
  "owner": "CURRENT_USER",
  "status": "READY"
}
```

程序没有报错。

JSON 也完整。

只是这三个值都不是请求人说的。

[画面高亮三个字段]

- 输出默认成 PPT；
- 截止日期默认成下周五；
- 负责人默认成当前用户。

如果这是一段个人小脚本，默认值有时很方便。

进入多人工作以后，默认值会开始替人做决定。

这里的危险很安静。没有异常，没有红字，文件甚至比原始请求更完整。

---

## 08:10–10:10｜定位 v0 的问题

[画面：打开代码中 `apply_v0_defaults`]

```python
card["expected_output"] = card["expected_output"] or ["PPT"]
card["due_date"] = card["due_date"] or "NEXT_FRIDAY"
card["owner"] = card["owner"] or "CURRENT_USER"
```

这三行代码做的事情很清楚：字段为空，就补一个值。

程序无法知道：

- 请求人通常用不用 PPT；
- 评审是不是下周五；
- 当前用户有没有责任接这个任务。

代码执行正确。

工作语义错了。

这类问题换一个更大的模型也不会自动消失。模型可能猜得更像，来源仍然是猜。

我们把默认值删掉。

---

## 10:10–12:40｜定义任务开始前需要什么

[画面：打开 `REQUIRED_FIELDS`]

v1 先定义执行前必须确认的字段：

```python
REQUIRED_FIELDS = (
    "objective",
    "source",
    "time_range",
    "expected_output",
    "due_date",
    "owner",
    "acceptance_criteria",
)
```

这份清单不代表所有企业、所有任务都要用同样字段。

它只代表当前这个教学任务的开始条件。

再看一项规则：

```python
if missing_fields:
    status = "NEEDS_CLARIFICATION"
```

任务不会继续猜，也不会进入执行。

先跑一次没有确认文件的 v1。

---

## 12:40–15:20｜运行 v1：信息不足，明确停止

[画面：终端]

```bash
python modules/M01/lab/task_pipeline.py \
  --mode v1 \
  --request modules/M01/lab/data/request.txt \
  --output modules/M01/lab/output-v1
```

终端输出：

```text
status=NEEDS_CLARIFICATION
missing=source,time_range,expected_output,due_date,owner,acceptance_criteria
```

打开 `questions.md`。

```markdown
1. 用户问题存放在哪里？
2. “上个月”对应哪个具体日期范围？
3. 需要输出什么文件或材料？
4. 评审的具体日期和截止时间是什么？
5. 谁负责完成这项任务？
6. 哪些条件满足后，可以认为整理工作完成？
```

这一版没有完成任务。

它完成了更小的一件事：把无法继续的原因写清楚。

看一下输出目录。

没有最终任务卡，只有草稿、问题和运行记录。

这正是我们需要的行为。

---

## 15:20–17:00｜检查 run_record

[画面：打开 `run_record.json`]

```json
{
  "status": "NEEDS_CLARIFICATION",
  "source_request": "request.txt",
  "missing_fields": [
    "source",
    "time_range",
    "expected_output",
    "due_date",
    "owner",
    "acceptance_criteria"
  ],
  "confirmed_fields": [],
  "message": "任务信息不足，尚未进入执行阶段"
}
```

运行记录回答了几个简单问题：

- 这次读的是哪一条请求；
- 缺了什么；
- 有没有人确认过字段；
- 为什么停下。

它没有记录复杂推理过程。

目前用不上。

先把关键事实留住。

---

## 17:00–19:10｜加入人工确认

[画面：打开 `data/confirmation.json`]

现在假设请求人给了补充信息：

```json
{
  "source": "feedback.csv",
  "time_range": {
    "start": "2026-07-01",
    "end": "2026-07-31"
  },
  "expected_output": [
    "Excel 汇总表",
    "一页摘要"
  ],
  "due_date": "2026-08-10T17:00:00+08:00",
  "owner": "Alex",
  "reviewer": "Morgan",
  "acceptance_criteria": [
    "全部问题完成分类",
    "重复项已合并",
    "每项保留原始编号"
  ],
  "confirmed_by": "DEMO_REQUESTER"
}
```

姓名、日期和文件都属于教学样例。

这里最重要的是最后一项：`confirmed_by`。

我们需要区分系统填入的值和人确认过的值。

---

## 19:10–21:00｜再次运行 v1

[画面：终端]

```bash
python modules/M01/lab/task_pipeline.py \
  --mode v1 \
  --request modules/M01/lab/data/request.txt \
  --confirmation modules/M01/lab/data/confirmation.json \
  --output modules/M01/lab/output-ready
```

终端显示：

```text
status=READY
```

打开 `task_card.json`。

[画面逐项高亮]

现在任务卡里有：

- 明确目标；
- 数据来源；
- 日期范围；
- 输出形式；
- 截止时间；
- 负责人；
- 验收条件；
- 确认来源。

这次 `READY` 有依据。

---

## 21:00–23:00｜READY 到底表示什么

[画面：状态条 DRAFT → NEEDS_CLARIFICATION → READY]

`READY` 的含义很窄：

> 当前定义的必填信息已经得到确认，可以进入下一阶段。

它没有表示：

- 用户问题已经整理完；
- 输出质量已经通过评审；
- 文件可以正式发布；
- 负责人接受了最终结果。

状态名要和证据匹配。

状态写得过大，系统会制造一种完成感。后面的工作还没发生，界面已经绿了。

---

## 23:00–25:10｜现在给几个东西起名字

[画面：展示流程 SVG]

刚才我们实际经历了五个结构。

第一，任务开始前需要一组明确字段。这个可以叫**输入契约**。

第二，任务会停在草稿、等待澄清或者准备完成。这里出现了**状态**。

第三，系统没有替人确认日期、负责人和验收条件。这里有一个很小的 **Human-in-the-loop**。

第四，原始请求、缺失字段、确认来源和状态被保存下来。这是最小的 **Trace 与 Evidence**。

第五，程序负责检查字段；人负责确认任务含义。这里已经有了**责任边界**。

这些概念不需要先背。

它们刚刚都在文件里出现过。

---

## 25:10–26:30｜模型以后放在哪里

[画面：在“原始请求”和“候选任务卡”之间增加一个灰色模型框]

下一集会把模型放在这里。

它可以：

- 从自然语言提取候选目标；
- 识别“上个月”“下周”这类相对表达；
- 发现可能缺少的字段；
- 生成更自然的澄清问题。

模型输出先叫候选。

确定性程序继续检查字段。

人确认日期、负责人和验收标准。

这一节没有接模型，原因也很简单：确定性骨架还没跑清楚时，很难看出模型具体帮了什么，也很难发现它越过了哪条边界。

---

## 26:30–28:20｜学员实践

[真人镜头｜约 20 秒，可先用屏幕标题替代]

从自己的工作里找一句常见请求。

不要上传真实内部内容。保留句子结构，替换人名、文件、日期和项目。

你需要提交：

```text
request.txt
confirmation.json
task_card.json
questions.md
run_record.json
```

再加一个系统必须停止的条件。

例如：

- 数据来源没有确认；
- 截止时间含糊；
- 负责人为空；
- 验收标准只有“整理好看一点”。

第一版控制在一个小时以内。

---

## 28:20–29:00｜收束

[真人镜头｜近景｜约 20 秒]

这一集只做了一张任务卡。

它能区分已知和未知，缺信息会停，确认以后能继续，过程也留了记录。

下一集，我们让模型进入这条流程。

到时候要看的问题很具体：它提取了什么，猜了什么，哪些值仍然需要人确认。

[结束画面：M01 生成的四份文件 + M02 预告]

---

# 录制注意

- 所有命令在正式录屏前完整跑一遍；
- 保留 v0 的错误结果，不剪掉；
- JSON 展示时使用 125%–150% 字号；
- 终端每次只运行一条命令；
- 状态变更使用同一位置的状态条；
- 真人口播可自由调整语气，不改动技术边界；
- 不展示本机用户名、绝对路径、通知和浏览器账号。
