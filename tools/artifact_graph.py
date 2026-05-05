import os
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Any


class ArtifactGraphBuilder:
    def __init__(self, workspace_root: str):
        self.workspace_root = Path(workspace_root)
        self.aris_dir = self.workspace_root / ".aris"
        self.wiki_dir = self.aris_dir / "research_wiki"
        self.nodes = {}
        self.edges = []

    def ensure_dirs(self):
        self.aris_dir.mkdir(parents=True, exist_ok=True)
        self.wiki_dir.mkdir(parents=True, exist_ok=True)

    def scan_artifacts(self):
        # Scan for different types of artifacts
        self.scan_directory("papers", "paper", [".tex", ".pdf", ".md"])
        self.scan_directory("experiments", "experiment", [".json", ".csv", ".log"])
        self.scan_directory("figures", "figure", [".png", ".jpg", ".svg", ".pdf"])
        self.scan_directory(".aris", "report", [".json", ".md"])

        # Build logical relations (Edges)
        self._build_edges()

    def scan_directory(self, subdir: str, artifact_type: str, extensions: List[str]):
        target_dir = self.workspace_root / subdir
        if not target_dir.exists():
            return

        for ext in extensions:
            for file_path in target_dir.rglob(f"*{ext}"):
                # filter out research wiki itself to avoid loop
                if "research_wiki" in file_path.parts:
                    continue

                rel_path = file_path.relative_to(self.workspace_root)
                raw_path = str(rel_path).replace("\\", "/")
                node_id = f"artifact:{raw_path}"
                self.nodes[node_id] = {
                    "id": node_id,
                    "type": "artifact",
                    "subtype": artifact_type,
                    "label": file_path.name,
                    "path": raw_path,
                }

    def _build_edges(self):
        # Heuristics for edges
        # Papers depend on figures and experiments
        paper_nodes = [n for n in self.nodes.values() if n.get("subtype") == "paper"]
        figure_nodes = [n for n in self.nodes.values() if n.get("subtype") == "figure"]
        exp_nodes = [n for n in self.nodes.values() if n.get("subtype") == "experiment"]
        report_nodes = [n for n in self.nodes.values() if n.get("subtype") == "report"]

        for paper in paper_nodes:
            # Paper includes figures
            for fig in figure_nodes:
                self.edges.append(
                    {
                        "from": fig["id"],
                        "to": paper["id"],
                        "type": "consumed_by",
                    }
                )
            # Paper relies on experiments
            for exp in exp_nodes:
                self.edges.append(
                    {"from": exp["id"], "to": paper["id"], "type": "consumed_by"}
                )

        # Reports review papers or experiments
        for report in report_nodes:
            for paper in paper_nodes:
                if (
                    "review" in report["label"].lower()
                    or "report" in report["label"].lower()
                ):
                    self.edges.append(
                        {
                            "from": paper["id"],
                            "to": report["id"],
                            "type": "consumed_by",
                        }
                    )

    def export_graph(self, filename: str = "artifact_graph.json"):
        self.ensure_dirs()
        out_path = self.aris_dir / filename

        graph_data = {
            "schema_version": "1",
            "nodes": list(self.nodes.values()),
            "edges": self.edges,
            "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        }

        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(graph_data, f, indent=2, ensure_ascii=False)
        return out_path

    def generate_research_wiki(self, template_path: str):
        self.ensure_dirs()
        template_file = Path(template_path)

        if not template_file.exists():
            print(f"Template {template_path} not found. Skipping Wiki generation.")
            return

        with open(template_file, "r", encoding="utf-8") as f:
            template = f.read()

        # Group nodes by subtype for markdown generation
        grouped_nodes = {}
        for node in self.nodes.values():
            grouped_nodes.setdefault(node.get("subtype", "unknown"), []).append(node)

        content = ""
        for n_type, nodes in grouped_nodes.items():
            content += f"## {n_type.capitalize()}s\n"
            for node in nodes:
                content += f"- [{node['label']}]({node['path']})\n"
            content += "\n"

        wiki_content = template.replace("{{ARTIFACT_LIST}}", content)

        wiki_index = self.wiki_dir / "index.md"
        with open(wiki_index, "w", encoding="utf-8") as f:
            f.write(wiki_content)

        return wiki_index


if __name__ == "__main__":
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    builder = ArtifactGraphBuilder(root)
    builder.scan_artifacts()
    builder.export_graph()
    builder.generate_research_wiki(
        os.path.join(root, "templates", "RESEARCH_WIKI_INDEX_TEMPLATE.md")
    )
    print("Artifact graph and Research Wiki generated successfully.")
