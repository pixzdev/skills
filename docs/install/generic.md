# Install on Generic Agent (Codex/Cursor/Gemini etc.) — PARTIALLY VERIFIED

> Spec: AGENTS.md open standard (Agentic AI Foundation); SKILL.md as open format.

**Via CLI:**
```bash
npx skills add pixzdev/skills --skill orchestrator
# lands in .agents/skills/ or .claude/skills/ depending on detected agent
```

**Manual:**
```bash
git clone https://github.com/pixzdev/skills /tmp/pixz
mkdir -p .agents/skills/orchestrator
cp -r /tmp/pixz/core/orchestrator/* .agents/skills/orchestrator/
# global:
mkdir -p ~/.agents/skills/orchestrator
cp -r /tmp/pixz/core/orchestrator/* ~/.agents/skills/orchestrator/
```

**Discovery:** agent reads `AGENTS.md` (project) and scans `.agents/skills/<name>/SKILL.md` at session start. Not all generic agents implement skill loading — check `npx skills list` and agent's docs. Classified **PARTIALLY VERIFIED** because spec exists but smoke not automated here.

**Verify:** `ls .agents/skills/orchestrator/SKILL.md`.
