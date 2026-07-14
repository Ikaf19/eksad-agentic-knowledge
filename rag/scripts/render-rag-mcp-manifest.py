#!/usr/bin/env python3
"""Render the RAG MCP manifest summary/config without mutating runtime config."""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
manifest_path = ROOT / "mcp" / "servers" / "rag-api-readonly" / "manifest.json"
manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

rendered = {
    "server_id": manifest["id"],
    "display_name": manifest["display_name"],
    "default_enabled": manifest["default_enabled"],
    "risk": manifest["risk"],
    "tools": manifest.get("tool_contract", {}).get("default_tools", []),
    "forbidden_by_default": manifest.get("tool_contract", {}).get("forbidden_by_default", []),
    "hermes_config_example": manifest["hermes_config"],
    "runtime_boundary": "Hermes -> MCP rag-api-readonly -> RAG API; no direct Milvus/MinIO/Ollama credentials in Hermes."
}
print(json.dumps(rendered, indent=2))
