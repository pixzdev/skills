# PixzFlow

[![PIXZ.DEV PRODUCTION views](https://pixz.dev/badge/custom.svg?order=logo,brand,text,views&text=PRODUCTION&style=flat&bg=wave)](https://pixz.dev)

> **The persistent, adaptive, model-agnostic operating layer for capable AI agents.**
> Installation → detection → orientation → learning → adaptation — without pasting a self-training prompt every session.

PIXZ.DEV is the brand; **PixzFlow** is the system. It does not teach frontier models basic engineering and does not replace native capability — it makes strong behavior more **consistent, persistent, inspectable, transferable, and recoverable**, while keeping trivial work cheap.

---

## What is PixzFlow?

A Level-2 operating layer between a model's native intelligence and its runtime:

```
MODEL     intelligence            (L0 — native, cannot be replaced)
RUNTIME   execution               (L1 — tools, MCP, sandbox, subagents)
PIXZFLOW  operating discipline    (L2 — AGENTS.md, modes, state, evidence, policies)
OVERLAYS  one-runtime parameters  (L2.5 — ZAI.md for Super Z / GLM / Z.AI Web)
SKILLS    specialized capability  (L3 — 29 skills, stable IDs, dependency-aware)
AGENTS    parallel specialization (L4 — contract-bound subagent roles)
STATE     continuity              (L5 — task-state + adaptation-state + evidence)
```

| Artifact | Role |
|---|---|
| `AGENTS.md` | Canonical operating contract (agent entry point) |
| `registry.json` | Machine source of truth — skills, protocols, policies, limits |
| `llms.txt` | LLM map (projection of the registry) |
| `schemas/` | `task-state` · `adaptation-state` · `handoff` · `skill` · `registry` · `eval` |
| `scripts/` | `validate.py` · `check-cycles.py` · `resolve.py` · `activation.py` (incl. `verify-installed`) · `doctor.py` · `assess.py` · `sitrep.py` · `hooks.py` · `integration-smoke.sh` |
| `evals/` | documentary (19) + behavioral (33) + lifecycle (14) |
| `adapters/` | Thin runtime translators (claude, openclaw, opencode, hermes) |
| `core/` + domains | 14 core + 15 domain skills (`pixz.<domain>.<name>` IDs) |

## Why it exists

The GLM benchmark (`docs/benchmark/GLM-benchmark-findings.md`) measured native vs. PixzFlow honestly:

| Finding | Consequence |
|---|---|
| 52/52 acceptance in **both** conditions | Don't teach basics to strong models |
| ~+0.17 blind-grading delta | Real but small — don't oversell |
| ~1.48× token overhead, worst on trivial tasks | Orchestration must have a budget |
| Skills alone ≈ no advantage (B≈B1, C≈A) | Activation + state + evidence are the product, not "more skills" |
| Skills not discovered natively, used when explicit | **availability ≠ invocation** → post-install adaptation |
| Source-of-record strongest narrow signal (n=2) | Promoted to a formal protocol |

## Architecture

PixzFlow is **state + transitions + capabilities + evidence**, not a phase checklist:

```
ORIENT → MODEL → ASSESS → MODE → PLAN → ACT → OBSERVE → VERIFY → DECIDE
                                                     done · continue · replan
                                                     delegate · research · challenge · escalate · stop
```

- **Modes** `fast | balanced | deep | autonomous` — behavioral differences, not labels. A mode is an *upper tendency*, never a minimum ceremony: a deep-mode agent still runs a trivial rename fast.
- **Assessment bands** (low/medium/high/critical) over complexity · risk · uncertainty · reversibility · horizon drive plan size, activation count, delegation, verification depth, challenge intensity.
- **Evidence discipline** — typed claims (`fact · observed · assumption · hypothesis · verified · falsified …`) with explicit transitions; source-of-record rule: actual artifacts beat descriptive records.

## Self-learning lifecycle

After installation, PixzFlow does not wait for the user to paste a training prompt. The contract (`AGENTS.md`) is read by participating runtimes at session start and contains the activation protocol; the state survives in files.

```
INSTALL → DETECT → INVENTORY → BASELINE → ADAPT → VERIFY → PERSIST → READY
                                                                       │
        OPERATE ← VERIFY ← ADAPT(re-delta) ← DRIFT CHECK ←────────────┘
          │
          └─ OBSERVE → DIAGNOSE → CHALLENGE → IMPROVE → VERIFY → REGRESS → PERSIST → REUSE ↺
```

Five distinct states — never conflated, never claimed out of order:

| State | Meaning | Machine evidence |
|---|---|---|
| **Installation** | capabilities available | discovery listing shows them |
| **Activation** | agent can invoke them | runtime invocation observed |
| **Adaptation** | working behavior changed | RUNTIME-ACTIVE verification + probe READY |
| **Learning** | reusable lessons extracted | `learning.lessons[]` with origin + status |
| **Improvement** | verified mechanisms/tests/procedures | `learning.improvements[]` = `verified` + regression check |

Mechanism: `pixz.core.self-learning` + `scripts/activation.py` (probe exit codes: `0` ready · `10` new/stale · `1` error) + `.pixz/adaptation-state.json` (`schemas/adaptation-state.schema.json`). Skill-version change never assumes behavior change — the delta is inspected and only the changed capabilities are re-adapted. This is behavioral/runtime adaptation: **no model weights are modified**; learning is evidence-driven; persistent changes require verification; unsupported capabilities remain UNKNOWN rather than invented.

Supporting tooling (all stdlib-only):

| Tool | Purpose |
|---|---|
| `scripts/doctor.py` | **measures** the baseline (state persistence, command execution, tools, contract reachability) instead of self-reporting; `--write` fills only `unknown` dimensions |
| `scripts/assess.py` | adoption score 0–100 = sum of named evidence-backed checks (each PASS/FAIL; UNVERIFIED scores 0). **Auto-runs after `mark-adapted`.** Not a quality metric |
| `scripts/sitrep.py` | one-block orientation report (adaptation + task + learning) for ORIENT/compaction/handoff |
| `scripts/hooks.py` | runtime contract wiring (`check`/`install`, idempotent; Claude `CLAUDE.md → @AGENTS.md`, native runtimes no-op) |
| `activation.py verify-installed` | integrity: installed copies vs source digests (tamper/corruption detection) |

## Persistent state

| File | Scope | Survives |
|---|---|---|
| `.pixz/task-state.json` | one task: objective, plan, decisions (marked, never deleted), typed findings, evidence ledger, capability activation, failures+lessons, `next_action` | compaction · restart · handoff · model change · runtime change |
| `.pixz/adaptation-state.json` | runtime ↔ PixzFlow: baseline, digested inventory (drift detector), adaptation status+evidence, learning ledger | same boundaries; read at session start |

Entries are summaries + references — never transcripts, never hidden chain-of-thought.

## Capability system

29 skills, stable `pixz.<domain>.<name>` IDs, dependency-aware (`requires` / `aggregates` / `optional` / `conflicts`). 14 core: orchestrator, planning, context-engineering, environment-awareness, capability-discovery, workflow-continuity, delegation-handoff, epistemic-reasoning, epistemic-challenger, verification, change-safety, replanning, quality-gate, **self-learning**. 15 domain: quality, engineering, security, design, frontend, motion, devops, ai.

**Main skill:** `pixz.core.orchestrator` is the practical operating skill. Specialist skills answer HOW. If you want more practical multi-step methodology, activate the orchestrator; load `core/orchestrator/references/operating-methodology.md` when the work is complex.

```
DISCOVER (metadata only) → MATCH → LOAD (progressive) → ACTIVATE → USE → VERIFY → PERSIST → REINVOKE → COMPLETE
```

Budget rule: every activation earns its context cost. The orchestrator's mandatory closure is 4 nodes (the evidence floor: orchestrator → verification → epistemic-reasoning → context-engineering); everything else activates on demand. Resolver: `python scripts/resolve.py --install pixz.core.orchestrator --runtime claude` → 4 nodes (15 with `--with-optional`).

## Evidence + verification

**Verification depth must match the claim** (`pixz.protocol.verification-depth`):

| Claim | Minimum depth |
|---|---|
| EXISTS | existence check |
| PARSES | parser |
| SCHEMA-COMPLIANT | schema validation |
| CORRECT | behavioral verification |
| INTEGRATED | integration test |
| RUNTIME-ACTIVE | runtime invocation |
| PERSISTENT | repeated/delayed observation |
| IMPROVED | baseline comparison |

Never: `file exists = valid` · `command succeeded = correct` · `test passed = requirement satisfied` · `agent said success = verified`.

| Layer | Harness | Proves |
|---|---|---|
| 1 Structural | `scripts/validate.py` + `check-cycles.py` | registry/metadata/schemas consistent; contracts hold |
| 2 Documentary | `evals/runner.py` (19, heuristic) | skills document required methodology |
| 3 Behavioral | `evals/behavioral/runner.py` (33 + invariants, heuristic) | routing/activation smoke, evidence floor, trivial-task budget, mode consistency |
| 3b Lifecycle | `evals/lifecycle/run_tests.py` (14, deterministic) | self-learning state machine + 2.2 tooling: activation, reload, drift, failed adaptation, regression, doctor, integrity, sitrep, assessment, hooks |
| 4 Integration | `scripts/integration-smoke.sh` | installer → discovery → invocation where runtimes exist |

## Adaptive complexity

Self-improvement must not cause process inflation. Process depth scales with the assessment bands; self-improvement itself is costed against reliability gain vs token cost, latency, tool calls, context consumption and permanent complexity. **Anti-proliferation gate:** a failure must not spawn a new skill/agent/protocol/schema/instruction file/dependency unless existing mechanisms cannot express the fix, the failure class recurs, the benefit justifies permanent cost, and the result is testable. Prefer: policy → extend existing mechanism → new test → (last) new abstraction. A mechanism that improves one edge case while making every trivial task worse is rejected or redesigned.

## Delegation

Only when `information gain + parallelism + specialization > coordination cost`. Structured dispatch + mandatory structured return (`schemas/handoff.schema.json`); the parent inspects — no "looks good" returns; subagents never spawn subagents. Restraint is evaluated (anti-delegation scenario).

## Runtime overlays

An overlay parameterizes one runtime without changing universal semantics. Currently: **`ZAI.md`** (Super Z / GLM / Z.AI Web) — mandatory mode-selection ritual + compute policy. Status: SPECIFIED; behavioral effect UNVERIFIED.

## Installation

Installation is **not** the end of the process:

```
INSTALL → VALIDATE → ACTIVATE → SELF-TRAIN → VERIFY → READY
```

```bash
# skills.sh — any agent with `npx skills` (VERIFIED)
npx skills add pixzdev/skills --skill orchestrator        # one capability
npx skills add pixzdev/skills                              # full ecosystem (29 skills)

# Claude Code (VERIFIED)
npx skills add pixzdev/skills --skill orchestrator --agent claude-code

# OpenClaw (VERIFIED)
openclaw skills install ./core/orchestrator --as pixz-orchestrator

# OpenCode (VERIFIED, singular `skill`)
mkdir -p .opencode/skill/orchestrator && cp -r core/orchestrator/* .opencode/skill/orchestrator/

# Hermes (VERIFIED)
mkdir -p ~/.hermes/skills/orchestrator && cp -r core/orchestrator/* ~/.hermes/skills/orchestrator/

# Generic — Codex/Cursor class (PARTIALLY VERIFIED)
mkdir -p .agents/skills/orchestrator && cp -r core/orchestrator/* .agents/skills/orchestrator/
```

**Source checkout (development):**

```bash
git clone https://github.com/pixzdev/skills.git
python scripts/validate.py && python scripts/check-cycles.py
python evals/runner.py && python evals/behavioral/runner.py && python evals/lifecycle/run_tests.py
```

Full matrix with evidence per runtime: `docs/install/README.md`.

## Post-install activation

What happens after installation — and why it survives sessions:

1. **VALIDATE** — the runtime's discovery command shows each capability at its install location; discovery output is the evidence, not the clone. Optionally check integrity of installed copies: `activation.py verify-installed --runtime <rt>`.
2. **ACTIVATE + SELF-TRAIN** — `python3 scripts/doctor.py --write` measures the baseline; `python3 scripts/activation.py init --runtime <detected>` records inventory (with content digests) + dimensions; the agent adapts its working behavior per `AGENTS.md` (entry protocol, modes, evidence rules, verification triggers, delegation constraints); wire the contract if needed (`scripts/hooks.py install --runtime <rt>`).
3. **VERIFY** — adaptation is a RUNTIME-ACTIVE claim: run the validation layers, invoke a real capability, show the probe transitions. Then `python3 scripts/activation.py mark-adapted --evidence "<observed>"` — refused without evidence — which **automatically runs the adoption assessment** (score 0–100, named checks).
4. **READY** — every later session probes once (`activation.py status`): `ready` + no drift → work immediately (`scripts/sitrep.py` for the one-block report). Version/content drift → inspect the actual delta, re-adapt only what changed (`sync` → `mark-adapted`).

No self-training prompt needs to be pasted again: the trigger lives in `AGENTS.md` (read at session start), the state lives in `.pixz/adaptation-state.json`.

## Supported runtimes

| Runtime | Mechanism | Status |
|---|---|---|
| Claude Code | `.claude/skills/`, `CLAUDE.md` → `@AGENTS.md` import | VERIFIED |
| OpenClaw | `openclaw skills install`, allowlist | VERIFIED |
| OpenCode | `.opencode/skill/` | VERIFIED |
| Hermes | `~/.hermes/skills/` | VERIFIED |
| Codex / Cursor / generic | `AGENTS.md` + `SKILL.md` copies | PARTIALLY VERIFIED |
| Super Z / GLM / Z.AI Web | overlay `ZAI.md` | SPECIFIED (behavior UNVERIFIED) |

## Repository structure

```
AGENTS.md · ZAI.md · llms.txt · registry.json · VERSION
core/<skill>/SKILL.md + metadata.yaml     # 14 core capabilities
<domain>/<skill>/…                        # 15 domain capabilities
schemas/                                  # task-state, adaptation-state, handoff, skill, registry, eval
scripts/                                  # validate, check-cycles, resolve, activation, integration-smoke
evals/cases · evals/behavioral · evals/lifecycle
adapters/{claude,openclaw,opencode,hermes} · agents/ · profiles/
docs/                                     # architecture, evaluation, taxonomy, install matrix, research, benchmark
```

## Evaluation

See `docs/evaluation.md`. Per-layer results, never cross-layer inflation: structural PASS/FAIL · documentary `X/19 heuristic` · behavioral `X/33` + invariants · lifecycle `X/14 deterministic` · integration PASS/FAIL per runtime. The behavioral E-series covers: first activation · existing runtime (no duplicate setup) · skill upgrade · failed assumption · self-improvement · anti-overengineering · regression · persistence · validation depth · contradictory evidence · trivial-task budget · high-risk escalation.

## Benchmarks

- **GLM benchmark (run, recorded):** 52/52 both conditions; ~+0.17 blind delta; ~1.48× token overhead; B≈B1, C≈A; T11 source-of-record n=2. See `docs/benchmark/GLM-benchmark-findings.md`.
- **Successor benchmark (designed, UNRUN):** model-graded ablation cells A–H including self-learning effect (`docs/benchmark/successor-benchmark.md`). This repo never fabricates results — unrun cells say UNRUN.

## Limitations (honest)

- Behavioral eval is heuristic smoke + deterministic state-machine tests — **not** model-graded; successor benchmark cells are UNRUN.
- `ZAI.md` overlay: SPECIFIED; behavioral effect UNVERIFIED.
- `pinned` channel (`pixz.lock`): documented future — resolver accepts the flag, writes no lockfile.
- Generic runtime: PARTIALLY VERIFIED (spec exists, no CI smoke).
- Install needs `npx` (Node 18+) or manual `cp -r`; no hosted marketplace yet.
- Self-learning improves *operating behavior via files and protocol* — it cannot and does not modify model weights; measured task-quality gain is HYPOTHESIS until the ablation runs.

## Development

```bash
python scripts/validate.py            # registry/metadata/schemas/consistency + contracts
python scripts/check-cycles.py        # dependency graph acyclic
python evals/runner.py                # layer 2 documentary
python evals/behavioral/runner.py     # layer 3 behavioral smoke
python evals/lifecycle/run_tests.py   # layer 3b self-learning lifecycle
bash scripts/integration-smoke.sh     # layer 4 integration
```

New capabilities pass the seven standalone criteria + anti-overengineering gate (`docs/taxonomy.md`) — or they are protocols/policies/docs, not skills.

## Versioning

`VERSION` (repo) + per-skill SemVer in the same commit; channels `latest` / `stable` / `pinned` (documented future). Breaking changes require a major bump; deprecation keeps one major of runway. See `docs/versioning.md`.

## Contributing

`CONTRIBUTING.md` — taxonomy gate, folder contract, validation checklist, PR process. Keep `registry.json` as the single machine truth and `llms.txt` its projection — never a third copy.

## License

MIT — `LICENSE`.

---

## AI Agent Installation Prompt

Copy-paste the block below into any AI agent (Claude Code, OpenClaw, OpenCode, Hermes, Cursor, Codex, or any Agent Skills runtime). It is runtime-agnostic — the agent detects its own environment and uses the repository's official mechanisms.

```markdown
You are installing PixzFlow (PIXZ.DEV) capabilities into the CURRENT AI agent runtime — not cloning a repository, not reading documentation for its own sake. Installation is only the first step: after installing you must ACTIVATE and SELF-TRAIN per steps 10–11.

Repo: https://github.com/pixzdev/skills (machine source of truth: registry.json).

1. INSPECT ENVIRONMENT — probe, do not assume:
   - Paths: ls -la ~/.claude/skills .claude/skills .opencode/skill ~/.config/opencode/skill ~/.hermes/skills .agents/skills ./skills
   - CLIs: npx skills --help; openclaw --help; opencode --help; hermes --help; claude --version (report whichever succeed)
   - OS, git state, package manager, write permission to the intended install path. If something blocks installation, report it before acting.
2. LOCATE PIXZFLOW — obtain the source once (git clone https://github.com/pixzdev/skills /tmp/pixz is fine). Read AGENTS.md (operating contract), registry.json (capabilities), and docs/install/README.md (official install matrix).
3. INSPECT COMPATIBILITY — for your detected runtime, confirm the official mechanism from that matrix (skills.sh CLI, openclaw skills install, or the adapter's copy path in adapters/). Use the repository's runtime adapter — do NOT invent a new skill format. Preserve existing user configuration: never overwrite an existing skill of the same name; if one exists, stop and report it.
4. RESOLVE DEPENDENCIES — if the requested capability declares requires/aggregates, resolve the full set first:
   python3 /tmp/pixz/scripts/resolve.py --install <skill-id> --runtime <detected>
   (Add --with-optional only if the user asked for the full capability set.) Default capability if none was requested: pixz.core.orchestrator (resolves to 4 nodes; 15 with --with-optional).
5. INSTALL — execute exactly ONE install mechanism per capability in resolved order and capture command, exit code, and output. Cloning is NOT installation.
6. VERIFY INSTALLATION — mandatory and evidence-based: the runtime's discovery command must show each capability at its installed location:
   - skills.sh: npx skills list
   - OpenClaw: openclaw skills list (+ openclaw skills check)
   - Others: ls <installed path>/SKILL.md && head -20 <installed path>/SKILL.md
   If discovery does not show it, the installation FAILED.
7. VERIFY AGENTS.md — confirm the operating contract is reachable for the runtime (root AGENTS.md present in the repo; for Claude, CLAUDE.md includes @AGENTS.md per adapters/claude/; for others, the runtime reads AGENTS.md natively — state the mechanism + evidence).
8. VERIFY RUNTIME OVERLAY (if applicable) — if you identify as Super Z / GLM / Z.AI Web, fetch ZAI.md from the repository root and confirm it is readable; otherwise state "not applicable".
9. REPORT INSTALLATION — every field backed by command output you actually saw:
   PIXZFLOW INSTALLATION REPORT
   Runtime: <name, evidence>
   Capabilities: <ids + versions from metadata.yaml>
   Source: pixzdev/skills@<SHA or VERSION>
   Installation: SUCCESS | FAILED — <command, exit code> per capability
   Installed locations: <paths verified by ls>
   Discovery: PASS | FAIL — <list/check output excerpt>
   AGENTS.md: PASS | FAIL — <how the runtime reaches the contract>
   Overlay: PASS | FAIL | N/A — <ZAI.md reachable? evidence>
10. ACTIVATE + SELF-TRAIN (post-install lifecycle — do not skip):
   - Probe first: python3 scripts/activation.py status   (if STATE=READY and no drift, skip to step 12 report — do NOT duplicate setup)
   - Measure the baseline: python3 scripts/doctor.py --write  (measures state persistence, command execution, tools, contract reachability; fills only unknown dimensions — what it cannot measure stays unknown, never invented). Wire the contract if the runtime needs it: python3 scripts/hooks.py install --runtime <detected>
   - First activation: python3 scripts/activation.py init --runtime <detected> --source pixzdev/skills@<sha> --dim delegation=<yes|no|unknown> --dim research=<yes|no|unknown> (record only OBSERVED dimensions; delegation/research are not locally measurable — the agent records them from runtime self-report)
   - Adapt your working behavior to AGENTS.md (entry protocol, modes, evidence rules, verification triggers, delegation constraints, capability-activation protocol, stopping rules).
   - VERIFY the adaptation at RUNTIME-ACTIVE depth (run the repo validation layers where the source is available; invoke one real capability; show the probe transition), then: python3 scripts/activation.py mark-adapted --evidence "<what you actually observed>". This command refuses without evidence — "I have learned PixzFlow" is not evidence.
11. ADOPTION ASSESSMENT (automatic) — mark-adapted auto-runs scripts/assess.py and prints an adoption score 0–100. The score is a sum of named evidence-backed checks (each PASS/FAIL; UNVERIFIED items score 0; gaps listed) — it is NOT a model-quality or workflow-effectiveness metric. Reproduce with python3 scripts/assess.py [--full]. If installed skill copies exist, also run python3 scripts/activation.py verify-installed --runtime <detected> and report any MODIFIED copies (inspect before trusting).
12. FINAL REPORT — append to the installation report:
   Activation: NEW->BASELINED->READY | ALREADY READY — <probe output>
   Adaptation evidence: <commands run + observed output>
   Baseline dimensions: <measured by doctor.py; unknowns listed, not invented>
   Adoption score: <N/100 + verdict, exactly as printed by the assessment; list the failing checks>
   Integrity: verify-installed PASS | MODIFIED(<ids>) | NOT RUN — <reason>
   Notes: <fallbacks used, limitations>

Success means steps 6–12 are backed by evidence. An honest FAILED report with evidence is an acceptable outcome; fabricating a PASS is not.
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
3. ACTIVATE PIXZFLOW PERSISTENTLY — read AGENTS.md and registry.json in the repository; install capabilities via the verified mechanisms in docs/install/README.md; resolve dependencies with scripts/resolve.py first; verify installation and invocation with evidence. Operate under the capability-activation protocol: skills are persistent capabilities available throughout the task lifecycle, loaded progressively and tracked in task state. Then run the post-install self-learning lifecycle (steps 10–12 of the standard prompt): measure the baseline via scripts/doctor.py, init via scripts/activation.py, adapt behavior, verify at RUNTIME-ACTIVE depth, mark-adapted with evidence (auto-runs the adoption assessment) — never duplicate an existing READY adaptation.
4. OPERATE AT THE SELECTED MODE (per ZAI.md):
   - Fast: minimum overhead; direct execution; targeted verification.
   - Balanced: complexity-aware routing; minimum sufficient delegation; challenger only when risk×uncertainty×impact×irreversibility is high.
   - Deep: deep capability discovery before implementation; activate multiple complementary capabilities when justified (state each reason); specialist subagents with structured handoffs (schemas/handoff.schema.json) where materially useful; independent verification passes; adversarial challenge of consequential conclusions; full task-state with checkpoints.
   - Autonomous: Deep-level rigor with minimal interruptions — interrupt only for true blockers or irreversible/high-impact actions; record every decision and its evidence for after-the-fact review.
5. USE MAXIMUM USEFUL COMPUTE — your runtime's generous compute is not permission to waste compute. Dynamically load capabilities as the task demands; parallelize only independent work; keep state persistent; perform deeper verification at Deep/Autonomous. Objective: MAXIMUM USEFUL INTELLIGENCE, not MAXIMUM ACTIVITY.
6. AVOID UNNECESSARY ORCHESTRATION — never invoke every capability automatically; never spawn subagents without an independent responsibility; never research trivial facts that local inspection answers; never add ceremony to trivial changes; never repeat verification with no new information; no recursive orchestration; stop at justified stop conditions.
7. NEVER OVERRIDE — regardless of mode: universal skill semantics; dependency resolution; confirmation for irreversible/high-impact actions; verification triggers; source-of-record discipline; honest OBSERVED/SPECIFIED/INFERRED/UNKNOWN reporting.
8. REPORT — state the mode in use, capabilities activated (with reasons), the activation/adaptation status (probe output), and the evidence for each installation step (per the standard report format).
```

---

*Build the system, not the deck. Optimize for observable agent performance — a shorter workflow that produces better outcomes beats a sophisticated workflow that merely sounds intelligent.*
