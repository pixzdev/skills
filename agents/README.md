# Agents — PIXZ Ecosystem

> Agents PERFORM; skills teach HOW; tools ENABLE; orchestrator COORDINATES.

## Definitions

| Agent | Role | When Spawned | Skills It Uses | Limits |
|-------|------|--------------|----------------|--------|
| `orchestrator` | Meta-coordinator (human or primary agent) | complex tasks, risk×uncertainty×impact high | `pixz.core.orchestrator` + its aggregates | `max_orchestration_depth=6`, `max_iterations=8` |
| `specialist` | Domain expert (security, design, motion, etc.) | delegated sub-task with bounded scope | one domain skill + core verification | inherits parent workflow, returns structured handoff |
| `challenger` | Adversarial reviewer | verification phase, high-risk | `pixz.core.epistemic-challenger` | intensity scaled, must exit |
| `verifier` | Inspector | pre-ship | `pixz.core.verification` | evidence-required |
| `researcher` | Source gatherer | external info needed | `pixz.core.capability-discovery` + `context-engineering` | official docs first |

## Orchestrator Agent Contract (`agents/orchestrator.yaml`)

- Owns `UNDERSTAND → SHIP` loop
- Determines WHEN/WHO/WHAT/WHY; never writes HOW (delegates to skills)
- Never treats subagent output as truth — inspects
- Tracks argument ledger, position change attribution
- Enforces depth/iteration caps and cycle detection

## Specialist Handoff Contract (`schemas/workflow.schema.json#handoff`)

```json
{
  "payload": { "objective": "...", "constraints": [], "phase": "EXECUTE", "context_packet": {} },
  "expected": { "artifact": "...", "findings": [], "assumptions": [], "evidence": [], "verification": {} }
}
```

Every child inherits: objective, requirements, constraints, phase, decisions, assumptions, evidence, open questions, verification requirements.

## Tool Policy

Agents select tools by task-fit, cost, freshness, reversibility, risk, permissions, availability. Prefer local read before web/model calls. Irreversible mutations require `change-safety` check.

## Example Spawn (conceptual)

```
orchestrator: PLAN step "API contract" → delegate to specialist(api-design)
  payload: {objective, constraints, context_packet, success_criteria}
specialist returns: {artifact: openapi.yaml, findings, evidence, verification}
orchestrator INSPECTs → CHALLENGEs → VERIFYs → REPLAN if needed
```
