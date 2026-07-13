# Role MCP Matrix

Legend: ✅ allowed, 🟡 optional/conditional, ❌ forbidden by default.

| Role | Code intelligence | Git RO | CI evidence | Sonar/Trivy | DB schema RO | OpenAPI | Browser | Event/Mongo RO | Observability | Prod write/deploy |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Business Analyst | ❌ | 🟡 | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| System Analyst | ✅ | ✅ | 🟡 | 🟡 | ✅ | ✅ | ❌ | 🟡 | ❌ | ❌ |
| Technical Leader | ✅ | ✅ | ✅ | ✅ | 🟡 | ✅ | ❌ | 🟡 | 🟡 | ❌ |
| Developer Backend | ✅ | ✅ | 🟡 | 🟡 | ✅ | ✅ | ❌ | 🟡 | ❌ | ❌ |
| Developer Frontend | ✅ | ✅ | 🟡 | 🟡 | ❌ | ✅ | ✅ | ❌ | ❌ | ❌ |
| QA Engineer | 🟡 | ✅ | ✅ | 🟡 | 🟡 | ✅ | ✅ | 🟡 | 🟡 | ❌ |
| Project Manager | ❌ | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | 🟡 | ❌ |
| DevOps Engineer | 🟡 | ✅ | ✅ | ✅ | 🟡 | 🟡 | ❌ | 🟡 | ✅ | ❌ by default |
| General Coordinator | ❌ | 🟡 | 🟡 | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |

## Rule

A role may consume evidence from an MCP capability only if the capability is allowed or optional for that role and the current task justifies it.
