---
name: Self-Learning
description: Post-install activation and self-learning — detect the installed PixzFlow workflow, baseline the runtime, adapt behavior, verify the adaptation, persist verified lessons, and convert recurring failures into the smallest reusable mechanism that survives challenge.
version: 2.1.0
id: pixz.core.self-learning
category: core
triggers: [self-train, self-learn, first activation, post-install, skill version changed, adaptation baseline, improve workflow, learn from failure]
compatible_runtimes: [claude, openclaw, opencode, hermes, codex, generic]
---

# Self-Learning — `pixz.core.self-learning`

> Installation makes capabilities **available**. Activation makes the agent **able to invoke them**. Adaptation **changes working behavior**. Learning extracts **reusable lessons**. Improvement converts verified lessons into **mechanisms, tests, or durable procedures**. These are five different states — never conflate them, and never claim one while only having done the previous.

## Purpose

Closes the gap measured by the GLM benchmark (availability ≠ invocation) and the session-boundary problem (a self-training prompt pasted once does not survive restarts). After PixzFlow is installed into a runtime, this skill lets the agent **discover the workflow itself, adapt its behavior to it once, persist the adaptation, and keep improving** — without the user re-pasting anything each session. It is behavioral/runtime adaptation: **no model weights are modified**; learning lives in compact inspectable files.

## Triggers

- Post-install: PixzFlow files detected but no `.pixz/adaptation-state.json` (first activation).
- Session start probe finds adaptation state `stale` or inventory drift (skill version changed / skill added or removed).
- A recurring failure class asks to be converted into a durable fix (learn from failure).
- Explicit: self-train / self-learn / improve workflow.

**Do NOT use when:** the task is trivial (rename/typo) and adaptation state is `ready` with no drift — a single probe (`scripts/activation.py status`, or `ls .pixz/adaptation-state.json`) suffices, then work. Self-learning must never add ceremony to tasks that predate it.

## Inputs / Outputs

- **Inputs:** runtime signals, installed capability set (`registry.json` / install locations), existing state files (`.pixz/adaptation-state.json`, `.pixz/task-state.json`), observed failures.
- **Outputs:** adaptation baseline, adaptation record (status + evidence), delta report on drift, learning ledger entries (lessons, improvements), verification receipts.

## Methodology A — Post-install activation lifecycle

```
DETECT → INVENTORY → BASELINE → ADAPT → VERIFY → PERSIST → READY
```

1. **DETECT** — is PixzFlow present and am I adapted? Run `python3 scripts/activation.py status` (exit 0 = ready, 10 = attention: new/stale). If state exists, is `ready`, and there is **no drift** → stop here and work. Do not duplicate setup (mission E2).
2. **INVENTORY** — record what is actually installed (not what the source contains): capability ids, versions, install paths, verified-by-discovery flags. `scripts/activation.py init` writes the machine-checkable part; the agent confirms discovery evidence per the install protocol.
3. **BASELINE** — record the compact runtime baseline (`schemas/adaptation-state.schema.json#dimensions`): runtime + model (self-report only), instruction sources, tool availability, state/verification/delegation/research capability, session characteristics. **Observe, don't assume**; anything unobserved stays `unknown` — unsupported capabilities are never invented. Never record hidden chain-of-thought.
4. **ADAPT** — change working behavior, concretely: recognize available capabilities and their activation conditions; adopt the entry protocol (`AGENTS.md`), evidence rules, source-of-record rule, verification triggers, delegation constraints, mode selection, anti-overengineering rules, and state persistence. Write the resulting operating understanding into state (summaries, not skill text).
5. **VERIFY** — prove adaptation at the right depth (verification-depth ladder): adaptation is a **RUNTIME-ACTIVE** claim, so demonstrate invocation, not existence — e.g. run the validation layers, execute one real capability invocation, show the probe now reports the new status. `file exists = valid` is rejected here.
6. **PERSIST** — `scripts/activation.py mark-adapted --evidence "<what was observed>"` (refuses without evidence). The state file is what makes the next session skip setup.
7. **READY** — subsequent sessions: probe → ready → work. Second activation is a **check**, not a re-run.

## Methodology B — Drift & skill-version adaptation

```
OLD VERSION → detect delta → inspect changes → identify behavioral implications
            → update activation knowledge → verify → persist
```

- `scripts/activation.py status` reports per-skill deltas (added / removed / version-changed / content-changed, via digests).
- **Never assume "version changed = behavior changed"** — inspect the actual diff (SKILL.md frontmatter/triggers/methodology) and identify behavioral implications (new trigger? changed verification requirement? new dependency?).
- Prefer **progressive re-activation of the delta** over reloading everything: only capabilities whose behavior-relevant content changed get re-read and re-verified.
- Persist with `scripts/activation.py sync` (updates digests, records history) and a fresh `mark-adapted --evidence` if behavior changed.

## Methodology C — Self-improvement loop (during normal work)

```
OBSERVE → IDENTIFY failure/inefficiency → ROOT-CAUSE → GENERALIZE → CHALLENGE
        → PROPOSE → SELECT → IMPLEMENT → VERIFY → REGRESSION CHECK → PERSIST
```

- **Distinguish the artifacts:** a **LESSON** ("what not to repeat") is not a **MECHANISM** (a change that prevents recurrence); a mechanism is not a **TEST**; a test is not a **VERIFIED IMPROVEMENT**; and a verified improvement is not **EMPIRICALLY IMPROVED** (which needs baseline comparison). A successful task does **not** automatically mean the process improved.
- **Root-cause before generalizing** — use the failure-recovery ladder (`core/replanning`); a lesson from one incident may be overfitting.
- **CHALLENGE every persistent improvement** (six challenges, via `pixz.core.epistemic-challenger` at calibrated intensity): failure (how could this make the agent worse?) · regression (what existing behavior could break?) · overfitting (is this one incident?) · complexity (does this add ceremony to trivial work?) · confirmation (what evidence would disprove it?) · adversarial (can hostile/contradictory input defeat it?).
- **Anti-proliferation gate (hard):** do not answer failure with a new skill / agent / protocol / schema / instruction file / dependency unless all of these hold: existing mechanisms cannot express it · the failure class is recurring (≥2 observed) · it is reusable beyond the incident · benefit justifies permanent context cost · it is testable. Prefer, in order: policy/heuristic → extend an existing mechanism → new test → (last) new abstraction. Expected value must beat: token cost, latency, tool calls, context consumption, persistent complexity.
- **Adaptive complexity:** the improvement process itself scales with risk. Low risk: record a lesson in state, move on. High/critical or irreversible: full loop with regression checks and challenge. A mechanism that improves one edge case while making every trivial task worse is **rejected or redesigned**.
- Persist only verified entries into `learning[]` (status ladder: `proposed → challenged → implemented → verified`; `regressed`/`rejected` are marked with reason, never deleted).

## Session-boundary behavior

The lifecycle must survive: context compaction · session restart · runtime restart · subagent handoff · model/runtime change — because **all durable state is in files** (`.pixz/adaptation-state.json` + `.pixz/task-state.json#adaptation`), and the trigger to check them lives in `AGENTS.md`, which participating runtimes read at session start. Handoff: a subagent receives the adaptation status in its context packet; it never re-runs setup. What cannot be tested in this repo is marked **UNVERIFIED**, never faked.

## Failure Conditions

- Claiming "I have learned PixzFlow" without adaptation evidence → fake learning; the probe still reports `baselined`/`stale`.
- Re-running setup when state is `ready` and no drift → duplicate-setup failure (waste + state churn).
- Assuming version change implies behavior change without inspecting the delta.
- Persisting an unverified lesson as a mechanism, or any entry containing transcripts/chain-of-thought.
- Creating a new skill/schema/agent for a one-off failure (proliferation) → reject at the gate.
- Letting self-learning add ceremony to trivial tasks → budget violation.

## Verification

- Machine level (VERIFIED by `evals/lifecycle/run_tests.py`): init/second-init refusal, state reload, drift detection, sync, mark-adapted evidence requirement, staleness regression.
- Probe level: `python3 scripts/activation.py status` exit codes (0 ready · 10 new/stale · 1 error).
- Behavioral level (heuristic, not model-graded): `evals/behavioral/` E-series scenarios (first/second activation, upgrade, failed assumption, self-improvement, anti-overengineering, regression, persistence, validation depth, trivial-task budget, high-risk escalation).
- Depth rule: READY is a PERSISTENT claim (repeated/delayed observation) — one probe in one session is not enough; the lifecycle test re-runs the probe in a fresh process.

## Structured Output

```yaml
activation: {status: new|baselined|ready|stale, evidence, probe_exit_code}
baseline: {runtime, dimensions, unknowns}
delta: [{id, change: added|removed|version|content, implication}]
lessons: [{id, lesson, status: candidate|stable}]
improvements: [{id, kind, status, verification, regression_check}]
```

---
