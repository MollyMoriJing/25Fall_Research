from pathlib import Path
from typing import List
from config import PipelineConfig


def discover_inputs(cfg: PipelineConfig) -> List[Path]:
    # walk input dir and return supported files
    return [p for p in sorted(cfg.input_dir.iterdir()) if p.suffix.lower() in cfg.doc_exts]


def read_text_or_binary(path: Path):
    # read raw bytes or text depending on suffix
    if path.suffix.lower() == ".txt":
        return path.read_text(errors="ignore")
    return path.read_bytes()


