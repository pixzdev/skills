---
name: Change Safety
description: Static pre-mutation policy — classifies every change (reversible / partially / irreversible), checks authority and scope; irreversible actions require confirmation in every mode. Use before mutations. Main operating loop is pixz.core.orchestrator.
version: 2.1.0
id: pixz.core.change-safety
category: core
triggers: [safe change, risk, reversible, scope control, tool selection]
compatible_runtimes: [claude, openclaw, opencode, hermes, codex, generic]
---

# Change Safety — `pixz.core.change-safety`

> **Specialist HOW skill (safety gate).** For practical multi-step operating methodology, activate the **MAIN skill** `pixz.core.orchestrator`. Load `core/orchestrator/references/operating-methodology.md` for high-impact / irreversible work.

## Purpose

Every mutation classified as reversible / partially reversible / irreversible; stronger verification for higher risk.

> **Static policy, not routed capability:** this classification runs before mutations regardless of orchestrator routing or operating mode — the router cannot route itself out of safety.

## When to Use / When NOT

Always before a mutation. There is no "skip in fast mode" for irreversible actions. You may skip *recording* a classification for a pure in-memory thought, not for a write.

## Methodology

1. **What will change?** files, data, external systems, third parties, secrets exposure, prod impact.
2. **Is it authorized?** scope + authority vs requested; confirm if irreversible.
3. **Is it reversible?** classify + mitigation (backup, branch, dry-run). Irreversible actions require confirmation **in every mode, including autonomous** (overlay-invariant — see `ZAI.md`).
4. **Scope control:** distinguish requested/necessary/optional/out-of-scope; no “fix one bug → rewrite architecture” without evidence.
5. **Gate:** reversible + scoped + authorized → proceed; else require confirmation or research. Pre-action verification runs for irreversible/high-impact steps (per `pixz.core.verification` triggers).

### Reversibility cheat sheet

| Tier | Examples | Required before acting |
|------|----------|------------------------|
| Reversible | edit a file on a branch, local config | diff; tests if behavior changes |
| Partially | migrate a table with a down-path, publish a package | backup/snapshot, rollback notes, confirmation if prod |
| Irreversible | `DROP`, prod data delete, send email to users, DNS cutover, `kubectl --force` | explicit confirmation, pre-action verification, runbook |

### Tool selection

Prefer the least-powerful tool that works: read before write, dry-run before apply, scoped path before repo-wide. Do not run destructive flags to "save a step".

## Outputs

`safety_assessment` {changes[], risk, reversibility, authority_verdict, proceed: bool}

## Failure Conditions

- Irreversible action without confirmation → blocked.
- Scope expanded from "fix bug" to "rewrite" without evidence → rollback the plan.
- Dry-run skipped on prod apply → process failure.

## Example

> `kubectl apply -f deploy.yaml` on prod. Classify: partially reversible (rollout undo exists if history kept). Required: `kubectl diff`, `--dry-run=server`, rollback revision noted, confirmation. Proceed only after those.

## Main Skill

Safety is a gate inside the operating loop. Sequencing the work around the gate is `pixz.core.orchestrator`.
