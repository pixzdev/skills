# Install on Claude Code — VERIFIED

> Docs: Anthropic Skills + Claude Code, https://docs.anthropic.com/claude-code/skills

**Via skills CLI (preferred):**
```bash
npx skills add pixzdev/skills --skill orchestrator --agent claude-code
npx skills add pixzdev/skills --skill verification --agent claude-code
# or all:
npx skills add pixzdev/skills --agent claude-code
```
Writes to `~/.claude/skills/<name>/SKILL.md` (global) or `.claude/skills/<name>/` (project) depending on `-g`.

**Manual — global (personal, every project):**
```bash
git clone https://github.com/pixzdev/skills /tmp/pixz
mkdir -p ~/.claude/skills/orchestrator
cp -r /tmp/pixz/core/orchestrator/* ~/.claude/skills/orchestrator/
ls ~/.claude/skills/orchestrator/SKILL.md   # must be exactly SKILL.md, case-sensitive
# restart Claude Code
```

**Manual — project (team-shared, committed):**
```bash
mkdir -p .claude/skills/orchestrator
cp -r /tmp/pixz/core/orchestrator/* .claude/skills/orchestrator/
git add .claude/skills/orchestrator
git commit -m "Add pixz orchestrator"
```

**Discovery:** At session start, Claude scans `~/.claude/skills/` then `./.claude/skills/` (project overrides global). Only frontmatter `name`/`description` loaded initially (progressive disclosure); body on relevance; `references/`/`scripts/` on demand. File must be exactly `SKILL.md` (not `skill.md`).

**Invocation:** automatic when request matches `description`, or slash `/orchestrator`. Verify with `/skills` (lists loaded).

**Update:** overwrite SKILL.md + restart.

**Import AGENTS.md:** add to `CLAUDE.md`:
```
@AGENTS.md
```

**Verify:** `ls ~/.claude/skills/orchestrator/SKILL.md && head -20 ~/.claude/skills/orchestrator/SKILL.md` (check `---` frontmatter with `name:` and `description:`).
