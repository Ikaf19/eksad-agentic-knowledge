#!/usr/bin/env python3
"""Validate portable portal delivery-mode contracts.

Read-only source-of-truth guardrail: this script checks that the repository
models ExternalWorkItemLink and DeliveryProfile while keeping JIRA-first delivery
future/orchestrator-dependent and JIRA write integration out of the current baseline.
"""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
required_files = {
    "portable/portal/README.md": [
        "ExternalWorkItemLink",
        "DeliveryProfile",
        "link-only external work item references",
    ],
    "portable/portal/external-work-item-link-model.md": [
        "external_work_item_link:",
        "sync_mode: none | manual_snapshot | read_only | orchestrator_managed",
        "`orchestrator_managed` must not be used in Phase 1",
    ],
    "portable/portal/delivery-profile-model.md": [
        "delivery_profile:",
        "jira-linked-manual",
        "jira-first-orchestrated",
        "orchestrator_required: true",
        "jira_write_allowed: false",
    ],
    "portable/portal/jira-first-orchestrator-dependency.md": [
        "Future/orchestrator-dependent",
        "does not approve JIRA runtime write integration",
        "Approved JIRA card",
        "No create card",
        "No update status",
        "No comment writeback",
    ],
    "docs/future/FUTURE_ALIGN_JIRA_FIRST_ORCHESTRATED_DELIVERY.md": [
        "JFD-01",
        "JFD-02",
        "JFD-03",
        "JFD-04",
        "JFD-05",
        "Do not create/update JIRA cards",
    ],
}

errors = []
for rel, snippets in required_files.items():
    path = ROOT / rel
    if not path.is_file():
        errors.append(f"missing required portal delivery file: {rel}")
        continue
    text = path.read_text(encoding="utf-8")
    for snippet in snippets:
        if snippet not in text:
            errors.append(f"{rel} missing expected snippet: {snippet}")

# Prevent accidental current-baseline wording that suggests live JIRA writes are approved.
for rel in [
    "portable/portal/README.md",
    "portable/portal/delivery-profile-model.md",
    "portable/portal/jira-first-orchestrator-dependency.md",
    "docs/future/FUTURE_ALIGN_JIRA_FIRST_ORCHESTRATED_DELIVERY.md",
]:
    path = ROOT / rel
    if not path.is_file():
        continue
    text = path.read_text(encoding="utf-8").lower()
    forbidden = [
        "jira_write_allowed: true",
        "write integration approved",
        "automatic jira mutation is approved",
        "production jira write",
    ]
    for phrase in forbidden:
        if phrase in text:
            errors.append(f"{rel} contains forbidden write-approval wording: {phrase}")

if errors:
    for err in errors:
        print(f"ERROR: {err}")
    sys.exit(1)

print("PASS: portal delivery-mode validation")
