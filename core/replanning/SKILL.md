---
name: Replanning
description: Structured replanning and escalation when verification fails or constraints change.
version: 1.0.1
id: pixz.core.replanning
category: core
triggers: [replan, pivot, strategy failed, alternative approach, escalation]
compatible_runtimes: [claude, openclaw, opencode, hermes]
---

# Replanning — `pixz.core.replanning`

## Purpose
Prevents endless retry of same failed strategy; provides escalation ladder.

## Methodology
Escalation ladder: retry → inspect → alternate approach → research → specialist → challenge → parent orchestrator → user (ask with precise missing context only).

Steps:
1. Diagnose: failed verification cause, assumption broken, constraint changed?
2. Alternate: enumerate alternatives with tradeoffs (via epistemic-reasoning).
3. Re-plan minimal delta; preserve ledger history.
4. Bound iterations; if diminishing returns, note residual and defer.

---
