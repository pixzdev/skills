---
name: Verification
description: Evidence-based verification — inspection, regression, consistency and impact analysis before shipping.
version: 1.0.1
id: pixz.core.verification
category: core
triggers: [verify, inspect, validate, check correctness, regression, impact analysis]
compatible_runtimes: [claude, openclaw, opencode, hermes]
---

# Verification — `pixz.core.verification`

> Compilation is not correctness. Tests are evidence, not proof.

## Purpose
Provides the inspection/verification discipline that gates shipping. Separate from the ship decision (owned by `quality-gate`).

## Triggers
- Pre-ship for any non-trivial change
- After INSPECT or CHALLENGE in orchestrator loop; after replanning

## Methodology

### 1. Five Checks (apply proportionally)
- **inspection** — read artifact against requirements; does it actually satisfy the stated objective?
- **failure-mode analysis** — how could this fail in prod? (use `change-safety` risk tiers)
- **regression awareness** — what existing behavior could this break? Run targeted tests/inspections.
- **consistency checking** — does change contradict existing conventions, types, schema, docs?
- **change-impact analysis** — blast radius: who/what downstream is affected?

### 2. Evidence, Not Claims
Record `checks_performed` + `evidence` + `results` with source. Do not mark “verified” without evidence artifact (test output, diff, reproduction steps, citation).

### 3. Distinguish Proven vs Trusted
- **Proven:** reproduced + inspected + regression-checked
- **Trusted:** cited primary source but not reproduced — keep confidence capped at medium
- **Unknown:** neither — must remain UNKNOWN with residual risk

### 4. Regression Discipline
At minimum: run relevant tests/lints/type-checks; note environment (OS, runtime) from `environment-awareness`. Compilation ≠ correctness.

### 5. Report Residual Risks
Even on pass, list unknowns and risks that remain after verification. Residual risks feed `quality-gate`.

## Inputs / Outputs
- **Inputs:** artifact, requirements, assumptions ledger, environment report
- **Outputs:** `verification_report` {checks_performed[], evidence[], results (pass|fail|conditional), residual_risks[], recommended_next_actions[]}

## Failure Conditions
- Verification steps skipped due to time → fail; do not wave through.
- Tests pass but manual inspection would have caught contradiction → fail open → require inspection.

## Structured Output
```yaml
checks_performed: ["inspection vs requirements", "failure-mode: token replay", "regression: auth.spec.ts"]
evidence: [{claim: "All auth specs green", source: "pnpm test auth.spec.ts:14 passed", strength: high}]
results: conditional_pass  # pending: load test not run
residual_risks: ["replay under clock-skew not verified"]
recommended_next_actions: ["Run chaos-clock test"]
```

## Relationship
- Consumes `epistemic-reasoning` arguments; challenged by `epistemic-challenger`; gates `quality-gate`.
---
