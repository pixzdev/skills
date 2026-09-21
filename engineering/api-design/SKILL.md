---
name: API Design
description: Methodology for consistent, versioned, secure and observable API contracts.
version: 1.0.1
id: pixz.engineering.api-design
category: engineering
triggers: [api design, rest, graphql, openapi, endpoint, versioning]
compatible_runtimes: [claude, openclaw, opencode, hermes]
---

# API Design — `pixz.engineering.api-design`

## Purpose
Contracts that survive versioning, auth, and observability.

## Methodology
1. **Contract:** OpenAPI/GraphQL SDL, idempotency, pagination, error envelope, versioning (URL or header — choose and justify).
2. **Security:** authN/Z, input validation, rate-limit, idempotency keys where needed.
3. **Observability:** request-id, structured errors, metrics, audit trail without PII.
4. **Verify:** contract review (no breaking change without major), mock + spec tests, backward-compat check.
---
