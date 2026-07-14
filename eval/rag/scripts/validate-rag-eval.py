#!/usr/bin/env python3
"""Validate RAG evaluation fixture schemas."""
from __future__ import annotations
import json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
EVAL = ROOT / "eval" / "rag"
CHECKS = {
    "golden-questions.json": {"id", "role", "question", "expected_citations_any"},
    "expected-citations.json": {"id", "claim", "must_cite_any"},
    "abstention-tests.json": {"id", "role", "question", "expected_behavior", "forbidden_citations"},
    "role-boundary-tests.json": {"id", "role", "question", "expected_behavior"},
}

def main() -> int:
    errors = []
    for name, required in CHECKS.items():
        path = EVAL / name
        if not path.exists():
            errors.append(f"missing {path}")
            continue
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:
            errors.append(f"{path}: invalid JSON: {exc}")
            continue
        if not isinstance(data, list) or not data:
            errors.append(f"{path}: expected non-empty list")
            continue
        seen = set()
        for i, item in enumerate(data):
            if not isinstance(item, dict):
                errors.append(f"{path}[{i}]: expected object")
                continue
            missing = required - set(item)
            if missing:
                errors.append(f"{path}[{i}]: missing {sorted(missing)}")
            iid = item.get("id")
            if iid in seen:
                errors.append(f"{path}: duplicate id {iid}")
            seen.add(iid)
    if errors:
        print("FAIL: RAG eval validation")
        for err in errors:
            print(f"- {err}")
        return 1
    print("PASS: RAG eval validation")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
