# AGENTS.md — PIXZ.DEV Skills (Agent Guide)

> **Canonical for agents.** Source of truth for discovery, workflow, skill/registry conventions, validation, and contribution. Human overview is `README.md`; this file is operational.

## Purpose

Portable skills that answer: *what skill for this task, what does it require, which runtime can run it, how is it verified/challenged?* See `README.md#why` for narrative; this file tells you how to work in this repo.

## Architecture (source of truth)

- **Core:** `SKILL.md` + `metadata.yaml` per skill, validated by `schemas/skill.schema.json`
- **Registry:** `registry.json` is **machine source** (validated by `schemas/registry.schema.json`); `AGENTS.md` (this file) is its human/agent projection; `*/AGENTS.md` are navigation only.
- **Workflow state:** `schemas/workflow.schema.json` (11 runtime phases: `DEFINE`, `DISCOVER`, `RESEARCH`, `PLAN`, `EXECUTE`, `INSPECT`, `CHALLENGE`, `VERIFY`, `REPLAN`, `IMPROVE`, `SHIP`). Methodological `NORMALIZE`/`ARCHITECT` map to `PLAN`; `IMPLEMENT` maps to `EXECUTE`. `REINITIATE` is a policy (restart from `DEFINE`), not a state — see `docs/architecture.md`.
- **Adapter:** `adapters/` are thin translators; core methodology never forks per runtime.

## Workflow — How Agents Work Here

Follow:
```
UNDERSTAND → DISCOVER → PLAN → EXECUTE → INSPECT → CHALLENGE → VERIFY → REPLAN → IMPROVE → VERIFY → SHIP
```
- **Complexity-aware:** trivial rename → `UNDERSTAND→EXECUTE→VERIFY` (no orchestrator). High risk×uncertainty×impact → full loop with challenger + quality-gate. See `docs/architecture/routing.md`.
- **Context protocol:** `workflow state → repo/local → tools/MCP → docs → external research (official first) → user last`
- **Environment first:** inspect OS/runtime/framework/package-manager/git (`pixz.core.environment-awareness`) before assuming `npm` vs `pnpm`, `Next.js` vs `Vite`.

## Skill Conventions

- **Folder:** `<domain>/<name>/SKILL.md` + `metadata.yaml` (required). `name` in frontmatter **should be kebab-case slug matching folder** for `npx skills` CLI compat (`orchestrator`, not `Orchestrator`). Currently titles are human-case but folder slug is used for CLI `--skill <folder>`.
- **Frontmatter:** `---` with `name` and `description` (progressive disclosure budget; frontmatter always visible). When `id`, `version`, `triggers`, or `compatible_runtimes` are present in frontmatter they **must equal the registry values** — `scripts/validate.py` cross-checks them (hard error on drift).
- **Contract (all):** Purpose, Triggers, When to use / NOT, Inputs, Required context, Methodology (operational steps), Dependencies, Tools, Constraints/Failure, Verification, Example, Structured output. Long rationale → `docs/`.
- **ID:** stable `pixz.<domain>.<name>` — never filename.

## Registry Conventions

- **Single source:** `registry.json`. Do not edit this projection (`AGENTS.md` trigger table) without editing `registry.json` + `metadata.yaml`; run `python scripts/validate.py` to catch drift.
- **Generated files:** `registry.json` is **not** generated from a separate builder here; it's manually maintained but cross-checked by `scripts/validate.py` (registry ↔ metadata ↔ filesystem ↔ schemas). If you add a skill, update both `metadata.yaml` and `registry.json`.
- **Do not edit `registry.json` without validating.**

## Validation / Test Commands

```bash
python scripts/validate.py                  # layer 1: registry/metadata/schemas/cycles + SKILL.md frontmatter consistency + profile/README contracts
python scripts/check-cycles.py              # layer 1: no cycles
python evals/runner.py                      # layer 2: doc validation heuristic (15 cases)
python evals/behavioral/runner.py           # layer 3: routing smoke (15 scenarios)
bash scripts/integration-smoke.sh           # layer 4: installer → discovery → invocation (where CLI available)
python scripts/resolve.py --install pixz.core.orchestrator --runtime claude
python scripts/resolve.py --install pixz.core.orchestrator --runtime claude --with-optional  # 12 nodes
```

All must pass before tagging `v*.*.*`.

## Documentation Rules

- **SKILL.md** = instructions at invocation time (operational, concise)
- **`docs/`** = human explanation, architecture, install, troubleshooting, evaluation
- Do not duplicate whole README into this file; do not inflate SKILL.md with docs.

Structure: `docs/getting-started.md`, `docs/install/README.md` (+ `skills-sh.md`, `claude-code.md`, `openclaw.md`, `opencode.md`, `hermes.md`, `generic.md`), `docs/architecture.md`, `docs/architecture/routing.md`, `docs/evaluation.md`, `docs/development/*`, `docs/troubleshooting.md`, `docs/install-as-skill.md`, `docs/prompts/install-skill-agent.md`.

## Dependency Rules

- `requires` hard, `aggregates` mandatory when parent installed, `optional` **opt-in** via `--with-optional`, `conflicts` mutual exclusion. See `docs/dependency-model.md`.
- Resolver is `scripts/resolve.py` — deterministic, cycle-DFS, runtime/version gates, depth caps (`max_skill_chain_depth=15`, `max_orchestration_depth=6`, `max_iterations=8` from `registry.json#limits`).
- Do not add `conflicts` without justification; do not make `requires` optional to game the graph.

## Contribution Rules

See `CONTRIBUTING.md`. New skill must pass seven standalone criteria (distinct objective, methodology, triggers, I/O, failure, independent value) and `scripts/validate.py` + `scripts/check-cycles.py`. Do not create a skill when a protocol/policy/doc suffices.

## Anti-AI-Slop Rules

- No generic SaaS glassmorphism, template grids, meaningless gradients/animations, filler copy — see `pixz.quality.anti-ai-slop/SKILL.md`
- No boilerplate comments, fake evidence, citation dumping, invented capabilities
- No badge wall, no `🚀 Revolutionary` without evidence
- Every claim in docs → evidence label: **OBSERVED** (repo/file), **VERIFIED** (official docs + CLI/ls output), **PARTIALLY VERIFIED**, **DOCUMENTED ONLY**, **UNKNOWN**
- Repo must not exhibit the problems its skills prevent — see `docs/troubleshooting.md`

## How to Avoid Modifying Generated Artifacts Incorrectly

- `registry.json` ↔ `*/metadata.yaml` ↔ `*/SKILL.md` ↔ `schemas/*` must stay consistent — `scripts/validate.py` is the gate.
- Do not hand-edit `registry.json` skills without creating the matching `metadata.yaml` + `SKILL.md` and running validation.
- `docs/` may contain generated sections; check file header for source.

## Discovery — Capability Map (projection of `registry.json`)

> **Install ≠ clone.** `git clone` gives source; install registers in `<runtime>/skills/`. See `docs/install/README.md` matrix.

**Core (mandatory via orchestrator — 10 nodes, 12 with `--with-optional`):**

| ID | Name | Path | Triggers | Requires |
|----|------|------|----------|----------|
| `pixz.core.orchestrator` | Orchestrator | `core/orchestrator/` | orchestrate, coordinate, delegate, complex task | — (aggregates 8) |
| `pixz.core.planning` | Planning | `core/planning/` | plan, roadmap | context-engineering |
| `pixz.core.context-engineering` | Context Engineering | `core/context-engineering/` | context, requirements | — |
| `pixz.core.environment-awareness` | Environment Awareness | `core/environment-awareness/` | environment, stack detection | — |
| `pixz.core.capability-discovery` | Capability Discovery | `core/capability-discovery/` | discover, available tools | — |
| `pixz.core.workflow-continuity` | Workflow Continuity | `core/workflow-continuity/` | workflow, handoff | context-engineering |
| `pixz.core.delegation-handoff` | Delegation & Handoff | `core/delegation-handoff/` | delegate, handoff | workflow-continuity, context-engineering |
| `pixz.core.epistemic-reasoning` | Epistemic Reasoning | `core/epistemic-reasoning/` | reason, evidence, confidence | context-engineering |
| `pixz.core.epistemic-challenger` | Epistemic Challenger | `core/epistemic-challenger/` | challenge, falsify | epistemic-reasoning |
| `pixz.core.verification` | Verification | `core/verification/` | verify, inspect | epistemic-reasoning |
| `pixz.core.change-safety` | Change Safety | `core/change-safety/` | safe change, reversible | environment-awareness |
| `pixz.core.replanning` | Replanning | `core/replanning/` | replan, pivot | planning, verification |
| `pixz.core.quality-gate` | Quality Gate | `core/quality-gate/` | quality gate, ship check | verification, change-safety |

`orchestrator` aggregates: planning, context-engineering, environment-awareness, capability-discovery, workflow-continuity, epistemic-reasoning, verification, quality-gate — mandatory (10). Optional (opt-in): epistemic-challenger, anti-ai-slop.

**Quality / Domain:**

| ID | Path | Triggers |
|----|------|----------|
| `pixz.quality.anti-ai-slop` | `quality/anti-ai-slop/` | anti slop, boilerplate |
| `pixz.engineering.api-design` | `engineering/api-design/` | api design, openapi |
| `pixz.engineering.system-design` | `engineering/system-design/` | system design |
| `pixz.security.review` | `security/review/` | security review |
| `pixz.security.threat-modeling` | `security/threat-modeling/` | threat model, STRIDE |
| `pixz.design.uiux` | `design/uiux/` | ui design, ux review |
| `pixz.design.design-system` | `design/design-system/` | design system, tokens |
| `pixz.frontend.react` | `frontend/react/` | react, next.js |
| `pixz.frontend.accessibility` | `frontend/accessibility/` | a11y, wcag |
| `pixz.motion.gsap` | `motion/gsap/` | gsap, scrolltrigger |
| `pixz.motion.remotion` | `motion/remotion/` | remotion |
| `pixz.devops.docker` | `devops/docker/` | docker |
| `pixz.devops.kubernetes` | `devops/kubernetes/` | k8s, helm |
| `pixz.ai.rag` | `ai/rag/` | rag, retrieval |
| `pixz.ai.agent-design` | `ai/agent-design/` | agent design |

Runtime compat for all: `claude, openclaw, opencode, hermes, codex, generic` — see `docs/install/README.md` for VERIFIED vs PARTIALLY classification.

## Installation (not clone) — where skills land

See matrix `docs/install/README.md`. Summary: skills.sh `npx skills add` auto-picks `~/.claude/skills` / `.opencode/skill` / `.agents/skills`; Claude `~/.claude/skills/` or `.claude/skills/`; OpenClaw `skills/` / `~/.openclaw/skills/` / `openclaw skills list`; OpenCode `.opencode/skill/` (singular) + compat; Hermes `~/.hermes/skills/` or `skills/`; Generic `.agents/skills/`.

For agent copy-paste: `README.md` inline prompts (**AI Agent Installation Prompt**, **Super Z / GLM / Z.AI Web Prompt**), `docs/install-as-skill.md` (short), and `docs/prompts/install-skill-agent.md` (runtime-adaptive full with verification report).

## Runtime Profiles (isolated — not skills)

A **profile** is a runtime-specific operating overlay (class: PROFILE / restricted POLICY). It is **not a skill**: no `pixz.*` ID, not in `registry.json`, not resolved by `scripts/resolve.py`, and it **does not change** universal skill semantics, the dependency model, or the verification layers. It only parameterizes orchestrator operating depth and runtime compute/interaction policy; on conflict, skills and repo policies win.

- **Super Z / GLM / Z.AI Web** → `profiles/super-z/PROFILE.md`: mandatory `AskUserQuestion` mode selection before substantive work (FAST / BALANCED / DEEP / AUTONOMOUS; default BALANCED), mode semantics, compute policy ("generous compute is not permission to waste compute"), graceful degradation when `AskUserQuestion` is absent.
- Status: **SPECIFIED** (2026-09-22); behavioral effect **UNVERIFIED** — never cite the profile as behaviorally effective.
- Isolation contract + extension rules: `profiles/README.md`. Machine-checked by `scripts/validate.py` (presence + required sections + README prompt sections).
- README entry points: **AI Agent Installation Prompt** and **Super Z / GLM / Z.AI Web Prompt** (copy-paste, inline in `README.md`); full runtime-adaptive prompt: `docs/prompts/install-skill-agent.md`.

## Versioning

`VERSION` 1.1.0 repo; `metadata.yaml:version` per skill; `latest` (main HEAD) / `stable` (latest `v*.*.*` tag) / `pinned` (future — no `pixz.lock` yet, see `docs/versioning.md`).

## Verification (layers)

1 `validate.py` + `check-cycles.py`  2 `evals/runner.py`  3 `evals/behavioral/runner.py`  4 `scripts/integration-smoke.sh` — never present 1–2 as 3–4.

## Portability Classification (keep honest)

- **Native portable** — same `SKILL.md` works with no adapter (all runtimes here)
- **Adapter-compatible** — path translation only (our adapters)
- **Documentation-compatible** — understood but not auto-installable
- **Unsupported** — no verified path (don't claim)

Do not call everything “universal”.
