---
name: Commit Hygiene
description: Pre-commit and pre-push hygiene gate — detect and block secrets, credentials, and tokens about to be committed, review the manifest/lockfile diff for unintended dependency changes, verify the commit message matches the actual diff, and keep the working tree clean of stray generated/credential artifacts. Use right before committing or pushing.
version: 1.0.0
id: pixz.security.commit-hygiene
category: security
triggers: [pre-commit, secret scan, commit hygiene, dependency review, supply chain]
compatible_runtimes: [claude, openclaw, opencode, hermes, codex, generic]
---

# Commit Hygiene — `pixz.security.commit-hygiene`

> **Specialist HOW skill (security).** For practical multi-step operating methodology, activate the **MAIN skill** `pixz.core.orchestrator`.
>
> The commit is a public, permanent artifact. This gate stops secrets and surprise dependencies from becoming permanent.

## Purpose

Run a fast, high-signal hygiene pass immediately before a commit/push: no secrets, no unintended dependency drift, message matches diff, no stray artifacts. It is a tripwire, not a substitute for the full `pixz.security.review`.

## When to Use / When NOT

| Use | Use instead |
|-----|-------------|
| About to commit or push, especially with new deps or config | Deep threat-model / dependency CVE audit → `pixz.security.review` |
| Adding lockfiles, `.env.example`, config, or vendored code | Broad code review for logic bugs |

## Methodology

1. **STAGE SNAPSHOT.** Determine exactly what will be committed: `git diff --cached --name-status` (or the changed set if not staged). Work from the *actual* set, not memory.
2. **SECRET SCAN (block on hit).** Scan the staged diff for: API keys / tokens (long high-entropy strings, `sk-`, `AKIA`, `ghp_`, `xox`, private-key headers `BEGIN ... PRIVATE KEY`), connection strings with credentials, hardcoded passwords, JWTs, and `.env`-style key=value with sensitive-looking keys. Real secrets → **BLOCK**: remove, rotate if it was ever real, and add the path to ignore. A placeholder (`your-key-here`, `CHANGEME`, obviously-fake) is a pass but note it.
3. **MANIFEST / LOCKFILE DIFF (review on hit).** If a manifest (`package.json`, `pyproject.toml`, `requirements.txt`, `Cargo.toml`, `go.mod`, lockfiles) changed: list added/removed/changed dependencies with versions. Flag: (a) new deps not mentioned in the change intent, (b) lockfile changes that don't match the manifest, (c) broad version ranges or `*`, (d) a new `postinstall`/`preinstall` script (supply-chain surface). Report each with a one-line why; do not silently approve.
4. **ARTIFACT / STRAY CHECK.** Flag files that should not be in VCS and now are: build output, `node_modules`, `.env` (real), logs, `.DS_Store`, editor/IDE state, large binaries, `.gitignore`-covered paths that slipped in. Recommend the ignore rule; never force-commit them.
5. **MESSAGE ↔ DIFF CONSISTENCY.** Read the commit message; check it describes the dominant change. A message that contradicts the diff (e.g. "fix bug" for a feature, "chore" for a dependency bump) → flag and suggest an accurate message.
6. **VERDICT + NEXT.** Produce a pass/fail gate result. **Block** on any real secret. **Warn** on dependency drift, stray artifacts, or message mismatch (commit allowed only after the user acknowledges). Pass when clean.

## Outputs

- Gate result: `PASS` / `WARN` (itemized) / `BLOCK` (secrets)
- Secret findings (location + what to do: remove, rotate, ignore) — never echo the secret value itself
- Dependency diff table (dep, change, version, why flagged)
- Stray-artifact list + suggested `.gitignore` lines
- Commit-message verdict + suggested correction

## Failure Conditions

- Committing a real secret (block-level)
- Letting an unintended dependency/lockfile change through unreported
- Reporting a secret's full value in the report (re-leaks it)
- Passing a commit whose message misrepresents the diff without flagging it
- Flagging placeholders (`CHANGEME`) as real secrets and blocking forever
- Running on "what I think I changed" instead of the actual staged set

## Verification

Scan ran on the *actual* staged diff (command shown) · every flag has a file path + reason · block conditions are binary (secret present or not) · the gate result is reproducible by re-running the same commands.

## Main Skill

For orchestration of larger work, use `pixz.core.orchestrator`. For a full dependency/CVE security review, `pixz.security.review`; for safe, reviewable change structure, `pixz.core.change-safety`.
