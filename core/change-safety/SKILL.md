---
name: Change Safety
description: Static pre-mutation policy — classifies every change (reversible / partially / irreversible), checks authority and scope; irreversible actions require confirmation in every mode.
version: 2.0.0
id: pixz.core.change-safety
category: core
triggers: [safe change, risk, reversible, scope control, tool selection]
compatible_runtimes: [claude, openclaw, opencode, hermes, codex, generic]
---

# Change Safety — `pixz.core.change-safety`

## Purpose
Every mutation classified as reversible / partially reversible / irreversible; stronger verification for higher risk.

> **Static policy, not routed capability:** this classification runs before mutations regardless of orchestrator routing or operating mode — the router cannot route itself out of safety.

## Methodology
1. **What will change?** files, data, external systems, third parties, secrets exposure, prod impact.
2. **Is it authorized?** scope + authority vs requested; confirm if irreversible.
3. **Is it reversible?** classify + mitigation (backup, branch, dry-run). Irreversible actions require confirmation **in every mode, including autonomous** (overlay-invariant — see `ZAI.md`).
4. **Scope control:** distinguish requested/necessary/optional/out-of-scope; no “fix one bug → rewrite architecture” without evidence.
5. **Gate:** reversible + scoped + authorized → proceed; else require confirmation or research. Pre-action verification runs for irreversible/high-impact steps (per `pixz.core.verification` triggers).

## Outputs
`safety_assessment` {changes[], risk, reversibility, authority_verdict, proceed: bool}

---
