import os
from pathlib import Path


def create_mock_artifacts(workspace_root: str):
    """
    Creates empty mock files to simulate a real research process for testing artifact_graph.py
    """
    root = Path(workspace_root)
    print(f"Creating mock artifacts in: {root}")

    # Define the mock directories and files
    mock_structure = {
        "papers": ["main.tex", "supplementary.md"],
        "figures": ["ablation_study.png", "architecture.svg"],
        "experiments": ["run_001_metrics.json", "hyperparams.json"],
        ".aris": ["quality_report.md", "rebuttal_trace.json"],
    }

    # Create directories and touch files
    for folder, files in mock_structure.items():
        dir_path = root / folder
        dir_path.mkdir(parents=True, exist_ok=True)
        print(f"📁 Created directory: {dir_path.relative_to(root)}")

        for file in files:
            file_path = dir_path / file
            file_path.touch(exist_ok=True)
            print(f"  📄 Mocked file: {file_path.relative_to(root)}")

    print(
        "\nMock setup complete. You can now run `python tools/artifact_graph.py` to generate the graph."
    )


if __name__ == "__main__":
    # If run directly as a script, create mock files in the project root
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    create_mock_artifacts(project_root)
