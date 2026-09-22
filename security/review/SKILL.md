---
name: Security Review
description: Checklist-driven security review covering auth, authz, input, secrets, deps and architecture — scoped to authorized environments.
version: 1.1.0
id: pixz.security.review
category: security
triggers: [security review, threat model, secure coding, audit]
compatible_runtimes: [claude, openclaw, opencode, hermes, codex, generic]
---

# Security Review — `pixz.security.review`

> Responsible, evidence-backed review for authorized environments only. Never tests production without explicit authority.

## Purpose
Systematic security inspection of code, architecture and configuration. Covers: authentication, authorization, input validation, output encoding, secrets management, dependency security, transport, storage, logging, rate-limiting.

## Triggers
- Pre-ship for auth, payments, PII, public API, infra change
- Explicit security review or audit request

## Methodology — OWASP-informed Checklist (scoped)

### 1. Authority & Scope Gate
- Confirm authorization to review (environment: authorized?). No out-of-scope testing.
- Record `requested scope` vs `necessary scope`; do not expand to “rewrite architecture” without evidence.

### 2. Enumerate Surfaces
- Entrypoints: routes, APIs, webhooks, file parsers, LLM inputs, deserialization.
- Trust boundaries: client ↔ server, service ↔ db, MCP ↔ agent.

### 3. Check per Surface
- **Auth:** session/token lifecycle, revocation, rotation, MFA where needed, side-channel, replay.
- **AuthZ:** IDOR, privilege escalation, object-level vs function-level.
- **Input:** injection (SQL/NoSQL/template), SSRF, path traversal, file limits; validate at boundary.
- **Secrets:** no hardcoded/inline secrets, no logs exposure, vault/env discipline, rotation.
- **Deps:** known CVEs (`npm audit`, `pnpm audit`), supply chain pinning.
- **Transport/Storage:** TLS, HSTS, cookie flags, at-rest encryption where required.
- **Observability:** no PII in logs, rate-limit present, error messages not leaking internals.

### 4. Verify, Not Assert
- Reproduce or cite primary source (e.g., “auth bypass via header X confirmed locally”).
- Unknowns remain `UNKNOWN`; confidence capped.

### 5. Report with Risk
Each finding: `{surface, weakness, impact (low/med/high/critical), likelihood, evidence, remediation, verification_step, responsible}`

## Inputs / Outputs
- Inputs: artifact, dependency manifest, env report, threat model (if present)
- Outputs: `security_report` {scope, surfaces[], findings[], verification[], residual_risks[], confidence}

## Failure Conditions
- Testing without authorization → abort.
- Tool indicates irreversible prod impact → require explicit confirmation.

## Verification
- Re-run after remediation; targeted tests for each finding.
- Cross-check by challenger: “What would falsify this is-safe claim?”

---
