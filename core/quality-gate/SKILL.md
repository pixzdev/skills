---
name: Quality Gate
description: Final ship gate — consolidates verification, risk, stop conditions and residual unknowns.
version: 1.0.0
id: pixz.core.quality-gate
category: core
triggers: [quality gate, ship check, done criteria, release gate]
compatible_runtimes: [claude, openclaw, opencode, hermes]
---

# Quality Gate — `pixz.core.quality-gate`

## Purpose
Decides SHIP vs REVISE vs REPLAN. Owns the final “definition of done.”

## Methodology
- Input: artifact + verification_report + challenger verdict + environment_report + assumptions ledger.
- Check all five: requirements satisfied / verification sufficient / critical risks addressed / remaining uncertainty acceptable / additional iteration has diminishing returns.
- Do not ship because code compiles or tests pass.
- Emit gate verdict with residual_risks and explicit unknown acceptance.

## Outputs
`gate_report` {verdict: ship|revise|replan, checks[], residual_risks[], unknowns_accepted[]}

---
