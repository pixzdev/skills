# PixzFlow

> **PIXZ.DEV's agent operating workflow + persistent skill ecosystem.** A persistent, adaptive, **model-agnostic operating layer** for capable AI agents — it makes strong behavior more *consistent, persistent, inspectable, transferable, and recoverable*, while keeping trivial work cheap.

## What PixzFlow Is

Not a prompt bundle. Not a rigid checklist. PixzFlow is the **Level 2 operating layer** between a model's native intelligence and its runtime:

```
MODEL     provides intelligence        (Level 0 — native; cannot be replaced)
RUNTIME   provides execution           (Level 1 — tools, MCP, sandbox, subagents)
PIXZFLOW  provides operating discipline (Level 2 — AGENTS.md, modes, state, evidence, policies)
OVERLAYS  parameterize one runtime     (Level 2.5 — ZAI.md for Super Z / GLM / Z.AI Web)
SKILLS    provide specialized capability (Level 3 — 28 skills, stable IDs, dependency-aware)
AGENTS    provide specialized parallel capability (Level 4 — conditional, contract-bound)
STATE     provides continuity          (Level 5 — task-state files, findings, evidence, handoffs)
```

Full layer model + architecture delta (old→new): `docs/architecture.md`.

## Why It Exists

The GLM benchmark (record: `docs/benchmark/GLM-benchmark-findings.md`) measured native vs. PixzFlow under controlled conditions. Honest findings:

- **52/52 objective acceptance in both conditions** — the model already does basic engineering. Don't teach basics.
- **~+0.17 blind-grading delta** — real but small; don't oversell it.
- **~1.48× token overhead, worst on trivial tasks** — orchestration must have a budget.
- **B≈B1, C≈A** — skills *alone* created no measurable advantage.
- **Skills weren't discovered natively, but were used when made explicit** — availability ≠ invocation.
- **T11 (source-of-record): n=2** — the strongest narrow differentiator; now a formal protocol, pending n≥5 replication.

So PixzFlow 2.0's job is not "more skills". It is: **adaptive capability activation + persistent state + evidence discipline + verification + runtime-aware execution**, sized to the task.

## The Operating Model

`AGENTS.md` is the **canonical operating contract** (high authority, high signal, no duplicated tables). The loop is state + transitions, not phases:

```
ORIENT → MODEL → ASSESS → MODE → PLAN → ACT → OBSERVE → VERIFY → DECIDE
                                                        ├── done · continue · replan
                                                        └── delegate · research · challenge · escalate · stop
```

- **Modes** (behavioral, not labels): `fast` · `balanced` · `deep` · `autonomous` — user instruction > runtime overlay > balanced default. A mode is an *upper tendency*, never a minimum ceremony: a deep-mode agent still runs a trivial rename fast.
- **Assessment**: qualitative bands (low/medium/high/critical) over complexity, risk, uncertainty, reversibility, horizon — driving plan size, activation count, delegation, verification depth.
- **Capability activation** (persistent): `DISCOVER → MATCH → LOAD (progressive) → ACTIVATE → USE → VERIFY → PERSIST → REINVOKE → COMPLETE`. Skills are persistent capabilities, not one-time prompt attachments; activation state (with reactivation conditions) survives phase transitions in task-state.
- **Evidence discipline**: typed claims (`fact · observed · source_claim · inference · assumption · hypothesis · unknown · unverified · contradicted · verified · falsified`) with explicit transitions; compact evidence ledger; **source-of-record rule** — actual artifacts beat descriptive records.
- **State & continuity**: one compact file per task (`schemas/task-state.schema.json`, default `.pixz/task-state.json`), checkpointed, with a deterministic resume protocol — survives compaction, session restart, subagent handoff, model change, runtime change.
- **Verification as a loop**: before irreversible action · after significant mutation · before claims · before handoff · before completion.
- **Delegation with economics**: only when `information gain + parallelism + specialization > coordination cost`; mandatory structured returns; parent inspects; no "looks good"; no sub-subagents. Restraint is a first-class eval.

## Architecture

| Artifact | Role |
|----------|------|
| `AGENTS.md` | Canonical operating contract (the entry point for agents) |
| `registry.json` | Machine source of truth — capabilities, dependencies, limits, protocols, policies |
| `llms.txt` | LLM map (capability projection) |
| `ZAI.md` | Runtime overlay: Super Z / GLM / Z.AI Web (mode ritual + compute policy; isolation contract in `profiles/README.md`) |
| `<domain>/<skill>/SKILL.md` + `metadata.yaml` | Capabilities (28; stable `pixz.<domain>.<name>` IDs) |
| `schemas/` | `task-state` · `handoff` · `skill` · `registry` · `eval` |
| `scripts/` | `validate.py` · `check-cycles.py` · `resolve.py` · `integration-smoke.sh` |
| `evals/` | Layer 2 documentary (15) + Layer 3 behavioral (23 + registry invariants) |
| `adapters/` | Thin runtime translators (claude, openclaw, opencode, hermes) |
| `agents/` | Orchestrator + specialist role contracts |
| `docs/` | Architecture, routing, evaluation, install matrix, benchmark, research |

## Skill Ecosystem

28 skills, stable IDs, dependency-aware: 13 core (orchestrator, planning, context-engineering, environment-awareness, capability-discovery, workflow-continuity, delegation-handoff, epistemic-reasoning, epistemic-challenger, verification, change-safety, replanning, quality-gate) + 15 domain (quality, engineering, security, design, frontend, motion, devops, ai).

**2.0.0 graph change:** the orchestrator's mandatory aggregate is now just `pixz.core.verification` (the evidence floor) — a 4-node install closure (was 10). The other core capabilities are **activated at runtime** by the capability-activation protocol, not force-installed. Evidence: benchmark skill-marginality + trivial-task overhead. Full map: `llms.txt` (projection of `registry.json`).

## Runtime Overlays

An overlay is a runtime-specific POLICY — **not a skill**, not in `registry.json`, never changes universal semantics. Currently one exists:

- **Super Z / GLM / Z.AI Web → `ZAI.md`** (top-level). Mandatory `AskUserQuestion` operating-mode selection before substantive work (Fast / Balanced / Deep / Autonomous; default Balanced); mode semantics; compute policy ("generous compute is not permission to waste compute"); graceful degradation when the question tool is absent. Status: **SPECIFIED**; behavioral effect **UNVERIFIED** — no behavioral evaluation exists yet. Contract: `profiles/README.md`.

## Install — Source ≠ Install

Cloning gives **source**. Installation registers capabilities where the runtime discovers them.

```bash
# skills.sh — any agent with `npx skills` (VERIFIED)
npx skills add pixzdev/skills --list
npx skills add pixzdev/skills --skill orchestrator
npx skills list

# Claude Code — VERIFIED
npx skills add pixzdev/skills --skill orchestrator --agent claude-code
# or manual project: cp -r core/orchestrator/* .claude/skills/orchestrator/

# OpenClaw — VERIFIED
openclaw skills install ./core/orchestrator --as pixz-orchestrator

# OpenCode — VERIFIED (singular `skill`)
mkdir -p .opencode/skill/orchestrator && cp -r core/orchestrator/* .opencode/skill/orchestrator/

# Hermes — VERIFIED
mkdir -p ~/.hermes/skills/orchestrator && cp -r core/orchestrator/* ~/.hermes/skills/orchestrator/

# Generic (Codex/Cursor) — PARTIALLY VERIFIED
mkdir -p .agents/skills/orchestrator && cp -r core/orchestrator/* .agents/skills/orchestrator/

# Full ecosystem — all 28 skills at once (skills.sh)
npx skills add pixzdev/skills
```

**Source checkout (development):**
```bash
git clone https://github.com/pixzdev/skills.git
python scripts/validate.py && python scripts/check-cycles.py && python evals/runner.py && python evals/behavioral/runner.py
```

Full matrix (VERIFIED vs PARTIALLY VERIFIED per runtime): `docs/install/README.md`.

> **Copy-paste prompts for agents:** see **AI Agent Installation Prompt** and **Super Z / GLM / Z.AI Web Install & Activation Prompt** below. Full runtime-adaptive version: `docs/prompts/install-skill-agent.md`; short version: `docs/install-as-skill.md`.

## AI Agent Installation Prompt

Copy-paste the block below into any AI agent (Claude Code, OpenClaw, OpenCode, Hermes, Cursor, Codex, or any Agent Skills runtime). It is runtime-agnostic — the agent detects its own environment and uses the repository's official mechanisms.

```markdown
You are installing PixzFlow (PIXZ.DEV) capabilities into the CURRENT AI agent runtime — not cloning a repository, not reading documentation for its own sake.

Repo: https://github.com/pixzdev/skills (machine source of truth: registry.json).

1. INSPECT ENVIRONMENT — probe, do not assume:
   - Paths: ls -la ~/.claude/skills .claude/skills .opencode/skill ~/.config/opencode/skill ~/.hermes/skills .agents/skills ./skills
   - CLIs: npx skills --help; openclaw --help; opencode --help; hermes --help; claude --version (report whichever succeed)
   - OS, git state, package manager, write permission to the intended install path. If something blocks installation, report it before acting.
2. LOCATE PIXZFLOW — obtain the source once (git clone https://github.com/pixzdev/skills /tmp/pixz is fine). Read AGENTS.md (operating contract), registry.json (capabilities), and docs/install/README.md (official install matrix).
3. INSPECT COMPATIBILITY — for your detected runtime, confirm the official mechanism from that matrix (skills.sh CLI, openclaw skills install, or the adapter's copy path in adapters/). Use the repository's runtime adapter — do NOT invent a new skill format. Preserve existing user configuration: never overwrite an existing skill of the same name; if one exists, stop and report it.
4. RESOLVE DEPENDENCIES — if the requested capability declares requires/aggregates, resolve the full set first:
   python3 /tmp/pixz/scripts/resolve.py --install <skill-id> --runtime <detected>
   (Add --with-optional only if the user asked for the full capability set.) Default capability if none was requested: pixz.core.orchestrator (resolves to 4 nodes; 14 with --with-optional).
5. INSTALL — execute exactly ONE install mechanism per capability in resolved order and capture command, exit code, and output. Cloning is NOT installation.
6. VERIFY INSTALLATION — mandatory and evidence-based: the runtime's discovery command must show each capability at its installed location:
   - skills.sh: npx skills list
   - OpenClaw: openclaw skills list (+ openclaw skills check)
   - Others: ls <installed path>/SKILL.md && head -20 <installed path>/SKILL.md
   If discovery does not show it, the installation FAILED.
7. VERIFY AGENTS.md — confirm the operating contract is reachable for the runtime (root AGENTS.md present in the repo; for Claude, CLAUDE.md includes @AGENTS.md per adapters/claude/; for others, the runtime reads AGENTS.md natively — state the mechanism + evidence).
8. VERIFY RUNTIME OVERLAY (if applicable) — if you identify as Super Z / GLM / Z.AI Web, fetch ZAI.md from the repository root and confirm it is readable; otherwise state "not applicable".
9. REPORT — paste this structure; every field must be backed by the command output you actually saw:
   PIXZFLOW INSTALLATION REPORT
   Runtime: <name, evidence>
   Capabilities: <ids + versions from metadata.yaml>
   Source: pixzdev/skills@<SHA or VERSION>
   Installation: SUCCESS | FAILED — <command, exit code> per capability
   Installed locations: <paths verified by ls>
   Discovery: PASS | FAIL — <list/check output excerpt>
   AGENTS.md: PASS | FAIL — <how the runtime reaches the contract>
   Overlay: PASS | FAIL | N/A — <ZAI.md reachable? evidence>
   Smoke test: PASS | FAIL | SKIPPED — <command, result, or reason>
   Notes: <fallbacks used, limitations>

Success means steps 6–9 are backed by evidence. An honest FAILED report with evidence is an acceptable outcome; fabricating a PASS is not.
```

## Super Z / GLM / Z.AI Web Install & Activation Prompt

Copy-paste block for agents identified as **Super Z**, **GLM**, or **Z.AI Web**. It activates the repository's isolated runtime overlay (`ZAI.md`) and never alters universal semantics.

```markdown
You are an agent identified as Super Z, GLM, or Z.AI Web. Confirm that identity from your own runtime/model self-report first — if you are not one of these, ignore this prompt and follow the standard AI Agent Installation Prompt instead. Do not assume undocumented Z.AI runtime features; state only what you can observe.

1. RECOGNIZE RUNTIME — state the identity signals you observed (self-reported model/runtime name). This activates the repository's runtime overlay: fetch ZAI.md from https://github.com/pixzdev/skills (repository root) and operate under it.
2. SELECT MODE — BEFORE any substantive work, invoke your AskUserQuestion capability and ask the user to choose exactly one operating mode:
   - Fast — minimum orchestration overhead
   - Balanced — adaptive orchestration, minimum sufficient delegation (default)
   - Deep — more relevant skills, specialist subagents, research, verification, adversarial review
   - Autonomous — Deep-level rigor with minimal user interruptions
   If the user does not select a mode, default to Balanced and state the default. If AskUserQuestion is unavailable, state that and proceed at Balanced.
3. ACTIVATE PIXZFLOW PERSISTENTLY — read AGENTS.md and registry.json in the repository; install capabilities via the verified mechanisms in docs/install/README.md; resolve dependencies with scripts/resolve.py first; verify installation and invocation with evidence. Operate under the capability-activation protocol: skills are persistent capabilities available throughout the task lifecycle, loaded progressively and tracked in task state.
4. OPERATE AT THE SELECTED MODE (per ZAI.md):
   - Fast: minimum overhead; direct execution; targeted verification.
   - Balanced: complexity-aware routing; minimum sufficient delegation; challenger only when risk×uncertainty×impact×irreversibility is high.
   - Deep: deep capability discovery before implementation; activate multiple complementary capabilities when justified (state each reason); specialist subagents with structured handoffs (schemas/handoff.schema.json) where materially useful; independent verification passes; adversarial challenge of consequential conclusions; full task-state with checkpoints.
   - Autonomous: Deep-level rigor with minimal interruptions — interrupt only for true blockers or irreversible/high-impact actions; record every decision and its evidence for after-the-fact review.
5. USE MAXIMUM USEFUL COMPUTE — your runtime's generous compute is not permission to waste compute. Dynamically load capabilities as the task demands; parallelize only independent work; keep state persistent; perform deeper verification at Deep/Autonomous. Objective: MAXIMUM USEFUL INTELLIGENCE, not MAXIMUM ACTIVITY.
6. AVOID UNNECESSARY ORCHESTRATION — never invoke every capability automatically; never spawn subagents without an independent responsibility; never research trivial facts that local inspection answers; never add ceremony to trivial changes; never repeat verification with no new information; no recursive orchestration; stop at justified stop conditions.
7. NEVER OVERRIDE — regardless of mode: universal skill semantics; dependency resolution; confirmation for irreversible/high-impact actions; verification triggers; source-of-record discipline; honest OBSERVED/SPECIFIED/INFERRED/UNKNOWN reporting.
8. REPORT — state the mode in use, capabilities activated (with reasons), and the evidence for each installation step (per the standard report format).
```

## Persistence & State

- Task state: `.pixz/task-state.json` per task (schema: `schemas/task-state.schema.json`) — objective, acceptance criteria, assessment, plan, **decisions (marked, never deleted)**, typed **findings**, **evidence ledger** (`verified_against`), **capability activation state** (with reactivation conditions), failures (with lessons), verification, `next_action`, checkpoint.
- Checkpoints: before long substeps, before irreversible actions, at phase boundaries.
- Resume protocol: read state → restate objective → honor `next_action` → re-establish active capabilities → check stale assumptions → continue.
- The state file is the **continuity substrate**: conversation is lossy (compaction, restarts, model/runtime changes); a well-formed state file survives all of them.

## Verification

| Layer | Harness | What it proves |
|-------|---------|----------------|
| 1 Structural | `scripts/validate.py` + `check-cycles.py` | registry/metadata/schemas consistent; no cycles; ZAI.md + README contracts; 2.0 migration guard |
| 2 Documentary | `evals/runner.py` (15, heuristic) | skills document required sections |
| 3 Behavioral | `evals/behavioral/runner.py` (23 + registry invariants) | routing smoke + evidence floor + trivial-task budget + mode consistency (heuristic, not model-graded) |
| 4 Integration | `scripts/integration-smoke.sh` | installer → discovery → invocation where runtimes exist |

Layers never imply each other: a passing structural check is **not** behavioral proof. Model-graded behavioral measurement (activation precision/recall, persistence, continuation, evidence quality, recovery, restraint, efficiency) is the **successor benchmark** — `docs/benchmark/successor-benchmark.md` (ablation cells A–H; cells report UNRUN until executed).

```bash
python scripts/validate.py
python scripts/check-cycles.py
python evals/runner.py
python evals/behavioral/runner.py
bash scripts/integration-smoke.sh
```

## Portability

- **Model-agnostic:** no assumption that a model is weak, and none that it is perfectly disciplined. PixzFlow provides the missing operating structure while letting capable models exercise native intelligence.
- **Runtime-aware:** adapters for claude / openclaw / opencode / hermes; generic path for Codex/Cursor-class. Classification stays honest: **VERIFIED** (docs + CLI/ls evidence) vs **PARTIALLY VERIFIED** vs **Unsupported**.
- **No undocumented vendor assumptions:** every architectural claim is classified (verified / documented / observed / inferred / hypothesis / unknown) — see `docs/research/frontier-agent-findings.md`.

## Limitations (honest)

- `pinned` channel (`pixz.lock`) is **documented future** — `stable`/`latest` work; `pinned` accepts the flag but writes no lockfile.
- Behavioral eval is heuristic smoke — **not** model-graded; the successor benchmark is designed but its cells are **UNRUN**.
- `ZAI.md` overlay is **SPECIFIED**; behavioral effect **UNVERIFIED**.
- Generic runtime is **partially verified** (spec exists, no CI smoke).
- Installation needs `npx` (Node 18+) or manual `cp -r`; offline/hermetic envs use manual copy.
- No hosted skill marketplace yet — install via `skills.sh` CLI or manual copy.

## Contributing

See `CONTRIBUTING.md` (taxonomy gate, folder contract, anti-overengineering gate, validation checklist, PR process). New capability must pass the seven standalone criteria — or it's a protocol/policy/doc, not a skill.

## License

MIT — `LICENSE`.

---

*Build the system, not the deck. Optimize for observable agent performance — a shorter workflow that produces better outcomes beats a sophisticated workflow that merely sounds intelligent.*
