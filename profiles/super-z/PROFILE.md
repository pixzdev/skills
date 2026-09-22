# Profile — Super Z / GLM / Z.AI Web

> **Class:** PROFILE (runtime-specific POLICY overlay). **Status:** SPECIFIED (mission spec, 2026-09-22). **Behavioral effect:** UNVERIFIED — no behavioral evaluation exists for this profile yet. Do not claim otherwise.

## Applies to (identification)

This profile applies when the agent identifies — from its own runtime self-report, model identity, or environment — as one of:

- **Super Z**
- **GLM** (Z.AI / Zhipu model family)
- **Z.AI Web** (web-based Z.AI agent surface)

If the agent cannot identify as one of these, this profile **does not apply** — use the universal skills and routing as-is. Identification is based on observable identity signals only; do not speculate about which model is running.

## Does not change universal semantics

This profile **does not change** universal skill semantics: the methodology in any `SKILL.md`, `registry.json`, the dependency model, `scripts/resolve.py` behavior, change-safety tiers, the 4 verification layers, and honest-reporting rules all remain exactly as specified. On any conflict, the skill and the repository policies win. This profile only parameterizes:

1. the orchestrator's **operating depth** (see axis below), and
2. the runtime's **compute and user-interaction policy**.

## Mandatory mode selection (before substantive work)

Before beginning substantive work, the agent **MUST** invoke its available **`AskUserQuestion`** capability (or the runtime's equivalent structured question tool) and ask the user to select one operating mode:

- **FAST** — minimum orchestration overhead
- **BALANCED** — adaptive orchestration, minimum sufficient delegation
- **DEEP** — substantially more skills, specialist subagents, research, verification, adversarial review
- **AUTONOMOUS** — Deep-level rigor with minimal user interruptions

**Default:** if the user does not select a mode (no answer, declined, or the tool is unavailable), the agent **defaults to BALANCED** and states the default it is using.

**Degradation:** if no `AskUserQuestion`-equivalent capability exists in the runtime, the agent states that fact in one line, proceeds at BALANCED, and does not block the task.

## Mode semantics

Depth axis (from `docs/architecture.md` / `docs/architecture/routing.md`): `MINIMAL → STRUCTURED → MULTI-SKILL → MULTI-AGENT → ADVERSARIAL → DEEP VERIFICATION`. The profile selects a **target depth** for the orchestrator; the orchestrator still classifies each task and may use less than the target when a task is trivial — the target is an upper tendency, never a minimum ceremony.

| Mode | Target depth | Observable behavior |
|------|--------------|---------------------|
| FAST | MINIMAL–STRUCTURED | Minimum sufficient capability per task; usually `UNDERSTAND→EXECUTE→VERIFY`; one skill where justified; no subagents unless the user asks; skip challenger/quality-gate ceremony for low-risk work. |
| BALANCED | STRUCTURED–MULTI-SKILL | Complexity-aware routing per `docs/architecture/routing.md`; minimum sufficient delegation; challenger only when risk×uncertainty×impact is high; verification always evidence-based. |
| DEEP | MULTI-AGENT–ADVERSARIAL–DEEP VERIFICATION | Substantially more: discover relevant skills before implementation; invoke multiple complementary skills when justified; use specialist subagents with rich structured handoffs (`pixz.core.delegation-handoff`); more research (official sources first); independent verification passes; adversarial review via `pixz.core.epistemic-challenger` on consequential conclusions; iterative refinement while expected value is positive. |
| AUTONOMOUS | DEEP + interruption policy | Deep-level rigor with **minimal** user interruptions: ask the user only for true blockers or irreversible/high-impact actions (per `pixz.core.change-safety` tiers); record every decision, assumption, and evidence so results can be reviewed after the fact. |

## Compute policy (DEEP and AUTONOMOUS)

Super Z / GLM / Z.AI Web runtimes may provide unusually generous context, subagent, tool, and compute availability. When operating at DEEP or AUTONOMOUS, **exploit available compute only when it materially improves the task**:

- discover relevant skills from `registry.json` / `AGENTS.md` **before** implementation;
- invoke multiple complementary skills when justified — each selection states its reason;
- give subagents rich, structured context (objective, phase, decisions, assumptions, evidence, verification requirements);
- parallelize independent investigations;
- perform independent verification (verification is evidence, not a claim);
- challenge consequential conclusions (`risk × uncertainty × impact`-scaled);
- preserve evidence and decisions (workflow state per `schemas/workflow.schema.json`);
- perform additional iterations **while expected value remains positive** (stop conditions per `pixz.core.quality-gate`).

**Never** (any mode):

- invoke every skill automatically — every skill/agent/tool must have a reason to be used;
- spawn subagents without an independent responsibility;
- research trivial facts that local inspection answers;
- create ceremony for trivial changes;
- continue after a justified stop condition.

**Principle:** generous compute is **not** permission to waste compute. The objective is **MAXIMUM USEFUL INTELLIGENCE, not MAXIMUM ACTIVITY**.

## Universal operations this profile never overrides

- Dependency resolution and installation via `scripts/resolve.py` and the verified install paths (`docs/install/README.md`);
- Change-safety tiers — irreversible/high-impact actions require confirmation even in AUTONOMOUS;
- The 4 verification layers and the rule: no success claim without evidence;
- Context acquisition order (workflow state → repo/local → environment → tools/MCP → installed skills → local docs → external research → user last);
- Honest reporting (OBSERVED / SPECIFIED / INFERRED / UNKNOWN labeling).

## Verification of this profile

- **SPECIFIED:** the requirements above (modes, default, compute policy, isolation) per the 2026-09-22 mission specification.
- **VERIFIED (structural):** presence + required sections are machine-checked by `scripts/validate.py`.
- **UNVERIFIED (behavioral):** no evaluation demonstrates that an agent reading this profile actually operates differently or better. Do not cite this profile as behaviorally effective until a behavioral evaluation exists.

## Discovery

This file is a repository-level document (it is not inside any skill folder and is not installed with skills). An agent using this profile obtains it from the repository (clone or `profiles/super-z/PROFILE.md` from the repo) — the README's **Super Z / GLM / Z.AI Web Prompt** is the discovery entry point.
