---
name: Delegation & Handoff
description: Structured delegation with explicit inputs, constraints, success criteria and structured returns.
version: 1.0.1
id: pixz.core.delegation-handoff
category: core
triggers: [delegate, handoff, subagent, dispatch task]
compatible_runtimes: [claude, openclaw, opencode, hermes]
---

# Delegation & Handoff — `pixz.core.delegation-handoff`

## Purpose
Bounded dispatch that preserves workflow continuity and accountability.

## Methodology
1. **Package:** objective, requirements, constraints, phase, decisions, assumptions, evidence, open questions, verification requirements, expected output schema.
2. **Bound:** scope + authority + reversibility note; set `max_iterations` for child.
3. **Dispatch:** child inherits semantics; not an isolated chatbot.
4. **Receive:** enforce structured handoff (artifact, findings, evidence, verification, residual risks). Inspect — do not trust blindly.
5. **Ledger:** log delegation + handoff + inspection result.

## Outputs
`handoff_envelope` {payload, return, inspection}

---
