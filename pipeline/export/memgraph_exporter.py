import csv
from pathlib import Path
from typing import List, Dict
from config import PipelineConfig


class MemgraphExporter:
    def __init__(self, cfg: PipelineConfig):
        self.nodes_csv = cfg.output_dir / "nodes_v1.csv"
        self.edges_csv = cfg.output_dir / "edges_v1.csv"

    def write(self, nodes: List[Dict], edges: List[Dict]):
        # write minimal CSVs (placeholder schema: id,type,properties_json / edge fields)
        with self.nodes_csv.open("w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=["id", "type", "properties_json"])
            w.writeheader()
            for n in nodes:
                w.writerow({"id": n.get("id"), "type": n.get("type"), "properties_json": n.get("properties_json", {})})
        with self.edges_csv.open("w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=["src_id", "src_type", "relation", "dst_id", "dst_type", "properties_json"])
            w.writeheader()
            for e in edges:
                w.writerow(e)


