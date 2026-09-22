---
name: Planning
description: Minimal, mode-sized execution plans with verifiable steps, explicit assumptions (deep mode), and defined stop conditions.
version: 2.0.0
id: pixz.core.planning
category: core
triggers: [plan, roadmap, break down task, milestone]
compatible_runtimes: [claude, openclaw, opencode, hermes, codex, generic]
---

# Planning — `pixz.core.planning`

> Plans are sized to the assessment, not to habit. A fast-mode plan is 0–2 steps; a deep-mode plan carries explicit assumptions and an evidence plan. Both are verifiable.

## Purpose
Turns vague objectives into correctly-sequenced plans whose steps close with evidence. Separate from execution (ACT) and from replanning (failure/change response).

## Methodology
1. **Size to mode:** fast 0–2 steps or none · balanced 3–7 steps · deep full plan + explicit assumptions + evidence plan (what verification will run, against which source-of-record).
2. **Decompose:** each step with inputs, outputs, owner (self/skill/agent), tools, and **the verification that closes it**. No "and then magic" steps.
3. **Sequence:** dependency-ordered; mark independent steps as parallelizable (delegation only where independence is real).
4. **Gate:** stop conditions up front — acceptance criteria met + verification sufficient + residual risks acceptable + diminishing returns.
5. **Risk note:** flag irreversible/high-scope steps for `pixz.core.change-safety`; irreversible steps get pre-action verification.
6. **Store** in task-state `plan` (strategy, iteration, steps with status). Replan bumps `iteration` — the old plan is marked, not deleted.

## Outputs
`plan` {strategy, iteration, steps[{description, owner, status, verification}], stop_conditions, risk_flags}

## Failure Conditions
- Plan step without a closing verification → not a plan step; fix or fold.
- Plan larger than the assessment warrants (10 steps for a rename) → over-planning; shrink.
- Plan ignoring known constraints (authority, budget, scope) → redo ASSESS.

---
