# Architecture — PIXZ.DEV Universal Agent Skills Ecosystem

## Governing Loop
```
UNDERSTAND → DISCOVER → PLAN → EXECUTE → INSPECT → CHALLENGE → VERIFY → REPLAN → IMPROVE → VERIFY → SHIP
```

## Separation of Concerns

| Concept | Definition | Example |
|---------|------------|---------|
| **AGENT** | who performs work | Claude, subagent, human, CI |
| **SKILL** | how a class of work should be performed (portable methodology) | `pixz.security.review` |
| **TOOL** | what agent uses | bash, read_file, MCP server |
| **ORCHESTRATOR** | who coordinates overall work | `pixz.core.orchestrator` |
| **PROTOCOL** | how agents behave across tasks | workflow-continuity, context protocol |
| **POLICY** | constraints applying globally | change-safety, scope control |
| **EVAL** | how skill behavior is tested | `evals/cases/*.yaml` |
| **REGISTRY** | discovery index | `AGENTS.md` + `registry.json` |

Do not collapse these into a single prompt.

## Universal Core → Adapter

```
Universal Core (methodology, schemas, contracts)
        ↓
Runtime Adapter (translation layer)
        ↓
Runtime-specific representation (.claude/skills/, ~/.openclaw/skills/, etc.)
```

Core remains vendor-neutral. Adapters are thin translators.

## Core Skill Graph

```
orchestrator
 ├── planning
 ├── context-engineering
 ├── environment-awareness
 ├── capability-discovery
 ├── workflow-continuity → delegation-handoff
 ├── epistemic-reasoning → epistemic-challenger
 ├── verification → quality-gate
 └── (optional) anti-ai-slop, change-safety

All orchestrator aggregates are mandatory when orchestrator is installed.
Resolver recursively expands `requires` and validates `conflicts` and cycles.
```

## Registry

- `AGENTS.md` (human + agent entry point) — hierarchical discovery
- `registry.json` (machine-readable) — validated against `schemas/registry.schema.json`
- `*/AGENTS.md` per domain — navigation only, no duplicate truth

## Complexity-Aware Orchestration

| Signal | Minimal Workflow | Full Orchestration |
|--------|----------------|-------------------|
| scope small, reversible | UNDERSTAND→EXECUTE→VERIFY | — |
| risk×uncertainty×impact high | — | Full loop with CHALLENGE/REPLAN/QUALITY-GATE |

Prevent `orchestration overhead > task value`.

## Limits

From `registry.json#limits`:

- `max_skill_chain_depth: 12`
- `max_orchestration_depth: 6`
- `max_iterations: 8`

Adapters enforce these.

## Observability

Workflow state conforms to `schemas/workflow.schema.json` — objective, phase, decisions, assumptions, arguments, evidence, unknowns, verification, iteration history, residual risks. Persistence is adapter-defined.

## Anti-Patterns Guarded

- Skill explosion → taxonomy normalization (standalone skill needs distinct objective/trigger/I/O/failure value)
- Recursive orchestration → cycle detection + depth caps
- Silent breaking change → SemVer + `VERSION` pinning + `latest/stable/pinned` channels
