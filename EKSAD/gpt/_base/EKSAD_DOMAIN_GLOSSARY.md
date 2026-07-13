# EKSAD Domain Glossary
# Technical & Business Terms Reference

**Version:** 1.2
**Date:** 2026-05-31
**Owner:** EKSAD Platform Team
**Audience:** Developers, Business Analysts, QA, Product Owners (via GPT Knowledge)

> This file is uploaded as a **Custom GPT knowledge file**.
> The GPT uses these definitions to give consistent, EKSAD-specific answers.

---

## Part A — Technical Terms

### A.1 Framework & Platform

| Term | Definition |
|------|------------|
| **Quarkus** | Java framework optimized for Kubernetes and cloud-native deployments. Compiles to fast-starting JVM JARs or native images (GraalVM). EKSAD standard framework, version `3.30.6`. |
| **Vert.x** | Reactive toolkit that Quarkus is built on. Provides the non-blocking event loop. Quarkus services run on Vert.x's event loop threads. |
| **CDI (Contexts and Dependency Injection)** | Jakarta EE standard for dependency injection. Quarkus uses Arc (CDI subset) for managing beans. |
| **`@ApplicationScoped`** | CDI scope — one bean instance per application lifetime. Standard scope for services and repositories in EKSAD. |
| **`@RequestScoped`** | CDI scope — one bean instance per HTTP request. Use for beans that carry per-request state. |
| **`@Singleton`** | CDI scope — single instance, eager initialization. Use only for truly stateless utilities. |
| **`@Inject`** | CDI annotation for dependency injection. |
| **Arc** | Quarkus's CDI implementation — a subset of the full CDI spec optimized for compile-time processing. |

---

### A.2 Reactive & Async

| Term | Definition |
|------|------------|
| **Reactive** | Programming paradigm where operations return streams or futures (non-blocking). In EKSAD, all DB and messaging operations are reactive. |
| **`Uni<T>`** | Mutiny type representing a single async result (0 or 1 item). Used for all CRUD operations. Similar to `CompletableFuture<T>`. |
| **`Multi<T>`** | Mutiny type representing an async stream of multiple items. Used for SSE, streaming queries. |
| **Mutiny** | SmallRye Mutiny — reactive library used by Quarkus. Provides `Uni`, `Multi`, and operators like `flatMap`, `map`, `onFailure`. |
| **`flatMap`** | Chains async operations — takes a result and returns a new `Uni`. Core pattern in reactive code. |
| **`@WithSession`** | Quarkus annotation on service class — ensures a Hibernate session is open for all methods in the class. Required for reactive Panache. |
| **`@ReactiveTransactional`** | Wraps a method in a reactive database transaction. Use on service methods, NOT repository methods. |
| **Event Loop** | Single-threaded non-blocking executor in Vert.x. Quarkus reactive code runs on it. Never block the event loop with synchronous I/O. |
| **Fire-and-Forget** | Sending a message without waiting for the result. Used for audit trail: `emitter.sendAndForget(payload)`. |
| **`MutinyEmitter<T>`** | SmallRye Reactive Messaging type for programmatically sending messages to a channel. Used in `LogHandler` to publish audit events. |

---

### A.3 Persistence

| Term | Definition |
|------|------------|
| **Panache** | Quarkus extension simplifying Hibernate ORM with the Repository pattern. `PanacheRepositoryBase<E, I>` is the base interface. |
| **Hibernate Reactive** | Reactive version of Hibernate ORM — all DB operations return `Uni`/`Multi` instead of blocking. |
| **`PanacheRepositoryBase<E, I>`** | Quarkus interface providing standard `persist()`, `findById()`, `delete()`, etc. as reactive methods. `E` = entity type, `I` = ID type. |
| **PostgreSQL** | Primary relational database for all EKSAD services. Each service has its own database (schema isolation). |
| **Reactive PG Client** | Quarkus extension for non-blocking PostgreSQL connection via `quarkus-reactive-pg-client`. |
| **Flyway** | Database schema migration tool. All DDL changes are in versioned SQL files (`V{N}__{description}.sql`). Never use `ddl-auto=update` in production. |
| **`ddl-auto=update`** | Hibernate setting that auto-modifies the DB schema to match entity classes. **FORBIDDEN in EKSAD production** — use Flyway instead. |
| **MongoDB** | NoSQL document database. Used exclusively by `eksad-core-audittrail` for storing audit logs. |
| **MongoDB Panache** | Quarkus extension for reactive MongoDB access. `MongoEntity` and `PanacheMongoRepositoryBase` are its core types. |
| **Soft Delete** | Pattern where records are never permanently removed. Instead, `deleted_at` (Long epoch ms) and `deleted_by` (String) are set. Queries must filter `WHERE deleted_at IS NULL`. |
| **`BaseEntity`** | EKSAD abstract superclass (in `eksad-core-common`) providing: `created_at`, `created_by`, `updated_at`, `updated_by`, `deleted_at`, `deleted_by`. All service entities extend this. |
| **`NUMERIC(20,4)`** | PostgreSQL type for financial amounts — 20 total digits, 4 decimal places. Maps to Java `BigDecimal`. **Always use this for money** — never `FLOAT`, `DOUBLE`, or `VARCHAR`. |
| **Epoch Milliseconds** | Timestamps stored as `BIGINT` (Java `Long`) representing milliseconds since Unix epoch (Jan 1, 1970 UTC). EKSAD standard for all `BaseEntity` timestamp columns. Fast B-tree indexing. |
| **`tenant_id`** | A `VARCHAR(100)` column on every entity that identifies which tenant owns the record. Sourced from JWT claim `eksad_tenant_id`. **Required on all tables.** |

---

### A.4 Messaging (RabbitMQ & Kafka)

| Term | Definition |
|------|------------|
| **RabbitMQ** | **Default** message broker for async communication between EKSAD services. |
| **Kafka** | **Opt-in** alternative broker (per service Stack Profile) for high-throughput event streaming / replayable log / many consumer groups, or when the owning team is Kafka-native. The event envelope is identical to RabbitMQ — only the transport differs. See `EKSAD_EVENT_CATALOG.md §11.2`. |
| **Exchange** | RabbitMQ component that receives messages and routes them to queues based on routing keys. EKSAD naming: `exc-{domain}` (e.g., `exc-log-activity`). |
| **Queue** | Stores messages until a consumer processes them. EKSAD naming: `q-{action}-{service}` (e.g., `q-log-activity-eksad`). |
| **Routing Key** | String that binds a queue to an exchange. EKSAD naming: `r.q-{action}-{service}` (e.g., `r.q-log-activity-eksad`). |
| **Binding** | The link between an exchange and a queue using a routing key. |
| **Direct Exchange** | Routes message to the queue whose binding key exactly matches the routing key. EKSAD default exchange type. |
| **Durable** | Queue/exchange property — survives RabbitMQ restart. All EKSAD queues and exchanges are durable. |
| **Dead Letter Queue (DLQ)** | A queue where messages go after failing processing. EKSAD naming: `q-dlq-{queue-name}`. |
| **Publisher Confirm** | RabbitMQ feature where the broker ACKs that a message was received. EKSAD enables this for reliability. |
| **SmallRye Reactive Messaging** | Quarkus extension for RabbitMQ **and** Kafka integration. `@Incoming` / `@Outgoing` annotations declare channels; the connector (`smallrye-rabbitmq` / `smallrye-kafka`) sets the transport. |
| **`@Incoming`** | Annotation on a method — triggers on every message arriving on the named channel. Used in `eksad-core-audittrail`'s `IncomingMessage`. |
| **`@Outgoing`** | Annotation to declare a message-producing method. Used via `@Channel` + `MutinyEmitter` in `LogHandler`. |
| **Virtual Host** | RabbitMQ namespace for isolating connections. EKSAD uses `eksad_vhost`. |
| **Topic (Kafka)** | Named, partitioned, append-only event stream — the Kafka analogue of a RabbitMQ exchange. EKSAD naming: `{purpose}` or `{domain}.{purpose}` (e.g., `log-activity`, `automotive.master-data`). |
| **Partition Key (Kafka)** | Record key that decides the partition → controls ordering. EKSAD default = `tenantId` (per-tenant ordering); use `{entity}Id` only when strict per-entity ordering is required. |
| **Consumer Group (Kafka)** | Set of consumers sharing partitions of a topic for parallel processing. EKSAD naming: `cg-{service}` (e.g., `cg-audittrail`). |
| **Dead Letter Topic (DLT)** | Kafka analogue of a DLQ — failed records routed to `{topic}.dlt`. Paired with a `{topic}.retry` topic for backoff. |
| **Dual-Ingress (Audit)** | `eksad-core-audittrail` consumes audit events from **both** RabbitMQ (always-on) and Kafka (opt-in, `AUDIT_KAFKA_ENABLED=true`, topic `log-activity`), de-duplicating by `eventId`. Audit producers always publish to RabbitMQ. |

---

### A.4b Stack Profiles

| Term | Definition |
|------|------------|
| **Stack Profile** | The per-service technology selection across **three independent axes** — Framework (Quarkus/Spring Boot) · Paradigm (Reactive/Imperative) · Broker (RabbitMQ/Kafka). Chosen by the System Analyst and recorded in the TSD §3.1. Default (unspecified) = Quarkus · Reactive · RabbitMQ. See `EKSAD_BASE_PRINCIPLES.md → Stack Profiles`. |
| **Tier-1 Profile** | Battle-tested, fully supported profiles — *Quarkus · Reactive · RabbitMQ* and *Spring Boot · Imperative · RabbitMQ*. Pick when unsure. |
| **Tier-2 Profile** | Any other valid combination (e.g., Quarkus · Imperative, Spring Boot · Reactive, any · Kafka). Permitted for scalability/team-familiarity; rationale documented in the TSD. |
| **Transport-Agnostic Envelope** | The shared event JSON envelope (`eventType`, `eventId`, `tenantId`, `occurredAt`, `payload`, …) that is **identical on RabbitMQ and Kafka** — only the transport binding differs, which is what lets mixed-profile services interoperate. |

---

### A.5 Security & Auth

| Term | Definition |
|------|------------|
| **JWT (JSON Web Token)** | Compact, self-contained token for transmitting claims between parties. EKSAD uses RS256-signed JWTs. |
| **RS256** | JWT signing algorithm using RSA with SHA-256. Uses a private key to sign, public key to verify. Auth service holds private key; all other services have public key only. |
| **Bearer Token** | HTTP authentication scheme: `Authorization: Bearer {jwt}`. Required header for all EKSAD API calls. |
| **SmallRye JWT** | Quarkus extension for JWT validation. Services declare `mp.jwt.verify.publickey.location` and validation is automatic. |
| **`@RolesAllowed`** | Jakarta EE annotation restricting endpoint access to specified roles. Maps to JWT `groups` claim. |
| **Access Token** | Short-lived JWT (24 hours in EKSAD) authorizing API access. |
| **Refresh Token** | Long-lived token (7 days) stored in `auth.refresh_token` table. Used to get a new access token. |
| **`eksad_tenant_id`** | Custom JWT claim carrying the caller's tenant identifier. Read by `UserContext.getTenantId()`. |
| **`eksad_role`** | Custom JWT claim carrying the caller's role code. Read by `UserContext.getRole()`. |
| **`eksad_permissions`** | Custom JWT claim carrying an array of permission strings (e.g., `SUBMISSION_READ`). |
| **Impersonation** | When an admin acts on behalf of another user. JWT carries both `sub` (acting user) and `original_user` claim. `UserContext.getAuditActor()` captures this as `"admin (impersonating user)"`. |
| **CORS** | Cross-Origin Resource Sharing — allows browsers to call APIs from different domains. EKSAD enables CORS on all services with configurable origins. |
| **`@PKCS8`** | Private key format required by SmallRye JWT. Convert with `openssl pkcs8` command. |

---

### A.6 Code Quality & Build

| Term | Definition |
|------|------------|
| **Lombok** | Java annotation processor that auto-generates boilerplate: `@Data`, `@Builder`, `@NoArgsConstructor`, `@AllArgsConstructor`, `@SuperBuilder`. EKSAD standard, version `1.18.32`. |
| **`@SuperBuilder`** | Lombok annotation enabling builder pattern for classes with inheritance (required for entities extending `BaseEntity`). |
| **`@MappedSuperclass`** | JPA annotation on `BaseEntity` — not an entity itself, but its fields are mapped to subclass tables. |
| **MapStruct** | Code generator for Java bean mappings. Generates compile-time mappers between DTOs and entities. EKSAD standard, version `1.5.5.Final`. |
| **`@Mapper`** | MapStruct annotation declaring a mapper interface. Quarkus CDI variant: `@Mapper(componentModel = "cdi")`. |
| **Maven** | Build tool for all EKSAD projects. Each service repo declares `eksad-parent` as its `<parent>` BOM. Services are **independent repos** — NOT a multi-module reactor. |
| **Nexus** | Self-hosted Maven artifact registry (Sprint 3+). Hosts `eksad-core-common`, `eksad-core-auth-client`, and `eksad-parent` as published artifacts. Sprint 1 uses **GitHub Packages** instead; migration requires only a `settings.xml` URL change. |
| **BOM (Bill of Materials)** | Maven POM (`<packaging>pom</packaging>`) that centralizes dependency versions. `eksad-parent` is EKSAD's BOM — pins Quarkus, Lombok, MapStruct, Jackson versions for all services. Services that declare it as `<parent>` inherit all version pins; no explicit `<version>` tags needed for managed dependencies. |
| **Artifact Registry** | Repository that stores and serves published Maven artifacts (JARs and POMs). EKSAD uses **GitHub Packages** (Sprint 1) → **Nexus** (Sprint 3+). Only libraries and the BOM are published here; service Docker images go to the container registry. |
| **GitHub Packages** | GitHub's package registry (`maven.pkg.github.com/eksad/`). Sprint 1 artifact registry for `eksad-parent`, `eksad-core-common`, `eksad-core-auth-client`. Free for public/private repos; authenticated via `GITHUB_TOKEN`. |
| **Model B (Repo Strategy)** | EKSAD's repo model: one Git repo per service, `eksad-parent` published as BOM, libraries published as JARs. Opposite of Model A (monorepo reactor). Enables independent CI/CD, independent deploy, team ownership. See `EKSAD_REPO_STRATEGY.md`. |
| **`-SNAPSHOT`** | Maven version suffix indicating work-in-progress. Published to Nexus snapshots repo. Remove for releases. Never use SNAPSHOT in production `pom.xml`.
| **Native Image** | GraalVM compilation of Java to a native executable — fast startup, low memory. Build with `mvn package -Pnative`. |
| **Testcontainers** | Java library for spinning up Docker containers in tests (e.g., PostgreSQL, RabbitMQ). Used in EKSAD integration tests. |
| **`@QuarkusTest`** | Quarkus annotation starting the full application context for integration tests. |

---

### A.7 EKSAD Libraries

| Term | Definition |
|------|------------|
| **`eksad-core-common`** | Maven library (`com.eksad.core:eksad-core-common`) providing: `BaseEntity`, `BaseRepository`, `CrudFlows`, `LogHandler`, `UserContext`, `UriResolver`, `LogActivityDTO`, `ValidationException`. All services depend on this. |
| **`eksad-core-audittrail`** | Standalone Quarkus microservice (`com.eksad.core:eksad-core-audittrail`) that receives audit events from RabbitMQ and persists them to MongoDB. |
| **`eksad-core-storage`** | Standalone Quarkus microservice (`com.eksad.core:eksad-core-storage`) providing all file upload, metadata management, CDN URL resolution, and thumbnail generation for the EKSAD platform. Runs on `:8090`. Domain services reference files only by `file_id`. |
| **`eksad-parent`** | Maven parent POM (`com.eksad.platform:eksad-parent`, `<packaging>pom</packaging>`) serving as the company BOM. All EKSAD services and libraries declare this as `<parent>`. **Model B only** — NOT a multi-module reactor. Published to Artifact Registry (GitHub Packages → Nexus). Services are built independently; never as modules inside `eksad-parent`. See `EKSAD_REPO_STRATEGY.md`. |
| **`CrudFlows<E,D,I>`** | Generic interface in `eksad-core-common` providing default `createFlow`, `updateFlow`, `deleteFlow`, `commandFlow` with built-in audit trail. `E`=entity, `D`=DTO, `I`=ID type. |
| **`BaseRepository<E,D,I>`** | Abstract class in `eksad-core-common` implementing `CrudFlows`. Inject this; extend it in each service. Provides `auditMutator()`, `softDeleteMutator()`, `currentUser()`. |
| **`LogHandler`** | Bean in `eksad-core-common` that builds and fires `LogActivityDTO` to RabbitMQ. Injected into `BaseRepository` automatically. |
| **`UserContext`** | Bean in `eksad-core-common` that reads `user`, `role`, `tenantId` from JWT. Injected into `BaseRepository`. |
| **`UriResolver`** | Bean in `eksad-core-common` that extracts the current request URI for audit logs. |
| **`LogActivityDTO`** | Shared DTO in `eksad-core-common` representing an audit log entry. Serialized to **snake_case JSON** and sent over RabbitMQ (or Kafka topic `log-activity` for Kafka-native producers). Carries both `tenant_id` and `company_id` (see below). See `EKSAD_EVENT_CATALOG.md §6`. |
| **`tenant_id` (audit)** | Top-level tenant identifier on every audit record — the **isolation key**; always present and always the audit query filter (prevents cross-tenant leakage, Principle #4). Sourced from the JWT `tenant_id` claim. |
| **`company_id` (audit)** | Optional **finer scope** on an audit record for the case where one tenant contains multiple companies (group of companies): same `tenant_id`, different `company_id`. Nullable; sourced from the JWT `company_id` claim. Kept as a **separate field** from `tenant_id` — never aliased. |
| **`data_changes`** | Consumer-computed JSON array on the audit document holding field-level diffs (`[{ attribute, before, after }]`). Computed by `eksad-core-audittrail` `LogActivityService` from `data_before` vs `data_after` via JSONAssert; CREATE/DELETE yield `[]`. Producers send `data_before`/`data_after` only (must be valid Jackson JSON, never `toString()`), never `data_changes`. |
| **`LogActivityDifferentDataDTO`** | DTO in `eksad-core-audittrail` representing one field-level change (`attribute`, `before`, `after`). The element type of the `data_changes` array. |
| **`ValidationException`** | EKSAD standard exception for business rule violations. HTTP 422. Used in `CrudFlows` guard failures. |
| **`StorageProvider`** | Internal interface in `eksad-core-storage` abstracting object storage operations (`upload`, `delete`, `buildCdnUrl`, `generateSignedUrl`). Two implementations: `AwsS3StorageProvider` and `CloudflareR2StorageProvider`. Selected via `STORAGE_PROVIDER` env var. |
| **`StorageModuleType`** | Java interface in `eksad-core-storage` declaring module type string constants for audit trail: `EKSAD_CORE_STORAGE.FILE.UPLOAD`, `EKSAD_CORE_STORAGE.FILE.DELETE`, `EKSAD_CORE_STORAGE.FILE.ACCESS` (reserved). |

### A.8 File Storage Terms

| Term | Definition |
|------|------------|
| **`file_id`** | A `BIGINT` stored in a domain service entity referencing a file record in `eksad-core-storage`. Domain services must never store raw S3 keys or CDN URLs — only `file_id`. Resolved to a URL by calling `GET /api/v1/storage/{fileId}/url` at render-time. |
| **File Visibility** | Every file uploaded to `eksad-core-storage` is classified as `PUBLIC` or `PRIVATE`. Controls bucket policy, CDN URL type, and thumbnail access. |
| **`PUBLIC` file** | A file accessible to anyone with the CDN URL. Stored in a public-read bucket. `cdn_url` is permanent and stored in `file_metadata`. Suitable for logos, brochures, public images. |
| **`PRIVATE` file** | A file requiring authentication to access. Stored in a private bucket. `cdn_url` is NOT stored — a signed short-lived URL is generated per request (TTL = `STORAGE_SIGNED_URL_TTL_SECONDS`). Suitable for contracts, reports, confidential documents. |
| **Signed URL** | A time-limited, tamper-proof URL granting temporary access to a PRIVATE file. Signed by the CDN (CloudFront signed URL or Cloudflare presigned URL). Expires after TTL. Frontend must not cache these URLs long-term. |
| **Thumbnail** | A compressed, smaller preview image of an uploaded file. Generated asynchronously after upload. Supported source types: PNG, JPG, GIF, WEBP (via Thumbnailator); PDF (via Apache PDFBox — renders page 1 to JPEG). Inherits the `visibility` of its parent file. Falls back to original file URL if generation fails. |
| **`thumbnail_status`** | Column in `file_metadata` tracking thumbnail generation lifecycle: `PENDING` → `READY` / `FAILED`. Also `SKIPPED` for unsupported file types. |
| **`confidential`** | Boolean flag in `file_metadata` (`default false`). Reserved for future enhancement — when `true`, access will emit an audit log event (`EKSAD_CORE_STORAGE.FILE.ACCESS`). Currently not enforced. |
| **`ref_entity_type`** | String stored in `file_metadata` indicating which domain entity owns the file (e.g., `contract`, `lead`, `submission`). Used for filtering and cross-referencing. |
| **`ref_entity_id`** | String stored in `file_metadata` containing the ID of the owning entity in the caller's domain service. |
| **`StorageProvider`** | Interface in `eksad-core-storage` abstracting the object storage backend. Implementations: `AwsS3StorageProvider` (AWS S3 + CloudFront) and `CloudflareR2StorageProvider` (Cloudflare R2 + CDN). Selected via `STORAGE_PROVIDER=aws\|cloudflare` env var. |
| **Thumbnailator** | Java library (`net.coobird:thumbnailator`) for high-quality image resizing and thumbnail generation. Used in `eksad-core-storage` for image thumbnails. |
| **Apache PDFBox** | Java library for reading and rendering PDF documents. Used in `eksad-core-storage` to render PDF page 1 to a JPEG thumbnail. |
| **`exc-file-processing`** | RabbitMQ exchange in `eksad-core-storage` for async thumbnail generation events. Queue: `q-generate-thumbnail-core-storage`. Routing key: `r.q-generate-thumbnail-core-storage`. |

---

## Part B — Business Terms

### B.1 Organizational Structure

| Term | Definition |
|------|------------|
| **EKSAD / PT EKSAD** | The company. Also referred to as "Eksad Group". The EKSAD platform is the company's internal engineering platform. |
| **Holding Company** | Parent company that owns stakes in multiple subsidiary companies. Uses consolidated financial reporting from all subsidiaries. |
| **Subsidiary (SubCo)** | A company owned or controlled by the holding company. Submits periodic financial reports to HQ. |
| **Business Unit (BU)** | A division or team within EKSAD that may have its own domain service (e.g., finance, HR, leads). |
| **Tenant** | In the EKSAD multi-tenant platform, each "tenant" is an independent organizational unit (a company, subsidiary, or business group) with fully isolated data. |

---

### B.2 Financial Domain (from TIA Reference Project)

| Term | Definition |
|------|------------|
| **TIA (Triputra Investment Authority)** | Headquarters function of Triputra Group responsible for collecting and analyzing financial reports from subsidiaries. Reference customer for EKSAD platform. |
| **Master Budget (MB)** | Annual budget plan submitted by a SubCo before the upcoming fiscal year. Covers all financial sub-reports. |
| **Monthly Report (MR)** | Actual financial results for the previous calendar month. Submitted monthly by each SubCo. |
| **Outlook PA (OPA)** | Performance Appraisal Outlook — annual performance targets and outlook. |
| **Rolling Outlook (RO)** | Quarterly rolling forecast — updated 3 times per year (Q1, Q2, Q3). |
| **Profit & Loss (PL)** | Financial statement showing revenue, expenses, and profit/loss over a period. |
| **Balance Sheet (BS)** | Financial statement showing assets, liabilities, and equity at a point in time. |
| **Tax Planning (TP)** | Forward-looking tax liability estimation and planning document. |
| **Fixed Assets Movement (FAM)** | Report tracking additions, disposals, and depreciation of fixed assets. |
| **Cash Flow (CF)** | Statement of cash inflows and outflows over a period. |
| **LOCF (List of Credit Facilities)** | Inventory of all credit lines, loans, and financing facilities. |
| **CAT (Corporate Annual Target)** | KPI targets set at the corporate level for the year. |
| **OI (Operating Indicator)** | Operational metrics and KPIs specific to the business unit. |
| **YTD (Year-to-Date)** | Accumulated value from the start of the fiscal year to the current month. Common calculation in financial reports. |
| **CAFRM** | Corporate Annual Financial Review Meeting — annual consolidated review session. In the TIA system, it's a dedicated bounded-context service. |

---

### B.3 Workflow & Process Terms

| Term | Definition |
|------|------------|
| **Approval Workflow** | Multi-step human review process where a record moves through states (DRAFT → SUBMITTED → APPROVED/REJECTED) via authorized actors. |
| **State Machine** | Formal model of a system with defined states, transitions, and guards. Used to model approval flows in EKSAD. |
| **Guard (in state machine)** | A condition that must be true for a state transition to be allowed. Example: "can only APPROVE if current status is SUBMITTED". |
| **Soft Delete** | Business policy that records are never permanently erased. `deleted_at` is stamped; deleted records are invisible to normal queries but recoverable by admins. |
| **Audit Trail** | Complete historical log of all operations performed on data — who did what, when, before/after values. Stored in MongoDB via `eksad-core-audittrail`. |
| **RBAC (Role-Based Access Control)** | Authorization model where permissions are assigned to roles, and users are assigned roles. EKSAD roles: `ROLE_SUPER_ADMIN`, `ROLE_ADMIN`, `ROLE_VIEWER`, plus domain-specific roles. |
| **Multi-Tenant** | Architecture where a single system serves multiple independent organizational units (tenants) with complete data isolation between them. |
| **SaaS (Software as a Service)** | Delivery model where software is hosted and provided as a service, often multi-tenant. The EKSAD platform is designed as a SaaS skeleton. |
| **White-label** | Product that can be re-branded and licensed to other organizations. EKSAD platform is designed to be white-labeled for clients. |
| **Idempotency** | Property of an operation that produces the same result regardless of how many times it is executed. Important for retry scenarios in event-driven systems. |

---

### B.4 API & Integration Terms

| Term | Definition |
|------|------------|
| **REST (Representational State Transfer)** | Architectural style for HTTP APIs using standard methods (GET, POST, PUT, PATCH, DELETE). EKSAD APIs are RESTful. |
| **OpenAPI / Swagger** | Standard for describing REST APIs. EKSAD exposes Swagger UI at `/q/swagger-ui` on every service. |
| **JSON-B** | Jakarta EE standard for Java ↔ JSON serialization. EKSAD uses JSON-B (not Jackson) with `@JsonbProperty` annotations. |
| **HTTP Status Codes** | Standard codes: 200 OK, 201 Created, 400 Bad Request, 401 Unauthorized, 403 Forbidden, 404 Not Found, 422 Unprocessable Entity, 500 Internal Server Error. |
| **Pagination** | Returning large result sets in pages. EKSAD APIs use `page` and `size` query parameters. |
| **DTO (Data Transfer Object)** | Object used to transfer data between layers (API ↔ Service ↔ Repository). Never expose entities directly from APIs. |
| **Mapper** | Class (generated by MapStruct) that converts between DTOs and entities. Lives in `core/mapper/` package. |
| **Request DTO** | DTO for incoming data (e.g., `{Entity}CreateDTO`, `{Entity}UpdateDTO`). |
| **Response DTO** | DTO for outgoing data (e.g., `{Entity}ResponseDTO`). May include computed fields not in the entity. |
| **Module Type** | EKSAD-specific string identifying the source of an audit event. Format: `<PROJECT>.<MODULE>.<ACTION>`. Example: `EKSAD_SVC_LEADS.TRANSACTION.CREATE`. |

---

### A.9 Master Data & Cache Sync

| Term | Definition |
|------|------------|
| **Master Data** | Shared catalog/reference entities (brands, models, types, departments, positions, etc.) used by multiple domain services. Owned exclusively by `svc-master-data`. NOT inventory/stock data. |
| **Master Data Service** | Dedicated Quarkus microservice (`svc-master-data`) that is the single source of truth for all master data entities within a domain. Other services consume via events. |
| **Denormalized Cache** | A local read-only copy of master data maintained in each domain service's database. Populated via RabbitMQ events. Enables local JOINs without cross-service API calls. |
| **Cache Table** | Database table (e.g., `brand_cache`, `model_cache`, `department_cache`) storing denormalized copies of master data in a domain service. Includes `last_synced_at` for event ordering. |
| **Cache Sync** | The process of keeping denormalized cache tables up-to-date via event consumption from `exc-{domain}-master-data`. |
| **Startup Sync** | On service startup, if cache tables are empty, perform a full sync from `svc-master-data` REST API before accepting traffic. |
| **Topic Exchange** | RabbitMQ exchange type that routes messages based on routing-key patterns (wildcards). Used by `exc-{domain}-master-data` for flexible event routing. |
| **Stale Event** | An event whose `occurredAt` timestamp is older than the cache's `last_synced_at`. Must be skipped to prevent data regression. |

---

### A.10 CQRS & Event Patterns (Future — Sprint 4+)

| Term | Definition |
|------|------------|
| **CQRS** | Command Query Responsibility Segregation — pattern that separates write models (commands) from read models (queries). Planned for EKSAD Sprint 4+. |
| **Domain Event** | A typed, semantic business event published by a domain service after a state change. Different from audit events (generic dataBefore/dataAfter). |
| **Read Model** | A denormalized, query-optimized database/table populated by consuming domain events. Used for dashboards and cross-service reporting. |
| **Projection** | The process of building a read model by consuming and transforming domain events into denormalized rows. |
| **Eventual Consistency** | Data state where read models may lag behind write models by a short time window. Acceptable for dashboards; not acceptable for transactional operations. |
| **Event Sourcing** | Pattern where state is derived from replaying all events. NOT used in EKSAD — too complex for current needs. EKSAD uses CQRS with state-based storage instead. |

---

### A.11 Multi-Tenancy & Auth Infrastructure

| Term | Definition |
|------|------------|
| **`eksad-core-auth`** | Core infrastructure service for credential storage, JWT signing (RS256), token refresh/revoke, JWKS endpoint. PostgreSQL-backed. Internal API only except JWKS. |
| **`svc-user-management`** | Service handling user CRUD, RBAC, roles/permissions, JWT claim packaging. MongoDB-backed. Calls `eksad-core-auth` via SDK. |
| **`svc-tenant-management`** | Service managing tenant registry, N-level hierarchy (materialized path), config inheritance, provisioning. MongoDB-backed. |
| **`eksad-core-auth-client`** | Java Maven library wrapping `eksad-core-auth` internal API. Used by user-management services and external project adapters. |
| **JWKS** | JSON Web Key Set — RFC 7517 standard endpoint (`/.well-known/jwks.json`) exposing public keys for JWT signature verification. |
| **Materialized Path** | Tree-storage pattern using a `path` string field (e.g., `/tenant-astra/tenant-ahm`) for efficient hierarchy queries. |
| **Config Inheritance** | Child tenant inherits all config from parent unless explicitly overridden. Resolution: child > parent > grandparent > platform defaults. |
| **Tenant Context** | CDI `@RequestScoped` bean holding `tenant_id`, `scope`, `path` for the current request. Populated by `TenantContextFilter` from JWT claims. |
| **Scope (auth)** | Access level encoded in JWT: `platform` (all tenants), `group` (descendants of one tenant), `tenant` (single tenant). |
| **Reserved Field** | Pre-allocated column in a transactional entity table (5 string + 3 numeric + 2 date + 2 boolean + 1 JSONB) that can be mapped to a tenant-specific custom field via `reserved_field_config`. |
| **`BaseTransactionalEntity`** | Subclass of `BaseEntity` adding 13 reserved field columns. Used by transactional entities that opt-in to reserved fields. |

---

### A.12 Resilience & Observability

| Term | Definition |
|------|------------|
| **Correlation ID** | UUID propagated across services via `X-Correlation-ID` HTTP header and RabbitMQ message headers. Enables end-to-end request tracing through logs. |
| **MDC (Mapped Diagnostic Context)** | Per-thread / per-request key-value store used by logging frameworks. EKSAD populates `correlation_id`, `tenant_id`, `user_ref`. |
| **Distributed Tracing** | Capturing spans across multiple services to visualize request flow. EKSAD uses OpenTelemetry → Jaeger (Sprint 2+). |
| **Circuit Breaker** | Resilience pattern that stops calls to a failing dependency after a failure threshold. States: CLOSED → OPEN → HALF_OPEN. |
| **Bulkhead** | Resilience pattern that isolates resource pools (e.g., max 5 concurrent calls to a slow REST client) to prevent cascading failure. |
| **Dead Letter Queue (DLQ)** | RabbitMQ queue that captures messages which failed processing after maximum retries. Allows post-mortem investigation without losing data. |
