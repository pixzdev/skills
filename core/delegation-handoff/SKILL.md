---
name: Delegation & Handoff
description: Bounded delegation with an explicit economics test, structured dispatch contract, mandatory structured return, and parent inspection — no "looks good" returns.
version: 2.1.0
id: pixz.core.delegation-handoff
category: core
triggers: [delegate, handoff, subagent, dispatch task]
compatible_runtimes: [claude, openclaw, opencode, hermes, codex, generic]
---

# Delegation & Handoff — `pixz.core.delegation-handoff`

> **Specialist HOW skill (dispatch contract).** For practical multi-step operating methodology — who to summon, how to coordinate, how to inspect — activate the **MAIN skill** `pixz.core.orchestrator`. Load `core/orchestrator/references/operating-methodology.md` for the specialist catalog and swarm rules.
>
> Delegation is a **context-isolation + parallelism** mechanism, not a capability upgrade. A subagent earns its existence only when the economics test passes.

## Purpose
Bounded dispatch with explicit inputs, constraints, success criteria, and a **mandatory structured return** — preserving continuity and accountability.

## The Economics Test (pass before delegating)

```
expected information gain  +  parallelism benefit  +  specialization benefit  >  coordination cost
```

**Good candidates:** independent research · independent verification · security review · test generation · alternative-implementation analysis.
**Bad candidates:** dependent edits · shared mutable state · unclear ownership · conflicting architecture decisions · "second opinion" ceremony on trivial work.

If the test fails, do it yourself (or skip) and **record the decision + reason** in task-state — restraint is observable behavior, not silence.

## Methodology
1. **Package** per `schemas/handoff.schema.json`: objective (bounded subset, never the whole task), constraints (scope, authority, reversibility note, iteration cap), context_packet (relevant decisions, assumptions, evidence refs, verification requirements — not the whole conversation), success_criteria (observable).
2. **Bound:** one independent responsibility per subagent. Subagents do **not** spawn subagents (recursion protection; caps from `registry.json#limits`).
3. **Dispatch:** child inherits semantics; not an isolated chatbot. Log the dispatch in task-state `delegations[]`.
4. **Receive + Inspect (mandatory):** the return must contain: work_performed, findings, evidence, assumptions, unknowns, decisions, tests, verification (result+checks+residual_risks), remaining_work, recommended_next_action. **Missing field → reject the return**, do not accept partial. Inspect: does the evidence back the claims? Was scope controlled? Verdict: `accepted | returned_to_agent | escalated`.
5. **Merge:** accepted findings/evidence flow into parent task-state; the child's state_digest is retained.

## Parallelism Rules
Parallelize by **evidence independence**, not agent count. Independent investigations may run in parallel; anything sharing mutable state, dependent edits, or architecture authority runs serially with clear ownership.

## Outputs
`handoff_envelope` {dispatch, return, inspection}

## Failure Conditions
- Delegation without passing the economics test → over-delegation; record and avoid repeating.
- Return missing required fields → reject; one bounded re-dispatch, then escalate.
- Parent trusts a return without inspection → accountability failure; redo inspection.

---
