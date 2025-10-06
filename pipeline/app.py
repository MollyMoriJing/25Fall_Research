#!/usr/bin/env python3
"""
Pipeline v1 entry point.
Coordinates: ingest -> OCR -> normalize -> extract -> graph -> export.
"""
import argparse
from pathlib import Path

from config import PipelineConfig
from utils.logging import get_logger
from ingest.reader import discover_inputs, read_text_or_binary
from ocr.pdf_ocr import ocr_if_needed
from normalize.text_normalizer import normalize_text
from extract.entities import extract_entities
from extract.line_items import extract_line_items
from graph.build_graph import GraphAssembler
from export.jsonl_exporter import JsonlExporter
from export.memgraph_exporter import MemgraphExporter


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--input", type=str, default="./input_docs")
    p.add_argument("--output", type=str, default="./out_graph")
    return p.parse_args()


def main():
    args = parse_args()
    cfg = PipelineConfig(input_dir=Path(args.input), output_dir=Path(args.output))
    cfg.output_dir.mkdir(parents=True, exist_ok=True)
    log = get_logger()

    inputs = discover_inputs(cfg)
    graph = GraphAssembler(cfg)
    jsonl = JsonlExporter(cfg)
    csv = MemgraphExporter(cfg)

    for inp in inputs:
        # read or OCR
        payload = read_text_or_binary(inp)
        text = ocr_if_needed(inp, payload)

        # normalize
        text = normalize_text(text)

        # extract
        ents = extract_entities(text)
        items = extract_line_items(text)

        # assemble graph
        nodes, edges = graph.add_document(inp, text, ents, items)

        # export JSONL record
        jsonl.append(inp, ents, items)

        log.info(f"ok {inp.name} nodes:{len(nodes)} edges:{len(edges)}")

    # finalize CSVs
    csv.write(graph.nodes, graph.edges)
    log.info("done")


if __name__ == "__main__":
    main()


