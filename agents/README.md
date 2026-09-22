# Agents — PixzFlow Ecosystem

> Agents PERFORM; skills teach HOW; tools ENABLE; the orchestrator DECIDES (when/which/how-deeply/under-what-verification/for-how-long).

## Roles (created only when the economics test passes)

| Role | When Spawned | Uses | Limits |
|------|--------------|------|--------|
| `orchestrator` | complex tasks, high risk×uncertainty×impact, long horizon | `pixz.core.orchestrator` + activated capabilities | `max_orchestration_depth=6`, `max_iterations=8` |
| `specialist` | delegated sub-task with bounded scope + passed economics test | one domain skill + verification floor | inherits parent state, returns structured handoff |
| `challenger` | high-stakes verification (intensity > 0) | `pixz.core.epistemic-challenger` | intensity-scaled, **explicit stop rule** |
| `verifier` | pre-completion / pre-handoff inspection | `pixz.core.verification` | evidence-required |
| `researcher` | external info needed, local context insufficient | `pixz.core.capability-discovery` + `context-engineering` | official docs first |

Do **not** spawn roles by default. A role must pass: `expected information gain + parallelism + specialization > coordination cost`. Anti-delegation (correctly *not* delegating trivial work) is a first-class behavioral eval. Subagents never spawn subagents.

## Orchestrator Agent Contract (`agents/orchestrator.yaml`)

- Runs `ORIENT → MODEL → ASSESS → MODE → PLAN → ACT → OBSERVE → VERIFY → DECIDE`
- Determines WHEN/WHO/WHAT/WHY/HOW-DEEPLY; never writes HOW (delegates to skills)
- Activates capabilities per the persistent protocol; records every activation + rejection with reason
- Never treats subagent output as truth — inspects structured returns
- Tracks typed findings, position-change attribution, capability state, failures
- Enforces depth/iteration caps, cycle detection, and the orchestration budget

## Specialist Handoff Contract (`schemas/handoff.schema.json`)

```json
{
  "objective": "...",
  "constraints": ["...", "reversibility note", "iteration cap"],
  "context_packet": { "decisions": [], "assumptions": [], "evidence_refs": [], "verification_requirements": [] },
  "success_criteria": ["observable ..."]
}
```

Return **must** contain: `work_performed, findings, evidence, assumptions, unknowns, decisions, tests, verification{result,checks,residual_risks}, remaining_work, recommended_next_action`. Missing field → rejected. Parent inspection verdict: `accepted | returned_to_agent | escalated`. No vague “looks good.”
