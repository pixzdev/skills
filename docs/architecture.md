# Architecture — PixzFlow 2.0

> **PixzFlow** = a persistent, adaptive, model-agnostic **operating layer** for capable AI agents. PIXZ.DEV is the brand; this repository is the PixzFlow ecosystem.
> This document is authoritative for the layer model and the operating model. `AGENTS.md` is the agent-facing contract; `registry.json` is the machine source of truth.

## Layer Model (conceptual, not infrastructure)

```
LEVEL 0 — Model-native infrastructure
    reasoning · context window · native tool use · native memory · native planning · native safety
    (cannot be replaced by PixzFlow — never try)
        ↓
LEVEL 1 — Model/runtime infrastructure
    runtime · tool APIs · MCP · sandbox · filesystem · shell · subagents · model routing
        ↓
LEVEL 2 — PixzFlow persistent operating layer (this repository)
    AGENTS.md (contract) · entry protocol · operating modes · task-state protocol ·
    evidence discipline · source-of-record · delegation policy · verification policy ·
    capability-activation protocol · stopping rules · schemas/
        ↓
LEVEL 2.5 — Runtime-specific persistent overlays
    ZAI.md (Super Z / GLM / Z.AI Web) · future: other runtime overlays
    (parameterize operating depth + compute policy; never change L2 semantics)
        ↓
LEVEL 3 — PixzFlow capabilities
    skills (registry.json) · specialist workflows · domain knowledge · verification modules
        ↓
LEVEL 4 — Dynamic execution
    agents · subagents · tools · MCP · commands · external systems
        ↓
LEVEL 5 — Task state / evidence
    task-state files · findings · decisions · artifacts · tests · verification records ·
    handoffs · residual risks
```

The hierarchy is conceptual: it organizes responsibility. It is **not** an excuse to create infrastructure for each level. Levels 0–1 belong to the model/runtime; PixzFlow owns 2, 2.5, 3 and the *protocol* for 4–5 (the runtime executes them).

## Operating Model (state + transitions, not phases)

v1.1.0's 11-phase loop (`DEFINE→...→SHIP`) is **retired**. The fundamental unit is **state + transition + capability + evidence + verification + decision**. The loop:

```
ORIENT → MODEL → ASSESS → MODE → PLAN → ACT → OBSERVE → VERIFY → DECIDE
                                                        ├── done
                                                        ├── continue
                                                        ├── replan
                                                        ├── delegate
                                                        ├── research
                                                        ├── challenge
                                                        └── escalate / stop
```

- **State**: one compact file per task (`schemas/task-state.schema.json`, default `.pixz/task-state.json`) — objective, acceptance criteria, assessment, plan, decisions (marked, never deleted), typed findings, evidence ledger, capability activation state, failures, verification, next_action, checkpoint.
- **Transitions** are decisions with causes; every material transition is recorded.
- **Depth is set by assessment**, not by habit: a trivial task is `ORIENT → ACT → VERIFY → done` with zero skills activated, in any mode.
- **REINITIATE** remains a *decision* (discard the flawed plan, keep the objective) — never a state.

### Operating Modes (behavioral differences, not labels)

| | Discovery | Planning | Delegation | Verification | Challenge | State |
|---|-----------|----------|------------|--------------|-----------|-------|
| **fast** | none/registry scan | 0–2 steps | none | targeted | none (intensity 0) | in-context |
| **balanced** | registry + relevant bodies | 3–7 steps | minimum sufficient | evidence + regression | high risk×uncertainty×impact only | task-state file when task outlives one step |
| **deep** | deep capability discovery | full + assumptions + evidence plan | specialists, structured handoffs, parallel only independent | multiple independent checks, source-of-record | adversarial on consequential claims | full state + checkpoints |
| **autonomous** | as deep | dynamic decomposition | as deep + explicit stop/escalation | continuous; pre-irreversible checkpoints | as deep | full state + periodic checkpoints |

Mode selection: user instruction > runtime overlay (`ZAI.md` mandatory AskUserQuestion for Super Z/GLM/Z.AI Web) > balanced default. Mode is an **upper tendency** — a deep-mode agent still runs a trivial subtask fast.

### Assessment

Qualitative bands (`low / medium / high / critical`), not numeric scores: complexity · risk · uncertainty · reversibility · horizon. Bands drive plan size, activation count, delegation, research, challenge intensity, verification depth, checkpoint frequency. Reassessment on material new information is required; silent band changes are bugs. (Bands over numbers: HYPOTHESIS — validated by the successor benchmark's cross-model cells.)

## Capability Activation (the benchmark's core finding)

The GLM benchmark showed: **skills alone ≈ no measurable advantage (B≈B1, C≈A)** and **availability ≠ invocation** (native GLM didn't discover installed skills; used them when made explicit). PixzFlow's primary job is therefore to determine **WHEN / WHY / WHICH / HOW DEEPLY / UNDER WHAT VERIFICATION / FOR HOW LONG** capabilities are active.

```
DISCOVER (metadata only) → MATCH (fit + compat; rejected recorded with reason)
  → LOAD (progressive: metadata → body → references) → ACTIVATE (state recorded)
  → USE → VERIFY → PERSIST compact state → REINVOKE (conditions fire) → COMPLETE
```

Statuses: `available → discovered → considered → activated → active → suspended | reactivation_required → completed`. Persisted in task-state `capabilities[]` with `state_digest` (never full skill text), `findings`, `unresolved`, `required_verification`, `reactivation_conditions`. This is what makes a security review survive the architecture→implementation→deployment transition.

**Budget rule (policy `pixz.policy.orchestration-budget`):** every activation must earn its context cost. Skill spam is a failure.

## Evidence Model (compact graph, not graph database)

- **Claims** (`findings[]`) carry a type: `fact · observed · source_claim · inference · assumption · hypothesis · unknown · unverified · contradicted · verified · falsified`, a confidence with basis, and `status` with **explicit transitions** (`unknown→hypothesis→tested→supported` · `assumption→challenged→falsified` · `claim→evidence→verified`).
- **Evidence** (`evidence[]`) carries a `kind`: `artifact · filesystem · git · command_output · test_result · external_source · agent_report · log · documentation · user_statement`.
- **The graph is the references**: `findings.evidence_refs → evidence[].id` and `evidence.verified_against`. No DB, no ceremony.
- **Source-of-record protocol** (promotes T11, n=2 → now testable): descriptive records are never authoritative by appearance; system-state claims verify against actual filesystem / git tree / fresh test output / command output / artifacts / deployed state; `verified_against` recorded, else the evidence is explicitly unverified.

## Delegation & Parallelism

- **Economics test** before delegating: `expected information gain + parallelism + specialization > coordination cost`. Restraint is observable (decision + reason recorded) — anti-delegation is a first-class eval.
- **Contract**: `schemas/handoff.schema.json` — bounded objective, constraints, context packet, success criteria; mandatory structured return (work, findings, evidence, assumptions, unknowns, decisions, tests, verification, remaining work, next action); parent **inspects** (contract met? evidence backs claims? scope controlled?) and accepts/returns/escalates.
- Subagents = **context isolation + summary return** (documented in Claude Code & Gemini CLI), not capability upgrades. **No subagent spawns subagents** (recursion protection, as in Gemini CLI). Caps: `limits` (depth 6, iterations 8, chain 15).
- **Parallelism by evidence independence**, not agent count: independent research/verification/security/test-gen/alt-implementation in parallel; dependent edits & shared state serial.

## Context Engineering (lifecycle)

`DISCOVER → FILTER → PRIORITIZE → LOAD → COMPRESS → PIN → UPDATE → EVICT → RESTORE`. Task state is the PIN substrate: pinned specifics (objective, acceptance criteria, irreversible-constraint list, active assumptions) are written **before** compaction events and restored **after** them. Stale-context detection: findings older than a relevant change are suspect. Goal: maximum useful information per context token (documented principle: Anthropic context engineering; observed compaction behavior: Claude Code docs).

## Failure Recovery (formal)

`FAIL → CLASSIFY (environment|assumption|specification|implementation|external|unknown) → INSPECT → ISOLATE → HYPOTHESIS → TEST → REPAIR → REGRESSION CHECK → CONTINUE`. Each retry must add information (recorded in `failures[]` with a `lesson`). Escalation ladder: retry → inspect → alternate → research → specialist → challenge → parent → user. Research backing: structured verification feedback enables ~70% test-time error recovery (LH-Bench); failures cluster early (LongCLI-Bench) — hence hard ORIENT/ASSESS, drift counters later.

## Verification (first-class loop)

Triggers: before irreversible action · after significant mutation · after dependency/architecture change · before consequential claims · before handoff · before completion. Kinds: implementation · claim · artifact · regression · security · deployment. Proven vs trusted (confidence capped medium) vs unknown. Residual risks always reported.

## Observability

Recorded (never private chain-of-thought): state transitions with causes · capabilities activated (+reason) · delegations + inspections · decisions · findings transitions · evidence (with kind + verified_against) · failures + lessons · verification results · final gate verdict. The task-state file **is** the trace — readable by any observer or auditor, re-injectable after compaction.

## Circular-Safety Mitigation (carried from v1.1.0, restated)

1. **Evidence floor:** `verification` is a hard aggregate of the orchestrator — even a mis-routed task keeps it. Machine-checked by `evals/behavioral/runner.py` (registry invariant).
2. **Static policy not routed:** change-safety tiers (irreversible → confirmation, every mode) run independent of routing.
3. **Risk-based hard constraint:** high risk×impact → challenger intensity high; not skippable without a recorded intensity-0 justification.
4. **Second pass outside the router:** `scripts/validate.py` + `check-cycles.py` run pre-ship, static.
5. **Escalation cannot be routed away:** the failure-recovery ladder is policy.

## Anti-Overengineering Gate (applies to any new subsystem)

Before adding any protocol, schema, skill, agent, state file, registry, abstraction, or evaluator, answer: **What failure does this prevent? What behavior does it enable? What measurable improvement should it produce? What is its context/runtime cost? Can the same benefit be achieved more simply?** If the answer is weak — do not build it. (Applied repeatedly during 2.0 — see delta below.)

## Architecture Delta — v1.1.0 → v2.0.0 (with evidence)

| Area | OLD (1.1.0) | NEW (2.0.0) | Evidence / reason |
|------|-------------|-------------|-------------------|
| Identity | "PIXZ.DEV Skills" | **PixzFlow** operating layer (PIXZ.DEV = brand) | Mission §0; consistent identity |
| Entry point | AGENTS.md as "agent registry" (162 lines incl. 28-row skill table) | AGENTS.md as **operating contract** (~160 lines, no duplicated tables; llms.txt carries the map) | AGENTS.md ecosystem: ≤150 lines recommended, 32 KiB Codex cap, duplication hurts (research 1.1–1.5) |
| Workflow | 11-phase runtime enum (`schemas/workflow.schema.json`) | **State + transitions**: compact task-state schema; phases only optional narrative | Benchmark: native models already cycle understand/verify/recover — phase theater added 1.48× overhead on trivial tasks; research 7.8 |
| Orchestrator | aggregates 8 mandatory skills (10-node install) | aggregates **1** (verification = evidence floor; 4-node closure incl. transitive requires) | B≈B1, C≈A (skills alone ≈ no advantage); trivial-task overhead |
| Skills | installed = invoked; no activation state | **Persistent activation protocol** with 8-state lifecycle + compact state + reactivation conditions | Benchmark: availability ≠ invocation; T12 continuation amortization |
| Evidence | `evidence: [string]` in workflow schema | Typed findings + typed evidence ledger with `verified_against` (compact graph) | T11 source-of-record (n=2) promoted to protocol; claim-type taxonomy |
| Epistemics | 8-label taxonomy, no transitions | 11-type taxonomy + **explicit transitions** + confidence-with-basis | Mission §17; epistemic discipline as testable behavior |
| Challenger | intensity ≈ risk×uncertainty×impact | intensity ≈ risk×uncertainty×impact**×irreversibility** + **binding stop rule** | Mission §20; no debate loops (research 4.2) |
| Delegation | handoff fields in workflow schema | **Economics test** + `schemas/handoff.schema.json` + mandatory return + inspection + anti-delegation eval | OpenAI handoffs/guardrails pattern (research 4); Gemini no-recursion (5.2) |
| Context | acquisition order only | full lifecycle DISCOVER→…→RESTORE + PIN-before-compaction | Anthropic context engineering (3.3); Claude Code compaction re-injection (3.1) |
| Failure | escalation ladder | formal 9-step recovery ladder; each retry adds information; failures ledger with lesson | LH-Bench 70% recovery via verification feedback (7.3); LongCLI early-failure clustering (7.2) |
| State | workflow.json (phase-centric) | task-state.json (state-centric; checkpoint; resume protocol) | PRO-LONG state-as-log (7.4); YC-Bench goal drift (7.5) |
| Modes | only in super-z profile | **universal** operating modes (fast/balanced/deep/autonomous) + profile | Mission §9; benchmark T12 |
| Super Z profile | `profiles/super-z/PROFILE.md` | top-level **`ZAI.md`** (Level 2.5 overlay; discoverability) | Mission §15; benchmark discovery finding |
| Schemas | workflow.schema.json (11 phases) | task-state.schema.json + handoff.schema.json | Mission §34 (state/transition over phase) |
| Evals | 15 doc + 15 routing smoke | 15 doc + **23 behavioral** (incl. 8 new mechanism scenarios) + registry invariants + successor benchmark design | Mission §30–31 |
| Anti-slop | taxonomy + "diagnostic not dogmatic" | + explicit **"never slop merely because…"** list (verbose/abstract/animated/componentized/AI-generated/unconventional) | Mission §28 |

## Deleted / Reduced (explicit)

- `schemas/workflow.schema.json` — **deleted** (superseded by `task-state.schema.json`; migration: field mapping in `docs/versioning.md`).
- `profiles/super-z/PROFILE.md` — **deleted** (consolidated into top-level `ZAI.md`; contract preserved in `profiles/README.md`).
- Orchestrator mandatory aggregates: **8 → 1** (10-node install → 4-node closure).
- AGENTS.md 28-row discovery table: **removed** (lives in `llms.txt` — single source, no drift).
- "Phase" as a machine state: **retired** (kept as optional narrative labels only).
- Not deleted (kept deliberately): the four verification layers, dependency model + resolver, adapters, the 14 domain skills (unchanged), limits/caps.

## Anti-Patterns Guarded

- Skill explosion → taxonomy 7-criteria + anti-overengineering gate
- Recursive orchestration → cycle detection + depth caps + no sub-subagents
- Phase theater on trivial tasks → mode is upper tendency; budget invariant machine-checked
- Silent breaking change → SemVer + VERSION + channel
- Documentation drift → single source (`registry.json`) + `validate.py` cross-checks
- Context rot / compaction loss → PIN-before-compaction + restore-from-state
- Blind trust in subagents → mandatory structured return + inspection
- Decorative intelligence → observable-performance-only principle (docs/evaluation.md)
