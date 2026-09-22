# AGENTS.md — PixzFlow Operating Contract

> **Canonical for agents.** This file is the PixzFlow operating layer (Level 2): how to work, what to verify, how to stay persistent. Machine registry: `registry.json` (source of truth). LLM map: `llms.txt`. Human overview: `README.md`. Runtime overlay for Super Z / GLM / Z.AI Web: `ZAI.md`.

## What PixzFlow Is

A persistent, adaptive, **model-agnostic** operating layer for capable AI agents. Division of labor:

```
MODEL provides intelligence · RUNTIME provides execution · PIXZFLOW provides operating discipline
SKILLS provide specialized capability · STATE provides continuity · EVIDENCE provides epistemic grounding
VERIFICATION provides reality checks · AGENTS provide specialized parallel capability · TOOLS provide access to the world
```

Layers (conceptual, not infrastructure): **L0** model-native (reasoning, context window, native tools/memory — cannot be replaced) → **L1** runtime (tools, MCP, sandbox, subagents) → **L2** PixzFlow (this file, workflow, state, evidence, policies) → **L2.5** runtime overlays (`ZAI.md`) → **L3** capabilities (`registry.json` skills) → **L4** dynamic execution (agents, subagents, MCP, external systems) → **L5** task state/evidence (artifacts, tests, verification, handoffs).

PixzFlow **does not** teach basic engineering to frontier models, does not force one rigid checklist on every model, and does not replace native capability. It makes strong behavior more **consistent, persistent, inspectable, transferable, and recoverable** — and it keeps trivial work cheap.

## Entry Protocol (every task)

```
ORIENT   → state exists? read task-state first (continuation). Environment relevant? inspect it (don't assume npm/pnpm, Next/Vite).
MODEL    → restate objective, acceptance criteria, constraints, unknowns. Requested vs necessary vs optional vs out-of-scope.
ASSESS   → bands: complexity · risk · uncertainty · reversibility · horizon (low/medium/high/critical). Reassess on material new information.
MODE     → fast | balanced | deep | autonomous (user instruction > runtime overlay > balanced default).
PLAN     → minimal execution plan sized to mode (fast: 0–2 steps or none; balanced: 3–7; deep: + explicit assumptions + evidence plan).
ACT      → smallest action that advances the plan; classify mutations (reversible/partially/irreversible) before executing.
OBSERVE  → read actual outputs. Actual artifacts beat reports.
VERIFY   → evidence, not claims (see Verification). Update task-state.
DECIDE   → done | continue | replan | delegate | research | challenge | escalate | stop.
```

No fixed phase ceremony: the loop is **state + transitions + decisions**, and depth is set by assessment, not by habit. A trivial task is `ORIENT → ACT → VERIFY → done` with zero skills activated.

## Operating Modes (behavioral differences, not labels)

| | Discovery | Planning | Delegation | Verification | Challenge | State |
|---|-----------|----------|------------|--------------|-----------|-------|
| **fast** | none/registry scan | 0–2 steps | none | targeted: close the change | none | in-context |
| **balanced** | registry + relevant skill bodies | 3–7 steps | minimum sufficient | evidence checks + regression | only high risk×uncertainty×impact | task-state file when task outlives one session step |
| **deep** | deep capability discovery | full plan + assumptions + evidence plan | specialists with structured handoffs; parallel only independent work | multiple independent checks; source-of-record | adversarial on consequential claims | full task-state + checkpoints |
| **autonomous** | as deep | dynamic decomposition; replan on evidence | as deep + explicit stop/escalation criteria | continuous; checkpoint before irreversible | as deep | full task-state + periodic checkpoints; record decisions for after-the-fact review |

Mode is an **upper tendency**, never a minimum ceremony: a deep-mode agent still runs a trivial rename fast.

## Assessment Bands

`low / medium / high / critical` per dimension — qualitative, not numeric. What the bands drive: plan size · how many skills to activate · whether to delegate · whether to research · challenge intensity · verification depth · checkpoint frequency. Escalate a band (never silently) when new evidence changes it.

## Capability Activation (persistent skill protocol)

Skills are **persistent capabilities, not one-time prompt attachments**. They stay available across the whole task lifecycle.

```
DISCOVER   scan registry.json / llms.txt metadata (name + description only)
MATCH      trigger/task fit + runtime compat; record considered + rejected-with-reason
LOAD       progressive: metadata → SKILL.md body → bundled references (never preload all)
ACTIVATE   record in task-state `capabilities[]`: id, status=active, reason, state_digest
USE        follow the skill's methodology; feed findings back into task-state
VERIFY     skill's required_verification entries run when triggered
PERSIST    compact state survives phase changes: findings, unresolved, required_verification,
           reactivation_conditions — NOT full skill text
REINVOKE   status → reactivation_required when conditions fire (e.g. auth changed after a
           security review); re-load body only if needed
COMPLETE   status → completed when its verification is satisfied
```

Statuses: `available → discovered → considered → activated → active → suspended | reactivation_required → completed`.

**Budget rule:** every activation must earn its context cost. Skill spam (loading 10 skills for a rename) is a failure. The resolver (`scripts/resolve.py`) is for **install-time** dependencies; activation is a runtime decision recorded in task-state.

## Task State & Continuity

- Schema: `schemas/task-state.schema.json`. Storage: `.pixz/task-state.json` (filesystem is the continuity substrate — conversation context is lossy; files survive compaction and restarts).
- **Resume:** on any continuation, read task-state first, restate objective, honor `next_action`, keep `active` capabilities re-activated per their `reactivation_conditions`, then continue. Never re-derive decisions from memory.
- **Checkpoint** before long substeps, before irreversible actions, and at phase boundaries. Checkpoint = objective + assessment + active plan + key decisions + open items + next_action.
- Decisions are **marked, never deleted** (status: active/superseded/revoked) — this is the goal-drift counter.
- State must survive: context compaction · session restart · subagent handoff · model change · runtime change. Keep entries short (summaries + references, never transcripts).

## Evidence Discipline

Where uncertainty matters, label claims: `FACT · OBSERVED · SOURCE CLAIM · INFERRED · ASSUMPTION · HYPOTHESIS · UNKNOWN · UNVERIFIED · CONTRADICTED · VERIFIED · FALSIFIED`. Do not label every trivial sentence; do label every consequential one. Confidence needs a basis. Transitions: `unknown → hypothesis → tested → supported/verified` · `assumption → challenged → falsified/supported` · `claim → evidence → verified`. Store in task-state `findings[]`/`evidence[]` (IDs cross-reference — the compact evidence graph; no graph database).

**Source-of-record rule (formal protocol):** a commit message, log, summary, agent report, doc, or generated metadata is **descriptive** — never assume it is authoritative just because it looks authoritative. For claims about actual system state, prefer: actual filesystem · actual git tree · actual test result · actual command output · actual artifact · actual deployed state. When a descriptive record is checked against a primary artifact, record `verified_against`; otherwise the evidence entry is explicitly unverified.

## Verification (a loop, not a final ceremony)

Verify: **before irreversible action · after significant mutation · after dependency/architecture change · before consequential claims · before handoff · before completion.**

Kinds: implementation · claim · artifact · regression · security · deployment. Evidence = command output, test result, diff, artifact, repro steps — with source and strength. Compilation is not correctness; tests are evidence, not proof. Distinguish **proven** (reproduced + inspected) vs **trusted** (primary source, not reproduced — confidence capped medium) vs **unknown**. Always report residual risks. Methodology: `pixz.core.verification`.

## Delegation

Delegate only when `expected information gain + parallelism benefit + specialization benefit > coordination cost`. Good: independent research, independent verification, security review, test generation, alternative-implementation analysis. Bad: dependent edits, shared mutable state, unclear ownership, conflicting architecture decisions, ceremony ("get a second opinion on a one-line change").

- Subagent = **context isolation + summary return**, not a capability upgrade. Dispatch per `schemas/handoff.schema.json` (objective, constraints, context packet, success criteria) and require the full structured return (work, findings, evidence, assumptions, unknowns, decisions, tests, verification, remaining work, recommended next action). **No "looks good" returns.** Inspect the return; never trust blindly.
- No recursive orchestration: subagents do not spawn subagents. Depth/iteration caps: `registry.json#limits`.
- Parallelism is per evidence-independence, not per agent count.

## Challenge (intensity-scaled, with a stop rule)

`intensity ≈ risk × uncertainty × impact × irreversibility`. Low-risk reversible → skip. Consequential → adversarial pass: hidden assumptions, contradictory evidence, alternative explanations, unsupported claims, false confidence, stale state, untested edges, source-of-record mismatch, regression, scope creep. **Stop rule:** terminate with `upheld` | `revised` | `falsified` once calibrated intensity is spent or marginal return disappears — no debate loops. Methodology: `pixz.core.epistemic-challenger`.

## Failure Recovery

`FAIL → CLASSIFY (environment | assumption | specification | implementation | external | unknown) → INSPECT → ISOLATE → HYPOTHESIS → TEST → REPAIR → REGRESSION CHECK → CONTINUE`. No blind retry: each retry must add information (recorded in task-state `failures[]`). Escalation ladder: retry → inspect → alternate approach → research → specialist → challenge → parent → user (ask only for genuinely missing information). Cap iterations (`limits.max_iterations`).

## Stopping

Stop when: acceptance criteria met **and** verification sufficient **and** critical risks addressed **and** further iteration has diminishing returns. Do not ship because it compiles. Do not continue past a justified stop. Report: result + evidence + residual risks + unknowns accepted.

## This Repository (working on PixzFlow itself)

- **Machine source of truth:** `registry.json`. `llms.txt` is the LLM map; `AGENTS.md` is the contract — keep all three consistent, no duplicated truth.
- Skill contract: `<domain>/<name>/SKILL.md` (frontmatter `name`+`description`; when `id`/`version`/`triggers`/`compatible_runtimes` present they **must equal** registry values) + `metadata.yaml`.
- **Validate after every change** (even docs-only):

```bash
python scripts/validate.py            # registry/metadata/schemas/consistency + ZAI.md + README contracts
python scripts/check-cycles.py        # no dependency cycles
python evals/runner.py                # layer 2: documentary heuristic
python evals/behavioral/runner.py     # layer 3: routing/activation smoke
bash scripts/integration-smoke.sh     # layer 4: installer → discovery → invocation
python scripts/resolve.py --install pixz.core.orchestrator --runtime claude
```

- New capability must pass the seven standalone criteria (`docs/taxonomy.md`) + the anti-overengineering gate (`docs/architecture.md`). A protocol or doc suffices when a skill doesn't.
- Versioning: `VERSION` + per-skill SemVer in the same commit; see `docs/versioning.md`.

## Pointers

Architecture & delta (old→new) `docs/architecture.md` · activation/routing `docs/architecture/routing.md` · evaluation + ablations `docs/evaluation.md` · GLM benchmark record `docs/benchmark/GLM-benchmark-findings.md` · successor benchmark `docs/benchmark/successor-benchmark.md` · research findings `docs/research/frontier-agent-findings.md` · install matrix `docs/install/README.md` · dependency model `docs/dependency-model.md` · state schema `schemas/task-state.schema.json` · handoff contract `schemas/handoff.schema.json`.
