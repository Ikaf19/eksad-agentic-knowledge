#!/usr/bin/env bash
set -euo pipefail

echo "== EKSAD MCP Doctor (read-only) =="
echo "PWD: $(pwd)"

echo "
-- Hermes CLI --"
if command -v hermes >/dev/null 2>&1; then
  hermes --version || true
  hermes mcp list || true
else
  echo "hermes: not found"
fi

echo "
-- Runtime commands --"
for cmd in git python3 uv uvx node npm npx; do
  if command -v "$cmd" >/dev/null 2>&1; then
    echo "$cmd: $(command -v "$cmd")"
  else
    echo "$cmd: missing"
  fi
done

echo "
-- Resource hint --"
awk '/MemTotal|MemAvailable|SwapTotal|SwapFree/ {print}' /proc/meminfo 2>/dev/null || true

echo "
Doctor is read-only. It does not install or write runtime config."
