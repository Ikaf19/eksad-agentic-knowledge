#!/usr/bin/env python3
from pathlib import Path
import sys

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

# Portable contracts may describe adapter-neutral extension points, but they must
# never depend on a runtime-specific source path.
for path in sorted((ROOT / 'portable').rglob('*.md')):
    text = path.read_text(encoding='utf-8')
    if 'agent-adapters/' in text:
        errors.append(f'{path.relative_to(ROOT)}: portable layer must not reference runtime adapter paths')

if errors:
    print('FAIL')
    for e in errors:
        print('-', e)
    sys.exit(1)
print(f'PASS: portable layer validation ({len(ROLES)} canonical roles)')
