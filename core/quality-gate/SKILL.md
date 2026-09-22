---
name: Quality Gate
description: The done-decision — consolidates acceptance criteria, verification, challenge verdicts, residual risks and the orchestration budget into stop/ship/revise/replan.
version: 2.0.0
id: pixz.core.quality-gate
category: core
triggers: [quality gate, ship check, done criteria, release gate]
compatible_runtimes: [claude, openclaw, opencode, hermes, codex, generic]
---

# Quality Gate — `pixz.core.quality-gate`

> Owns the final "definition of done." Decides **stop / ship / revise / replan** — and refuses to ship on vibes.

## Purpose
Consolidates verification, challenge verdicts, risk, and the orchestration budget into one accountable decision. The gate is where "is this actually done, with evidence?" gets a yes/no.

## Methodology
Input: artifact + verification_report + challenger verdict + environment_report + findings/assumptions ledger.

The gate answers one question: **are the declared stop conditions met?** Check **all five** (each with evidence ref):
1. **Requirements satisfied** — every acceptance criterion has a closing check.
2. **Verification sufficient** — the right *kind* of verification ran (implementation/claim/artifact/regression/security/deployment) at the right moments.
3. **Critical risks addressed** — high/critical risks resolved or explicitly accepted with owner.
4. **Remaining uncertainty acceptable** — residual unknowns are recorded and do not undermine the objective.
5. **Diminishing returns** — another iteration would not materially improve the result (orchestration budget check: does more cost pay off?).

**Do not ship because it compiles or tests pass.** Those are inputs, not the verdict.

Emit the gate verdict with `residual_risks` and explicit `unknowns_accepted` (each accepted unknown: what it is, why acceptable, who owns it).

## Outputs
`gate_report` {verdict: ship|stop|revise|replan, checks[{name, evidence_ref, met}], residual_risks[], unknowns_accepted[], next_actions[]}

## Failure Conditions
- A check marked met without an evidence ref → invalid verdict; redo.
- Ship with unaddressed critical risk → blocked; escalate.
- Continuing past a justified stop "to be thorough" → orchestration budget violation; stop.

---
