from dataclasses import dataclass
from pathlib import Path


@dataclass
class PipelineConfig:
    input_dir: Path
    output_dir: Path
    doc_exts: tuple = (".txt", ".pdf", ".png", ".jpg", ".jpeg")

    # toggles (placeholders)
    use_pdf_tables: bool = True
    prefer_address_block: bool = True


