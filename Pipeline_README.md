# Medical GraphRAG Pipeline v1

A modular, testable pipeline for converting documents into a patient-centric graph.

## Structure

```
pipeline_v1/
  app.py                 # Entry point (CLI orchestrator)
  config.py              # Configuration (paths, flags)
  schemas/
    ontology.py          # Ontology definition (nodes/edges)
  ingest/
    reader.py            # File discovery and raw text loading
  ocr/
    pdf_ocr.py           # PDF/image OCR utilities
  normalize/
    text_normalizer.py   # Text cleanup and normalization
  extract/
    entities.py          # Entity/metadata extraction (patient, provider, accounts)
    line_items.py        # Line item parsing (codes, qty, amounts)
  graph/
    build_graph.py       # Graph construction from extracted features
  export/
    jsonl_exporter.py    # Write per-document extraction JSONL
    memgraph_exporter.py # Write nodes/edges CSV for Memgraph
  utils/
    logging.py           # Logger setup
  tests/
    test_pipeline_smoke.py # Basic smoke tests
```

## Run

```
python pipeline_v1/app.py --input ./input_docs --output ./out_graph
```
