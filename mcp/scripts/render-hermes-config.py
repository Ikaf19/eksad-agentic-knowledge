#!/usr/bin/env python3
"""Render Hermes mcp_servers YAML snippets from mcp/servers/*/manifest.json.

This script is read-only: it prints YAML to stdout and never edits
~/.hermes/config.yaml.
"""
from pathlib import Path
import argparse, json, sys

ROOT = Path(__file__).resolve().parents[2]
MANIFESTS = sorted((ROOT / 'mcp' / 'servers').glob('**/manifest.json'))

def load():
    out = {}
    for p in MANIFESTS:
        data = json.loads(p.read_text(encoding='utf-8'))
        out[data['id']] = data
    return out

def yaml_scalar(v):
    if isinstance(v, bool):
        return 'true' if v else 'false'
    if isinstance(v, (int, float)):
        return str(v)
    return '"' + str(v).replace('"', '\\"') + '"'

def render_server(data):
    cfg = data['hermes_config']
    name = cfg['server_name']
    lines = [f'  {name}:']
    lines.append(f'    command: {yaml_scalar(cfg["command"])}')
    args = cfg.get('args', [])
    if args:
        lines.append('    args:')
        for a in args:
            lines.append(f'      - {yaml_scalar(a)}')
    else:
        lines.append('    args: []')
    env = cfg.get('env', {})
    lines.append('    env:')
    if env:
        for k, v in env.items():
            lines.append(f'      {k}: {yaml_scalar(v)}')
    else:
        lines.append('      {}')
    lines.append(f'    timeout: {cfg.get("timeout", 120)}')
    lines.append(f'    connect_timeout: {cfg.get("connect_timeout", 60)}')
    sampling = cfg.get('sampling', {'enabled': False})
    lines.append('    sampling:')
    lines.append(f'      enabled: {yaml_scalar(sampling.get("enabled", False))}')
    return '\n'.join(lines)

def main():
    parser = argparse.ArgumentParser(description='Render Hermes MCP config snippet from EKSAD MCP manifests')
    parser.add_argument('servers', nargs='*', help='Server IDs to render. Use --list to list available IDs.')
    parser.add_argument('--list', action='store_true', help='List available server IDs')
    args = parser.parse_args()
    data = load()
    if args.list or not args.servers:
        for sid in sorted(data):
            m = data[sid]
            print(f'{sid}\t{m["priority"]}\t{m["status"]}\t{m["display_name"]}')
        if not args.servers:
            print('\n# Pass one or more server IDs to render YAML, e.g.:')
            print('# python3 mcp/scripts/render-hermes-config.py codebase-memory github-readonly')
        return
    missing = [s for s in args.servers if s not in data]
    if missing:
        print(f'Unknown server IDs: {", ".join(missing)}', file=sys.stderr)
        print('Use --list to see available servers.', file=sys.stderr)
        sys.exit(2)
    print('# Generated Hermes MCP config snippet — review before applying.')
    print('# Do not commit live runtime config or real secrets.')
    print('mcp_servers:')
    for sid in args.servers:
        print(render_server(data[sid]))

if __name__ == '__main__':
    main()
