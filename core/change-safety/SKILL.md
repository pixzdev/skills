---
name: Change Safety
description: Evaluates risk, reversibility, scope and authority before mutating state or invoking tools.
version: 1.0.0
id: pixz.core.change-safety
category: core
triggers: [safe change, risk, reversible, scope control, authority]
compatible_runtimes: [claude, openclaw, opencode, hermes]
---

# Change Safety — `pixz.core.change-safety`

## Purpose
Every mutation classified as reversible / partially reversible / irreversible; stronger verification for higher risk.

## Methodology
1. **What will change?** files, data, external systems, third parties, secrets exposure, prod impact.
2. **Is it authorized?** scope + authority vs requested; confirm if irreversible.
3. **Is it reversible?** classify + mitigation (backup, branch, dry-run).
4. **Scope control:** distinguish requested/necessary/optional/out-of-scope; no “fix one bug → rewrite architecture” without evidence.
5. **Gate:** reversible + scoped + authorized → proceed; else require confirmation or research.

## Outputs
`safety_assessment` {changes[], risk, reversibility, authority_verdict, proceed: bool}

---
