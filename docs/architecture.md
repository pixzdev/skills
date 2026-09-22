# Architecture — PIXZ.DEV Universal Agent Skills Ecosystem

## Governing Loop — Methodological

```
UNDERSTAND → DISCOVER → PLAN → EXECUTE → INSPECT → CHALLENGE → VERIFY → REPLAN → IMPROVE → VERIFY → SHIP
```

*This is the loop the orchestrator owns (see `core/orchestrator/SKILL.md`).*

## Runtime Workflow State — Machine Representation

`schemas/workflow.schema.json` persists **runtime state**, not the full methodological narrative.

- **Enum (11):** `DEFINE, DISCOVER, RESEARCH, PLAN, EXECUTE, INSPECT, CHALLENGE, VERIFY, REPLAN, IMPROVE, SHIP`
- **Why 11 not 13:** Methodological phases `NORMALIZE` (taxonomy), `ARCHITECT` (design), and `IMPLEMENT` are **substeps** of the runtime `PLAN` and `EXECUTE` states. The earlier design doc used `NORMALIZE → ARCHITECT → IMPLEMENT` as human-facing decomposition of `PLAN/EXECUTE`; those are not separate machine states. This corrects audit finding #9 (phase drift).
- **Mapping:** `NORMALIZE + ARCHITECT → PLAN`; `IMPLEMENT → EXECUTE`. `UNDERSTAND` is the content of `DEFINE`. Two `VERIFY` stages in the loop collapse to one `VERIFY` state with iteration count.

If you need the human methodology vs machine state distinction, treat this document as authoritative for the mapping; `schemas/workflow.schema.json` is authoritative for persistence.

## REINITIATE — Control-Flow Policy, Not a State

`REINITIATE` is **not** a `workflow.schema.json` phase. It is a **policy** evaluated by the orchestrator:

> If architecture or plan is fundamentally flawed (evidence disproves premise), discard the plan (not the objective) and restart from `DEFINE` with new assumptions.

This is **C — orchestrator policy** per audit finding #10, not a workflow enum. It is triggered by failed verification, falsified assumptions, or contradictory evidence, and bounded by `max_iterations`.

## Separation of Concerns

| Concept | Definition | Example | Class |
|---------|------------|---------|-------|
| **AGENT** | who performs work | Claude, subagent, human, CI | agent |
| **SKILL** | how a class of work should be performed (portable methodology) | `pixz.security.review` | skill |
| **TOOL** | what agent uses | bash, read_file, MCP server | tool |
| **ORCHESTRATOR** | who coordinates overall work | `pixz.core.orchestrator` | skill (meta) |
| **PROTOCOL** | how agents behave across tasks | workflow-continuity, context protocol | protocol |
| **POLICY** | constraints applying globally | change-safety, scope control, REINITIATE | policy |
| **EVAL** | how skill behavior is tested | `evals/` four layers | eval |
| **REGISTRY** | discovery index | `AGENTS.md` + `registry.json` | registry |

Do not collapse these into a single prompt.

## Universal Core → Adapter

```
Universal Core (methodology, schemas, contracts — SPECIFIED)
        ↓
Runtime Adapter (translation — VERIFIED for 4 runtimes)
        ↓
Runtime-specific representation (.claude/skills/, ~/.openclaw/skills/, etc.)
```

Core remains vendor-neutral. Adapters are thin translators — see `adapters/README.md` for VERIFIED vs PARTIALLY VERIFIED matrix.

## Core Skill Graph — Verified (v1.1.0)

```
orchestrator (mandatory aggregates: 8)
 ├── planning → context-engineering
 ├── context-engineering
 ├── environment-awareness
 ├── capability-discovery
 ├── workflow-continuity → context-engineering → delegation-handoff (separate)
 ├── epistemic-reasoning → context-engineering → challenger (optional)
 ├── verification → epistemic-reasoning
 └── quality-gate → verification + change-safety → environment-awareness

Resolved mandatory: 10 nodes (see docs/dependency-model.md)
With --with-optional (+challenger +anti-slop): 12 nodes
All orchestrator aggregates are mandatory when orchestrator is installed.
Optional requires explicit flag. Resolver recursively expands `requires` and validates `conflicts` and cycles.
```

## Registry

- `AGENTS.md` (human + agent entry point) — hierarchical discovery
- `registry.json` (machine-readable, generated from `metadata.yaml` via `scripts/validate.py` consistency check) — validated against `schemas/registry.schema.json`
- `*/AGENTS.md` per domain — navigation only, no duplicate truth
- Source of truth for skill metadata is `registry.json`; `AGENTS.md` is its projection. See `docs/taxonomy.md`.

## Complexity-Aware Orchestration

| Signal | Minimal: UNDERSTAND→EXECUTE→VERIFY | Full: DISCOVER→...→SHIP |
|--------|------------------------------------|-------------------------|
| scope small, reversible, low risk×uncertainty×impact | ✓ | — |
| risk×uncertainty×impact high, multi-file, irreversible, research-heavy | — | ✓ with CHALLENGE/REPLAN/QUALITY-GATE |

Prevent `orchestration overhead > task value`. See `core/quality-gate/SKILL.md` for stop conditions.

## Safety — Circular Router Mitigation

If the router selects work skill, challenger, verifier and gate all via same mechanism, a routing failure can disable safety. Mitigations **implemented**:

- **Non-optional baseline:** `verification` is a hard `requires` of `quality-gate`; `quality-gate` is mandatory via orchestrator aggregates. Even if router mis-selects, resolver guarantees gate presence for orchestrated tasks.
- **Static policy guard:** `change-safety` classification (reversible/partially/irreversible) is policy, not routed — irreversible mutations require confirmation regardless of router.
- **Risk-based hard constraint:** tasks with `risk×impact=high` (security, prod migration) escalate via `epistemic-challenger` intensity — not optional skip.
- **Independent second-pass:** `scripts/validate.py` + `scripts/check-cycles.py` run pre-ship outside router (static check).
- **See:** `docs/architecture/routing.md` for routing tests and under/over-routing metrics.

## Limits

From `registry.json#limits` (VERIFIED, enforced by adapters):

- `max_skill_chain_depth: 15`
- `max_orchestration_depth: 6`
- `max_iterations: 8`

## Observability

Workflow state conforms to `schemas/workflow.schema.json` — objective, phase, decisions, assumptions, arguments, evidence, unknowns, verification, iteration history, residual risks. Persistence is adapter-defined (filesystem `/.pixz/workflow.json` example in `examples/` or in-memory). 

## Anti-Patterns Guarded

- Skill explosion → taxonomy normalization (7 criteria)
- Recursive orchestration → cycle detection + depth caps
- Silent breaking change → SemVer + `VERSION` + channel (pinned as future, see `docs/versioning.md`)
- Documentation drift → single source (`registry.json`) + `scripts/validate.py` consistency
