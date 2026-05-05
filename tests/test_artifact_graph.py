import os
import sys
import json
import tempfile
import unittest
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from tools.artifact_graph import ArtifactGraphBuilder


class TestArtifactGraph(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.test_dir.name)

        # Create mock structure
        (self.root / "papers").mkdir()
        (self.root / "papers" / "main.tex").write_text("% mock paper")

        (self.root / "figures").mkdir()
        (self.root / "figures" / "result.png").write_text("mock image")

        (self.root / ".aris").mkdir()
        (self.root / ".aris" / "quality_report.md").write_text("# Review")

        (self.root / "templates").mkdir()
        self.template_path = self.root / "templates" / "RESEARCH_WIKI_INDEX_TEMPLATE.md"
        self.template_path.write_text("# Research Wiki\n\n{{ARTIFACT_LIST}}")

    def tearDown(self):
        self.test_dir.cleanup()

    def test_graph_generation(self):
        builder = ArtifactGraphBuilder(str(self.root))
        builder.scan_artifacts()
        graph_path = builder.export_graph()

        self.assertTrue(graph_path.exists())

        with open(graph_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.assertIn("nodes", data)
        self.assertIn("edges", data)

        # Check node parsing
        node_ids = [n["id"] for n in data["nodes"]]
        self.assertIn("artifact:papers/main.tex", node_ids)
        self.assertIn("artifact:figures/result.png", node_ids)

        # Check edges
        self.assertTrue(len(data["edges"]) > 0)

    def test_empty_directories_fallback(self):
        # Test with an empty new directory
        empty_dir = tempfile.TemporaryDirectory()
        builder = ArtifactGraphBuilder(empty_dir.name)
        builder.scan_artifacts()
        graph_path = builder.export_graph()

        with open(graph_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.assertEqual(len(data["nodes"]), 0)
        self.assertEqual(len(data["edges"]), 0)
        empty_dir.cleanup()

    def test_wiki_generation(self):
        builder = ArtifactGraphBuilder(str(self.root))
        builder.scan_artifacts()
        wiki_path = builder.generate_research_wiki(str(self.template_path))

        self.assertTrue(wiki_path.exists())
        with open(wiki_path, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn("papers/main.tex", content)


if __name__ == "__main__":
    unittest.main()
