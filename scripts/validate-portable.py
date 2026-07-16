#!/usr/bin/env python3
from pathlib import Path
import re, sys

ROOT = Path(__file__).resolve().parents[1]
ROLES = [
    'business-analyst', 'system-analyst', 'technical-leader',
    'developer-backend', 'developer-frontend', 'qa-engineer',
    'project-manager', 'devops-engineer', 'general-coordinator',
]
errors = []

for role in ROLES:
    if not (ROOT / 'portable' / 'roles' / f'{role}.md').exists():
        errors.append(f'missing role card: {role}')

matrix = ROOT / 'portable' / 'mcp' / 'role-mcp-matrix.md'
if not matrix.exists():
    errors.append('missing role-mcp-matrix.md')
else:
    text = matrix.read_text(encoding='utf-8')
    display_names = {
        'business-analyst': 'Business Analyst',
        'system-analyst': 'System Analyst',
        'technical-leader': 'Technical Leader',
        'developer-backend': 'Developer Backend',
        'developer-frontend': 'Developer Frontend',
        'qa-engineer': 'QA Engineer',
        'project-manager': 'Project Manager',
        'devops-engineer': 'DevOps Engineer',
        'general-coordinator': 'General Coordinator',
    }
    for role, display in display_names.items():
        if display not in text:
            errors.append(f'role missing from MCP matrix: {display}')

high_confidence_secret_patterns = [
    re.compile(r'ghp_[A-Za-z0-9_]{20,}'),
    re.compile(r'github_pat_[A-Za-z0-9_]{20,}'),
    re.compile(r'glpat-[A-Za-z0-9_-]{20,}'),
    re.compile(r'sk-[A-Za-z0-9]{20,}'),
    re.compile(r'-----BEGIN (RSA |OPENSSH |EC |DSA )?PRIVATE KEY-----'),
]

# Deliberately line-based and conservative. The EKSAD knowledge pack contains
# security guidance and intentionally-bad examples such as
# `password=mypassword123 # ❌`; those must remain documented. This scanner
# blocks high-confidence live credentials, not educational placeholders.
for path in ROOT.rglob('*'):
    if not path.is_file() or '.git' in path.parts:
        continue
    if path.name.endswith(('.png','.jpg','.jpeg','.gif','.pdf','.zip','.gz','.zst','.db','.sqlite')):
        continue
    text = path.read_text(errors='ignore')
    for i, line in enumerate(text.splitlines(), 1):
        stripped = line.strip()
        if not stripped or stripped.startswith('#'):
            continue
        lowered = stripped.lower()
        if any(marker in lowered for marker in ['example', 'placeholder', '[redacted]', '${', '__env.', 'os.environ/', 'mypassword', 'eksad_dev_password']):
            continue
        if re.search(r"(?i)(token|password|secret|api[_-]?key)\s*[:=][ \t]*['\"]?[A-Za-z0-9_./:+-]{32,}", stripped):
            errors.append(f'possible live credential in {path.relative_to(ROOT)}:{i}')
            break
        for pat in high_confidence_secret_patterns:
            if pat.search(stripped):
                errors.append(f'possible live credential in {path.relative_to(ROOT)}:{i}')
                break

if errors:
    print('FAIL')
    for e in errors:
        print('-', e)
    sys.exit(1)
print('PASS: portable layer validation')
