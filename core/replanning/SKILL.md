---
name: Replanning
description: Failure recovery and structured replanning — classify, hypothesize, test, repair, regression-check; each retry must add information; bounded escalation ladder.
version: 2.1.0
id: pixz.core.replanning
category: core
triggers: [replan, pivot, strategy failed, alternative approach, failure, recovery]
compatible_runtimes: [claude, openclaw, opencode, hermes, codex, generic]
---

# Replanning — `pixz.core.replanning`

> **Specialist HOW skill (recovery).** For practical multi-step operating methodology — when to re-plan vs re-initiate vs iterate — activate the **MAIN skill** `pixz.core.orchestrator`. Load `core/orchestrator/references/operating-methodology.md` for the full re-plan / re-initiate / super-iteration rules.
>
> No blind retry. A retry that changes nothing is a loop, not a recovery. Each retry must **add information** — recorded in task-state `failures[]`.

## Purpose
Formal failure recovery + structured replanning when verification fails, evidence contradicts the plan, or constraints change. Preserves the objective; discards the plan when the plan is what's wrong.

## Failure Recovery Ladder (formal)

```
FAIL → CLASSIFY → INSPECT → ISOLATE → HYPOTHESIS → TEST → REPAIR → REGRESSION CHECK → CONTINUE
```

1. **CLASSIFY:** environment | assumption | specification | implementation | external | unknown. (Most "mysterious" failures are environment or assumption — check those first.)
2. **INSPECT:** read the actual error/output. Source-of-record: the real error text, not a summary of it.
3. **ISOLATE:** minimal repro; pin the failure to one component/step.
4. **HYPOTHESIS:** one root-cause hypothesis with a falsification test. (No "it's probably X" without a test.)
5. **TEST:** run the falsification test. Pass → repair. Fail → next hypothesis (record both).
6. **REPAIR:** smallest change that fixes the classified cause.
7. **REGRESSION CHECK:** verify the fix didn't break what was working (targeted tests).
8. **CONTINUE:** update task-state (failure entry: what, classification, hypothesis, tested, resolution, **lesson**); resume from `next_action`.

## Escalation Ladder (when the ladder stalls)
retry → inspect → alternate approach → research (official sources first) → specialist (delegation) → challenge → parent → user (ask only for genuinely missing information, precisely).

## Replanning (not just failure)
Triggers: failed verification · falsified assumption · contradictory evidence · changed requirement/constraint.
1. Diagnose: which premise broke? (the failure entry is the input)
2. Enumerate alternatives with tradeoffs (via `pixz.core.epistemic-reasoning`)
3. Re-plan the **minimal delta**; mark the old plan superseded; bump `plan.iteration`
4. **Bound:** `limits.max_iterations` (8) on plan iterations. Diminishing returns → stop, record residual, escalate or defer.

## Rules
- **REINITIATE** (plan fundamentally flawed: evidence disproves its premise) = discard the plan, **not** the objective; restart modeling with new assumptions. It is a decision, not a state.
- Every failure entry must have a `lesson` — the thing the next attempt must not repeat.
- Never retry the identical action after a recorded failure without a new hypothesis.

## Outputs
`replan_artifact` {failure: {what, classification, hypothesis, tested, resolution, lesson}, alternatives[], new_plan, iteration, escalation_level}

---
