# Example — Full Orchestrated Task (production design)

> Goal: design and ship a rate-limited public API for a Next.js monorepo.

## 1. UNDERSTAND (orchestrator)

- **Requested:** “public API for external partners”
- **Necessary:** contract, rate-limit, auth, audit, tests, docs, security review
- **Optional:** SDK generation (deferred)
- **Out-of-scope:** rewrite auth system without evidence

Stop conditions: contract reviewed + security review pass + tests green + challenger upheld + quality-gate ship.

## 2. DISCOVER

```bash
python scripts/resolve.py --install pixz.core.orchestrator --runtime claude --channel stable
# → resolves 10 skills
cat package.json          # Next.js 15, pnpm
ls apps/web/src/app/api   # existing internal routes
```

**Skills selected:** `planning`, `context-engineering`, `environment-awareness`, `api-design`, `security.review`, `threat-modeling`, `verification`, `epistemic-challenger`, `quality-gate`, `anti-ai-slop` (docs).

Complexity: `full` → full loop with challenge.

## 3. PLAN (pixz.core.planning)

| Step | Owner | Inputs | Outputs | Verification |
|------|-------|--------|---------|--------------|
| 1. Contract | api-design | requirements | OpenAPI + error schema | review vs existing routes |
| 2. Impl | engineering | contract | handlers + middleware | unit + integration |
| 3. Security | security.review + threat-modeling | contract + code | STRIDE + findings | repro each finding |
| 4. Docs | anti-ai-slop | contract | public docs | no generic SaaS filler |
| 5. Verify | verification | artifact | report + residual Risks | challenger interrogation |
| 6. Ship | quality-gate | all above | gate verdict | diminishing returns check |

## 4. DELEGATE (pixz.core.delegation-handoff)

Each delegation carries:
```json
{
  "objective": "...",
  "constraints": ["no breaking internal API", "p95 <200ms"],
  "phase": "EXECUTE",
  "context_packet": { "facts": [...], "sources": [...] },
  "expected_outputs": ["OpenAPI YAML", "verification block"],
  "success_criteria": ["review pass", "no critical residual"]
}
```

## 5. INSPECT & CHALLENGE

Challenger (intensity high due to public auth impact):
- “How could rate-limit be bypassed?” → found missing per-API-key partition → revised.
- Falsification test: `100 rps with 10 keys, expect 429 after quota`.

## 6. VERIFY → QUALITY-GATE

```yaml
checks_performed: ["inspection vs contract", "regression: existing routes", "failure-mode: replay", "change-impact: billing"]
evidence: [{claim: "All specs green", source: "pnpm test", strength: high}]
residual_risks: ["partner clock-skew not load-tested at 10k rps"]
verdict: conditional_ship  # with monitoring task
```

Ledger records: decisions, counterarguments, confidence basis, iteration history (2 iterations).

## 7. SHIP

Quality-gate: requirements satisfied + verification sufficient + critical risks addressed + remaining uncertainty acceptable → **SHIP** with follow-up task for load test at 10k rps.

---
*Workflow state conforms to `schemas/workflow.schema.json`; resolver validated no cycles.*
