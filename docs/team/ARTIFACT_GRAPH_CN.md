# Artifact Graph（产物图谱工具）

## 作用与定位
核心目的在于管理科研过程里产生的各类文件（如论文、实验结果、报告、图表、评审追踪记录等）。
提供产物追踪拓扑关系提取功能，可导出为 JSON 和 Markdown 的 Research Wiki。

## 适用成员
成员 4 直接负责这个模块。成员 3 和成员 5 通过消费 `.aris/artifact_graph.json` 来进行后续的流水线任务或质量审核。

## 主要功能
1. **自动扫描**：能够根据配置自动检索工作区别下的产物。
2. **关系推断**：构建节点间的网络（如：实验数据驱动了某篇论文写作，分析结果图表被插入核心文档，等）。
3. **维基导出**：渲染清晰的研究索引页 Markdown（`.aris/research_wiki/index.md`），方便答辩展示。

## 运行方式
```bash
python tools/artifact_graph.py
```
这将在 `.aris` 目录下自动生成 `artifact_graph.json`。

## 文件结构说明
- `tools/artifact_graph.py`: 脚本文本，实现扫描、解析及导出。
- `tests/test_artifact_graph.py`: 在缺少文件夹时保证逻辑鲁棒的单测。
- `templates/RESEARCH_WIKI_INDEX_TEMPLATE.md`: Wiki 的占位符模板。
- `tools/mock_artifact_graph.py`:生成 mock 产物文件的 Python 脚本
