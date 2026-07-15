#!/usr/bin/env python3
"""Render a read-only ingestion plan from RAG corpus manifests."""
from __future__ import annotations
import glob, json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MANIFEST_DIR = ROOT / "rag" / "corpora"


def resolve(patterns, excludes):
    excluded = set()
    for pat in excludes:
        for item in glob.glob(str(ROOT / pat), recursive=True):
            p = Path(item)
            if p.is_file():
                excluded.add(p.resolve())
    out = set()
    for pat in patterns:
        if "<" in pat or ">" in pat:
            continue
        for item in glob.glob(str(ROOT / pat), recursive=True):
            p = Path(item)
            if p.is_file() and p.resolve() not in excluded:
                out.add(p.resolve())
    return sorted(out)


def main():
    print("# RAG Ingestion Plan (read-only)\n")
    print("This is a plan only. It does not build an index or call an embedding model.\n")
    print("| Corpus | Status | Indexable | Sensitivity | Chunk profile | Files |")
    print("|---|---|---:|---|---|---:|")
    for path in sorted(MANIFEST_DIR.glob("*.manifest.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        files = resolve(data["paths"], data["exclude"])
        print(f"| `{data['id']}` | {data['status']} | {str(data['indexable']).lower()} | {data['sensitivity']} | `{data['default_chunk_profile']}` | {len(files)} |")
    print("\n## Next runtime steps\n")
    print("1. Review this plan and corpus sensitivity.")
    print("2. Choose embedding/reranker aliases via the LLM gateway plan.")
    print("3. Build a disposable runtime index outside Git.")
    print("4. Run `eval/rag` fixtures before exposing retrieval to agents.")

if __name__ == "__main__":
    main()
