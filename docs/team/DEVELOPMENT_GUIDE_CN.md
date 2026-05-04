# ARIS 科研增强版开发文档（组员公开版）

本文档是组员开发入口。请配合阅读：

- `AGENT_GUIDE.md`
- `README.md`
- `docs/team/INTERFACES_CN.md`
- `docs/team/GITHUB_COLLABORATION_CN.md`

---

## 1. 开发边界

本课程项目只面向 Claude Code 宿主。

不做：

- Codex CLI 原生适配
- `skills/skills-codex/` 镜像开发
- 多 reviewer 投票
- 完整后端服务

保留：

- 原项目 Claude Code + 外部 reviewer 的双模型协作机制
- 原项目 skill / tool / artifact 文件协议

---

## 2. 原项目结构速览

| 目录 | 作用 |
|---|---|
| `skills/` | Claude Code 技能说明 |
| `tools/` | Python / Bash 工具脚本 |
| `templates/` | 输出模板 |
| `mcp-servers/` | 外部能力桥接 |
| `tests/` | 测试 |
| `paper/` | 论文输出，通常运行后生成 |
| `.aris/` | 本地状态与 dashboard 数据，通常运行后生成 |

---

## 3. 本次新增模块

### 成员 1：论文质量评价

负责：

- `skills/paper-quality-eval/SKILL.md`
- `tests/test_paper_quality_eval_contract.py`
- `tests/fixtures/mock_paper_quality_report.json`

输出：

- `paper/PAPER_QUALITY_REPORT.json`

是否需要 API：

- 写 schema 和测试不需要。
- 真实运行 reviewer 需要。

### 成员 2：投稿准备度

负责：

- `tools/submission_readiness.py`
- `skills/submission-assurance/SKILL.md`
- `tests/test_submission_readiness.py`
- `templates/SUBMISSION_READINESS_REPORT_TEMPLATE.md`

输出：

- `paper/SUBMISSION_READINESS_REPORT.json`
- `paper/SUBMISSION_READINESS_REPORT.md`

是否需要 API：不需要。

### 成员 3：统一状态中心

负责：

- `tools/state_exporter.py`
- `tools/experiment_state_exporter.py`
- `tests/test_state_exporter.py`

输出：

- `.aris/state.json`
- `.aris/dashboard_data.json`

是否需要 API：不需要。

### 成员 4：阶段产物图谱

负责：

- `tools/artifact_graph.py`
- `tests/test_artifact_graph.py`
- 可选：`docs/team/ARTIFACT_GRAPH_CN.md`

输出：

- `.aris/artifact_graph.json`

是否需要 API：不需要。

### 成员 5：报告渲染与静态仪表盘

负责：

- `tools/render_paper_quality_report.py`
- `tools/render_dashboard.py`
- `dashboard/index.html`
- `dashboard/app.js`
- `dashboard/style.css`
- `tests/test_paper_quality_report_renderer.py`
- `tests/test_coursework_dashboard.py`

输出：

- `paper/PAPER_QUALITY_REPORT.md`
- `dashboard/index.html`

是否需要 API：不需要。

---

## 4. 静态仪表盘是什么

静态仪表盘不是一个完整网站。

它的流程是：

```text
.aris/dashboard_data.json
-> tools/render_dashboard.py
-> dashboard/index.html
```

它不需要：

- 后端服务
- 数据库
- 前端框架
- 实时通信

打开 `dashboard/index.html` 就能展示。

---

## 5. 测试要求

每个成员至少提供：

- 一个 mock JSON
- 一个测试文件
- 一个示例输出

推荐命令：

```bash
python -m pytest tests/<your_test_file>.py
```

如果本地没安装 pytest：

```bash
python -m compileall tools tests
```

---

## 6. API 与费用

默认所有成员都用 mock JSON 开发，不调用 API。

只有以下情况可能需要 API：

- 成员 1 真实运行 `paper-quality-eval`
- 组长最终运行真实论文评价和审计

请不要把 API key 写进仓库。

---

## 7. 开发原则

- 只改自己负责的目录。
- 先看 `INTERFACES_CN.md`，再写代码。
- JSON 是模块之间唯一稳定接口。
- 渲染层不决定评分逻辑。
- 评分层不决定展示样式。
- 不提交私有讨论文档。

