---
name: Workflow Continuity
description: Persistent task state, checkpointing, and resumability across compaction, session restart, subagent handoff, model change and runtime change.
version: 2.1.0
id: pixz.core.workflow-continuity
category: core
triggers: [workflow, continue, resume, handoff, persist state, task state, checkpoint]
compatible_runtimes: [claude, openclaw, opencode, hermes, codex, generic]
---

# Workflow Continuity — `pixz.core.workflow-continuity`

> **Specialist HOW skill (state).** For practical multi-step operating methodology, activate the **MAIN skill** `pixz.core.orchestrator`. Load `core/orchestrator/references/operating-methodology.md` for long-horizon / second-pass work that must survive compaction.
>
> Continuity is a **file-based substrate**, not a conversation habit. Context compaction, session restarts, model changes and runtime changes all destroy conversation; they do not destroy a well-formed state file.

## Purpose
Defines the task-state model, checkpoint discipline, and resume protocol. Persistence mechanism varies per runtime (filesystem default, in-memory for constrained runners, MCP state server) — the logical model does not.

## Triggers
- Continuation of any prior task (session restart, resume, handoff back from a subagent)
- Long-horizon work; any task expected to outlive one session step
- Context compaction event; model or runtime switch

## Methodology

### 1. Model (`schemas/task-state.schema.json`)
One file per task (default: `.pixz/task-state.json`). Required at minimum:
```
task_id, objective, acceptance_criteria, constraints, status, mode, assessment,
plan, decisions[], findings[], evidence[], capabilities[], failures[],
unknowns, verification, delegations[], next_action, checkpoint
```
Entries are **summaries + references** — never transcripts. Keep the file small enough to re-inject cheaply.

### 2. Checkpoint Discipline
Write a checkpoint: before long substeps · before irreversible actions · at phase boundaries · after material findings · before delegation dispatch. A checkpoint = objective + assessment + active plan + key decisions + open items + `next_action`.

### 3. Resume Protocol (deterministic)
1. Read task-state first — before any other context.
2. Restate objective + acceptance criteria (goal-drift counter).
3. Honor `next_action`.
4. Re-establish all capabilities with status `active` / `reactivation_required` (re-load skill bodies only if needed).
5. Check for stale assumptions: any `findings` of type `assumption`/`unverified` whose conditions may have changed get re-checked.
6. Continue. Never re-derive decisions from memory — decisions are **marked, never deleted** (active/superseded/revoked).

### 4. Propagation to Children
Child inherits (via `schemas/handoff.schema.json` context packet): objective, requirements, constraints, relevant decisions, assumptions, evidence refs, verification requirements, success criteria. It does **not** inherit the whole conversation.

### 5. Iteration & Observability
Bump `plan.iteration` on replan; cap at `limits.max_iterations` (8). Any observer reading the state file can answer: what is the objective, what is done, what is pending, which decisions are active, which capabilities are active, what is verified, what remains, what is the next action.

## Persistence Abstraction
- **Logical state per schema** — universal core.
- **Adapter implements storage:** `.pixz/task-state.json` on filesystem (default — re-injectable after compaction), in-memory for constrained runners, MCP state server.
- Never require every runtime to share the same storage; require the same logical fields.

## Inputs / Outputs
- **Inputs:** existing task state (or task spec), checkpoint trigger, resume trigger
- **Outputs:** `continuity_envelope` {state_path, checkpoint, propagated_packet, resume_receipt}

## Failure Conditions
- Child loses parent constraints or decision history → fail handoff.
- State diverges without an entry (a change happened, state doesn't reflect it) → fail verification.
- Resume without re-stating objective → drift risk; redo step 2.

## Verification
- Handoff round-trip: can the parent reconstruct everything it needs from the child's structured return?
- Re-entry test: kill the session, resume from state, and confirm the agent continues correctly from `next_action`.
- Stale-state detection: no `assumption` older than a relevant change survives without re-check.

---
