# AGENTS.md — PIXZ.DEV Skills Ecosystem (Root Registry)

> **Canonical entry point for agent-driven discovery.** This file is both human-readable and machine-parseable. It delegates to hierarchical registries without duplicating truth.
> Machine source of truth: [`registry.json`](./registry.json) validated by [`schemas/registry.schema.json`](./schemas/registry.schema.json). Agent execution contracts: [`schemas/skill.schema.json`](./schemas/skill.schema.json).

## How to Install / Discover

```bash
# Stable (production) — pin a known-good version
git clone --branch v1.0.0 https://github.com/pixzdev/skills.git
# or: git clone https://github.com/pixzdev/skills.git && git checkout v1.0.0

# Latest (development)
git clone https://github.com/pixzdev/skills.git

# Hierarchical discovery
cat AGENTS.md                 # this file — full index
cat core/AGENTS.md            # core capabilities
cat engineering/AGENTS.md     # engineering domain
cat design/AGENTS.md          # design domain
# etc.

# Automated resolution with validation
python scripts/resolve.py --install pixz.core.orchestrator --runtime claude --channel stable
python scripts/validate.py
python scripts/check-cycles.py
```

> **Discovery rule for agents:** Start here. Do not search the repo blindly. This file lists stable IDs, triggers, dependencies and runtime compatibility. Hierarchical `*/AGENTS.md` files improve navigation — they never introduce conflicting metadata.

## Operating Loop

```
UNDERSTAND → DISCOVER → PLAN → EXECUTE → INSPECT → CHALLENGE → VERIFY → REPLAN → IMPROVE → VERIFY → SHIP
```

## Capability Map — 28 Skills, 5 Schemas, 4 Adapters

### Core (mandatory via orchestrator aggregates)

| ID | Name | Path | Triggers | Requires |
|----|------|------|----------|----------|
| `pixz.core.orchestrator` | Orchestrator | `core/orchestrator/` | orchestrate, coordinate, delegate, complex task | — (aggregates 8) |
| `pixz.core.planning` | Planning | `core/planning/` | plan, roadmap, break down | context-engineering |
| `pixz.core.context-engineering` | Context Engineering | `core/context-engineering/` | context, requirements, gather context | — |
| `pixz.core.environment-awareness` | Environment Awareness | `core/environment-awareness/` | environment, stack detection, package manager | — |
| `pixz.core.capability-discovery` | Capability Discovery | `core/capability-discovery/` | discover, available tools, find skill | — |
| `pixz.core.workflow-continuity` | Workflow Continuity | `core/workflow-continuity/` | workflow, handoff, persist state | context-engineering |
| `pixz.core.delegation-handoff` | Delegation & Handoff | `core/delegation-handoff/` | delegate, handoff, subagent | workflow-continuity, context-engineering |
| `pixz.core.epistemic-reasoning` | Epistemic Reasoning | `core/epistemic-reasoning/` | reason, evidence, assumption, confidence | context-engineering |
| `pixz.core.epistemic-challenger` | Epistemic Challenger | `core/epistemic-challenger/` | challenge, how could this be wrong, falsify | epistemic-reasoning |
| `pixz.core.verification` | Verification | `core/verification/` | verify, inspect, validate | epistemic-reasoning |
| `pixz.core.change-safety` | Change Safety | `core/change-safety/` | safe change, reversible, scope control | environment-awareness |
| `pixz.core.replanning` | Replanning | `core/replanning/` | replan, pivot, strategy failed | planning, verification |
| `pixz.core.quality-gate` | Quality Gate | `core/quality-gate/` | quality gate, ship check, release gate | verification, change-safety |

> `orchestrator` aggregates: planning, context-engineering, environment-awareness, capability-discovery, workflow-continuity, epistemic-reasoning, verification, quality-gate. Installing orchestrator resolves them and their transitive `requires`. Optional: epistemic-challenger, change-safety, anti-ai-slop.

### Quality

| ID | Name | Path | Triggers | Requires |
|----|------|------|----------|----------|
| `pixz.quality.anti-ai-slop` | Anti-AI Slop | `quality/anti-ai-slop/` | anti slop, generic design, boilerplate | verification |

### Domain / Niche

| ID | Name | Path | Triggers | Requires |
|----|------|------|----------|----------|
| `pixz.engineering.api-design` | API Design | `engineering/api-design/` | api design, rest, openapi | context-engineering |
| `pixz.engineering.system-design` | System Design | `engineering/system-design/` | system design, architecture | planning, epistemic-reasoning |
| `pixz.security.review` | Security Review | `security/review/` | security review, audit | verification |
| `pixz.security.threat-modeling` | Threat Modeling | `security/threat-modeling/` | threat model, STRIDE | context-engineering, epistemic-reasoning |
| `pixz.design.uiux` | UI/UX Design | `design/uiux/` | ui design, ux review | context-engineering |
| `pixz.design.design-system` | Design System | `design/design-system/` | design system, tokens | design.uiux |
| `pixz.frontend.react` | React Engineering | `frontend/react/` | react, next.js, hooks | environment-awareness |
| `pixz.frontend.accessibility` | Accessibility | `frontend/accessibility/` | a11y, wcag, aria | design.uiux |
| `pixz.motion.gsap` | GSAP Motion | `motion/gsap/` | gsap, scrolltrigger | environment-awareness |
| `pixz.motion.remotion` | Remotion | `motion/remotion/` | remotion, programmatic video | environment-awareness |
| `pixz.devops.docker` | Docker & Containers | `devops/docker/` | docker, container | environment-awareness |
| `pixz.devops.kubernetes` | Kubernetes | `devops/kubernetes/` | kubernetes, k8s, helm | docker |
| `pixz.ai.rag` | RAG Systems | `ai/rag/` | rag, retrieval, grounding | epistemic-reasoning, verification |
| `pixz.ai.agent-design` | Agent Design | `ai/agent-design/` | agent design, tool calling | orchestrator, change-safety |

## Runtime Compatibility

All 28 skills declare `compatible_runtimes: [claude, openclaw, opencode, hermes, codex, generic]`.

- **Claude / Claude Code:** `SKILL.md` frontmatter (`name`, `description`) progressive disclosure; install to `.claude/skills/` or project root; import via `@AGENTS.md` inside `CLAUDE.md`.
- **OpenClaw:** install to `<workspace>/skills/` or `~/.openclaw/skills/`; `agents.entries.*.skills` allowlist is final (non-merging).
- **OpenCode / Hermes / generic:** generic `SKILL.md` — adapter translates paths. See `adapters/`.

Compatibility differences are documented in `adapters/README.md` — core methodology stays runtime-agnostic.

## Dependency Model

- `requires` — hard; missing → install fails
- `aggregates` — orchestrator composition (recursive)
- `optional` — best-effort if compatible & non-conflicting
- `conflicts` — mutual exclusion

Resolver: `scripts/resolve.py` (topo-sort + cycle DFS + runtime/version gates). Limits: `max_skill_chain_depth=12`, `max_orchestration_depth=6`, `max_iterations=8` (from `registry.json`).

## Skill Contract (every SKILL.md)

Purpose · Triggers · When to use / when NOT · Inputs · Required context · Methodology · Outputs · Dependencies · Tools · Failure conditions · Verification · Example · Structured output

Tools selected by task-fit, cost, freshness, reversibility and risk — not by availability.

## Protocols & Policies

- **Protocols:** Context, Workflow Propagation, Argumentation, Escalation Ladder — see `docs/architecture.md`, `schemas/workflow.schema.json`.
- **Policies:** Scope Control, Simplicity, Change Safety, Anti-AI Slop — globally enforced.

## Evaluation

Each skill has `metadata.yaml` + `SKILL.md`. Central evals: `evals/cases/*.yaml` (trigger/method/output/failure/verification/scope/hallucination/consistency). Run `python evals/runner.py`.

## Hierarchical Registries

- `core/AGENTS.md`, `engineering/AGENTS.md`, `security/AGENTS.md`, `design/AGENTS.md`, `frontend/AGENTS.md`, `motion/AGENTS.md`, `devops/AGENTS.md`, `ai/AGENTS.md`, `quality/AGENTS.md`

Each delegates here for truth; they add domain navigation, examples and boundary notes.

## Versioning

- **IDs stable:** `pixz.<domain>.<name>`
- **Channels:** `latest` (HEAD main), `stable` (latest `v*.*.*` tag that passed quality-gate), `pinned` (exact SemVer / git SHA)
- **File:** `VERSION` at root; per-skill `version` in `metadata.yaml`

## Agent Instructions

1. **Discover** via this file before any tool search.
2. **Environment-awareness first:** inspect OS/runtime/framework/package-manager/git before assuming.
3. **Capability-discovery second:** only after discovery should you select.
4. **Complexity-aware:** do not invoke full orchestration for trivial reversible tasks.
5. **Preserve workflow state** per `schemas/workflow.schema.json` and handoff via `delegation-handoff`.
6. **Cite sources** for research; distinguish `FACT` vs `INFERENCE` vs `ASSUMPTION` vs `UNKNOWN`.

## Research Grounding

Conventions researched from official docs / repos:
- Claude Skills progressive disclosure (anthropic: `SKILL.md` + `name/description` frontmatter, `scripts/references/assets`)
- AGENTS.md open standard (Agentic AI Foundation / Linux Foundation) — cascading hierarchy, `AGENTS.override.md` optional
- OpenClaw skill loading order, allowlists, workshop skills
- OpenCode / Hermes generic SKILL.md
- `llms.txt` for LLM-friendly index (see `llms.txt`)

## Quick Triggers Index

> “What capability do I need?” → scan *Triggers* table above. Resolver answers: dependencies, runtime, context, verification, challenge routing.

---

*This registry is validated by `scripts/validate.py` — do not edit skills without re-validating. See `CONTRIBUTING.md` for taxonomy rules.*
