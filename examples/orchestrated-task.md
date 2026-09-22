# Example — Full Orchestrated Task (production design, mode deep)

> Goal: design and ship a rate-limited public API for a Next.js monorepo.
>
> This is the **MAIN skill** (`pixz.core.orchestrator`) in action. Specialist skills answer HOW. For the full practical operating loop, see `core/orchestrator/references/operating-methodology.md`.

## 1. ORIENT & MODEL (orchestrator)

- **State?** None (new task). **Environment?** `package.json` → Next.js 15, `pnpm-lock.yaml` → pnpm. `git status` clean.
- **Requested:** “public API for external partners”
- **Necessary:** contract, rate-limit, auth, audit, tests, docs, security review
- **Optional:** SDK generation (deferred)
- **Out-of-scope:** rewrite auth system without evidence
- **Objective (restate):** expose rate-limited public endpoints with per-key quotas, verified and shipped.

## 2. ASSESS → MODE

| Band | Value | Note |
|------|-------|------|
| complexity | high | multi-file, new surface |
| risk | high | public auth + billing adjacency |
| uncertainty | medium | rate-limit semantics partially specified |
| reversibility | partially | contract + schema |
| horizon | medium | multi-phase |

→ **mode deep.** Stop conditions declared: contract reviewed + security pass + tests green + challenger upheld + gate ship.

## 3. PLAN (pixz.core.planning, deep)

| Step | Owner | Verification that closes it |
|------|-------|------------------------------|
| 1. Contract | api-design | review vs existing routes |
| 2. Impl | self/engineering | unit + integration |
| 3. Security | security.review + threat-modeling | repro each finding |
| 4. Docs | anti-ai-slop | no generic SaaS filler |
| 5. Verify | verification (floor) | source-of-record + regression |
| 6. Gate | quality-gate | diminishing-returns check |

Plan stored in `.pixz/task-state.json` (`plan.steps`, `stop_conditions`).

## 4. ACTIVATE CAPABILITIES (persistent)

```yaml
capabilities:
  - {id: pixz.engineering.api-design,      status: active, reason: "contract step"}
  - {id: pixz.security.review,             status: active, reason: "public auth, risk=high",
     reactivation_conditions: ["authentication changes", "deployment changes"]}
  - {id: pixz.core.verification,           status: active, reason: "mandatory evidence floor"}
  - {id: pixz.core.epistemic-challenger,   status: activated, reason: "high impact auth design"}
  - {id: pixz.quality.anti-ai-slop,        status: active, reason: "public docs"}
```
Rejected with reason: `pixz.devops.kubernetes` (no deploy target in scope), `pixz.motion.gsap` (no UI motion in scope).

## 5. DELEGATE (pixz.core.delegation-handoff — economics passed: independent security review)

Dispatch per `schemas/handoff.schema.json`:
```json
{
  "objective": "Security review of the rate-limit + auth contract",
  "constraints": ["no breaking internal API", "p95 <200ms", "read-only, do not modify"],
  "context_packet": { "decisions": ["per-key quota"], "evidence_refs": ["contract.yaml"] },
  "success_criteria": ["STRIDE covered", "each finding reproducible"]
}
```
Return **must** include work_performed, findings, evidence, assumptions, unknowns, decisions, tests, verification, remaining_work, recommended_next_action — parent inspects and records `accepted`.

## 6. ACT → OBSERVE → VERIFY → CHALLENGE

Challenger (intensity ≈ risk high × uncertainty medium × impact high × irreversibility partial = **high**):
- “How could rate-limit be bypassed?” → found missing per-API-key partition → **revised**.
- Falsification test: `100 rps with 10 keys, expect 429 after quota`.
- Stop rule met: disconfirming evidence found; verdict `revised`, recorded.

Verification (source-of-record applied to the deploy/contract claims):
```yaml
checks_performed: ["source-of-record: contract file vs described behavior", "regression: existing routes", "failure-mode: replay", "change-impact: billing"]
evidence:
  - {id: e1, kind: test_result, source: "pnpm test", summary: "142 passed"}
  - {id: e2, kind: artifact, source: "openapi/public.yaml", summary: "3 endpoints, quota headers"}
residual_risks: ["partner clock-skew not load-tested at 10k rps"]
```

## 7. DECIDE → GATE → SHIP

Quality-gate (all five with evidence refs): requirements satisfied ✓ · verification sufficient ✓ · critical risks addressed ✓ · uncertainty acceptable ✓ · diminishing returns ✓ → **SHIP**, with a follow-up task (load test at 10k rps) recorded in `next_action` and the follow-up task's state.

Task-state left for continuation: decisions (marked, not deleted), findings (typed, with transitions), evidence ledger, capability states, residual risks.

---
*Task state conforms to `schemas/task-state.schema.json`; handoff to `schemas/handoff.schema.json`; resolver validated no cycles. Mode deep was chosen by assessment, not habit — a trivial rename in the same repo would run `fast` with zero activations.*
