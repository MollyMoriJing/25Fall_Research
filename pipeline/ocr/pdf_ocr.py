from pathlib import Path


def ocr_if_needed(path: Path, payload) -> str:
    # if text is provided, return; else run OCR for pdf/images (placeholder)
    if isinstance(payload, str):
        return payload
    # TODO: implement pdfplumber/tesseract as needed
    return ""


