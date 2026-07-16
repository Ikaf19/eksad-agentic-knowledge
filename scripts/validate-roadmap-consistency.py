#!/usr/bin/env python3
"""Validate roadmap/status documents stay aligned with the current source-of-truth baseline.

This validator is intentionally read-only. It checks navigation and status anchors only;
it does not validate every historical statement in long-form docs.
"""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]

required_files = [
    "README.md",
    "docs/GRAND_PLAN.md",
    "docs/ROADMAP.md",
    "docs/PHASE_HISTORY.md",
    "docs/NEXT_PHASE_CANDIDATES.md",
    "docs/future/FUTURE_ALIGN_WEB_PORTAL_CONTROL_PLANE.md",
    "docs/future/FUTURE_ALIGN_JIRA_FIRST_ORCHESTRATED_DELIVERY.md",
]

errors = []
for rel in required_files:
    if not (ROOT / rel).is_file():
        errors.append(f"missing required roadmap file: {rel}")

if errors:
    for err in errors:
        print(f"ERROR: {err}")
    sys.exit(1)

texts = {rel: (ROOT / rel).read_text(encoding="utf-8") for rel in required_files}

checks = {
    "README.md": [
        "docs/ROADMAP.md",
        "docs/PHASE_HISTORY.md",
        "docs/NEXT_PHASE_CANDIDATES.md",
        "13 role profiles",
        "Future Alignment",
    ],
    "docs/GRAND_PLAN.md": [
        "Historical grand plan",
        "docs/ROADMAP.md",
        "Current canonical navigation",
    ],
    "docs/ROADMAP.md": [
        "Current baseline",
        "13 canonical role profiles",
        "NEXT-02",
        "NEXT-03",
        "NEXT-04",
        "NEXT-05",
        "NEXT-06",
        "NEXT-07",
        "NEXT-08",
        "FUTURE_ALIGN_WEB_PORTAL_CONTROL_PLANE.md",
        "FUTURE_ALIGN_JIRA_FIRST_ORCHESTRATED_DELIVERY.md",
        "JIRA-First Orchestrated Delivery",
    ],
    "docs/PHASE_HISTORY.md": [
        "0a66076",
        "0834354",
        "13 roles",
        "Historical documents vs current roadmap",
    ],
    "docs/NEXT_PHASE_CANDIDATES.md": [
        "NEXT-02",
        "NEXT-03",
        "NEXT-04",
        "NEXT-05",
        "NEXT-06",
        "NEXT-07",
        "NEXT-08",
        "not auto-approved",
    ],
    "docs/future/FUTURE_ALIGN_WEB_PORTAL_CONTROL_PLANE.md": [
        "WPC-01",
        "WPC-02",
        "WPC-03",
        "WPC-04",
        "not the next numbered phase",
        "ExternalWorkItemLink",
        "DeliveryProfile",
    ],
    "docs/future/FUTURE_ALIGN_JIRA_FIRST_ORCHESTRATED_DELIVERY.md": [
        "JFD-01",
        "orchestrator",
        "Do not create/update JIRA cards",
    ],
}

for rel, snippets in checks.items():
    text = texts[rel]
    for snippet in snippets:
        if snippet not in text:
            errors.append(f"{rel} missing expected snippet: {snippet}")

# Keep early bootstrap-only blocker wording out of current roadmap docs.
current_docs = ["README.md", "docs/ROADMAP.md", "docs/NEXT_PHASE_CANDIDATES.md"]
for rel in current_docs:
    text = texts[rel]
    for stale in ["Blocked until credential", "feat/initial-commit` on GitHub", "All 9 roles mapped"]:
        if stale in text:
            errors.append(f"{rel} contains stale bootstrap wording: {stale}")

if errors:
    for err in errors:
        print(f"ERROR: {err}")
    sys.exit(1)

print("PASS: roadmap consistency validation")
