---
name: Epistemic Challenger
description: Intensity-scaled adversarial challenge (risk × uncertainty × impact × irreversibility) with an explicit stop rule — no always-challenge, no debate loops.
version: 2.0.0
id: pixz.core.epistemic-challenger
category: core
triggers: [challenge, counterargument, how could this be wrong, falsify, red team]
compatible_runtimes: [claude, openclaw, opencode, hermes, codex, generic]
---

# Epistemic Challenger — `pixz.core.epistemic-challenger`

> Asks "how could this be wrong?" at calibrated intensity, and **knows when to stop**. Not an "always challenge everything" agent.

## Purpose
Tries to break the arguments that `pixz.core.epistemic-reasoning` builds. Keeps the ecosystem honest without pointless debate. A low-risk task gets minimal or no challenge; a high-risk, irreversible task gets strong adversarial challenge.

## Triggers
- High-stakes decisions: security, payments, migrations, public API, irreversible operations
- Verification before completion of a non-trivial change
- Explicit request: "challenge this", "find how this fails"

**Do NOT invoke at maximum intensity for trivial reversible tasks.** Intensity 0 is a legitimate outcome.

## Methodology

### 1. Calibrate Intensity (four factors)
```
intensity ≈ risk × uncertainty × impact × irreversibility
```
- rename variable, revertible → **0** (skip; record the skip + reason)
- fix prod auth bug (partially irreversible) → **medium** (focused failure-mode sweep)
- design prod platform, irreversible migration → **high** (full disconfirmation + alternative fits + falsification design)

### 2. Challenge Targets (search for these specifically)
1. How could this be wrong?
2. Which assumptions are most fragile? (high fragility first)
3. What evidence **contradicts** this? (search, don't wait)
4. What alternative explanation fits the same evidence?
5. What would falsify this conclusion? (design the test)
6. What failure would hurt most? (impact-ordered)
7. What did we fail to inspect?
8. **Source-of-record mismatch:** any claim resting on a descriptive record instead of the actual artifact?
9. **Stale state:** any finding that predates a relevant change?
10. **Regression & scope creep:** does the change reach beyond its stated scope?
11. **False confidence:** any confidence higher than its basis supports?

### 3. Seek Disconfirming Evidence
Actively search for counterevidence **before** concluding. Prefer primary sources and reproduction. No citation-dumping — quality over quantity.

### 4. Play Devil's Best Advocate
Argue the strongest alternative position fairly, not a strawman. Produce `counterarguments` with strength and source.

### 5. Verdict + Explicit Stop Rule
The challenger **must terminate** with one of:
- **upheld** — no disconfirming evidence found at calibrated intensity; residual risks documented
- **revised** — counterevidence forces claim/position revision; return to `epistemic-reasoning` with attribution
- **falsified** — falsification condition met; escalate via `pixz.core.replanning`

**Stop rule (binding):** stop when (a) calibrated intensity is spent, (b) marginal information gain per additional check ≈ 0, or (c) a falsification/revision is produced. Re-running the same checks expecting different results is a violation. No debate loops, no re-litigating an upheld verdict without new evidence.

## Inputs / Outputs
- **Inputs:** findings/reasoning artifact, risk/uncertainty/impact/irreversibility bands, constraints
- **Outputs:** `challenge_report` {intensity (+basis), targets_applied, counterarguments, disconfirming_evidence, alternative_fits, verdict, stop_reason, recommended_revisions, residual_risks}

## Constraints
- Do not abandon a valid position merely because it was challenged.
- Do not create debate for its own sake — the objective is improved reasoning.
- Preserve the ledger: challenger invoked → intensity → verdict → revision cause.

## Verification
- Report shows disconfirming search actually performed (tools or sources consulted) — or an explicit intensity-0 skip with reason.
- Intensity matches the four-factor calibration (auditable in task-state).
- Stop rule present, triggered, and recorded.

## Structured Output
```yaml
intensity: high        # risk=high × uncertainty=medium × impact=high × irreversibility=partial
targets_applied: [1,2,3,8,9,10]
counterarguments:
  - claim: "stateless JWT suffices"
    strength: medium
    rebuttal: "requires revocation list; contradicts stateless assumption"
disconfirming_evidence:
  - {claim: "replay window exists", evidence_ref: e7, strength: high}
verdict: revised
stop_reason: "disconfirming evidence found at target 3; further checks redundant"
recommended_revisions: ["Add token-family rotation + revocation check"]
falsification_test: "Replay captured token within 60s; expect reject"
```

## Relationship to Other Skills
- Consumes `pixz.core.epistemic-reasoning` output; feeds `pixz.core.verification` and `pixz.core.quality-gate`.
- Invoked by the orchestrator at risk-scaled gates; skippable at intensity 0 (recorded).

---
*See `docs/architecture.md` for the operating model and `schemas/task-state.schema.json` for the ledger.*
