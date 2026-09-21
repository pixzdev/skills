---
name: Planning
description: Decomposes objectives into verifiable, sequenced steps with dependencies and exit criteria.
version: 1.0.1
id: pixz.core.planning
category: core
triggers: [plan, roadmap, break down task, milestone, decompose]
compatible_runtimes: [claude, openclaw, opencode, hermes]
---

# Planning — `pixz.core.planning`

## Purpose
Turns vague objectives into verifiable, correctly-sequenced plans with dependencies and exit criteria. Separate from execution and from replanning.

## Methodology
1. **Decompose:** 3–7 steps, each with inputs, outputs, owner skill/agent, tools, verification, done criteria.
2. **Sequence:** dependency-ordered (requires/aggregates), parallelize where independent.
3. **Size:** each step independently verifiable; no “and then magic” steps.
4. **Gate:** define stop conditions: requirements satisfied + verification sufficient + residual risks acceptable + diminishing returns.
5. **Risk note:** flag irreversible/high-scope steps for `change-safety`.

## Outputs
`plan` {steps[], dependencies, stop_conditions, risk_flags}

---
