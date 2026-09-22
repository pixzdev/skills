# Installation — PIXZ Skills

> **Source ≠ Install ≠ Discovery ≠ Invocation.** Cloning copies source; installation registers the skill where the runtime discovers it.

## Matrix — Verified Mechanisms Only

| Runtime | Install method | Scope | Installed location | Discovery | Invocation | Update | Verify |
|---------|----------------|-------|--------------------|-----------|------------|--------|--------|
| **skills.sh (Vercel, VERIFIED)** | `npx skills add pixzdev/skills --skill <name>` or `npx skills add pixzdev/skills` (all) | project (`./.claude/skills`, `.agents/skills` etc. auto-detected) or `-g` global (`~/.claude/skills`, `~/.config/opencode/skills`) | agent-specific directory (CLI auto-detects; see `npx skills add --help`) | `npx skills list` | agent loads SKILL.md when `description` matches task; or explicit `/<skill>` if runtime supports slash | `npx skills update` / `npx skills check` | `npx skills list` shows installed; SKILL.md exists at path |
| **Claude Code (VERIFIED)** | `npx skills add pixzdev/skills --skill <name> --agent claude-code` **or** manual `git clone` → copy | project: `.claude/skills/<name>/` (team-shared via git) / global: `~/.claude/skills/<name>/` (personal) | `.claude/skills/<name>/SKILL.md` or `~/.claude/skills/<name>/SKILL.md` | scan at session start; frontmatter `name`/`description` indexed | automatic by task match or slash `/<name>`; `CLAUDE.md` may `@AGENTS.md` | overwrite SKILL.md + restart | `ls ~/.claude/skills/<name>/SKILL.md` && restart → `/skills` shows it |
| **OpenClaw (VERIFIED)** | `openclaw skills install git:pixzdev/skills --skill <name>`? No — use one of: `openclaw skills install skills-sh:pixzdev/skills/<name>` (via skills.sh) <br> `openclaw skills install git:pixzdev/skills@main` (whole repo — then select) <br> `openclaw skills install ./core/orchestrator --as pixz-orchestrator` (local) <br> ClawHub if published: `openclaw skills install @pixzdev/<slug>` | workspace: `./skills/<name>/` / `~/.openclaw/skills/` with `--global` | `<workspace>/skills/<name>/SKILL.md` or `~/.openclaw/skills/<name>/` or `<state-dir>/skills/` | priority: workspace > project .agents/skills > personal ~/.agents/skills > managed > workshop > bundled (see docs/tools/skills.md) | `openclaw skills list` / `openclaw skills check` ; agent loads by description | `openclaw skills update --all` (ClawHub only); else reinstall git/local | `openclaw skills list` + `openclaw skills verify @pixzdev/<slug> --card` |
| **OpenCode (VERIFIED)** | `npx skills add pixzdev/skills --skill <name>` (writes to Claude path, OpenCode reads it) **or** `mkdir -p .opencode/skill/<name> && cp -r core/<name> .opencode/skill/<name>/` **or** global `~/.config/opencode/skill/<name>/` | project: `.opencode/skill/<name>/` (singular `skill` canonical; `skills` plural also scanned) / global | `.opencode/skill/<name>/SKILL.md` or `~/.config/opencode/skill/<name>/SKILL.md` + cross-compatible `.claude/skills/` `/.agents/skills/` | project `.opencode/skills/` + global `~/.config/opencode/skills/` + `.claude/skills/` + `.agents/skills/` walk-up (see `opencode/skills` docs) | same description-match | `cp -r` overwrite | `ls .opencode/skill/<name>/SKILL.md` or `npx skills list` |
| **Hermes (VERIFIED)** | manual `cp -r core/<name> ~/.hermes/skills/<name>/` or `skills/<name>/` project | project: `skills/<name>/` / global: `~/.hermes/skills/<name>/` (`%USERPROFILE%\.hermes\skills\` Win) | `~/.hermes/skills/<name>/SKILL.md` or `skills/<name>/SKILL.md` | `~/.hermes/skills/` is source of truth; hub via `skills.sh`/`/.well-known/skills/` also | description-match on startup; `/learn` for knowledge-base | overwrite folder | `ls ~/.hermes/skills/<name>/SKILL.md`; `/skills` or `/bundles` equivalent |
| **Generic Agent (Codex/Cursor etc., PARTIALLY VERIFIED)** | `npx skills add pixzdev/skills --skill <name>` (writes to `.agents/skills`/`.claude/skills`) **or** `mkdir -p .agents/skills/<name> && cp -r core/<name> .agents/skills/<name>/` | project `.agents/skills/` / global `~/.agents/skills/` | `.agents/skills/<name>/SKILL.md` | read at session start if agent supports AGENTS.md/SKILL.md standard (Agentic AI Foundation) | AGENTS.md-guided | overwrite | `ls .agents/skills/<name>/SKILL.md` |

**Legend:** VERIFIED = tested against official docs + install flow; PARTIALLY VERIFIED = spec exists but not integration-smoked in CI; DOCUMENTED ONLY = cited but not tested; UNKNOWN/UNSUPPORTED = no claim.

For this repo (v1.1.0):
- skills.sh: VERIFIED (Vercel Labs docs, `npx skills` CLI)
- Claude Code: VERIFIED (Anthropic/cld skills docs, `~/.claude/skills` per project/global)
- OpenClaw: VERIFIED (openclaw docs/tools/skills.md, ClawHub, `skills-sh:` and `git:`)
- OpenCode: VERIFIED (opencode docs + addyosmani guide, singular/plural paths)
- Hermes: VERIFIED (NousResearch hermes-agent docs, `~/.hermes/skills/`)
- Generic/Codex/Cursor: PARTIALLY VERIFIED (AGENTS.md standard, cross-compatible paths)

Do not conflate `git clone` with install. Clone gives **source**; install registers it where the runtime discovers it. See `docs/install-as-skill.md` for agent prompt that distinguishes these.

## Quick Start per Runtime

### skills.sh (any agent)
```bash
npx skills add pixzdev/skills --list          # preview 28 skills
npx skills add pixzdev/skills --skill orchestrator   # one skill (folder name)
npx skills add pixzdev/skills                 # all skills (if CLI supports)
npx skills list
npx skills update
```
- Where: CLI auto-picks `~/.claude/skills`, `.opencode/skill`, `.agents/skills` based on detected agents.
- Discovery: CLI writes SKILL.md; agent scans on next start.
- Verify: `npx skills list | grep orchestrator` and `ls ~/.claude/skills/orchestrator/SKILL.md` (or path CLI printed).

### Claude Code
```bash
# via CLI (preferred, VERIFIED)
npx skills add pixzdev/skills --skill orchestrator --agent claude-code

# manual — project (team-shared)
git clone https://github.com/pixzdev/skills /tmp/pixz
mkdir -p .claude/skills/orchestrator
cp -r /tmp/pixz/core/orchestrator/* .claude/skills/orchestrator/
git add .claude/skills/orchestrator && git commit -m "Add pixz orchestrator"

# manual — global (personal)
mkdir -p ~/.claude/skills/orchestrator
cp -r /tmp/pixz/core/orchestrator/* ~/.claude/skills/orchestrator/
# restart Claude Code
ls ~/.claude/skills/orchestrator/SKILL.md
```

### OpenClaw
```bash
# VERIFIED mechanisms (see https://docs.openclaw.ai/tools/skills)
openclaw skills install skills-sh:pixzdev/skills/orchestrator   # via skills.sh listing
openclaw skills install git:pixzdev/skills@main                  # git (whole repo)
openclaw skills install ./core/orchestrator --as pixz-orchestrator  # local dir
openclaw skills install ./core/orchestrator --as pixz-orchestrator --global  # global
openclaw skills list
openclaw skills check
openclaw skills verify pixz-orchestrator --card
# ClawHub (when published): openclaw skills install @pixzdev/orchestrator
```

### OpenCode
```bash
# CLI writes to Claude path — OpenCode reads it (VERIFIED cross-compatible)
npx skills add pixzdev/skills --skill orchestrator
# if it lands in .claude/skills but you want primary path:
mkdir -p .opencode/skill/orchestrator
cp -r .claude/skills/orchestrator/* .opencode/skill/orchestrator/
# or direct:
git clone https://github.com/pixzdev/skills /tmp/pixz
mkdir -p .opencode/skill/orchestrator
cp -r /tmp/pixz/core/orchestrator/* .opencode/skill/orchestrator/
ls .opencode/skill/orchestrator/SKILL.md
```

### Hermes
```bash
git clone https://github.com/pixzdev/skills /tmp/pixz
mkdir -p ~/.hermes/skills/orchestrator
cp -r /tmp/pixz/core/orchestrator/* ~/.hermes/skills/orchestrator/
ls ~/.hermes/skills/orchestrator/SKILL.md
# project alternative:
mkdir -p skills/orchestrator && cp -r /tmp/pixz/core/orchestrator/* skills/orchestrator/
```

## Addressing Multi-Skill Repo

This repo bundles 28 skills. Addressing:

- **skills.sh:** `--skill <folder>` where `<folder>` is the short directory name (`orchestrator`, `planning`, `context-engineering`, etc.) — not the namespaced `pixz.core.orchestrator` ID. The ID is stable for resolver; the CLI uses filesystem path. When in doubt, `npx skills add pixzdev/skills --list` shows available.
- **OpenClaw git/local:** install whole repo or local folder; use `--as <slug>` to avoid collision (e.g., `pixz-orchestrator`).
- **Manual:** copy the skill's folder (`core/orchestrator/` → `~/.claude/skills/orchestrator/`), preserving `SKILL.md` at top level.

## Version / Channel

- `VERSION` file (`1.1.0`) is repo version; per-skill `metadata.yaml:version` (SemVer) is skill version.
- `latest` = `main` HEAD; `stable` = latest `v*.*.*` tag (resolver `--channel stable`).
- `pinned` = `pixz.lock` — **DOCUMENTED ONLY** (future). Resolver accepts flag but does not yet write lockfile.
- For reproducible installs, pin via git SHA: `npx skills add pixzdev/skills#<sha>` or `openclaw skills install git:pixzdev/skills@<sha>`.

## Uninstall

```bash
npx skills remove <skill>  # if CLI supports, or rm -rf <installed path>
rm -rf ~/.claude/skills/orchestrator .claude/skills/orchestrator
openclaw skills uninstall <slug>  # or rm -rf <workspace>/skills/<name>
rm -rf .opencode/skill/orchestrator ~/.config/opencode/skill/orchestrator
rm -rf ~/.hermes/skills/orchestrator skills/orchestrator
```

## Security & Trust

SKILL.md is instructions, not arbitrary code execution, but review `SKILL.md` + `metadata.yaml` + `scripts/` before installing. See `docs/install/README.md#security`.
