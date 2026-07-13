# EKSAD Spring Boot Mappings
# Quarkus Reactive → Spring Boot Imperative Pattern Equivalents

**Version:** 1.0
**Date:** 2026-04-23
**Owner:** EKSAD Platform Team
**Audience:** Developers, System Analysts, Technical Leaders working on Spring Boot projects

> **EKSAD Standard is Quarkus Reactive.**
> This file is a compatibility reference for teams whose projects use Spring Boot imperative.
> All EKSAD architecture principles (tenant_id, Flyway, soft delete, audit trail, no hard-coded secrets) still apply — only the framework layer changes.
>
> **When GPT detects "Spring Boot" in the conversation**, switch to these mappings automatically.

---

## 1. Framework Philosophy Difference

| Aspect | Quarkus Reactive (EKSAD Standard) | Spring Boot Imperative |
|--------|----------------------------------|----------------------|
| Execution model | Non-blocking event loop (Vert.x) | Thread-per-request (Tomcat/Jetty) |
| Return types | `Uni<T>`, `Multi<T>` | `T` (blocking), `CompletableFuture<T>` (async) |
| DB access | Hibernate Reactive (non-blocking) | Spring Data JPA (blocking JDBC) |
| Transaction mgmt | `@ReactiveTransactional` on method | `@Transactional` on method |
| Session scope | `@WithSession` on class | Managed by Spring automatically |
| CDI/IoC | Quarkus Arc (CDI subset) | Spring IoC (`@Component`, `@Service`, `@Repository`) |
| Error model | `Uni.createFrom().failure(e)` | `throw new Exception()` |
| Messaging | SmallRye Reactive Messaging | Spring AMQP (`spring-rabbit`) |
| JWT | SmallRye JWT | Spring Security OAuth2 Resource Server |
| REST | RESTEasy Reactive (JAX-RS) | Spring MVC (`@RestController`) |
| Config | MicroProfile Config | Spring Boot `application.properties` / `@Value` |

---

## 2. Dependency Injection Mappings

| Quarkus (EKSAD Standard) | Spring Boot Equivalent |
|--------------------------|----------------------|
| `@ApplicationScoped` | `@Service` or `@Component` |
| `@RequestScoped` | `@Scope("request")` |
| `@Singleton` | `@Component` (default singleton in Spring) |
| `@Inject` | `@Autowired` or constructor injection |
| `@Named` | `@Qualifier` |
| `@Alternative @Priority(1)` | `@Primary` or `@Profile("test")` |
| `Instance<T>` | `ApplicationContext.getBean(T)` or `@Autowired List<T>` |

**Best practice in Spring Boot:** Prefer constructor injection over `@Autowired` on fields.

```java
// ✅ Spring Boot — constructor injection (preferred)
@Service
public class TransactionService {
    private final TransactionRepository repository;

    public TransactionService(TransactionRepository repository) {
        this.repository = repository;
    }
}
```

---

## 3. Persistence Mappings

| Quarkus (EKSAD Standard) | Spring Boot Equivalent |
|--------------------------|----------------------|
| `PanacheRepositoryBase<E, I>` | `JpaRepository<E, I>` (Spring Data) |
| `@Entity` + `@Table` | Same — `@Entity` + `@Table` (Jakarta Persistence) |
| `@MappedSuperclass` | Same — `@MappedSuperclass` |
| `@WithSession` on service class | Not needed — Spring manages JPA session |
| `@ReactiveTransactional` on method | `@Transactional` on method |
| `Uni<E> persist(entity)` | `repository.save(entity)` (blocking) |
| `Uni<E> findById(id)` | `repository.findById(id)` returns `Optional<E>` |
| `findById(id).onItem().ifNull()...` | `repository.findById(id).orElseThrow(...)` |
| Hibernate Reactive (non-blocking) | Spring Data JPA (blocking JDBC) |
| `quarkus-reactive-pg-client` | `spring-boot-starter-data-jpa` + `postgresql` driver |

### BaseEntity Equivalent

```java
// Quarkus (EKSAD Standard)
@MappedSuperclass
public abstract class BaseEntity {
    private Long createdAt;
    private String createdBy;
    private Long updatedAt;
    private String updatedBy;
    private Long deletedAt;
    private String deletedBy;
}

// Spring Boot — same structure, same fields (Long timestamps)
@MappedSuperclass
public abstract class BaseEntity {
    @Column(name = "created_at", nullable = false)
    private Long createdAt;
    @Column(name = "created_by", nullable = false)
    private String createdBy;
    @Column(name = "updated_at")
    private Long updatedAt;
    @Column(name = "updated_by")
    private String updatedBy;
    @Column(name = "deleted_at")
    private Long deletedAt;
    @Column(name = "deleted_by")
    private String deletedBy;
}
```

---

## 4. CrudFlows / BaseRepository Equivalent in Spring Boot

In Quarkus, `BaseRepository` provides auto-audited CRUD via reactive flows.
In Spring Boot imperative, this becomes an **abstract service class** (not repository layer):

```java
// Spring Boot equivalent of BaseRepository
@Transactional
public abstract class BaseService<E, D, ID> {

    protected abstract JpaRepository<E, ID> getRepository();
    protected abstract UserContext getUserContext();
    protected abstract LogHandler getLogHandler();
    protected abstract String moduleType();

    protected abstract ID toId(D dto);
    protected abstract String extractEntityId(E entity);
    protected abstract E toNewEntity(D dto);

    // CREATE flow — equivalent of createFlow()
    public E createEntity(D dto, String moduleType) {
        LogActivityDTO log = getLogHandler().buildBaseLog(dto, null, moduleType);
        E entity = toNewEntity(dto);
        E saved = getRepository().save(entity);
        getLogHandler().logSuccess(log, extractEntityId(saved), saved); // fire async
        return saved;
    }

    // UPDATE flow — equivalent of updateFlow()
    public E updateEntity(ID id, Consumer<E> mutator, String moduleType) {
        LogActivityDTO log = getLogHandler().buildBaseLog(id, id.toString(), moduleType);
        E entity = getRepository().findById(id)
                .orElseThrow(() -> getLogHandler().logFailureAndThrow(log, "Data not found"));
        mutator.accept(entity);
        E updated = getRepository().save(entity);
        getLogHandler().logSuccess(log, extractEntityId(updated), updated);
        return updated;
    }

    // SOFT DELETE flow — equivalent of deleteFlow()
    public E deleteEntity(ID id, String moduleType) {
        return updateEntity(id, entity -> {
            try {
                entity.getClass().getMethod("setDeletedAt", Long.class)
                      .invoke(entity, Instant.now().toEpochMilli());
                entity.getClass().getMethod("setDeletedBy", String.class)
                      .invoke(entity, getUserContext().getUser());
            } catch (Exception ignore) {}
        }, moduleType);
    }
}
```

### Audit Fire-and-Forget in Spring Boot

Replace `MutinyEmitter` with `@Async` + `RabbitTemplate`:

```java
// Spring Boot LogHandler — async fire-and-forget
@Component
public class LogHandler {

    @Autowired
    private RabbitTemplate rabbitTemplate;

    @Async  // ← non-blocking, runs in separate thread pool
    public void logSuccess(LogActivityDTO log, String txId, Object afterState) {
        log.setTransactionId(txId);
        log.setResponseTime(Instant.now().toEpochMilli());
        log.setDataAfter(new ObjectMapper().writeValueAsString(afterState));
        log.setStatus("SUCCESS");
        rabbitTemplate.convertAndSend("exc-log-activity", "r.q-log-activity-eksad",
                new ObjectMapper().writeValueAsString(log));
    }
}
```

Enable `@Async` in Spring Boot:
```java
@Configuration
@EnableAsync
public class AsyncConfig { }
```

---

## 5. REST / HTTP Layer Mappings

| Quarkus (EKSAD Standard) | Spring Boot Equivalent |
|--------------------------|----------------------|
| `@Path("/api/v1/resource")` | `@RequestMapping("/api/v1/resource")` on class |
| `@GET` | `@GetMapping` |
| `@POST` | `@PostMapping` |
| `@PUT` | `@PutMapping` |
| `@PATCH` | `@PatchMapping` |
| `@DELETE` | `@DeleteMapping` |
| `@PathParam("id")` | `@PathVariable Long id` |
| `@QueryParam("page")` | `@RequestParam int page` |
| `@RolesAllowed({"ROLE_ADMIN"})` | `@PreAuthorize("hasRole('ADMIN')")` |
| `@Produces(APPLICATION_JSON)` | Not needed — `@RestController` defaults to JSON |
| `@Consumes(APPLICATION_JSON)` | Not needed — `@RequestBody` handles this |
| `Uni<Response>` return | `ResponseEntity<T>` return |
| `Response.status(201).entity(dto)` | `ResponseEntity.status(HttpStatus.CREATED).body(dto)` |
| `@Tag(name = "...")` (OpenAPI) | `@Tag(name = "...")` (same — springdoc-openapi) |

```java
// Quarkus
@POST
@RolesAllowed({"ROLE_ADMIN"})
public Uni<Response> create(TransactionDTO dto) {
    return service.create(dto)
            .map(e -> Response.status(201).entity(e).build());
}

// Spring Boot equivalent
@PostMapping
@PreAuthorize("hasRole('ADMIN')")
public ResponseEntity<TransactionEntity> create(@RequestBody TransactionDTO dto) {
    TransactionEntity saved = service.create(dto);
    return ResponseEntity.status(HttpStatus.CREATED).body(saved);
}
```

---

## 6. Security / JWT Mappings

| Quarkus (EKSAD Standard) | Spring Boot Equivalent |
|--------------------------|----------------------|
| `quarkus-smallrye-jwt` | `spring-security-oauth2-resource-server` |
| `mp.jwt.verify.issuer=...` | `spring.security.oauth2.resourceserver.jwt.issuer-uri=...` |
| `mp.jwt.verify.publickey.location=...` | `spring.security.oauth2.resourceserver.jwt.public-key-location=...` |
| `@Inject JsonWebToken jwt` | `@AuthenticationPrincipal Jwt jwt` |
| `jwt.getClaim("eksad_tenant_id")` | `jwt.getClaim("eksad_tenant_id")` |
| `@RolesAllowed({"ROLE_ADMIN"})` | `@PreAuthorize("hasRole('ADMIN')")` |
| `@PermitAll` | `@PermitAll` or omit `@PreAuthorize` + configure `permitAll()` |

### Spring Boot Security Config

```java
@Configuration
@EnableWebSecurity
@EnableMethodSecurity
public class SecurityConfig {

    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        http
            .authorizeHttpRequests(auth -> auth
                .requestMatchers("/api/v1/auth/**").permitAll()
                .anyRequest().authenticated()
            )
            .oauth2ResourceServer(oauth2 -> oauth2.jwt(Customizer.withDefaults()));
        return http.build();
    }
}
```

### UserContext Equivalent in Spring Boot

```java
@Component
@RequestScope
public class UserContext {

    @Autowired
    private HttpServletRequest request;

    public String getUser() {
        Jwt jwt = extractJwt();
        return jwt != null ? jwt.getSubject() : "SYSTEM";
    }

    public String getRole() {
        Jwt jwt = extractJwt();
        if (jwt == null) return "GUEST";
        return Optional.ofNullable(jwt.getClaim("eksad_role"))
                       .map(Object::toString).orElse("GUEST");
    }

    public String getTenantId() {
        Jwt jwt = extractJwt();
        if (jwt == null) return null;
        return jwt.getClaim("eksad_tenant_id");
    }

    private Jwt extractJwt() {
        Authentication auth = SecurityContextHolder.getContext().getAuthentication();
        if (auth != null && auth.getCredentials() instanceof Jwt) {
            return (Jwt) auth.getCredentials();
        }
        return null;
    }
}
```

---

## 7. Messaging (RabbitMQ) Mappings

| Quarkus (EKSAD Standard) | Spring Boot Equivalent |
|--------------------------|----------------------|
| `quarkus-messaging-rabbitmq` | `spring-boot-starter-amqp` |
| `@Incoming("channel-name")` | `@RabbitListener(queues = "queue-name")` |
| `@Outgoing("channel-name")` | `rabbitTemplate.convertAndSend(exchange, routingKey, msg)` |
| `@Channel("out-x") MutinyEmitter<String>` | `@Autowired RabbitTemplate rabbitTemplate` |
| `emitter.sendAndForget(payload)` | `@Async rabbitTemplate.convertAndSend(...)` |
| `mp.messaging.incoming.{ch}.queue.name=...` | `@RabbitListener(queues = "queue-name")` directly |

```java
// Quarkus consumer
@Incoming("in-log-activity")
public Uni<String> consume(String message) { ... }

// Spring Boot equivalent consumer
@RabbitListener(queues = "q-log-activity-eksad")
public void consume(String message) { ... }
```

```java
// Spring Boot RabbitMQ config — declare exchange + queue + binding
@Configuration
public class RabbitConfig {

    @Bean
    public DirectExchange logActivityExchange() {
        return new DirectExchange("exc-log-activity", true, false);
    }

    @Bean
    public Queue logActivityQueue() {
        return QueueBuilder.durable("q-log-activity-eksad").build();
    }

    @Bean
    public Binding logActivityBinding() {
        return BindingBuilder
                .bind(logActivityQueue())
                .to(logActivityExchange())
                .with("r.q-log-activity-eksad");
    }
}
```

### 7.1 Master Data Cache Consumer Mapping

For domain services that consume `exc-master-data` (topic) events into local `_cache` tables — see `EKSAD_CACHE_SYNC_PATTERNS.md` for the Quarkus pattern.

| Quarkus (EKSAD Standard) | Spring Boot Equivalent |
|--------------------------|------------------------|
| `@Incoming("master-data-events")` consumer method | `@RabbitListener(queues = "q-master-sync-{service}")` on a `@Component` |
| `@Channel("master-data-out") MutinyEmitter` publisher | `@Autowired RabbitTemplate` + `convertAndSend("exc-master-data", routingKey, payload)` |
| Topic exchange binding via `mp.messaging.incoming.{ch}.exchange.name=exc-master-data` + routing-key `r.brand.*` | `TopicExchange("exc-master-data")` bean + `Binding` with routing-key pattern |
| `@Observes StartupEvent` → startup cache sync via `@RegisterRestClient` | `@EventListener(ApplicationReadyEvent.class)` → cache sync via `WebClient` / `RestTemplate` |
| Cache repository `extends PanacheRepositoryBase` (no audit) | Cache repository `extends JpaRepository` (no `@Auditable`) |

```java
// Spring Boot master-data event consumer
@Component
@RequiredArgsConstructor
public class MasterDataEventConsumer {
    private final BrandCacheRepository cache;

    @RabbitListener(queues = "q-master-sync-pipeline")
    public void onEvent(MasterDataEvent evt) {
        if (evt.occurredAt() <= cache.maxLastSyncedAt()) return; // stale
        switch (evt.eventType()) {
            case "BRAND.CREATED", "BRAND.UPDATED" -> cache.upsert(evt.payload());
            case "BRAND.DELETED"                  -> cache.deleteById(evt.payload().id());
            default                               -> log.warn("Unknown {}", evt.eventType());
        }
    }
}

@Configuration
public class MasterDataRabbitConfig {
    @Bean TopicExchange masterDataExchange() { return new TopicExchange("exc-master-data", true, false); }
    @Bean Queue masterSyncQueue() { return QueueBuilder.durable("q-master-sync-pipeline").build(); }
    @Bean Binding brandBinding(Queue q, TopicExchange ex) {
        return BindingBuilder.bind(q).to(ex).with("r.brand.*");
    }
}

// Startup sync — Spring Boot
@Component
@RequiredArgsConstructor
public class BrandStartupSync {
    private final BrandCacheRepository cache;
    private final MasterDataRestClient client;   // WebClient/RestTemplate-backed

    @EventListener(ApplicationReadyEvent.class)
    public void syncOnStartup() {
        if (cache.count() == 0) cache.saveAll(client.listBrands());
    }
}
```

---

## 8. Flyway & Database Mappings

Flyway works **identically** in both frameworks. The same SQL migration files apply with no changes.

| Property | Quarkus | Spring Boot |
|----------|---------|------------|
| Enable | `quarkus.flyway.migrate-at-start=true` | `spring.flyway.enabled=true` |
| Locations | `quarkus.flyway.locations=db/migration` | `spring.flyway.locations=classpath:db/migration` |
| Baseline | `quarkus.flyway.baseline-on-migrate=true` | `spring.flyway.baseline-on-migrate=true` |
| DDL auto | `quarkus.hibernate-orm.database.generation=none` | `spring.jpa.hibernate.ddl-auto=none` |

> ⚠️ **`spring.jpa.hibernate.ddl-auto=update` is FORBIDDEN in EKSAD — same rule as Quarkus.**

---

## 9. Testing Mappings

| Quarkus (EKSAD Standard) | Spring Boot Equivalent |
|--------------------------|----------------------|
| `@QuarkusTest` | `@SpringBootTest` |
| `@TestHTTPEndpoint(Resource.class)` | `@AutoConfigureMockMvc` or `@WebMvcTest` |
| `@QuarkusTestResource(Container.class)` | `@DynamicPropertySource` + Testcontainers |
| REST Assured (same library) | REST Assured or `MockMvc` |
| `@Alternative @Priority(1)` mock bean | `@MockBean` or `@TestConfiguration` with `@Primary` |
| `Uni.await().indefinitely()` | Not needed — blocking return |
| `UniAssertSubscriber` | Standard JUnit assertions |

```java
// Spring Boot integration test
@SpringBootTest(webEnvironment = WebEnvironment.RANDOM_PORT)
@AutoConfigureMockMvc
class TransactionResourceTest {

    @Autowired MockMvc mockMvc;

    @MockBean TransactionRepository repository;

    @Test
    void create_validPayload_returns201() throws Exception {
        mockMvc.perform(post("/api/v1/transactions")
                .header("Authorization", "Bearer " + adminToken())
                .contentType(MediaType.APPLICATION_JSON)
                .content("""{ "type": "CREDIT", "amount": 1000.0000 }"""))
            .andExpect(status().isCreated())
            .andExpect(jsonPath("$.type").value("CREDIT"));
    }
}
```

---

## 10. application.properties Mappings

```properties
# ─── Quarkus (EKSAD Standard) ──────────────────────────────
quarkus.http.port=${PORT:8080}
quarkus.datasource.reactive.url=${DB_REACTIVE_URL}
quarkus.hibernate-orm.database.generation=none
quarkus.flyway.migrate-at-start=true
mp.jwt.verify.issuer=eksad-auth-service

# ─── Spring Boot Equivalent ────────────────────────────────
server.port=${PORT:8080}
spring.datasource.url=${DB_URL}
spring.datasource.username=${DB_USERNAME}
spring.datasource.password=${DB_PASSWORD}
spring.jpa.hibernate.ddl-auto=none
spring.flyway.enabled=true
spring.flyway.baseline-on-migrate=true
spring.security.oauth2.resourceserver.jwt.issuer-uri=eksad-auth-service
spring.rabbitmq.host=${RABBITMQ_HOST}
spring.rabbitmq.port=${RABBITMQ_PORT:5672}
spring.rabbitmq.username=${RABBITMQ_USERNAME}
spring.rabbitmq.password=${RABBITMQ_PASSWORD}
spring.rabbitmq.virtual-host=${RABBITMQ_VHOST:eksad_vhost}
```

---

## 11. What Does NOT Change Between Frameworks

These EKSAD principles apply **identically** regardless of framework:

| Principle | Quarkus | Spring Boot |
|-----------|---------|------------|
| `tenant_id` on every entity | ✅ Same | ✅ Same |
| Soft delete (`deleted_at`, `deleted_by`) | ✅ Same | ✅ Same |
| `Long` epoch ms timestamps | ✅ Same | ✅ Same |
| `NUMERIC(20,4)` / `BigDecimal` for finance | ✅ Same | ✅ Same |
| Flyway only (no `ddl-auto`) | ✅ Same | ✅ Same |
| No hard-coded secrets (`${ENV_VAR}`) | ✅ Same | ✅ Same |
| Module type format `<PROJECT>.<MODULE>.<ACTION>` | ✅ Same | ✅ Same |
| Audit trail to RabbitMQ → MongoDB | ✅ Same pattern | ✅ Async via `@Async RabbitTemplate` |
| RBAC on every endpoint | `@RolesAllowed` | `@PreAuthorize` |
| API versioning `/api/v{N}/` | ✅ Same | ✅ Same |
