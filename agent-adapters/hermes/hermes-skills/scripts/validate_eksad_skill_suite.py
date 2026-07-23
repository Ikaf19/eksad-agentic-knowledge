#!/usr/bin/env python3
"""Read-only, deterministic validator for the EKSAD v31 Hermes skill suite.

Set EKSAD_VALIDATION_ROOT to validate an adversarial temporary copy.
"""

from __future__ import annotations

import os
import re
import sys
from collections import defaultdict
from pathlib import Path

DEFAULT_ROOT = Path(__file__).resolve().parents[4]
ROOT = Path(os.environ.get("EKSAD_VALIDATION_ROOT", DEFAULT_ROOT)).resolve()
ADAPTER_ROOT = ROOT / "agent-adapters/hermes" if (ROOT / "agent-adapters/hermes").is_dir() else ROOT
SKILLS_ROOT = ADAPTER_ROOT / "hermes-skills"

REQUIRED_FIELDS = ("name", "description", "version", "author", "license", "metadata")
REQUIRED_V31_SKILLS = {
    "eksad-be-impl": "hermes-skills/software-development/eksad-be-impl/SKILL.md",
    "eksad-qa-delivery": "hermes-skills/quality-assurance/eksad-qa-delivery/SKILL.md",
    "eksad-adr-workflow": "hermes-skills/technical-design/eksad-adr-workflow/SKILL.md",
    "eksad-appsec-review": "hermes-skills/security/eksad-appsec-review/SKILL.md",
}
TEMPLATE_CONVENTIONS = {
    "EKSAD/gpt/_template/EKSAD_GENERIC_UR_TEMPLATE.md": (
        "UR", "UR_{PROJECT_CODE}_v{VERSION}.md", "UR_TIA_v1.0.md"
    ),
    "EKSAD/gpt/_template/EKSAD_GENERIC_TEST_PLAN_RTM_TEMPLATE.md": (
        "Test Plan / RTM", "TESTPLAN_{MODULE_CODE}_v{VERSION}.md", "TESTPLAN_AUTH_v1.0.md"
    ),
    "EKSAD/gpt/_template/EKSAD_GENERIC_ADR_TEMPLATE.md": (
        "ADR", "ADR-{PROJECT_CODE}-{NNN}_{SHORT_TITLE}.md", "ADR-TIA-001_AUTH_BOUNDARY.md"
    ),
    "EKSAD/gpt/_template/EKSAD_GENERIC_WBS_TEMPLATE.md": (
        "WBS", "{PROJECT_CODE}_WBS_{SCOPE}_v{VERSION}.md", "TIA_WBS_AUTH_v1.0.md"
    ),
    "EKSAD/gpt/_template/EKSAD_GENERIC_PROJECT_CLOSURE_TEMPLATE.md": (
        "Project Closure", "{PROJECT_CODE}_PROJECT_CLOSURE_v{VERSION}.md", "TIA_PROJECT_CLOSURE_v1.0.md"
    ),
    "EKSAD/gpt/_template/EKSAD_GENERIC_THREAT_MODEL_TEMPLATE.md": (
        "Threat Model", "{PROJECT_CODE}_THREAT_MODEL_{SCOPE}_v{VERSION}.md", "TIA_THREAT_MODEL_AUTH_v1.0.md"
    ),
}
PROFILE_ROWS = {
    "General Coordinator": "eksad-general",
    "Project Manager": "project-manager",
    "Business Analyst": "business-analyst",
    "System Analyst": "system-analyst",
    "Technical Leader": "technical-leader",
    "Backend Developer": "developer-backend",
    "Frontend Developer": "developer-frontend",
    "QA Engineer": "qa-engineer",
    "DevOps Engineer": "devops-engineer",
    "Data Analyst": "data-analyst",
    "Data Scientist": "data-scientist",
    "UI/UX Designer": "ui-ux-designer",
    "Content Creator": "content-creator",
}
PROFILE_FILES = {f"{slug}.md" for slug in PROFILE_ROWS.values() if slug != "eksad-general"} | {"general.md"}
NAVIGATION_FILES = (
    "README.md",
    "EKSAD/gpt/README.md",
    "EKSAD/gpt/_template/README.md",
    "per-role-knowledge-index.md",
)
CANONICAL_APPSEC = (
    "Any role may raise an AppSec trigger and supply evidence; the System Analyst or Technical Leader "
    "coordinates and invokes the shared `eksad-appsec-review` workflow; only the named risk authority "
    "accepts residual risk or grants a waiver. AppSec is not a profile."
)
ACTIVE_BRANCH = "main"


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def source_path(item: str) -> Path:
    """Resolve source metadata while confining it to the selected validation root."""
    raw = Path(item)
    if raw.is_absolute():
        raise ValueError(f"absolute source path is forbidden: {item}")
    if item == "README.md" or item == "per-role-knowledge-index.md":
        candidate = ADAPTER_ROOT / item
    elif item.startswith(("hermes-skills/", "role-system-instructions/")):
        candidate = ADAPTER_ROOT / item
    else:
        candidate = ROOT / item
    resolved = candidate.resolve(strict=False)
    try:
        resolved.relative_to(ROOT)
    except ValueError as exc:
        raise ValueError(f"source path escapes validation root: {item}") from exc
    return resolved


def require_phrases(path: Path, phrases: tuple[str, ...], errors: list[str], label: str) -> None:
    if not path.is_file():
        errors.append(f"{rel(path)}: missing file required for {label}")
        return
    body = text(path)
    for phrase in phrases:
        if phrase not in body:
            errors.append(f"{rel(path)}: missing {label} invariant: {phrase}")


def parse_frontmatter(path: Path) -> tuple[dict[str, str], str | None]:
    lines = text(path).splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, "missing opening frontmatter delimiter"
    try:
        end = next(i for i in range(1, len(lines)) if lines[i].strip() == "---")
    except StopIteration:
        return {}, "missing closing frontmatter delimiter"
    fields: dict[str, str] = {}
    for line in lines[1:end]:
        match = re.match(r"^([A-Za-z][A-Za-z0-9_-]*):(?:\s*(.*))?$", line)
        if match:
            fields[match.group(1)] = (match.group(2) or "").strip().strip('"').strip("'")
    return fields, None


def canonical_target(token: str, source: Path) -> Path | None:
    cleaned = token.strip("`*.,;:()[]{}")
    if cleaned.startswith("~/.hermes/knowledge/eksad/"):
        return source_path(cleaned.removeprefix("~/.hermes/knowledge/eksad/"))
    if cleaned.startswith(("EKSAD/gpt/", "hermes-skills/", "role-system-instructions/")):
        return source_path(cleaned)
    if cleaned.startswith(("_base/", "_template/", "vibe-coding/")):
        return ROOT / "EKSAD/gpt" / cleaned
    if cleaned.startswith(("references/", "templates/")):
        return source.parent / cleaned
    return None


def check_referenced_paths(path: Path, errors: list[str]) -> None:
    for token in sorted(set(re.findall(r"`([^`\n]+)`", text(path)))):
        if any(char in token for char in ("<", ">", "{", "}", " ", "|")):
            continue
        target = canonical_target(token, path)
        if target is not None and not target.exists():
            errors.append(f"{rel(path)}: referenced canonical path does not exist: {token}")


def check_profiles_and_routing(errors: list[str]) -> None:
    role_dir = ADAPTER_ROOT / "role-system-instructions"
    actual = {path.name for path in role_dir.glob("*.md")}
    if actual != PROFILE_FILES:
        errors.append(
            f"thirteen-profile file invariant failed; missing={sorted(PROFILE_FILES-actual)}, "
            f"extra={sorted(actual-PROFILE_FILES)}"
        )

    orchestrator = ADAPTER_ROOT / "hermes-skills/productivity/stage-gated-orchestrator/SKILL.md"
    body = text(orchestrator) if orchestrator.is_file() else ""
    section_match = re.search(
        r"### Thirteen-profile routing plus shared AppSec workflow\s*(.*?)(?=\n#### Shared AppSec)",
        body,
        flags=re.DOTALL,
    )
    if not section_match:
        errors.append(f"{rel(orchestrator)}: thirteen-profile routing table not found")
        return
    rows: list[tuple[str, str]] = []
    for line in section_match.group(1).splitlines():
        match = re.match(r"^\|\s*(.*?)\s*/\s*`([^`]+)`\s*\|", line)
        if match:
            rows.append((match.group(1).strip(), match.group(2)))
    if len(rows) != 13 or dict(rows) != PROFILE_ROWS:
        errors.append(f"{rel(orchestrator)}: routing rows must be exactly {list(PROFILE_ROWS.items())}; found={rows}")
    if any("appsec" in (name + slug).lower() for name, slug in rows):
        errors.append(f"{rel(orchestrator)}: AppSec must not be a profile routing row")


def check_appsec(errors: list[str]) -> None:
    required = [ADAPTER_ROOT / "README.md", ROOT / "EKSAD/gpt/README.md", ADAPTER_ROOT / "per-role-knowledge-index.md"]
    required += sorted((ADAPTER_ROOT / "role-system-instructions").glob("*.md"), key=rel)
    for path in required:
        if CANONICAL_APPSEC not in text(path):
            errors.append(f"{rel(path)}: canonical shared AppSec routing rule missing or altered")


def check_metadata(errors: list[str]) -> None:
    metadata_docs = [ADAPTER_ROOT / "README.md", ROOT / "EKSAD/gpt/README.md", ADAPTER_ROOT / "per-role-knowledge-index.md"]
    for path in metadata_docs:
        body = text(path)
        if "v31" not in body or ACTIVE_BRANCH not in body:
            errors.append(f"{rel(path)}: active metadata must identify v31 and {ACTIVE_BRANCH}")
        if "feature/eksad-knowledge-v2" in body:
            errors.append(f"{rel(path)}: stale active source branch feature/eksad-knowledge-v2")

    portable_roles = {"data-analyst.md", "data-scientist.md", "ui-ux-designer.md", "content-creator.md"}
    for path in sorted((ADAPTER_ROOT / "role-system-instructions").glob("*.md"), key=rel):
        body = text(path)
        if path.name in portable_roles:
            for required in ("> Source: Phase E portable role expansion", "> Portable role card:", "> Workflow:"):
                if required not in body:
                    errors.append(f"{rel(path)}: portable role metadata missing: {required}")
        elif "> Knowledge pack release: v31" not in body or "branch `main`" not in body:
            errors.append(f"{rel(path)}: legacy role metadata must identify v31 and curated branch main")
        if "feature/eksad-knowledge-v2" in body:
            errors.append(f"{rel(path)}: stale active source branch feature/eksad-knowledge-v2")
        match = re.search(r"^> Extracted source: `([^`]+)`", body, flags=re.MULTILINE)
        if not match and path.name not in portable_roles:
            errors.append(f"{rel(path)}: missing extracted source path metadata")
        elif match:
            try:
                source = source_path(match.group(1))
            except ValueError as exc:
                errors.append(f"{rel(path)}: invalid extracted source path: {exc}")
            else:
                if not source.is_file():
                    errors.append(f"{rel(path)}: extracted source path does not exist: {match.group(1)}")


def check_template_conventions(errors: list[str]) -> None:
    catalog_path = ROOT / "EKSAD/gpt/_template/README.md"
    catalog = text(catalog_path)
    for path_string, (kind, convention, example) in TEMPLATE_CONVENTIONS.items():
        path = source_path(path_string)
        if not path.is_file():
            errors.append(f"required v31 template missing: {path_string}")
            continue
        body = text(path)
        if body.count(convention) < 2:
            errors.append(f"{path_string}: exact filename convention must appear in header and use-footer: {convention}")
        row = f"| {kind} | `{convention}` | `{example}` |"
        if row not in catalog:
            errors.append(f"{rel(catalog_path)}: exact naming row missing: {row}")

    skill_conventions = {
        "hermes-skills/business-analysis/eksad-ba-workflow/SKILL.md": "UR_{PROJECT_CODE}_v{VERSION}.md",
        "hermes-skills/technical-design/eksad-adr-workflow/SKILL.md": "ADR-{PROJECT_CODE}-{NNN}_{SHORT_TITLE}.md",
        "hermes-skills/security/eksad-appsec-review/SKILL.md": "{PROJECT_CODE}_THREAT_MODEL_{SCOPE}_v{VERSION}.md",
        "hermes-skills/quality-assurance/eksad-qa-delivery/SKILL.md": "TESTPLAN_{MODULE_CODE}_v{VERSION}.md",
        "hermes-skills/technical-design/eksad-task-breakdown/SKILL.md": "{PROJECT_CODE}_WBS_{SCOPE}_v{VERSION}.md",
        "hermes-skills/project-management/eksad-pm-delivery/SKILL.md": "{PROJECT_CODE}_PROJECT_CLOSURE_v{VERSION}.md",
    }
    for path_string, convention in skill_conventions.items():
        if convention not in text(source_path(path_string)):
            errors.append(f"{path_string}: missing exact output filename convention: {convention}")

    forbidden = (
        "ADR_{PROJECT_CODE}_{NNN}_{SHORT_TITLE}.md",
        "{PROJECT_CODE}_THREAT_MODEL.md",
        "{PROJECT_CODE}_TEST_PLAN_RTM.md",
        "{PROJECT_CODE}_WBS.md",
        "{PROJECT_CODE}_PROJECT_CLOSURE.md",
        "UR_<PROJECT>",
        "TESTPLAN_<MODULE>",
        "PLAN_<MODULE>",
    )
    active = [ADAPTER_ROOT / "README.md", ADAPTER_ROOT / "per-role-knowledge-index.md", catalog_path]
    active += sorted((ADAPTER_ROOT / "role-system-instructions").glob("*.md"), key=rel)
    active += sorted(SKILLS_ROOT.rglob("SKILL.md"), key=rel)
    active += [ROOT / item for item in TEMPLATE_CONVENTIONS]
    for path in active:
        body = text(path)
        for rejected in forbidden:
            if rejected in body:
                errors.append(f"{rel(path)}: rejected filename convention found: {rejected}")


def check_forbidden_assumptions(errors: list[str], skill_files: list[Path]) -> None:
    provenance = ADAPTER_ROOT / "hermes-skills/PROVENANCE.md"
    active = [ADAPTER_ROOT / "README.md", ROOT / "EKSAD/gpt/README.md", ADAPTER_ROOT / "per-role-knowledge-index.md"]
    active += sorted((ADAPTER_ROOT / "role-system-instructions").glob("*.md"), key=rel) + skill_files
    active += [provenance]
    for path in active:
        body = text(path)
        for pattern, label in ((r"localhost:9876", "localhost:9876"), (r"\.claude/", ".claude/")):
            matches = list(re.finditer(pattern, body, flags=re.IGNORECASE))
            if not matches:
                continue
            if path != provenance:
                errors.append(f"{rel(path)}: rejected assumption is allowed only in PROVENANCE: {label}")
            elif "## Rejected assumptions" not in body or len(matches) != 1:
                errors.append(f"{rel(path)}: {label} must appear once, only as a rejected-assumption record")


def check_no_gates_and_ownership(errors: list[str]) -> None:
    orchestrator = ADAPTER_ROOT / "hermes-skills/productivity/stage-gated-orchestrator/SKILL.md"
    require_phrases(
        orchestrator,
        (
            "contains neither Project Manager nor DevOps work",
            "A pipeline containing either role must fail closed with gates enabled",
            "If `--no-gates` is requested and any stage includes `project-manager` or `devops-engineer` ownership, reject no-gates initialization",
        ),
        errors,
        "PM/DevOps no-gates incompatibility",
    )
    for item in (
        "role-system-instructions/project-manager.md",
        "hermes-skills/project-management/eksad-pm-delivery/SKILL.md",
        "role-system-instructions/devops-engineer.md",
        "hermes-skills/devops/eksad-devops-delivery/SKILL.md",
    ):
        body = text(source_path(item)).lower()
        if "no-gates" not in body or not re.search(r"(?:prohibit|never|no `--no-gates`|cannot|do not use)", body):
            errors.append(f"{item}: must explicitly prohibit no-gates execution")

    require_phrases(
        ADAPTER_ROOT / "role-system-instructions/general.md",
        ("never absorb BA, SA, TL, developer, QA, PM, DevOps, Data Analyst, Data Scientist, UI/UX, or Content Creator ownership",),
        errors,
        "General non-ownership",
    )
    require_phrases(
        orchestrator,
        ("The General Coordinator role coordinates and never absorbs specialist ownership",),
        errors,
        "General non-ownership",
    )
    require_phrases(
        ADAPTER_ROOT / "per-role-knowledge-index.md",
        ("General Coordinator coordinates and never owns specialist outputs",),
        errors,
        "General non-ownership",
    )


def check_qa_and_cache(errors: list[str]) -> None:
    require_phrases(
        ADAPTER_ROOT / "role-system-instructions/qa-engineer.md",
        (
            "This assistant = Mode A (Design)",
            "This Hermes profile produces no test code",
            "designated in-IDE agent, not this assistant",
        ),
        errors,
        "QA Mode-A-only",
    )
    require_phrases(
        ADAPTER_ROOT / "hermes-skills/quality-assurance/eksad-qa-delivery/SKILL.md",
        ("Produces no test code", "Mode A — Design / Docs", "no code writes"),
        errors,
        "QA Mode-A-only",
    )
    require_phrases(
        ADAPTER_ROOT / "per-role-knowledge-index.md",
        ("this Hermes profile produces no test code", "Mode B automation remains with the in-IDE QA agent"),
        errors,
        "QA Mode-A-only catalog",
    )

    cache_phrases = (
        "event-sourced `{entity}_cache`",
        "do not extend `BaseEntity`",
        "do not use `BaseRepository`",
        "no soft-delete columns",
        "source DELETE event",
        "tenant-scoped",
    )
    require_phrases(
        ADAPTER_ROOT / "hermes-skills/software-development/eksad-be-impl/SKILL.md",
        cache_phrases,
        errors,
        "cache exception",
    )
    require_phrases(
        ADAPTER_ROOT / "role-system-instructions/developer-backend.md",
        cache_phrases,
        errors,
        "cache exception",
    )


def check_role_contract_regressions(errors: list[str]) -> None:
    general_paths = (
        "EKSAD/gpt/SYSTEM_INSTRUCTIONS_SHORT.md",
        "EKSAD/gpt/SYSTEM_INSTRUCTIONS.md",
        "role-system-instructions/general.md",
    )
    for item in general_paths:
        body = text(source_path(item))
        if "Route specialist production" not in body:
            errors.append(f"{item}: missing General coordinator boundary: Route specialist production")
        if not re.search(r"(?:must not author|Author or revise) BRD, FSD, TSD", body, flags=re.IGNORECASE):
            errors.append(f"{item}: missing General prohibition on specialist artifact authoring")
        for forbidden in (
            "Your primary roles:",
            "before generating any BRD or FSD",
            "Code examples must use EKSAD stack",
            "Frontend Developer — implement",
        ):
            if forbidden.lower() in body.lower():
                errors.append(f"{item}: legacy General specialist-production contract found: {forbidden}")

    qa_paths = (
        "EKSAD/gpt/qa/QA_SYSTEM_INSTRUCTIONS_SHORT.md",
        "EKSAD/gpt/qa/QA_SYSTEM_INSTRUCTIONS.md",
        "role-system-instructions/qa-engineer.md",
    )
    for item in qa_paths:
        body = text(source_path(item))
        for required in (
            "baselined `TESTPLAN_{MODULE_CODE}_v{VERSION}.md`",
            "generated test source",
        ):
            if required not in body:
                errors.append(f"{item}: missing QA Mode-A/Mode-B handoff boundary: {required}")
        for forbidden in (
            "PLAN_<MODULE>",
            "API Test scripting",
            "## REST Assured Test Scripting",
            "building API test scripts",
        ):
            if forbidden.lower() in body.lower():
                errors.append(f"{item}: QA test-code authorization regression found: {forbidden}")

    sa_paths = (
        "EKSAD/gpt/system-analyst/SA_SYSTEM_INSTRUCTIONS_SHORT.md",
        "EKSAD/gpt/system-analyst/SA_SYSTEM_INSTRUCTIONS.md",
        "role-system-instructions/system-analyst.md",
    )
    for item in sa_paths:
        body = text(source_path(item))
        for required in ("developer-backend", "developer-frontend", "Technical Leader reviews"):
            if required not in body:
                errors.append(f"{item}: missing Developer implementation routing and TL review boundary: {required}")
        if "implementation code is in the Technical Leader" in body:
            errors.append(f"{item}: implementation is incorrectly assigned to Technical Leader")

    pm_paths = (
        "hermes-skills/project-management/eksad-pm-delivery/SKILL.md",
        "EKSAD/gpt/project-manager/PM_SYSTEM_INSTRUCTIONS_SHORT.md",
        "EKSAD/gpt/project-manager/PM_SYSTEM_INSTRUCTIONS.md",
        "role-system-instructions/project-manager.md",
    )
    for item in pm_paths:
        body = text(source_path(item))
        for required in (
            "EKSAD_GENERIC_WBS_TEMPLATE.md",
            "{PROJECT_CODE}_WBS_{SCOPE}_v{VERSION}.md",
            "approved WBS baseline",
        ):
            if required not in body:
                errors.append(f"{item}: missing PM WBS governance invariant: {required}")

    pm_setup_paths = (
        "EKSAD/gpt/README.md",
        "EKSAD/gpt/CLAUDE_SETUP_GUIDE.md",
        "EKSAD/gpt/project-manager/CLAUDE_PM_SETUP_GUIDE.md",
        "EKSAD/gpt/project-manager/GPT_PM_SETUP_GUIDE.md",
    )
    for item in pm_setup_paths:
        body = text(source_path(item))
        if "EKSAD_GENERIC_WBS_TEMPLATE.md" not in body:
            errors.append(f"{item}: PM setup/upload guidance must include EKSAD_GENERIC_WBS_TEMPLATE.md")
    index_body = text(ADAPTER_ROOT / "per-role-knowledge-index.md")
    if "~/.hermes/profiles/project-manager/skills/project-management/eksad-pm-delivery/" not in index_body:
        errors.append("per-role-knowledge-index.md: PM skill path must be profile-local")
    if "~/.hermes/skills/project-management/eksad-pm-delivery/" in index_body:
        errors.append("per-role-knowledge-index.md: PM skill path must not point to global runtime skill")

    backend_source_paths = (
        "EKSAD/gpt/developer/DEV_SYSTEM_INSTRUCTIONS_SHORT.md",
        "EKSAD/gpt/developer/DEV_SYSTEM_INSTRUCTIONS.md",
    )
    for item in backend_source_paths:
        body = text(source_path(item))
        for required in ("5 contract methods", "ActionLabels", "source DELETE event"):
            if required not in body:
                errors.append(f"{item}: missing current Backend CrudFlows/cache invariant: {required}")
        for forbidden in ("4 abstract methods", "4 contract methods"):
            if forbidden in body:
                errors.append(f"{item}: stale Backend repository contract found: {forbidden}")

    for item in qa_paths:
        body = text(source_path(item))
        for required in ("remains `NOT_RUN` permanently", "separate attributable evidence/assessment artifacts"):
            if required not in body:
                errors.append(f"{item}: missing immutable Mode-A test-plan invariant: {required}")
        for forbidden in ("all return 422", "have at least 1 passing test", "✅ = Passed", "❌ = Failed"):
            if forbidden.lower() in body.lower():
                errors.append(f"{item}: mutable or hard-coded QA outcome regression found: {forbidden}")

    fe_paths = (
        "EKSAD/gpt/developer/DEV_FE_SYSTEM_INSTRUCTIONS.md",
        "EKSAD/gpt/developer/DEV_FE_SYSTEM_INSTRUCTIONS_SHORT.md",
        "role-system-instructions/developer-frontend.md",
        "EKSAD/gpt/developer/CLAUDE_DEV_FE_SETUP_GUIDE.md",
        "EKSAD/gpt/_template/EKSAD_GENERIC_FE_TSD_TEMPLATE.md",
        "EKSAD/gpt/system-analyst/SA_SYSTEM_INSTRUCTIONS.md",
        "EKSAD/gpt/vibe-coding/developer-fe/COPILOT_DEV_FE_INSTRUCTIONS.md",
        "EKSAD/gpt/vibe-coding/developer-fe/CLAUDE_CODE_DEV_FE_INSTRUCTIONS.md",
        "EKSAD/gpt/vibe-coding/developer-fe/CURSOR_DEV_FE_RULES.md",
    )
    for item in fe_paths:
        body = text(source_path(item))
        for required in ("apiClient", "withCredentials", "HttpOnly"):
            if required not in body:
                errors.append(f"{item}: missing FE real-API/session invariant: {required}")
        for forbidden in (
            "default mock data layer",
            "mock-to-real",
            "VITE_AUTH_TOKEN_KEY",
            "parseJwt(",
            "localStorage.setItem",
            "sessionStorage.setItem",
        ):
            if forbidden.lower() in body.lower():
                errors.append(f"{item}: forbidden FE mock/token implementation found: {forbidden}")

    navigation_contracts = {
        "EKSAD/gpt/README.md": ("General Coordinator", "eksad-general", "real API", "HttpOnly"),
        "per-role-knowledge-index.md": ("General Coordinator (`eksad-general`)", "does not author or approve specialist-owned artifacts"),
        "EKSAD/gpt/CLAUDE_SETUP_GUIDE.md": ("General Coordinator", "real API", "HttpOnly"),
        "EKSAD/gpt/qa/CLAUDE_QA_SETUP_GUIDE.md": ("Mode A (Design)", "does **not** write"),
        "EKSAD/gpt/qa/GPT_QA_CHAT_STARTERS.md": ("Mode B", "handoff"),
    }
    for item, required_phrases in navigation_contracts.items():
        body = text(source_path(item))
        for required in required_phrases:
            if required not in body:
                errors.append(f"{item}: missing navigation/role contract: {required}")

    claude_guide = ROOT / "EKSAD/gpt/CLAUDE_SETUP_GUIDE.md"
    body = text(claude_guide)
    for required in ("exactly 9 active Claude Assistants", "devops-engineer/CLAUDE_DEVOPS_SETUP_GUIDE.md"):
        if required not in body:
            errors.append(f"{rel(claude_guide)}: missing nine-assistant guide invariant: {required}")
    if re.search(r"\b8 Claude Assistants\b", body, flags=re.IGNORECASE):
        errors.append(f"{rel(claude_guide)}: stale eight-assistant identity found")


def check_provenance(errors: list[str]) -> None:
    path = ADAPTER_ROOT / "hermes-skills/PROVENANCE.md"
    body = text(path)
    if "Verified:" in body or "**Verified" in body:
        errors.append(f"{rel(path)}: external license claim is asserted verified without repository evidence")
    if body.count("Needs verification") < 7:
        errors.append(f"{rel(path)}: every external source license status must remain explicitly unverified")
    if "no vendored snapshot or license evidence" not in body:
        errors.append(f"{rel(path)}: missing repository-evidence limitation for external license claims")


def validate() -> list[str]:
    errors: list[str] = []
    skill_files = sorted(SKILLS_ROOT.rglob("SKILL.md"), key=rel)
    names: defaultdict[str, list[str]] = defaultdict(list)
    if not skill_files:
        errors.append("hermes-skills: no SKILL.md files found")

    for path in skill_files:
        fields, fm_error = parse_frontmatter(path)
        if fm_error:
            errors.append(f"{rel(path)}: {fm_error}")
            continue
        for field in REQUIRED_FIELDS:
            if field not in fields:
                errors.append(f"{rel(path)}: missing required frontmatter field '{field}'")
            elif field != "metadata" and not fields[field]:
                errors.append(f"{rel(path)}: empty required frontmatter field '{field}'")
        name = fields.get("name", "")
        if name:
            names[name].append(rel(path))
            if name != path.parent.name:
                errors.append(f"{rel(path)}: frontmatter name '{name}' does not match directory '{path.parent.name}'")
        check_referenced_paths(path, errors)

    for name, paths in sorted(names.items()):
        if len(paths) > 1:
            errors.append(f"duplicate skill name '{name}': {', '.join(paths)}")
    for name, expected in sorted(REQUIRED_V31_SKILLS.items()):
        if not (source_path(expected)).is_file():
            errors.append(f"required v31 skill missing: {expected}")
        elif name not in names:
            errors.append(f"required v31 skill name not discovered: {name}")

    for nav in NAVIGATION_FILES:
        path = source_path(nav)
        if not path.is_file():
            errors.append(f"canonical navigation file missing: {nav}")
            continue
        check_referenced_paths(path, errors)
        body = text(path)
        required_mentions = []
        if nav in ("EKSAD/gpt/README.md", "per-role-knowledge-index.md"):
            required_mentions += [Path(item).name for item in TEMPLATE_CONVENTIONS]
        if nav == "per-role-knowledge-index.md":
            required_mentions += list(REQUIRED_V31_SKILLS)
        for item in required_mentions:
            if item not in body:
                errors.append(f"{nav}: missing v31 catalog entry '{item}'")

    check_profiles_and_routing(errors)
    check_appsec(errors)
    check_metadata(errors)
    check_template_conventions(errors)
    check_forbidden_assumptions(errors, skill_files)
    check_no_gates_and_ownership(errors)
    check_qa_and_cache(errors)
    check_role_contract_regressions(errors)
    check_provenance(errors)
    return sorted(set(errors))


def main() -> int:
    errors = validate()
    if errors:
        print(f"FAIL: EKSAD v31 skill suite validation found {len(errors)} error(s):")
        for error in errors:
            print(f"  - {error}")
        return 1
    skill_count = len(list(SKILLS_ROOT.rglob("SKILL.md")))
    print(
        "PASS: EKSAD v31 skill suite validated "
        f"({skill_count} skills, {len(TEMPLATE_CONVENTIONS)} required v31 templates, "
        "exactly 13 profile routes, AppSec shared)."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
