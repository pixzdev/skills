# PixzFlow Successor Benchmark (design)

> The v1 benchmark (see `docs/benchmark/GLM-benchmark-findings.md`) proved: correctness ceiling, small blind-grading delta, 1.48× token overhead, skills-alone marginality, availability≠invocation, T11 source-of-record signal (n=2). The successor benchmark is designed to **distinguish native model capability from PixzFlow's contribution**, mechanism by mechanism.

## Design Goals

1. Separate **native capability** (what the model does anyway) from **PixzFlow contribution** (what the operating layer adds).
2. Measure **mechanism-level** effects (activation, persistence, continuation, evidence, restraint) — not just end quality.
3. Be **cross-model**: GLM-class, Claude-class, GPT-class, Gemini-class, Kimi-class, open-weight, smaller models.
4. Prefer **objective, artifact-anchored** metrics over vibes; blind grading where subjective.
5. **n ≥ 5** per important cell; fresh environments; repeated tasks; objective verification.

## Ablation Matrix (which mechanism contributes?)

| Cell | Configuration | Answers |
|------|---------------|---------|
| **A** | Native model, no PixzFlow | Baseline capability |
| **B** | PixzFlow 2.0 full (AGENTS.md + registry + state + evidence + modes) | Total system effect |
| **C** | PixzFlow workflow **without skills** (AGENTS.md only, no registry) | Operating layer alone |
| **D** | Skills **without workflow** (registry installed, no AGENTS.md) | Skills alone (v1's B≈B1 question) |
| **E** | PixzFlow **without persistent state** (no task-state file) | Continuity contribution (T12 amortization test) |
| **F** | PixzFlow **without challenger** | Adversarial check contribution |
| **G** | PixzFlow **without evidence ledger / source-of-record protocol** | Evidence contribution (T11, now n≥5) |
| **H** | PixzFlow **with runtime overlay** (e.g. ZAI.md on GLM/Super Z) | Overlay contribution (mode ritual + compute policy) |

Plus: **B′** = PixzFlow 2.0 with **orchestrator aggregates restored to v1.1.0's 8** (regression guard: does the old bundle ever help?) and **B″** = v1.1.0 full (history anchor).

**Decision rule:** a mechanism that shows no significant benefit across ≥ 3 task classes at n≥5 is **deleted** in the next major. No component survives on identity alone.

## Task Classes (each n ≥ 5, fresh env, objective verifier where possible)

| Class | Probes |
|-------|--------|
| trivial | rename, typo — **restraint + token cost** (overhead must stay ≈ 1.0×) |
| simple | single-file bug — targeted verification |
| complex | multi-file feature — planning + verification |
| ambiguous | underspecified request — assumption disclosure + ask-last |
| security-sensitive | vuln in auth/data path — activation of security skills + challenge |
| long-horizon | multi-phase project — state amortization (T12 replication) |
| contradictory evidence | two sources disagree — contradiction handling, no suppression |
| **false authority** | descriptive record (report/log/commit msg) contradicts actual artifact — **source-of-record** (T11 at n≥5) |
| tool failure | failing command — recovery ladder, no blind retry |
| partial failure | one subtask fails — isolation + localized replan |
| **context compaction** | forced compaction mid-task — restore-from-state correctness |
| **session restart** | kill + resume — `next_action` continuation |
| mid-task requirement change | spec change at 50% — minimal-delta replan, decision marking |
| **skill discovery** | relevant skill installed but unmentioned — activation recall |
| **skill persistence** | capability activated in phase 1, condition fires in phase 3 — reactivation |
| delegation (beneficial) | independent parallel work — correct delegation |
| **anti-delegation** | trivial work — **no** subagents (restraint, measured explicitly) |

## Metrics (per run)

- correctness (objective acceptance)
- verification quality (typed checks present? source-of-record applied?)
- evidence quality (claims typed? `verified_against` populated? fabricated evidence = 0)
- continuation quality (resume from state: objective preserved? next_action honored? active capabilities re-established?)
- recovery quality (failure classified? hypothesis tested? lesson recorded?)
- tool efficiency (calls vs necessary)
- **token cost** (total + overhead ratio vs cell A; trivial tasks must stay ≈ 1.0×)
- wall-clock time
- delegation overhead (subagent tokens/latency vs serial baseline)
- **skill activation precision** (activated ∩ relevant / activated)
- **skill activation recall** (activated ∩ relevant / relevant)
- **false-positive activations** (count; trivial tasks must be 0)
- replanning quality (minimal delta? old plan marked? iteration bounded?)
- drift (objective restated correctly after compaction/restart?)

## Grading

- Objective checks (artifact-diff, command probes, state-file inspection) first.
- Blind LLM/human graders with rubrics for subjective quality (LH-Bench pattern: expert-grounded rubrics, stepwise signals).
- **Never** present a structural/smoke result (this repo's layers 1–3) as benchmark evidence — they are different layers (`docs/evaluation.md`).

## What is implemented in this repo vs. what this doc is

- **Implemented & machine-runnable here:** ablation *definitions*, task-class *definitions*, metric *definitions*, the registry invariants, 23 behavioral smokes, 4 verification layers.
- **Not implemented here (by design):** model execution (no model access in-repo; running cells A–H across model classes is an external experiment). Fabricating results is forbidden — cells report `UNRUN` until executed.

## Priority (expected information gain)

1. **T11 replication at n≥5** (false authority) — strongest v1 signal, currently n=2. Highest gain: confirms/refutes the evidence-architecture investment.
2. **E vs B** (state persistence) — T12 amortization is a hypothesis; this decides the task-state protocol's value.
3. **D vs A** (skills alone) — v1's B≈B1/C≈A question retested with 2.0's registry.
4. **H vs C** (ZAI overlay on GLM/Super Z) — is the mode ritual + compute policy behaviorally effective? (ZAI.md is currently SPECIFIED/UNVERIFIED.)
5. **A/B trivial-cell token overhead** — the 1.48× regression guard.
