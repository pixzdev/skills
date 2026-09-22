---
name: Security Review
description: Checklist-driven security review covering auth, authz, input, secrets, deps and architecture — scoped to authorized environments. Use before shipping auth, payments, PII, or public APIs. Never test production without authority.
version: 1.2.0
id: pixz.security.review
category: security
triggers: [security review, threat model, secure coding, audit]
compatible_runtimes: [claude, openclaw, opencode, hermes, codex, generic]
---

# Security Review — `pixz.security.review`

> **Specialist HOW skill.** For practical multi-step operating methodology, activate the **MAIN skill** `pixz.core.orchestrator`. Load `core/orchestrator/references/operating-methodology.md` for high-risk work (second pass, pentester role, ship criteria).
>
> Responsible, evidence-backed review for authorized environments only. Never tests production without explicit authority.

## Purpose

Systematic security inspection of code, architecture and configuration. Covers: authentication, authorization, input validation, output encoding, secrets management, dependency security, transport, storage, logging, rate-limiting.

## Triggers

- Pre-ship for auth, payments, PII, public API, infra change
- Explicit security review or audit request

**Do NOT use when:** a typo fix with no trust-boundary change; unauthorized environments; "just pentest prod".

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

### 4. Practical probes (authorized only)

Prefer reading code and running *local* tests over speculative claims:

- Replay a captured token; expect reject after logout/rotation.
- Access object `{id}` belonging to another user; expect 403/404, never 200.
- Submit `' OR 1=1` / `${7*7}` / `http://169.254.169.254/` at each parser; expect rejection.
- `git grep -E 'api[_-]?key|secret|BEGIN PRIVATE' -- ':!*.md'` and inspect hits.

Do not run destructive or out-of-scope payloads. Do not write exploit PoCs.

### 5. Verify, Not Assert

- Reproduce or cite primary source (e.g., “auth bypass via header X confirmed locally”).
- Unknowns remain `UNKNOWN`; confidence capped.

### 6. Report with Risk

Each finding: `{surface, weakness, impact (low/med/high/critical), likelihood, evidence, remediation, verification_step, responsible}`

## Inputs / Outputs

- Inputs: artifact, dependency manifest, env report, threat model (if present)
- Outputs: `security_report` {scope, surfaces[], findings[], verification[], residual_risks[], confidence}

## Failure Conditions

- Testing without authorization → abort.
- Tool indicates irreversible prod impact → require explicit confirmation.
- "Looks fine" with no surfaces enumerated → invalid review; redo.

## Verification

- Re-run after remediation; targeted tests for each finding.
- Cross-check by challenger: “What would falsify this is-safe claim?”
- Pair with `pixz.security.threat-modeling` when the system is new or the trust boundary moved.

## Example

> Auth service review, staging only. Surfaces: `/login`, `/refresh`, `/users/:id`. Finding: refresh tokens not rotated (replay window). Impact high. Evidence: local replay succeeded. Remediation: token family + reuse detection. Re-test: replay within 60s must 401.

## Main Skill

A security review that must sequence threat model → fix → re-verify → ship is orchestrator work. Activate `pixz.core.orchestrator`.
