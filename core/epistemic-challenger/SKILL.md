---
name: Epistemic Challenger
description: Adaptive challenger that stress-tests claims by seeking disconfirming evidence and failure modes.
version: 1.1.0
id: pixz.core.epistemic-challenger
category: core
triggers: [challenge, counterargument, how could this be wrong, falsify]
compatible_runtimes: [claude, openclaw, opencode, hermes, codex, generic]
---

# Epistemic Challenger — `pixz.core.epistemic-challenger`

> Asks “How could this be wrong?” with intensity scaled to risk, and an exit condition.

## Purpose
Distinct from reasoning (which builds arguments), challenger tries to break them. Keeps the ecosystem honest without pointless debate.

## Triggers
- Verification phase before ship; high-stakes decisions (security, payments, migration, public API)
- Explicit request: “challenge this”, “find how this fails”

Do NOT invoke at maximum intensity for trivial reversible tasks.

## Methodology

### 1. Calibrate Intensity
```
intensity ≈ risk × uncertainty × impact
```
- rename variable → intensity 0 (skip)
- fix prod auth bug → medium (focused failure-mode sweep)
- design prod AI platform → high (full disconfirmation + alternative fits + falsification design)

### 2. Seven Challenge Questions
1. How could this be wrong?
2. What assumptions are most fragile? (high fragility first)
3. What evidence contradicts this?
4. What alternative explanation fits the same evidence?
5. What would falsify this conclusion? (design test)
6. What failure would hurt most? (impact-ordered)
7. What did we fail to inspect?

### 3. Seek Disconfirming Evidence
Actively search for counterevidence before concluding. Prefer primary sources and reproduction. Do not citation-dump — quality over quantity.

### 4. Play Devil’s Best Advocate
Argue the strongest alternative position fairly, not a strawman. Produce `counterarguments` with strength and source.

### 5. Deliver Verdict + Exit
Challenger must terminate with one of:
- **upheld** — no disconfirming evidence found at calibrated intensity; residual risks documented
- **revised** — counterevidence forces claim/position revision; return to `epistemic-reasoning` with attribution
- **falsified** — falsification condition met; escalate via `replanning`

No infinite loops. If additional iteration has diminishing returns, note residual unknowns and defer.

## Inputs / Outputs
- **Inputs:** `reasoning_artifact` from epistemic-reasoning, risk/impact scores, constraints
- **Outputs:** `challenge_report` {intensity, questions_applied, counterarguments, disconfirming_evidence, alternative_fits, verdict, recommended_revisions, residual_risks}

## Constraints
- Do not abandon a valid position merely because challenged.
- Do not create debate for its own sake — objective is improved reasoning.
- Must preserve the argument ledger: origin challenger → verdict → revision cause.

## Verification
- Report shows disconfirming search actually performed (tools or sources consulted).
- Intensity matches risk×uncertainty×impact (auditable).
- Exit condition present and verifiable.

## Structured Output
```yaml
intensity: high  # basis: risk=high × uncertainty=medium × impact=high
questions:
  - q: "How could this be wrong? Attacker replays valid token after rotation"
    finding: "No replay window check found — contradicted by docs chap 3"
counterarguments:
  - claim: "stateless JWT suffices"
    strength: medium
    rebuttal: "requires revocation list; contradicts stateless assumption"
verdict: revised
recommended_revisions: ["Add token-family rotation + revocation check"]
falsification_test: "Replay captured token within 60s; expect reject"
```

## Relationship to Other Skills
- Consumes `pixz.core.epistemic-reasoning` output; feeds `pixz.core.verification` and `pixz.core.quality-gate`.
- Called by orchestrator during INSPECT→CHALLENGE at risk-scaled gate.

---
*See `docs/architecture.md` for orchestration flow and `schemas/workflow.schema.json` for ledger.*
