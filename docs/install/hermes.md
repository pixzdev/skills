# Install on Hermes — VERIFIED

> Docs: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/features/skills.md

**Manual:**
```bash
git clone https://github.com/pixzdev/skills /tmp/pixz
# global (source of truth):
mkdir -p ~/.hermes/skills/orchestrator
cp -r /tmp/pixz/core/orchestrator/* ~/.hermes/skills/orchestrator/
# project:
mkdir -p skills/orchestrator
cp -r /tmp/pixz/core/orchestrator/* skills/orchestrator/
```

**Hub:** `skills.sh` via `npx skills add https://pixzdev/skills` (serves `/.well-known/skills/` if documented) or `/learn` for large sources (creates knowledge-base skill with `references/`).

**Discovery:** `~/.hermes/skills/` is primary; `skills/` project next. Bundled skills copied on install.

**Verify:** `ls ~/.hermes/skills/orchestrator/SKILL.md`.

**Bundles:** `~/.hermes/skill-bundles/<slug>.yaml` groups skills.
