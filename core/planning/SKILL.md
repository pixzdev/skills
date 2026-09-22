---
name: Planning
description: Minimal, mode-sized execution plans with verifiable steps, explicit assumptions (deep mode), and defined stop conditions. Use before substantial multi-step work. Do not write a 10-step plan for a rename. Operating loop lives in MAIN skill pixz.core.orchestrator.
version: 2.1.0
id: pixz.core.planning
category: core
triggers: [plan, roadmap, break down task, milestone]
compatible_runtimes: [claude, openclaw, opencode, hermes, codex, generic]
---

# Planning — `pixz.core.planning`

> **Specialist HOW skill (planning).** For the full practical operating methodology — define, research, delegate, inspect, challenge, verify, replan, ship — activate the **MAIN skill** `pixz.core.orchestrator`. Load `core/orchestrator/references/operating-methodology.md` when the plan is for complex work.
>
> Plans are sized to the assessment, not to habit. A fast-mode plan is 0–2 steps; a deep-mode plan carries explicit assumptions and an evidence plan. Both are verifiable.

## Purpose

Turns vague objectives into correctly-sequenced plans whose steps close with evidence. Separate from execution (ACT) and from replanning (failure/change response).

## When to Use / When NOT

| Use | Do not |
|-----|--------|
| Multi-step work, unknown sequencing, multiple owners | Trivial reversible edit — skip to ACT |
| Deep mode (assumptions + evidence plan required) | Replacing a failed plan (that's `pixz.core.replanning`) |

## Methodology

1. **Size to mode:** fast 0–2 steps or none · balanced 3–7 steps · deep full plan + explicit assumptions + evidence plan (what verification will run, against which source-of-record).
2. **Decompose:** each step with inputs, outputs, owner (self/skill/agent), tools, and **the verification that closes it**. No "and then magic" steps.
3. **Sequence:** dependency-ordered; mark independent steps as parallelizable (delegation only where independence is real).
4. **Gate:** stop conditions up front — acceptance criteria met + verification sufficient + residual risks acceptable + diminishing returns.
5. **Risk note:** flag irreversible/high-scope steps for `pixz.core.change-safety`; irreversible steps get pre-action verification.
6. **Store** in task-state `plan` (strategy, iteration, steps with status). Replan bumps `iteration` — the old plan is marked, not deleted.

> **Plans are disposable. Objectives are not.** If evidence contradicts the plan, change the plan (`pixz.core.replanning`). Do not keep executing an obsolete sequence.

### Practical step template

```yaml
- id: p3
  description: "Add object-level authz on GET /v1/items/:id"
  owner: self
  skill: pixz.engineering.api-design
  inputs: ["openapi/public.yaml", "auth middleware"]
  outputs: ["policy check + tests"]
  verification: "request as user B for user A's id → 403; source-of-record = test output"
  irreversibility: reversible
  status: pending
```

## Outputs

`plan` {strategy, iteration, steps[{description, owner, status, verification}], stop_conditions, risk_flags}

## Failure Conditions

- Plan step without a closing verification → not a plan step; fix or fold.
- Plan larger than the assessment warrants (10 steps for a rename) → over-planning; shrink.
- Plan ignoring known constraints (authority, budget, scope) → redo ASSESS.

## Example

> Mode balanced, "add export CSV to reports". Steps: (1) confirm columns from existing UI — verify by reading the table component; (2) endpoint + authz — verify with 403/200 tests; (3) UI download — verify keyboard + empty state. Stop: tests + one manual download. Not in plan: rewrite of reporting pipeline.

## Main Skill

Planning is one move in the operating loop. Use `pixz.core.orchestrator` to decide whether a plan is even needed.
