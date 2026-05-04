from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import shutil


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "tools" / "render_dashboard.py"
ASSET_DIR = REPO_ROOT / "dashboard"
MOCK_DASHBOARD = REPO_ROOT / "tests" / "fixtures" / "mock_dashboard_data.json"
TMP_ROOT = REPO_ROOT / ".tmp_test_outputs" / "dashboard"


def load_module():
    spec = importlib.util.spec_from_file_location("render_dashboard", SCRIPT)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_static_dashboard_assets_exist() -> None:
    assert (ASSET_DIR / "index.html").exists()
    assert (ASSET_DIR / "app.js").exists()
    assert (ASSET_DIR / "style.css").exists()


def test_render_dashboard_embeds_data_without_backend() -> None:
    module = load_module()
    data = json.loads(MOCK_DASHBOARD.read_text(encoding="utf-8"))
    html = module.render_html(data, ASSET_DIR)

    assert "ARIS Coursework Demo" in html
    assert "dashboard-data" in html
    assert "Workflow Status" in html
    assert "Paper Quality" in html
    assert "fetch(" not in html
    assert "Static dashboard data" in html


def test_render_dashboard_file() -> None:
    module = load_module()
    if TMP_ROOT.exists():
        shutil.rmtree(TMP_ROOT)
    output = TMP_ROOT / "index.html"
    module.render_file(MOCK_DASHBOARD, output, ASSET_DIR)

    html = output.read_text(encoding="utf-8")
    assert "ARIS Coursework Demo" in html
    assert "app.js" not in html
    assert "style.css" not in html
    shutil.rmtree(TMP_ROOT)
