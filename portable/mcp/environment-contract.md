# MCP Environment Contract

## Git may contain

- Server names
- Capability mapping
- Example config
- Env var names
- Doctor/validate/render scripts

## Git must not contain

- Tokens
- Passwords
- Connection strings
- Private endpoints if sensitive
- Downloaded binaries
- Caches/indexes

## Runtime must provide

- Approved binaries or package managers
- Local env values
- Network access to approved endpoints
- Least-privilege credentials
- Explicit apply/restart step
