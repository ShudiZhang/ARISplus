# ARIS 科研增强版接口文档

本文档定义各成员模块之间的 JSON 接口。所有成员都应优先遵守这里的字段，不要临时发明新字段。

---

## 1. `paper/PAPER_QUALITY_REPORT.json`

生产者：成员 1，`paper-quality-eval（论文质量评价）`

消费者：

- 成员 2：`submission-readiness（投稿准备度）`
- 成员 5：`render_paper_quality_report.py（论文质量报告渲染器）`
- 成员 3：`state_exporter.py（状态导出器）`

最小结构：

```json
{
  "schema_version": "1",
  "report_type": "paper-quality-eval",
  "rubric_source": "stanford_agentic_reviewer_style",
  "paper": {
    "title": "unknown",
    "directory": "paper",
    "main_tex": "paper/main.tex",
    "main_pdf": "paper/main.pdf"
  },
  "venue": "ICLR",
  "overall_score": 7.1,
  "overall_verdict": "almost",
  "overall_confidence": "medium",
  "summary": "One-paragraph summary.",
  "rubric_scores": {
    "originality": {
      "score": 7.0,
      "confidence": "medium",
      "rationale": "Reviewer rationale.",
      "evidence": [
        {"file": "paper/main.tex", "location": "Introduction", "note": "Why it matters."}
      ],
      "minimum_fix": "Smallest concrete improvement."
    }
  },
  "blocking_issues": [],
  "minimum_fixes": [],
  "inputs": {
    "paper_files": [],
    "audit_artifacts": [],
    "missing_optional": []
  },
  "trace_path": ".aris/traces/paper-quality-eval/20260504_run01/",
  "thread_id": "review-thread-id",
  "reviewer_model": "gpt-5.4",
  "reviewer_reasoning": "xhigh",
  "generated_at": "2026-05-04T12:00:00Z"
}
```

必须包含的 7 个 `rubric_scores（评价量表分数）` key：

- `originality`
- `importance`
- `claims_supported`
- `experiment_soundness`
- `writing_clarity`
- `community_value`
- `prior_work_context`

缺失策略：

- 分数缺失时写 `0`。
- 文本缺失时写 `"not available"`。
- 列表缺失时写 `[]`。

---

## 2. `paper/SUBMISSION_READINESS_REPORT.json`

生产者：成员 2，`submission-readiness（投稿准备度）`

消费者：

- 成员 3：`state_exporter.py`
- 成员 5：`dashboard（仪表盘）`

建议结构：

```json
{
  "schema_version": "1",
  "report_type": "submission-readiness",
  "status": "almost",
  "summary": "The paper is close to submission but has one non-blocking audit warning.",
  "quality": {
    "overall_score": 7.1,
    "overall_verdict": "almost",
    "source": "paper/PAPER_QUALITY_REPORT.json"
  },
  "audits": [
    {"name": "proof-checker", "verdict": "NOT_APPLICABLE", "blocking": false},
    {"name": "paper-claim-audit", "verdict": "WARN", "blocking": false},
    {"name": "citation-audit", "verdict": "PASS", "blocking": false}
  ],
  "blocking_items": [],
  "recommended_actions": [],
  "generated_at": "2026-05-04T12:00:00Z"
}
```

允许状态：

- `ready`：可投稿
- `almost`：接近可投稿
- `blocked`：存在阻塞
- `draft_only`：仅适合草稿

---

## 3. `.aris/state.json`

生产者：成员 3，`state_exporter.py（状态导出器）`

消费者：

- 成员 5：`dashboard（仪表盘）`
- 组长：最终整合

建议结构：

```json
{
  "schema_version": "1",
  "project": {
    "name": "ARIS Coursework Project",
    "summary": "Research workflow enhanced with structured paper evaluation."
  },
  "workflow": {
    "phases": [
      {"name": "idea-discovery", "label": "Idea Discovery", "status": "completed", "summary": "Idea report exists."},
      {"name": "paper-quality-eval", "label": "Paper Quality Eval", "status": "completed", "summary": "Quality report exists."}
    ]
  },
  "paper_quality": {
    "overall_score": 7.1,
    "overall_verdict": "almost",
    "source": "paper/PAPER_QUALITY_REPORT.json"
  },
  "submission": {
    "status": "almost",
    "source": "paper/SUBMISSION_READINESS_REPORT.json"
  },
  "experiments": {
    "counts": {"queued": 0, "running": 0, "completed": 0, "failed": 0, "unknown": 0}
  },
  "generated_at": "2026-05-04T12:00:00Z"
}
```

---

## 4. `.aris/artifact_graph.json`

生产者：成员 4，`artifact_graph.py（阶段产物图谱）`

消费者：

- 成员 3：`state_exporter.py`
- 成员 5：`dashboard（仪表盘）`

建议结构：

```json
{
  "schema_version": "1",
  "nodes": [
    {"id": "artifact:paper/PAPER_QUALITY_REPORT.json", "type": "artifact", "label": "PAPER_QUALITY_REPORT.json"}
  ],
  "edges": [
    {"from": "artifact:paper/main.tex", "to": "artifact:paper/PAPER_QUALITY_REPORT.json", "type": "consumed_by"}
  ],
  "generated_at": "2026-05-04T12:00:00Z"
}
```

---

## 5. `.aris/dashboard_data.json`

生产者：成员 3，`state_exporter.py`

消费者：成员 5，`render_dashboard.py（仪表盘渲染器）`

该文件是 dashboard 的唯一数据入口。成员 5 不直接读取 ARIS 原始产物。

建议结构：

```json
{
  "project": {"name": "ARIS Coursework Project", "summary": "Static dashboard data."},
  "workflow": {"phases": []},
  "paper_quality": {},
  "submission": {},
  "artifacts": [],
  "experiments": {"counts": {"queued": 0, "running": 0, "completed": 0, "failed": 0, "unknown": 0}}
}
```

---

## 6. 兼容原则

- 消费者必须容忍缺字段，显示 `unknown（未知）` 或 `not available（不可用）`。
- 生产者必须尽量输出完整字段。
- 不要让展示层决定评分逻辑。
- 不要让评分层决定页面样式。
- 不要把 API key 写进任何 JSON 或 Markdown。

