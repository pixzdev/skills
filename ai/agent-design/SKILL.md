---
name: Agent Design
description: Design tool-enabled agents with bounded autonomy, tool contracts, verification and escalation. Use when specifying an agent. Do not grant unbounded tools. The runtime operating layer is MAIN skill pixz.core.orchestrator — use it for practical operation.
version: 1.2.0
id: pixz.ai.agent-design
category: ai
triggers: [agent design, tool calling, orchestration, autonomous agent]
compatible_runtimes: [claude, openclaw, opencode, hermes, codex, generic]
---

# Agent Design — `pixz.ai.agent-design`

> **Specialist HOW skill.** This designs *an* agent. For practical multi-step operating methodology of *this* agent, activate the **MAIN skill** `pixz.core.orchestrator` and load `core/orchestrator/references/operating-methodology.md`.

## Purpose

Tool-enabled agents that are useful *and* bounded: allowlists, loop caps, verification, human gates for irreversible work.

## When to Use / When NOT

| Use | Do not |
|-----|--------|
| Specifying a new agent, tool set, or subagent role | Implementing a one-off script with no tools |
| Adding tools to an existing agent | Granting "all tools" to skip design |

## Methodology

### 1. Bound autonomy

- Loop cap (`max_iterations`) and a wall-clock/budget cap.
- Tool allowlist — deny-by-default.
- Scope ticket: what the agent may change (paths, envs, APIs).
- Human gate for irreversible/high-impact actions (`pixz.core.change-safety`), including autonomous mode.
- Stop conditions: success criteria, budget exhausted, repeated identical failure, missing authority.

### 2. Tool contract (every tool)

Each tool documents:

```yaml
name: ...
purpose: one sentence
inputs: {schema, required}
outputs: {schema}
failure_modes: [timeout, 4xx, empty, permission]
idempotency: true|false
side_effects: none|writes|external
auth_scope: ...
```

If a tool cannot be described this way, it is not ready to expose.

### 3. Orchestrate vs execute

- `pixz.core.orchestrator` determines WHEN / WHO / WHAT / WHY / HOW DEEPLY.
- Domain skills determine HOW.
- Recursive orchestration is capped (`registry.json#limits`). Subagents do not spawn subagents.
- Context isolation + structured return (`schemas/handoff.schema.json`). No "looks good" returns.

### 4. Memory & state

- Durable state in files (task-state, artifacts), not hidden chain-of-thought.
- Compaction: pin objective, constraints, decisions, next_action before compressing.

### 5. Verify & escalate

Plan includes verification (`pixz.core.verification`) + challenger at calibrated intensity + escalation ladder:

```
retry → inspect → alternate → research → specialist → challenge → parent → user
```

Each retry must add information.

### 6. Evaluation

- Golden tasks with expected tools (and forbidden tools).
- Budget tests: trivial tasks must not activate the whole swarm.
- Failure injection: tool error, empty retrieval, contradictory docs.

## Failure Conditions

- Unbounded `bash` / unrestricted browser on a production agent → blocked.
- No loop cap → blocked.
- Tools without schemas or failure modes → incomplete contract.

## Example

> "Docs-Q&A agent." Tools: `search_docs`, `read_chunk` (read-only). No shell. Loop cap 8. If retrieval UNKNOWN, stop and ask. Eval: 30 gold questions, citation required, zero invented URLs. Trivial greeting must use zero tools.

## Structured Output

```yaml
agent_spec:
  objective: ...
  allowlist: [...]
  caps: {iterations, budget}
  tools: [{name, purpose, io, failure_modes, idempotency}]
  gates: {irreversible: confirm}
  verification: [...]
  escalation: [...]
  evals: [...]
```

## Main Skill

Designing the agent is this skill. *Operating* it in production is `pixz.core.orchestrator`.
