#!/usr/bin/env python3
"""Read-only, high-confidence secret scan for the EKSAD knowledge repository.

The scanner is intentionally conservative: it detects well-known credential signatures,
never prints matched values, does not follow symlinks, and streams text files line by line.
"""
from __future__ import annotations

import argparse
from pathlib import Path
import re
import sys
from typing import Iterator

DEFAULT_ROOT = Path(__file__).resolve().parents[1]
SKIP_PARTS = {".git", "__pycache__", ".pytest_cache", ".venv", "venv", "node_modules"}
BINARY_SUFFIXES = {
    ".png", ".jpg", ".jpeg", ".gif", ".webp", ".ico", ".pdf", ".zip",
    ".gz", ".zst", ".db", ".sqlite", ".pyc", ".class", ".jar", ".woff", ".woff2",
}
SAFE_PUBLIC_SAMPLES = (
    "AKIAIOSFODNN7EXAMPLE",  # AWS public documentation access-key example.
)
SAFE_EXAMPLE_URL_RE = re.compile(
    r"https?://(?:user|username):(?:pass|password)@(?:example\.com|example\.org|example\.net)(?=[:/]|$)",
    flags=re.IGNORECASE,
)
SAFE_ENV_CREDENTIAL_RE = re.compile(
    r"((?:https?|postgres(?:ql)?|mongodb(?:\+srv)?|redis)://)[^\s:/@]+:\$\{[A-Z_][A-Z0-9_]*\}@",
    flags=re.IGNORECASE,
)
PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("private key", re.compile(r"-----BEGIN (?:ENCRYPTED |RSA |EC |DSA |OPENSSH )?PRIVATE KEY-----")),
    ("GitHub token", re.compile(r"\bgh[opusr]_[A-Za-z0-9]{20,}\b")),
    ("GitLab token", re.compile(r"\bglpat-[A-Za-z0-9_-]{20,}\b")),
    ("OpenAI-style key", re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b")),
    ("Slack token", re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{10,}\b")),
    ("Google API key", re.compile(r"\bAIza[0-9A-Za-z_-]{35}\b")),
    ("AWS access key", re.compile(r"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b")),
    (
        "credential-bearing URL",
        re.compile(r"\b(?:https?|postgres(?:ql)?|mongodb(?:\+srv)?|redis)://[^\s:/@]+:[^\s/@]+@", re.IGNORECASE),
    ),
)


def candidate_files(root: Path) -> Iterator[Path]:
    root_resolved = root.resolve()
    for path in root.rglob("*"):
        if path.is_symlink() or any(part in SKIP_PARTS for part in path.parts):
            continue
        if not path.is_file() or path.suffix.lower() in BINARY_SUFFIXES:
            continue
        try:
            path.resolve().relative_to(root_resolved)
        except ValueError:
            continue
        yield path


def normalized_line(line: str) -> str:
    safe = line
    for sample in SAFE_PUBLIC_SAMPLES:
        safe = safe.replace(sample, "[PUBLIC_SAMPLE]")
    safe = SAFE_EXAMPLE_URL_RE.sub("https://[PUBLIC_EXAMPLE]@example.com", safe)
    return SAFE_ENV_CREDENTIAL_RE.sub(r"\1[ENV_AUTH]@", safe)


def scan(root: Path) -> tuple[list[str], int]:
    root = root.resolve()
    findings: list[str] = []
    checked = 0
    for path in candidate_files(root):
        checked += 1
        try:
            with path.open("r", encoding="utf-8", errors="ignore") as handle:
                for lineno, raw_line in enumerate(handle, start=1):
                    line = normalized_line(raw_line)
                    for label, pattern in PATTERNS:
                        if pattern.search(line):
                            findings.append(f"{path.relative_to(root)}:{lineno}: possible {label}")
        except OSError as exc:
            findings.append(f"{path.relative_to(root)}: unable to scan safely: {exc.__class__.__name__}")
    return findings, checked


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=DEFAULT_ROOT)
    args = parser.parse_args()
    findings, checked = scan(args.root)
    if findings:
        print(f"FAIL: high-confidence secret scan found {len(findings)} issue(s):")
        for finding in findings:
            print(f"  - {finding}")
        return 1
    print(f"PASS: high-confidence secret scan ({checked} text files checked)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
