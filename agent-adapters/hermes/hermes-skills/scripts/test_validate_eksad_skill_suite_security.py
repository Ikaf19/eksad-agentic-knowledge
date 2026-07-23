#!/usr/bin/env python3
"""Adversarial path-confinement tests for the EKSAD skill-suite validator."""
from __future__ import annotations

import importlib.util
import os
from pathlib import Path
import tempfile

SCRIPT = Path(__file__).with_name("validate_eksad_skill_suite.py")

with tempfile.TemporaryDirectory(prefix="eksad-skill-validator-") as tmp:
    root = Path(tmp)
    os.environ["EKSAD_VALIDATION_ROOT"] = str(root)
    spec = importlib.util.spec_from_file_location("eksad_skill_validator", SCRIPT)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    for unsafe in ("/etc/passwd", "../outside.txt", "nested/../../outside.txt"):
        try:
            module.source_path(unsafe)
        except ValueError:
            pass
        else:
            raise SystemExit(f"FAIL: unsafe metadata path accepted: {unsafe}")

    external = root.parent / f"{root.name}-external.txt"
    external.write_text("external", encoding="utf-8")
    link = root / "linked-source.txt"
    link.symlink_to(external)
    try:
        module.source_path("linked-source.txt")
    except ValueError:
        pass
    else:
        raise SystemExit("FAIL: source symlink escaping validation root was accepted")
    external.unlink()

print("PASS: skill-suite source metadata confinement tests")
