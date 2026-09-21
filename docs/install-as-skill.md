# Install This as a Skill — Agent Prompt

> **Copy-paste this into any AI agent to install a PIXZ skill natively — not just clone.**

**What to copy:**

---

```markdown
You are installing an actual AI Skill, not downloading a repository.

Goal: Install skill `pixz.core.orchestrator` (or the skill named in the user's request) from `pixzdev/skills` into the **current runtime** using its **native** skill mechanism.

You MUST:

1. **Do NOT merely clone** `https://github.com/pixzdev/skills`. Do NOT merely inspect README/AGENTS.md. Do NOT cite installation as complete after cloning.

2. **Detect runtime.** Run capability discovery first: which agent/runtime are you? Check for:
   - `claude` (look for `.claude/skills` or `CLAUDE.md` or `npx skills --help`)
   - `openclaw` (`openclaw --help`, `~/.openclaw/skills`, `openclaw skills list`)
   - `opencode` (`.opencode/skill` or `.config/opencode/skill` or `opencode --help`)
   - `hermes` (`~/.hermes/skills` or `hermes --help`)
   - generic (`.agents/skills`, `npx skills --help`)
   Report detected runtime with evidence (path exists, command output).

3. **Discover native mechanism.** Read `docs/install/README.md` matrix for that runtime; verify the exact install syntax from official docs (never invent). Prefer `npx skills add` for skills.sh-compatible runtimes; use `openclaw skills install` on OpenClaw; use file copy to `<runtime>/skills/` if CLI unavailable.

4. **Identify skill.** Find the requested skill in this repo: `registry.json` → `path` → `SKILL.md`. Default if unspecified is `pixz.core.orchestrator` at `core/orchestrator/SKILL.md`. Confirm `name`/`description` frontmatter.

5. **Install via native mechanism.** Examples (use the one matching detected runtime):
   - skills.sh: `npx skills add pixzdev/skills --skill orchestrator`
   - Claude Code: `npx skills add pixzdev/skills --skill orchestrator --agent claude-code` or `mkdir -p ~/.claude/skills/orchestrator && cp -r core/orchestrator/* ~/.claude/skills/orchestrator/`
   - OpenClaw: `openclaw skills install ./core/orchestrator --as pixz-orchestrator` or `openclaw skills install skills-sh:pixzdev/skills/orchestrator`
   - OpenCode: `mkdir -p .opencode/skill/orchestrator && cp -r core/orchestrator/* .opencode/skill/orchestrator/`
   - Hermes: `mkdir -p ~/.hermes/skills/orchestrator && cp -r core/orchestrator/* ~/.hermes/skills/orchestrator/`
   Report exact command executed and its stdout/stderr.

6. **Verify runtime recognizes it.**
   - `npx skills list` must show it (if skills.sh)
   - `openclaw skills list` / `openclaw skills check` / `openclaw skills verify pixz-orchestrator --card`
   - `ls ~/.claude/skills/orchestrator/SKILL.md` + restart check
   - `ls .opencode/skill/orchestrator/SKILL.md`
   - `ls ~/.hermes/skills/orchestrator/SKILL.md`
   Paste discovery output. If discovery fails, explain why and do NOT claim success.

7. **Invoke / load skill.** Read the installed `SKILL.md` (from installed location, not source) and execute its **verification** smoke from its `Methodology` (e.g., orchestrator: `python scripts/resolve.py --install pixz.core.orchestrator --runtime <detected>`).

8. **Report — do not fabricate:**

```
SKILL INSTALLATION REPORT
Runtime: <detected, evidence>
Skill: pixz.core.orchestrator (pixzdev/skills@<sha or VERSION>)
Source: pixzdev/skills/<path>
Installation: SUCCESS | FAILED — <reason, command, output>
Installed location: <actual path verified by ls>
Discovery: PASS | FAIL — <list/check output>
Invocation: PASS | FAIL — <how you invoked, what happened>
Smoke test: PASS | FAIL — <command + result>
Version/ref: <git SHA, VERSION file, or metadata.yaml:version>
Notes: <limitations, next steps, was fallback used?>
```

9. **If native install unavailable,** explain exactly why (missing CLI, permissions, no runtime support) and provide the nearest manual copy command. Do NOT silently fall back to `git clone`.

10. **Distinguish:** source checkout (`git clone`) ≠ skill installation (registers in `<runtime>/skills/`). Never claim installation succeeded without verification in step 6–7.

Failure is an acceptable outcome if you report it honestly with evidence. Fabrication is not.
```

---

**For the user:** replace `pixz.core.orchestrator` with any ID from `registry.json` / `AGENTS.md` (e.g., `pixz.security.review`, `pixz.quality.anti-ai-slop`).

**See full runtime-adaptive version:** `docs/prompts/install-skill-agent.md` (includes routing tests and portability table).
