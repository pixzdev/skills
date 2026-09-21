---
name: System Design
description: Structures system tradeoffs, constraints, failure domains and verification for architecture decisions.
version: 1.0.1
id: pixz.engineering.system-design
category: engineering
triggers: [system design, architecture, scalability, tradeoffs, failure modes]
compatible_runtimes: [claude, openclaw, opencode, hermes]
---

# System Design — `pixz.engineering.system-design`

## Purpose
Makes tradeoffs explicit and verifiable.

## Methodology
1. **Constraints:** latency, throughput, consistency, cost, operational complexity.
2. **Options:** 2–3 architectures with failure domains, scalability limits, operational burden.
3. **Falsify:** what breaks each? Use challenger for high-impact.
4. **Decide:** ADR with rationale, alternatives, confidence basis, residual risks.
5. **Verify:** prototype or model if uncertainty high; define SLIs/SLOs.

## Outputs
`design_decision` {options[], tradeoffs, decision, ADR, verification_plan, residual_risks}
---
