"use strict";

const requestText = "请把上个月收到的用户问题整理一下，下周评审时用。";

const explicitCard = {
  objective: "整理用户问题",
  time_range_text: "上个月",
  usage_context: "下周评审",
  source: null,
  time_range: null,
  expected_output: null,
  due_date: null,
  owner: null,
  acceptance_criteria: []
};

const v0Card = {
  ...explicitCard,
  source: "feedback.csv",
  time_range: { relative: "LAST_MONTH" },
  expected_output: ["PPT"],
  due_date: "NEXT_FRIDAY",
  owner: "CURRENT_USER",
  acceptance_criteria: ["内容已整理"]
};

const confirmation = {
  source: "feedback.csv",
  time_range: { start: "2026-07-01", end: "2026-07-31" },
  expected_output: ["Excel 汇总表", "一页摘要"],
  due_date: "2026-08-10T17:00:00+08:00",
  owner: "Alex",
  reviewer: "Morgan",
  acceptance_criteria: [
    "全部问题完成分类",
    "重复项已合并",
    "每项保留原始编号"
  ],
  confirmed_by: "DEMO_REQUESTER"
};

const questions = [
  "用户问题存放在哪里？请给出一个明确的数据来源或演示文件。",
  "“上个月”对应哪个具体日期范围？",
  "需要输出什么文件或材料？",
  "评审的具体日期和截止时间是什么？",
  "谁负责完成这项任务？",
  "哪些条件满足后，可以认为整理工作完成？"
];

const steps = [
  {
    navTitle: "打开请求",
    navSubtitle: "先看一个具体对象",
    title: "从一条模糊需求开始",
    subtitle: "今天只完成一件事：把原始请求变成一张可以确认的任务卡。",
    status: "DRAFT",
    boundary: "请求刚被记录，系统尚未判断能否开始。",
    evidence: [
      ["原始请求", "request.txt 已读取"],
      ["公开边界", "PUBLIC_DEMO 合成案例"]
    ],
    render: () => `
      <p class="step-kicker">STEP 01 · REQUEST</p>
      <h2>先读文件</h2>
      <p class="stage-intro">不从 Agent 定义开始。屏幕上先出现一条日常工作消息。</p>
      <div class="request-card fade-in">
        <blockquote>${requestText}</blockquote>
      </div>
      <div class="question-cloud fade-in" aria-label="原始请求中的不确定信息">
        ${[
          "用户问题在哪里？",
          "上个月是哪段日期？",
          "输出什么格式？",
          "评审具体哪一天？",
          "谁负责？",
          "怎样算完成？"
        ].map(item => `<div class="question-pill">${item}</div>`).join("")}
      </div>
    `
  },
  {
    navTitle: "人工提取",
    navSubtitle: "只记录原文明确内容",
    title: "原文给了什么，就先写什么",
    subtitle: "空值准确地表示当前未知。任务卡不需要假装完整。",
    status: "DRAFT",
    boundary: "当前只有目标、相对时间和使用场景来自原文。",
    evidence: [
      ["目标", "整理用户问题 · SOURCE_TEXT"],
      ["相对时间", "上个月 · SOURCE_TEXT"],
      ["使用场景", "下周评审 · SOURCE_TEXT"]
    ],
    render: () => `
      <p class="step-kicker">STEP 02 · EXPLICIT FIELDS</p>
      <h2>只提取明确存在的信息</h2>
      <p class="stage-intro">日期范围、数据来源、输出、负责人和验收标准仍然为空。这里没有错误，只是还不知道。</p>
      ${renderFieldGrid([
        field("objective", "整理用户问题", "source"),
        field("time_range_text", "上个月", "source"),
        field("usage_context", "下周评审", "source"),
        field("source", null, "missing"),
        field("expected_output", null, "missing"),
        field("due_date", null, "missing"),
        field("owner", null, "missing"),
        field("acceptance_criteria", null, "missing")
      ])}
    `
  },
  {
    navTitle: "运行 v0",
    navSubtitle: "观察静默默认值",
    title: "第一版代码运行成功",
    subtitle: "v0 会给空字段补默认值，然后把任务标记为 READY。",
    status: "READY",
    boundary: "READY 由未确认默认值产生，当前证据不足。",
    evidence: [
      ["进程", "退出码 0"],
      ["状态", "READY"],
      ["确认来源", "无"]
    ],
    render: () => `
      <p class="step-kicker">STEP 03 · RUN V0</p>
      <h2>先运行，再看结果</h2>
      <p class="stage-intro">点击运行。这个步骤故意保留一个常见设计问题。</p>
      ${renderCodeWindow("course $", `python task_pipeline.py \\\n  --mode v0 \\\n  --request data/request.txt \\\n  --output output-v0`)}
      <div class="terminal-output" id="v0-output">等待运行。</div>
      <button class="button button-primary inline-action" data-action="run-v0" type="button">运行 v0</button>
    `
  },
  {
    navTitle: "检查 v0",
    navSubtitle: "代码正确，语义错误",
    title: "文件很完整，依据却不存在",
    subtitle: "PPT、NEXT_FRIDAY 和 CURRENT_USER 都由系统补入，原始请求没有提供这些信息。",
    status: "READY",
    boundary: "任务被过早标记为 READY。系统默认值不能自动升级为业务事实。",
    evidence: [
      ["输出形式", "PPT · 未确认默认值"],
      ["截止日期", "NEXT_FRIDAY · 未确认默认值"],
      ["负责人", "CURRENT_USER · 未确认默认值"]
    ],
    render: () => `
      <p class="step-kicker">STEP 04 · INSPECT V0</p>
      <h2>定位安静的错误</h2>
      <p class="stage-intro">程序没有崩溃。问题发生在工作语义里。</p>
      <div class="diff-grid fade-in">
        <section class="diff-panel bad">
          <h3>v0 写入的值</h3>
          ${diffLine("+", 'expected_output = ["PPT"]')}
          ${diffLine("+", 'due_date = "NEXT_FRIDAY"')}
          ${diffLine("+", 'owner = "CURRENT_USER"')}
          ${diffLine("+", 'status = "READY"')}
        </section>
        <section class="diff-panel good">
          <h3>原始请求能支持的值</h3>
          ${diffLine("✓", 'objective = "整理用户问题"')}
          ${diffLine("✓", 'time_range_text = "上个月"')}
          ${diffLine("✓", 'usage_context = "下周评审"')}
          ${diffLine("—", "其余字段仍未知")}
        </section>
      </div>
      <div class="alert-card danger fade-in">
        <div class="alert-icon">!</div>
        <div>
          <strong>代码执行正确，任务语义错误</strong>
          <p>模型可以猜得更自然，来源仍然是猜。下一版先删除静默默认值。</p>
        </div>
      </div>
    `
  },
  {
    navTitle: "构建 v1",
    navSubtitle: "缺信息时明确停止",
    title: "把未知变成澄清问题",
    subtitle: "v1 检查必填字段。信息不足时，任务停留在 NEEDS_CLARIFICATION。",
    status: "NEEDS_CLARIFICATION",
    boundary: "任务尚未具备执行条件，系统只生成问题和记录。",
    evidence: [
      ["缺失字段", "6 个"],
      ["状态", "NEEDS_CLARIFICATION"],
      ["最终任务卡", "尚未批准"]
    ],
    render: () => `
      <p class="step-kicker">STEP 05 · BUILD V1</p>
      <h2>缺什么，直接写出来</h2>
      <p class="stage-intro">这一版不会填默认值。点击运行，查看系统为什么停下。</p>
      ${renderCodeWindow("course $", `python task_pipeline.py \\\n  --mode v1 \\\n  --request data/request.txt \\\n  --output output-v1`)}
      <div class="terminal-output" id="v1-output">等待运行。</div>
      <button class="button button-primary inline-action" data-action="run-v1" type="button">运行 v1</button>
      <div id="question-result"></div>
    `
  },
  {
    navTitle: "人工确认",
    navSubtitle: "确认任务含义",
    title: "让负责人补齐任务卡",
    subtitle: "确认文件给出具体日期、负责人、输出和验收条件，并记录 confirmed_by。",
    status: "NEEDS_CLARIFICATION",
    boundary: "确认值尚未应用到任务卡，系统仍停在等待澄清。",
    evidence: [
      ["确认文件", "confirmation.json"],
      ["确认人", "DEMO_REQUESTER"],
      ["当前状态", "等待应用确认"]
    ],
    render: () => `
      <p class="step-kicker">STEP 06 · HUMAN CONFIRMATION</p>
      <h2>系统不替人确认任务含义</h2>
      <p class="stage-intro">这份确认文件同样是公开合成数据。字段进入任务卡时会标记为 HUMAN_CONFIRMED。</p>
      ${renderCodeWindow("confirmation.json", JSON.stringify(confirmation, null, 2))}
      <div class="alert-card warning">
        <div class="alert-icon">i</div>
        <div>
          <strong>confirmed_by 是必要字段</strong>
          <p>系统需要知道哪些值已经得到明确确认，以及由谁确认。</p>
        </div>
      </div>
      <button class="button button-primary inline-action" data-action="apply-confirmation" type="button">应用人工确认</button>
      <div id="confirmation-result"></div>
    `
  },
  {
    navTitle: "READY 与证据",
    navSubtitle: "状态保持窄定义",
    title: "这次 READY 有依据",
    subtitle: "必填字段已经确认，可以进入执行准备。任务尚未执行，也没有完成评审。",
    status: "READY",
    boundary: "READY 只表示信息足够完整；执行、评审、发布和签发仍未发生。",
    evidence: [
      ["缺失字段", "0"],
      ["确认来源", "DEMO_REQUESTER"],
      ["运行记录", "run_record.json"],
      ["状态", "READY · 窄定义"]
    ],
    render: () => `
      <p class="step-kicker">STEP 07 · READY WITH EVIDENCE</p>
      <h2>检查最终任务卡</h2>
      <p class="stage-intro">状态来自明确的开始条件和人工确认。把它和“任务已完成”分开。</p>
      ${renderFieldGrid([
        field("objective", "整理用户问题", "source"),
        field("source", "feedback.csv", "human"),
        field("time_range", "2026-07-01 → 2026-07-31", "human"),
        field("expected_output", "Excel 汇总表 + 一页摘要", "human"),
        field("due_date", "2026-08-10 17:00 +08:00", "human"),
        field("owner", "Alex", "human"),
        field("reviewer", "Morgan", "human"),
        field("acceptance_criteria", "分类完成 / 重复项合并 / 保留原始编号", "human")
      ])}
      <div class="state-flow fade-in">
        ${stateNode("DRAFT", "请求已记录", "current-draft")}
        ${stateNode("NEEDS_CLARIFICATION", "信息不足，等待确认", "current-needs")}
        ${stateNode("READY", "可进入执行准备", "current-ready")}
      </div>
      <div class="alert-card success">
        <div class="alert-icon">✓</div>
        <div>
          <strong>READY 的窄定义</strong>
          <p>它没有表示任务已执行、交付已评审或结果已发布。</p>
        </div>
      </div>
    `
  },
  {
    navTitle: "概念与迁移",
    navSubtitle: "先经历，再命名",
    title: "刚才已经出现了五个 Agent 工程概念",
    subtitle: "下一集会在确定性骨架中加入模型，让模型只生成候选信息。",
    status: "READY",
    boundary: "模型将生成候选；规则检查和人工确认继续保留。",
    evidence: [
      ["本集资产", "4 份输出文件"],
      ["失败路径", "v0 静默默认值"],
      ["下一层", "模型候选提取器"]
    ],
    render: () => `
      <p class="step-kicker">STEP 08 · NAME & TRANSFER</p>
      <h2>现在再给它们起名字</h2>
      <p class="stage-intro">概念都已经在文件、状态和操作里出现过。</p>
      <div class="concept-grid fade-in">
        ${conceptCard("输入契约", "任务开始前必须具备哪些字段。")}
        ${conceptCard("状态", "任务当前处于草稿、等待澄清或准备完成。")}
        ${conceptCard("Human-in-the-loop", "人确认日期、负责人和验收条件。")}
        ${conceptCard("Trace / Evidence", "原始请求、缺失字段、确认来源和状态可回看。")}
        ${conceptCard("责任边界", "程序检查字段，人确认任务含义。")}
      </div>
      <div class="model-insert fade-in" aria-label="M02 模型插入位置">
        ${modelNode("原始请求", "自然语言")}
        <div class="flow-arrow">→</div>
        ${modelNode("模型", "只生成候选", "candidate")}
        <div class="flow-arrow">→</div>
        ${modelNode("规则 + 人工确认", "决定是否 READY")}
      </div>
      <h3 class="section-heading">你的 M01 提交物</h3>
      <div class="file-grid">
        ${fileCard("request.txt", "虚构或彻底脱敏的原始请求")}
        ${fileCard("confirmation.json", "明确的人工确认")}
        ${fileCard("task_card.json", "带字段来源的任务卡")}
        ${fileCard("questions.md", "缺失信息对应的问题")}
        ${fileCard("run_record.json", "状态、原因与确认来源")}
        ${fileCard("停止条件", "至少一项不能继续的情况")}
      </div>
    `
  }
];

let currentStep = 0;
const localState = {
  v0Ran: false,
  v1Ran: false,
  confirmationApplied: false
};

const nav = document.querySelector("#lesson-nav");
const stage = document.querySelector("#stage");
const title = document.querySelector("#step-title");
const subtitle = document.querySelector("#step-subtitle");
const statusChip = document.querySelector("#status-chip");
const evidenceList = document.querySelector("#evidence-list");
const evidenceCount = document.querySelector("#evidence-count");
const boundaryCopy = document.querySelector("#boundary-copy");
const progressLabel = document.querySelector("#progress-label");
const progressBar = document.querySelector("#progress-bar");
const prevButton = document.querySelector("#prev-button");
const nextButton = document.querySelector("#next-button");

function field(name, value, source) {
  return { name, value, source };
}

function sourceMeta(source) {
  const lookup = {
    source: ["SOURCE_TEXT", "source-text"],
    default: ["UNCONFIRMED", "source-default"],
    human: ["HUMAN_CONFIRMED", "source-human"],
    missing: ["MISSING", "source-missing"]
  };
  return lookup[source] || lookup.missing;
}

function valueToText(value) {
  if (value === null || value === undefined || value === "") return "当前未知";
  if (Array.isArray(value)) return value.join(" / ");
  if (typeof value === "object") return JSON.stringify(value);
  return String(value);
}

function renderFieldGrid(items) {
  return `
    <div class="field-grid fade-in">
      ${items.map(item => {
        const [label, className] = sourceMeta(item.source);
        const missing = item.source === "missing";
        return `
          <section class="field-card">
            <div class="field-card-header">
              <span class="field-name">${item.name}</span>
              <span class="source-tag ${className}">${label}</span>
            </div>
            <div class="field-value ${missing ? "missing" : ""}">${valueToText(item.value)}</div>
          </section>
        `;
      }).join("")}
    </div>
  `;
}

function renderCodeWindow(windowTitle, code) {
  const escaped = code
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;");
  return `
    <div class="code-window fade-in">
      <div class="window-bar">
        <span></span><span></span><span></span>
        <strong class="window-title">${windowTitle}</strong>
      </div>
      <pre><code>${escaped}</code></pre>
    </div>
  `;
}

function diffLine(symbol, text) {
  return `<div class="diff-line"><span class="diff-symbol">${symbol}</span><span>${text}</span></div>`;
}

function stateNode(name, copy, className) {
  return `<section class="state-node ${className}"><strong>${name}</strong><span>${copy}</span></section>`;
}

function conceptCard(name, copy) {
  return `<section class="concept-card"><strong>${name}</strong><p>${copy}</p></section>`;
}

function fileCard(name, copy) {
  return `<section class="file-card"><code>${name}</code><p>${copy}</p></section>`;
}

function modelNode(name, copy, className = "") {
  return `<section class="model-node ${className}"><strong>${name}</strong><span>${copy}</span></section>`;
}

function buildNav() {
  nav.innerHTML = steps.map((step, index) => `
    <button class="nav-step" type="button" data-step="${index}">
      <span class="nav-step-index">${String(index + 1).padStart(2, "0")}</span>
      <span class="nav-step-copy">
        <strong>${step.navTitle}</strong>
        <span>${step.navSubtitle}</span>
      </span>
    </button>
  `).join("");

  nav.addEventListener("click", event => {
    const button = event.target.closest("[data-step]");
    if (!button) return;
    currentStep = Number(button.dataset.step);
    render();
  });
}

function setStatus(status) {
  statusChip.textContent = status;
  statusChip.className = "status-chip";
  if (status === "READY") statusChip.classList.add("status-ready");
  else if (status === "NEEDS_CLARIFICATION") statusChip.classList.add("status-needs");
  else statusChip.classList.add("status-draft");
}

function renderEvidence(items) {
  evidenceCount.textContent = String(items.length);
  if (!items.length) {
    evidenceList.innerHTML = `<div class="evidence-empty">当前还没有可用证据。</div>`;
    return;
  }

  evidenceList.innerHTML = items.map(([name, copy]) => `
    <div class="evidence-item fade-in">
      <strong>${name}</strong>
      <span>${copy}</span>
    </div>
  `).join("");
}

function render() {
  const step = steps[currentStep];
  title.textContent = step.title;
  subtitle.textContent = step.subtitle;
  stage.innerHTML = step.render();
  setStatus(step.status);
  renderEvidence(step.evidence);
  boundaryCopy.textContent = step.boundary;

  progressLabel.textContent = `${currentStep + 1} / ${steps.length}`;
  progressBar.style.width = `${((currentStep + 1) / steps.length) * 100}%`;

  [...nav.querySelectorAll("[data-step]")].forEach((button, index) => {
    if (index === currentStep) button.setAttribute("aria-current", "step");
    else button.removeAttribute("aria-current");
  });

  prevButton.disabled = currentStep === 0;
  nextButton.disabled = currentStep === steps.length - 1;
  nextButton.textContent = currentStep === steps.length - 2 ? "进入总结" : "下一步";

  attachStageActions();
  window.scrollTo({ top: 0, behavior: "smooth" });
}

function attachStageActions() {
  stage.querySelectorAll("[data-action]").forEach(button => {
    button.addEventListener("click", () => handleAction(button.dataset.action, button));
  });
}

function handleAction(action, button) {
  if (action === "run-v0") {
    localState.v0Ran = true;
    const output = document.querySelector("#v0-output");
    output.innerHTML = `<strong>status=READY</strong><br>exit_code=0<br>confirmed_by=null`;
    button.textContent = "v0 已运行";
    button.disabled = true;
    return;
  }

  if (action === "run-v1") {
    localState.v1Ran = true;
    const output = document.querySelector("#v1-output");
    output.innerHTML = `<span class="warning-text">status=NEEDS_CLARIFICATION</span><br>missing=source,time_range,expected_output,due_date,owner,acceptance_criteria<br>exit_code=2`;
    const result = document.querySelector("#question-result");
    result.innerHTML = `
      <h3 class="section-heading">questions.md</h3>
      <ol class="question-list fade-in">
        ${questions.map(question => `<li>${question}</li>`).join("")}
      </ol>
    `;
    button.textContent = "v1 已运行";
    button.disabled = true;
    return;
  }

  if (action === "apply-confirmation") {
    localState.confirmationApplied = true;
    const result = document.querySelector("#confirmation-result");
    result.innerHTML = `
      <div class="terminal-output fade-in">
        <strong>status=READY</strong><br>
        missing=<br>
        confirmed_by=DEMO_REQUESTER
      </div>
      <div class="alert-card success fade-in">
        <div class="alert-icon">✓</div>
        <div>
          <strong>确认已应用</strong>
          <p>必填字段均有明确来源。下一步检查 READY 的窄定义。</p>
        </div>
      </div>
    `;
    button.textContent = "人工确认已应用";
    button.disabled = true;
  }
}

prevButton.addEventListener("click", () => {
  if (currentStep <= 0) return;
  currentStep -= 1;
  render();
});

nextButton.addEventListener("click", () => {
  if (currentStep >= steps.length - 1) return;
  currentStep += 1;
  render();
});

window.addEventListener("keydown", event => {
  if (["INPUT", "TEXTAREA", "SELECT"].includes(document.activeElement?.tagName)) return;
  if (event.key === "ArrowLeft" && currentStep > 0) {
    currentStep -= 1;
    render();
  }
  if (event.key === "ArrowRight" && currentStep < steps.length - 1) {
    currentStep += 1;
    render();
  }
});

buildNav();
render();
