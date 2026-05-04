---
name: paper-quality-eval
description: "Structured paper-quality evaluation using one external reviewer and a Stanford Agentic Reviewer-style rubric. Use after paper-writing, before submission-assurance, or when the user asks for paper quality scoring, structured review, venue readiness, or Stanford-style paper evaluation."
argument-hint: [paper-directory]
allowed-tools: Bash(*), Read, Grep, Glob, Write, Edit, Agent, mcp__codex__codex
---

# Paper Quality Eval: Structured Reviewer Rubric

Evaluate the paper at: **$ARGUMENTS**

This skill is the **evaluation producer**. It creates the machine-readable
`paper/PAPER_QUALITY_REPORT.json`. It does **not** own Markdown rendering or
dashboard presentation; those are handled by the report renderer and dashboard
tools.

## Core Design

Keep ARIS's original two-model executor-reviewer architecture:

- Executor: the host agent collects file paths, audit artifacts, and context.
- Reviewer: one external cross-family reviewer evaluates the paper.
- No multi-reviewer voting. Do not spawn a panel of reviewers.

The enhancement is **structured review**, not more reviewers.

## Constants

- REVIEWER_MODEL = `gpt-5.4`
- REVIEWER_REASONING = `xhigh`
- OUTPUT_JSON = `paper/PAPER_QUALITY_REPORT.json`
- TRACE_DIR = `.aris/traces/paper-quality-eval/<date>_run<NN>/`
- RUBRIC_SOURCE = `stanford_agentic_reviewer_style`

## Inputs

Collect paths only. Prefer passing file paths to the reviewer where possible.

Required:

- `paper/main.tex`
- `paper/main.pdf` if it exists
- `paper/sections/*.tex` if present

Optional supporting artifacts:

- `paper/PROOF_AUDIT.json`
- `paper/PAPER_CLAIM_AUDIT.json`
- `paper/CITATION_AUDIT.json`
- `review-stage/AUTO_REVIEW.md`
- `NARRATIVE_REPORT.md`
- `PAPER_PLAN.md`

Do not block if optional artifacts are missing. Record missing optional inputs in
`inputs.missing_optional`.

## Rubric

Use exactly these seven dimensions:

| Key | Dimension |
| --- | --- |
| `originality` | Originality |
| `importance` | Importance of research question |
| `claims_supported` | Whether claims are well supported |
| `experiment_soundness` | Soundness of experiments |
| `writing_clarity` | Clarity of writing |
| `community_value` | Value to the research community |
| `prior_work_context` | Contextualized relative to prior work |

Each dimension must include:

- `score`: number from 1 to 10
- `confidence`: `low | medium | high`
- `rationale`: concise reviewer reasoning
- `evidence`: list of evidence objects
- `minimum_fix`: the smallest concrete fix that would improve this dimension

Each evidence object must include:

- `file`: path string
- `location`: section, line, table, figure, or page if known
- `note`: why this evidence matters

## Workflow

### Step 1: Gather Input Paths

Find the paper directory. If `$ARGUMENTS` is empty, default to `paper/`.

Collect the input paths above. Do not summarize the whole paper yourself; the
external reviewer must judge from paper source/PDF and audit artifacts.

### Step 2: Fresh Structured Review

Use a fresh reviewer thread every run:

```text
mcp__codex__codex:
  model: gpt-5.4
  config: {"model_reasoning_effort": "xhigh"}
  prompt: |
    You are a senior ML paper reviewer performing a structured paper-quality
    evaluation. Use one reviewer perspective only; do not simulate a committee
    vote.

    Paper files:
    [list absolute or workspace-relative paths]

    Audit artifacts:
    [list available audit JSON/MD paths]

    Evaluate the current paper using exactly these seven dimensions:
    1. originality
    2. importance
    3. claims_supported
    4. experiment_soundness
    5. writing_clarity
    6. community_value
    7. prior_work_context

    For every dimension, output:
    - score: 1-10
    - confidence: low | medium | high
    - rationale
    - evidence: file/location/note list
    - minimum_fix

    Also output:
    - overall_score: weighted or holistic 1-10 score
    - overall_verdict: ready | almost | not_ready | blocked
    - summary
    - blocking_issues: severity, dimension, issue, evidence, minimum_fix
    - minimum_fixes: highest-leverage fixes across all dimensions

    Important:
    - Be strict and venue-aware.
    - Do not reward unsupported claims.
    - If audit artifacts show FAIL/BLOCKED/ERROR, reflect that in
      claims_supported, experiment_soundness, or prior_work_context.
    - Return valid JSON only. Do not wrap it in markdown.
```

### Step 3: Save Trace

Save the raw reviewer prompt and response under:

```text
.aris/traces/paper-quality-eval/<date>_run<NN>/
```

Follow `shared-references/review-tracing.md`.

### Step 4: Normalize JSON

Write `paper/PAPER_QUALITY_REPORT.json` with this top-level shape:

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
  "venue": "unknown",
  "overall_score": 0,
  "overall_verdict": "not_ready",
  "overall_confidence": "medium",
  "summary": "",
  "rubric_scores": {
    "originality": {
      "score": 0,
      "confidence": "medium",
      "rationale": "",
      "evidence": [],
      "minimum_fix": ""
    }
  },
  "blocking_issues": [],
  "minimum_fixes": [],
  "inputs": {
    "paper_files": [],
    "audit_artifacts": [],
    "missing_optional": []
  },
  "trace_path": ".aris/traces/paper-quality-eval/<date>_run<NN>/",
  "thread_id": "",
  "reviewer_model": "gpt-5.4",
  "reviewer_reasoning": "xhigh",
  "generated_at": "<UTC ISO-8601>"
}
```

Rules:

- Keep all seven rubric keys even if the reviewer omits one.
- Use `0` for unavailable scores, not `null`.
- Use `"not available"` for unavailable text fields.
- Do not generate `PAPER_QUALITY_REPORT.md`; rendering is owned by
  `tools/render_paper_quality_report.py`.

### Step 5: Handoff

After writing the JSON, print:

```text
Paper quality JSON written: paper/PAPER_QUALITY_REPORT.json
To render Markdown, run:
python tools/render_paper_quality_report.py --input paper/PAPER_QUALITY_REPORT.json --output paper/PAPER_QUALITY_REPORT.md
```

## Key Rules

- Do not use multi-reviewer voting.
- Do not let the executor assign the scores.
- Do not hide failed audits.
- Do not overwrite the schema shape.
- Keep JSON machine-readable; Markdown rendering is a separate module.

