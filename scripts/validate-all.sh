#!/usr/bin/env bash
# Run the complete EKSAD Git source-of-truth validation suite.
# This script is read-only: it does not activate profiles, install tools,
# ingest corpora, render live config, deploy services, or call external systems.

set -Eeuo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

run() {
  printf '\n==> %s\n' "$*"
  "$@"
}

run python3 scripts/validate-role-coverage.py
run python3 scripts/validate-portable.py
run python3 agent-adapters/hermes/hermes-skills/scripts/validate_eksad_skill_suite.py
run python3 agent-adapters/hermes/hermes-skills/scripts/test_validate_eksad_skill_suite_security.py
run python3 agent-adapters/hermes/mcp/scripts/eksad-mcp-validate.py
run python3 mcp/scripts/validate-mcp-catalog.py
run python3 rag/scripts/validate-rag-corpus.py
run python3 rag/scripts/validate-rag-api-contract.py
run python3 eval/rag/scripts/validate-rag-eval.py
run python3 llm-gateway/scripts/validate-llm-gateway-config.py
run python3 scripts/validate-roadmap-consistency.py
run python3 scripts/validate-portal-delivery-mode.py
run python3 scripts/validate-source-consistency.py
run bash agent-adapters/hermes/scripts/test-eksad-pack-resync.sh
run python3 scripts/test-validate-secrets.py
run python3 scripts/validate-secrets.py

printf '\nPASS: complete EKSAD source-of-truth validation suite\n'
