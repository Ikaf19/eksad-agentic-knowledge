#!/usr/bin/env python3
"""Adversarial regression tests for the high-confidence repository secret scanner."""
from __future__ import annotations

from pathlib import Path
import subprocess
import sys
import tempfile

SCANNER = Path(__file__).with_name("validate-secrets.py")


def run(root: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCANNER), "--root", str(root)],
        text=True,
        capture_output=True,
        check=False,
    )


def assert_detected(filename: str, payload: str, label: str) -> None:
    with tempfile.TemporaryDirectory(prefix="eksad-secret-detect-") as tmp:
        root = Path(tmp)
        (root / filename).write_text(payload, encoding="utf-8")
        result = run(root)
        if result.returncode == 0 or label not in result.stdout:
            raise SystemExit(f"FAIL: scanner missed {label}: {result.stdout}{result.stderr}")
        if payload.strip() in result.stdout:
            raise SystemExit(f"FAIL: scanner echoed secret value for {label}")


def assert_safe(filename: str, payload: str, label: str) -> None:
    with tempfile.TemporaryDirectory(prefix="eksad-secret-safe-") as tmp:
        root = Path(tmp)
        (root / filename).write_text(payload, encoding="utf-8")
        result = run(root)
        if result.returncode != 0:
            raise SystemExit(f"FAIL: safe case rejected ({label}): {result.stdout}{result.stderr}")


def main() -> int:
    detections = (
        ("github.txt", "ghp_" + "A" * 24, "GitHub token"),
        ("gitlab.txt", "glpat-" + "B" * 24, "GitLab token"),
        ("openai.txt", "sk-proj-" + "C" * 24, "OpenAI-style key"),
        ("slack.txt", "xoxb-" + "1234567890-" + "D" * 20, "Slack token"),
        ("google.txt", "AIza" + "E" * 35, "Google API key"),
        ("aws.txt", "AKIA" + "F" * 16, "AWS access key"),
        ("url.txt", "postgresql://" + "dbuser:***@db.internal/app", "credential-bearing URL"),
        ("private.pem", "-----BEGIN " + "ENCRYPTED PRIVATE KEY-----\nopaque\n", "private key"),
    )
    for filename, payload, label in detections:
        assert_detected(filename, payload, label)

    safe_cases = (
        ("env.md", "OPENAI_API_KEY=${OPENAI_API_KEY}\n", "environment placeholder"),
        ("aws-doc.md", "AKIAIOSFODNN7EXAMPLE\n", "AWS documentation sample"),
        ("url-doc.md", "https://user:password@example.com/path\n", "example.com credential URL"),
        ("url-env.md", "postgresql://dbuser:${DB_AUTH}@db.internal/app\n", "environment URL placeholder"),
        ("lookalike.md", "sk-short xoxb-short AIza-short glpat-short\n", "short lookalikes"),
    )
    for filename, payload, label in safe_cases:
        assert_safe(filename, payload, label)

    with tempfile.TemporaryDirectory(prefix="eksad-secret-large-") as tmp:
        root = Path(tmp)
        token = "ghp_" + "G" * 24
        with (root / "large.md").open("w", encoding="utf-8") as handle:
            handle.write("safe filler\n" * 500_000)
            handle.write(token + "\n")
        result = run(root)
        if result.returncode == 0 or "GitHub token" not in result.stdout:
            raise SystemExit("FAIL: scanner missed token in large streamed file")
        if token in result.stdout:
            raise SystemExit("FAIL: scanner echoed token from large file")

    with tempfile.TemporaryDirectory(prefix="eksad-secret-invalid-") as tmp:
        root = Path(tmp)
        (root / "invalid.md").write_bytes(b"safe\xfftext\n")
        result = run(root)
        if result.returncode != 0:
            raise SystemExit(f"FAIL: invalid UTF-8 handling failed: {result.stdout}{result.stderr}")

    with tempfile.TemporaryDirectory(prefix="eksad-secret-symlink-") as tmp:
        root = Path(tmp) / "root"
        root.mkdir()
        external = Path(tmp) / "external.txt"
        external_token = "ghp_" + "H" * 24
        external.write_text(external_token, encoding="utf-8")
        (root / "external-link.txt").symlink_to(external)
        result = run(root)
        if result.returncode != 0 or external_token in result.stdout:
            raise SystemExit(f"FAIL: scanner followed external symlink: {result.stdout}{result.stderr}")

    print("PASS: secret scanner adversarial regression tests")
    return 0


if __name__ == "__main__":
    sys.exit(main())
