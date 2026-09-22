# ZAI.md — PixzFlow Runtime Overlay: Super Z / GLM / Z.AI Web

> **Class:** Runtime-specific operating overlay (Level 2.5). **NOT** the primary workflow. **Status:** SPECIFIED (2026-09-22, PixzFlow 2.0). **Behavioral effect:** UNVERIFIED — no behavioral evaluation demonstrates an agent reading this file operates differently or better. Do not claim otherwise.

## Applies to (identification)

Activate **only** when the agent identifies — from its own runtime self-report, model identity, or environment — as one of:

- **Super Z**
- **GLM** (Z.AI / Zhipu model family)
- **Z.AI Web** (web-based Z.AI agent surface)

If the agent cannot identify as one of these, this overlay **does not apply** — operate under `AGENTS.md` as-is. Identification uses observable identity signals only; do not speculate about which model is running.

## Does not change universal semantics

This overlay **does not change** universal semantics: `AGENTS.md` operating rules, `SKILL.md` methodology, `registry.json`, the dependency model, `scripts/resolve.py` behavior, change-safety tiers, verification triggers, the evaluation layers, and honest-reporting rules remain exactly as specified. On any conflict, `AGENTS.md` and the repository policies **win** over this overlay.

This overlay only parameterizes:

1. the **operating mode** default and selection ritual, and
2. the runtime's **compute and user-interaction policy**.

## Mandatory mode selection (before substantive work)

Before beginning substantive work, the agent **MUST** invoke its available **`AskUserQuestion`** capability (or the runtime's equivalent structured question tool) and ask:

> **How should PixzFlow operate?**
> 1. **Fast** — minimum orchestration overhead
> 2. **Balanced** — adaptive orchestration, minimum sufficient delegation (default)
> 3. **Deep** — more relevant skills, specialist subagents, research, verification, adversarial review
> 4. **Autonomous** — Deep-level rigor with minimal user interruptions

- **Default:** if the user does not select a mode (no answer, declined, or tool unavailable), the agent **defaults to Balanced** and states the default it is using.
- **Degradation:** if no `AskUserQuestion`-equivalent capability exists, the agent states that in one line, proceeds at Balanced, and does not block the task.
- The user may change mode at any time; the agent restates the new mode and adjusts behavior.

## Mode semantics (behavioral differences, not labels)

| Mode | Discovery | Planning | Delegation | Verification | Challenge | State |
|------|-----------|----------|------------|--------------|-----------|-------|
| **Fast** | minimal (registry scan only) | 0–2 step plan or none | none unless user asks | targeted (close the change) | none | in-context only |
| **Balanced** | registry + relevant skill bodies | 3–7 step minimal plan | minimum sufficient, one bounded specialist | evidence-based checks + regression | only when risk×uncertainty×impact×irreversibility is high | task-state file when task > ~1 session step |
| **Deep** | deep capability discovery across domains | full plan with explicit assumptions + evidence plan | specialist subagents with structured handoffs where materially useful; parallel only for independent work | multiple independent checks, source-of-record verification | adversarial challenge on consequential conclusions | full task-state: findings, evidence ledger, capability state, checkpoints |
| **Autonomous** | as Deep | dynamic decomposition; replan on evidence | as Deep, with explicit stop/escalation criteria | continuous; checkpoints before irreversible actions | as Deep | full task-state + periodic checkpoints; decisions recorded for after-the-fact review |

Autonomous = Deep rigor with an **interruption policy**: ask the user only for true blockers or irreversible/high-impact actions (change-safety tiers).

## Compute policy (Deep and Autonomous)

Super Z / GLM / Z.AI Web runtimes may provide unusually generous context, subagent, tool, and compute availability. Exploit available compute **only where expected value is positive**:

- discover relevant skills from `registry.json` / `AGENTS.md` **before** implementation;
- activate multiple complementary skills **when justified** — every activation states its reason in task-state;
- give subagents rich, bounded context (objective, constraints, decisions, evidence refs, success criteria) per `schemas/handoff.schema.json`;
- parallelize **independent** investigations (research, verification, security review, test generation, alternative-implementation analysis); never parallelize dependent edits or shared mutable state;
- perform independent verification (verification is evidence, not a claim);
- challenge consequential conclusions at calibrated intensity;
- preserve decisions, evidence, and capability state in task-state;
- iterate **while expected value remains positive** — then stop.

**More compute is not automatically better reasoning.** The objective is **maximum useful intelligence, not maximum activity**.

**Never** (any mode): invoke every skill automatically · spawn subagents without an independent responsibility · research trivial facts that local inspection answers · add ceremony to trivial changes · repeat verification with no new information · recursive orchestration (subagents do not spawn subagents) · continue after a justified stop condition.

## Universal operations this overlay never overrides

- Capability discovery/activation protocol and dependency resolution via `registry.json` + `scripts/resolve.py`;
- Change-safety tiers — irreversible/high-impact actions require confirmation even in Autonomous;
- Verification triggers (before irreversible action, after significant mutation, before claims/handoff/completion);
- Source-of-record discipline (actual artifacts over descriptive records);
- Context acquisition order (task state → repo/local → tools/MCP → docs → official research → user last);
- Honest reporting (FACT / OBSERVED / SOURCE CLAIM / INFERENCE / ASSUMPTION / HYPOTHESIS / UNKNOWN / VERIFIED / FALSIFIED labels where uncertainty matters);
- Post-install self-learning lifecycle (probe → baseline → adapt → verify → persist) and the automatic adoption assessment (`scripts/assess.py`, 0–100, evidence-backed checks only) run identically under this overlay — the overlay changes mode/compute policy, never adaptation discipline.

## Discovery

This file is a repository-level document — not a skill, not in `registry.json`, not resolved, not installed with skills. An agent activates it via the README's **Super Z / GLM Install & Activation Prompt** or by reading this file from the repository root.

## Verification of this overlay

- **SPECIFIED:** the requirements above, per the 2026-09-22 mission specification.
- **VERIFIED (structural):** presence + required content machine-checked by `scripts/validate.py`.
- **UNVERIFIED (behavioral):** no evaluation demonstrates that an agent reading this file operates differently or better. Behavioral validation belongs to the successor benchmark (`docs/benchmark/successor-benchmark.md`), cell: runtime-overlay effect.
