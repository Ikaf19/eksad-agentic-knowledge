#!/usr/bin/env python3
"""Render a LiteLLM config example from EKSAD alias manifest.

Read-only: prints to stdout; does not read env values or write live config.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ALIASES = ROOT / "llm-gateway" / "aliases" / "eksad-model-aliases.json"


def main() -> None:
    data = json.loads(ALIASES.read_text(encoding="utf-8"))
    print("# Rendered example only. Do not store real keys in Git.")
    print("model_list:")
    for item in data["aliases"]:
        alias = item["alias"]
        model_env = item["litellm_model_env"]
        key_env = item["api_key_env"]
        base_env = item.get("api_base_env")
        print(f"  - model_name: {alias}")
        print("    litellm_params:")
        print(f"      model: openai/${{{model_env}}}")
        print(f"      api_key: os.environ/{key_env}")
        if base_env:
            print(f"      api_base: os.environ/{base_env}")
    print("")
    print("router_settings:")
    print("  routing_strategy: least-busy")
    print("  num_retries: 1")
    print("  timeout: 60")
    print("")
    print("litellm_settings:")
    print("  drop_params: true")
    print("  set_verbose: false")
    print("")
    print("general_settings:")
    print("  master_key: os.environ/EKSAD_LITELLM_MASTER_KEY")
    print("  database_url: os.environ/EKSAD_LITELLM_DATABASE_URL")


if __name__ == "__main__":
    main()
