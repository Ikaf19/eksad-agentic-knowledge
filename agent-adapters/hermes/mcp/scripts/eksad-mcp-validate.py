#!/usr/bin/env python3
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[4]
errors = []

# Repository-wide credential detection is centralized in
# scripts/validate-secrets.py; this validator checks Hermes MCP structure only.

required = [
    'portable/policies/mcp-policy.md',
    'portable/mcp/role-mcp-matrix.md',
    'portable/mcp/capability-catalog.md',
    'agent-adapters/hermes/mcp/servers/codebase-memory.hermes.example.yaml',
]
for rel in required:
    if not (ROOT / rel).exists():
        errors.append(f'missing required file: {rel}')

if errors:
    print('FAIL')
    for e in errors:
        print('-', e)
    sys.exit(1)
print('PASS: Hermes MCP adapter validation')
