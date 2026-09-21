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
```

**Source checkout (development only):**

```bash
git clone https://github.com/pixzdev/skills.git
python scripts/validate.py && python scripts/check-cycles.py && python evals/runner.py
```

> See `docs/install-as-skill.md` for the copy-paste prompt that tells any agent to *install* (not just clone) and verify.

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
| 3 Behavioral | `evals/behavioral/runner.py` (4 scenarios) | routing, orchestration decisions, challenge/verification (smoke) |
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
VERSION                # repo SemVer (1.0.1)
llms.txt               # machine map
schemas/               # skill, registry, workflow, eval
core/ quality/ engineering/ security/ design/ frontend/ motion/ devops/ ai/  # 28 skills (SKILL.md + metadata.yaml)
adapters/              # claude, openclaw, opencode, hermes
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
