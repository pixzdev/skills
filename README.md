# PIXZ.DEV Skills

Portable, dependency-aware skills for Claude Code, OpenClaw, OpenCode and Hermes — one methodology, four verified runtimes.

## Why

Agents fail when they guess *what* capability to use, *what* it requires, and *how* to verify it. This repo gives them a capability layer: 28 skills with stable IDs, explicit dependencies, and verification contracts, discoverable from one registry and installable where the runtime actually discovers them.

It separates **Agent** (who), **Skill** (how), **Tool** (what), **Orchestrator** (WHEN/WHO/WHAT/WHY), **Protocol** (how agents behave), **Policy** (constraints), **Eval** (how to measure), **Registry** (discovery).

## Install — Source ≠ Install

Cloning gives you **source**. Installation registers the skill where the runtime discovers it.

**Pick your runtime (see `docs/install/README.md` for full matrix):**

```bash
# skills.sh — any agent with `npx skills` (VERIFIED)
npx skills add pixzdev/skills --list
npx skills add pixzdev/skills --skill orchestrator
npx skills list

# Claude Code — VERIFIED
npx skills add pixzdev/skills --skill orchestrator --agent claude-code
# or manual project: git clone .../skills /tmp/pixz && mkdir -p .claude/skills/orchestrator && cp -r /tmp/pixz/core/orchestrator/* .claude/skills/orchestrator/

# OpenClaw — VERIFIED
openclaw skills install ./core/orchestrator --as pixz-orchestrator
# or: openclaw skills install skills-sh:pixzdev/skills/orchestrator

# OpenCode — VERIFIED (singular `skill`)
mkdir -p .opencode/skill/orchestrator && cp -r core/orchestrator/* .opencode/skill/orchestrator/

# Hermes — VERIFIED
mkdir -p ~/.hermes/skills/orchestrator && cp -r core/orchestrator/* ~/.hermes/skills/orchestrator/

# Generic (Codex/Cursor) — PARTIALLY VERIFIED
mkdir -p .agents/skills/orchestrator && cp -r core/orchestrator/* .agents/skills/orchestrator/

# Full ecosystem — all 28 skills at once (skills.sh)
npx skills add pixzdev/skills
```

**Source checkout (development only):**

```bash
git clone https://github.com/pixzdev/skills.git
python scripts/validate.py && python scripts/check-cycles.py && python evals/runner.py
```

> **Copy-paste prompts for agents:** see **AI Agent Installation Prompt** and **Super Z / GLM / Z.AI Web Prompt** below. Full runtime-adaptive version: `docs/prompts/install-skill-agent.md`; short version: `docs/install-as-skill.md`.

## Supported Runtimes

| Runtime | Status | Install | Discovery | Invocation |
|---------|--------|---------|-----------|------------|
| skills.sh | VERIFIED | `npx skills add pixzdev/skills --skill <name>` | `npx skills list` | description-match |
| Claude Code | VERIFIED | `npx skills add ... --agent claude-code` or `~/.claude/skills/` / `.claude/skills/` | scan at session start | auto or `/<name>` |
| OpenClaw | VERIFIED | `openclaw skills install` (`skills-sh:`/`git:`/`./path --as`) | workspace > personal > managed | `openclaw skills list/check/verify --card` |
| OpenCode | VERIFIED | `.opencode/skill/` (singular canonical) or `.claude/skills/` compat | walk-up `skill`/`skills` | description-match |
| Hermes | VERIFIED | `~/.hermes/skills/` or `skills/` | `~/.hermes/skills/` primary | description-match |
| Generic (Codex/Cursor etc.) | PARTIALLY VERIFIED | `.agents/skills/` | session start if supported | per-agent |

Classification: **VERIFIED** = official docs + CLI help/ls evidence; **PARTIALLY VERIFIED** = spec exists but not smoke-tested in CI. Full matrix with commands: `docs/install/README.md`.

## Use a Skill

```bash
# 1. Discover
cat AGENTS.md           # trigger table
cat registry.json | jq '.skills[] | .id'

# 2. Resolve dependencies (mandatory 10, with optional 12)
python scripts/resolve.py --install pixz.core.orchestrator --runtime claude
python scripts/resolve.py --install pixz.core.orchestrator --runtime claude --with-optional

# 3. Apply methodology from that skill's SKILL.md (Purpose, When to use/NOT, Methodology, Verification)
# Example: security review before shipping auth change
cat security/review/SKILL.md
```

Minimal vs full routing: rename → `UNDERSTAND→EXECUTE→VERIFY` (no orchestrator). Production migration → full loop with challenger + quality-gate. See `docs/architecture/routing.md`.

## AI Agent Installation Prompt

Copy-paste the block below into any AI agent (Claude Code, OpenClaw, OpenCode, Hermes, Cursor, Codex, or any Agent Skills runtime). It is runtime-agnostic by design — the agent detects its own environment and uses the repository's official mechanisms.

```markdown
You are installing a PIXZ.DEV skill into the CURRENT AI agent runtime — not cloning a repository, not reading documentation.

Repo: https://github.com/pixzdev/skills (machine source of truth: registry.json).

1. IDENTIFY RUNTIME — probe, do not assume:
   - Paths: ls -la ~/.claude/skills .claude/skills .opencode/skill ~/.config/opencode/skill ~/.hermes/skills .agents/skills ./skills
   - CLIs: npx skills --help; openclaw --help; opencode --help; hermes --help; claude --version (report whichever succeed)
   - Report the runtime + evidence. If several are present, prefer the active one and say why. If none is recognized, treat the runtime as generic (.agents/skills, manual copy) and say so.
2. INSPECT ENVIRONMENT — OS, git state, package manager, and write permission to the intended install path. If something blocks installation, report it before acting.
3. LOCATE SKILLS — obtain the source once (git clone https://github.com/pixzdev/skills /tmp/pixz is fine). Read docs/install/README.md in the checkout — it is the official, verified install-matrix for each runtime.
4. DISCOVER INSTALLATION METHOD — for your detected runtime, use its official mechanism from that matrix (skills.sh CLI, openclaw skills install, or the adapter's copy path in adapters/). Use the repository's runtime adapter — do NOT invent a new skill format. Preserve existing user configuration: never overwrite an existing skill of the same name; if one exists, stop and report it.
5. RESOLVE DEPENDENCIES — if the requested skill declares requires/aggregates, resolve the full set first:
   python3 /tmp/pixz/scripts/resolve.py --install <skill-id> --runtime <detected>
   (Add --with-optional only if the user asked for optional skills.) Install the resolved set in the printed order. Default skill if none was requested: pixz.core.orchestrator.
6. INSTALL — execute exactly ONE install mechanism and capture command, exit code, and output. Cloning is NOT installation.
7. VERIFY — mandatory and evidence-based: the runtime's discovery command must show the skill at its installed location:
   - skills.sh: npx skills list
   - OpenClaw: openclaw skills list (+ openclaw skills check)
   - Others: ls <installed path>/SKILL.md && head -20 <installed path>/SKILL.md
   If discovery does not show it, the installation FAILED.
8. REPORT — paste this structure; every field must be backed by the command output you actually saw:
   SKILL INSTALLATION REPORT
   Runtime: <name, evidence>
   Skill: <id, name, version from metadata.yaml>
   Source: pixzdev/skills@<SHA or VERSION>
   Installation: SUCCESS | FAILED — <command, exit code>
   Installed location: <path verified by ls>
   Discovery: PASS | FAIL — <list/check output excerpt>
   Invocation: PASS | FAIL — <how you loaded it, result>
   Smoke test: PASS | FAIL | SKIPPED — <command, result, or reason>
   Notes: <fallbacks used, limitations>

Success means steps 7–8 are backed by evidence. An honest FAILED report with evidence is an acceptable outcome; fabricating a PASS is not.
```

## Super Z / GLM / Z.AI Web Prompt

Separate, copy-paste block for agents identified as **Super Z**, **GLM**, or **Z.AI Web**. It selects the repository's isolated runtime profile (`profiles/super-z/PROFILE.md`) and never alters universal skill semantics.

```markdown
You are an agent identified as Super Z, GLM, or Z.AI Web. Confirm that identity from your own runtime/model self-report first — if you are not one of these, ignore this prompt and follow the standard AI Agent Installation Prompt instead.

1. RECOGNIZE RUNTIME — state the identity signals you observed (self-reported model/runtime name). This activates the repository's runtime profile: fetch profiles/super-z/PROFILE.md from https://github.com/pixzdev/skills and operate under it.
2. SELECT MODE — BEFORE any substantive work, invoke your AskUserQuestion capability and ask the user to choose exactly one mode:
   - FAST — minimum orchestration overhead
   - BALANCED — adaptive orchestration, minimum sufficient delegation
   - DEEP — more relevant skills, specialist subagents, research, verification, adversarial review
   - AUTONOMOUS — Deep-level rigor with minimal user interruptions
   If the user does not select a mode, default to BALANCED and state that you are using the default. If AskUserQuestion is unavailable, state that and proceed at BALANCED.
3. DISCOVER & INSTALL SKILLS — read AGENTS.md and registry.json in the repository; resolve dependencies with scripts/resolve.py before implementation; install via the verified mechanisms in docs/install/README.md; verify actual installation and invocation with evidence (skills list / ls of the installed path). Never claim success without that evidence.
4. OPERATE AT THE SELECTED MODE (per profiles/super-z/PROFILE.md):
   - FAST: minimum overhead; a single skill where justified; no subagents unless asked.
   - BALANCED: adaptive orchestration; minimum sufficient delegation; challenger only when risk×uncertainty×impact is high.
   - DEEP: discover relevant skills before implementation; invoke multiple complementary skills when justified; use specialist subagents with rich structured handoffs; research (official sources first); independent verification passes; adversarial review of consequential conclusions; iterate while expected value is positive.
   - AUTONOMOUS: Deep-level rigor with minimal interruptions — interrupt only for true blockers or irreversible/high-impact actions (change-safety tiers); record every decision and its evidence for later review.
5. COMPUTE POLICY — your runtime's generous compute is not permission to waste compute. Never: invoke every skill automatically; spawn subagents without an independent responsibility; research trivial facts; add ceremony to trivial changes; continue after a justified stop condition. Objective: MAXIMUM USEFUL INTELLIGENCE, not MAXIMUM ACTIVITY.
6. NEVER OVERRIDE — regardless of mode, these remain binding: universal skill semantics; dependency resolution; confirmation for irreversible/high-impact actions; the verification layers; honest OBSERVED/SPECIFIED/INFERRED/UNKNOWN reporting.
```

## Runtime Profiles

A **profile** is an isolated, runtime-specific operating overlay (POLICY) — **not a skill**, not in `registry.json`, and it **does not change** universal skill semantics. Currently one profile exists: **Super Z / GLM / Z.AI Web** → `profiles/super-z/PROFILE.md` (operating modes FAST/BALANCED/DEEP/AUTONOMOUS, default BALANCED, mandatory `AskUserQuestion` mode selection, compute policy). Status: SPECIFIED; behavioral effect UNVERIFIED. Contract: `profiles/README.md`. Machine-checked by `scripts/validate.py`.

## Skill Architecture

```
Universal Core (SKILL.md + metadata.yaml + schemas — vendor-neutral)
        ↓
Adapter (thin translation — docs/install/*)
        ↓
~/.claude/skills/  ~/.openclaw/skills/  .opencode/skill/  ~/.hermes/skills/  .agents/skills/
```

Loop: `UNDERSTAND → DISCOVER → PLAN → EXECUTE → INSPECT → CHALLENGE → VERIFY → REPLAN → IMPROVE → VERIFY → SHIP`
Methodological `NORMALIZE`/`ARCHITECT` map to `PLAN`; `IMPLEMENT` maps to `EXECUTE`. `REINITIATE` is a policy (restart from `DEFINE`), not a workflow state — see `docs/architecture.md`.

## Core Skills (13 of 28)

`orchestrator`, `planning`, `context-engineering`, `environment-awareness`, `capability-discovery`, `workflow-continuity`, `delegation-handoff`, `epistemic-reasoning`, `epistemic-challenger`, `verification`, `change-safety`, `replanning`, `quality-gate` — installing orchestrator resolves its 8 mandatory aggregates (10 nodes; 12 with `--with-optional`). Full list + domain skills: `AGENTS.md` and `docs/architecture.md`.

Taxonomy: standalone skill requires distinct objective, methodology, triggers, I/O, failure conditions, independent value — otherwise it's a protocol/policy/doc. See `docs/taxonomy.md`.

## Dependency Model

- `requires` — hard, transitive, fail if missing/incompatible
- `aggregates` — orchestrator composition, mandatory when parent installed
- `optional` — **opt-in** via `--with-optional` (e.g., `epistemic-challenger`, `anti-ai-slop`); otherwise reported as `excluded_optional` with reason
- `conflicts` — mutual exclusion
- `compatible_runtimes` — resolver checks `runtime ∩ skill.compatible_runtimes`

No cycles (DFS), deterministic topo-sort, depth caps (`max_skill_chain_depth=15`, `max_orchestration_depth=6`, `max_iterations=8`). See `docs/dependency-model.md`.

## Verification — 4 Layers

| Layer | Harness | What |
|-------|---------|------|
| 1 Structural | `scripts/validate.py` + `check-cycles.py` | frontmatter, files, IDs, registry consistency, graph, schemas |
| 2 Documentary | `evals/runner.py` (15 cases) | required sections, install commands, examples (heuristic) |
| 3 Behavioral | `evals/behavioral/runner.py` (15 scenarios) | routing, orchestration decisions, challenge/verification (smoke) |
| 4 Integration | `scripts/integration-smoke.sh` | repo → installer → runtime → discovery → invocation (where CLI available) |

Layer 1–2 never imply 3–4. See `docs/evaluation.md`.

```bash
python scripts/validate.py
python scripts/check-cycles.py
python evals/runner.py
python evals/behavioral/runner.py
bash scripts/integration-smoke.sh
```

## Development

```bash
# create skill
mkdir -p <domain>/<name>
# write <domain>/<name>/SKILL.md (frontmatter name/description) + metadata.yaml (see schemas/skill.schema.json)
python scripts/validate.py && python scripts/check-cycles.py
python scripts/resolve.py --install pixz.<domain>.<name> --runtime claude
```

Contract per skill: Purpose, When to use / NOT, Inputs, Outputs, Dependencies, Compatible runtimes, Methodology, Verification, Failure conditions, Example. Long rationale → `docs/`. See `docs/development/creating-a-skill.md` and `docs/development/testing.md`.

## Repository Structure

```
AGENTS.md              # agent registry (human)
registry.json          # machine registry (source of truth, validated)
VERSION                # repo SemVer (1.1.0)
llms.txt               # machine map
schemas/               # skill, registry, workflow, eval
core/ quality/ engineering/ security/ design/ frontend/ motion/ devops/ ai/  # 28 skills (SKILL.md + metadata.yaml)
adapters/              # claude, openclaw, opencode, hermes (install translation only)
profiles/              # isolated runtime profiles (super-z) — not skills, no semantics change
scripts/               # resolve, validate, check-cycles, integration-smoke
evals/                 # cases, behavioral, runner
examples/              # basic-usage, orchestrated-task, custom-skill
docs/                  # architecture, install, evaluation, getting-started, troubleshooting, prompts
agents/                # orchestrator, specialist
```

## Limitations (honest)

- `pinned` channel (`pixz.lock`) is **documented future** — `stable`/`latest` work, `pinned` accepts flag but does not write lockfile
- Behavioral eval is heuristic smoke, not model-graded
- Generic runtime is **partially verified** (AGENTS.md spec, manual `ls`/`list` only)
- Installation needs `npx` (Node 18+) or manual `cp -r`; offline/hermetic envs use manual copy
- No hosted skill marketplace yet — install via `skills.sh` CLI or manual copy

## Contributing

See `CONTRIBUTING.md` (taxonomy gate, folder contract, validation checklist, PR process). New skill must pass the seven standalone criteria and `scripts/validate.py` + `scripts/check-cycles.py`.

## License

MIT — `LICENSE`.

---

*Build the system, not the deck. Minimum necessary complexity, maximum operational clarity.*
