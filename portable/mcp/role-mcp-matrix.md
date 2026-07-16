# Role MCP Matrix

Legend: ✅ allowed, 🟡 optional/conditional, ❌ forbidden by default.

| Role | Code intel | Git RO | CI evidence | Quality/Security | DB schema/data RO | OpenAPI | Browser/UI | Event/Mongo RO | Observability | Data/BI RO | Notebook sandbox | Design asset RO | Content draft | Prod write/deploy |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Business Analyst | ❌ | 🟡 | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| System Analyst | ✅ | ✅ | 🟡 | 🟡 | ✅ | ✅ | ❌ | 🟡 | ❌ | 🟡 | ❌ | 🟡 | ❌ | ❌ |
| Technical Leader | ✅ | ✅ | ✅ | ✅ | 🟡 | ✅ | ❌ | 🟡 | 🟡 | 🟡 | ❌ | 🟡 | ❌ | ❌ |
| Developer Backend | ✅ | ✅ | 🟡 | 🟡 | ✅ | ✅ | ❌ | 🟡 | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Developer Frontend | ✅ | ✅ | 🟡 | 🟡 | ❌ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ |
| QA Engineer | 🟡 | ✅ | ✅ | 🟡 | 🟡 | ✅ | ✅ | 🟡 | 🟡 | 🟡 | ❌ | 🟡 | ❌ | ❌ |
| Project Manager | ❌ | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | 🟡 | 🟡 | ❌ | ❌ | 🟡 | ❌ |
| DevOps Engineer | 🟡 | ✅ | ✅ | ✅ | 🟡 | 🟡 | ❌ | 🟡 | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ by default |
| General Coordinator | ❌ | 🟡 | 🟡 | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Data Analyst | ❌ | 🟡 | ❌ | ❌ | ✅ | 🟡 | ❌ | ❌ | 🟡 | ✅ | 🟡 | ❌ | ❌ | ❌ |
| Data Scientist | 🟡 | 🟡 | ❌ | ❌ | 🟡 | ❌ | ❌ | ❌ | 🟡 | ✅ | ✅ | ❌ | ❌ | ❌ |
| UI/UX Designer | ❌ | 🟡 | ❌ | ❌ | ❌ | 🟡 | ✅ | ❌ | ❌ | ❌ | ❌ | ✅ | 🟡 | ❌ |
| Content Creator | ❌ | 🟡 | ❌ | ❌ | ❌ | ❌ | 🟡 | ❌ | ❌ | ❌ | ❌ | 🟡 | ✅ | ❌ |

## Rule

A role may consume evidence from an MCP capability only if the capability is allowed or optional for that role and the current task justifies it. Optional access does not grant approval authority or write permission.
