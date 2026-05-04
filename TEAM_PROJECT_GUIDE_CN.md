# ARISplus 科研增强项目组员上手说明

本文档是本课程项目的公开上手入口，适合所有组员在开始开发前阅读。它说明三件事：

1. 我们为什么要改进原始 ARIS 项目。
2. 五个成员分别负责什么模块。
3. 当前仓库里已经有哪些文件可以参考、修改和测试。

请注意：本文档面向组员公开，不包含组长与 Agent 讨论项目推进时使用的私有材料。

---

## 1. 项目定位

原始项目 `ARIS / Auto-claude-code-research-in-sleep` 是一个面向科研全流程的 Agent 工作流系统。它不是从零实现一个新的 Agent runtime（Agent 运行时），而是在 Claude Code 这类宿主 Agent 之上增加科研任务能力。

原始 ARIS 的核心思路是：

- Claude Code（宿主执行 Agent）负责读文件、写代码、跑实验、整理结果。
- 外部 reviewer（评审模型）负责审稿、打分、指出弱点和给出修改建议。
- 两个模型不互相给自己的产物打分，形成跨模型 feedback loop（反馈循环）。

本课程项目不准备推翻原始设计，而是在保留 ARIS 原有科研 workflow（工作流）的基础上做增强。

我们的项目可以概括为：

```text
在原始 ARIS 科研工作流之上，增加论文质量评价、投稿准备度、统一状态、产物图谱和静态 dashboard。
```

---

## 2. 本次改进目标

当前希望把 ARIS 增强成一个更适合课程展示和最终答辩的科研增强版 Agent。重点不是多做几个互相评分的 Agent，而是让科研过程更可评价、可追踪、可展示、可协作。

本次改进分为五个方向：

1. Paper Quality Eval（论文质量评价）
2. Submission Readiness（投稿准备度）
3. Unified State（统一状态中心）
4. Artifact Graph / Research Wiki（产物图谱 / 研究维基）
5. Static Dashboard（静态仪表盘）与报告展示

这些方向的关系是：

```text
成员 1 生成论文质量评价 JSON
成员 2 聚合投稿准备度
成员 3 汇总统一状态和 dashboard 数据
成员 4 生成产物图谱
成员 5 渲染报告和 dashboard 页面
```

成员之间通过 JSON 文件协作，不需要等待其他人完全写完才能开始。每个人都可以先使用 mock data（模拟数据）开发自己的模块。

---

## 3. 开发边界

本课程项目当前只考虑 Claude Code 方向，不做 Codex CLI 原生适配。

本项目要做：

- 保留原始 ARIS 的 skill（技能）机制。
- 保留 Claude Code + external reviewer（外部评审模型）的双模型协作设计。
- 增加结构化 JSON 输出，便于后续展示和测试。
- 增加静态 dashboard（仪表盘），便于答辩展示。
- 增加可测试的 Python 工具脚本。

本项目暂时不做：

- 不做 Codex CLI 原生 skill 镜像。
- 不做多 reviewer 投票系统。
- 不做完整后端服务。
- 不做数据库。
- 不做复杂前端框架。
- 不把私有讨论文档提交给组员。

---

## 4. 原始项目结构速览

开始开发前，建议先理解这些目录：

| 路径 | 作用 |
|---|---|
| `README.md` | 原始项目英文说明 |
| `README_CN.md` | 原始项目中文说明 |
| `AGENT_GUIDE.md` | 原始项目 Agent 使用说明 |
| `skills/` | Claude Code 使用的 skill（技能）说明 |
| `tools/` | 本地工具脚本，主要是 Python / Bash / PowerShell |
| `templates/` | Markdown 报告模板 |
| `tests/` | 自动测试 |
| `dashboard/` | 本次新增的静态 dashboard 页面 |
| `docs/team/` | 本次新增的组员开发文档 |

运行后可能会出现这些目录或文件：

| 路径 | 作用 |
|---|---|
| `paper/` | 论文和评价报告输出目录 |
| `.aris/` | 本地状态、追踪记录、dashboard 数据目录 |

---

## 5. 当前已经新增的公开文件

以下文件已经在当前 GitHub 仓库中，可以直接查看。

### 5.1 根目录入口文档

| 文件 | 用途 |
|---|---|
| `TEAM_PROJECT_GUIDE_CN.md` | 当前这份总览文档，所有组员优先阅读 |

### 5.2 组员开发文档

| 文件 | 用途 |
|---|---|
| `docs/team/DEVELOPMENT_GUIDE_CN.md` | 更具体的开发说明、模块边界和测试要求 |
| `docs/team/INTERFACES_CN.md` | 各模块 JSON 接口约定 |
| `docs/team/GITHUB_COLLABORATION_CN.md` | GitHub 协作流程说明 |

### 5.3 论文质量评价模块

| 文件 | 用途 |
|---|---|
| `skills/paper-quality-eval/SKILL.md` | 成员 1 的核心 skill（技能）说明 |
| `tests/test_paper_quality_eval_contract.py` | 论文质量评价 JSON contract test（结构测试） |
| `tests/fixtures/mock_paper_quality_report.json` | 论文质量评价 mock JSON（模拟数据） |

### 5.4 报告与 dashboard 展示模块

| 文件 | 用途 |
|---|---|
| `templates/PAPER_QUALITY_REPORT_TEMPLATE.md` | 论文质量 Markdown 报告模板 |
| `tools/render_paper_quality_report.py` | 把 JSON 渲染成 Markdown 报告的工具 |
| `tools/render_dashboard.py` | 把 dashboard 数据写入静态页面的工具 |
| `dashboard/index.html` | 静态 dashboard 页面 |
| `dashboard/app.js` | dashboard 前端逻辑 |
| `dashboard/style.css` | dashboard 样式 |
| `tests/test_paper_quality_report_renderer.py` | 报告渲染测试 |
| `tests/test_coursework_dashboard.py` | dashboard 渲染测试 |
| `tests/fixtures/mock_dashboard_data.json` | dashboard mock JSON（模拟数据） |

---

## 6. 五个成员分工

下面是五个可选模块。组员可以根据兴趣选择，也可以由组长最终协调。

### 成员 1：Paper Quality Eval（论文质量评价核心）

成员 1 负责“怎么评价论文”。

主要任务：

- 新增和完善 `paper-quality-eval` skill（论文质量评价技能）。
- 设计 reviewer prompt（评审提示词）。
- 让外部 reviewer（评审模型）按 rubric（评价量表）输出结构化 JSON。
- 保证输出文件 `paper/PAPER_QUALITY_REPORT.json` 的结构稳定。
- 每个评分维度都要包含 score（分数）、evidence（证据）、rationale（理由）和 minimum_fix（最小修复建议）。

主要负责文件：

- `skills/paper-quality-eval/SKILL.md`
- `tests/test_paper_quality_eval_contract.py`
- `tests/fixtures/mock_paper_quality_report.json`

最终输出：

- `paper/PAPER_QUALITY_REPORT.json`

是否需要 API：

- 写 schema（结构约定）、prompt（提示词）和测试时不需要。
- 真实调用外部 reviewer（评审模型）时需要大模型 API。

验收标准：

- JSON 能通过 `tests/test_paper_quality_eval_contract.py`。
- 7 个 rubric（评价量表）维度完整。
- 每个维度都有证据和最小修改建议。
- 输出不要包含 API key（密钥）或私人信息。

---

### 成员 2：Submission Readiness（投稿准备度）

成员 2 负责“当前论文是否接近可投稿”。

主要任务：

- 读取论文质量评价、实验结果、审计结果等文件。
- 汇总论文当前是否 ready（可投稿）、almost（接近可投稿）、blocked（被阻塞）或 draft_only（仅适合草稿）。
- 输出结构化投稿准备度报告。
- 给出 blocking items（阻塞项）和 recommended actions（推荐行动）。

建议新增或修改文件：

- `tools/submission_readiness.py`
- `skills/submission-assurance/SKILL.md`
- `templates/SUBMISSION_READINESS_REPORT_TEMPLATE.md`
- `tests/test_submission_readiness.py`
- `tests/fixtures/mock_submission_readiness_report.json`

最终输出：

- `paper/SUBMISSION_READINESS_REPORT.json`
- `paper/SUBMISSION_READINESS_REPORT.md`

是否需要 API：

- 默认不需要。这个模块主要是规则聚合和文件检查。

验收标准：

- 能读取 `paper/PAPER_QUALITY_REPORT.json`。
- 能在缺少部分文件时给出合理的 warning（警告）而不是崩溃。
- 能输出投稿准备度状态和阻塞项。
- 测试覆盖 ready / almost / blocked 等典型情况。

---

### 成员 3：Unified State（统一状态中心）

成员 3 负责“把零散状态整理成统一状态文件”。

主要任务：

- 扫描项目已有产物，例如论文评价、投稿准备度、实验状态、产物图谱。
- 生成 `.aris/state.json`。
- 生成 `.aris/dashboard_data.json`，作为 dashboard（仪表盘）的唯一数据入口。
- 让展示层不需要直接到处读取原始文件。

建议新增或修改文件：

- `tools/state_exporter.py`
- `tools/experiment_state_exporter.py`
- `tests/test_state_exporter.py`
- `tests/fixtures/mock_state_inputs/`

最终输出：

- `.aris/state.json`
- `.aris/dashboard_data.json`

是否需要 API：

- 不需要。这个模块只做本地文件聚合。

验收标准：

- 能消费成员 1、成员 2、成员 4 的 JSON。
- 能生成 dashboard 所需的数据结构。
- 缺少某个模块输出时，状态显示为 unknown（未知）或 not available（不可用），不能直接报错退出。
- dashboard 只需要读取 `.aris/dashboard_data.json`。

---

### 成员 4：Artifact Graph / Research Wiki（产物图谱 / 研究维基）

成员 4 负责“科研过程里产生了哪些文件，它们之间有什么关系”。

主要任务：

- 扫描论文、实验结果、报告、图表、review trace（评审追踪记录）等 artifact（产物）。
- 生成 artifact graph（产物图谱），记录节点和依赖关系。
- 可选：导出 research-wiki（研究维基）风格的 Markdown 索引。
- 帮助答辩时说明整个科研流程是可追踪的。

建议新增或修改文件：

- `tools/artifact_graph.py`
- `tests/test_artifact_graph.py`
- `docs/team/ARTIFACT_GRAPH_CN.md`
- 可选：`templates/RESEARCH_WIKI_INDEX_TEMPLATE.md`

最终输出：

- `.aris/artifact_graph.json`
- 可选：`.aris/research_wiki/index.md`

是否需要 API：

- 不需要。这个模块主要是文件扫描和结构化整理。

验收标准：

- 能识别关键产物，例如论文、质量报告、投稿报告、实验结果、图表。
- 能生成 nodes（节点）和 edges（边）。
- 输出结构能被成员 3 和成员 5 消费。
- 缺少部分文件时仍能生成空图或部分图。

---

### 成员 5：Static Dashboard + Report Rendering（静态仪表盘 + 报告渲染）

成员 5 负责“怎么把结果展示给人看”。

主要任务：

- 读取 `paper/PAPER_QUALITY_REPORT.json`，渲染 `paper/PAPER_QUALITY_REPORT.md`。
- 读取 `.aris/dashboard_data.json`，渲染静态 dashboard（仪表盘）。
- 在 dashboard 中展示论文质量评分、投稿准备度、阶段状态、实验摘要和产物摘要。
- 保证页面打开即可展示，不需要后端服务。

主要负责文件：

- `tools/render_paper_quality_report.py`
- `tools/render_dashboard.py`
- `templates/PAPER_QUALITY_REPORT_TEMPLATE.md`
- `dashboard/index.html`
- `dashboard/app.js`
- `dashboard/style.css`
- `tests/test_paper_quality_report_renderer.py`
- `tests/test_coursework_dashboard.py`
- `tests/fixtures/mock_dashboard_data.json`

最终输出：

- `paper/PAPER_QUALITY_REPORT.md`
- `dashboard/index.html`

是否需要 API：

- 不需要。这个模块只消费 JSON 并展示。

验收标准：

- 能使用 mock JSON 生成 Markdown 报告。
- 能使用 mock dashboard data 生成可打开的 dashboard。
- 缺字段时页面显示 unknown（未知）或 not available（不可用），不能崩溃。
- 不修改成员 1 的评分逻辑。

---

## 7. 组长负责内容

组长不建议承担过多单一模块开发，而是负责整体整合和流程把控。

组长主要任务：

- 冻结 JSON schema（结构约定）。
- 审核成员 pull request（合并请求）。
- 处理跨模块接口不一致问题。
- 最终联调五个模块。
- 运行真实论文评价流程。
- 准备课程答辩展示材料。
- 确保私有讨论文档不会被提交到公开仓库。

组长重点关注：

- 每个成员是否只修改自己负责范围。
- 输出文件是否符合 `docs/team/INTERFACES_CN.md`。
- 测试是否能跑通。
- dashboard 是否能消费最终真实数据。
- API key（密钥）是否没有进入 git（版本控制）。

---

## 8. 模块之间的依赖关系

从最终产品角度看，模块之间有依赖关系：

```text
成员 1 -> 成员 2
成员 1 -> 成员 3
成员 2 -> 成员 3
成员 4 -> 成员 3
成员 3 -> 成员 5
成员 1 -> 成员 5
```

但是从开发角度看，大家可以并行开发。

原因是：

- 每个模块都可以先用 mock JSON（模拟数据）。
- 接口已经写在 `docs/team/INTERFACES_CN.md`。
- 生产者和消费者只需要遵守同一份 JSON schema（结构约定）。
- 最终联调时再把 mock JSON 换成真实输出。

建议并行方式：

1. 成员 1 先固定 `PAPER_QUALITY_REPORT.json` 的核心字段。
2. 成员 2 使用 mock `PAPER_QUALITY_REPORT.json` 开发投稿准备度。
3. 成员 3 使用所有 mock JSON 开发统一状态。
4. 成员 4 独立开发产物扫描和图谱输出。
5. 成员 5 使用 mock dashboard data 开发展示页面。

---

## 9. 推荐开发流程

每位成员开始前建议按以下流程：

1. 阅读 `README_CN.md`，了解原始 ARIS 是什么。
2. 阅读本文档，了解本课程项目要改什么。
3. 阅读 `docs/team/INTERFACES_CN.md`，确认自己的输入和输出。
4. 选择一个模块并新建 git branch（分支）。
5. 先写 mock data（模拟数据）和 test（测试）。
6. 再写工具脚本或 skill（技能）。
7. 本地测试通过后提交 pull request（合并请求）。

推荐分支命名：

```text
member1-paper-quality-eval
member2-submission-readiness
member3-unified-state
member4-artifact-graph
member5-dashboard
```

---

## 10. 测试方式

如果本地安装了 pytest：

```bash
python -m pytest tests/test_paper_quality_eval_contract.py
python -m pytest tests/test_paper_quality_report_renderer.py
python -m pytest tests/test_coursework_dashboard.py
```

如果本地没有 pytest，也可以先做语法检查：

```bash
python -m compileall tools tests
```

成员新增模块时，至少要提供：

- 一个 mock JSON（模拟数据）。
- 一个测试文件。
- 一个能生成目标输出的命令或函数。

---

## 11. API 与费用说明

默认情况下，大部分成员不需要调用大模型 API。

需要 API 的情况：

- 成员 1 如果真实运行 reviewer（评审模型）生成论文质量评价，需要 API。
- 组长最终联调真实论文评价时，可能需要 API。

不需要 API 的情况：

- 成员 2 投稿准备度聚合。
- 成员 3 统一状态中心。
- 成员 4 产物图谱。
- 成员 5 dashboard 和报告渲染。
- 所有成员使用 mock JSON 开发和测试。

重要要求：

- 不要把 API key（密钥）写进代码。
- 不要把 API key 写进 JSON、Markdown 或测试文件。
- 如果需要共享 API，由组长统一提供运行方式，不要提交到 GitHub。

---

## 12. GitHub 协作方式

建议协作方式：

1. 组员 fork（派生）或 clone（克隆）当前仓库。
2. 每个人基于 `main` 新建自己的 branch（分支）。
3. 只修改自己负责模块的文件。
4. 提交 pull request（合并请求）。
5. 组长 review（审核）后合并。

提交前请检查：

- 没有提交 `.private/`。
- 没有提交 `docs/coursework/`。
- 没有提交 `AGENTS.md`。
- 没有提交 API key。
- 测试文件能运行或至少能通过语法检查。

更详细的 GitHub 操作说明见：

- `docs/team/GITHUB_COLLABORATION_CN.md`

---

## 13. 选择模块时可以参考的标准

如果你更喜欢 prompt engineering（提示词工程）和论文评价，可以选成员 1。

如果你更喜欢规则聚合、质量门禁和流程判断，可以选成员 2。

如果你更喜欢数据结构、状态管理和系统整合，可以选成员 3。

如果你更喜欢文件扫描、知识图谱和可追踪性，可以选成员 4。

如果你更喜欢前端展示、报告排版和答辩可视化，可以选成员 5。

每个模块都可以独立开始开发。真正需要统一协调的是 JSON 字段命名和最终联调。

