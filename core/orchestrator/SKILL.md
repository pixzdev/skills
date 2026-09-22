---
name: Orchestrator
description: PixzFlow's adaptive agent operating system — assesses task, selects operating mode, activates capabilities on demand, delegates when beneficial, and decides done/continue/replan/escalate with an explicit orchestration budget.
version: 2.0.0
id: pixz.core.orchestrator
category: core
triggers: [orchestrate, coordinate, delegate, complex task, multi-step]
compatible_runtimes: [claude, openclaw, opencode, hermes, codex, generic]
---

# Orchestrator — `pixz.core.orchestrator`

> PixzFlow's **adaptive agent operating system**. It is not a workflow narrator with a fixed phase list. It answers **WHEN / WHY / WHICH / HOW DEEPLY / UNDER WHAT VERIFICATION / FOR HOW LONG** — capabilities answer HOW.

## Purpose
Owns task assessment, operating-mode selection, capability activation, delegation, state continuity, and the done/continue/replan/delegate/research/challenge/escalate decision loop. It does not contain every methodology — it activates capabilities. It never treats subagent output as truth.

## Triggers
- Task complexity signals: scope > 1 file, risk×uncertainty×impact high, multiple dependencies, irreversible actions, external research needed, long horizon, continuation of prior work.
- Explicit request: orchestrate / coordinate / full workflow.

**Do NOT use when:** single reversible trivial edit (rename, typo) where orchestration overhead exceeds value. Run `ORIENT → ACT → VERIFY → done` directly. Orchestration overhead > task value is a failure, not rigor.

## When to Use / When NOT
| Use orchestrator | Do not |
|-----------------|--------|
| Production feature, cross-cutting change, architecture decision, security fix, long-horizon or resumed task | Rename token, typo fix |
| Multiple capabilities/agents/tools must be sequenced or coordinated | One deterministic local edit |
| Verification + challenge required before completion | Task where a targeted test already closes it |

## Inputs
- `objective` — verifiable goal + acceptance criteria
- `constraints` — scope, authority, deadlines, budget, non-goals
- `task_state` — per `schemas/task-state.schema.json` (continuation: read it first)

## Required Context (before planning)
1. Existing task state (if continuation)
2. Repository/local context (`pixz.core.context-engineering`)
3. Environment signals (`pixz.core.environment-awareness`)
4. Capability inventory (`pixz.core.capability-discovery`)
Ask the user only for information that cannot be discovered locally.

## Methodology

### 1. ORIENT & MODEL
Restate objective, acceptance criteria, constraints, unknowns. Split requested / necessary / optional / out-of-scope. Declare stop conditions up front.

### 2. ASSESS
Bands (low/medium/high/critical): complexity · risk · uncertainty · reversibility · horizon. Write the assessment + rationale into task-state. Reassess when material new information arrives — a silent band change is a bug.

### 3. SELECT MODE
`fast | balanced | deep | autonomous` — user instruction > runtime overlay (e.g. `ZAI.md` mode selection) > balanced default. Mode sets an **upper tendency** of depth, never a minimum ceremony: even in deep mode, a trivial subtask runs fast.

### 4. BUILD MINIMAL PLAN
Steps sized to mode: fast 0–2 · balanced 3–7 · deep full plan with explicit assumptions + evidence plan. Each step: owner (self/skill/agent), inputs, outputs, **verification that closes it**. No "and then magic" steps.

### 5. ACTIVATE CAPABILITIES (persistent protocol)
`DISCOVER → MATCH → LOAD (progressive) → ACTIVATE → USE → VERIFY → PERSIST state → REINVOKE`. Every activation records id, status, reason, state_digest in task-state `capabilities[]`. Do not preload skill bodies; do not activate skills that do not earn their context cost; keep earlier activations alive across transitions (a security review stays `active` with reactivation conditions, it does not vanish when you move to implementation).

### 6. ACT → OBSERVE → VERIFY (continuous)
Smallest action that advances the plan. Classify mutations before executing (change-safety tiers: reversible / partially / irreversible — irreversible requires confirmation). Observe **actual outputs and artifacts**, not reports. Verify on triggers: before irreversible action, after significant mutation, before consequential claims, before handoff, before completion.

### 7. DECIDE
After each observe/verify: **done | continue | replan | delegate | research | challenge | escalate | stop**.
- **delegate** only when `expected information gain + parallelism + specialization > coordination cost`; dispatch per `schemas/handoff.schema.json`; inspect the return; never trust blindly; subagents do not spawn subagents.
- **challenge** at `intensity ≈ risk × uncertainty × impact × irreversibility`, with an explicit stop rule (upheld / revised / falsified).
- **replan** on contradictory evidence or failed verification: discard the plan (not the objective), record the failure + lesson, bump `plan.iteration` (cap `limits.max_iterations`).
- **stop** when acceptance criteria met + verification sufficient + critical risks addressed + diminishing returns.

### 8. PERSIST & HAND OFF
Update task-state at checkpoints (before long substeps, before irreversible actions, at phase boundaries). On completion: residual risks + unknowns documented, decisions preserved (marked, never deleted), state file left for continuation.

## Orchestration Budget
Every added capability, subagent, research pass, or verification round must have **expected value > context/coordination cost**. When in doubt, do the cheaper thing and record the deferral. Trivial tasks must stay cheap — this is a first-class requirement, not a hint.

## Dependencies
- **aggregates (mandatory when installed):** `pixz.core.verification` — the evidence floor. Even a mis-routed task keeps verification.
- **optional (activated on demand via the capability protocol):** `pixz.core.planning`, `pixz.core.context-engineering`, `pixz.core.environment-awareness`, `pixz.core.capability-discovery`, `pixz.core.workflow-continuity`, `pixz.core.delegation-handoff`, `pixz.core.epistemic-reasoning`, `pixz.core.epistemic-challenger`, `pixz.core.replanning`, `pixz.core.quality-gate`, `pixz.core.change-safety`, `pixz.quality.anti-ai-slop`, `pixz.core.self-learning`
- **requires:** none (top-level composition) · **conflicts:** none
- Rationale (2.0.0): v1.1.0 made 8 capabilities mandatory aggregates; the GLM benchmark showed skills-alone ≈ no measurable advantage (B≈B1, C≈A) and 1.48× token overhead, worst on trivial tasks. Mandatory set reduced to the one structural floor; everything else activates on demand. See `docs/benchmark/GLM-benchmark-findings.md`.

## Constraints & Failure Conditions
- Fails if hard dependency missing, runtime incompatible, cycle detected, or limits exceeded.
- Fails if a subagent handoff return lacks required contract fields — return it, do not accept.
- Fails if a position flips without attributable cause (new evidence, better reasoning, changed constraint, failed verification, new requirement).
- Unbounded recursion forbidden: depth caps from `registry.json#limits`.

## Verification
- Per delegation: contract + output + evidence inspection.
- Per consequential claim: evidence recorded, source-of-record rule applied.
- Pre-completion: acceptance criteria + verification triggers satisfied; residual risks + unknowns documented.
- Pre-ship (repo work): `scripts/validate.py`, `scripts/check-cycles.py`, eval layers — run them, do not claim them.

## Structured Output
```yaml
assessment: {complexity, risk, uncertainty, reversibility, horizon, rationale}
mode: balanced
plan: [{step, owner, verification, status}]
activations: [{skill, status, reason}]
delegations: [{to, objective, return_status, inspection}]
findings: [{claim, type, evidence_refs, status}]
decisions: [{what, why, status}]
verification: {checks: [...], residual_risks: [...]}
stop_conditions: {criteria_met: bool, verification_sufficient: bool, diminishing_returns: bool}
next_action: "..."
```

## Example
> Task: "Design and ship rate-limited public API for Next.js service"
> ORIENT: inspect env (Next.js? pnpm?) + repo state. ASSESS: complexity high, risk high, reversibility partially (DB schema), horizon medium → mode deep. PLAN: contract → impl → security review → tests → verification. ACTIVATE: `pixz.engineering.api-design`, `pixz.security.review`, `pixz.core.verification` (mandatory floor), challenger on the auth/rate-limit design. DELEGATE: independent security review + test generation in parallel (independent work). VERIFY: source-of-record check on the deployment report. DECIDE: stop when criteria + checks + residual risks documented.

## Anti-Patterns
- Orchestration overhead > task value (10 skills for a rename).
- Workflow narrator: forcing 11 phases on a 2-minute task.
- Blind trust in subagent output.
- Recursive orchestration without depth guard.
- Skill spam, or silently dropping an active capability when the task moves on.

## Runtime Notes
- Claude: `.claude/skills/orchestrator/SKILL.md`; `CLAUDE.md` includes `@AGENTS.md`.
- OpenClaw: `~/.openclaw/skills/orchestrator/SKILL.md`; respects `agents.entries.*.skills` final allowlist.
- OpenCode/Hermes: generic `skills/` import via adapter.
- Super Z / GLM / Z.AI Web: operate under `ZAI.md` overlay (mode selection + compute policy; does not change this skill's semantics).

---
*See `docs/architecture.md` for the layer model and the 2.0 architecture delta.*
