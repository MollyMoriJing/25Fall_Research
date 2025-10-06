import re


def normalize_text(text: str) -> str:
    # placeholder normalization: collapse spaces and newlines
    if not text:
        return ""
    t = text.replace("\u00A0", " ")
    t = re.sub(r"[ \t]+", " ", t)
    t = re.sub(r"\n{3,}", "\n\n", t)
    return t.strip()


