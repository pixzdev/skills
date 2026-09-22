---
name: API Design
description: Design consistent, versioned, secure, observable API contracts (REST/GraphQL/OpenAPI). Use when adding or changing endpoints. Do not use for unrelated UI work. For multi-step shipping, activate the MAIN skill pixz.core.orchestrator.
version: 1.2.0
id: pixz.engineering.api-design
category: engineering
triggers: [api design, rest, graphql, openapi, endpoint]
compatible_runtimes: [claude, openclaw, opencode, hermes, codex, generic]
---

# API Design — `pixz.engineering.api-design`

> **Specialist HOW skill.** For practical multi-step operating methodology (define → plan → research → delegate → inspect → challenge → verify → replan → ship), activate the **MAIN skill** `pixz.core.orchestrator`. Load `core/orchestrator/references/operating-methodology.md` when the work is complex.

## Purpose

Contracts that survive versioning, auth, pagination, and observability — not one-off route lists.

## When to Use / When NOT

| Use | Do not |
|-----|--------|
| New public or partner API, breaking change, auth/rate-limit surface | Pure UI/CSS, internal function rename with no wire contract |
| OpenAPI/GraphQL SDL, error envelope, idempotency, pagination | "Add a button that calls an existing endpoint" |

## Inputs

Existing routes, auth model, consumers, SLOs, error conventions, `openapi`/`schema` files if present.

## Methodology

### 1. Inventory before inventing

Read existing API conventions in-repo (error shape, auth header, pagination). Do not introduce a second envelope without evidence.

### 2. Contract

- Resources are nouns; verbs live in HTTP methods (or GraphQL fields with explicit side-effect naming).
- Choose and justify versioning: URL (`/v1`) or header (`Accept-Version`). Do not mix.
- Pagination: cursor for volatile lists; offset only when the set is stable and small. Always return `next_cursor` or `has_more`.
- Idempotency: `Idempotency-Key` on all non-safe writes that can double-charge or double-create.
- Filtering/sorting: allowlist fields; never pass raw column names from the client.

### 3. Error envelope (canonical unless the repo already has one)

```json
{
  "error": {
    "code": "rate_limited",
    "message": "Quota exceeded for this API key",
    "details": {"limit": 100, "reset_at": "2026-09-22T12:00:00Z"},
    "request_id": "req_01HZX…"
  }
}
```

Map: 400 validation · 401 unauthenticated · 403 unauthorized · 404 unknown · 409 conflict · 429 rate-limit · 5xx unexpected. Never leak stack traces or internals.

### 4. Security (pair with `pixz.security.review` when public)

AuthN/Z at the gateway and again at the object (no IDOR). Input validation at the boundary. Rate-limit per principal, not just per IP. HTTPS only. No secrets in URLs.

### 5. Observability

`request_id` on every response. Structured logs without PII. Metrics: latency histogram, error rate by code, saturation. Audit trail for authz denials.

### 6. Compatibility

Additive changes are minor. Renames, type changes, removed fields, stricter validation → major. Provide a deprecation window and a `Sunset`/`Deprecation` header when retiring.

### 7. Spec

Write OpenAPI 3.1 or GraphQL SDL *before* or *with* the implementation — the spec is the source of the mock and contract tests, not a post-hoc essay.

## Failure Conditions

- Two error shapes in one API → unify or document the exception with evidence.
- Breaking change without major version → blocked.
- Authz checked only at the collection, not the object → IDOR; fix before ship.

## Verification

- Contract review: no breaking change without major.
- Mock + spec tests (schemathesis / dredd / pact as available).
- Backward-compat check against previous spec diff.
- Rate-limit and auth negative tests.

## Example

> Add `POST /v1/keys` with per-key quota. Inventory shows existing `{error:{code,message}}`. Reuse it. Idempotency-Key required. 429 uses `Retry-After`. OpenAPI path + examples. Contract test hits 401/403/409/429.

## Structured Output

```yaml
api_contract:
  style: rest|graphql
  versioning: url|header
  resources: [...]
  errors: {envelope, codes}
  auth: {mode, object_level: true}
  pagination: cursor|offset
  idempotency: required_on
  observability: [request_id, metrics]
  compatibility: {breaking: false, migration: "..."}
verification: {spec_diff, contract_tests, residual_risks}
```

## Main Skill

Complex API work (public surface + auth + rollout) is an orchestration problem. Activate `pixz.core.orchestrator`.
