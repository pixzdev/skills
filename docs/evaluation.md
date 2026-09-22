# Evaluation — PixzFlow 2.4

> A passing structural check must never be presented as behavioral proof. A heuristic smoke must never be presented as a benchmark.

## Layers — Separation Required

### Layer 1 — Structural validation (automated, machine-contract)
- frontmatter valid + **frontmatter ↔ registry consistency** (id/version/triggers/compatible_runtimes — hard error on drift)
- required files (`SKILL.md` + `metadata.yaml` per skill); IDs valid (`pixz.<domain>.<name>`, SemVer)
- registry ↔ metadata ↔ filesystem consistency; no duplicate IDs/paths
- schemas exist and are valid JSON (`skill`, `registry`, `task-state`, `handoff`, `eval`)
- dependency graph acyclic (DFS); limits present
- **overlay contract:** `ZAI.md` exists with required content (4 modes, `AskUserQuestion`, isolation, UNVERIFIED disclosure); `AGENTS.md` exists
- **README contract:** AI Agent Installation Prompt + Super Z / GLM / Z.AI Web Prompt sections present
- **2.0 migration guard:** `schemas/workflow.schema.json` and `profiles/super-z/PROFILE.md` must be gone (superseded)

How: `python scripts/validate.py` + `python scripts/check-cycles.py`. Exit non-zero on fail. Result: PASS/FAIL + evidence list.

### Layer 2 — Documentary validation (heuristic)
- required sections in each SKILL.md (Purpose, Triggers/When, Methodology, Verification, Structured output — per category)
- install commands present where relevant; examples present; metadata complete

How: `python evals/runner.py` — 26 cases, keyword/section presence. **Heuristic, not semantic.** Report as `X/26 heuristic` — no fake precision.

### Layer 3 — Behavioral smoke (heuristic + registry invariants)
What it checks **now (2.5.0)**:
- **registry invariants:** (1) evidence floor — orchestrator mandatory closure contains `pixz.core.verification`; (2) trivial-task budget — orchestrator mandatory closure ≤ 4 nodes (v1.1.0: 10; self-learning is *optional*, so the invariant still holds); (3) mode consistency — low risk never deep/autonomous, high/critical risk never fast
- **36 scenarios:** 15 v1 routing + 8 mechanism + **10 self-learning (E-series)** + **1 MCP routing (2.4)** + **2 motion/repro routing (2.5)** (framer-motion library routing; flaky-test repro-before-fix):
  E1 first-activation · E2 existing-runtime (no duplicate setup) · E3 skill-upgrade · E4 failed-assumption · E5 improvement-loop · E6 anti-overengineering · E7 regression-after-improvement · E8 persistence-reload · E9 validation-depth · E12 high-risk-escalation (E10 contradictory-evidence and E11 trivial-task map to the existing contradictory-reports / trivial-rename scenarios, extended with setup/failure-condition/verification fields). Each E-scenario defines setup · expected behavior · failure condition · verification — keyword presence is never the only evidence.
- false-positive activations per scenario (`should_not_select`), expected activations (`should_select`); trivial-rename additionally asserts `pixz.core.self-learning` does NOT activate (self-training must not add ceremony).

How: `python evals/behavioral/runner.py`. **Heuristic keyword routing + static invariants — not model-graded.**

### Layer 3b — Self-learning lifecycle (deterministic, model-free)
What it checks: the state-machine half of self-learning, in subprocess-isolated tests — first activation (NEW→BASELINED) · duplicate-setup refusal · persisted state reload in a **fresh process** · skill version change (drift→sync→re-adapt) · version-without-content distinction · newly discovered skill · failed adaptation (no-evidence refusal, corrupt-state loud failure) · regression of READY after drift · task-state adaptation pointer.

How: `python evals/lifecycle/run_tests.py`. Deterministic assertions, exit non-zero on fail. **Proves the mechanism at PERSISTENT rung; the behavioral half (a real model actually adapting) remains heuristic/UNVERIFIED — no cross-session model behavior is faked.** Since 2.2.0 the suite also covers doctor (measured baseline), verify-installed (integrity), sitrep, adoption assessment (auto-run at first-run completion), and hooks wiring.

### Layer 4 — Integration (where feasible)
repo → installer → runtime → discovery → invocation: clean-env `npx skills list` before/after, `openclaw skills list/check`, manual `cp -r` + `ls` evidence, resolver dry-runs. Where CI lacks a runtime binary: **manual smoke** with required `ls`/`list` evidence; claim level per runtime VERIFIED vs PARTIALLY VERIFIED (`docs/install/README.md`).

How: `bash scripts/integration-smoke.sh`.

## What this repo's layers prove (and don't)

| Proves | Does not prove |
|--------|----------------|
| registry/metadata/schemas consistent; no cycles; overlay+README contracts hold | that any model behaves differently |
| skills document required sections | that the documented behavior is correct |
| routing smoke + invariants hold for the heuristic router | model-graded activation precision/recall |
| self-learning state machine transitions are correct across fresh processes | that a real model performs the behavioral half |
| install path works where the CLI exists | behavioral effectiveness of PixzFlow on real tasks |

**Model-graded behavioral measurement (capability activation, persistence, continuation, verification quality, evidence quality, recovery, delegation, restraint, efficiency) is the successor benchmark** — see `docs/benchmark/successor-benchmark.md`. Cells A–H report `UNRUN` until executed; this repo never fabricates results.

## Regression obligation (against the v1 GLM benchmark)

Any 2.0 change must not: make trivial tasks slower (token overhead guard) · create unnecessary subagents (anti-delegation cell) · increase context waste · cause recursive invocation · lower native-model initiative · block useful model-native behavior. A strong model must be able to bypass PixzFlow ceremony for trivial work — **PixzFlow is an enabler, not a cage.**

## Scoring & Reporting

- No invented numeric quality score. Per layer: structural PASS/FAIL · documentary `X/26 heuristic` · behavioral `X/36` + invariants · lifecycle `X/14 deterministic` · integration PASS/FAIL per runtime with evidence.
- Every eval result carries: `test_id`, `scenario`, `expected`, `actual`, `pass`, `evidence`, `limitations`.
- Layer 1–2 results must never be presented as Layer 3–4 evidence.

## Artifacts

- `evals/cases/*.json` — Layer 2 (19)
- `evals/behavioral/*.json` + `runner.py` — Layer 3 (34 + invariants)
- `evals/lifecycle/run_tests.py` — Layer 3b (14 deterministic self-learning tests)
- `scripts/integration-smoke.sh` — Layer 4 (includes lifecycle suite + activation probe)
- `docs/benchmark/GLM-benchmark-findings.md` — v1 empirical record
- `docs/benchmark/successor-benchmark.md` — model-graded benchmark design (ablation A–H, task classes, metrics)
- `docs/research/frontier-agent-findings.md` — Phase Zero research with classification labels
