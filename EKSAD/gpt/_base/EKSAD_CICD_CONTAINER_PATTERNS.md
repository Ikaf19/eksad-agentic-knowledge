# EKSAD CI/CD & Container Patterns

**Version:** 1.0
**Date:** 2026-05-23
**Owner:** EKSAD Platform Team
**Audience:** Developers, DevOps, Architects (via GPT Knowledge)
**Priority:** 🟢 P2
**Related:** `EKSAD_DB_DEPLOYMENT_STRATEGY.md`, `EKSAD_OBSERVABILITY_PATTERNS.md`, `EKSAD_RESILIENCE_PATTERNS.md`

> Universal CI/CD + container conventions for every EKSAD service (Quarkus primary, Spring Boot alternative).

---

## Table of Contents

1. [Deployment Architecture Overview](#1-deployment-architecture-overview)
2. [Dockerfile — Quarkus (Primary)](#2-dockerfile--quarkus-primary)
3. [Dockerfile — Spring Boot (Alternative)](#3-dockerfile--spring-boot-alternative)
4. [docker-compose — Local Development](#4-docker-compose--local-development)
5. [Environment Configuration — 3 Profiles](#5-environment-configuration--3-profiles)
6. [Jenkins Pipeline](#6-jenkins-pipeline)
7. [Kubernetes Manifests](#7-kubernetes-manifests)
8. [Container Registry Migration](#8-container-registry-migration)
9. [Multi-Service Dev Workflow](#9-multi-service-dev-workflow)
10. [Image Versioning & Tagging](#10-image-versioning--tagging)
11. [Secrets Management](#11-secrets-management)
12. [Spring Boot Specifics](#12-spring-boot-specifics)

---

## 1. Deployment Architecture Overview

| Stage | Platform | Topology |
|-------|----------|----------|
| **Dev** | docker-compose (developer laptop) | All services + infra in one compose file |
| **Staging** | Kubernetes — shared namespace `eksad-staging` | One Deployment per service |
| **Production** | Kubernetes — namespace per tenant group (future) | HPA, Ingress, TLS |
| **CI/CD** | Jenkins (declarative pipeline) | One `Jenkinsfile` per service |
| **Registry** | Sprint 1 → Docker Hub. Sprint 3+ → Harbor (self-hosted) | OCI standard |

Both Quarkus and Spring Boot services share the same K8s manifest pattern; only the Dockerfile and probe paths differ.

---

## 2. Dockerfile — Quarkus (Primary)

### 2.1 Mode Selection

| Mode | Image | Startup | When |
|------|-------|--------:|------|
| **JVM (Sprint 1)** | `eclipse-temurin:21-jre-alpine` ~200 MB | 2–3 s | Default — simpler debug, faster build |
| Native (Sprint 5+) | distroless ~50 MB | ~50 ms | Serverless, fast auto-scale; longer build |

### 2.2 JVM Multi-Stage Template

```dockerfile
# syntax=docker/dockerfile:1.7
FROM maven:3.9-eclipse-temurin-21 AS build
WORKDIR /app
COPY pom.xml .
RUN --mount=type=cache,target=/root/.m2 mvn -B dependency:go-offline
COPY src ./src
RUN --mount=type=cache,target=/root/.m2 mvn -B package -DskipTests

FROM eclipse-temurin:21-jre-alpine
LABEL org.opencontainers.image.title="svc-pipeline" \
      org.opencontainers.image.source="https://github.com/eksad/svc-pipeline"
WORKDIR /app
COPY --from=build /app/target/quarkus-app /app
EXPOSE 8082
HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
  CMD wget -qO- http://localhost:8082/q/health/live || exit 1
ENTRYPOINT ["java", "-jar", "quarkus-run.jar"]
```

`.dockerignore`:

```
target/
.git/
*.md
.env
.idea/
```

---

## 3. Dockerfile — Spring Boot (Alternative)

```dockerfile
FROM maven:3.9-eclipse-temurin-21 AS build
WORKDIR /app
COPY pom.xml .
RUN --mount=type=cache,target=/root/.m2 mvn -B dependency:go-offline
COPY src ./src
RUN --mount=type=cache,target=/root/.m2 mvn -B package -DskipTests

FROM eclipse-temurin:21-jre-alpine
WORKDIR /app
COPY --from=build /app/target/*.jar app.jar
EXPOSE 8082
HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
  CMD wget -qO- http://localhost:8082/actuator/health || exit 1
ENTRYPOINT ["java", "-jar", "app.jar"]
```

**Alternative:** Jib (no Dockerfile) — `mvn compile jib:dockerBuild -Dimage=eksad/svc-pipeline:latest`.

---

## 4. docker-compose — Local Development

```yaml
version: "3.9"
services:
  # ── Infrastructure ────────────────────────────────────────
  postgres:
    image: postgres:16-alpine
    ports: ["5432:5432"]
    volumes: ["./init-databases.sql:/docker-entrypoint-initdb.d/init.sql"]
    environment: { POSTGRES_PASSWORD: eksad }
  mongodb:
    image: mongo:7
    ports: ["27017:27017"]
  rabbitmq:
    image: rabbitmq:3-management-alpine
    ports: ["5672:5672", "15672:15672"]

  # ── Observability (profile: observability) ────────────────
  jaeger:
    image: jaegertracing/all-in-one:latest
    ports: ["16686:16686", "4317:4317"]
    profiles: [observability]
  prometheus:
    image: prom/prometheus:latest
    ports: ["9090:9090"]
    volumes: ["./prometheus.yml:/etc/prometheus/prometheus.yml"]
    profiles: [observability]
  grafana:
    image: grafana/grafana:latest
    ports: ["3001:3000"]
    profiles: [observability]

  # ── Core services (profile: full) ─────────────────────────
  eksad-core-auth:
    build: ./eksad-core-auth
    ports: ["8090:8090"]
    depends_on: [postgres]
    env_file: [.env]
    profiles: [full]
  svc-user-management:
    build: ./svc-user-management
    ports: ["8087:8087"]
    depends_on: [mongodb, eksad-core-auth]
    profiles: [full]
  svc-tenant-management:
    build: ./svc-tenant-management
    ports: ["8091:8091"]
    depends_on: [mongodb]
    profiles: [full]
  svc-master-data:
    build: ./svc-master-data
    ports: ["8086:8086"]
    depends_on: [postgres, rabbitmq]
    profiles: [full]

  # ── Domain services (profile: full) ───────────────────────
  svc-pipeline:
    build: ./svc-pipeline
    ports: ["8082:8082"]
    depends_on: [postgres, rabbitmq, svc-master-data]
    profiles: [full]
```

`init-databases.sql` mirrors `EKSAD_DB_DEPLOYMENT_STRATEGY.md` — one `CREATE DATABASE` + `CREATE USER` per service.

Usage:

```bash
docker compose up                          # infra only
docker compose --profile full up           # infra + all services
docker compose --profile observability up  # infra + monitoring stack
```

---

## 5. Environment Configuration — 3 Profiles

| Profile | DB Host | TLS | Logging | Config Source |
|---------|---------|-----|---------|--------------|
| **dev** (compose) | `localhost:5432` | none | human-readable | `application-dev.properties` / `%dev` |
| **staging** (K8s) | `postgres.eksad-staging.svc.cluster.local` | service-to-service TLS | JSON structured | ConfigMap + Secret |
| **prod** (K8s) | dedicated PG / managed (RDS/CloudSQL) | TLS + optional mTLS | JSON → Loki | Secret from Vault / external-secrets |

### 5.1 Standard Env Vars (every service)

```
DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD
MONGODB_URI                       # mongo-backed services only
RABBITMQ_HOST, RABBITMQ_PORT, RABBITMQ_USER, RABBITMQ_PASSWORD
EKSAD_CORE_AUTH_URL               # SDK consumers
EKSAD_AUTH_SIGNING_KEY_SECRET     # core-auth only
EKSAD_AUTH_ACCESS_TOKEN_LIFETIME_MINUTES
EKSAD_AUTH_REFRESH_TOKEN_LIFETIME_DAYS
EKSAD_AUTH_MAX_SESSIONS
EKSAD_SERVICE_NAME                # observability
OTEL_EXPORTER_OTLP_ENDPOINT       # Jaeger / OTEL (Sprint 2+)
```

---

## 6. Jenkins Pipeline

### 6.1 Declarative `Jenkinsfile` Template

```groovy
pipeline {
  agent { docker { image 'maven:3.9-eclipse-temurin-21' } }

  environment {
    DOCKER_REGISTRY = 'docker.io/eksad'
    SERVICE_NAME    = 'svc-pipeline'
    VERSION         = "${env.BUILD_NUMBER}"
  }

  stages {
    stage('Checkout')         { steps { checkout scm } }
    stage('Build')            { steps { sh 'mvn -B package -DskipTests' } }
    stage('Unit Test')        { steps { sh 'mvn -B test' } }
    stage('Integration Test') { steps { sh 'mvn -B verify -Pintegration-test' } }

    stage('Security Scan') {
      steps { sh 'mvn -B org.owasp:dependency-check-maven:check' }
      // Add `trivy image` after Docker build for image-level scan
    }

    stage('Docker Build') {
      steps {
        sh "docker build -t ${DOCKER_REGISTRY}/${SERVICE_NAME}:${VERSION} ."
        sh "docker tag  ${DOCKER_REGISTRY}/${SERVICE_NAME}:${VERSION} ${DOCKER_REGISTRY}/${SERVICE_NAME}:latest"
      }
    }

    stage('Docker Push') {
      steps {
        withCredentials([usernamePassword(credentialsId: 'docker-registry',
                                          usernameVariable: 'U', passwordVariable: 'P')]) {
          sh 'echo $P | docker login -u $U --password-stdin'
          sh "docker push ${DOCKER_REGISTRY}/${SERVICE_NAME}:${VERSION}"
          sh "docker push ${DOCKER_REGISTRY}/${SERVICE_NAME}:latest"
        }
      }
    }

    stage('Deploy Dev')     { when { branch 'develop'    } steps { sh 'kubectl apply -k k8s/overlays/dev'     } }
    stage('Deploy Staging') { when { branch 'release/*'  } input { message 'Deploy to staging?' }
                              steps { sh 'kubectl apply -k k8s/overlays/staging' } }
    stage('Deploy Prod')    { when { branch 'main'       } input { message 'Deploy to prod?' submitter 'admin' }
                              steps { sh 'kubectl apply -k k8s/overlays/prod' } }
  }

  post {
    always  { junit '**/target/surefire-reports/*.xml' }
    failure { slackSend channel: '#eksad-ci', message: "❌ BUILD FAILED: ${SERVICE_NAME}#${VERSION}" }
    success { slackSend channel: '#eksad-ci', message: "✅ ${SERVICE_NAME}:${VERSION} deployed" }
  }
}
```

### 6.2 Branch Strategy

| Branch | Target | Gate |
|--------|--------|------|
| `develop` | Dev cluster | auto |
| `release/*` | Staging | manual `input` |
| `main` | Production | manual `input` with `submitter` |

Each service has its own independent pipeline — services version independently.

### 6.3 Shared Library

`eksad-jenkins-shared-lib` — reusable steps (`eksadBuild()`, `eksadDockerPush()`, `eksadDeployK8s(env)`).

---

## 7. Kubernetes Manifests

### 7.1 Kustomize Layout

```
k8s/
  base/
    deployment.yaml
    service.yaml
    configmap.yaml
    hpa.yaml
  overlays/
    dev/        { kustomization.yaml, configmap-patch.yaml }
    staging/    { kustomization.yaml, secret.yaml }
    prod/       { kustomization.yaml, secret.yaml, ingress.yaml }
```

### 7.2 Deployment Template

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: svc-pipeline
  labels: { app: svc-pipeline, tier: domain }
spec:
  replicas: 2              # 3 in prod overlay
  strategy:
    type: RollingUpdate
    rollingUpdate: { maxSurge: 1, maxUnavailable: 0 }
  selector: { matchLabels: { app: svc-pipeline } }
  template:
    metadata: { labels: { app: svc-pipeline } }
    spec:
      containers:
        - name: svc-pipeline
          image: eksad/svc-pipeline:1.0.0   # never `:latest` in prod
          ports: [{ containerPort: 8082 }]
          envFrom: [{ configMapRef: { name: svc-pipeline-config } }]
          env:
            - name: DB_PASSWORD
              valueFrom: { secretKeyRef: { name: svc-pipeline-secret, key: db-password } }
          resources:
            requests: { cpu: 250m, memory: 256Mi }
            limits:   { cpu: 1000m, memory: 512Mi }
          livenessProbe:
            httpGet: { path: /q/health/live, port: 8082 }
            initialDelaySeconds: 15
            periodSeconds: 30
          readinessProbe:
            httpGet: { path: /q/health/ready, port: 8082 }
            initialDelaySeconds: 10
            periodSeconds: 10
```

### 7.3 HPA

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata: { name: svc-pipeline-hpa }
spec:
  scaleTargetRef: { apiVersion: apps/v1, kind: Deployment, name: svc-pipeline }
  minReplicas: 2
  maxReplicas: 10
  metrics:
    - type: Resource
      resource: { name: cpu,    target: { type: Utilization, averageUtilization: 70 } }
    - type: Resource
      resource: { name: memory, target: { type: Utilization, averageUtilization: 80 } }
```

### 7.4 Ingress (prod overlay)

Host `api.eksad.{tenant-domain}` → TLS via cert-manager + Let's Encrypt → paths `/api/v1/{service}/*` routed to ClusterIP services.

### 7.5 Namespace Strategy

- `eksad-dev`, `eksad-staging`, `eksad-prod`
- Future: `eksad-{tenant-group}` for dedicated isolation per major tenant

---

## 8. Container Registry Migration

| Sprint | Registry | Notes |
|--------|----------|-------|
| 1 | Docker Hub (`docker.io/eksad`) | Free tier, rate-limited pulls, good enough for dev/staging |
| 3+ | Harbor (self-hosted on K8s) | No rate limits, built-in Trivy scan, RBAC per project, audit log, air-gap support |

**Migration steps:** retag images → update `DOCKER_REGISTRY` in `Jenkinsfile` → update K8s `image:` references → keep Docker Hub mirror during transition for rollback.

---

## 9. Multi-Service Dev Workflow

| Component | How to run locally |
|-----------|--------------------|
| Infra (PG/Mongo/RMQ) | `docker compose up` (default profile) |
| YOUR service | IDE — Quarkus `mvn quarkus:dev` (hot reload) |
| `svc-master-data` | WireMock container OR `docker compose --profile full up svc-master-data` |
| `eksad-core-auth` | WireMock via `CoreAuthWireMockSetup` (from SDK test utils) OR run locally |
| Other domain services | Usually not needed — services are independent |

### 9.1 Port Map (canonical)

```
PostgreSQL : 5432       MongoDB  : 27017       RabbitMQ : 5672 / 15672
core-auth  : 8090       user-mgmt: 8087        tenant-mgmt : 8091
master-data: 8086       gateway  : 8080
domain svc : 8082–8085  (project-specific — see EKSAD_DOMAIN_REGISTRY.md)
Jaeger UI  : 16686      Prometheus: 9090       Grafana  : 3001
```

---

## 10. Image Versioning & Tagging

- Format: `{registry}/{service}:{semver}-{build}` → e.g. `eksad/svc-pipeline:1.0.0-42`
- `:latest` only on `develop` branch builds — **never** referenced from prod manifests
- Per-branch:
  - `develop` → `:latest`
  - `release/1.2` → `:1.2.0-rc.{build}`
  - `main` → `:1.2.0`
- Semantic versioning per service — services are versioned independently

---

## 11. Secrets Management

| Stage | Storage | Tooling |
|-------|---------|---------|
| Dev | `.env` file (gitignored) | docker-compose `env_file` |
| Staging | K8s `Secret` | sealed-secrets controller |
| Prod | K8s `Secret` | external-secrets-operator → HashiCorp Vault |

**Hard rules:**
1. NEVER commit secrets to Git
2. NEVER put secrets in a `ConfigMap` — use `Secret`
3. NEVER log secrets (see `EKSAD_OBSERVABILITY_PATTERNS.md` redaction rules)
4. Jenkins credentials store for Docker registry + kubeconfig — referenced via `withCredentials`

---

## 12. Spring Boot Specifics

| Concern | Spring Boot Variant |
|---------|---------------------|
| Dockerfile | Use layered JAR extraction (`jarmode=layertools`) for better cache; or Jib |
| Health probes | `/actuator/health/liveness`, `/actuator/health/readiness` |
| K8s probes | Adjust paths from `/q/health/*` → `/actuator/health/*` |
| Build image | `mvn spring-boot:build-image` (Buildpack) |
| Config | `application-{profile}.yml` instead of Quarkus `%profile.*` |
| Devtools | `spring-boot-devtools` for auto-restart |

---

## Cross-References

- DB provisioning per service → `EKSAD_DB_DEPLOYMENT_STRATEGY.md`
- Health check internals → `EKSAD_RESILIENCE_PATTERNS.md` §8
- Logging / tracing exporter config → `EKSAD_OBSERVABILITY_PATTERNS.md`
- Test container setup mirrored from compose → `EKSAD_TESTING_GUIDE.md` §22
- Port allocation & service registry → `EKSAD_DOMAIN_REGISTRY.md`
