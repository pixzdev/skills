---
name: Workflow Continuity
description: Maintains, persists and propagates workflow state across parent and child agents.
version: 1.0.0
id: pixz.core.workflow-continuity
category: core
triggers: [workflow, continue, handoff, persist state, workflow state, iteration state]
compatible_runtimes: [claude, openclaw, opencode, hermes]
---

# Workflow Continuity — `pixz.core.workflow-continuity`

> Every subagent inherits the relevant parent workflow; none behaves as an isolated chatbot.

## Purpose
Defines the logical workflow model and handoff contract. Persistence mechanism varies per runtime (filesystem, memory, adapter) — the logical model does not.

## Triggers
- Continuation across DEFINE→RESEARCH→PLAN→EXECUTE→VERIFY branches
- Delegation / subagent dispatch; multi-iteration replanning

## Methodology

### 1. Model (schemas/workflow.schema.json)
Persist at minimum:
```
objective, requirements, constraints, phase, completed_work, pending_work,
decisions[], assumptions[], arguments[], evidence[], unknowns[], verification, iteration_history, residual_risks
```

### 2. Propagation Rule
Child inherits: objective, requirements, constraints, current phase, decisions, assumptions, evidence, open questions, verification requirements. It MUST continue within compatible workflow semantics under parent’s DEFINITION.

### 3. Persistence Abstraction
- **Define logical state per schema** — universal core.
- **Adapter implements storage:** `.pixz/workflow.json` on filesystem, or in-memory for constrained runners, or via MCP state server. Inspect `adapters/` for translation.
- Never require every runtime to share same persistence; require same logical fields.

### 4. Handoff Contract
Dispatch includes: `{objective, requirements, constraints, phase, context_packet, expected_outputs, success_criteria}`.
Return includes: `{artifact, findings, assumptions, unknowns, evidence, decisions, arguments, verification, residual_risks, recommended_next}` (subset of schema; must preserve ledger).

### 5. Iteration & Observability
Increment `iteration`; cap at `max_iterations=8`. Any observer can answer: current phase, completed vs pending, open decisions, unknowns, verification, residual risks.

## Inputs / Outputs
- **Inputs:** parent workflow state, child task spec
- **Outputs:** `continuity_envelope` {propagated_state, handoff_payload, persistence_receipt}

## Failure Conditions
- Child loses parent constraints or decision history → fail handoff.
- Workflow state diverges without ledger entry → fail verification.

## Verification
- Handoff round-trip: can parent reconstruct full state from child’s return?
- Re-entry test: after crash, can workflow resume from persisted state?

---
