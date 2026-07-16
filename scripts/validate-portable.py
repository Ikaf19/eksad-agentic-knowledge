#!/usr/bin/env python3
from pathlib import Path
import re, sys

ROOT = Path(__file__).resolve().parents[1]
ROLES = [
    'general-coordinator', 'business-analyst', 'system-analyst', 'technical-leader',
    'developer-backend', 'developer-frontend', 'qa-engineer', 'project-manager',
    'devops-engineer', 'data-analyst', 'data-scientist', 'ui-ux-designer', 'content-creator',
]
DISPLAY_NAMES = {
    'general-coordinator': 'General Coordinator',
    'business-analyst': 'Business Analyst',
    'system-analyst': 'System Analyst',
    'technical-leader': 'Technical Leader',
    'developer-backend': 'Developer Backend',
    'developer-frontend': 'Developer Frontend',
    'qa-engineer': 'QA Engineer',
    'project-manager': 'Project Manager',
    'devops-engineer': 'DevOps Engineer',
    'data-analyst': 'Data Analyst',
    'data-scientist': 'Data Scientist',
    'ui-ux-designer': 'UI/UX Designer',
    'content-creator': 'Content Creator',
}
errors = []

for role in ROLES:
    if not (ROOT / 'portable' / 'roles' / f'{role}.md').exists():
        errors.append(f'missing role card: {role}')

required_docs = [
    'portable/mcp/role-mcp-matrix.md',
    'portable/rag/corpus-matrix.md',
    'portable/llm-gateway/role-model-matrix.md',
    'portable/roles/role-collaboration-matrix.md',
    'portable/policies/role-boundaries.md',
]
for rel in required_docs:
    path = ROOT / rel
    if not path.exists():
        errors.append(f'missing portable doc: {rel}')
        continue
    text = path.read_text(encoding='utf-8')
    for role, display in DISPLAY_NAMES.items():
        if role not in text and display not in text:
            errors.append(f'{rel}: missing role coverage for {role}')

matrix = (ROOT / 'portable' / 'llm-gateway' / 'role-model-matrix.md').read_text(encoding='utf-8')
if '| Visual input |' not in matrix or 'eksad.visual_input' not in matrix:
    errors.append('role-model-matrix: missing normalized visual input column/alias')
if '| UI/UX Designer | `eksad.vision`' in matrix or '| UI/UX Designer | `eksad.visual_input`' in matrix:
    errors.append('role-model-matrix: UI/UX primary must not be a visual alias')

high_confidence_secret_patterns = [
    re.compile(r'ghp_[A-Za-z0-9_]{20,}'),
    re.compile(r'github_pat_[A-Za-z0-9_]{20,}'),
    re.compile(r'glpat-[A-Za-z0-9_-]{20,}'),
    re.compile(r'sk-[A-Za-z0-9]{20,}'),
    re.compile(r'-----BEGIN (RSA |OPENSSH |EC |DSA )?PRIVATE KEY-----'),
]

# Deliberately line-based and conservative. The EKSAD knowledge pack contains
# security guidance and intentionally-bad examples; block high-confidence live
# credentials, not educational placeholders.
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
print(f'PASS: portable layer validation ({len(ROLES)} canonical roles)')
