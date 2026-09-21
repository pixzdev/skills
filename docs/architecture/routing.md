# Routing — Task → Skill

> `scripts/resolve.py` resolves **install-time dependencies** (what a skill needs). **Runtime routing** decides which skills to apply to a task. They must not be conflated (audit #14).

## Model

```
TASK
  → TASK CLASSIFICATION (scope, risk×uncertainty×impact, requested vs necessary vs optional vs out-of-scope)
  → RELEVANT SKILL SET (filter by triggers overlap + compatible_runtimes + context sufficiency)
  → SELECTED SKILLS (orchestrator routes: WHEN/WHO/WHAT/WHY; skills define HOW)
  → UNSELECTED SKILLS + REASON (explicit)
  → EXECUTION (bounded, with change-safety gates)
  → VERIFICATION (evidence, not claims) + CHALLENGE (risk-scaled)
```

Record router decisions as structured output (selected, unselected+reason, verification depth, challenge intensity).

## Tests — Behavioral (audit #13, #14)

Each scenario evaluated on: skill selection, unnecessary activation, missed activation, verification depth, challenge activation, research depth, stop behavior, overhead, correctness, residual risk.

### Orchestrator decision tests (from `evals/behavioral/orchestrator-smoke.json`)

| Scenario | Expected routing | Not expected | Verification | Challenge | Overhead |
|----------|------------------|--------------|--------------|-----------|----------|
| trivial rename | minimal (UNDERSTAND→EXECUTE→VERIFY), 0-1 skill, no orchestrator | full loop, challenger | minimal (ls + test) | none | low |
| typo in docs | minimal | API design, security | inspection only | none | low |
| ordinary bug (single file) | capability-discovery + verification | system-design | targeted tests | none/low | low-med |
| unknown repo bug | full discover + context-engineering + environment-awareness | — | failure-mode + regression | medium if high risk | med |
| UI design task | uiux + design-system + anti-slop + accessibility | docker, kubernetes | usability + a11y | low | med |
| security-sensitive review | security.review + threat-modeling + verification | — (must include verification) | checklist + repro | high | med-high |
| production migration | orchestrator + planning + change-safety + verification + quality-gate | minimal | full impact + rollback plan | high | high |
| contradictory reports | epistemic-reasoning + challenger | — | source fidelity | high | med |
| incomplete requirements | context-engineering (ask user last) | — | sufficiency check | medium | med |
| large unfamiliar repo | environment-awareness + capability-discovery | — | repo scan evidence | medium | med |
| rapidly changing ecosystem | capability-discovery + research (official docs first) | stale cache | freshness check | medium | med |
| destructive operation | change-safety (irreversible gate) + verification | silence | reversibility + authority | high | high |
| long-running multi-agent | workflow-continuity + delegation-handoff + orchestrator | — | handoff contract + iteration cap | medium | high |
| research unnecessary (trivial) | minimal, no research | external search | — | none | low |
| research needed (risk high) | RAG / research with citation discipline | — | source evaluation | high if needed | med-high |

See `evals/behavioral/orchestrator-smoke.json` for machine-readable scenarios and runner.

### Router metrics (audit #14)

| Split | Example | Mitigation |
|-------|---------|------------|
| **Under-routing** | security task missing `verification` | hard `requires` ensures gate; `quality-gate` mandatory via orchestrator |
| **Over-routing** | rename triggers 5 skills | minimal vs full classification; `anti-ai-slop` gate |
| **Recursive routing** | orchestrator → skill → orchestrator | depth caps + cycle DFS |
| **Irrelevant activation** | UI task triggers `k8s` | trigger overlap threshold + context filter |
| **Missed safety** | prod change skips `change-safety` | static policy (reversible tiers) not routed; mandatory baseline |
| **Excessive** | 10 skills for typo | complexity-aware routing |

Current heuristic router simulation (keyword overlap) is **documented as smoke**, not production router — see `limitations` in each behavioral result.

## Circular Safety Mitigation (audit #15)

> Router must not be able to route itself out of safety.

Implemented:

1. **Mandatory baseline:** `verification` + `quality-gate` are **hard** aggregates of orchestrator — even if router mis-selects, resolver guarantees them. Tested: `python scripts/resolve.py --install pixz.core.orchestrator` always returns them.
2. **Static policy not routed:** `change-safety` reversible tiers (irreversible → confirmation) enforced before tool calls, independent of router.
3. **Risk-based hard constraint:** `risk×impact=high` (security/prod) → challenger intensity high, not skippable. Documented in `epistemic-challenger/SKILL.md`.
4. **Second-pass outside router:** `scripts/validate.py` + `scripts/check-cycles.py` run pre-ship, static.
5. **Escalation not routed away:** `replanning` ladder `retry→...→parent→user` is policy; router cannot disable it.

Not yet complexity: no independent second router (kept simple per `simplicity` policy).

## How to run

```bash
python evals/behavioral/runner.py            # routing smoke
python scripts/resolve.py --install pixz.core.orchestrator --runtime claude
python scripts/validate.py
```
