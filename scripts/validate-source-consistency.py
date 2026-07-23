#!/usr/bin/env python3
"""Validate onboarding/source consistency without mutating runtime state."""
from __future__ import annotations

from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]

# Historical provenance may retain references to the old repository. Operational
# setup/instruction surfaces must direct new users to the curated source instead.
OPERATIONAL_GLOBS = (
    "README.md",
    "CONTRIBUTING.md",
    "docs/ONBOARDING.md",
    "agent-adapters/hermes/**/*.md",
    "agent-adapters/hermes/hermes-skills/scripts/**/*.py",
    "EKSAD/gpt/README.md",
    "EKSAD/gpt/CLAUDE_SETUP_GUIDE.md",
    "EKSAD/gpt/vibe-coding/**/*.md",
    "EKSAD/gpt/_base/EKSAD_REPO_STRATEGY.md",
)

FORBIDDEN_OPERATIONAL_PATTERNS = {
    "legacy repository URL": re.compile(r"github\.com/Ikaf19/brainstorming", re.IGNORECASE),
    "legacy source branch": re.compile(r"feature/eksad-knowledge-v3", re.IGNORECASE),
    "legacy absolute/example path": re.compile(r"/path/to/brainstorming", re.IGNORECASE),
    "legacy setup source phrase": re.compile(r"(?:copy|copied|copying).{0,40}from (?:this |the )?brainstorming repo", re.IGNORECASE),
    "legacy curated-checkout SI path": re.compile(r"~/\.hermes/knowledge/eksad/role-system-instructions/", re.IGNORECASE),
}

REQUIRED_ONBOARDING_MARKERS = {
    "docs/ONBOARDING.md": (
        "13 roles",
        "independent Hermes role agent",
        "JIRA writes are forbidden",
        "./scripts/validate-all.sh",
        "Runtime profile",
    ),
    "README.md": (
        "docs/ONBOARDING.md",
        "./scripts/validate-all.sh",
    ),
    "CONTRIBUTING.md": (
        "Definition of Done",
        "change-impact",
        "runtime activation",
    ),
}


def iter_operational_files() -> list[Path]:
    files: set[Path] = set()
    for pattern in OPERATIONAL_GLOBS:
        files.update(path for path in ROOT.glob(pattern) if path.is_file())
    return sorted(files)


def main() -> int:
    errors: list[str] = []

    for path in iter_operational_files():
        body = path.read_text(encoding="utf-8", errors="replace")
        rel = path.relative_to(ROOT)
        for label, pattern in FORBIDDEN_OPERATIONAL_PATTERNS.items():
            for match in pattern.finditer(body):
                line = body.count("\n", 0, match.start()) + 1
                errors.append(f"{rel}:{line}: {label}: {match.group(0)!r}")

    for rel, markers in REQUIRED_ONBOARDING_MARKERS.items():
        path = ROOT / rel
        if not path.is_file():
            errors.append(f"missing required onboarding/governance file: {rel}")
            continue
        body = path.read_text(encoding="utf-8")
        for marker in markers:
            if marker not in body:
                errors.append(f"{rel}: missing required marker: {marker}")

    index_rel = "agent-adapters/hermes/per-role-knowledge-index.md"
    index_body = (ROOT / index_rel).read_text(encoding="utf-8")
    if re.search(r"(?m)^\s*\d+\|", index_body):
        errors.append(f"{index_rel}: numbered read-output prefix contamination detected")
    extracted_paths = re.findall(r"(?m)^\*\*Extracted SI:\*\* `([^`]+)`", index_body)
    expected_prefix = "~/.hermes/knowledge/eksad/"
    if len(extracted_paths) != 13:
        errors.append(f"{index_rel}: expected 13 Extracted SI paths, found {len(extracted_paths)}")
    for runtime_path in extracted_paths:
        if not runtime_path.startswith(expected_prefix):
            errors.append(f"{index_rel}: invalid curated checkout path: {runtime_path}")
            continue
        source_path = ROOT / runtime_path[len(expected_prefix):]
        if not source_path.is_file():
            errors.append(f"{index_rel}: Extracted SI source does not exist: {source_path.relative_to(ROOT)}")

    if errors:
        print(f"FAIL: source consistency validation found {len(errors)} error(s):")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"PASS: source consistency validation ({len(iter_operational_files())} operational documents checked)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
