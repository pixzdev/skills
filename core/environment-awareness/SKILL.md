---
name: Environment Awareness
description: Inspects actual OS, runtime, framework, package manager, git, filesystem and tooling during ORIENT — before any environment-dependent decision.
version: 2.1.0
id: pixz.core.environment-awareness
category: core
triggers: [environment, stack detection, runtime, package manager, git state]
compatible_runtimes: [claude, openclaw, opencode, hermes, codex, generic]
---

# Environment Awareness — `pixz.core.environment-awareness`

> **Specialist HOW skill (environment).** For practical multi-step operating methodology, activate the **MAIN skill** `pixz.core.orchestrator`. Load `core/orchestrator/references/operating-methodology.md` when environment risk is part of a larger delivery.
>
> A prevention mechanism against hallucinated assumptions.

## Purpose
Before environment-dependent decisions, inspect the actual environment when tools permit. Never assume `npm` when repo uses `pnpm`, nor `Next.js` when repo is `Vite`.

## Triggers
- Any task touching build, run, install, test, deploy, scaffolding, or stack-specific code generation
- ORIENT step, whenever the task is environment-dependent (see `AGENTS.md#entry-protocol`)

## Methodology

### Signals to Inspect (when tools permit)
```
OS / arch / Node/Bun/Deno version
Runtime (claude/codex/generic), shell, env vars (non-secret)
Language / framework (package.json, pyproject, go.mod)
Package manager (lockfile: pnpm-lock.yaml vs package-lock.json vs yarn.lock vs bun.lockb)
Repository (git status, remote, branch, dirty)
Working directory / filesystem (monorepo layout, apps/packages)
Dependencies (installed commands, MCP servers, versions)
CI/CD / deployment target / hardware / resource constraints / permissions
```

### Procedure
1. **Probe locally first:** `bash` checks (`uname`, `node -v`, `ls -la`, `cat package.json`, `git status`, `ls pnpm-lock.yaml` etc). Do not assume.
2. **Record evidence:** for each signal, store observed value + source command.
3. **Derive implications:** e.g., `pnpm` → use `pnpm add`, not `npm install`; `AGENTS.override.md` present → it overrides.
4. **Fail safe:** if inspection not permitted (no tool access), explicitly mark assumption as UNVERIFIED with low confidence and downstream risk.

## Inputs / Outputs
- **Inputs:** task scope hint, workflow state
- **Outputs:** `environment_report` {os, runtime, language, framework, package_manager, repository, filesystem, dependencies, permissions, evidence[]}

## Failure Conditions
- Tool to inspect unavailable → emit UNKNOWN rather than hallucinate.
- Contradictory signals (e.g., both `package-lock.json` and `pnpm-lock.yaml` present) → flag staleness, prefer lockfile with newer mtime and explicit config.

## Verification
- Report is reproducible: re-running probes yields same signals.
- Cross-check: does inferred framework match config files and dependencies?
- Peer review: would another agent with same report make the same tool choices?

## Structured Output
```yaml
environment_report:
  os: {value, evidence}
  package_manager: {value: pnpm, evidence: "pnpm-lock.yaml mtime ..."}
  framework: {value: next.js, evidence: "next.config.js + package.json deps"}
  git: {branch, remote, dirty, evidence}
  constraints: [ ... ]
assumptions: [{claim, basis, fragility}]
unknowns: [ ... ]
```

## Example
> Prompt: “Install deps and run tests”
> Inspect: `ls pnpm-lock.yaml` exists, `packageManager: pnpm@9` in package.json, `git status` clean on main.
> Action: `pnpm install && pnpm test` — not `npm install`.

## Runtime Notes
Tool availability differs: Claude Code has bash/MCP, OpenClaw has node allowlist, some hermes runners are sandboxed. Methodology same; evidence collection adapts.
