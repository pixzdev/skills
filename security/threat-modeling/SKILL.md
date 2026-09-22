---
name: Threat Modeling
description: STRIDE-based threat enumeration, impact scoring and mitigation mapping. Use before new trust boundaries, auth, or public surfaces. Do not use for a local-only helper with no data flow. Pair with MAIN skill pixz.core.orchestrator on high-risk systems.
version: 1.2.0
id: pixz.security.threat-modeling
category: security
triggers: [threat model, STRIDE, attack surface, abuse case]
compatible_runtimes: [claude, openclaw, opencode, hermes, codex, generic]
---

# Threat Modeling — `pixz.security.threat-modeling`

> **Specialist HOW skill.** For practical multi-step operating methodology, activate the **MAIN skill** `pixz.core.orchestrator`. Load `core/orchestrator/references/operating-methodology.md` when impact is high.

## Purpose

Enumerate how the system can be abused *before* implementation freezes the design. Complements `pixz.security.review` (review inspects what exists; this models what could go wrong).

## When to Use / When NOT

| Use | Do not |
|-----|--------|
| New service, new trust boundary, payments/PII/auth, public API | Purely local pure-function with no I/O |
| Architecture decision that changes data flow | After-the-fact checkbox with no DFD |

## Methodology

### 1. DFD (data flow)

Draw: actors · processes · data stores · data flows · **trust boundaries**. If you cannot name the boundary, you cannot name the threat.

### 2. Enumerate STRIDE per element

| Letter | Question | Typical control |
|--------|----------|-----------------|
| Spoofing | Can someone pretend to be this actor? | Authn, mTLS, signed webhooks |
| Tampering | Can data/code be modified in transit or at rest? | Integrity, signatures, least-write |
| Repudiation | Can an actor deny an action? | Audit logs, non-repudiable events |
| Info disclosure | What leaks if this store/flow is read? | Encryption, minimization, field filters |
| DoS | How do we exhaust this? | Timeouts, quotas, backpressure |
| Elevation | Can this principal gain another role? | Authz, object-level checks |

LLM/tool surfaces add: prompt injection, tool-abuse, data exfil through tools. Treat model I/O as an untrusted boundary.

### 3. Score and prioritize

`priority ≈ impact × likelihood`, with basis (not decorative numbers). Critical/high must have a mitigation or an explicit accepted residual with owner.

### 4. Mitigate

One control per threat. Prefer prevention over detection. Record residual risk honestly.

### 5. Misuse cases (verification)

For each high threat write a misuse case the QA/review can run: "as attacker, I replay webhook X without signature → expect 401".

## Failure Conditions

- STRIDE table with no DFD → fiction; start over.
- Every threat "medium" → uncalibrated; redo scoring with basis.
- Mitigations that are slogans ("be careful") → not a control.

## Verification

- Misuse-case tests exist for high/critical threats.
- Review (`pixz.security.review`) covers the same surfaces.
- Model is updated when a trust boundary moves.

## Example

> Partner webhook. Boundary: internet → API. Spoofing: unsigned body. Mitigation: HMAC + timestamp window. Misuse: replay 10m-old signed body → 401. Residual: partner clock skew ±30s accepted, owner=platform.

## Structured Output

```yaml
threat_model:
  dfd: {actors, processes, stores, flows, boundaries}
  threats: [{id, stride, element, impact, likelihood, basis, mitigation, residual}]
  misuse_cases: [{threat_id, steps, expected}]
  residual_risks: [...]
```

## Main Skill

Threat model → controls → tests → review → ship is orchestrator work. Activate `pixz.core.orchestrator`.
