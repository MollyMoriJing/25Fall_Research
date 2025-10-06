import json
from pathlib import Path
from config import PipelineConfig


class JsonlExporter:
    def __init__(self, cfg: PipelineConfig):
        self.path = cfg.output_dir / "documents_extracted_v1.jsonl"
        # reset file
        self.path.write_text("")

    def append(self, path: Path, ents: dict, items: list):
        # append a line per document
        rec = {"doc_id": f"doc_{path.stem}", "file": path.name, "extracted": {"entities": ents, "line_items": items}}
        with self.path.open("a") as f:
            f.write(json.dumps(rec) + "\n")


