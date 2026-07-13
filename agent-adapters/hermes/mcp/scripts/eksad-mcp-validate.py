#!/usr/bin/env python3
from pathlib import Path
import re, sys

ROOT = Path(__file__).resolve().parents[4]
errors = []

high_confidence_secret_patterns = [
    re.compile(r'ghp_[A-Za-z0-9_]{20,}'),
    re.compile(r'github_pat_[A-Za-z0-9_]{20,}'),
    re.compile(r'glpat-[A-Za-z0-9_-]{20,}'),
    re.compile(r'sk-[A-Za-z0-9]{20,}'),
    re.compile(r'-----BEGIN (RSA |OPENSSH |EC |DSA )?PRIVATE KEY-----'),
]

for path in ROOT.rglob('*'):
    if not path.is_file() or '.git' in path.parts:
        continue
    if path.name.endswith(('.png','.jpg','.jpeg','.gif','.pdf','.zip','.gz','.zst','.db','.sqlite')):
        continue
    text = path.read_text(errors='ignore')
    # Deliberately conservative: docs may include intentionally-bad examples
    # and placeholders. Block high-confidence live credentials only.
    for i, line in enumerate(text.splitlines(), 1):
        stripped = line.strip()
        if not stripped or stripped.startswith('#'):
            continue
        lowered = stripped.lower()
        if any(marker in lowered for marker in ['example', 'placeholder', '[redacted]', '${', '__env.', '***', 'mypassword', 'eksad_dev_password']):
            continue
        if re.search(r"(?i)(token|password|secret|api[_-]?key|private[_-]?key)\s*[:=][ \t]*['\"]?[A-Za-z0-9_./:+-]{32,}", stripped):
            errors.append(f'possible live credential {path}:{i}: {line[:80]}')
            break
        for pat in high_confidence_secret_patterns:
            if pat.search(stripped):
                errors.append(f'possible live credential {path}:{i}: {line[:80]}')
                break

required = [
    'portable/policies/mcp-policy.md',
    'portable/mcp/role-mcp-matrix.md',
    'portable/mcp/capability-catalog.md',
    'agent-adapters/hermes/mcp/servers/codebase-memory.hermes.example.yaml',
]
for rel in required:
    if not (ROOT / rel).exists():
        errors.append(f'missing required file: {rel}')

if errors:
    print('FAIL')
    for e in errors:
        print('-', e)
    sys.exit(1)
print('PASS: Hermes MCP adapter validation')
