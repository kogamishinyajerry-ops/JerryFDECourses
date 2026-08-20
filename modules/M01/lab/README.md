# M01 Build Lab

## 目标

用 Python 标准库构建一条任务准备闭环：

```text
原始请求
→ 明确信息
→ 缺失字段
→ 澄清问题
→ 人工确认
→ READY 任务卡
→ 运行记录
```

本实验不调用模型。

## 环境

- Python 3.10+；
- Windows / macOS / Linux；
- 无第三方依赖；
- 所有数据为公开合成样例。

## 目录

```text
lab/
├── task_pipeline.py
├── data/
│   ├── request.txt
│   └── confirmation.json
├── schemas/
│   └── task_card.schema.json
├── tests/
│   └── test_task_pipeline.py
└── reference_output/
```

## 实验 1｜运行 v0

```bash
python modules/M01/lab/task_pipeline.py \
  --mode v0 \
  --request modules/M01/lab/data/request.txt \
  --output modules/M01/lab/output-v0
```

预期退出码：`0`

预期状态：

```text
READY
```

打开 `output-v0/task_card.json`，找到：

```json
{
  "expected_output": ["PPT"],
  "due_date": "NEXT_FRIDAY",
  "owner": "CURRENT_USER"
}
```

检查 `field_provenance`。这些字段标记为：

```text
SYSTEM_DEFAULT_UNCONFIRMED
```

本轮要回答：代码为什么成功，任务仍然不能安全开始？

## 实验 2｜运行没有人工确认的 v1

```bash
python modules/M01/lab/task_pipeline.py \
  --mode v1 \
  --request modules/M01/lab/data/request.txt \
  --output modules/M01/lab/output-v1
```

预期退出码：`2`

预期状态：

```text
NEEDS_CLARIFICATION
```

检查：

```text
output-v1/task_card.json
output-v1/questions.md
output-v1/run_record.json
output-v1/status.txt
```

本轮要回答：系统为什么停下？缺失字段是否足以支持实际执行？

## 实验 3｜加入人工确认

```bash
python modules/M01/lab/task_pipeline.py \
  --mode v1 \
  --request modules/M01/lab/data/request.txt \
  --confirmation modules/M01/lab/data/confirmation.json \
  --output modules/M01/lab/output-ready
```

预期退出码：`0`

预期状态：

```text
READY
```

检查：

- `confirmed_by` 是否存在；
- 人工字段的 provenance 是否为 `HUMAN_CONFIRMED`；
- `missing_fields` 是否为空；
- `READY` 是否被正确解释为“可以进入执行准备”。

## 实验 4｜运行自动测试

```bash
python -m unittest discover modules/M01/lab/tests -v
```

测试覆盖：

- 原文显式字段提取；
- v0 静默默认值；
- v1 缺字段停止；
- v1 人工确认后 READY；
- 缺少 `confirmed_by` 时拒绝确认文件；
- 输出文件完整性；
- CLI 退出码。

## 学员改造

选择一句常见工作请求，改写为公开安全样例。

示例：

```text
请把最近的报名信息整理一下，周会上用。
```

不要提交真实人名、项目、日期、文件名和内部流程。

修改：

1. `request.txt`；
2. `confirmation.json`；
3. `QUESTION_MAP`；
4. 必填字段；
5. 至少一个单元测试。

## 思考题

1. 哪些字段适合由程序判断“有没有”？
2. 哪些字段只能由任务负责人确认含义？
3. 相对日期可以由程序解析到什么程度？
4. 什么时候允许系统使用默认值？需要留下什么证据？
5. `READY` 之后还需要哪些状态？
6. M02 加入模型以后，哪些测试必须继续保留？

## 公开边界声明

本实验只演示任务建模、状态、校验和人工确认。它不包含真实工程数据、专业工具链或内部流程，也不构成任何工程批准或业务决策依据。
