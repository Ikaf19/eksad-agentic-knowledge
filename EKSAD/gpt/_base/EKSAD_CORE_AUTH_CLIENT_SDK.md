# EKSAD Core Auth Client SDK

**Version:** 1.0
**Date:** 2026-05-23
**Owner:** EKSAD Platform Team
**Audience:** Developers, Architects, External Project Integrators
**Priority:** 🟡 P1
**Related:** `EKSAD_CORE_AUTH_PATTERNS.md`, `EKSAD_RESILIENCE_PATTERNS.md`, `EKSAD_TESTING_GUIDE.md`

> The `eksad-core-auth-client` Java library is the **only supported entry point** to `eksad-core-auth`. Direct REST access to the internal `/internal/core-auth/*` endpoints from outside the SDK is forbidden.

---

## Table of Contents

1. [Overview](#1-overview)
2. [Maven Module Structure](#2-maven-module-structure)
3. [`CoreAuthClient` Interface](#3-coreauthclient-interface)
4. [DTO Definitions](#4-dto-definitions)
5. [Error Handling](#5-error-handling)
6. [Quarkus Implementation](#6-quarkus-implementation)
7. [Spring Boot Implementation](#7-spring-boot-implementation)
8. [Consumer Integration Guide](#8-consumer-integration-guide)
9. [Mock Implementation for Testing](#9-mock-implementation-for-testing)
10. [WireMock Testing Pattern](#10-wiremock-testing-pattern)
11. [Versioning & Publishing](#11-versioning--publishing)
12. [Configuration Reference](#12-configuration-reference)

---

## 1. Overview

`eksad-core-auth-client` is a Maven library that wraps the internal HTTP API of `eksad-core-auth`. It is consumed by:

- **`svc-user-management`** (EKSAD primary consumer — wires identity onto credentials/tokens)
- **External project adapters** (e.g., Keycloak/LDAP/OAuth2 facades that delegate to core-auth)

The library hides URL construction, error mapping, retry, circuit breaker, and supports both **Quarkus** (CDI + REST Client Reactive) and **Spring Boot** (WebClient + Resilience4j) consumers from a single dependency.

> Rule: **Consumers never call core-auth REST API directly.** Always inject and use `CoreAuthClient`.

---

## 2. Maven Module Structure

```
eksad-core-auth-client/
├── pom.xml
└── src/
    ├── main/java/com/eksad/platform/auth/client/
    │   ├── CoreAuthClient.java               ← main interface
    │   ├── CoreAuthClientImpl.java           ← Quarkus impl
    │   ├── CoreAuthClientSpringImpl.java     ← Spring Boot impl
    │   ├── CoreAuthConfig.java               ← config properties
    │   ├── dto/
    │   │   ├── RegisterCredentialRequest.java
    │   │   ├── RegisterCredentialResponse.java
    │   │   ├── ValidateCredentialRequest.java
    │   │   ├── ValidateCredentialResponse.java
    │   │   ├── IssueTokenRequest.java
    │   │   ├── RefreshTokenRequest.java
    │   │   ├── TokenResult.java
    │   │   ├── RevokeTokenRequest.java
    │   │   ├── SessionInfo.java
    │   │   ├── DeviceInfo.java
    │   │   └── LockoutInfo.java
    │   └── exception/
    │       ├── CoreAuthException.java
    │       ├── CoreAuthErrorCode.java
    │       ├── CredentialNotFoundException.java
    │       ├── AccountLockedException.java
    │       ├── InvalidCredentialException.java
    │       ├── TokenExpiredException.java
    │       └── TokenRevokedException.java
    └── test/java/com/eksad/platform/auth/client/
        ├── CoreAuthClientTest.java           ← WireMock-based
        ├── CoreAuthClientMock.java           ← In-memory mock for consumer tests
        └── CoreAuthWireMockSetup.java        ← reusable stub helpers
```

### 2.1 Coordinates

```xml
<dependency>
  <groupId>com.eksad.platform</groupId>
  <artifactId>eksad-core-auth-client</artifactId>
  <version>1.0.0</version>
</dependency>
```

### 2.2 pom.xml Dependencies

```xml
<dependencies>
  <dependency>
    <groupId>io.quarkus</groupId>
    <artifactId>quarkus-rest-client-reactive-jackson</artifactId>
    <scope>provided</scope>
  </dependency>
  <dependency>
    <groupId>org.eclipse.microprofile.rest.client</groupId>
    <artifactId>microprofile-rest-client-api</artifactId>
    <scope>provided</scope>
  </dependency>
  <dependency>
    <groupId>com.fasterxml.jackson.core</groupId>
    <artifactId>jackson-databind</artifactId>
  </dependency>

  <!-- test -->
  <dependency>
    <groupId>com.github.tomakehurst</groupId>
    <artifactId>wiremock-jre8-standalone</artifactId>
    <scope>test</scope>
  </dependency>
</dependencies>
```

`scope=provided` keeps the library lightweight — consumers supply the framework runtime.

---

## 3. `CoreAuthClient` Interface

```java
public interface CoreAuthClient {

  // ── Credential management ─────────────────────────────────
  RegisterCredentialResponse registerCredential(
      String userRef, String providerSource, String credentialValue) throws CoreAuthException;

  ValidateCredentialResponse validateCredential(
      String userRef, String providerSource, String credentialValue) throws CoreAuthException;

  void updateCredential(
      String userRef, String providerSource, String newCredentialValue) throws CoreAuthException;

  void deleteCredential(String userRef, String providerSource) throws CoreAuthException;

  // ── Token management ──────────────────────────────────────
  TokenResult issueToken(String userRef, Map<String, Object> claims) throws CoreAuthException;
  TokenResult issueToken(String userRef, Map<String, Object> claims, DeviceInfo device) throws CoreAuthException;

  TokenResult refreshToken(String refreshToken) throws CoreAuthException;

  void revokeToken(String refreshToken, boolean revokeAll) throws CoreAuthException;
  void revokeByDevice(String userRef, String deviceId) throws CoreAuthException;
  void revokeAllSessions(String userRef, String reason) throws CoreAuthException;

  // ── Session queries ───────────────────────────────────────
  List<SessionInfo> getActiveSessions(String userRef) throws CoreAuthException;

  // ── Health check ──────────────────────────────────────────
  boolean isHealthy();
}
```

---

## 4. DTO Definitions

### 4.1 `RegisterCredentialRequest` / `Response`

```java
// Request
String userRef;
String providerSource;   // "local" | "ldap" | "oauth2" | "saml"
String credentialValue;  // raw password / token — never logged

// Response
Long   credentialId;
Long   createdAt;        // epoch ms
```

### 4.2 `ValidateCredentialRequest` / `Response`

```java
// Request
String userRef;
String providerSource;
String credentialValue;

// Response
boolean      valid;
LockoutInfo  lockoutInfo;   // populated only when not valid due to lockout
```

`LockoutInfo`: `{ locked, lockedUntil (epoch ms), failedAttempts, maxAttempts }`.

### 4.3 `IssueTokenRequest` / `TokenResult`

```java
// Request
String userRef;
Map<String, Object> claims;     // tenant_id, roles, permissions, domain_profile, ...
DeviceInfo deviceInfo;          // optional — for per-device session tracking

// TokenResult
String accessToken;             // signed RS256 JWT
String refreshToken;            // opaque, hashed server-side
long   expiresIn;               // seconds
String tokenType;               // always "Bearer"
```

`DeviceInfo`: `{ deviceId, deviceName, deviceType, ipAddress }`.

### 4.4 `RevokeTokenRequest`

Three flavours, one DTO:

| Flavour | Fields |
|---------|--------|
| Single | `refreshToken` |
| All for user | `refreshToken`, `revokeAll = true` |
| By device | `userRef`, `deviceId` |
| All sessions | `userRef`, `reason ∈ { password_change, admin, user }` |

### 4.5 `SessionInfo`

```java
String sessionId;
String deviceId;
String deviceName;
String deviceType;
String ipAddress;
long   issuedAt;
long   lastUsedAt;
```

---

## 5. Error Handling

### 5.1 Hierarchy

```
RuntimeException
└─ CoreAuthException                  { errorCode, message, httpStatus }
   ├─ CredentialNotFoundException     CREDENTIAL_NOT_FOUND
   ├─ AccountLockedException          ACCOUNT_LOCKED      (+ lockoutInfo)
   ├─ InvalidCredentialException      INVALID_CREDENTIAL
   ├─ TokenExpiredException           TOKEN_EXPIRED
   └─ TokenRevokedException           TOKEN_REVOKED
```

### 5.2 `CoreAuthErrorCode` Enum

```
CREDENTIAL_NOT_FOUND          user_ref + provider_source not registered
CREDENTIAL_ALREADY_EXISTS     duplicate registration
INVALID_CREDENTIAL            wrong password
ACCOUNT_LOCKED                too many failed attempts
TOKEN_EXPIRED                 refresh token expired
TOKEN_REVOKED                 refresh token already revoked
TOKEN_INVALID                 malformed / unknown
SESSION_LIMIT_EXCEEDED        informational — SDK auto-handles by kicking oldest
SIGNING_KEY_ERROR             key rotation issue in core-auth
RATE_LIMITED                  429 from core-auth
SERVICE_UNAVAILABLE           core-auth down / timeout
INTERNAL_ERROR                unexpected
```

### 5.3 HTTP → Exception Mapping

| HTTP | Mapped exception |
|------|------------------|
| 400 | parse body → specific subtype (e.g. `INVALID_CREDENTIAL`) |
| 401 | `InvalidCredentialException` or `TokenExpiredException` |
| 403 | `AccountLockedException` (`lockoutInfo` populated) |
| 404 | `CredentialNotFoundException` |
| 429 | `CoreAuthException(RATE_LIMITED)` |
| 500 | `CoreAuthException(INTERNAL_ERROR)` |
| 503 / timeout | `CoreAuthException(SERVICE_UNAVAILABLE)` |

---

## 6. Quarkus Implementation

### 6.1 Internal REST Client

```java
@RegisterRestClient(configKey = "core-auth")
@Path("/internal/core-auth")
public interface CoreAuthRestClient {

  @POST @Path("/credentials")
  RegisterCredentialResponse register(RegisterCredentialRequest req);

  @POST @Path("/validate")
  ValidateCredentialResponse validate(ValidateCredentialRequest req);

  @POST @Path("/token/issue")
  TokenResult issue(IssueTokenRequest req);

  @POST @Path("/token/refresh")
  TokenResult refresh(RefreshTokenRequest req);

  @POST @Path("/token/revoke")
  void revoke(RevokeTokenRequest req);
}
```

### 6.2 CDI Bean

```java
@ApplicationScoped
public class CoreAuthClientImpl implements CoreAuthClient {

  @Inject @RestClient CoreAuthRestClient rest;
  @Inject CoreAuthErrorMapper errorMapper;

  @Override
  @Timeout(5000)
  @Retry(maxRetries = 3, delay = 500, jitter = 200,
         retryOn   = { ConnectException.class, TimeoutException.class },
         abortOn   = { BadRequestException.class, NotFoundException.class })
  @CircuitBreaker(requestVolumeThreshold = 10, failureRatio = 0.5, delay = 10000)
  public ValidateCredentialResponse validateCredential(String userRef, String src, String value) {
    try {
      return rest.validate(new ValidateCredentialRequest(userRef, src, value));
    } catch (WebApplicationException ex) {
      throw errorMapper.map(ex);   // → CoreAuthException subtypes
    }
  }
  // ... other methods follow identical pattern
}
```

### 6.3 Consumer `application.properties`

```properties
quarkus.rest-client."core-auth".url=${EKSAD_CORE_AUTH_URL:http://eksad-core-auth:8090}
quarkus.rest-client."core-auth".connect-timeout=${eksad.core-auth.connect-timeout:5000}
quarkus.rest-client."core-auth".read-timeout=${eksad.core-auth.read-timeout:10000}
```

Bean is auto-discovered via CDI — consumers just add the Maven dep and `@Inject CoreAuthClient`.

---

## 7. Spring Boot Implementation

### 7.1 Auto-Configuration

```java
@AutoConfiguration
@EnableConfigurationProperties(CoreAuthConfig.class)
@ConditionalOnProperty(prefix = "eksad.core-auth", name = "url")
public class CoreAuthClientAutoConfiguration {

  @Bean
  WebClient coreAuthWebClient(CoreAuthConfig cfg) {
    HttpClient http = HttpClient.create()
        .responseTimeout(Duration.ofMillis(cfg.getReadTimeout()))
        .option(ChannelOption.CONNECT_TIMEOUT_MILLIS, cfg.getConnectTimeout());
    return WebClient.builder()
        .baseUrl(cfg.getUrl())
        .clientConnector(new ReactorClientHttpConnector(http))
        .filter(CoreAuthErrorFilter.INSTANCE)
        .build();
  }

  @Bean
  CoreAuthClient coreAuthClient(WebClient client) {
    return new CoreAuthClientSpringImpl(client);
  }
}
```

Register in `META-INF/spring/org.springframework.boot.autoconfigure.AutoConfiguration.imports`:

```
com.eksad.platform.auth.client.CoreAuthClientAutoConfiguration
```

### 7.2 Resilience

Resilience4j annotations on each method:

```java
@Retryable(retryFor = {WebClientRequestException.class}, maxAttempts = 3,
           backoff = @Backoff(delay = 500, multiplier = 2))
@CircuitBreaker(name = "coreAuth", fallbackMethod = "fallbackUnavailable")
public ValidateCredentialResponse validateCredential(String userRef, String src, String value) { /* ... */ }
```

Consumer `application.yml`:

```yaml
eksad:
  core-auth:
    url: http://eksad-core-auth:8090
    connect-timeout: 5000
    read-timeout: 10000
    retry-max: 3
    retry-delay-ms: 500
resilience4j:
  circuitbreaker:
    instances:
      coreAuth: { failureRateThreshold: 50, waitDurationInOpenState: 10s, slidingWindowSize: 10 }
```

---

## 8. Consumer Integration Guide

### 8.1 Primary Consumer: `svc-user-management`

```java
@ApplicationScoped
public class UserAuthService {

  @Inject CoreAuthClient coreAuth;
  @Inject UserRepository userRepo;
  @Inject ClaimBuilder   claimBuilder;

  public TokenResult login(String email, String password, DeviceInfo device) {
    User user = userRepo.findByEmail(email)
        .orElseThrow(() -> new InvalidCredentialException());

    ValidateCredentialResponse res =
        coreAuth.validateCredential(user.getUserRef(), "local", password);

    if (!res.isValid()) {
      if (res.getLockoutInfo() != null && res.getLockoutInfo().isLocked()) {
        throw new AccountLockedException(res.getLockoutInfo());
      }
      throw new InvalidCredentialException();
    }

    Map<String, Object> claims = claimBuilder.buildClaims(user);
    return coreAuth.issueToken(user.getUserRef(), claims, device);
  }
}
```

### 8.2 External Project Adapter (e.g., Keycloak)

```java
public TokenResult keycloakLogin(KeycloakToken kc) {
  String userRef = kc.getSubject();
  // Idempotent — registers on first login, no-op otherwise
  coreAuth.registerCredential(userRef, "keycloak", kc.getRaw());
  Map<String, Object> claims = mapKeycloakClaims(kc);
  return coreAuth.issueToken(userRef, claims);
}
```

### 8.3 Quick-Start Checklist

- [ ] Add `eksad-core-auth-client` Maven dependency
- [ ] Set `eksad.core-auth.url` in `application.properties` / `application.yml`
- [ ] `@Inject CoreAuthClient` (Quarkus) or `@Autowired CoreAuthClient` (Spring)
- [ ] Implement login flow: `validateCredential` → build claims → `issueToken`
- [ ] Map `CoreAuthException` subtypes in your exception handler (`@ServerExceptionMapper` / `@RestControllerAdvice`)
- [ ] Add WireMock-based test for the login flow

---

## 9. Mock Implementation for Testing

`CoreAuthClientMock` — in-memory implementation suitable for consumer unit/integration tests; no HTTP calls.

```java
@Alternative
@Priority(1)
@ApplicationScoped
public class CoreAuthClientMock implements CoreAuthClient {

  private final Map<String, String> credentials = new ConcurrentHashMap<>();
  private final Map<String, Integer> failedAttempts = new ConcurrentHashMap<>();
  private final Set<String> revokedTokens = ConcurrentHashMap.newKeySet();

  @Override
  public RegisterCredentialResponse registerCredential(String userRef, String src, String value) {
    credentials.put(key(userRef, src), BCrypt.hashpw(value, BCrypt.gensalt()));
    return new RegisterCredentialResponse(System.nanoTime(), Instant.now().toEpochMilli());
  }

  @Override
  public ValidateCredentialResponse validateCredential(String userRef, String src, String value) {
    int attempts = failedAttempts.getOrDefault(userRef, 0);
    if (attempts >= 5) {
      return ValidateCredentialResponse.locked(new LockoutInfo(true,
          Instant.now().plus(15, MINUTES).toEpochMilli(), attempts, 5));
    }
    String hash = credentials.get(key(userRef, src));
    boolean ok = hash != null && BCrypt.checkpw(value, hash);
    if (!ok) failedAttempts.merge(userRef, 1, Integer::sum);
    else     failedAttempts.remove(userRef);
    return new ValidateCredentialResponse(ok, null);
  }

  // ... issueToken returns a dummy JWT signed with a test key
  // ... refreshToken / revoke / sessions implemented in-memory
}
```

### 9.1 Predefined Scenarios

| Constant | Behaviour |
|----------|-----------|
| `SCENARIO_VALID_LOGIN` | user exists, correct password |
| `SCENARIO_INVALID_PASSWORD` | user exists, wrong password |
| `SCENARIO_LOCKED_ACCOUNT` | user locked after 5 failures |
| `SCENARIO_EXPIRED_TOKEN` | refresh returns `TokenExpiredException` |
| `SCENARIO_SERVICE_DOWN` | every call throws `SERVICE_UNAVAILABLE` |

Usage in tests:

```java
@QuarkusTest
class LoginResourceTest {
  @InjectMock CoreAuthClient coreAuth;  // CoreAuthClientMock auto-injected by CDI Alternative
  // ... given/when/then
}
```

Spring Boot equivalent: `@MockBean CoreAuthClient coreAuth;`.

---

## 10. WireMock Testing Pattern

For HTTP-level verification (request body shape, headers, retry counting).

```java
class CoreAuthWireMockSetup {

  public static void setupValidLogin(String userRef, String password) {
    stubFor(post("/internal/core-auth/validate")
      .withRequestBody(matchingJsonPath("$.userRef", equalTo(userRef)))
      .withRequestBody(matchingJsonPath("$.credentialValue", equalTo(password)))
      .willReturn(okJson("{\"valid\": true}")));
  }

  public static void setupInvalidLogin(String userRef) {
    stubFor(post("/internal/core-auth/validate")
      .withRequestBody(matchingJsonPath("$.userRef", equalTo(userRef)))
      .willReturn(jsonResponse(
        "{\"valid\": false, \"lockoutInfo\": null}", 401)));
  }

  public static void setupLockedAccount(String userRef) {
    stubFor(post("/internal/core-auth/validate")
      .withRequestBody(matchingJsonPath("$.userRef", equalTo(userRef)))
      .willReturn(jsonResponse(
        "{\"valid\": false, \"lockoutInfo\": {\"locked\": true, " +
        "\"lockedUntil\": 1745280000000, \"failedAttempts\": 5, \"maxAttempts\": 5}}", 403)));
  }

  public static void setupTokenIssue(String userRef, Map<String, Object> claims) {
    stubFor(post("/internal/core-auth/token/issue")
      .willReturn(okJson("{\"accessToken\": \"jwt.eyJ...\", \"refreshToken\": \"opaque-...\", " +
                         "\"expiresIn\": 900, \"tokenType\": \"Bearer\"}")));
  }

  public static void setupServiceDown() {
    stubFor(any(anyUrl()).willReturn(aResponse().withStatus(503)));
  }
}
```

---

## 11. Versioning & Publishing

### 11.1 SemVer

| Bump | Trigger |
|------|---------|
| MAJOR | Breaking API change (removed method, changed signature, removed DTO field) |
| MINOR | New methods / new optional DTO fields (backward compatible) |
| PATCH | Bug fix, internal improvement, dependency bump |

### 11.2 Pipeline

- Published to internal Nexus / Artifactory: `nexus.eksad.internal/repository/maven-releases/`
- Jenkins job builds + publishes on Git tag push (`v1.0.0`)
- Consumers bump version in `pom.xml`; no other change required

### 11.3 Backward Compatibility Rules

- New DTO fields are nullable / `Optional`
- New `CoreAuthErrorCode` values are non-breaking — consumers should `switch` with `default` branch
- Deprecation: `@Deprecated(since = "1.2", forRemoval = true)` + minimum 2 minor versions before removal

---

## 12. Configuration Reference

| Property | Default | Description |
|----------|--------:|-------------|
| `eksad.core-auth.url` | (required) | Base URL of `eksad-core-auth` |
| `eksad.core-auth.connect-timeout` | 5000 ms | Connection timeout |
| `eksad.core-auth.read-timeout` | 10000 ms | Read timeout |
| `eksad.core-auth.retry-max` | 3 | Max retry attempts on transient failure |
| `eksad.core-auth.retry-delay-ms` | 500 | Base delay between retries |
| `eksad.core-auth.circuit-breaker-threshold` | 0.5 | Failure ratio to open circuit |
| `eksad.core-auth.circuit-breaker-delay` | 10000 ms | Time before HALF_OPEN probe |
| `eksad.core-auth.health-check-enabled` | true | Expose `isHealthy()` via `/q/health/ready` |

Environment override (standard mapping):

```
EKSAD_CORE_AUTH_URL=https://core-auth.eksad-prod.svc.cluster.local
EKSAD_CORE_AUTH_CONNECT_TIMEOUT=3000
```

---

## Cross-References

- Server-side auth design → `EKSAD_CORE_AUTH_PATTERNS.md`
- Timeout / Retry / CB semantics → `EKSAD_RESILIENCE_PATTERNS.md`
- Test fixtures (WireMock, CDI Alternative) → `EKSAD_TESTING_GUIDE.md` §17, §23
- Module type strings (audit) → `EKSAD_DOMAIN_REGISTRY.md`
