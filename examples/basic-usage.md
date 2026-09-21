# Example — Basic Usage (single skill, minimal orchestration)

> Goal: fix a pnpm vs npm assumption bug without full orchestration.

## Task
> “Tests fail on CI but pass locally — `npm test` works locally, CI uses `pnpm`.”

## Complexity Gate
Scope: one file, reversible, risk low → `minimal` workflow: UNDERSTAND → EXECUTE → VERIFY (no orchestrator, no challenger).

## Steps

### 1. DISCOVER (via context-engineering + environment-awareness)

```bash
cat package.json          # check packageManager field
ls -la | grep lock        # pnpm-lock.yaml exists
cat AGENTS.md             # notes: use pnpm, not npm
```

**Findings:**
- `packageManager: pnpm@9`, `pnpm-lock.yaml` mtime today
- Local env used `npm` (hallucinated assumption)
- CI correctly uses `pnpm`

### 2. EXECUTE (via least privilege)

```bash
pnpm install
pnpm test
```

Fix: replace docs that say `npm install` with `pnpm install`; add `engine-strict` guard.

### 3. VERIFY

```yaml
checks:
  - "pnpm-lock.yaml present → pnpm is authoritative"
  - "pnpm test: 12 passed"
residual_risks: []
verification: pass
```

### 4. Structured Output (excerpt)

```yaml
findings: ["Package manager mismatch: pnpm vs npm"]
assumptions: [{claim: "CI env matches local", basis: "local success", fragility: high, validated: false}]
evidence: [{claim: "pnpm-lock.yaml exists", source: "ls", strength: high}]
confidence: high
basis: ["primary: lockfile", "reproduced: pnpm test passes"]
```

No challenger needed — risk × uncertainty × impact low. If this were prod auth, escalation to `epistemic-challenger` + `quality-gate` would trigger.
