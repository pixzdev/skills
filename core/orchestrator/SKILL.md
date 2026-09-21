---
name: Orchestrator
description: Meta-coordination layer that routes work to the right skills, agents and tools with accountability and verification.
version: 1.0.1
id: pixz.core.orchestrator
category: core
triggers: [orchestrate, coordinate, delegate, complex task, multi-step, route work]
compatible_runtimes: [claude, openclaw, opencode, hermes]
---

# Orchestrator — `pixz.core.orchestrator`

> Meta-coordination that answers WHEN/WHO/WHAT/WHY; skills answer HOW; agents EXECUTE; tools PROVIDE CAPABILITY. Never collapses those layers.

## Purpose
Orchestrator owns coordination and accountability across the full loop: `UNDERSTAND → DISCOVER → PLAN → ROUTE → DELEGATE → COORDINATE → INSPECT → CHALLENGE → VERIFY → REPLAN → RE-EXECUTE → IMPROVE → SHIP`. It does not contain every methodology itself — it delegates. It never treats subagent output as truth without verification.

## Triggers
- Task mentions: orchestrate, coordinate, delegate, multi-step, route work, full workflow, complex task
- Task complexity signals: scope > 1 file, risk×uncertainty×impact high, multiple dependencies, irreversible actions, external research needed
- Explicit install: `python scripts/resolve.py --install pixz.core.orchestrator`

Do NOT use when: single reversible trivial edit (rename variable) where orchestration overhead exceeds value. Use complexity-aware routing instead.

## When to Use / When NOT
| Use orchestrator | Do not |
|-----------------|--------|
| Production feature, cross-cutting change, architecture decision, security fix | Rename token, typo fix |
| Need multiple skills/agents/tools sequenced | One deterministic local edit |
| Verification + challenge required before ship | Task where tests + inspection already sufficient |

## Inputs
- `objective` — verifiable goal + acceptance criteria
- `constraints` — scope, authority, deadlines, budget, non-goals
- `current_state` — workflow state per `schemas/workflow.schema.json` (phase, decisions, assumptions, evidence, unknowns)
- `requirements` — explicit verification requirements

## Required Context
Inherit parent workflow semantics; child agents are not isolated chatbots. Before routing, confirm:
1. Existing workflow state (if continuation)
2. Repository/local context (via context-engineering)
3. Environment signals (via environment-awareness)
4. Capability inventory (via capability-discovery)
Ask user only for information that cannot be discovered locally.

## Methodology

### 1. UNDERSTAND & DEFINE
- Restate objective in own words; extract requested vs necessary vs optional vs out-of-scope.
- List unknowns and assumptions (fragility: low/medium/high).
- Declare stop conditions: requirements satisfied + verification sufficient + critical risks addressed + diminishing returns.

### 2. DISCOVER
- Call `pixz.core.capability-discovery` and `pixz.core.environment-awareness` before planning.
- Map required skills by trigger overlap; resolve dependencies via `scripts/resolve.py`.
- Classify complexity: `minimal` (understand→execute→verify) vs `full` (full loop with challenger + quality-gate).

### 3. PLAN & ROUTE
- Decompose into 3–7 steps with owner (skill/agent), inputs/outputs, tools, verification per step.
- Define routing: skill determines HOW, agent performs, tool enables. Orchestrator determines WHEN/WHO/WHAT/WHY.
- Publish plan with dependencies and aggregated skills. Installing orchestrator MUST resolve: planning, context-engineering, environment-awareness, capability-discovery, workflow-continuity, epistemic-reasoning, verification, quality-gate (and their transitive `requires`).

### 4. DELEGATE & COORDINATE
- Dispatch via `pixz.core.delegation-handoff`: pass objective, constraints, phase, decisions, assumptions, evidence, open questions, verification requirements, and expected structured handoff schema.
- Track in-flight work; enforce `max_orchestration_depth=6`, `max_iterations=8`.
- Preserve context for downstream agents (context protocol).

### 5. INSPECT & CHALLENGE
- Inspect each handoff: does artifact satisfy contract? Evidence backs claim? Scope controlled?
- Decide challenge intensity ≈ risk × uncertainty × impact (trivial → none; production security → substantial via `pixz.core.epistemic-challenger`).
- Challenger must have exit condition — improved reasoning, not argument volume.

### 6. VERIFY → REPLAN → IMPROVE → SHIP
- Verification is evidence, not proof. Require inspection, regression, consistency, change-impact.
- On failure: follow escalation ladder retry → inspect → alternate → research → specialist → challenge → parent → user (see `core/replanning`).
- Iterate until stop conditions met. Do NOT ship because code compiles or tests pass.

## Dependencies
- **aggregates (mandatory when installed):** pixz.core.planning, pixz.core.context-engineering, pixz.core.environment-awareness, pixz.core.capability-discovery, pixz.core.workflow-continuity, pixz.core.epistemic-reasoning, pixz.core.verification, pixz.core.quality-gate
- **optional:** pixz.core.epistemic-challenger, pixz.quality.anti-ai-slop
- **requires:** none (top-level composition). Resolver recursively expands aggregates' `requires`.
- **conflicts:** none (orchestrator must not conflict with its aggregates)

## Tools
Select by task-fit, cost, latency, reliability, freshness, risk, permissions, reversibility, availability. Prefer local inspection over expensive agents; expensive research gated behind DISCOVER.

## Constraints & Failure Conditions
- Fails if hard dependency missing, runtime incompatible, cycle detected, or limits exceeded.
- Fails if subagent handoff lacks required fields (findings, evidence, verification) — return to subagent.
- Fails if position flips without attributable cause (new evidence, reasoning, constraint change, failed verification, new requirement).
- Unbounded recursion forbidden: orchestrator → skill → orchestrator must be bounded by depth caps.

## Verification
- Pre-ship: registry validation (`scripts/validate.py`), cycle check, resolver dry-run.
- Per-delegation: contract + output + evidence inspection.
- Post-ship: residual risks + unknowns documented, iteration history preserved.

## Structured Output
```yaml
objective: "..."
plan: [{step, owner_skill, inputs, outputs, verification}]
delegations: [{to, payload, received_handoff, inspection_result}]
findings: [ ... ]
arguments:
  - {claim, position, rationale, evidence, counterarguments, confidence, basis, status}
assumptions: [{claim, basis, fragility, validated}]
unknowns: [ ... ]
verification: {checks: [...], results: "...", residual_risks: [...]}
stop_conditions: {requirements_satisfied: bool, verification_sufficient: bool, diminishing_returns: bool}
recommended_next_actions: [ ... ]
```

## Example
> Task: “Design and ship rate-limited public API for Next.js service”
> Orchestrator detects: needs `environment-awareness` (confirm Next.js/pnpm), `capability-discovery` (existing auth, infra), `planning` (decompose: contract→impl→security review→tests→verification), `api-design` + `security.review`, challenger for auth design, `quality-gate` before ship. Resolves graph via `scripts/resolve.py`; delegates with structured handoffs; inspects each; challenges auth assumptions; verifies integration; ships with ledger.

## Anti-Patterns
- Orchestrator containing every skill's methodology (bloat).
- Blind trust in subagent output.
- Recursive orchestration without depth guard.
- Orchestration overhead > task value.

## Runtime Notes
- Claude: `.claude/skills/orchestrator/SKILL.md` + `CLAUDE.md` includes `@AGENTS.md`
- OpenClaw: `~/.openclaw/skills/orchestrator/SKILL.md`; respects `agents.entries.*.skills` final allowlist
- OpenCode/Hermes: generic `skills/` import via adapter

---
*See `docs/architecture.md` + `docs/dependency-model.md`. Methodology stays runtime-agnostic.*
