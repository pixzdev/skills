# PIXZ.DEV — Universal Agent Skills Ecosystem

> **Portable, composable, dependency-aware, versioned skills for any agent runtime.**
> One methodology, four runtimes: Claude / OpenClaw / OpenCode / Hermes (extensible).

[![Version](https://img.shields.io/badge/version-1.0.0-blue)](#versioning)
[![Registry](https://img.shields.io/badge/registry-AGENTS.md-green)](#discovery)
[![Validated](https://img.shields.io/badge/validated-registry%2Bschemas-success)](#project-structure)

## Why

Agents need more than prompts. They need a **capability layer** that answers:

- *What capability do I need for this task?*
- *Which skill provides it, and what does it require?*
- *Which runtime can run it? What context is authoritative?*
- *How is the result verified — and should another skill challenge it?*

This repo separates **Agent** (who) / **Skill** (how) / **Tool** (what) / **Orchestrator** (who coordinates) / **Protocol** (how agents behave) / **Policy** (constraints) / **Eval** (how to measure) / **Registry** (discovery).

## Install

```bash
# Production — stable pinned version (recommended)
git clone --branch v1.0.0 https://github.com/pixzdev/skills.git

# Development — latest
git clone https://github.com/pixzdev/skills.git

# Resolve a complete dependency graph (with cycle + runtime checks)
python scripts/resolve.py --install pixz.core.orchestrator --runtime claude --channel stable
# Optional: validate & inspect
python scripts/validate.py
python scripts/check-cycles.py
python evals/runner.py
```

> **Entry point for agents:** [`AGENTS.md`](./AGENTS.md) (root registry). Hierarchical `*/AGENTS.md` files improve navigation without duplicating truth. Machine source: [`registry.json`](./registry.json).

## 30-Second Usage

```markdown
# In any agent that reads AGENTS.md:
# 1. Discover
Read AGENTS.md → find skill by trigger (e.g., "security review" → pixz.security.review)

# 2. Resolve dependencies
install orchestrator → aggregates → requires → conflicts? → cycles? → runtime?

# 3. Execute with methodology
Follow that skill's SKILL.md (Purpose, Inputs, Methodology, Verification)
Preserve workflow state via schemas/workflow.schema.json

# 4. Challenge & verify (risk-scaled)
Low-risk rename → minimal challenge; production security → full challenger + quality-gate
```

## Architecture

```
Universal Core (methodology, schemas, contracts — vendor-neutral)
        ↓
Runtime Adapter (thin translation)
        ↓
Runtime-specific representation (.claude/skills/, ~/.openclaw/skills/, etc.)
```

Governing loop: `UNDERSTAND → DISCOVER → PLAN → EXECUTE → INSPECT → CHALLENGE → VERIFY → REPLAN → IMPROVE → VERIFY → SHIP`

28 skills across **core (13) + quality (1) + engineering (2) + security (2) + design (2) + frontend (2) + motion (2) + devops (2) + ai (2)** — intentionally curated (see `docs/taxonomy.md` — taxonomy normalization, anti skill-explosion).

## Skills at a Glance

| Domain | Skills |
|--------|--------|
| **core** | orchestrator, planning, context-engineering, environment-awareness, capability-discovery, workflow-continuity, delegation-handoff, epistemic-reasoning, epistemic-challenger, verification, change-safety, replanning, quality-gate |
| **quality** | anti-ai-slop |
| **engineering / security / design / frontend / motion / devops / ai** | api-design, system-design, review, threat-modeling, uiux, design-system, react, accessibility, gsap, remotion, docker, kubernetes, rag, agent-design |

Each skill: `SKILL.md` (portable methodology) + `metadata.yaml` (machine contract).

## Project Structure

```
AGENTS.md                 # root registry (human + agent)
registry.json             # machine-readable registry
VERSION                   # ecosystem SemVer (1.0.0)
llms.txt                  # LLM-friendly index
schemas/                  # skill, registry, workflow, eval schemas (JSON Schema)
core/ ... quality/ ... engineering/ ...  # 28 skill folders (SKILL.md + metadata.yaml)
adapters/{claude,openclaw,opencode,hermes}/  # runtime translators
scripts/{resolve,validate,check-cycles}.py  # resolver & validation
evals/{runner.py,cases/}  # evaluation harness
examples/                 # basic-usage, orchestrated-task, custom-skill
docs/{architecture,taxonomy,dependency-model,versioning}.md
agents/                   # agent definitions (orchestrator runtime role)
```

## Runtime Adapters

| Adapter | Maps core → | Notes |
|---------|------------|-------|
| `adapters/claude/` | `.claude/skills/` + `CLAUDE.md @AGENTS.md` | progressive disclosure, frontmatter `name/description` |
| `adapters/openclaw/` | `~/.openclaw/skills/` / `<workspace>/skills/` | allowlist `agents.entries.*.skills` (final, non-merging) |
| `adapters/opencode/` | `.opencode/skills/` | generic SKILL.md |
| `adapters/hermes/` | `hermes/skills/` | generic SKILL.md |

See `adapters/README.md` for compatibility differences — core methodology never forks per runtime.

## Versioning

- **IDs stable:** `pixz.<domain>.<name>` — filenames are not identity.
- **Channels:** `latest` (HEAD main) · `stable` (latest `v*.*.*` passing quality-gate) · `pinned` (exact SemVer / SHA)
- **Consumer pins a known-good version** — no silent breaking change (major bump required for contract breaks).

## Contributing

See [`CONTRIBUTING.md`](./CONTRIBUTING.md). New skills must pass the seven standalone criteria (distinct objective, methodology, triggers, I/O, failure conditions, independent value) and taxonomy review — no micro-persona explosion.

## Research

Built after researching official sources: Anthropic Skills spec, AGENTS.md open standard (Agentic AI Foundation), OpenClaw skills loading/allowlist docs, OpenCode/Hermes conventions, `llms.txt` pattern, GitHub agent instruction conventions. See `docs/architecture.md` + `AGENTS.md` research notes and `adapters/README.md` compatibility table.

## License

MIT — see `LICENSE`.

---

*Build the ecosystem, not merely the prompts. Smallest coherent system that makes agents more reliable, transparent, safe and portable.*
