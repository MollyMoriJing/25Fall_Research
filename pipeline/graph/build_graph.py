from dataclasses import dataclass, field
from typing import List, Dict, Tuple
from pathlib import Path
from config import PipelineConfig


@dataclass
class GraphAssembler:
    cfg: PipelineConfig
    nodes: List[Dict] = field(default_factory=list)
    edges: List[Dict] = field(default_factory=list)

    def add_document(self, path: Path, text: str, ents: Dict, items: List[Dict]) -> Tuple[List[Dict], List[Dict]]:
        # placeholder graph assembly, append minimal Document node
        doc_id = f"doc_{path.stem}"
        self.nodes.append({"id": doc_id, "type": "Document", "properties_json": {"id": doc_id}})
        return self.nodes, self.edges


