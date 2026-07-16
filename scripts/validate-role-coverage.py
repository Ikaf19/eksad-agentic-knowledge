#!/usr/bin/env python3
"""Validate canonical role coverage across portable and Hermes adapter layers."""
from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]

CANONICAL_ROLES = {
    "general-coordinator": {"display": "General Coordinator", "skill": "eksad-general-coordination", "si_file": "general.md"},
    "business-analyst": {"display": "Business Analyst", "skill": "eksad-ba-workflow"},
    "system-analyst": {"display": "System Analyst", "skill": "eksad-tsd-design"},
    "technical-leader": {"display": "Technical Leader", "skill": "eksad-code-review"},
    "developer-backend": {"display": "Developer Backend", "skill": "eksad-be-impl"},
    "developer-frontend": {"display": "Developer Frontend", "skill": "eksad-fe-impl"},
    "qa-engineer": {"display": "QA Engineer", "skill": "eksad-qa-delivery"},
    "project-manager": {"display": "Project Manager", "skill": "eksad-pm-delivery"},
    "devops-engineer": {"display": "DevOps Engineer", "skill": "eksad-devops-delivery"},
    "data-analyst": {"display": "Data Analyst", "skill": "eksad-data-analysis"},
    "data-scientist": {"display": "Data Scientist", "skill": "eksad-data-science"},
    "ui-ux-designer": {"display": "UI/UX Designer", "skill": "eksad-ui-ux-delivery"},
    "content-creator": {"display": "Content Creator", "skill": "eksad-content-creation"},
}

ROLE_EVAL_FIXTURE = "eval/roles/role-expansion-tests.json"

MATRIX_FILES = [
    "portable/mcp/role-mcp-matrix.md",
    "portable/rag/corpus-matrix.md",
    "portable/llm-gateway/role-model-matrix.md",
    "portable/deliverables/deliverable-matrix.md",
    "portable/policies/role-boundaries.md",
    "agent-adapters/hermes/per-role-knowledge-index.md",
    "agent-adapters/hermes/rag/role-usage-matrix.md",
    "portable/roles/role-collaboration-matrix.md",
]


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def main() -> int:
    errors: list[str] = []

    for slug, meta in CANONICAL_ROLES.items():
        role_path = ROOT / "portable/roles" / f"{slug}.md"
        if not role_path.is_file():
            errors.append(f"missing portable role card: {role_path.relative_to(ROOT)}")
        si_name = meta.get("si_file", f"{slug}.md")
        si_path = ROOT / "agent-adapters/hermes/role-system-instructions" / si_name
        if not si_path.is_file():
            errors.append(f"missing Hermes role SI: {si_path.relative_to(ROOT)}")
        skill = meta["skill"]
        if skill:
            skill_hits = list((ROOT / "agent-adapters/hermes/hermes-skills").rglob(f"{skill}/SKILL.md"))
            if not skill_hits:
                errors.append(f"missing Hermes skill for role {slug}: {skill}")
        mcp_profile = ROOT / "mcp" / "profiles" / f"{slug}.md"
        if not mcp_profile.is_file():
            errors.append(f"missing MCP profile for role {slug}: {mcp_profile.relative_to(ROOT)}")
        for rel in MATRIX_FILES:
            body = read(rel)
            if slug not in body and meta["display"] not in body:
                errors.append(f"{rel}: missing role coverage for {slug}")

    aliases = json.loads(read("llm-gateway/aliases/eksad-model-aliases.json"))
    alias_map = {item["alias"]: set(item.get("allowed_roles", [])) for item in aliases.get("aliases", [])}
    defaults = aliases.get("role_defaults", {})
    for slug in CANONICAL_ROLES:
        if slug == "general-coordinator":
            # Existing alias manifest uses this canonical slug.
            pass
        if slug not in defaults:
            errors.append(f"llm-gateway aliases: missing role_defaults for {slug}")
            continue
        for key, alias in defaults[slug].items():
            if alias not in alias_map:
                errors.append(f"llm-gateway aliases: {slug}.{key} references unknown alias {alias}")
            elif slug not in alias_map[alias] and alias not in {"eksad.embedding", "eksad.reranker"}:
                errors.append(f"llm-gateway aliases: {slug}.{key}={alias} but role not allowed")

    # Verify Phase E-specific workflow and deliverables are linked from each new role skill.
    phase_e_links = {
        "data-analyst": ["data-analysis-workflow.md", "data-analysis-report.md", "dashboard-spec.md"],
        "data-scientist": ["data-science-workflow.md", "ml-experiment-report.md"],
        "ui-ux-designer": ["ui-ux-workflow.md", "ux-research-report.md", "wireframe-handoff.md"],
        "content-creator": ["content-creation-workflow.md", "content-brief.md", "content-calendar.md"],
    }
    for slug, required in phase_e_links.items():
        skill = CANONICAL_ROLES[slug]["skill"]
        skill_path = next((ROOT / "agent-adapters/hermes/hermes-skills").rglob(f"{skill}/SKILL.md"), None)
        if skill_path is None:
            continue
        body = skill_path.read_text(encoding="utf-8")
        for marker in required:
            if marker not in body:
                errors.append(f"{skill_path.relative_to(ROOT)}: missing linked artifact {marker}")


    # Verify Phase E-specific eval fixtures.
    eval_fixture_path = ROOT / ROLE_EVAL_FIXTURE
    phase_e_roles = {"data-analyst", "data-scientist", "ui-ux-designer", "content-creator"}
    if not eval_fixture_path.is_file():
        errors.append(f"missing role eval fixture: {ROLE_EVAL_FIXTURE}")
    else:
        try:
            cases = json.loads(eval_fixture_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"{ROLE_EVAL_FIXTURE}: invalid JSON: {exc}")
            cases = []
        seen_eval_roles: set[str] = set()
        required_case_fields = {
            "id",
            "role",
            "prompt",
            "expected_deliverable",
            "expected_behavior",
            "must_handoff_to",
            "forbidden_behavior",
        }
        for idx, case in enumerate(cases):
            missing = required_case_fields - set(case)
            if missing:
                errors.append(f"{ROLE_EVAL_FIXTURE}[{idx}]: missing fields {sorted(missing)}")
                continue
            role = case["role"]
            if role not in phase_e_roles:
                errors.append(f"{ROLE_EVAL_FIXTURE}[{idx}]: role must be one of Phase E roles, got {role}")
            else:
                seen_eval_roles.add(role)
            deliverable = ROOT / case["expected_deliverable"]
            if not deliverable.is_file():
                errors.append(f"{ROLE_EVAL_FIXTURE}[{idx}]: expected_deliverable not found: {case['expected_deliverable']}")
            for owner in case.get("must_handoff_to", []):
                if owner not in CANONICAL_ROLES:
                    errors.append(f"{ROLE_EVAL_FIXTURE}[{idx}]: unknown handoff owner {owner}")
            if not case.get("forbidden_behavior"):
                errors.append(f"{ROLE_EVAL_FIXTURE}[{idx}]: forbidden_behavior must not be empty")
        missing_roles = phase_e_roles - seen_eval_roles
        if missing_roles:
            errors.append(f"{ROLE_EVAL_FIXTURE}: missing eval cases for {sorted(missing_roles)}")

    if errors:
        print(f"FAIL: role coverage validation found {len(errors)} error(s):")
        for error in sorted(set(errors)):
            print(f"- {error}")
        return 1
    print(f"PASS: role coverage validation ({len(CANONICAL_ROLES)} canonical roles).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
