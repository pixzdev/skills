# AGENTS.md — Core — Orchestration & Reasoning (`core/`)

> Hierarchical registry for `core/`. This file navigates; canonical truth remains [`/AGENTS.md`](../AGENTS.md) + [`/registry.json`](../registry.json). Do not duplicate dependency truth here.

## Skills in `core/`

| ID | Name | Path | Triggers |
|----|------|------|----------|
| `pixz.core.orchestrator` | Orchestrator | `core/orchestrator/` | orchestrate, coordinate |
| `pixz.core.planning` | Planning | `core/planning/` | plan, roadmap |
| `pixz.core.context-engineering` | Context Engineering | `core/context-engineering/` | context, requirements |
| `pixz.core.environment-awareness` | Environment Awareness | `core/environment-awareness/` | environment, stack detection |
| `pixz.core.capability-discovery` | Capability Discovery | `core/capability-discovery/` | discover, available tools |
| `pixz.core.workflow-continuity` | Workflow Continuity | `core/workflow-continuity/` | workflow, handoff |
| `pixz.core.delegation-handoff` | Delegation & Handoff | `core/delegation-handoff/` | delegate, handoff |
| `pixz.core.epistemic-reasoning` | Epistemic Reasoning | `core/epistemic-reasoning/` | reason, evidence |
| `pixz.core.epistemic-challenger` | Epistemic Challenger | `core/epistemic-challenger/` | challenge, falsify |
| `pixz.core.verification` | Verification | `core/verification/` | verify, inspect |
| `pixz.core.change-safety` | Change Safety | `core/change-safety/` | safe change, reversible |
| `pixz.core.replanning` | Replanning | `core/replanning/` | replan, pivot |
| `pixz.core.quality-gate` | Quality Gate | `core/quality-gate/` | quality gate, ship check |
| `pixz.core.self-learning` | Self-Learning | `core/self-learning/` | self-train, post-install, skill version changed |

## Discovery
```bash
cat core/AGENTS.md  # this file — domain navigation
cat AGENTS.md           # full ecosystem index
python scripts/resolve.py --install pixz.core.orchestrator --runtime claude
```

## Boundaries
- This file does not redefine `requires`/`aggregates` — see `metadata.yaml` + `registry.json`.
- See `docs/taxonomy.md` for why these domain boundaries exist and what was merged.
- See `core/*/SKILL.md` for methodology contracts and `core/*/metadata.yaml` for machine contracts.

## Related
- Root registry: `../AGENTS.md`
- Adapter notes: `../adapters/README.md`
- Eval harness: `../evals/`
