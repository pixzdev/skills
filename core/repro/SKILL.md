---
name: Repro — Minimal Repro Constructor
description: Reduce a failing test, flaky behavior, or bug report to the smallest reliably reproducing case before attempting a fix — classify the failure, bisect/minimize the repro, freeze it, then fix and verify against the frozen repro. Fixes made without a repro are rejected unless the repro is proven impossible. Use when debugging bugs, flaky tests, or regressions.
version: 1.0.0
id: pixz.core.repro
category: core
triggers: [repro, minimal repro, flaky test, bisect, reduce test case]
compatible_runtimes: [claude, openclaw, opencode, hermes, codex, generic]
---

# Repro (Minimal Repro Constructor) — `pixz.core.repro`

> **Specialist HOW skill (core/debug).** For practical multi-step operating methodology, activate the **MAIN skill** `pixz.core.orchestrator`.
>
> A fix without a repro is a guess. This skill exists to make "I fixed it" mean something.

## Purpose

Convert a vague failure into a minimal, reliable reproduction, freeze it, and make the fix provable. The repro is the acceptance test for the fix.

## When to Use / When NOT

| Use | Use instead |
|-----|-------------|
| Bug reports, flaky tests, regressions, "it sometimes fails" | A single assertion already fails deterministically → fix directly, keep the test as the repro |
| You're about to "just tweak" code to try to make it go away | Performance profiling, security review, feature work |

## Methodology (REPRO → CLASSIFY → MINIMIZE → FREEZE → FIX → VERIFY)

1. **REPRO — capture the exact failure.** Record: the command that fails, the exact error/output, the environment (deps, versions, seed), and the *expected* vs *actual*. If it's flaky, run it N times (default 25) and record hit rate. If you cannot reproduce it at all after a real attempt → stop; report `NOT_REPRODUCIBLE` with what you tried. Do not proceed to fix.
2. **CLASSIFY.** Name the failure class: wrong-value / crash / hang / flaky-timing / env-dependent / data-dependent / race / nondeterminism. The class decides the minimization strategy (e.g. flaky-timing → find the timing assumption; data-dependent → reduce the dataset).
3. **MINIMIZE — shrink to the smallest repro.** Remove inputs, code paths, fixtures, and dependencies one at a time, re-running after each removal. Keep only what the failure needs. Target: a test that fails in isolation in under a few seconds, ideally one file / one function. For a race, add the minimal interleaving. For data, bisect the dataset.
4. **FREEZE — pin the repro.** Commit or save the minimal case with a clear name (`repro_<class>_<id>`). Record: exact failing command, expected output, actual output, environment, and the pass/fail predicate. This frozen case is the acceptance test.
5. **FIX — make the frozen repro pass.** Implement the smallest change that makes *the repro* pass. Change the cause, not the symptom; do not weaken the repro's predicate to make it pass.
6. **VERIFY — prove it.** Run the frozen repro (it must pass). Run the full suite (no new failures). If flaky, re-run N times to confirm the hit rate dropped to ~0. Report evidence: before (failing) and after (passing) output.

## Outputs

- The minimal frozen repro (file path + command + pass/fail predicate)
- Failure class + one-line root-cause hypothesis
- The fix (diff) + before/after evidence
- Verdict: `FIXED_AND_VERIFIED` / `NOT_REPRODUCIBLE` (with attempt log) / `REPRODUCED_FIX_PENDING`

## Failure Conditions

- Applying a fix without a repro when a repro was feasible
- "Fixing" by weakening the failing test / predicate
- A repro that still needs the whole suite/environment (not minimal)
- Claiming `FIXED` without re-running the frozen repro to green
- Treating flaky as fixed after a single passing run
- Fabricating a repro or an "after" result that wasn't actually run

## Verification

Repro `MINIMAL` (smallest that fails, isolated) · `FROZEN` (saved, named, with pass/fail predicate) · fix `VERIFIED` (frozen repro green + full suite green, N-run for flaky). The fix is not done until the evidence is attached.

## Main Skill

For orchestration of larger work, use `pixz.core.orchestrator`. For planning the overall debugging effort, `pixz.core.planning`; for post-fix validation, `pixz.core.verification`.
