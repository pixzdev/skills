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
PIXZFLOW  operating discipline    (L2 — AGENTS.md, modes, state, evidence, policies, mandate)
OVERLAYS  one-runtime parameters  (L2.5 — ZAI.md for Super Z / GLM / Z.AI Web)
SKILLS    specialized capability  (L3 — 30 skills, stable IDs, dependency-aware)
EXTERNAL  vetted external tools   (L3.5 — MCP servers + imported skills, mcp/catalog.json)
AGENTS    parallel specialization (L4 — contract-bound subagent roles)
STATE     continuity              (L5 — task-state + adaptation-state + evidence)
```

| Artifact | Role |
|---|---|
| `AGENTS.md` | Canonical operating contract (agent entry point, incl. the **PixzFlow Mandate**) |
| `registry.json` | Machine source of truth — skills, protocols, policies, limits |
| `llms.txt` | LLM map (projection of the registry) |
| `mcp/catalog.json` | Vetted MCP server + skill-source catalog (free + no-signup-only; 16 servers, 4 skill sources) |
| `schemas/` | `task-state` · `adaptation-state` · `handoff` · `skill` · `registry` · `eval` |
| `scripts/` | `validate.py` · `check-cycles.py` · `resolve.py` · `activation.py` (incl. `verify-installed`) · `doctor.py` · `assess.py` · `sitrep.py` · `hooks.py` · `mcp.py` (auto-config) · `integration-smoke.sh` |
| `evals/` | documentary (21) + behavioral (34) + lifecycle (14) |
| `adapters/` | Thin runtime translators (claude, openclaw, opencode, hermes) |
| `core/` + domains | 15 core + 15 domain skills (`pixz.<domain>.<name>` IDs) |

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

## The Mandate (complex work is obligated)

PixzFlow is not optional decoration on complex work — it is a **contract**:

- A task is **complex** if any of: complexity or risk band **high/critical** · irreversible/high-impact action · security or consequential surface · multiple files/components or external integrations · long horizon · continuation of prior work.
- A complex task **MUST** run under the full PixzFlow protocol: entry protocol, recorded assessment, plan, capability activation, task-state, typed evidence, verification at claim-matching depth (`pixz.policy.pixzflow-mandate`).
- A complex task completed **without** the protocol is a **contractual failure (GAGAL)** — even if the output looks correct. The work is reported as FAILED (incomplete) and is not accepted as done until the protocol is retrofitted with evidence.
- Trivial, reversible, single-step work stays exempt: `ORIENT → ACT → VERIFY`, zero ceremony. The mandate adds no ritual to cheap work.

The agent self-audits at `ORIENT` ("is this complex?") and at `DECIDE` ("was the protocol followed — where is the evidence?"), and complex tasks carry the audit in task-state (`mandate: {complex, protocol_followed, evidence}`).

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

30 skills, stable `pixz.<domain>.<name>` IDs, dependency-aware (`requires` / `aggregates` / `optional` / `conflicts`). 15 core: orchestrator, planning, context-engineering, environment-awareness, capability-discovery, workflow-continuity, delegation-handoff, epistemic-reasoning, epistemic-challenger, verification, change-safety, replanning, quality-gate, **self-learning**, **mcp**. 15 domain: quality, engineering, security, design, frontend, motion, devops, ai.

**Main skill:** `pixz.core.orchestrator` is the practical operating skill. Specialist skills answer HOW. If you want more practical multi-step methodology, activate the orchestrator; load `core/orchestrator/references/operating-methodology.md` when the work is complex.

```
DISCOVER (metadata only) → MATCH → LOAD (progressive) → ACTIVATE → USE → VERIFY → PERSIST → REINVOKE → COMPLETE
```

Budget rule: every activation earns its context cost. The orchestrator's mandatory closure is 4 nodes (the evidence floor: orchestrator → verification → epistemic-reasoning → context-engineering); everything else activates on demand. Resolver: `python scripts/resolve.py --install pixz.core.orchestrator --runtime claude` → 4 nodes (16 with `--with-optional`).

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
| 2 Documentary | `evals/runner.py` (21, heuristic) | skills document required methodology |
| 3 Behavioral | `evals/behavioral/runner.py` (34 + invariants, heuristic) | routing/activation smoke, evidence floor, trivial-task budget, mode consistency |
| 3b Lifecycle | `evals/lifecycle/run_tests.py` (14, deterministic) | self-learning state machine + 2.2 tooling: activation, reload, drift, failed adaptation, regression, doctor, integrity, sitrep, assessment, hooks |
| 4 Integration | `scripts/integration-smoke.sh` | installer → discovery → invocation where runtimes exist |

## Adaptive complexity

Self-improvement must not cause process inflation. Process depth scales with the assessment bands; self-improvement itself is costed against reliability gain vs token cost, latency, tool calls, context consumption and permanent complexity. **Anti-proliferation gate:** a failure must not spawn a new skill/agent/protocol/schema/instruction file/dependency unless existing mechanisms cannot express the fix, the failure class recurs, the benefit justifies permanent cost, and the result is testable. Prefer: policy → extend existing mechanism → new test → (last) new abstraction. A mechanism that improves one edge case while making every trivial task worse is rejected or redesigned.

## Delegation

Only when `information gain + parallelism + specialization > coordination cost`. Structured dispatch + mandatory structured return (`schemas/handoff.schema.json`); the parent inspects — no "looks good" returns; subagents never spawn subagents. Restraint is evaluated (anti-delegation scenario).

## Runtime overlays

An overlay parameterizes one runtime without changing universal semantics. Currently: **`ZAI.md`** (Super Z / GLM / Z.AI Web) — mandatory pre-work questions (setup tier + operating mode) + compute policy. Status: SPECIFIED (2.4); behavioral effect UNVERIFIED.

## MCP & Skills Integration (free + no-signup-first)

PixzFlow integrates **MCP servers** and **external agent skills** with the same discipline it applies to everything else: vetted sources, evidence before trust, budgeted activation.

- **Universe policy:** the default integration universe is **free + no signup + no API key**. Anything that requires an account or a key is excluded by default and only enters on explicit user request with user-managed credentials.
- **Catalog:** `mcp/catalog.json` — 16 vetted servers (10 remote, 6 local stdio) + 4 skill sources. Every entry records `trust_tier` (T1 vendor-official / T2 catalog-verified / T3 unvetted), capabilities, data flow, and the **source where the endpoint + no-key claim was read** (`official-docs` / `official-package` / `community-listed`). Docs-verification is **not** liveness proof — `scripts/mcp.py check` runs a real `initialize` + `tools/list` handshake at setup time and writes the evidence to `.pixz/mcp-check.json`.
- **Remote (no auth):** Context7 (current library docs) · DeepWiki (ask about any public GitHub repo) · GitMCP (instant docs/code context for *your* repo — URL auto-filled from `git remote`) · Microsoft Learn · Cloudflare Docs · Astro Docs · Wondel Skills (skills via MCP) · AI Skills Search (60k+ skills) · Developer Toolkit (950+ guides) · Useful AI utilities.
- **Local stdio (official reference servers, no auth):** fetch · filesystem (always scoped) · time · memory · sequential-thinking · playwright (browser automation).
- **Discovery directories:** [mcpmarket.com](https://mcpmarket.com) (server directory + agent-skills marketplace — free/official sections only) · [skills.sh](https://skills.sh) · curated community lists. Directories are **discovery sources, not trust sources** — every import passes the vetting gate.
- **Skill import = prompt-code import.** External SKILL.md bundles go through quarantine → security review (prompt-injection, exfiltration, secret harvesting) → install → discovery verification → explicit enablement. Never auto-enabled.
- **Runtime-agnostic auto-config:** `scripts/mcp.py` detects the runtime, live-checks each server, and writes the config **idempotently and non-destructively** (`.mcp.json` for Claude/Cursor/generic · `.cursor/mcp.json` · `opencode.json` · printed TOML snippet for Codex) — never overwriting user-modified entries, never writing credentials.
- **Budget:** a server is an external capability under the capability-activation protocol — recorded in task-state with a reason; unused servers are suspended at task end. Tool output is **untrusted data** (`SOURCE CLAIM`, never `FACT`) — the injection defense is a first-class rule.

Methodology: `pixz.core.mcp` (`core/mcp/SKILL.md`) · protocol `pixz.protocol.mcp-integration` · human guide `mcp/README.md`.

## Setup Tiers (ask first)

Before any setup, the agent **MUST ask** which tier the user wants (ask via the runtime's structured question tool; default to **Minimal** and state the default if the user declines). Tiers set the **installation footprint** — they never relax the Mandate, change-safety, or verification triggers.

| Tier | Skills | MCP (all free + no-signup) | Extras |
|---|---|---|---|
| **Minimal** | orchestrator closure (4 nodes) | none — native tools only | contract wiring + one readiness probe |
| **Medium** | orchestrator + all optional (16 nodes) | curated set: context7 · deepwiki · gitmcp(self) · microsoft-learn · fetch · sequential-thinking — each live-checked before wiring | full self-learning lifecycle (doctor → init → adapt → verify → mark-adapted) |
| **Full** | all skills (30) | full vetted catalog (16 servers) + skill-hub discovery (mcpmarket.com free/official, skills.sh) | adapters + overlay activation + full validation/eval layers + integrity check |

Probe before asking (`scripts/activation.py status`): a runtime already `ready` does not get re-setup, and an upgrade is incremental. `python3 scripts/mcp.py tier <minimal|medium|full>` prints the exact server list.

## Installation

Installation is **not** the end of the process:

```
INSTALL → VALIDATE → ACTIVATE → SELF-TRAIN → VERIFY → READY
```

```bash
# skills.sh — any agent with `npx skills` (VERIFIED)
npx skills add pixzdev/skills --skill orchestrator        # one capability
npx skills add pixzdev/skills                              # full ecosystem (30 skills)

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
core/<skill>/SKILL.md + metadata.yaml     # 15 core capabilities (incl. mcp)
<domain>/<skill>/…                        # 15 domain capabilities
mcp/                                      # catalog.json (vetted free/no-signup MCP servers + skill sources) + README
schemas/                                  # task-state, adaptation-state, handoff, skill, registry, eval
scripts/                                  # validate, check-cycles, resolve, activation, mcp (auto-config), integration-smoke
evals/cases · evals/behavioral · evals/lifecycle
adapters/{claude,openclaw,opencode,hermes} · agents/ · profiles/
docs/                                     # architecture, evaluation, taxonomy, install matrix, research, benchmark, prompts
```

## Evaluation

See `docs/evaluation.md`. Per-layer results, never cross-layer inflation: structural PASS/FAIL · documentary `X/21 heuristic` · behavioral `X/34` + invariants · lifecycle `X/14 deterministic` · integration PASS/FAIL per runtime. The behavioral E-series covers: first activation · existing runtime (no duplicate setup) · skill upgrade · failed assumption · self-improvement · anti-overengineering · regression · persistence · validation depth · contradictory evidence · trivial-task budget · high-risk escalation · MCP routing (free server add + no-ceremony guard).

## Benchmarks

- **GLM benchmark (run, recorded):** 52/52 both conditions; ~+0.17 blind delta; ~1.48× token overhead; B≈B1, C≈A; T11 source-of-record n=2. See `docs/benchmark/GLM-benchmark-findings.md`.
- **Successor benchmark (designed, UNRUN):** model-graded ablation cells A–H including self-learning effect (`docs/benchmark/successor-benchmark.md`). This repo never fabricates results — unrun cells say UNRUN.

## Limitations (honest)

- Behavioral eval is heuristic smoke + deterministic state-machine tests — **not** model-graded; successor benchmark cells are UNRUN.
- `ZAI.md` overlay: SPECIFIED; behavioral effect UNVERIFIED.
- `pinned` channel (`pixz.lock`): documented future — resolver accepts the flag, writes no lockfile.
- Generic runtime: PARTIALLY VERIFIED (spec exists, no CI smoke).
- MCP catalog: endpoints **docs-verified** (dated, with source, in `mcp/catalog.json`) — **liveness is proven only at setup time** by the live probe (`scripts/mcp.py check` → `.pixz/mcp-check.json`); a docs-level listing is never claimed as a live connection. Local stdio servers need `npx` (Node 18+) on first run.
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
You are installing PixzFlow (PIXZ.DEV) capabilities into the CURRENT AI agent runtime — not cloning a repository, not reading documentation for its own sake. Installation is only the first step: after installing you must ACTIVATE and SELF-TRAIN per steps 12–13. After setup, every COMPLEX task must run under the full PixzFlow protocol — a complex task done without it is a contractual failure (GAGAL). Trivial work stays cheap.

Repo: https://github.com/pixzdev/skills (machine source of truth: registry.json).

1. ASK SETUP TIER — MANDATORY, before any setup: invoke your AskUserQuestion capability (or the runtime's equivalent structured question tool) and ask:
   "Which PixzFlow setup tier should I install?"
   1. Minimal — orchestrator closure (4 skills) + contract wiring + one probe; NO MCP (native tools only)
   2. Medium — orchestrator + all optional skills (16) + curated free/no-signup MCP set (context7, deepwiki, gitmcp-self, microsoft-learn, fetch, sequential-thinking), live-checked before wiring; full self-learning lifecycle
   3. Full — all skills (30) + full vetted MCP catalog (16 servers) + skill-hub discovery (mcpmarket.com free/official, skills.sh) + adapters + overlays + full validation/eval layers
   Tiers set installation footprint only — never the mandate, change-safety, or verification. If the user does not answer (or the tool is unavailable), DEFAULT TO MINIMAL and state the default. For Super Z / GLM / Z.AI Web runtimes, ZAI.md governs this question (together with the operating-mode question).
2. INSPECT ENVIRONMENT — probe, do not assume:
   - Paths: ls -la ~/.claude/skills .claude/skills .opencode/skill ~/.config/opencode/skill ~/.hermes/skills .agents/skills ./skills
   - CLIs: npx skills --help; openclaw --help; opencode --help; hermes --help; claude --version (report whichever succeed)
   - OS, git state, package manager, write permission to the intended install path. If something blocks installation, report it before acting.
3. LOCATE PIXZFLOW — obtain the source once (git clone https://github.com/pixzdev/skills /tmp/pixz is fine). Read AGENTS.md (operating contract, incl. the PixzFlow Mandate), registry.json (capabilities), and docs/install/README.md (official install matrix).
4. INSPECT COMPATIBILITY — for your detected runtime, confirm the official mechanism from that matrix (skills.sh CLI, openclaw skills install, or the adapter's copy path in adapters/). Use the repository's runtime adapter — do NOT invent a new skill format. Preserve existing user configuration: never overwrite an existing skill of the same name; if one exists, stop and report it.
5. RESOLVE DEPENDENCIES per the selected tier:
   - Minimal: python3 /tmp/pixz/scripts/resolve.py --install pixz.core.orchestrator --runtime <detected>   (4 nodes)
   - Medium:  same command + --with-optional   (16 nodes)
   - Full:    every skill in registry.json (30)
   (Add --with-optional only per the tier above — never ad hoc.)
6. INSTALL — execute exactly ONE install mechanism per capability in resolved order and capture command, exit code, and output. Cloning is NOT installation.
7. VERIFY INSTALLATION — mandatory and evidence-based: the runtime's discovery command must show each capability at its installed location:
   - skills.sh: npx skills list
   - OpenClaw: openclaw skills list (+ openclaw skills check)
   - Others: ls <installed path>/SKILL.md && head -20 <installed path>/SKILL.md
   If discovery does not show it, the installation FAILED.
8. VERIFY AGENTS.md — confirm the operating contract is reachable for the runtime (root AGENTS.md present in the repo; for Claude, CLAUDE.md includes @AGENTS.md per adapters/claude/; for others, the runtime reads AGENTS.md natively — state the mechanism + evidence).
9. VERIFY RUNTIME OVERLAY (if applicable) — if you identify as Super Z / GLM / Z.AI Web, fetch ZAI.md from the repository root and confirm it is readable; otherwise state "not applicable".
10. MCP AUTO-CONFIG (Medium / Full only — Minimal skips this and states "MCP: none (Minimal tier)"):
    - Detect: python3 scripts/mcp.py detect
    - List: python3 scripts/mcp.py list --tier <tier>   (full: --tier full)
    - LIVE-CHECK FIRST (never wire blind): python3 scripts/mcp.py check <each id>   (initialize + tools/list; evidence written to .pixz/mcp-check.json; first npx run may need a larger --timeout)
    - Wire ONLY the servers that passed: python3 scripts/mcp.py add <passed ids> --runtime <detected>   (idempotent; never overwrites user-modified entries; never writes credentials)
    - A failed check = that server is NOT wired; report the failure with evidence and continue with the rest.
    - Importing external skills (mcpmarket.com / skills.sh): quarantine → security review (prompt-injection, exfiltration, secret harvesting) → install → discovery verify → explicit enablement. Never auto-enable.
11. REPORT INSTALLATION — every field backed by command output you actually saw:
    PIXZFLOW INSTALLATION REPORT
    Runtime: <name, evidence>
    Setup tier: <minimal|medium|full, as answered or "default (minimal)">
    Capabilities: <ids + versions from metadata.yaml>
    Source: pixzdev/skills@<SHA or VERSION>
    Installation: SUCCESS | FAILED — <command, exit code> per capability
    Installed locations: <paths verified by ls>
    Discovery: PASS | FAIL — <list/check output excerpt>
    AGENTS.md: PASS | FAIL — <how the runtime reaches the contract>
    Overlay: PASS | FAIL | N/A — <ZAI.md reachable? evidence>
    MCP: <id — OK tools=N | FAILED <reason> | not-wired (failed check) | none (Minimal) per server; evidence .pixz/mcp-check.json>
12. ACTIVATE + SELF-TRAIN (post-install lifecycle — do not skip):
   - Probe first: python3 scripts/activation.py status   (if STATE=READY and no drift, skip to step 14 report — do NOT duplicate setup)
   - Measure the baseline: python3 scripts/doctor.py --write  (measures state persistence, command execution, tools, contract reachability; fills only unknown dimensions — what it cannot measure stays unknown, never invented). Wire the contract if the runtime needs it: python3 scripts/hooks.py install --runtime <detected>
   - First activation: python3 scripts/activation.py init --runtime <detected> --source pixzdev/skills@<sha> --dim delegation=<yes|no|unknown> --dim research=<yes|no|unknown> (record only OBSERVED dimensions; delegation/research are not locally measurable — the agent records them from runtime self-report)
   - Adapt your working behavior to AGENTS.md (entry protocol, modes, the PixzFlow Mandate, evidence rules, verification triggers, delegation constraints, capability-activation protocol, stopping rules).
   - VERIFY the adaptation at RUNTIME-ACTIVE depth (run the repo validation layers where the source is available; invoke one real capability; show the probe transition), then: python3 scripts/activation.py mark-adapted --evidence "<what you actually observed>". This command refuses without evidence — "I have learned PixzFlow" is not evidence.
13. ADOPTION ASSESSMENT (automatic) — mark-adapted auto-runs scripts/assess.py and prints an adoption score 0–100. The score is a sum of named evidence-backed checks (each PASS/FAIL; UNVERIFIED items score 0; gaps listed) — it is NOT a model-quality or workflow-effectiveness metric. Reproduce with python3 scripts/assess.py [--full]. If installed skill copies exist, also run python3 scripts/activation.py verify-installed --runtime <detected> and report any MODIFIED copies (inspect before trusting).
14. FINAL REPORT — append to the installation report:
   Activation: NEW->BASELINED->READY | ALREADY READY — <probe output>
   Adaptation evidence: <commands run + observed output>
   Baseline dimensions: <measured by doctor.py; unknowns listed, not invented>
   Adoption score: <N/100 + verdict, exactly as printed by the assessment; list the failing checks>
   MCP: <wired list + check evidence path, or "none (Minimal tier)">
   Integrity: verify-installed PASS | MODIFIED(<ids>) | NOT RUN — <reason>
   Notes: <fallbacks used, limitations>
   Mandate reminder: complex tasks from now on MUST run under the full PixzFlow protocol (assessment + plan + activation + task-state + evidence + verification) — a complex task done without it is a contractual failure (GAGAL).

Success means steps 7–14 are backed by evidence. An honest FAILED report with evidence is an acceptable outcome; fabricating a PASS is not.
```

## Super Z / GLM / Z.AI Web Install & Activation Prompt

Copy-paste block for agents identified as **Super Z**, **GLM**, or **Z.AI Web**. It activates the repository's isolated runtime overlay (`ZAI.md`) and never alters universal semantics.

```markdown
You are an agent identified as Super Z, GLM, or Z.AI Web. Confirm that identity from your own runtime/model self-report first — if you are not one of these, ignore this prompt and follow the standard AI Agent Installation Prompt instead. Do not assume undocumented Z.AI runtime features; state only what you can observe.

1. RECOGNIZE RUNTIME — state the identity signals you observed (self-reported model/runtime name). This activates the repository's runtime overlay: fetch ZAI.md from https://github.com/pixzdev/skills (repository root) and operate under it.
2. PRE-WORK QUESTIONS — BEFORE any substantive work, invoke your AskUserQuestion capability and ask, in this order:
   a) SETUP TIER (only if the runtime is not already READY — probe with `scripts/activation.py status` first; never re-ask an adapted runtime):
      - Minimal — orchestrator closure (4 skills) + contract wiring + one probe; no MCP
      - Medium — orchestrator + all optional skills (16) + curated free/no-signup MCP set, live-checked before wiring; full self-learning lifecycle
      - Full — all skills (30) + full vetted MCP catalog (16 servers) + skill-hub discovery (mcpmarket.com free/official, skills.sh) + adapters + overlays
      Default to Minimal and state it if the user does not answer.
   b) OPERATING MODE — choose exactly one:
      - Fast — minimum orchestration overhead
      - Balanced — adaptive orchestration, minimum sufficient delegation (default)
      - Deep — more relevant skills, specialist subagents, research, verification, adversarial review
      - Autonomous — Deep-level rigor with minimal user interruptions
      Default to Balanced and state the default if the user does not select. If AskUserQuestion is unavailable, state that and proceed at Minimal + Balanced.
   The mandate never changes with tier or mode: complex work runs under the full protocol in every mode — a complex task done without it is a contractual failure (GAGAL).
3. ACTIVATE PIXZFLOW PERSISTENTLY — read AGENTS.md and registry.json in the repository; install capabilities via the verified mechanisms in docs/install/README.md; resolve dependencies with scripts/resolve.py per the selected tier first (Minimal: 4 nodes; Medium: 16; Full: all 30); verify installation and invocation with evidence. For Medium/Full tiers, run MCP auto-config per `pixz.core.mcp` (step 10 of the standard prompt): live-check each server (evidence in .pixz/mcp-check.json) BEFORE wiring via `scripts/mcp.py add`. Operate under the capability-activation protocol: skills are persistent capabilities available throughout the task lifecycle, loaded progressively and tracked in task state. Then run the post-install self-learning lifecycle (steps 12–14 of the standard prompt): measure the baseline via scripts/doctor.py, init via scripts/activation.py, adapt behavior, verify at RUNTIME-ACTIVE depth, mark-adapted with evidence (auto-runs the adoption assessment) — never duplicate an existing READY adaptation.
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

## MCP Auto-Config Agent Prompt

Copy-paste block for the **MCP auto-configuration** step on its own (also embedded as step 10 of the AI Agent Installation Prompt). It is the agent-side instruction for `pixz.core.mcp` + `scripts/mcp.py`:

```markdown
You are configuring Model Context Protocol (MCP) servers for the CURRENT AI agent runtime, using the PixzFlow vetted catalog. Rules of the universe: FREE + NO SIGNUP + NO API KEY only (mcp/catalog.json). Do not invent endpoints. Do not write credentials anywhere. Do not wire anything you have not live-checked.

1. DETECT — python3 scripts/mcp.py detect (report which runtime/config exists; if none, default to `generic` = ./.mcp.json).
2. CHOOSE — pick the fewest vetted servers that cover the stated capability need:
   - python3 scripts/mcp.py list --tier <minimal|medium|full>   (or --category docs|code|web|browser|skills|utilities)
   - If the user asks for a server that is NOT in the catalog: it is T3 (unvetted) — run the security review (who operates it, tool surface, data flow, secrets) and get EXPLICIT user approval first. Never silently add.
3. LIVE-CHECK FIRST — python3 scripts/mcp.py check <ids...> (or --all). A pass = initialize + tools/list observed; the evidence is written to .pixz/mcp-check.json. A failed server is NOT wired — report the failure with its error line and move on. First `npx` runs download the package: retry once with a larger --timeout before declaring failure.
4. WIRE (idempotent, non-destructive) — python3 scripts/mcp.py add <passed ids> --runtime <detected>.
   - Existing user entry with a different spec → left untouched, reported `exists`.
   - Codex → print the exact ~/.codex/config.toml snippet; never clobber the file.
   - Re-read the written config and show it (EXISTS + PARSES).
5. VERIFY INTEGRATION — the runtime must list the servers (e.g. `claude mcp list`); report tools per server from the check evidence. Claim RUNTIME-ACTIVE only after one real tool call whose result you inspected.
6. BUDGET + STATE — record each wired server in task-state capabilities[] (id: mcp.<id>, reason, tool count). Suspend/remove servers the plan no longer needs.
7. REPORT —
   MCP AUTO-CONFIG REPORT
   Runtime: <name, config file, evidence>
   Servers: <id — OK tools=N | FAILED <reason> | not-wired | printed-snippet (codex) per server>
   Evidence: .pixz/mcp-check.json (checked_at)
   User config preserved: YES | <what was left untouched>
   Residual risks: <data flow to vendor, unpinned packages, …>

Success means every OK line is backed by check evidence. An honest FAILED line is acceptable; a fabricated OK is not.
```

## Why PixzFlow is different (frontier differentiators)

Most "agent skills" packs are prompt collections: phase checklists, more tokens, no memory. PixzFlow is an **operating layer** — the differences that matter at the frontier:

| Generic skill packs | PixzFlow |
|---|---|
| Fixed phase checklists ("plan → code → test") | **State + transitions + decisions** (`ORIENT → … → DECIDE{done|replan|challenge|stop}`) — depth set by assessment, not habit |
| "More skills = smarter" | **Budgeted activation** — every capability earns its context cost; mandatory closure is 4 nodes; 10 skills for a rename is a *measured failure mode* (evals) |
| Claims at face value | **Typed evidence** (`FACT · OBSERVED · SOURCE CLAIM · INFERRED · … VERIFIED · FALSIFIED`) + the **source-of-record rule** (descriptive records never beat actual artifacts) |
| "Tests passed = done" | **Verification-depth ladder** — EXISTS → PARSES → SCHEMA → CORRECT → INTEGRATED → RUNTIME-ACTIVE → PERSISTENT → IMPROVED; the claim must match the rung |
| Install and forget | **Self-learning lifecycle** — install ≠ activate ≠ adapt ≠ learn ≠ improve; drift re-adapts only the inspected delta; second activation is a check, never a re-run |
| MCP servers wired blind | **Vetted free/no-signup MCP universe** — trust tiers, security vetting gate, live `initialize`+`tools/list` before wiring, untrusted-tool-output rule, idempotent auto-config |
| No consequences | **The Mandate** — complex work *must* run under the protocol; skipping it is a contractual failure (GAGAL), not a style difference |
| One prompt for all runtimes | **Runtime overlays** (ZAI.md) + per-runtime adapters — same universal semantics, per-runtime parameters |
| Subagent output = truth | **Handoff contract** — structured dispatch + mandatory structured return + parent inspection; "looks good" is rejected |
| Benchmark theater | **Honest evaluation** — 4 layers, per-layer results, UNRUN cells said as UNRUN; the GLM benchmark numbers (small delta, 1.48× overhead) are published, not hidden |

---

*Build the system, not the deck. Optimize for observable agent performance — a shorter workflow that produces better outcomes beats a sophisticated workflow that merely sounds intelligent.*
