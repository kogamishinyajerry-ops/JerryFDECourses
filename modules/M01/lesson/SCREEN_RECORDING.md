# M01 屏幕录制 Runbook

## 1. 录制目标

录出一套不依赖真人画面的技术主轨：

- 原始请求；
- 任务卡草稿；
- v0 静默默认值；
- v1 明确停止；
- 澄清问题；
- 人工确认；
- READY 任务卡；
- 运行记录；
- 单元测试。

所有素材均使用仓库内公开合成数据。

## 2. 录制前清理

- 使用独立浏览器 Profile；
- 关闭通知、邮件、聊天和日历；
- 隐藏书签栏和账号头像；
- 终端提示符设置为 `course $`；
- 编辑器隐藏最近文件、插件账号和 Git 身份；
- 窗口只显示相对路径；
- 输出目录在录制前删除；
- 系统时间如进入画面，使用课程演示环境；
- 不打开仓库以外的文件。

## 3. 推荐窗口

### 编辑器

- 字号：18–22 px；
- 行高：1.5；
- 左侧文件树宽度约 260 px；
- 自动隐藏 Mini Map；
- 不显示真实绝对路径。

### 终端

- 字号：20–24 px；
- 尺寸：100–120 列；
- 主题：深色高对比；
- 每次只保留一条命令和结果；
- 清屏后开始每一段录制。

### 互动页面

直接打开：

```text
modules/M01/site/index.html
```

浏览器缩放：100% 或 110%。

## 4. 准备命令

从仓库根目录执行：

```bash
rm -rf modules/M01/lab/output-v0
rm -rf modules/M01/lab/output-v1
rm -rf modules/M01/lab/output-ready
```

Windows PowerShell：

```powershell
Remove-Item modules/M01/lab/output-v0 -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item modules/M01/lab/output-v1 -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item modules/M01/lab/output-ready -Recurse -Force -ErrorAction SilentlyContinue
```

## 5. 素材录制顺序

### S01｜原始请求

打开：

```text
modules/M01/lab/data/request.txt
```

动作：

1. 文件树定位；
2. 单击打开；
3. 停留 4 秒；
4. 选中“上个月”；
5. 选中“下周评审”；
6. 清除选区。

建议素材长度：20–25 秒。

### S02｜任务卡草稿

使用互动页面第 2 步，或打开参考任务卡：

```text
modules/M01/lab/reference_output/needs_clarification/task_card.json
```

动作：依次高亮明确字段和空值。

建议素材长度：35–45 秒。

### S03｜运行 v0

```bash
python modules/M01/lab/task_pipeline.py \
  --mode v0 \
  --request modules/M01/lab/data/request.txt \
  --output modules/M01/lab/output-v0
```

必须录到：

```text
status=READY
```

建议素材长度：15–20 秒。

### S04｜检查 v0 输出

打开：

```text
modules/M01/lab/output-v0/task_card.json
```

依次高亮：

```text
PPT
NEXT_FRIDAY
CURRENT_USER
SYSTEM_DEFAULT_UNCONFIRMED
confirmed_by: null
```

建议素材长度：40–50 秒。

### S05｜定位默认值代码

打开 `task_pipeline.py`，搜索：

```text
V0_DEFAULTS
```

再定位：

```text
apply_v0_defaults
```

建议素材长度：30–40 秒。

### S06｜运行没有确认的 v1

```bash
python modules/M01/lab/task_pipeline.py \
  --mode v1 \
  --request modules/M01/lab/data/request.txt \
  --output modules/M01/lab/output-v1
```

命令预期返回非 0。录屏时不要立即清掉结果。

必须录到：

```text
status=NEEDS_CLARIFICATION
missing=source,time_range,expected_output,due_date,owner,acceptance_criteria
```

建议素材长度：20–25 秒。

### S07｜澄清问题

打开：

```text
modules/M01/lab/output-v1/questions.md
```

缓慢滚动全部六个问题。

建议素材长度：35–45 秒。

### S08｜停止记录

打开：

```text
modules/M01/lab/output-v1/run_record.json
```

高亮：

```text
status
missing_fields
confirmed_fields
message
```

建议素材长度：30–40 秒。

### S09｜人工确认

打开：

```text
modules/M01/lab/data/confirmation.json
```

高亮：

```text
time_range
expected_output
due_date
owner
acceptance_criteria
confirmed_by
```

建议素材长度：45–55 秒。

### S10｜运行 READY 路径

```bash
python modules/M01/lab/task_pipeline.py \
  --mode v1 \
  --request modules/M01/lab/data/request.txt \
  --confirmation modules/M01/lab/data/confirmation.json \
  --output modules/M01/lab/output-ready
```

必须录到：

```text
status=READY
```

建议素材长度：15–20 秒。

### S11｜READY 任务卡

打开：

```text
modules/M01/lab/output-ready/task_card.json
```

高亮字段来源和 `confirmed_by`。

建议素材长度：50–60 秒。

### S12｜运行记录

打开：

```text
modules/M01/lab/output-ready/run_record.json
```

高亮：

```text
missing_fields: []
confirmed_fields
confirmed_by
message
```

建议素材长度：35–45 秒。

### S13｜单元测试

```bash
python -m unittest discover modules/M01/lab/tests -v
```

录到全部通过结果。

建议素材长度：20–30 秒。

### S14｜互动课件

录制八个步骤的切换：

1. 打开请求；
2. 人工提取；
3. 运行 v0；
4. 检查 v0；
5. 构建 v1；
6. 人工确认；
7. READY 与证据；
8. 概念与迁移。

建议分别录制，不要一次从头点到尾。

## 6. 补充动画

使用：

```text
modules/M01/assets/m01-flow.svg
```

建议在剪辑软件中制作：

- 节点按课程进度依次出现；
- v0 时在任务卡上叠加红色虚线默认值；
- v1 时高亮 NEEDS_CLARIFICATION；
- 人工确认后再点亮 READY；
- 结尾加入灰色模型候选框。

## 7. 画面检查

每段录制结束后检查：

- 是否出现本机用户名；
- 是否出现绝对路径；
- 是否出现账号、通知或书签；
- 是否出现非仓库文件；
- 字号是否在手机横屏可读；
- 终端结果是否与讲稿一致；
- v0 错误有没有被完整保留；
- READY 是否没有被表现成“任务完成”。

## 8. 文件命名

```text
M01_S01_request_v01.mov
M01_S02_draft-card_v01.mov
M01_S03_run-v0_v01.mov
...
M01_S14_interactive-site_v01.mov
```

真人素材：

```text
M01_H01_opening_v01.mov
M01_H02_assignment_v01.mov
M01_H03_closing_v01.mov
```

## 9. 交付清单

- 原始录屏；
- 剪辑代理文件；
- 最终旁白；
- 独立 SRT；
- SVG 原文件；
- 使用的 commit SHA；
- 公开安全检查结果；
- 录制中发现的勘误 Issue。
