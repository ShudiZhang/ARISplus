from __future__ import annotations

import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
MAIN_SKILL = REPO_ROOT / "skills" / "paper-quality-eval" / "SKILL.md"
MOCK_REPORT = REPO_ROOT / "tests" / "fixtures" / "mock_paper_quality_report.json"

RUBRIC_KEYS = {
    "originality",
    "importance",
    "claims_supported",
    "experiment_soundness",
    "writing_clarity",
    "community_value",
    "prior_work_context",
}


def test_paper_quality_eval_skill_defines_producer_boundary() -> None:
    main = MAIN_SKILL.read_text(encoding="utf-8")

    assert "PAPER_QUALITY_REPORT.json" in main
    assert "PAPER_QUALITY_REPORT.md" in main
    assert "Do not generate `PAPER_QUALITY_REPORT.md`" in main
    assert "No multi-reviewer voting" in main
    assert "stanford_agentic_reviewer_style" in main
    assert "mcp__codex__codex" in main
    assert "spawn_agent:" not in main
    for key in RUBRIC_KEYS:
        assert f"`{key}`" in main or key in main


def test_mock_paper_quality_report_matches_contract() -> None:
    data = json.loads(MOCK_REPORT.read_text(encoding="utf-8"))

    assert data["schema_version"] == "1"
    assert data["report_type"] == "paper-quality-eval"
    assert data["rubric_source"] == "stanford_agentic_reviewer_style"
    assert isinstance(data["overall_score"], (int, float))
    assert data["overall_verdict"] in {"ready", "almost", "not_ready", "blocked"}
    assert set(data["rubric_scores"]) == RUBRIC_KEYS

    for key, value in data["rubric_scores"].items():
        assert 1 <= float(value["score"]) <= 10, key
        assert value["confidence"] in {"low", "medium", "high"}, key
        assert value["rationale"], key
        assert isinstance(value["evidence"], list), key
        assert value["minimum_fix"], key
        for evidence in value["evidence"]:
            assert {"file", "location", "note"} <= set(evidence), key

    assert isinstance(data["blocking_issues"], list)
    assert isinstance(data["minimum_fixes"], list)
    assert data["reviewer_model"]
    assert data["reviewer_reasoning"] == "xhigh"
