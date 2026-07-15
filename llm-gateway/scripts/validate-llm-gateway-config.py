#!/usr/bin/env python3
"""Validate EKSAD LLM gateway desired-state files.

Read-only: does not contact providers, read env secrets, or write runtime config.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
GW = ROOT / "llm-gateway"
ALIASES = GW / "aliases" / "eksad-model-aliases.json"

REQUIRED_ALIASES = {
    "eksad.fast",
    "eksad.default",
    "eksad.reasoning",
    "eksad.long_context",
    "eksad.embedding",
    "eksad.reranker",
    "eksad.vision",
    "eksad.guardrail",
}

REQUIRED_FILES = [
    "README.md",
    "ARCHITECTURE.md",
    "MODEL_ALIAS_POLICY.md",
    "MODEL_ALIAS_SCHEMA.md",
    "PROVIDER_MATRIX.md",
    "ROUTING_POLICY.md",
    "PER_TASK_ROUTING.md",
    "BUDGET_AND_RATE_LIMIT_POLICY.md",
    "OBSERVABILITY.md",
    "GUARDRAILS_POLICY.md",
    "FAILURE_AND_FALLBACK_POLICY.md",
    "SECURITY_MODEL.md",
    "aliases/eksad-model-aliases.json",
    "litellm/config.example.yaml",
    "litellm/env.example",
    "adapters/hermes/hermes.example.yaml",
    "adapters/generic-openai-compatible/client.example.json",
]

SECRET_PATTERNS = [
    re.compile(r"ghp_[A-Za-z0-9_]{20,}"),
    re.compile(r"github_pat_[A-Za-z0-9_]{20,}"),
    re.compile(r"glpat-[A-Za-z0-9_-]{20,}"),
    re.compile(r"sk-[A-Za-z0-9]{24,}"),
    re.compile(r"xox[baprs]-[A-Za-z0-9-]{20,}"),
    re.compile(r"AKIA[0-9A-Z]{16}"),
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    re.compile(r"(?i)(password|api_key|token|secret)\s*[:=]\s*['\"]?[A-Za-z0-9_./+=-]{16,}")
]

ALLOW_SECRET_PLACEHOLDER_FRAGMENTS = (
    "os.environ/",
    "${",
    "change-me",
    "placeholder",
)


def is_allowed_placeholder_line(line_text: str) -> bool:
    stripped = line_text.strip()
    if not stripped or stripped.startswith("#"):
        return True
    if any(fragment in stripped for fragment in ALLOW_SECRET_PLACEHOLDER_FRAGMENTS):
        return True
    # env.example-style empty assignment, e.g. EKSAD_PRIMARY_PROVIDER_API_KEY=
    if re.fullmatch(r"[A-Z0-9_]+\s*=\s*", stripped):
        return True
    return False


def fail(msg: str) -> None:
    print(f"FAIL: {msg}", file=sys.stderr)
    sys.exit(1)


def load_aliases() -> dict:
    if not ALIASES.exists():
        fail(f"missing {ALIASES.relative_to(ROOT)}")
    try:
        return json.loads(ALIASES.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail(f"invalid alias JSON: {exc}")


def validate_required_files() -> None:
    missing = [p for p in REQUIRED_FILES if not (GW / p).exists()]
    if missing:
        fail("missing required files: " + ", ".join(missing))


def validate_alias_manifest(data: dict) -> None:
    aliases = data.get("aliases")
    if not isinstance(aliases, list) or not aliases:
        fail("aliases must be a non-empty list")

    seen = set()
    alias_map = {}
    for item in aliases:
        if not isinstance(item, dict):
            fail("alias entries must be objects")
        name = item.get("alias")
        if not isinstance(name, str) or not name.startswith("eksad."):
            fail(f"invalid alias name: {name!r}")
        if name in seen:
            fail(f"duplicate alias: {name}")
        seen.add(name)
        alias_map[name] = item
        for field in ["capability", "cost_tier", "context_class", "litellm_model_env", "api_key_env", "fallback_aliases", "allowed_roles", "typical_tasks", "security_notes"]:
            if field not in item:
                fail(f"alias {name} missing {field}")
        if item["cost_tier"] not in {"low", "medium", "high"}:
            fail(f"alias {name} has invalid cost_tier")
        if not isinstance(item["fallback_aliases"], list):
            fail(f"alias {name} fallback_aliases must be a list")
        if not isinstance(item["allowed_roles"], list) or not item["allowed_roles"]:
            fail(f"alias {name} allowed_roles must be non-empty list")

    if not REQUIRED_ALIASES.issubset(seen):
        fail("missing required aliases: " + ", ".join(sorted(REQUIRED_ALIASES - seen)))

    declared_required = set(data.get("required_aliases", []))
    if declared_required != REQUIRED_ALIASES:
        fail("required_aliases does not match canonical set")

    for name, item in alias_map.items():
        for fallback in item.get("fallback_aliases", []):
            if fallback not in alias_map:
                fail(f"alias {name} references unknown fallback {fallback}")

    role_defaults = data.get("role_defaults", {})
    if not isinstance(role_defaults, dict) or not role_defaults:
        fail("role_defaults must be non-empty object")
    for role, mapping in role_defaults.items():
        if not isinstance(mapping, dict):
            fail(f"role_defaults.{role} must be object")
        for key, alias in mapping.items():
            if alias not in alias_map:
                fail(f"role_defaults.{role}.{key} references unknown alias {alias}")

    for service_alias in ["eksad.embedding", "eksad.reranker"]:
        item = alias_map[service_alias]
        if "rag-service" not in item.get("allowed_roles", []):
            fail(f"{service_alias} must allow rag-service")
        chat_roles = set(item.get("allowed_roles", [])) - {"rag-service"}
        if chat_roles:
            fail(f"{service_alias} must be service-only by default, found {sorted(chat_roles)}")


def validate_litellm_example(data: dict) -> None:
    text = (GW / "litellm" / "config.example.yaml").read_text(encoding="utf-8")
    for alias in REQUIRED_ALIASES:
        if f"model_name: {alias}" not in text:
            fail(f"LiteLLM example missing {alias}")
    if "os.environ/" not in text:
        fail("LiteLLM example must use environment variable references")


def validate_eval_fixtures() -> None:
    eval_dir = ROOT / "eval" / "llm-gateway"
    for name in ["alias-contract-tests.json", "routing-policy-tests.json", "budget-policy-tests.json"]:
        path = eval_dir / name
        if not path.exists():
            fail(f"missing eval fixture {path.relative_to(ROOT)}")
        data = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(data.get("tests"), list) or not data["tests"]:
            fail(f"eval fixture {name} must contain non-empty tests")


def scan_for_secrets() -> None:
    for path in GW.rglob("*"):
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for pattern in SECRET_PATTERNS:
            for match in pattern.finditer(text):
                line = text[:match.start()].count("\n") + 1
                line_text = text.splitlines()[line - 1].strip()
                if is_allowed_placeholder_line(line_text):
                    continue
                fail(f"possible secret in {path.relative_to(ROOT)}:{line}")


def main() -> None:
    validate_required_files()
    data = load_aliases()
    validate_alias_manifest(data)
    validate_litellm_example(data)
    validate_eval_fixtures()
    scan_for_secrets()
    print("PASS: LLM gateway desired-state validation")


if __name__ == "__main__":
    main()
