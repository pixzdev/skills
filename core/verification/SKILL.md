---
name: Verification
description: Evidence-based verification as a continuous loop — source-of-record discipline, the verification-depth ladder (claim depth must match evidence depth), triggered checks, typed verification, residual risks.
version: 2.2.0
id: pixz.core.verification
category: core
triggers: [verify, inspect, validate, check correctness, source of record]
compatible_runtimes: [claude, openclaw, opencode, hermes, codex, generic]
---

# Verification — `pixz.core.verification`

> **Specialist HOW skill (evidence).** For practical multi-step operating methodology, activate the **MAIN skill** `pixz.core.orchestrator` — verification is its mandatory evidence floor. Load `core/orchestrator/references/operating-methodology.md` for "code is not proof", second pass, and ship criteria.
>
> Compilation is not correctness. Tests are evidence, not proof. **A record is not the thing.**

## Purpose
Provides the inspection/verification discipline that gates every consequential claim and action. Verification is a **continuous loop**, not a final ceremony. Separate from the ship decision (owned by `pixz.core.quality-gate`).

## Triggers (verify at these moments, proportionally)
- **Before irreversible action** (deploy, migration, delete, send)
- **After significant mutation** (code, data, config, dependency, architecture)
- **Before consequential claims** (reports to the user, handoffs, docs)
- **Before handoff** (a subagent's return is inspected, not trusted)
- **Before completion** (acceptance criteria + residual risks)

## Methodology

### 1. Source-of-Record Protocol (formal — promotes the T11 benchmark finding)
A commit message, log, summary, agent report, documentation, or generated metadata is a **descriptive record** — never assume it is authoritative merely because it looks authoritative.

For claims about **actual system state**, prefer the primary source:

| Claim concerns | Verify against (primary) | Not against (descriptive) |
|----------------|--------------------------|---------------------------|
| files/content | actual filesystem (`ls`, `cat`, checksum) | summaries, docs, commit messages |
| git history/branch | actual git tree (`git log`, `git status`, `git show`) | PR descriptions, release notes |
| behavior | actual test run / command output (fresh) | "tests passed" reports, CI badges in docs |
| deployment | actual deployed state (probe the endpoint) | deploy logs, status pages, agent reports |
| dependency versions | actual installed (lockfile + `--version`) | package.json alone, docs |

When a descriptive record is checked against a primary artifact, record `verified_against` on the evidence entry. When it is **not** checked, the evidence is explicitly unverified — and the claim it supports carries that status.

### 2. Six Kinds of Verification
- **implementation** — does the artifact satisfy the requirements? (read it, run it)
- **claim** — does evidence back the claim? (source-of-record check)
- **artifact** — is the artifact the right shape/content? (schema, diff, repro)
- **regression** — what existing behavior could this break? (targeted tests)
- **security** — threat path checks per `pixz.security.review`
- **deployment** — actual live state, not deploy output

### 2.5 Verification-Depth Ladder (universal principle — `pixz.protocol.verification-depth`)

> **Verification depth must match the claim being made.** A claim is only as strong as the deepest rung its evidence actually reaches.

| Claim | Minimum evidence depth | What satisfies it |
|-------|------------------------|-------------------|
| EXISTS | existence check | `ls` / discovery output shows the artifact |
| PARSES | parser | the artifact is syntactically valid (parse succeeds) |
| SCHEMA-COMPLIANT | schema validation | structural validation against the governing schema |
| CORRECT | behavioral verification | running it produces the specified behavior (fresh output) |
| INTEGRATED | integration test | it works composed with its neighbors, not in isolation |
| RUNTIME-ACTIVE | runtime invocation | the actual runtime discovers and invokes it (not just present) |
| PERSISTENT | repeated/delayed observation | it survives a boundary: re-run, fresh process, next session |
| IMPROVED | baseline comparison | measured against the pre-change baseline, delta shown |

Rules:
- **Never substitute a weaker rung for a stronger claim:** `file exists = valid` ✗ · `command succeeded = correct` ✗ · `test passed = requirement satisfied` ✗ · `agent said success = verified` ✗.
- Escalate only as far as the claim demands — verifying EXISTS at RUNTIME-ACTIVE depth is waste (orchestration budget).
- When the required depth is not achievable in this environment, the claim is downgraded to UNVERIFIED with the gap stated — never silently claimed at a higher rung.
- Layers of this repo map onto the ladder: structural (EXISTS/PARSES/SCHEMA-COMPLIANT) → documentary/behavioral smoke (weak CORRECT) → integration (INTEGRATED/RUNTIME-ACTIVE) → lifecycle suite (PERSISTENT) → successor benchmark (IMPROVED).

### 3. Five Checks (apply proportionally)
- **inspection** — read artifact against requirements
- **failure-mode analysis** — how could this fail? (use change-safety risk tiers)
- **regression awareness** — targeted tests/inspections of affected behavior
- **consistency** — contradiction with conventions, types, schema, docs?
- **change-impact** — blast radius: who/what downstream is affected?

### 4. Evidence, Not Claims
Record `checks_performed` + `evidence` (id, kind, source) + `results` with strength. Do not mark "verified" without an evidence artifact (fresh test output, diff, reproduction steps, primary citation).

### 5. Distinguish Proven vs Trusted vs Unknown
- **Proven:** reproduced + inspected + regression-checked
- **Trusted:** cited primary source but not reproduced — confidence capped at **medium**
- **Unknown:** neither — remains UNKNOWN with recorded residual risk

### 6. Report Residual Risks
Even on pass, list unknowns and risks that remain. Residual risks feed `quality-gate`.

## Inputs / Outputs
- **Inputs:** artifact, requirements, findings/evidence ledger, environment report
- **Outputs:** `verification_report` {checks_performed[], evidence[], results (pass|fail|conditional), residual_risks[], recommended_next_actions[]}

## Failure Conditions
- Verification skipped due to time → fail; do not wave through.
- Claim verified only against a descriptive record when a primary source was available → source-of-record violation; redo.
- Tests pass but inspection contradicts the claim → trust the inspection; flag the test.

## Structured Output
```yaml
checks_performed: ["source-of-record: deploy report vs live endpoint", "regression: auth.spec.ts", "failure-mode: token replay"]
evidence:
  - {id: e1, kind: command_output, source: "curl -s https://api/health", summary: "200 OK, v2.0.1"}
  - {id: e2, kind: test_result, source: "pnpm test auth.spec.ts", summary: "14 passed"}
results: conditional_pass  # pending: load test not run
residual_risks: ["replay under clock-skew not verified"]
recommended_next_actions: ["Run chaos-clock test"]
```

## Relationship
Consumes `pixz.core.epistemic-reasoning` findings; challenged by `pixz.core.epistemic-challenger`; gates `pixz.core.quality-gate`. Mandatory aggregate of `pixz.core.orchestrator` (the evidence floor).

---
