#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"

echo "== EKSAD MCP Doctor (read-only) =="
echo "repo: $ROOT"
echo "branch: $(git branch --show-current 2>/dev/null || echo n/a)"
echo "head: $(git rev-parse --short HEAD 2>/dev/null || echo n/a)"

printf '\n-- Commands --\n'
for cmd in git python3 hermes uv uvx node npm npx; do
  if command -v "$cmd" >/dev/null 2>&1; then
    echo "$cmd: $(command -v "$cmd")"
  else
    echo "$cmd: missing"
  fi
done

printf '\n-- Hermes MCP status --\n'
if command -v hermes >/dev/null 2>&1; then
  hermes mcp list || true
else
  echo "hermes not installed/in PATH"
fi

printf '\n-- Resource hint --\n'
awk '/MemTotal|MemAvailable|SwapTotal|SwapFree/ {print}' /proc/meminfo 2>/dev/null || true

printf '\n-- Catalog validation --\n'
python3 mcp/scripts/validate-mcp-catalog.py

printf '\nDoctor is read-only: no install, no config write, no secrets.\n'
