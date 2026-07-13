# EKSAD Reserved Field Patterns

| Meta | Value |
|------|-------|
| **Version** | 1.0 |
| **Date** | 2026-05-23 |
| **Owner** | EKSAD Platform Team |
| **Audience** | Developers, Architects, BA, SA |
| **Priority** | 🔴 P0 |
| **Related** | Decision 8 (Hybrid Approach C); `EKSAD_CODING_STANDARDS.md` §18 |

---

## Table of Contents

1. [Overview & Rationale](#1-overview--rationale)
2. [Approach C — Hybrid Design](#2-approach-c--hybrid-design)
3. [Opt-In Model](#3-opt-in-model)
4. [Reserved Column Layout](#4-reserved-column-layout)
5. [`reserved_field_config` Table](#5-reserved_field_config-table)
6. [Config Cascade (tenant → domain → global)](#6-config-cascade-tenant--domain--global)
7. [Entity Pattern (`BaseTransactionalEntity`)](#7-entity-pattern-basetransactionalentity)
8. [Validation Hook (Simple / Conditional / Multiple Rules)](#8-validation-hook-simple--conditional--multiple-rules)
9. [API & Frontend Integration](#9-api--frontend-integration)
10. [DTO & Mapper Pattern](#10-dto--mapper-pattern)
11. [JSONB Overflow](#11-jsonb-overflow)
12. [BA / SA Workflow](#12-ba--sa-workflow)
13. [Flyway Migration Template](#13-flyway-migration-template)
14. [Testing](#14-testing)
15. [Anti-Patterns](#15-anti-patterns)
16. [FAQ](#16-faq)

---

## 1. Overview & Rationale

**Problem:** Each tenant wants project-specific custom fields on transactional entities (e.g., orders, leads, attendance) — but adding columns per tenant requires DDL migrations, deployments, and code changes. Multi-tenant SaaS cannot do that.

**Solution:** Pre-allocate generic "reserved" columns on transactional entities. Tenants configure **display labels, visibility, and validation** via a config table — **zero code change** per tenant.

> ⚠️ Reserved fields are **OPT-IN** per entity, not mandatory. Master data, cache tables, and audit logs are exempt.

---

## 2. Approach C — Hybrid Design

12 typed slots + 1 JSONB overflow = flexible but indexable.

| Slot Type | Count | Use Case |
|-----------|-------|----------|
| `VARCHAR(500)` (string) | 5 | Free-text custom fields |
| `NUMERIC(20,4)` (numeric) | 3 | Custom amounts/quantities |
| `BIGINT` (date — epoch ms) | 2 | Custom dates |
| `BOOLEAN` (boolean) | 2 | Flags / yes-no |
| `JSONB` (overflow) | 1 | Ad-hoc additional fields beyond 12 slots |

**Why Hybrid:**
- Typed slots → indexed queries possible (per-tenant filtered indexes).
- JSONB → flexibility for tenants with unusual needs.
- Most tenants use 0–5 slots; power users may use JSONB for the rest.

---

## 3. Opt-In Model

Entities **explicitly extend** `BaseTransactionalEntity` to gain reserved fields. Do NOT bolt onto everything.

| Entity Type | Opt-in to reserved fields? |
|-------------|----------------------------|
| Transactional (orders, leads, submissions, …) | ✅ Optional opt-in |
| Master data (brands, departments, …) | ❌ Never |
| Cache tables (`*_cache`) | ❌ Never |
| Audit logs | ❌ Never |
| Auth (credentials, tokens) | ❌ Never |

---

## 4. Reserved Column Layout

```sql
-- These 13 columns are added by BaseTransactionalEntity
reserved_str_1     VARCHAR(500),
reserved_str_2     VARCHAR(500),
reserved_str_3     VARCHAR(500),
reserved_str_4     VARCHAR(500),
reserved_str_5     VARCHAR(500),
reserved_num_1     NUMERIC(20,4),
reserved_num_2     NUMERIC(20,4),
reserved_num_3     NUMERIC(20,4),
reserved_date_1    BIGINT,
reserved_date_2    BIGINT,
reserved_bool_1    BOOLEAN,
reserved_bool_2    BOOLEAN,
reserved_ext       JSONB        DEFAULT '{}'::jsonb
```

**Indexing (per tenant if needed):**
```sql
-- Example: tenant-AHM uses reserved_str_1 as "Salesperson Code" frequently
CREATE INDEX idx_orders_ahm_salesperson
  ON orders (reserved_str_1)
  WHERE tenant_id = 'tenant-ahm';
```

---

## 5. `reserved_field_config` Table

Lives in `eksad_tenants` (MongoDB) or per-service config DB. Defines what each slot means per tenant.

```javascript
// MongoDB collection: reserved_field_config
{
  _id: ObjectId,
  scope_type: "tenant",                          // "global" | "domain" | "tenant"
  scope_id:   "tenant-ahm",                      // tenant_id, domain name, or "global"
  entity:     "orders",                          // entity table name
  slot:       "reserved_str_1",                  // which slot
  label:      "Salesperson Code",                // display label
  visible:    true,                              // show in UI?
  required:   false,                             // mandatory?
  data_type:  "string",                          // string | numeric | date | boolean
  validation: {                                  // optional validation rules
    pattern:   "^SP[0-9]{4}$",
    max_length: 8,
    min_value:  null,
    max_value:  null,
    enum:       null
  },
  created_at: 1745280000000,
  updated_at: 1745280000000
}
```

### Indexes
- `{ scope_type: 1, scope_id: 1, entity: 1, slot: 1 }` unique
- `{ entity: 1 }`

---

## 6. Config Cascade (tenant → domain → global)

Resolution order when computing the **effective config** for a tenant + entity + slot:

```
effective(slot) = tenant-level OR domain-level OR global-default
```

```pseudo
function resolveReservedFieldConfig(tenantId, entity, slot):
    cfg = find(scope_type=tenant, scope_id=tenantId, entity=entity, slot=slot)
    if cfg exists → return cfg
    domain = domainOfTenant(tenantId)
    cfg = find(scope_type=domain, scope_id=domain, entity=entity, slot=slot)
    if cfg exists → return cfg
    cfg = find(scope_type=global, entity=entity, slot=slot)
    if cfg exists → return cfg
    return { visible: false }   // default: hidden
```

**Caching:** resolved configs cached (Redis or local) with 5-min TTL, invalidated on config update.

---

## 7. Entity Pattern (`BaseTransactionalEntity`)

Lives in `eksad-core-common`.

```java
@MappedSuperclass
@Data
@EqualsAndHashCode(callSuper = true)
@SuperBuilder
@NoArgsConstructor
@AllArgsConstructor
public abstract class BaseTransactionalEntity extends BaseEntity {

    @Column(name = "reserved_str_1", length = 500)
    private String reservedStr1;
    @Column(name = "reserved_str_2", length = 500)
    private String reservedStr2;
    @Column(name = "reserved_str_3", length = 500)
    private String reservedStr3;
    @Column(name = "reserved_str_4", length = 500)
    private String reservedStr4;
    @Column(name = "reserved_str_5", length = 500)
    private String reservedStr5;

    @Column(name = "reserved_num_1", precision = 20, scale = 4)
    private BigDecimal reservedNum1;
    @Column(name = "reserved_num_2", precision = 20, scale = 4)
    private BigDecimal reservedNum2;
    @Column(name = "reserved_num_3", precision = 20, scale = 4)
    private BigDecimal reservedNum3;

    @Column(name = "reserved_date_1")
    private Long reservedDate1;
    @Column(name = "reserved_date_2")
    private Long reservedDate2;

    @Column(name = "reserved_bool_1")
    private Boolean reservedBool1;
    @Column(name = "reserved_bool_2")
    private Boolean reservedBool2;

    @Column(name = "reserved_ext", columnDefinition = "jsonb")
    @JdbcTypeCode(SqlTypes.JSON)
    private Map<String, Object> reservedExt;
}
```

**Domain entity opting in:**
```java
@Entity
@Table(name = "orders")
@SuperBuilder
@Data
@NoArgsConstructor
@AllArgsConstructor
public class OrderEntity extends BaseTransactionalEntity {
    // ... regular columns
}
```

---

## 8. Validation Hook (Simple / Conditional / Multiple Rules)

### 8.1 Simple Rules

Invoke at create/update boundary in the service layer:

```java
@ApplicationScoped
public class ReservedFieldValidator {

    @Inject ReservedFieldConfigResolver resolver;
    @Inject TenantContext tenantContext;

    public void validate(String entity, BaseTransactionalEntity e) {
        Map<String, Object> values = extractReservedValues(e);
        List<String> errors = new ArrayList<>();
        for (var entry : values.entrySet()) {
            String slot  = entry.getKey();
            Object value = entry.getValue();
            ReservedFieldConfig cfg = resolver.resolve(tenantContext.getTenantId(), entity, slot);
            if (cfg == null || !cfg.visible()) continue;

            if (cfg.required() && value == null) {
                errors.add(cfg.label() + " is required");
                continue;
            }
            if (cfg.validation() != null)
                applyRules(cfg, value, errors);
        }
        if (!errors.isEmpty())
            throw new ValidationException(String.join("; ", errors));   // ← aggregate, not first-fail
    }

    private void applyRules(ReservedFieldConfig cfg, Object value, List<String> errors) {
        /* regex, range, enum — each rule appends to errors list */
    }
}
```

Call from service:
```java
@ReactiveTransactional
public Uni<OrderEntity> create(OrderDTO dto) {
    return Uni.createFrom().item(() -> {
        OrderEntity entity = mapper.toEntity(dto);
        validator.validate("orders", entity);
        return entity;
    }).flatMap(repository::create);
}
```

---

### 8.2 Conditional Rules

A slot may be required / hidden / regex-changed **based on another slot's value**. Modeled via `conditions[]` in config:

```javascript
// reserved_field_config example — conditional required
{
  scope_type: "tenant", scope_id: "tenant-ahm", entity: "orders",
  slot: "reserved_str_3", label: "Promo Code",
  visible: true, required: false,
  conditions: [
    { when: { slot: "reserved_str_2", op: "eq", value: "PROMO" },
      then: { required: true } },
    { when: { slot: "reserved_num_1", op: "gt", value: 1000000 },
      then: { required: true } }
  ]
}
```

**Supported operators:** `eq` / `neq` / `gt` / `gte` / `lt` / `lte` / `in` / `notIn` / `isNull` / `isNotNull`.

**Java evaluation:**
```java
private ReservedFieldConfig applyConditions(ReservedFieldConfig base,
                                            Map<String, Object> values) {
    if (base.conditions() == null) return base;
    ReservedFieldConfig effective = base;
    for (ConditionalRule rule : base.conditions()) {
        Object actual = values.get(rule.when().slot());
        if (matches(rule.when().op(), actual, rule.when().value())) {
            effective = effective.mergeWith(rule.then());   // ← later-wins merge
        }
    }
    return effective;
}
```

> ⚠️ Conditions evaluate **left-to-right, later wins** on conflict. Document this in the BA Reserved Field Config Document so business owners don't get surprised.

---

### 8.3 Multiple Rules + Composition

A single slot may carry multiple validation rules — combine with AND / OR + always aggregate errors:

```javascript
// reserved_field_config — multi-rule composition
{
  slot: "reserved_str_1", label: "Salesperson Code",
  validation: {
    composition: "AND",                           // "AND" | "OR"
    rules: [
      { type: "pattern",   value: "^SP[0-9]{4}$",   message: "Must be SP#### format" },
      { type: "maxLength", value: 8,                message: "Max 8 chars" },
      { type: "notIn",     value: ["SP0000"],       message: "SP0000 reserved" }
    ]
  }
}
```

**Java composition:**
```java
private void applyRules(ReservedFieldConfig cfg, Object value, List<String> errors) {
    Validation v = cfg.validation();
    List<String> failed = new ArrayList<>();
    for (Rule r : v.rules()) {
        if (!r.test(value)) failed.add(r.message());
    }
    boolean violates = switch (v.composition()) {
        case "AND" -> !failed.isEmpty();             // any fail → violation
        case "OR"  -> failed.size() == v.rules().size(); // ALL fail → violation
        default    -> !failed.isEmpty();
    };
    if (violates) errors.addAll(failed);             // ← aggregate ALL failed rule messages
}
```

| Composition | Semantics | Use Case |
|-------------|-----------|----------|
| `AND` (default) | All rules must pass; on failure return **all** failed messages | Standard validation chain |
| `OR` | At least one rule must pass; on total failure return all messages | Tenant-A accepts either pattern X or pattern Y |

> ✅ **Always aggregate.** Never throw on first-fail — frontend needs all errors at once for a good UX.

---

## 9. API & Frontend Integration

### 9.1 Schema Endpoint
Frontend asks the backend "what fields do I show?":

```
GET /api/v1/orders/_schema
Authorization: Bearer <jwt>

Response:
{
  "standardFields": [...],
  "reservedFields": [
    { "slot": "reserved_str_1", "label": "Salesperson Code", "required": false,
      "dataType": "string", "validation": { "pattern": "^SP[0-9]{4}$" } },
    { "slot": "reserved_num_1", "label": "Discount %",       "required": true,
      "dataType": "numeric" }
  ]
}
```

Backend resolves the effective config per JWT's `tenant_id`.

### 9.2 Storing Values
The DTO carries reserved fields directly:
```json
POST /api/v1/orders
{
  "customer_id": 42,
  "amount": 100000.0000,
  "reserved_str_1": "SP1234",
  "reserved_num_1": 5.0000,
  "reserved_ext": { "marketing_source": "Instagram Ad" }
}
```

---

### 9.3 React Hook — `useReservedFields`

```typescript
// src/hooks/useReservedFields.ts
import { useEffect, useState } from "react";
import { api } from "@/lib/api";

export interface ReservedFieldConfig {
  slot: string;                   // "reserved_str_1"
  label: string;                  // "Salesperson Code"
  required: boolean;
  dataType: "string" | "numeric" | "date" | "boolean" | "jsonb";
  validation?: {
    pattern?: string;
    maxLength?: number;
    minValue?: number;
    maxValue?: number;
    enum?: string[];
  };
}

export function useReservedFields(entity: string) {
  const [fields, setFields] = useState<ReservedFieldConfig[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.get(`/api/v1/${entity}/_schema`)
      .then(r => setFields(r.data.reservedFields ?? []))
      .finally(() => setLoading(false));
  }, [entity]);

  return { fields, loading };
}
```

---

### 9.4 Input-Type Mapping (per Slot Prefix)

| Slot Prefix | HTML Input | Notes |
|-------------|-----------|-------|
| `reserved_str_*` | `<input type="text" maxLength={validation.maxLength}>` | Apply `pattern` attr if regex present |
| `reserved_num_*` | `<input type="number" min={validation.minValue} max={validation.maxValue} step="0.0001">` | Cast to `BigDecimal` on server |
| `reserved_date_*` | `<input type="date">` + epoch-ms convert helper | DB stores `BIGINT` epoch ms — convert via `toEpochMs(value)` / `fromEpochMs(value)` |
| `reserved_bool_*` | `<input type="checkbox">` | Tri-state if `required=false` (null allowed) |
| `reserved_ext` | `<KeyValueEditor />` | Custom component — key (str) + value (str/num/bool/json) per row |

---

### 9.5 Dynamic Form Render Example

```tsx
// src/components/OrderReservedFields.tsx
import { useReservedFields } from "@/hooks/useReservedFields";

const toInputType = (dt: string) => ({
  string:  "text",
  numeric: "number",
  date:    "date",
  boolean: "checkbox",
}[dt] ?? "text");

const epochToDate = (ms?: number) =>
  ms ? new Date(ms).toISOString().slice(0, 10) : "";
const dateToEpoch = (s: string) =>
  s ? new Date(s).getTime() : null;

export function OrderReservedFields({ value, onChange }) {
  const { fields, loading } = useReservedFields("orders");
  if (loading) return <div>Loading…</div>;

  return (
    <>
      {fields.map(f => {
        const isDate = f.dataType === "date";
        const isJsonb = f.dataType === "jsonb";
        if (isJsonb) {
          return <KeyValueEditor key={f.slot} value={value[f.slot]}
                                  onChange={v => onChange(f.slot, v)} />;
        }
        return (
          <label key={f.slot}>
            {f.label}{f.required && " *"}
            <input
              type={toInputType(f.dataType)}
              required={f.required}
              pattern={f.validation?.pattern}
              maxLength={f.validation?.maxLength}
              min={f.validation?.minValue}
              max={f.validation?.maxValue}
              value={isDate ? epochToDate(value[f.slot]) : (value[f.slot] ?? "")}
              onChange={e => onChange(
                f.slot,
                isDate ? dateToEpoch(e.target.value) : e.target.value
              )}
            />
          </label>
        );
      })}
    </>
  );
}
```

> See `EKSAD_FRONTEND_CODING_STANDARDS.md` §Reserved Field for the canonical component naming + Storybook story conventions.

---

## 10. DTO & Mapper Pattern

### 10.1 DTO

Reserved-field DTOs are plain records / POJOs with one field per slot — **never** a `Map<String, Object>` for typed slots (that defeats type safety). Use a `Map<String, Object>` only for `reserved_ext`.

```java
public record OrderDTO(
    Long      id,
    Long      customerId,
    BigDecimal amount,

    // ── Reserved typed slots (snake_case → camelCase via @JsonProperty) ──
    @JsonProperty("reserved_str_1")  String reservedStr1,
    @JsonProperty("reserved_str_2")  String reservedStr2,
    @JsonProperty("reserved_str_3")  String reservedStr3,
    @JsonProperty("reserved_str_4")  String reservedStr4,
    @JsonProperty("reserved_str_5")  String reservedStr5,
    @JsonProperty("reserved_num_1")  BigDecimal reservedNum1,
    @JsonProperty("reserved_num_2")  BigDecimal reservedNum2,
    @JsonProperty("reserved_num_3")  BigDecimal reservedNum3,
    @JsonProperty("reserved_date_1") Long reservedDate1,
    @JsonProperty("reserved_date_2") Long reservedDate2,
    @JsonProperty("reserved_bool_1") Boolean reservedBool1,
    @JsonProperty("reserved_bool_2") Boolean reservedBool2,

    // ── Overflow ──
    @JsonProperty("reserved_ext")    Map<String, Object> reservedExt
) {}
```

### 10.2 Mapper (MapStruct)

```java
@Mapper(componentModel = "cdi", nullValuePropertyMappingStrategy = NullValuePropertyMappingStrategy.IGNORE)
public interface OrderMapper {

    // Standard mapping — MapStruct auto-passes all reserved* fields by name match
    OrderEntity toEntity(OrderDTO dto);
    OrderDTO    toDto   (OrderEntity entity);

    // Patch (PATCH endpoint) — ignore nulls so caller can omit untouched reserved slots
    @BeanMapping(nullValuePropertyMappingStrategy = NullValuePropertyMappingStrategy.IGNORE)
    void patch(OrderDTO dto, @MappingTarget OrderEntity entity);
}
```

**Null-handling rule:**
| Operation | Behavior on `null` reserved field |
|-----------|-----------------------------------|
| `POST` (create) | `null` persisted as `NULL` (slot left empty) |
| `PUT` (replace) | `null` overwrites existing value with `NULL` |
| `PATCH` (partial) | `null` **ignored** — existing value retained |

> ⚠️ Do not hand-roll mappers — MapStruct handles the 13-field passthrough trivially; manual code drifts when slots are added.

---

## 11. JSONB Overflow

### 11.1 When to Use

Use `reserved_ext` when a tenant needs more than 12 typed slots, or for ad-hoc per-tenant key-value pairs.

```json
"reserved_ext": {
  "marketing_source":   "Instagram Ad",
  "referral_partner":   "Partner-42",
  "internal_campaign":  { "id": "C-001", "phase": "kickoff" }
}
```

### 11.2 Functional Index (per Tenant, Single Key)

```sql
CREATE INDEX idx_orders_ahm_marketing
  ON orders ((reserved_ext->>'marketing_source'))
  WHERE tenant_id = 'tenant-ahm';
```

### 11.3 Rules

- Avoid storing values that need strict typing/validation in JSONB — prefer typed slots.
- Don't index JSONB globally — only per tenant where needed.

### 11.4 GIN Index (Whole-Document Queries)

When a tenant needs to query **arbitrary keys** within `reserved_ext` (not just one known key), use a GIN index:

```sql
-- Whole-document GIN index — supports @> / ? / ?| / ?& operators
CREATE INDEX idx_orders_ahm_reserved_ext_gin
  ON orders USING GIN (reserved_ext)
  WHERE tenant_id = 'tenant-ahm';

-- jsonb_path_ops variant — smaller index, faster @> but does NOT support ? / ?| / ?&
CREATE INDEX idx_orders_ahm_reserved_ext_gin_path
  ON orders USING GIN (reserved_ext jsonb_path_ops)
  WHERE tenant_id = 'tenant-ahm';
```

| Index Type | Storage | Operators Supported | Use When |
|-----------|---------|---------------------|----------|
| **Functional** `((reserved_ext->>'key'))` | Smallest | `=`, `<`, range (single known key) | One specific key queried often |
| **GIN** `(reserved_ext)` | Medium | `@>`, `?`, `?\|`, `?&` | Multiple/unknown keys, containment |
| **GIN `jsonb_path_ops`** | Smallest GIN | `@>` only | Containment-only, write-heavy table |

### 11.5 Sprint Phasing (Optional Sprint 1)

> 📌 **JSONB overflow is OPTIONAL in Sprint 1.** Typed slots (12 columns) cover the vast majority of tenant requirements at v1 launch. Introduce `reserved_ext` + GIN indexes in **Sprint 2+** only if a power tenant explicitly requests >12 custom fields or ad-hoc key-value storage. Premature JSONB adoption complicates validation and indexing.

---

## 12. BA / SA Workflow

### 12.1 Discovery Prompt

During FSD creation, the BA should proactively ask:

> "Does this tenant need any custom fields on `[entity]` that aren't in the standard schema?"

Then the SA documents in TSD:

| Tenant | Entity | Slot | Label | Validation |
|--------|--------|------|-------|-----------|
| AHM | orders | `reserved_str_1` | Salesperson Code | `^SP[0-9]{4}$` |
| AHM | orders | `reserved_num_1` | Discount % | 0–30 |

Reserved field discovery workflow detail is in `EKSAD_BA_INSTRUCTIONS.md` (Decision 10).

---

### 12.2 Reserved Field Config Document (Deliverable Template)

The BA produces a **Reserved Field Config Document** per tenant per entity. Saved in `docs/eksad/reserved-fields/RFC_<TENANT>_<ENTITY>.md`.

```markdown
# Reserved Field Config — {TENANT} / {ENTITY}

| Meta | Value |
|------|-------|
| **Tenant** | tenant-ahm |
| **Entity** | orders |
| **Author (BA)** | [name] |
| **Date** | YYYY-MM-DD |
| **Status** | Draft / In Review / Approved |

---

## 1. Discovery Summary
[2–4 sentences: tenant business context, why these custom fields are needed, what
gap they fill that the standard schema does not cover. Reference BR-* IDs from BRD.]

---

## 2. Slot Allocation

| Slot | Label | DataType | Sample Value | Rationale |
|------|-------|----------|--------------|-----------|
| `reserved_str_1` | Salesperson Code | string | `SP1234` | Cross-reference with HR salesperson registry |
| `reserved_num_1` | Discount %      | numeric | `5.0000`  | Promo discount applied at checkout |
| `reserved_date_1` | Promised Delivery | date  | `1745280000000` | SLA tracking for fulfillment |
| `reserved_bool_1` | VIP Customer    | boolean | `true`  | Trigger priority dispatch |

---

## 3. Validation Rules

| Slot | Rule Type | Rule | Error Message |
|------|-----------|------|---------------|
| `reserved_str_1` | simple (pattern) | `^SP[0-9]{4}$` | Salesperson code must be SP#### |
| `reserved_num_1` | simple (range)   | 0 ≤ x ≤ 30 | Discount must be 0–30% |
| `reserved_str_3` | conditional      | required if `reserved_str_2 == "PROMO"` | Promo code required when promo active |
| `reserved_str_1` | composition AND  | pattern + maxLength=8 + notIn=["SP0000"] | (aggregated) |

---

## 4. Stakeholder Sign-off

| Role | Name | Signed-off | Date |
|------|------|------------|------|
| Product Owner | | ☐ | |
| BA | | ☐ | |
| Tech Lead | | ☐ | |
| Tenant Admin | | ☐ | |
```

> 🔒 **Sign-off rule:** No `reserved_field_config` rows are inserted in production until all 4 stakeholders sign off. This is a guardrail — reserved slot assignments are permanent per tenant.

---

## 13. Flyway Migration Template

When opting an existing transactional table into reserved fields, copy-paste the block below as `V{N}__add_reserved_fields_to_{table}.sql`. The 13-column shape **must** match `BaseTransactionalEntity` exactly — column names, types, and order.

```sql
-- V{N}__add_reserved_fields_to_orders.sql
-- ─────────────────────────────────────────────────────────────────────────
-- Adds the 13 reserved fields from BaseTransactionalEntity to {table}.
-- Approach C Hybrid: 5 str + 3 num + 2 date + 2 bool + 1 jsonb.
-- DO NOT rename / reorder / re-type these columns — schema is contractual.
-- ─────────────────────────────────────────────────────────────────────────

ALTER TABLE orders
    ADD COLUMN reserved_str_1   VARCHAR(500),
    ADD COLUMN reserved_str_2   VARCHAR(500),
    ADD COLUMN reserved_str_3   VARCHAR(500),
    ADD COLUMN reserved_str_4   VARCHAR(500),
    ADD COLUMN reserved_str_5   VARCHAR(500),
    ADD COLUMN reserved_num_1   NUMERIC(20,4),
    ADD COLUMN reserved_num_2   NUMERIC(20,4),
    ADD COLUMN reserved_num_3   NUMERIC(20,4),
    ADD COLUMN reserved_date_1  BIGINT,
    ADD COLUMN reserved_date_2  BIGINT,
    ADD COLUMN reserved_bool_1  BOOLEAN,
    ADD COLUMN reserved_bool_2  BOOLEAN,
    ADD COLUMN reserved_ext     JSONB DEFAULT '{}'::jsonb;

-- ─── Per-tenant functional index (one known key) ─────────────────────────
-- Repeat per tenant that frequently queries a specific reserved slot.
CREATE INDEX idx_orders_ahm_salesperson
    ON orders (reserved_str_1)
    WHERE tenant_id = 'tenant-ahm';

-- ─── Per-tenant functional index on JSONB key ────────────────────────────
CREATE INDEX idx_orders_ahm_marketing
    ON orders ((reserved_ext->>'marketing_source'))
    WHERE tenant_id = 'tenant-ahm';

-- ─── Per-tenant GIN index (whole-document, multi-key queries) ────────────
-- Use only for power tenants needing arbitrary-key JSONB search.
CREATE INDEX idx_orders_ahm_reserved_ext_gin
    ON orders USING GIN (reserved_ext)
    WHERE tenant_id = 'tenant-ahm';
```

> ✅ **Naming convention:** `idx_<table>_<tenant-slug>_<purpose>` for partial indexes — keeps tenant scope visible at a glance.
> ⚠️ **Never** add reserved columns conditionally or with different names per tenant — that breaks `BaseTransactionalEntity` portability.

---

## 14. Testing

| Test | Scenario |
|------|----------|
| Unit | Config cascade: tenant override beats domain default |
| Unit | Validator: required field missing → ValidationException |
| Unit | Validator: regex mismatch → ValidationException |
| Unit | Validator: hidden field → skip validation even if invalid |
| Unit | Validator: AND composition aggregates all failed rule messages |
| Unit | Validator: conditional rule triggers required when predicate matches |
| Unit | Mapper: PATCH ignores null reserved-field properties |
| Integration | Schema endpoint returns correct labels per tenant |
| Integration | Create order with reserved fields → values persisted |
| Integration | Same entity, two tenants, different schemas → both work |

---

## 15. Anti-Patterns

| ❌ Don't | ✅ Do |
|----------|------|
| Force every entity to extend `BaseTransactionalEntity` | Only opt-in for transactional entities that need it |
| Use reserved fields on master data | Master data uses its own schema |
| Use reserved fields on cache tables | Cache tables are simple — no audit, no reserved |
| Hard-code labels in code | Always read from `reserved_field_config` |
| Skip validation because "it's a custom field" | Always invoke `ReservedFieldValidator` |
| Migrate data between slots | Reserved slot assignments are permanent per tenant |
| Throw on first validation fail | Aggregate all failed rules and return together |
| Hand-roll DTO ↔ Entity mapping | Use MapStruct — auto-passes all 13 reserved fields |
| Index `reserved_ext` globally | Use partial indexes scoped to one tenant |

---

## 16. FAQ

**Q1: How many reserved slots should we plan for?**
A: Approach C provides 12 typed slots + 1 JSONB overflow. Most tenants use 0–5 typed slots. If a tenant requests >10 in discovery, escalate — usually means a missing standard column the BA should add to the entity schema directly.

**Q2: Can two tenants share the same slot meaning?**
A: Technically yes (same `reserved_field_config` row at `scope_type=global`), but **prefer per-tenant scope**. Global configs lock the slot for ALL tenants — that's a one-way door. Use global only for fields that are truly cross-tenant (e.g., regulatory codes).

**Q3: What if we run out of slots?**
A: Use `reserved_ext` JSONB overflow first. If that still isn't enough (very rare), the slot itself is the wrong abstraction — promote those fields to **standard columns** on the entity via a normal Flyway migration. Never add `reserved_str_6` — `BaseTransactionalEntity` is contractual.

**Q4: Can master data EVER use reserved fields?**
A: **No.** Master data has its own schema controlled by `svc-master-data` and is cached across services. Mixing reserved slots into master breaks cache reproducibility + multi-tenancy boundaries (master is typically global or domain-scoped, not tenant-scoped). See §3 Opt-In Model.

**Q5: How do reserved fields interact with audit trail?**
A: Reserved field changes are audited the same way as standard columns — `createFlow()` / `updateFlow()` / `deleteFlow()` snapshot the full entity including all `reserved_*` columns. The audit event payload includes the slot name (`reserved_str_1`) — not the tenant label (`Salesperson Code`) — so audit data stays interpretable even if labels change later.

**Q6: Performance impact at high cardinality?**
A: Typed slots have zero overhead vs. standard columns. JSONB has ~5–10% storage overhead and slower writes if GIN-indexed. Recommendation: prefer typed slots; reach for `reserved_ext` + GIN only when the tenant truly needs arbitrary-key search at scale (>1M rows).

---

*End of file.*
