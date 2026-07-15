#!/usr/bin/env python3
"""Validate enriched RAG API/tool/MCP contracts without external dependencies."""
from __future__ import annotations
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RAG = ROOT / "rag"
EVAL = ROOT / "eval" / "rag"
MCP_MANIFEST = ROOT / "mcp" / "servers" / "rag-api-readonly" / "manifest.json"
OPENAPI = RAG / "openapi" / "rag-api.openapi.yaml"

REQUIRED_DOCS = [
    "rag/RAG_API_CONTRACT.md",
    "rag/RAG_TOOL_CONTRACT.md",
    "rag/RAG_RUNTIME_COMPONENTS.md",
    "rag/RAG_AUTH_AND_RBAC.md",
    "rag/RAG_INDEXING_PIPELINE.md",
    "rag/RAG_QUERY_PIPELINE.md",
    "rag/RAG_EVIDENCE_AND_ARTIFACTS.md",
    "rag/RAG_FAILURE_MODES.md",
    "rag/RAG_OBSERVABILITY.md",
    "portable/workflows/rag-retrieval-workflow.md",
    "agent-adapters/hermes/skills/rag/eksad-rag-retrieval-workflow/SKILL.md",
    "agent-adapters/hermes/rag/mcp-rag-api.example.yaml",
    "agent-adapters/hermes/rag/profile-tool-policy.md",
    "agent-adapters/hermes/rag/role-usage-matrix.md",
]
REQUIRED_ENDPOINTS = [
    "/health",
    "/v1/corpora",
    "/v1/search",
    "/v1/retrieve",
    "/v1/documents/{document_id}",
    "/v1/artifacts/{artifact_id}/metadata",
    "/v1/citations/resolve",
]
REQUIRED_TOOLS = {
    "rag_search",
    "rag_retrieve",
    "rag_get_document",
    "rag_resolve_citation",
    "rag_get_artifact_metadata",
    "rag_healthcheck",
}
FORBIDDEN_DEFAULT_TOOLS = {
    "rag_index_corpus",
    "rag_rebuild_index",
    "rag_delete_document",
    "rag_write_annotation",
}
SECRET_PATTERNS = [
    re.compile(r"ghp_[A-Za-z0-9_]{20,}"),
    re.compile(r"github_pat_[A-Za-z0-9_]{20,}"),
    re.compile(r"glpat-[A-Za-z0-9_-]{20,}"),
    re.compile(r"sk-[A-Za-z0-9]{20,}"),
    re.compile(r"-----BEGIN (RSA |OPENSSH |EC |DSA )?PRIVATE KEY-----"),
]


def load_json(path: Path, errors: list[str]):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        errors.append(f"{path.relative_to(ROOT)} invalid JSON: {exc}")
        return None


def main() -> int:
    errors: list[str] = []

    for rel in REQUIRED_DOCS:
        if not (ROOT / rel).exists():
            errors.append(f"missing required RAG contract doc: {rel}")

    if not OPENAPI.exists():
        errors.append("missing rag/openapi/rag-api.openapi.yaml")
    else:
        text = OPENAPI.read_text(encoding="utf-8")
        for endpoint in REQUIRED_ENDPOINTS:
            if endpoint not in text:
                errors.append(f"OpenAPI missing endpoint: {endpoint}")
        for schema in ["SearchRequest", "RetrieveRequest", "CitationResolveRequest", "Citation"]:
            if schema not in text:
                errors.append(f"OpenAPI missing schema: {schema}")

    manifest = load_json(MCP_MANIFEST, errors) if MCP_MANIFEST.exists() else None
    if manifest is None:
        errors.append("missing mcp/servers/rag-api-readonly/manifest.json")
    else:
        if manifest.get("id") != "rag-api-readonly":
            errors.append("rag-api-readonly manifest id mismatch")
        if manifest.get("default_enabled") is not False:
            errors.append("rag-api-readonly default_enabled must be false")
        if manifest.get("hermes_config", {}).get("sampling", {}).get("enabled") is not False:
            errors.append("rag-api-readonly sampling must be false")
        tools = set(manifest.get("tool_contract", {}).get("default_tools", []))
        missing_tools = REQUIRED_TOOLS - tools
        if missing_tools:
            errors.append(f"rag-api-readonly missing default tools: {sorted(missing_tools)}")
        forbidden = set(manifest.get("tool_contract", {}).get("forbidden_by_default", []))
        if not FORBIDDEN_DEFAULT_TOOLS <= forbidden:
            errors.append("rag-api-readonly forbidden_by_default missing one or more write/index tools")
        if tools & FORBIDDEN_DEFAULT_TOOLS:
            errors.append("write/index tools must not be default tools")
        fields = set(manifest.get("tool_contract", {}).get("required_result_fields", []))
        for required in ["source_path", "citation", "sensitivity", "corpus_id"]:
            if required not in fields:
                errors.append(f"rag-api-readonly required_result_fields missing {required}")

    # Validate eval fixtures and consistency with manifest.
    fixture_files = [
        "api-contract-tests.json",
        "retrieval-tool-tests.json",
        "citation-contract-tests.json",
        "corpus-rbac-tests.json",
        "artifact-evidence-tests.json",
    ]
    for name in fixture_files:
        p = EVAL / name
        if not p.exists():
            errors.append(f"missing eval fixture: eval/rag/{name}")
            continue
        data = load_json(p, errors)
        if data is not None and not data.get("version"):
            errors.append(f"eval/rag/{name} missing version")

    retrieval = load_json(EVAL / "retrieval-tool-tests.json", errors) if (EVAL / "retrieval-tool-tests.json").exists() else None
    if retrieval:
        fixture_tools = {item.get("name") for item in retrieval.get("tools", [])}
        missing_fixture_tools = REQUIRED_TOOLS - fixture_tools
        if missing_fixture_tools:
            errors.append(f"retrieval-tool-tests missing tools: {sorted(missing_fixture_tools)}")
        forbidden_fixture = set(retrieval.get("forbidden_by_default", []))
        if not FORBIDDEN_DEFAULT_TOOLS <= forbidden_fixture:
            errors.append("retrieval-tool-tests forbidden_by_default incomplete")

    # Validate skill frontmatter minimally.
    skill_path = ROOT / "agent-adapters/hermes/skills/rag/eksad-rag-retrieval-workflow/SKILL.md"
    if skill_path.exists():
        skill = skill_path.read_text(encoding="utf-8")
        if not skill.startswith("---\n") or "name: eksad-rag-retrieval-workflow" not in skill:
            errors.append("Hermes RAG skill template frontmatter invalid")
        if "description:" not in skill:
            errors.append("Hermes RAG skill template missing description")

    # Conservative secret scan over new RAG/MCP/adapter docs. Skip placeholders/env substitutions.
    scan_roots = [RAG, ROOT / "mcp" / "servers" / "rag-api-readonly", ROOT / "agent-adapters" / "hermes" / "rag"]
    for root in scan_roots:
        if not root.exists():
            continue
        for path in root.rglob("*"):
            if not path.is_file() or "__pycache__" in path.parts:
                continue
            text = path.read_text(encoding="utf-8", errors="ignore")
            for i, line in enumerate(text.splitlines(), 1):
                if "${" in line or "placeholder" in line.lower() or "example" in line.lower():
                    continue
                for pat in SECRET_PATTERNS:
                    if pat.search(line):
                        errors.append(f"possible live secret in {path.relative_to(ROOT)}:{i}")
                        break

    if errors:
        print("FAIL: RAG API contract validation")
        for err in errors:
            print(f"- {err}")
        return 1
    print("PASS: RAG API contract validation")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
