#!/usr/bin/env python3
from pathlib import Path
import json, re, sys

ROOT = Path(__file__).resolve().parents[2]
MCP = ROOT / 'mcp'
errors = []

required_top = [
    'mcp/README.md', 'mcp/ROADMAP_P0_TO_PN.md', 'mcp/SETUP_FLOW.md',
    'mcp/SECURITY_MODEL.md', 'mcp/SERVER_MANIFEST_SCHEMA.md',
]
for rel in required_top:
    if not (ROOT / rel).exists():
        errors.append(f'missing top-level MCP file: {rel}')

manifest_paths = sorted((MCP / 'servers').glob('**/manifest.json'))
if not manifest_paths:
    errors.append('no MCP server manifests found')

required_fields = ['id','display_name','priority','status','capabilities','default_enabled','risk','roles','runtime','env_contract','hermes_config','generic_harness','notes']
valid_priorities = {'P0','P1','P2','P2/Pn','Pn'}
role_names = {'business-analyst','system-analyst','technical-leader','developer-backend','developer-frontend','qa-engineer','project-manager','devops-engineer','general-coordinator'}

for path in manifest_paths:
    try:
        data = json.loads(path.read_text(encoding='utf-8'))
    except Exception as e:
        errors.append(f'{path.relative_to(ROOT)} invalid JSON: {e}')
        continue
    for field in required_fields:
        if field not in data:
            errors.append(f'{path.relative_to(ROOT)} missing field: {field}')
    sid = data.get('id')
    if sid and path.parent.name != sid:
        errors.append(f'{path.relative_to(ROOT)} id does not match directory name')
    if data.get('priority') not in valid_priorities:
        errors.append(f'{path.relative_to(ROOT)} invalid priority: {data.get("priority")}')
    if data.get('default_enabled') is not False:
        errors.append(f'{path.relative_to(ROOT)} default_enabled must be false')
    roles = data.get('roles', {})
    for key in ['allowed','optional','forbidden']:
        vals = set(roles.get(key, []))
        unknown = vals - role_names
        if unknown:
            errors.append(f'{path.relative_to(ROOT)} unknown roles in {key}: {sorted(unknown)}')
    hermes = data.get('hermes_config', {})
    if hermes.get('sampling', {}).get('enabled') is not False:
        errors.append(f'{path.relative_to(ROOT)} Hermes sampling must default false')
    for adapter in ['adapters/hermes.example.yaml', 'adapters/generic-harness.example.json', 'README.md', 'install-plan.md', 'security.md', 'validation.md']:
        if not (path.parent / adapter).exists():
            errors.append(f'{path.parent.relative_to(ROOT)} missing {adapter}')

# Secret scan: conservative high-confidence only.
secret_patterns = [
    re.compile(r'ghp_[A-Za-z0-9_]{20,}'),
    re.compile(r'github_pat_[A-Za-z0-9_]{20,}'),
    re.compile(r'glpat-[A-Za-z0-9_-]{20,}'),
    re.compile(r'sk-[A-Za-z0-9]{20,}'),
    re.compile(r'-----BEGIN (RSA |OPENSSH |EC |DSA )?PRIVATE KEY-----'),
]
for path in MCP.rglob('*'):
    if not path.is_file():
        continue
    text = path.read_text(errors='ignore')
    for i, line in enumerate(text.splitlines(), 1):
        stripped = line.strip()
        lowered = stripped.lower()
        if '${' in stripped or '[redacted]' in lowered or 'placeholder' in lowered or 'example' in lowered:
            continue
        for pat in secret_patterns:
            if pat.search(stripped):
                errors.append(f'possible live secret in {path.relative_to(ROOT)}:{i}')
                break

if errors:
    print('FAIL: MCP catalog validation')
    for e in errors:
        print('-', e)
    sys.exit(1)
print(f'PASS: MCP catalog validation ({len(manifest_paths)} server manifests)')
