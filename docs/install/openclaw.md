# Install on OpenClaw — VERIFIED

> Docs: https://docs.openclaw.ai/tools/skills and https://github.com/openclaw/openclaw/blob/main/docs/tools/skills.md

**Mechanisms (VERIFIED):**

| Source | Command | Scope |
|--------|---------|-------|
| ClawHub (when published) | `openclaw skills install @pixzdev/orchestrator` | workspace (`./skills/`) or `--global` (`~/.openclaw/skills/`) |
| skills.sh listing | `openclaw skills install skills-sh:pixzdev/skills/orchestrator` | workspace / --global |
| Git | `openclaw skills install git:pixzdev/skills@main` (whole repo) or `git:pixzdev/skills@v1.1.0` | workspace / --global |
| Local directory | `openclaw skills install ./core/orchestrator --as pixz-orchestrator` | workspace / --global |

**Discovery order (VERIFIED):** workspace `skills/` > project `.agents/skills/` > personal `~/.agents/skills/` > managed `<state-dir>/skills/` > workshop `.../workshop-skills/` > bundled > extraDirs. `openclaw skills list` shows priority.

**Update:** `openclaw skills update --all` (ClawHub only). For `git:`/local, reinstall: `openclaw skills install git:pixzdev/skills@<new-sha> --as pixz-orchestrator` (overwrites).

**Verify:** `openclaw skills list` ; `openclaw skills check` ; `openclaw skills verify pixz-orchestrator --card` — shows trust envelope + card.

**Project vs global:** default is workspace. Add `--global` for `~/.openclaw/skills/` visible to all agents (unless `agents.entries.*.skills` allowlist narrows it).

**Local install of this repo (recommended for dev):**
```bash
git clone https://github.com/pixzdev/skills /tmp/pixz
openclaw skills install /tmp/pixz/core/orchestrator --as pixz-orchestrator
openclaw skills install /tmp/pixz/core/verification --as pixz-verification --global
```

**Uninstall:** `rm -rf ./skills/pixz-orchestrator ~/.openclaw/skills/pixz-orchestrator` or `openclaw skills uninstall` if CLI supports.

**Security:** See `security.installPolicy` + `openclaw skills verify`. SKILL.md may declare `requires.env`, `requires.config`, `install` specs — verified via gating section in docs.
