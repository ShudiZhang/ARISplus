# GitHub 协作流程

本文档给组长和组员使用，说明如何基于 GitHub 协作开发课程版 ARIS。

---

## 1. 推荐仓库策略

组长 fork 原始 ARIS 项目，作为课程小组主仓库。

建议：

- `main`：稳定整合分支
- `feature/paper-quality-eval`：成员 1
- `feature/submission-readiness`：成员 2
- `feature/state-exporter`：成员 3
- `feature/artifact-graph`：成员 4
- `feature/static-dashboard`：成员 5

组员不要直接 push 到 `main`。

---

## 2. 组长应该公开给组员的文件

建议公开：

- 原项目所有原生文件
- `docs/team/DEVELOPMENT_GUIDE_CN.md`
- `docs/team/INTERFACES_CN.md`
- `docs/team/GITHUB_COLLABORATION_CN.md`
- `skills/paper-quality-eval/`
- `tools/render_paper_quality_report.py`
- `tools/render_dashboard.py`
- `dashboard/`
- `tests/fixtures/mock_paper_quality_report.json`
- `tests/fixtures/mock_dashboard_data.json`
- 对应测试文件

不建议公开：

- `AGENTS.md`
- `.private/`
- `docs/coursework/`
- 任何包含组长思路、私下讨论、历史决策摇摆的文档

---

## 3. Issue 模板

每个成员一个 Issue，建议格式：

```markdown
## 负责模块

## 允许修改的文件/目录

## 输入文件

## 输出文件

## 必须通过的测试

## 是否允许调用 API

## 注意事项
```

---

## 4. Pull Request 要求

每个 PR 必须说明：

- 做了什么
- 修改了哪些文件
- 输入是什么
- 输出是什么
- 如何测试
- 是否调用了大模型 API
- 是否新增依赖

PR 不应包含：

- API key
- 大型实验数据
- 私人讨论记录
- `docs/coursework/`
- `.private/`

---

## 5. 合并顺序

推荐顺序：

1. `paper-quality-eval（论文质量评价）`
2. `static-dashboard（静态仪表盘）`
3. `submission-readiness（投稿准备度）`
4. `artifact-graph（阶段产物图谱）`
5. `state-exporter（统一状态导出）`

原因：

- 成员 5 可以先用 mock JSON 并行开发。
- 成员 3 最后整合所有真实输出为 `.aris/dashboard_data.json`。

---

## 6. API 使用规则

默认不分发公用 API key。

不需要 API 的模块：

- 投稿准备度聚合
- 状态导出
- 产物图谱
- 静态仪表盘
- Markdown 渲染

可能需要 API 的模块：

- `paper-quality-eval（论文质量评价）` 真实运行 reviewer 时
- 原项目已有的 `proof-checker（证明检查）`
- 原项目已有的 `paper-claim-audit（论文论点审计）`
- 原项目已有的 `citation-audit（引用审计）`

建议做法：

- 组员开发时使用 mock JSON。
- 组长最终集成时统一调用真实 API。
- 如果必须共享 API，使用单独课程 key，并设置额度上限。
- 永远不要提交 `.env` 或 API key。

---

## 7. 组长审核清单

合并前检查：

- 是否只改了自己负责的目录
- JSON 字段是否符合 `INTERFACES_CN.md`
- 是否能用 mock 数据测试
- 是否引入了 Codex CLI 原生适配
- 是否误提交私有文档
- 是否误提交 API key
- 是否有基本测试或示例输出

