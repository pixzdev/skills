# Runtime Adapters — PIXZ Universal Core → Runtime-Specific

> Universal Core holds methodology. Adapters are thin translators — no methodology duplication.

## Compatibility Differences (researched)

| Concern | Claude (Code) | OpenClaw | OpenCode | Hermes | Generic |
|---------|---------------|----------|----------|--------|---------|
| **Skill file** | `SKILL.md` with YAML frontmatter `name` + `description` | `SKILL.md` similar | `SKILL.md` (generic) | `SKILL.md` (generic) | `SKILL.md` |
| **Discovery** | progressive disclosure: frontmatter always visible, body on relevance, `references/`/`scripts/` on demand | loading order workspace → project/.agents → personal → managed → workshop → bundled | generic import | generic import | read `AGENTS.md` |
| **Install path** | `.claude/skills/<name>/` or project `skills/` | `<workspace>/skills/`, `~/.openclaw/skills/`, `<state-dir>/skills/` | `.opencode/skills/` | `hermes/skills/` | `skills/` |
| **AGENTS.md** | import via `CLAUDE.md: @AGENTS.md` (4-hop limit, <200 lines recommended) | reads `AGENTS.md` natively | reads `AGENTS.md` | reads `AGENTS.md` | reads `AGENTS.md` |
| **Allowlist** | — | `agents.entries.*.skills` is FINAL (non-merging); `agents.defaults.skills` baseline | — | — | — |
| **Hooks/mode** | hooks, bypassPermissions | approvalPolicy, workshop autonomous | — | — | — |
| **Token impact** | per-skill ~97 chars + name/description + XML escaping | similar | similar | similar | — |

Document confirmed via: Anthropic Skills spec, AGENTS.md open standard (Agentic AI Foundation), OpenClaw docs (`/tools/skills`, `/tools/skills-config`).

## Adapter Structure

```
adapters/
  README.md          # this file — compatibility truth
  claude/
    AGENT.md         # Claude-specific wiring (CLAUDE.md import line)
    SKILL_TEMPLATE.md
    install.sh
  openclaw/
    AGENT.md
    clawhub.json
    install.sh
  opencode/
    AGENT.md
    install.sh
  hermes/
    AGENT.md
    install.sh
```

## Translation Principle

```
Core SKILL.md (methodology) 
  → adapter replaces ONLY: install path, import line, frontmatter quota
  → methodology body untouched
```

Adapters must not fork methodology. Validation: `diff` skill body across adapters should show only header/path changes.

## Usage

```bash
# Claude
cp -r core/orchestrator .claude/skills/orchestrator
echo "@AGENTS.md" >> CLAUDE.md

# OpenClaw
openclaw skills install ./core/orchestrator --as pixz-orchestrator
# or: cp -r core/orchestrator ~/.openclaw/skills/pixz-orchestrator

# Generic (OpenCode/Hermes)
cp -r core/orchestrator skills/pixz-orchestrator
```

Resolver validates `compatible_runtimes` before suggesting install path.

## Limits

Adapters enforce from `registry.json#limits`: `max_skill_chain_depth=12`, `max_orchestration_depth=6`, `max_iterations=8`.
