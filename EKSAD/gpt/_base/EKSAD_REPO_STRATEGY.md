# EKSAD Repository & Build Strategy

**Version:** 1.0
**Date:** 2026-05-24
**Owner:** EKSAD Platform Team
**Audience:** ALL — Developers, Architects, SA, TL, DevOps, AI/Claude
**Priority:** 🔴 P0 — Every developer must understand repo boundaries
**Related:** `EKSAD_CICD_CONTAINER_PATTERNS.md`, `EKSAD_BASE_PRINCIPLES.md`, `EKSAD_DOMAIN_REGISTRY.md`

> **Decision 15:** EKSAD uses **Model B** — published BOM per independent repo. NOT a multi-module monorepo.

---

## Table of Contents

1. [Overview — Independent Repo per Service](#1-overview--independent-repo-per-service)
2. [Repo Categories & Naming Convention](#2-repo-categories--naming-convention)
3. [Dependency Flow Diagram](#3-dependency-flow-diagram)
4. [Artifact Publishing Strategy](#4-artifact-publishing-strategy)
5. [Version Pinning Policy](#5-version-pinning-policy)
6. [Per-Repo Folder Structure](#6-per-repo-folder-structure)
7. [CI/CD per Repo](#7-cicd-per-repo)
8. [How to Create a New Service Repo](#8-how-to-create-a-new-service-repo)
9. [Known Pitfalls](#9-known-pitfalls)

---

## 1. Overview — Independent Repo per Service

EKSAD uses **Model B: Published Parent POM as BOM** — every service lives in its **own Git repository** with its own independent build, test, and deploy pipeline.

| Model | Description | EKSAD? |
|-------|-------------|--------|
| **Model A** — Monorepo reactor | One Git repo, all services as Maven modules. Single `mvn install` builds everything. | ❌ NOT used |
| **Model B** — Independent repos + BOM | Each service is a standalone repo. `eksad-parent` publishes a BOM POM to an artifact registry. Services declare it as `<parent>`. | ✅ **EKSAD standard** |

### Why Model B?

- **Parallel development** — teams work on different repos without merge conflicts
- **Independent CI/CD** — `svc-pipeline` can release v1.3 while `svc-orders` is still at v1.1
- **Independent deploy** — rolling update one service without touching others
- **Team ownership** — one team owns one or more repos, clear accountability
- **Faster builds** — each repo builds only its own code (no 30-service reactor build)

### The Golden Rule

> **One service = one repo = one CI/CD pipeline = one Docker image**

No exceptions. Shared code lives in libraries (`eksad-core-common`, etc.), not in a sibling service.

---

## 2. Repo Categories & Naming Convention

EKSAD has **8 repo categories**:

| # | Category | Example Repos | Build Output | Published to Artifact Registry? |
|---|----------|--------------|--------------|--------------------------------|
| 1 | **BOM / Parent POM** | `eksad-parent` | POM file | ✅ Required — all repos inherit this |
| 2 | **Shared Libraries** | `eksad-core-common`, `eksad-core-auth-client` | JAR | ✅ Required — services depend on these |
| 3 | **Core Infra Services** | `eksad-core-auth`, `eksad-core-audittrail`, `eksad-core-storage`, `eksad-gateway` | Docker Image | ❌ Docker registry only |
| 4 | **Fixed-Name Services** | `svc-user-management`, `svc-master-data`, `svc-tenant-management` | Docker Image | ❌ Docker registry only |
| 5 | **Domain Services** | `svc-pipeline`, `svc-orders`, `svc-payment` | Docker Image | ❌ Docker registry only |
| 6 | **Frontend** | `eksad-frontend` | Static build / Docker | ❌ Docker registry only |
| 7 | **Infrastructure** | `eksad-infra` | Configs (K8s manifests, Jenkins templates) | ❌ Git only |
| 8 | **Knowledge & Docs** | `eksad-agentic-knowledge` | Markdown files | ❌ Git only |

### Naming Rules

| Type | Pattern | Examples |
|------|---------|----------|
| Core infra service | `eksad-core-{function}` | `eksad-core-auth`, `eksad-core-storage` |
| Shared library | `eksad-core-{name}` or `eksad-{name}-client` | `eksad-core-common`, `eksad-core-auth-client` |
| Fixed platform service | `svc-{function}` | `svc-user-management`, `svc-master-data` |
| Domain service | `svc-{function}` (BA→SA named) | `svc-pipeline`, `svc-orders` |
| Frontend | `eksad-frontend` or `{project}-frontend` | `eksad-frontend` |
| Infrastructure | `eksad-infra` | `eksad-infra` |

**All names:** lowercase, hyphen-separated, no underscores, no camelCase.

---

## 3. Dependency Flow Diagram

Dependencies flow **downward only**. Services never depend on other services as Maven artifacts.

```
┌──────────────────────────────────────────────────────┐
│                   eksad-parent                        │
│           (BOM — version management only)             │
│                 Published POM                         │
└──────────────────────┬───────────────────────────────┘
                       │ <parent> (all repos)
          ┌────────────┴────────────────────┐
          │                                 │
┌─────────▼──────────┐         ┌────────────▼───────────┐
│  eksad-core-common  │         │  eksad-core-auth-client │
│    Published JAR    │         │      Published JAR      │
└─────────┬──────────┘         └────────────┬───────────┘
          │ <dependency>                     │ <dependency>
          │ (all services)                   │ (if service needs auth)
          └──────────────┬───────────────────┘
                         │
┌────────────────────────▼──────────────────────────────┐
│                 All Services                          │
│  eksad-core-auth   │  svc-pipeline  │  svc-orders    │
│  svc-user-mgmt     │  svc-master    │  svc-payment   │
│  eksad-gateway     │  svc-tenant    │  ...           │
│           (Docker Images — never published to Maven)  │
└───────────────────────────────────────────────────────┘
              ↕ REST API / RabbitMQ events only ↕
              (NEVER Maven <dependency> between services)
```

### Dependency Rules

| Rule | Description |
|------|-------------|
| **DR-01** | Libraries (JAR) flow DOWN only: parent → common/client → service |
| **DR-02** | No service may declare another service as Maven `<dependency>` |
| **DR-03** | Inter-service communication = REST call OR RabbitMQ event |
| **DR-04** | `eksad-core-common` must contain ONLY infrastructure/utility code — no business logic |
| **DR-05** | Circular dependencies are forbidden — will fail CI |

---

## 4. Artifact Publishing Strategy

Only **Category 1 (BOM) and Category 2 (Libraries)** are published to an artifact registry. Services produce Docker images only.

### Phase Roadmap

| Phase | Registry | Timeline | Setup |
|-------|----------|----------|-------|
| **Phase 1** | GitHub Packages (`maven.pkg.github.com/eksad/`) | Sprint 1 | Free for public/private repos. CI: GitHub Actions → `mvn deploy`. No infrastructure required. |
| **Phase 2** | Nexus Repository (self-hosted on K8s) | Sprint 3+ | `nexus.eksad.internal`. Proxies Maven Central. Zero code change — only `settings.xml` URL update. |

### What Gets Published

| Artifact | Artifact Registry? | Docker Registry? | Notes |
|----------|-------------------|-----------------|-------|
| `eksad-parent` | ✅ POM | ❌ | Version anchor for all repos |
| `eksad-core-common` | ✅ JAR | ❌ | BaseEntity, BaseRepository, utilities |
| `eksad-core-auth-client` | ✅ JAR | ❌ | SDK for auth consumers |
| `eksad-core-auth` | ❌ | ✅ Docker | Contains JWT signing key — never JAR |
| `svc-pipeline`, `svc-orders`, ... | ❌ | ✅ Docker | Business services — Docker only |
| `eksad-gateway` | ❌ | ✅ Docker | API gateway — Docker only |

### GitHub Actions — Publish GitHub Packages (Phase 1)

```yaml
# .github/workflows/publish.yml (library repos only)
name: Publish to GitHub Packages
on:
  push:
    tags: ['v*.*.*']
jobs:
  publish:
    runs-on: ubuntu-latest
    permissions: { contents: read, packages: write }
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-java@v4
        with: { java-version: '21', distribution: 'temurin', server-id: github }
      - run: mvn -B deploy -DskipTests
        env: { GITHUB_TOKEN: '${{ secrets.GITHUB_TOKEN }}' }
```

```xml
<!-- settings.xml (consumer repos) -->
<servers>
  <server>
    <id>github</id>
    <username>${env.GITHUB_ACTOR}</username>
    <password>${env.GITHUB_TOKEN}</password>
  </server>
</servers>
```

---

## 5. Version Pinning Policy

All published artifacts use **Semantic Versioning (MAJOR.MINOR.PATCH)**.

| Artifact | MAJOR trigger | MINOR trigger | PATCH trigger | Consumer upgrade policy |
|----------|--------------|---------------|---------------|------------------------|
| `eksad-parent` | Breaking build config / plugin API change | New dependency pins, new plugin additions | Bug fix in plugin config, dependency version bump | Upgrade within **1 sprint** of release |
| `eksad-core-common` | Breaking API — method signature change, class rename, removed field | New features — new base class, new utility method | Bug fix, internal refactor | **2 sprints** to upgrade; migration guide required |
| `eksad-core-auth-client` | Follows `core-auth` API MAJOR (breaking endpoint change) | New SDK method for new endpoint | Bug fix, retry config | Backward compat within same MAJOR; **1 sprint** to upgrade |

### Pinning Rules

| Rule | Requirement |
|------|-------------|
| **VP-01** | Always pin exact version in `pom.xml` — never use SNAPSHOT in production |
| **VP-02** | SNAPSHOT versions allowed only in development branches |
| **VP-03** | New MINOR/PATCH version must not break existing consumers |
| **VP-04** | New DTO fields in libraries must be nullable / Optional |
| **VP-05** | Deprecation: `@Deprecated(since="X.Y", forRemoval=true)` — minimum 2 minor versions grace period |

---

## 6. Per-Repo Folder Structure

### 6.1 Service Repo Template

```
{service-name}/                             ← root
├── pom.xml                                 ← parent: eksad-parent (exact version)
├── Dockerfile                              ← see EKSAD_CICD_CONTAINER_PATTERNS.md §2
├── docker-compose.dev.yml                  ← local dev: infra deps only
├── Jenkinsfile                             ← CI/CD pipeline (or .github/workflows/)
├── README.md
├── CLAUDE.md                               ← AI assistant context for this service
├── docs/
│   └── eksad/
│       └── _base/                          ← copy of knowledge files for AI
├── src/
│   ├── main/
│   │   ├── java/com/eksad/{service}/
│   │   │   ├── entity/
│   │   │   ├── repository/
│   │   │   ├── service/
│   │   │   ├── resource/
│   │   │   └── dto/
│   │   └── resources/
│   │       ├── application.properties
│   │       └── db/migration/               ← Flyway SQL files
│   │           └── V1__init.sql
│   └── test/
│       └── java/com/eksad/{service}/
├── k8s/                                    ← Kubernetes manifests (Kustomize)
│   ├── base/
│   └── overlays/ { dev, staging, prod }
├── .github/
│   ├── workflows/ci.yml                    ← GitHub Actions (if not Jenkins)
│   └── copilot-instructions.md             ← AI instructions copy
└── .cursor/rules/eksad-dev.mdc             ← Cursor AI rules
```

### 6.2 Library Repo Template

```
{library-name}/                             ← root
├── pom.xml                                 ← parent: eksad-parent; packaging: jar
├── README.md
├── src/
│   ├── main/java/com/eksad/platform/{lib}/
│   └── test/java/com/eksad/platform/{lib}/
├── .github/
│   ├── workflows/
│   │   ├── ci.yml                          ← build + test on PR
│   │   └── publish.yml                     ← deploy to artifact registry on tag
│   └── copilot-instructions.md
└── CHANGELOG.md                            ← required for libraries
```

### 6.3 `pom.xml` Parent Declaration

```xml
<!-- All service and library repos start with this -->
<parent>
  <groupId>com.eksad.platform</groupId>
  <artifactId>eksad-parent</artifactId>
  <version>1.0.0</version>                  <!-- ← ALWAYS exact version, never SNAPSHOT in prod -->
  <!-- No <relativePath> — fetched from artifact registry -->
</parent>

<dependencies>
  <!-- Required for all services -->
  <dependency>
    <groupId>com.eksad.platform</groupId>
    <artifactId>eksad-core-common</artifactId>
    <!-- version managed by BOM — no explicit version tag needed -->
  </dependency>

  <!-- Required only for services that authenticate -->
  <dependency>
    <groupId>com.eksad.platform</groupId>
    <artifactId>eksad-core-auth-client</artifactId>
    <!-- version managed by BOM -->
  </dependency>
</dependencies>
```

---

## 7. CI/CD per Repo

Every repo has its **own independent pipeline**. No cross-repo build triggers.

### 7.1 Pipeline Types

| Repo Type | Pipeline Steps | Output |
|-----------|---------------|--------|
| **Library repo** | Checkout → Build → Unit Test → Integration Test → `mvn deploy` (on tag) | JAR in artifact registry |
| **Service repo** | Checkout → Build → Unit Test → Integration Test → Security Scan → Docker Build → Docker Push → Deploy | Docker image in registry + K8s deploy |
| **BOM/Parent repo** | Checkout → `mvn verify` (validate POM) → `mvn deploy` (on tag) | POM in artifact registry |
| **Frontend repo** | Checkout → `npm install` → `npm test` → `npm build` → Docker Build → Push | Docker image |
| **Infra repo** | Checkout → Lint manifests → Apply to target env (manual gate for prod) | K8s config applied |

### 7.2 Branch Strategy (all repos)

| Branch | CI trigger | Deploy target | Gate |
|--------|-----------|----------------|------|
| `develop` | push | dev cluster | auto |
| `release/*` | push | staging | manual input |
| `main` | push | production | manual + `submitter: admin` |

### 7.3 Pipeline Templates

Canonical pipeline templates live in `eksad-infra` repo:
- `templates/jenkins/Jenkinsfile.service` — for service repos
- `templates/jenkins/Jenkinsfile.library` — for library repos
- `templates/github-actions/ci.service.yml`
- `templates/github-actions/publish.library.yml`

**Rule:** copy templates into each repo; do not use shared library as a remote dependency for pipeline config.

---

## 8. How to Create a New Service Repo

Follow these 12 steps in order:

| # | Step | Detail |
|---|------|--------|
| 1 | Create Git repo | Name: `svc-{function}` following §2 naming convention. Initialize with `main` branch. |
| 2 | Copy service template | Copy folder structure from §6.1 into the new repo. |
| 3 | Set parent POM | Edit `pom.xml` → `<parent>` to `eksad-parent` at latest released version. |
| 4 | Add `eksad-core-common` | Add dependency (version managed by BOM — no explicit `<version>`). |
| 5 | Add `eksad-core-auth-client` | Add dependency only if this service handles authentication / token validation. |
| 6 | Configure `application.properties` | DB host/name/user, RabbitMQ, JWT validator URL, EKSAD_SERVICE_NAME. |
| 7 | Create `V1__init.sql` | Flyway migration at `src/main/resources/db/migration/`. Include `tenant_id`, `deleted_at`, `version`. |
| 8 | Create `Dockerfile` | Copy JVM multi-stage template from `EKSAD_CICD_CONTAINER_PATTERNS.md §2.2`. |
| 9 | Setup CI/CD | Copy Jenkinsfile / GitHub Actions workflow from `eksad-infra/templates/`. |
| 10 | Copy knowledge files | Copy `docs/eksad/_base/` from the curated `eksad-agentic-knowledge` repository. Copy `CLAUDE.md` and `.github/copilot-instructions.md`. |
| 11 | Add to infra compose | Add service block to `eksad-infra` docker-compose for local full-stack testing. |
| 12 | Register in domain registry | Add entry to `EKSAD_DOMAIN_REGISTRY.md` (port, service name, module type prefix). |

> ⚠️ Do NOT skip step 10 — AI assistants (GitHub Copilot, Claude, Cursor) need the knowledge files to generate EKSAD-compliant code.

---

## 9. Known Pitfalls

### Anti-Patterns — Never Do These

| ❌ Anti-pattern | ✅ Correct approach | Why |
|----------------|---------------------|-----|
| Add `svc-pipeline` as Maven `<dependency>` of `svc-orders` | Communicate via REST call or RabbitMQ event | Tight coupling — breaks independent deploy; circular compile-time dependency |
| Put business logic in `eksad-core-common` | Put only infrastructure/utility code (BaseEntity, BaseRepository, etc.) | `core-common` updates would break all services; logic belongs in domain service |
| Skip a BOM version for >2 sprints | Upgrade within 1–2 sprint window | Version drift makes future upgrades painful; security patches missed |
| Publish service JARs to artifact registry | Publish Docker images only | Services change API frequently; coupling services via JAR breaks Model B |
| Put two microservices in one Git repo | One service = one repo | Breaks independent CI/CD; forces coupled releases |
| Use `<relativePath>` for parent POM in service repo | Remove `<relativePath>` or leave empty | Works only locally; breaks CI where repos are in separate workspaces |
| Use `SNAPSHOT` in production pom.xml | Pin exact version | SNAPSHOT is non-deterministic — same version can produce different artifacts |
| Cross-update shared lib without CHANGELOG | Write CHANGELOG.md entry + bump version | Consumers cannot upgrade safely without knowing what changed |

### Warning Signs (Code Review Checklist)

- [ ] Service `pom.xml` declares `<dependency>` on another service artifact (not library)
- [ ] `eksad-core-common` contains a class with `@ApplicationScoped` / `@Service` business logic
- [ ] Service repo uses `<relativePath>../eksad-parent/pom.xml</relativePath>`
- [ ] Parent POM version is more than 2 sprints behind latest
- [ ] No `V1__init.sql` in new service repo
- [ ] No `CLAUDE.md` or `copilot-instructions.md` in new service repo

---

## Cross-References

- Container build patterns → `EKSAD_CICD_CONTAINER_PATTERNS.md`
- Service naming & port registry → `EKSAD_DOMAIN_REGISTRY.md`
- Flyway DDL standards → `EKSAD_CODING_STANDARDS.md` §3
- Architecture principles → `EKSAD_BASE_PRINCIPLES.md` Principle #14
- Deployment environments → `EKSAD_DB_DEPLOYMENT_STRATEGY.md`
