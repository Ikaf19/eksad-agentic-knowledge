#!/usr/bin/env python3
"""Validate RAG corpus manifests without external dependencies."""
from __future__ import annotations
import glob, json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MANIFEST_DIR = ROOT / "rag" / "corpora"
ROLE_DIR = ROOT / "portable" / "roles"
REQUIRED = {
    "id", "version", "description", "status", "source_layer", "indexable", "sensitivity",
    "paths", "exclude", "default_chunk_profile", "allowed_roles", "citation_required", "freshness", "activation"
}
ALLOWED_STATUS = {"active", "example"}
ALLOWED_SENSITIVITY = {"public", "internal", "confidential", "project-confidential"}
HIGH_CONFIDENCE_SECRET = re.compile(r"(ghp_[A-Za-z0-9_]{20,}|github_pat_[A-Za-z0-9_]{20,}|glpat-[A-Za-z0-9_-]{20,}|sk-[A-Za-z0-9]{20,}|Bearer\s+[A-Za-z0-9._~+/=-]{24,})")


def role_ids() -> set[str]:
    return {p.stem for p in ROLE_DIR.glob("*.md") if p.stem != "README"}


def resolve_patterns(patterns: list[str], excludes: list[str]) -> list[Path]:
    files: set[Path] = set()
    excluded: set[Path] = set()
    for pat in excludes:
        for item in glob.glob(str(ROOT / pat), recursive=True):
            p = Path(item)
            if p.is_file():
                excluded.add(p.resolve())
    for pat in patterns:
        # Skip template placeholders in example manifests.
        if "<" in pat or ">" in pat:
            continue
        for item in glob.glob(str(ROOT / pat), recursive=True):
            p = Path(item)
            if p.is_file() and p.resolve() not in excluded:
                files.add(p.resolve())
    return sorted(files)


def main() -> int:
    errors: list[str] = []
    roles = role_ids()
    manifests = sorted(MANIFEST_DIR.glob("*.manifest.json"))
    if not manifests:
        errors.append("No rag/corpora/*.manifest.json files found")
    seen_ids: set[str] = set()
    for path in manifests:
        text = path.read_text(encoding="utf-8")
        if HIGH_CONFIDENCE_SECRET.search(text):
            errors.append(f"{path}: high-confidence secret pattern detected")
        try:
            data = json.loads(text)
        except Exception as exc:
            errors.append(f"{path}: invalid JSON: {exc}")
            continue
        missing = REQUIRED - set(data)
        if missing:
            errors.append(f"{path}: missing required fields: {sorted(missing)}")
            continue
        cid = data["id"]
        if cid in seen_ids:
            errors.append(f"{path}: duplicate corpus id {cid}")
        seen_ids.add(cid)
        if data["status"] not in ALLOWED_STATUS:
            errors.append(f"{path}: invalid status {data['status']!r}")
        if data["sensitivity"] not in ALLOWED_SENSITIVITY:
            errors.append(f"{path}: invalid sensitivity {data['sensitivity']!r}")
        if not isinstance(data["paths"], list) or not data["paths"]:
            errors.append(f"{path}: paths must be a non-empty list")
        if not isinstance(data["exclude"], list):
            errors.append(f"{path}: exclude must be a list")
        allowed = set(data.get("allowed_roles", []))
        unknown = allowed - roles
        if not allowed:
            errors.append(f"{path}: allowed_roles must be non-empty")
        if unknown:
            errors.append(f"{path}: unknown allowed_roles: {sorted(unknown)}")
        if data["status"] == "active":
            if data.get("citation_required") is not True:
                errors.append(f"{path}: active corpus must set citation_required=true")
            resolved = resolve_patterns(data["paths"], data["exclude"])
            if not resolved:
                errors.append(f"{path}: active corpus paths resolved to zero files")
            if data.get("source_layer") != "project-specific":
                joined_excludes = "\n".join(data.get("exclude", []))
                for marker in ("TIA", "USED-CAR", "teams/tia"):
                    if marker not in joined_excludes:
                        errors.append(f"{path}: active base corpus should exclude {marker}")
    if errors:
        print("FAIL: RAG corpus validation")
        for err in errors:
            print(f"- {err}")
        return 1
    print(f"PASS: RAG corpus validation ({len(manifests)} manifests)")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
