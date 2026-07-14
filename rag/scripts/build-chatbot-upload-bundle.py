#!/usr/bin/env python3
"""Print a chatbot project upload file list for a role.

Default is read-only: prints paths, does not copy files.
"""
from __future__ import annotations
import argparse, glob, json
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
                out.add(p.relative_to(ROOT))
    return sorted(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--role", required=True, help="portable role id, e.g. business-analyst")
    ap.add_argument("--include-adapters", action="store_true", help="include adapter docs as upload guidance")
    args = ap.parse_args()
    files = set()
    for path in sorted(MANIFEST_DIR.glob("*.manifest.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        if data["status"] != "active" or not data["indexable"]:
            continue
        if args.role not in data.get("allowed_roles", []):
            continue
        if data["id"] == "eksad-portable-governance" and not args.include_adapters:
            # Keep chatbot bundles smaller by default: include portable, exclude mcp/rag heavy docs if desired by platform limits.
            pass
        for p in resolve(data["paths"], data["exclude"]):
            if not args.include_adapters and (str(p).startswith("mcp/") or str(p).startswith("rag/")):
                continue
            files.add(p)
    for p in sorted(files):
        print(p)

if __name__ == "__main__":
    main()
