# Install on OpenCode — VERIFIED

> Docs: https://opencode.ai/docs/skills + https://github.com/addyosmani/agent-skills/blob/main/docs/opencode-setup.md

**Via skills CLI (cross-compatible):**
```bash
npx skills add pixzdev/skills --skill orchestrator
# CLI may write to .claude/skills/ — OpenCode reads it. If so, copy to primary:
mkdir -p .opencode/skill/orchestrator
cp -r .claude/skills/orchestrator/* .opencode/skill/orchestrator/
```

**Direct (canonical singular `skill`):**
```bash
git clone https://github.com/pixzdev/skills /tmp/pixz
# project:
mkdir -p .opencode/skill/orchestrator
cp -r /tmp/pixz/core/orchestrator/* .opencode/skill/orchestrator/
# global:
mkdir -p ~/.config/opencode/skill/orchestrator
cp -r /tmp/pixz/core/orchestrator/* ~/.config/opencode/skill/orchestrator/
```

**Discovery (VERIFIED):** project `.opencode/skill/<name>/SKILL.md` (singular canonical), also scanned: `.opencode/skills/` (plural compat), `~/.config/opencode/skill/`, `~/.config/opencode/skills/`, `.claude/skills/`, `~/.claude/skills/`, `.agents/skills/`, `~/.agents/skills/`. Project overrides global.

**Invocation:** description-match.

**Verify:** `ls .opencode/skill/orchestrator/SKILL.md` or `ls .claude/skills/orchestrator/SKILL.md` (cross-compatible).

**Permissions:** `opencode.json` `permissions` may gate `allow`/`deny`/`ask` per skill.
