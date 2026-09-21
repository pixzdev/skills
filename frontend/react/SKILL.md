---
name: React Engineering
description: React/Next.js methodology — composition, state, boundaries, performance and verification.
version: 1.0.0
id: pixz.frontend.react
category: frontend
triggers: [react, next.js, component, hooks, composition]
compatible_runtimes: [claude, openclaw, opencode, hermes]
---

# React Engineering — `pixz.frontend.react`

## Methodology
1. **Composition:** server vs client boundaries (Next.js), props vs context vs state-machine.
2. **State:** colocation, minimal; no prop drilling heroics — lift only when evidence needs it.
3. **Performance:** memo only with measured gain; RSC streaming, suspensible data boundary; `transform/opacity` motion only.
4. **Verify:** type-check, unit + integration, a11y per `accessibility`, anti-slop (no abstraction astronautics).

---
