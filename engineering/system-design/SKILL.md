---
name: System Design
description: Make architecture tradeoffs explicit and verifiable — constraints, failure domains, ADRs, SLIs. Use for cross-service or scale decisions. Do not use for a single-function refactor. For multi-step shipping, use MAIN skill pixz.core.orchestrator.
version: 1.2.0
id: pixz.engineering.system-design
category: engineering
triggers: [system design, architecture, scalability, tradeoffs]
compatible_runtimes: [claude, openclaw, opencode, hermes, codex, generic]
---

# System Design — `pixz.engineering.system-design`

> **Specialist HOW skill.** For practical multi-step operating methodology, activate the **MAIN skill** `pixz.core.orchestrator`. Load `core/orchestrator/references/operating-methodology.md` when the design is high-impact.

## Purpose

Makes tradeoffs explicit and verifiable. Architecture is a set of decisions with alternatives, not a diagram dump.

## When to Use / When NOT

| Use | Do not |
|-----|--------|
| New service, data store choice, sync vs async, multi-region, failure-domain work | Local refactor, adding a field, renaming a module |
| Cross-cutting latency/consistency/cost conflict | "Make this function faster" without a system constraint |

## Inputs

Load, latency, consistency, cost, team/ops constraints, existing topology, SLOs if any.

## Methodology

### 1. Constraints first (numbers)

Estimate: QPS, p50/p95/p99, data size, fan-out, write/read ratio, consistency need (read-your-writes? cross-region?). If numbers are unknown, mark them `UNKNOWN` and design for a bounded range — do not invent precision.

### 2. Options (2–3, not 7)

For each option record: happy path, failure domains (what dies together), scalability limit (the first wall), operational burden (pages, runbooks, skill needed), cost envelope.

Typical forks: monolith vs services · sync vs async · single-primary vs multi-leader · cache vs materialized view · queue vs stream.

### 3. Falsify

What breaks each option? Activate `pixz.core.epistemic-challenger` for high-impact choices. Write one falsification test per option ("this design fails if p95 > X under Y").

### 4. Decide with an ADR

```
Title / Status / Context / Decision / Alternatives considered
Consequences (positive, negative, residual risks) / Confidence + basis
Review date
```

Confidence without basis is invalid.

### 5. Operability

Define SLIs/SLOs, dashboards, and the first alert that would fire. A design with no SLO is unfinished if the system is user-facing or paid.

### 6. Evolution

What is easy to change later vs frozen (data model, public contract, consistency model)? Prefer freezing less.

## Failure Conditions

- One option presented as inevitable → redo; missing alternatives.
- Diagram without failure domains → incomplete.
- "We'll just scale it" with no first-wall number → hypothesis, not a design.

## Verification

- Prototype or back-of-envelope when uncertainty is high (queue drain time, cache hit math, quorum write latency).
- Challenger pass on irreversible choices (data store, tenancy model).
- ADR stored in-repo; decision marked in task-state (never deleted).

## Example

> "Should notifications be sync HTTP or a queue?" Constraints: 5k signups/hour, email provider p95 900ms, signup p95 budget 300ms. Options: (A) sync — simple, blows p95; (B) queue + worker — extra moving part, meets budget; (C) outbox on the signup txn — exactly-once-ish, more code. Falsify B: poison messages. Decide B + outbox later if duplicates hurt. SLO: 99% of emails in 60s.

## Structured Output

```yaml
design_decision:
  constraints: {qps, latency, consistency, cost}
  options: [{name, failure_domains, first_wall, ops, cost}]
  tradeoffs: [...]
  decision: {choice, rationale, confidence, basis}
  adr_path: docs/adr/...
  slis_slos: [...]
  verification_plan: [...]
  residual_risks: [...]
```

## Main Skill

Architecture plus implementation plus rollout is orchestrator work. Activate `pixz.core.orchestrator`.
