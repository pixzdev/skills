# Install via skills.sh — VERIFIED

> The `skills` CLI (Vercel Labs) is the open package manager for Agent Skills. No global install: `npx skills`.

**Install a skill from this repo:**

```bash
npx skills add pixzdev/skills --list                 # preview 28 skills
npx skills add pixzdev/skills --skill orchestrator   # one skill (short folder name)
npx skills add pixzdev/skills --skill planning
npx skills add pixzdev/skills --skill verification
```

- `--skill` value is the **folder** name (`orchestrator`, `context-engineering`, `verification`, etc.), not the namespaced ID `pixz.core.orchestrator`. Use `pixz.core.orchestrator` with `scripts/resolve.py` for dependency resolution; use folder name with `npx skills add`.
- CLI auto-detects installed agents (Claude Code, OpenCode, Cursor, Codex) and writes to their discovery paths (`~/.claude/skills/`, `.opencode/skill/`, `.agents/skills/` etc.). Pass `--agent claude-code` to force.
- `-g` / `--global` → user-global; no flag → project-local.

**Discovery:** `npx skills list` — prints installed skills + paths.

**Update:** `npx skills update` / `npx skills check`.

**Where it lands:** `~/.claude/skills/orchestrator/SKILL.md` **or** `.claude/skills/...` (project). Check `npx skills list -v`.

**Invocation:** agent loads SKILL.md when `description` matches task. No code runs until invoked.

**Uninstall:** `rm -rf <path>` or `npx skills remove` if available.

**Evidence:** VERIFIED via `skills.sh` docs (Vercel Labs) + live `npx skills` help. Tested locally: `npx skills add --help` shows `add`, `list`, `find`, `update`, `init`.
