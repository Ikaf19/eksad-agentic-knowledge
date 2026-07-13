# EKSAD Core Auth Patterns

| Meta | Value |
|------|-------|
| **Version** | 1.3 |
| **Date** | 2026-05-31 |
| **Owner** | EKSAD Platform Team |
| **Audience** | ALL (Developers, Architects, SA, AI/Claude) |
| **Priority** | 🔴 P0 — Core infrastructure pattern |
| **Related** | Decisions 11, 12, 13; `EKSAD_CORE_AUTH_CLIENT_SDK.md` (T-24); `EKSAD_MULTI_TENANCY_PATTERNS.md` (T-20) |

---

## Table of Contents

1. [Overview — Auth as Core Infrastructure](#1-overview--auth-as-core-infrastructure)
2. [Architecture — Core Auth + User Management Split](#2-architecture--core-auth--user-management-split)
3. [Core Auth Internal API](#3-core-auth-internal-api)
4. [Core Auth Database Schema (PostgreSQL)](#4-core-auth-database-schema-postgresql--eksad_core_auth)
5. [JWT Signing & JWKS](#5-jwt-signing--jwks)
6. [`eksad-core-auth-client` SDK](#6-eksad-core-auth-client-sdk-overview)
7. [Multi-Project Auth Adapter Pattern](#7-multi-project-auth-adapter-pattern)
8. [User Management Patterns (`svc-user-management`)](#8-user-management-patterns-svc-user-management)
9. [Login Flow (Step-by-step)](#9-login-flow-step-by-step)
10. [Per-Service JWT Validation (Gateway Optional)](#10-per-service-jwt-validation-gateway-optional)
11. [Security Hardening](#11-security-hardening)
12. [Testing](#12-testing)
13. [Browser-Facing Cookie Token API (`CookieTokenResource`)](#13-browser-facing-cookie-token-api-cookietokenresource)

---

## 1. Overview — Auth as Core Infrastructure

- `eksad-core-auth` is **CORE infrastructure**, not a service — same tier as `eksad-core-audittrail` and `eksad-core-storage`.
- **Invisible to business users** — they never interact with it directly. Only `svc-user-management` (or equivalent) talks to it.
- **Split of concern:**
  - `eksad-core-auth` → credentials / tokens / signing keys
  - `svc-user-management` → users / roles / profiles / JWT claim packaging
- The 3-tier naming model applies: `eksad-core-auth` is **FIXED, never renamed**.

```
┌────────────────────────────────────────────────────────────────┐
│                      EKSAD PLATFORM                            │
│                                                                │
│  Public Layer (frontend / gateway)                             │
│  ┌──────────────────────┐                                      │
│  │ svc-user-management  │ ◄── Business users / login UI        │
│  └─────────┬────────────┘                                      │
│            │ (internal SDK calls)                              │
│  ┌─────────▼────────────┐                                      │
│  │   eksad-core-auth    │ ◄── Internal only (except JWKS)      │
│  │   (PostgreSQL)       │                                      │
│  └──────────────────────┘                                      │
│            │                                                   │
│            ▼  GET /.well-known/jwks.json (public)              │
│  ┌──────────────────────┐                                      │
│  │  All domain services │ ◄── validate JWT via JWKS            │
│  └──────────────────────┘                                      │
└────────────────────────────────────────────────────────────────┘
```

---

## 2. Architecture — Core Auth + User Management Split

| Service | Port | Database | Responsibility |
|---------|------|----------|----------------|
| `eksad-core-auth` | :8090 | PostgreSQL (`eksad_core_auth`) | Credential storage, JWT signing (RS256), token lifecycle, JWKS |
| `svc-user-management` | :8087 | MongoDB (`eksad_users`) | User CRUD, RBAC, roles/permissions, JWT claim packaging, domain profiles |

- `user_ref` is **opaque** — core-auth stores credential hash, doesn't know user details.
- Communication: **internal network only**, via `eksad-core-auth-client` SDK.
- Private signing key lives **exclusively** in core-auth — no other service holds it.

---

## 3. Core Auth Internal API

> All `/internal/*` endpoints are **NOT exposed via the gateway**. Auth between services uses internal network trust (no JWT needed for internal calls).

| Method | Path | Purpose |
|--------|------|---------|
| `POST` | `/internal/core-auth/credentials` | Register credential (called by user-mgmt on user create) |
| `POST` | `/internal/core-auth/validate` | Validate credential (called by user-mgmt on login) |
| `POST` | `/internal/core-auth/token/issue` | Issue JWT with claims from user-mgmt (server-to-server, trusted) |
| `POST` | `/internal/core-auth/token/refresh` | Refresh token (server-to-server, token in body) |
| `POST` | `/internal/core-auth/token/revoke` | Logout — current session, device, or all (server-to-server) |
| `GET`  | `/.well-known/jwks.json` | **Public** JWKS endpoint (RFC 7517) |
| `POST` | `/internal/core-auth/cookie/login` | **Browser** — validate password + issue both tokens as HTTP-only cookies |
| `POST` | `/internal/core-auth/cookie/issue` | **Browser (backend-proxied)** — trusted issue, sets cookies (no password check) |
| `POST` | `/internal/core-auth/cookie/refresh` | **Browser** — rotate tokens via `eksad_rt` cookie (no body needed) |
| `POST` | `/internal/core-auth/cookie/revoke` | **Browser** — revoke session, clear both cookies (`Max-Age=0`) |

> **Two API modes — choose by caller:**
> - Server-to-server (svc-user-management SDK): `/internal/core-auth/token/*` — tokens returned in response body.
> - Browser-direct: `/internal/core-auth/cookie/*` — tokens delivered as HTTP-only cookies, **never in body**.

### Request/Response Schemas

**Register credential**
- Request: `{ user_ref, provider_source, credential_value }`
- Response: `{ credential_id, created_at }`

**Validate credential**
- Request: `{ user_ref, provider_source, credential_value }`
- Response: `{ valid: boolean, lockout_info?: { locked, locked_until, failed_attempts, max_attempts } }`

**Issue token**
- Request: `{ user_ref, claims: { tenant_id, roles, permissions, domain_profile, ... }, device_info? }`
- Response: `{ access_token, refresh_token, expires_in, token_type: "Bearer" }`

**Refresh token**
- Request: `{ refresh_token }`
- Response: `{ access_token, refresh_token, expires_in }`

**Revoke token**
- Request: `{ refresh_token, revoke_all?: boolean }`
- Response: `{ revoked: true }`

---

## 4. Core Auth Database Schema (PostgreSQL — `eksad_core_auth`)

### `credentials`
```sql
CREATE TABLE credentials (
    id                       UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id                VARCHAR(100) NOT NULL,
    user_ref                 TEXT         NOT NULL,
    provider_source          TEXT         NOT NULL,   -- 'local','ldap','oauth2','saml'
    credential_hash          TEXT         NOT NULL,
    salt                     TEXT,
    algorithm                TEXT         NOT NULL DEFAULT 'bcrypt',
    failed_attempts          INTEGER      NOT NULL DEFAULT 0,
    locked_until             BIGINT,
    created_at               BIGINT       NOT NULL,
    updated_at               BIGINT,
    UNIQUE(user_ref, provider_source)
);
CREATE INDEX idx_credentials_tenant ON credentials (tenant_id);
CREATE INDEX idx_credentials_user_ref ON credentials (user_ref);
```

### `signing_keys`
```sql
CREATE TABLE signing_keys (
    id                       UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    kid                      TEXT UNIQUE  NOT NULL,
    algorithm                TEXT         NOT NULL DEFAULT 'RS256',
    public_key               TEXT         NOT NULL,
    private_key_encrypted    TEXT         NOT NULL,   -- AES-256 encrypted
    is_active                BOOLEAN      NOT NULL DEFAULT true,
    created_at               BIGINT       NOT NULL,
    expires_at               BIGINT
);
```
> Only **ONE active key** at a time; inactive keys stay for JWKS validation until expired.

### `refresh_tokens`
```sql
CREATE TABLE refresh_tokens (
    id                       UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id                VARCHAR(100) NOT NULL,
    token_hash               TEXT UNIQUE  NOT NULL,   -- BCrypt hash
    user_ref                 TEXT         NOT NULL,
    device_id                TEXT         NOT NULL,
    device_name              TEXT,
    device_type              TEXT,                    -- web | mobile | tablet | desktop
    ip_address               TEXT,
    issued_at                BIGINT       NOT NULL,
    expires_at               BIGINT       NOT NULL,
    last_used_at             BIGINT,
    revoked_at               BIGINT,
    revoked_by               TEXT                     -- user | admin | password_change | session_limit | system
);
CREATE INDEX idx_refresh_tokens_user ON refresh_tokens (user_ref);
CREATE INDEX idx_refresh_tokens_tenant ON refresh_tokens (tenant_id);
```

### `auth_events`
```sql
CREATE TABLE auth_events (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id       VARCHAR(100) NOT NULL,
    user_ref        TEXT         NOT NULL,
    event_type      TEXT         NOT NULL,    -- LOGIN_SUCCESS|LOGIN_FAILED|TOKEN_REFRESH|TOKEN_REVOKE|LOCKOUT|...
    ip_address      TEXT,
    device_info     TEXT,
    occurred_at     BIGINT       NOT NULL
);
CREATE INDEX idx_auth_events_user_ref ON auth_events (user_ref, occurred_at);
CREATE INDEX idx_auth_events_tenant ON auth_events (tenant_id);
```
> `auth_events` is **separate** from the business audit trail (`eksad-core-audittrail`).

---

## 5. JWT Signing & JWKS

- **RS256 (asymmetric)** — private key exclusively in core-auth.
- No other service holds the private key — **ever**.

### Key Rotation Workflow
1. Generate new RS256 key pair with new `kid`.
2. Set new key `is_active = true`.
3. Set old key `is_active = false` (keep in `signing_keys`).
4. JWKS endpoint returns **all non-expired keys** (old + new).
5. After old key's `expires_at` passes, remove from JWKS.

### JWT Claims Structure
```json
{
  "sub": "<user_ref>",
  "tenant_id": "tenant-ahm",
  "scope": "tenant",
  "roles": ["TENANT_ADMIN"],
  "permissions": ["pipeline:create", "pipeline:read"],
  "domain_profile": { "branch_id": "br-001" },
  "iss": "eksad-core-auth",
  "iat": 1745280000,
  "exp": 1745283600,
  "kid": "key-2026-05"
}
```
> Claims are **provided by user-management** — core-auth just signs them.

---

## 6. `eksad-core-auth-client` SDK (overview)

- Java Maven library: `com.eksad.platform:eksad-core-auth-client`.
- Built on Quarkus REST client (`@RegisterRestClient`) + Spring Boot WebClient implementation.
- Used by `svc-user-management` and any external project adapter.

| Method | Purpose |
|--------|---------|
| `registerCredential(userRef, providerSource, credentialValue)` | Register on user creation |
| `validateCredential(userRef, providerSource, credentialValue)` | Verify on login |
| `issueToken(userRef, claims)` | Sign new JWT pair |
| `refreshToken(refreshToken)` | Rotate token pair |
| `revokeToken(refreshToken, revokeAll)` | Logout |

**Consumer config:**
```properties
eksad.core-auth.url=http://eksad-core-auth:8090
```

> Full SDK design in `EKSAD_CORE_AUTH_CLIENT_SDK.md` (T-24).

---

## 7. Multi-Project Auth Adapter Pattern

Different projects can plug into the **same `eksad-core-auth`** through different user-management front-ends. Business users never know `eksad-core-auth` exists.

| Project | Flow |
|---------|------|
| **A — EKSAD full** | User → `svc-user-management` → SDK → `eksad-core-auth` |
| **B — Client's own user mgmt** | User → client-user-svc → SDK → `eksad-core-auth` |
| **C — External IdP (Keycloak)** | User → Keycloak → adapter-service → SDK → `eksad-core-auth` |

### Integration Steps for External Project
1. Add `eksad-core-auth-client` Maven dependency.
2. Configure `eksad.core-auth.url`.
3. On user create → `registerCredential()`.
4. On login → `validateCredential()` → resolve own roles → `issueToken()`.
5. Configure gateway/services to validate JWT via JWKS.
6. **Done** — zero user migration needed.

---

## 8. User Management Patterns (`svc-user-management`)

**Database:** MongoDB — `eksad_users`.

### Collections

| Collection | Shape |
|------------|-------|
| `users` | `{ user_ref, email, name, phone, tenant_id, domain_profile, status, created_at }` |
| `roles` | `{ code, name, description, permissions[], tenant_id }` |
| `role_assignments` | `{ user_ref, role_codes[], tenant_id }` |
| `jwt_claim_templates` | `{ domain, template: { ... } }` — determines what goes into JWT per domain |

### `domain_profile` Examples (schema-less)
- **Automotive:** `{ branch_id, dealer_code, sales_target }`
- **HRIS:** `{ employee_id, department_id, grade, manager_ref }`

### JWT Claim Template Example
```json
{
  "sub": "$user_ref",
  "tenant_id": "$tenant_id",
  "roles": "$role_codes",
  "branch_id": "$domain_profile.branch_id"
}
```

---

## 9. Login Flow (Step-by-step)

### A. Server-to-Server Flow (via svc-user-management SDK)

```
1. Client → POST /api/v1/auth/login { email, password } → svc-user-management
2. user-mgmt: lookup user by email → get user_ref
3. user-mgmt → SDK.validateCredential(user_ref, "local", password)
4. core-auth: hash + compare → check lockout
   - invalid → increment failed_attempts → { valid: false }
   - valid   → { valid: true }
5. user-mgmt: resolve roles/permissions from MongoDB
6. user-mgmt: build claims from JWT claim template + user data
7. user-mgmt → SDK.issueToken(user_ref, claims, device_info)
8. core-auth: sign JWT (RS256, active key) → create refresh token (BCrypt hash stored)
9. core-auth → { access_token, refresh_token, expires_in }
10. user-mgmt → client { access_token, refresh_token, expires_in }
```

### B. Browser-Direct Cookie Flow (via `CookieTokenResource`)

```
1. Browser → POST /internal/core-auth/cookie/login
             { user_ref, provider_source, credential_value, claims, device_info? }
2. core-auth: validateCredential(user_ref, provider_source, credential_value)
   - invalid → 401 { valid: false, lockoutInfo? }
   - valid   → continue
3. core-auth: issueToken → sign JWT + BCrypt hash refresh token
4. core-auth → Response 200 { expiresIn, tokenType }
             + Set-Cookie: eksad_at=<jwt>;      HttpOnly; Secure; SameSite=<config>; Path=/
             + Set-Cookie: eksad_rt=<rt_uuid>;  HttpOnly; Secure; SameSite=<config>; Path=/internal/core-auth/cookie
             + Set-Cookie: XSRF-TOKEN=<random>; Secure; SameSite=<config>; Path=/         (NON-HttpOnly — CSRF, see §11.3.1)
5. Browser stores cookies automatically — auth tokens never accessible from JavaScript (XSRF-TOKEN is readable by design)
```

> **Why two flows?** `svc-user-management` uses flow A because it needs to resolve roles from its own MongoDB before calling `issueToken`. Browser-direct uses flow B for simplicity — claims must still be provided by the caller (core-auth only signs, never resolves roles).

### Refresh (Server-to-Server)
```
1. POST /api/v1/auth/refresh { refresh_token } → user-mgmt
2. user-mgmt → SDK.refreshToken(refresh_token)
3. core-auth: validate hash → check not revoked/expired → issue new pair (rotation)
4. core-auth → { access_token, refresh_token, expires_in }
```

### Refresh (Browser Cookie)
```
1. Browser → POST /internal/core-auth/cookie/refresh (no body — cookie auto-sent)
2. core-auth: read eksad_rt cookie → validate hash → rotate
3. core-auth → 200 { expiresIn, tokenType }
             + Set-Cookie: eksad_at=<new_jwt>; ...
             + Set-Cookie: eksad_rt=<new_rt>;  ...
             + Set-Cookie: XSRF-TOKEN=<new_random>; Secure; SameSite=<config>; Path=/   (rotated — CSRF, see §11.3.1)
   Old refresh token revoked immediately (rotation).
```

### Logout (Server-to-Server)
```
1. POST /api/v1/auth/logout { refresh_token } → user-mgmt
2. user-mgmt → SDK.revokeToken(refresh_token, revokeAll?)
3. core-auth: mark token(s) revoked
```

### Logout (Browser Cookie)
```
1. Browser → POST /internal/core-auth/cookie/revoke
             Body (optional): { revokeAll?, deviceId?, revokedBy? }
2. core-auth: read eksad_rt cookie → revoke session(s)
3. core-auth → 200 { revoked: true }
             + Set-Cookie: eksad_at=; Path=/;                          Max-Age=0
             + Set-Cookie: eksad_rt=; Path=/internal/core-auth/cookie; Max-Age=0
             + Set-Cookie: XSRF-TOKEN=; Path=/;                         Max-Age=0   (cleared — CSRF, see §11.3.1)
```

### Lockout
- After **N** failed attempts (default 5) → lock for **M** minutes (default 15).
- `locked_until BIGINT` in `credentials` table.
- Auto-unlock after lockout period.

---

## 10. Per-Service JWT Validation (Gateway Optional)

Per Decision 13, every domain service MUST be able to validate JWT independently:

```properties
# Quarkus
mp.jwt.verify.publickey.location=http://eksad-core-auth:8090/.well-known/jwks.json
mp.jwt.verify.issuer=eksad-core-auth
quarkus.smallrye-jwt.enabled=true
```

```yaml
# Spring Boot
spring:
  security:
    oauth2:
      resourceserver:
        jwt:
          jwk-set-uri: http://eksad-core-auth:8090/.well-known/jwks.json
          issuer-uri: eksad-core-auth
```

### Extract claims in code
```java
@Inject JsonWebToken jwt;

String tenantId = jwt.getClaim("tenant_id");
String userRef  = jwt.getSubject();
```

- Use `@RolesAllowed` for endpoint protection.
- Every query MUST filter by `tenant_id` from JWT (see `EKSAD_MULTI_TENANCY_PATTERNS.md`).

---

## 11. Security Hardening

### 11.1 Password Policy (Moderate)
- Min 10 characters, ≥ 1 uppercase + 1 number + 1 special character.
- Password history: last 5 cannot be reused (`password_history` table, store hashes).
- No forced rotation (NIST 800-63B) — force change only on compromise.
- Validation enforced at registration/change.

### 11.2 MFA / 2FA (Optional per Tenant — NOT Sprint 1)
- Disabled / Optional / Required for admin / Required for all.
- Planned providers: TOTP (RFC 6238), Email OTP, SMS OTP.
- Sprint 1: placeholder hook only. Sprint 2-3: TOTP first.
- Tables (future): `mfa_config`, `user_mfa_secrets`.

### 11.3 Session Management
- Max concurrent sessions: **3 per user** (env: `EKSAD_AUTH_MAX_SESSIONS=3`).
- On limit reached: **KICK OLDEST** — auto-revoke oldest active session.
- Device tracking: `device_id` (UUID, client-generated), `device_name`, `device_type`, `ip_address`, `last_used_at`.
- **3 revocation levels:**
  - `POST /api/v1/auth/logout` — current session
  - `POST /api/v1/auth/logout-device` — specific device by `device_id`
  - `POST /api/v1/auth/logout-all` — ALL sessions (e.g., on password change)
- Access token: **30 min** (`EKSAD_AUTH_ACCESS_TOKEN_LIFETIME_MINUTES=30`), stateless JWT.
- Refresh token: **30 days** (`EKSAD_AUTH_REFRESH_TOKEN_LIFETIME_DAYS=30`), BCrypt hash stored in DB.
  - **Browser mode**: delivered via `Set-Cookie: eksad_rt=...; HttpOnly; Secure; SameSite=<config>` — never in response body.
  - **Server-to-server mode**: returned in response body `{ refresh_token }` — caller (svc-user-management) manages storage.

**Cookie configuration env vars (browser mode):**

| Env Var | Default | Notes |
|---------|---------|-------|
| `EKSAD_AUTH_COOKIE_ACCESS_NAME` | `eksad_at` | Cookie name for JWT access token (HTTP-only) |
| `EKSAD_AUTH_COOKIE_REFRESH_NAME` | `eksad_rt` | Cookie name for refresh token (HTTP-only) |
| `EKSAD_AUTH_COOKIE_SECURE` | `true` (prod) / `false` (dev) | Must be `false` for local HTTP dev |
| `EKSAD_AUTH_COOKIE_SAME_SITE` | `Lax` | `Lax` = same-host + cross-site GET; `Strict` = same-site only; `None` = cross-domain (requires `Secure=true`) |
| `EKSAD_AUTH_COOKIE_XSRF_NAME` | `XSRF-TOKEN` | CSRF token cookie name — **non-HttpOnly** (frontend JS must read it to echo in `X-XSRF-TOKEN` header). Set at login, rotated on refresh, cleared on revoke. See §11.3.1. |
| `EKSAD_AUTH_CSRF_ENABLED` | `true` (browser/cookie mode) | Enables double-submit CSRF verification on state-changing requests (`POST`/`PUT`/`PATCH`/`DELETE`). N/A for server-to-server bearer-token mode. |
| `EKSAD_AUTH_CSRF_HEADER_NAME` | `X-XSRF-TOKEN` | Request header the frontend echoes the CSRF token in; compared against the `XSRF-TOKEN` cookie. |

**SameSite selection guide:**

| Scenario | SameSite | Secure |
|----------|----------|--------|
| FE & service same machine (`localhost:3000 → localhost:8090`) | `Lax` | `false` |
| FE different machine, same network (HTTP) | `Lax` | `false` |
| Production HTTPS, same domain | `Strict` | `true` |
| Production HTTPS, cross-domain | `None` | `true` (mandatory) |

### 11.3.1 CSRF Protection (Double-Submit Cookie) — Browser/Cookie Mode Only

Cookie-delivered auth (`eksad_at`) is sent automatically by the browser, so cookie mode **must** add CSRF
protection. The XSRF token is **not** an identity/auth token — the JWT cookie authenticates; the XSRF token
proves the request originated from the EKSAD frontend (not a forged cross-site request).

> **Default = stateless, zero infra (NO Redis).** The backend stores nothing server-side; it only compares
> two values per request. Security comes from the browser **same-origin policy**, not from a server-side
> secret store. A cross-site attacker cannot read the victim's `XSRF-TOKEN` cookie, therefore cannot echo
> its value into the `X-XSRF-TOKEN` header — so `header == cookie` proves a same-origin (EKSAD frontend)
> request. Redis/stateful storage is an **optional upgrade** (see §11.3.2), not a requirement.

**Mechanism — stateless double-submit:**

```
LOGIN  → core-auth sets cookies:
   eksad_at   = <jwt>          HttpOnly  Secure  SameSite=<config>           (auth — JS cannot read)
   eksad_rt   = <rt>           HttpOnly  Secure  Path=/internal/core-auth/cookie
   XSRF-TOKEN = <random ≥32B>  NON-HttpOnly  Secure  SameSite=<config>  Path=/   (JS CAN read)

WRITE request (POST/PUT/PATCH/DELETE):
   Browser auto-sends eksad_at + XSRF-TOKEN cookies
   Frontend reads XSRF-TOKEN cookie → sends header  X-XSRF-TOKEN: <value>

BACKEND verifies (NO server lookup):
   1. eksad_at JWT valid?                          (authentication)
   2. header X-XSRF-TOKEN == XSRF-TOKEN cookie ?    (CSRF) → mismatch/absent → 403
```

**Two stateless variants:**

| Variant | Token value | Backend validation | Resists cookie-injection | When |
|---------|-------------|--------------------|--------------------------|------|
| **Plain double-submit** | `SecureRandom` ≥ 32B, base64url | string-compare header vs cookie | weak | enough for `SameSite=Lax`/`Strict` |
| **Signed double-submit** ✅ recommended | `HMAC(jti, EKSAD_AUTH_SIGNING_KEY_SECRET)` | recompute HMAC from JWT `jti` claim, compare to header — still **no store** | strong | **mandatory** for `SameSite=None` (cross-domain) |

> **"Encrypt/bind it in the JWT — still safe?"** Yes, and it is the hardened path. Do **not** put the token
> *only* inside the JWT (the JWT is HttpOnly — JS can't read it to echo a header). Instead **derive** the
> XSRF token = `HMAC(jti, secret)`, place it in the non-HttpOnly `XSRF-TOKEN` cookie, and let the backend
> recompute the HMAC from the JWT's `jti` claim. No Redis, still stateless, and the token cannot be guessed
> or forged without the server secret.

**Rules:**
- The `XSRF-TOKEN` cookie is **non-HttpOnly** (frontend must read it); the auth cookies stay HttpOnly.
- Verify **only** on state-changing methods — `GET`/`HEAD`/`OPTIONS` are exempt.
- Lifecycle: issue at `/cookie/login`, rotate at `/cookie/refresh`, clear (`Max-Age=0`) at `/cookie/revoke`.
- **No separate XSRF revocation needed.** The XSRF token is useless without the auth cookie, so sign-out is
  already covered by (a) revoking the refresh token server-side + (b) clearing all cookies (`Max-Age=0`).
  A dedicated XSRF revocation list is redundant in stateless mode (it only becomes relevant in §11.3.2).
- Applies to **cookie mode only** — server-to-server `Authorization: Bearer` requests carry no ambient cookie
  and are exempt (`EKSAD_AUTH_CSRF_ENABLED` N/A).
- Defense-in-depth with `SameSite`: `Strict`/`Lax` mitigates most CSRF; double-submit is **mandatory** when
  `SameSite=None` (cross-domain).

### 11.3.2 CSRF Protection (Stateful Synchronizer Token via Redis) — Optional Upgrade

The stateless model in §11.3.1 is the default and is sufficient for almost all cases. Move to a **stateful
synchronizer token** backed by Redis **only** when you need a capability stateless cannot provide:

| Need | Why stateless can't, why Redis can |
|------|-----------------------------------|
| **Instant per-token server-side revocation** | Stateless token lives until the cookie is cleared; Redis lets you `DEL` a token immediately |
| **One-time / per-request rotating tokens** | Server must remember the issued value to invalidate after first use |
| **Central audit of issued CSRF tokens** | Redis is the single source of truth |

**Is storing in Redis safe?** Yes — it is a well-established pattern (OWASP "Synchronizer Token"). Keep these
guarantees:

- **Key schema:** `xsrf:{sessionId}` (or `xsrf:{jti}`) → token value. **Never** key by `userRef` only —
  that would invalidate other tabs/devices (see scenario table in the brainstorm).
- **Value:** `SecureRandom` ≥ 32B, base64url. Store the token (or its HMAC), never anything sensitive.
- **TTL strategy (avoids the "TTL died mid-session" problem):** set the Redis TTL **equal to the refresh
  token lifetime** (`EKSAD_AUTH_REFRESH_TOKEN_LIFETIME_DAYS`, default 30d) and **re-write + extend on every
  `/cookie/refresh`**. Do **not** tie TTL to the 30-min access token — that would expire while the session
  is still alive and reject legitimate writes.
- **Validation:** compare `header X-XSRF-TOKEN` against the Redis value for the session (not against the
  cookie). Absent/expired/mismatch → `403`.
- **Lifecycle:** `SET` at `/cookie/login`, rotate (`SET` new + `DEL` old) at `/cookie/refresh`,
  `DEL` at `/cookie/revoke` (sign-out) — this is where **self-revocation on sign-out** is naturally honoured.
- **Multi-instance:** Redis must be a **shared** instance (never in-memory per pod) so any backend replica
  behind the load balancer can validate.
- **Resilience:** if Redis is unavailable, **fail closed** on writes (`403`) — never silently downgrade to
  no-CSRF. Consider a circuit-breaker fallback to stateless signed double-submit (§11.3.1) if availability is
  more important than instant revocation for your tenant.

**FE behaviour is identical** in both models: read the `XSRF-TOKEN` cookie, echo it in `X-XSRF-TOKEN`, and on
`403 CSRF` call `/cookie/refresh` once then retry — so switching stateless ↔ stateful is a backend-only change.

**Additional env vars (only when `EKSAD_AUTH_CSRF_STORE=redis`):**

| Env Var | Default | Notes |
|---------|---------|-------|
| `EKSAD_AUTH_CSRF_STORE` | `stateless` | `stateless` (default, no infra) or `redis` (stateful synchronizer token) |
| `EKSAD_AUTH_CSRF_REDIS_KEY_PREFIX` | `xsrf:` | Redis key prefix; full key = `{prefix}{sessionId}` |
| `EKSAD_AUTH_CSRF_REDIS_TTL_DAYS` | `30` | TTL for the stored token — keep aligned with refresh token lifetime |

### 11.4 Rate Limiting (Defense in Depth)
- With gateway present: gateway = primary, per-service = backup.
- Without gateway: per-service mandatory.

| Endpoint | Limit |
|----------|-------|
| Login | 5/min per `user_ref` |
| Token refresh | 10/min per `user_ref` |
| JWKS | 100/min per IP |
| `/internal/*` | No limit (trusted network) |

Implementation: Quarkus rate-limiter extension or Bucket4j.

### 11.5 Credential Storage
- **Hashing:** BCrypt (Sprint 1) → Argon2id migration path.
  - `credentials.algorithm` tracks which was used.
  - Auto-upgrade on login: if `algorithm='bcrypt'` and login success → re-hash with Argon2id, update column.
  - Zero downtime, gradual.
- **Signing key encryption at rest:** AES-256.
  - Master key: env var `EKSAD_AUTH_SIGNING_KEY_SECRET`.
  - Decrypt at startup, hold in memory only.
  - Future: HashiCorp Vault / Cloud KMS (no schema change).
- **TLS:** Dev = skip, Staging = TLS between services, Production = TLS everywhere + optional mTLS.

### 11.6 Auth Event Audit & Retention
- All auth events logged to `auth_events` (separate from business audit trail).
- Events: `LOGIN_SUCCESS`, `LOGIN_FAILED`, `TOKEN_REFRESH`, `TOKEN_REVOKE`, `PASSWORD_CHANGE`, `LOCKOUT_TRIGGERED`, `KEY_ROTATION`, `MFA_ENABLED`, `MFA_VERIFIED`.
- Retention: **90 days** — auto-purge via Quarkus `@Scheduled`.
- Configurable: `EKSAD_AUTH_EVENT_RETENTION_DAYS=90`.

---

## 12. Testing

| Test Type | Scenarios |
|-----------|-----------|
| Unit | BCrypt hash compare; lockout logic; JWT signing (RS256); key rotation; session limit kick-oldest |
| Integration | Full login flow with Testcontainers (PostgreSQL + MongoDB); register → validate → issue → refresh → revoke |
| SDK | WireMock core-auth endpoints; verify SDK methods + `CoreAuthException` mapping |
| JWT validation | Valid JWT → 200; expired → 401; wrong key → 401; tampered claims → 401 |
| Key rotation | Rotate → old JWT still valid → new JWT uses new `kid` |
| Multi-project | Two different user-mgmt services → both get valid JWTs from same core-auth |
| Device tracking | Login from 3 devices → 3 refresh tokens; logout-device → only that device revoked; logout-all → all revoked |

See `EKSAD_TESTING_GUIDE.md` Sections "Core Auth Testing" + "Security Testing".

---

## 13. Browser-Facing Cookie Token API (`CookieTokenResource`)

**Path prefix:** `/internal/core-auth/cookie`  
**Auth:** `@PermitAll` — security enforced at network layer (same trust model as internal API).  
**Token delivery:** Both access token and refresh token set as **HTTP-only cookies**. Tokens **never** appear in response body.

### 13.1 Why Two APIs Exist

| Dimension | `/token/*` (Server-to-Server) | `/cookie/*` (Browser-Facing) |
|-----------|-------------------------------|------------------------------|
| **Caller** | `svc-user-management` via SDK | Browser directly |
| **Token delivery** | Response body `{ access_token, refresh_token }` | `Set-Cookie` headers only |
| **Password check** | Caller responsible (calls `/validate` first) | `/login` enforces it inline |
| **Refresh input** | `{ refresh_token }` in body | `Cookie: eksad_rt=...` auto-sent |
| **Logout** | `{ refresh_token }` in body | Cookie read + `Max-Age=0` clear |

### 13.2 Endpoints

| Method | Path | Body | Purpose |
|--------|------|------|---------|
| `POST` | `/cookie/login` | `{ userRef, providerSource, credentialValue, claims, deviceInfo? }` | Validate password + issue cookies — **primary browser login** |
| `POST` | `/cookie/issue` | `{ userRef, claims, deviceInfo? }` (same as `/token/issue`) | Trusted issue → set cookies — for backend-proxied flows |
| `POST` | `/cookie/refresh` | None — reads `eksad_rt` cookie | Rotate token pair, set new cookies |
| `POST` | `/cookie/revoke` | `{ revokeAll?, deviceId?, revokedBy? }` (optional) — reads `eksad_rt` cookie | Revoke session + clear cookies |

### 13.3 `POST /cookie/login` — Request / Response

**Request body:**
```json
{
  "userRef":         "user-001",
  "providerSource":  "local",
  "credentialValue": "P@ssw0rd!",
  "claims": {
    "tenant_id":   "tenant-eksad",
    "roles":       ["ROLE_USER"],
    "permissions": ["READ_TRANSACTION"]
  },
  "deviceInfo": {
    "deviceId":   "device-abc-123",
    "deviceName": "Chrome macOS",
    "deviceType": "web",
    "ipAddress":  "192.168.1.5"
  }
}
```

**Response on success (HTTP 200):**
```json
{ "expiresIn": 1800, "tokenType": "Bearer" }
```
```
Set-Cookie: eksad_at=eyJhbG...; Path=/;                          HttpOnly; SameSite=Lax
Set-Cookie: eksad_rt=uuid-val; Path=/internal/core-auth/cookie; HttpOnly; SameSite=Lax
```

**Response on failure (HTTP 401):**
```json
{
  "valid": false,
  "lockoutInfo": {
    "locked": true,
    "lockedUntil": 1748234567890,
    "failedAttempts": 5,
    "maxAttempts": 5
  }
}
```

### 13.4 Quarkus Configuration Required

When Quarkus JWT extension is on the classpath, it proactively blocks ALL requests before `@PermitAll` is checked. Two `application.properties` entries are **mandatory**:

```properties
# 1. CORS — required for browser cross-origin requests
#    origins=* MUST NOT be combined with credentials=true (browser spec violation)
#    Use regex — Quarkus echoes back the actual Origin header if it matches
quarkus.http.cors=true
quarkus.http.cors.origins=${CORS_ORIGINS:/https?:\\/\\/.+/}
quarkus.http.cors.methods=GET,POST,PUT,PATCH,DELETE,OPTIONS
quarkus.http.cors.headers=Content-Type,Authorization,Accept,Origin,X-Requested-With
quarkus.http.cors.access-control-allow-credentials=true   # MANDATORY for cookies
quarkus.http.cors.access-control-max-age=PT1H

# 2. HTTP permission policies — bypass JWT proactive check for trusted paths
quarkus.http.auth.permission.permit-internal.paths=/internal/*
quarkus.http.auth.permission.permit-internal.policy=permit
quarkus.http.auth.permission.permit-public.paths=/.well-known/*,/q/*
quarkus.http.auth.permission.permit-public.policy=permit
```

> ⚠️ **Common mistake:** Setting `origins=*` with `credentials=true` causes browser to block all requests (CORS spec). Always use a regex pattern or explicit origins list.

### 13.5 Frontend Integration

**Fetch (browser):**
```js
const res = await fetch('http://auth:8090/internal/core-auth/cookie/login', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  credentials: 'include',   // MANDATORY — sends + receives cookies cross-origin
  body: JSON.stringify({ userRef, providerSource, credentialValue, claims })
});
```

**Axios:**
```js
axios.defaults.withCredentials = true;  // set once globally
```

> Cookies are `HttpOnly` — JavaScript cannot read them. Verify via DevTools → Application → Cookies.

---

*End of file. Cross-references: `EKSAD_CORE_AUTH_CLIENT_SDK.md`, `EKSAD_MULTI_TENANCY_PATTERNS.md`, `EKSAD_RESILIENCE_PATTERNS.md`.*
